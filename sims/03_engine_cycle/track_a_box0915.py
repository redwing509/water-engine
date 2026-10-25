"""Track A, Claude job water-engine-box-20261025-0915, steps 4 (coupled water-majority cases at their own
knock-limited CR) and 5 (port-wall temperature sensitivity of the bound-(i) film and the Module 11 misfire flag).

Run:  python -m sims.03_engine_cycle.track_a_box0915 run [--workers 4]
      python -m sims.03_engine_cycle.track_a_box0915 report

Model = the PR #8 coupled retained-liquid model (coupled_dual_temp.py task(); bound (ii) film-carried liquid sink,
bound (i) port-evaporated film capped by the Module 06 exhaust-heat surplus, the port-wall film capacity and
saturation), with Module 03's own SPEC phasing (default 2-CAD retard search) and SPEC eligibility.
  fuels      CH3OH, C2H5OH;   w 0.5, 0.6, 0.7;   CR 9 .. 24 (integer);   regimes as coupled_dual_temp.REGIMES
             (normal: chamber wall 450 K, port wall 363.15 K, T_intake 360 K; hot: 520 K, 388.15 K, 400 K)
  intake     dryair     : Module 09 ultrasonic_120kHz / nominal spray into dry air (PointProfile pinned to the
                          water_majority design point CR 24 / w 0.6 / 360 K - CAVEAT: Module 09 fractions are only
                          available at the design points, so w 0.5 / 0.7 and CR != 24 reuse that point's
                          fractions; the bound-(i) film deposit is scaled with the trapped water/fuel masses).
             humid_evap : water aerosolised into the intake air and evaporated before IVC (f_evap_intake = 1,
                          saturation/wet-bulb capped).  Water left liquid by saturation is a fine mist:
                          bound (ii) = it stays liquid to spark (liquid sink from IVC, spark at the Module 09
                          spark angle), bound (i) = it evaporates in-cylinder on the Module 03 schedule
                          (saturation capped) until first heat release, the rest is a liquid sink.
  port wall  step 5: 363.15 / 375.0 / 388.15 K at w 0.5, both regimes, dryair intake (bound (i) capacity and the
             Module 11 flag change; bound (ii) is port-wall independent).
Film capacity: sims/03_engine_cycle/port_film.py (vendored wme1-hiT budget; reproduces port_film_wall_T.csv
exactly at the design points), L_wet 0.05 m, h_film 3e4 W/m2K, plenum 360 K normal / 400 K hot.
Module 11 misfire flag (wme1-spray11 63815e6 definition): misfire reachable <=> X_strip_max = 1 - f_film_evap
>= x_crit(MIE 100 mJ) for 200/350/500 um film drops; x_crit of the water_majority design point
(results/track_a_box/inputs/m11_film_water_majority.json).  Status: EXECUTED; NOT validated.
"""
import argparse
import csv
import importlib
import json
import math
import sys
import time
from dataclasses import replace
from multiprocessing import get_context
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
OUT = REPO / "results" / "track_a_box"
M11 = OUT / "inputs" / "m11_film_water_majority.json"
FUELS = ("CH3OH", "C2H5OH")
WS = (0.5, 0.6, 0.7)
CRS = tuple(range(9, 25))
# Dry-only low-CR extension (added 2026-10-25 13:50 PDT, report pass): CH3OH hot has no SPEC-eligible dry point at
# CR 9-24 (Track B found its dry knock limit at CR 8), so every CH3OH-hot wet row had no baseline. New points only;
# no existing point is re-run (run() skips specs already in points.jsonl).
DRY_LOW_CRS = (6, 7, 8)
# Extension (added 2026-10-25 14:20 PDT, Grok Bot selfdir-1410 job, Track A): with the M03-CRN integrator fixed,
# the best wet rows (CH3OH hot/normal humid_evap w 0.5) and the C2H5OH normal dry baseline sit at CR 24 = TOP of the
# grid, i.e. grid-capped, not knock-limited.  New points only (run() skips specs already in points.jsonl):
#   CR 25..30 for dry (both T), humid_evap w 0.4-0.7 and dryair w 0.5-0.7 (dryair reuses the CR-24 Module 09 point,
#   so CR > 24 dryair is an extrapolation of the Module 09 fractions - caveat);
#   w refinement 0.4 / 0.45 / 0.55 for humid_evap on CR 9..24.
EXT_CRS = tuple(range(25, 31))
WS_REFINE = (0.4, 0.45, 0.55)
ATOM, VAR, POINT = "ultrasonic_120kHz", "nominal", "water_majority"
PORT_WALLS = (363.15, 375.0, 388.15)
T_INTAKE = {"normal": 360.0, "hot": 400.0}
DRY_T = {"normal": (320.0, 360.0), "hot": (400.0,)}
PLENUM = {"normal": 360.0, "hot": 400.0}
SMDS = ("200", "350", "500")


def _mods():
    C = importlib.import_module("sims.03_engine_cycle.coupled_dual_temp")
    m, ep = C._load()
    P = importlib.import_module("sims.03_engine_cycle.port_film")
    return C, m, ep, P


def film_deposit(fuel, row):
    d = json.loads(M11.read_text())["cases"][f"{fuel}/{POINT}/{ATOM}/{VAR}"]
    sa = float(row["fuel_mass_kg"]) / d["m_fuel_kg"]
    sw = float(row["water_mass_kg"]) / d["m_water_kg"]
    return d["film_alcohol_kg"] * sa, d["film_water_kg"] * sw, d


def misfire(fuel, row, T_wall, T_gas):
    P = importlib.import_module("sims.03_engine_cycle.port_film")
    da, dw, d = film_deposit(fuel, row)
    ca, cw, rg = P.capacity(da, dw, fuel, T_wall, T_gas, 0.05, 3.0e4)
    fa, fw = min(1.0, ca / da), min(1.0, cw / dw)
    x = 1.0 - (fa * da + fw * dw) / (da + dw)
    out = dict(film_deposit_mg=1e6 * (da + dw), film_capacity_mg=1e6 * (ca + cw), X_strip_max=x, film_regime=rg)
    for s in SMDS:
        xc = d[f"x_crit_SMD{s}"]
        out[f"misfire_SMD{s}"] = bool(xc not in (None, "never") and x >= float(xc))
    return out


def coupled_dryair(C, m, ep, P, spec):
    """PR #8 coupled_dual_temp.task() logic, with film capacity from the vendored budget at spec port_wall_K."""
    ign, fl = C._fits(m)
    fuel, regime, cr, w, T = spec["fuel"], spec["regime"], spec["CR"], spec["w"], spec["T_intake_K"]
    par = C.regime_par(m, regime)
    prof = ep.PointProfile(ATOM, VAR, POINT)
    f_ivc = prof.ivc_fraction(fuel)
    spark_deg, (f_ev, f_air, f_wall) = prof.spark_target(fuel, cr, w, T)
    m09 = dict(m09_spark_deg=spark_deg, m09_frac_ivc=f_ivc, m09_frac_evap_spark=f_ev,
               m09_frac_airborne_spark=f_air, m09_frac_wall_film_spark=f_wall)
    coup = dict(liquid_sink=True, intake_cap_frac=f_ivc)
    t0 = time.time()
    rows = []
    res = m.run_point(fuel, cr, w, T, ign[fuel], fl[fuel], par, "full", evap_profile=prof, coupling=coup)
    if not spec.get("bound_i_only"):
        rows.append(dict(bound="ii", res=res, extra=dict(m09, runtime_s=time.time() - t0)))
    if res["evo"] is None:
        return rows
    da, dw, _ = film_deposit(fuel, res["point"])
    ca, cw, _ = P.capacity(da, dw, fuel, spec["port_wall_K"], PLENUM[regime], 0.05, 3.0e4)
    cap = ca + cw
    f_pe, it, hist, evo, prow, res1, limit = None, 0, [], res["evo"], res["point"], res, ""
    while it < 4:
        it += 1
        b = C.heat_budget(m, fuel, prow, evo)
        mw = float(prow["water_mass_kg"])
        f_budget = max(0.0, b["surplus_J"]) / b["water_per_frac_J"] if b["water_per_frac_J"] > 0 else 0.0
        f_cap = cap / mw
        f_new = max(0.0, min(f_wall, f_budget, f_cap))
        limit = min((("wall_film", f_wall), ("module06_heat", f_budget), ("port_wall_capacity", f_cap)),
                    key=lambda kv: kv[1])[0]
        hist.append(dict(iteration=it, f_budget=f_budget, f_cap=f_cap, f_port=f_new))
        if f_pe is not None and abs(f_new - f_pe) < 0.002:
            break
        f_pe = f_new
        r1 = m.run_point(fuel, cr, w, T, ign[fuel], fl[fuel], par, "full", evap_profile=prof,
                         coupling=dict(coup, port_evap_frac=f_pe))
        res1 = r1
        if r1["evo"] is None:
            break
        evo, prow = r1["evo"], r1["point"]
    rows.append(dict(bound="i", res=res1, extra=dict(m09, iteration=it, port_evap_request=f_pe, port_limit=limit,
                                                      film_capacity_cycle_mg=cap * 1e6, f_cap=hist[-1]["f_cap"],
                                                      f_budget=hist[-1]["f_budget"], budget_history=json.dumps(hist),
                                                      runtime_s=time.time() - t0)))
    return rows


def humid(C, m, ep, spec):
    ign, fl = C._fits(m)
    fuel, regime, cr, w, T = spec["fuel"], spec["regime"], spec["CR"], spec["w"], spec["T_intake_K"]
    par = replace(C.regime_par(m, regime), f_evap_intake=1.0)
    spark_deg = ep.PointProfile(ATOM, VAR, POINT).spark_target(fuel, cr, w, T)[0]
    rows = []
    t0 = time.time()
    r2 = m.run_point(fuel, cr, w, T, ign[fuel], fl[fuel], par, "full",
                     evap_profile=ep.SyntheticProfile(0.0, spark_deg), coupling=dict(liquid_sink=True))
    rows.append(dict(bound="ii", res=r2, extra=dict(m09_spark_deg=spark_deg, runtime_s=time.time() - t0)))
    t0 = time.time()
    r1 = m.run_point(fuel, cr, w, T, ign[fuel], fl[fuel], par, "full", coupling=dict(liquid_sink=True))
    rows.append(dict(bound="i", res=r1, extra=dict(runtime_s=time.time() - t0)))
    return rows


def task(spec):
    C, m, ep, P = _mods()
    base = dict(step=spec["step"], kind=spec["kind"], intake=spec.get("intake", ""), fuel=spec["fuel"],
                regime=spec["regime"], chamber_wall_K=C.REGIMES[spec["regime"]]["chamber_wall_K"],
                port_wall_K=spec.get("port_wall_K", C.REGIMES[spec["regime"]]["port_wall_K"]),
                atomiser=ATOM if spec.get("intake") == "dryair" else "", variant=VAR if spec.get("intake") == "dryair" else "")
    try:
        if spec["kind"] == "dry":
            ign, fl = C._fits(m)
            t0 = time.time()
            res = m.run_point(spec["fuel"], spec["CR"], 0.0, spec["T_intake_K"], ign[spec["fuel"]], fl[spec["fuel"]],
                              C.regime_par(m, spec["regime"]), "full")
            items = [dict(bound="", res=res, extra=dict(runtime_s=time.time() - t0))]
        elif spec["intake"] == "dryair":
            items = coupled_dryair(C, m, ep, P, spec)
        else:
            items = humid(C, m, ep, spec)
    except Exception as exc:  # recorded, never retried blindly
        return [dict(base, CR=spec["CR"], w=spec["w"], status="failed", reason=f"{type(exc).__name__}: {exc}")]
    out = []
    for it in items:
        p = it["res"]["point"]
        r = dict(base, bound=it["bound"])
        r.update({k: p.get(k) for k in C.KEEP})
        r.update(it["extra"])
        r["eligible"] = bool(p.get("status") == "computed" and m.eligible(p, C.regime_par(m, spec["regime"])))
        if spec["kind"] == "coupled" and spec["intake"] == "dryair" and p.get("status") == "computed":
            r.update(misfire(spec["fuel"], p, r["port_wall_K"], PLENUM[spec["regime"]]))
        out.append({k: (float(v) if hasattr(v, "dtype") else v) for k, v in r.items()})
    return out


def specs():
    out = []
    for regime in ("normal", "hot"):
        pw = 363.15 if regime == "normal" else 388.15
        for fuel in FUELS:
            for cr in CRS:
                for T in DRY_T[regime]:
                    out.append(dict(step=4, kind="dry", fuel=fuel, regime=regime, CR=cr, w=0.0, T_intake_K=T))
                for w in WS:
                    for intake in ("dryair", "humid_evap"):
                        out.append(dict(step=4, kind="coupled", intake=intake, fuel=fuel, regime=regime, CR=cr, w=w,
                                        T_intake_K=T_INTAKE[regime], port_wall_K=pw))
                for T_pw in PORT_WALLS:
                    if abs(T_pw - pw) > 1e-6:
                        out.append(dict(step=5, kind="coupled", intake="dryair", fuel=fuel, regime=regime, CR=cr,
                                        w=0.5, T_intake_K=T_INTAKE[regime], port_wall_K=T_pw, bound_i_only=True))
        for fuel in FUELS:
            for cr in EXT_CRS:
                for T in DRY_T[regime]:
                    out.append(dict(step=4, kind="dry", fuel=fuel, regime=regime, CR=cr, w=0.0, T_intake_K=T))
                for w in sorted(set(WS) | set(WS_REFINE)):
                    for intake in ("dryair", "humid_evap"):
                        if intake == "dryair" and w not in WS:
                            continue
                        out.append(dict(step=4, kind="coupled", intake=intake, fuel=fuel, regime=regime, CR=cr, w=w,
                                        T_intake_K=T_INTAKE[regime], port_wall_K=pw))
            for cr in CRS:
                for w in WS_REFINE:
                    out.append(dict(step=4, kind="coupled", intake="humid_evap", fuel=fuel, regime=regime, CR=cr, w=w,
                                    T_intake_K=T_INTAKE[regime], port_wall_K=pw))
        for fuel in FUELS:
            for cr in DRY_LOW_CRS:
                for T in DRY_T[regime]:
                    out.append(dict(step=4, kind="dry", fuel=fuel, regime=regime, CR=cr, w=0.0, T_intake_K=T))
    return sorted(out, key=lambda s: (s["kind"] == "dry", -s["CR"]))


def key(s):
    return (s["step"], s["kind"], s.get("intake", ""), s["fuel"], s["regime"], float(s["CR"]), float(s["w"]),
            float(s["T_intake_K"]), float(s.get("port_wall_K", 0.0)))


def run(workers):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "points.jsonl"
    done = set()
    if path.exists():
        for l in open(path):
            done.add(tuple(json.loads(l)["_spec"]))
    sp = [s for s in specs() if list(key(s)) not in [list(d) for d in done]]
    print(f"{len(sp)} specs ({len(done)} done)", flush=True)
    with get_context("spawn").Pool(workers) as pool, open(path, "a") as fh:
        for i, (s, rows) in enumerate(zip(sp, pool.imap(task, sp))):
            fh.write(json.dumps(dict(_spec=list(key(s)), rows=rows), default=float) + "\n"); fh.flush()
            print(f"{i + 1}/{len(sp)} " + " ".join(str(x) for x in key(s)) + " | " + " ".join(
                f"{r.get('intake') or 'dry'}:{r.get('bound')}:{(r.get('gross_indicated_efficiency') or 0):.4f}"
                f"{'E' if r.get('eligible') else ''}" for r in rows), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "report", "smoke"])
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    if a.cmd == "run":
        run(min(4, a.workers))
    elif a.cmd == "smoke":
        for s in (dict(step=4, kind="coupled", intake="humid_evap", fuel="CH3OH", regime="normal", CR=16, w=0.5,
                       T_intake_K=360.0, port_wall_K=363.15),
                  dict(step=4, kind="coupled", intake="dryair", fuel="CH3OH", regime="normal", CR=16, w=0.5,
                       T_intake_K=360.0, port_wall_K=363.15)):
            t = time.time()
            for r in task(s):
                print(r.get("intake"), r.get("bound"), r.get("status"), r.get("reason"), r.get("gross_indicated_efficiency"),
                      r.get("ca50_used_deg"), r.get("eligible"), r.get("f_evap_intake_effective"),
                      r.get("evaporated_fraction_spark"), r.get("port_evap_fraction"), r.get("port_limit"),
                      r.get("X_strip_max"), r.get("misfire_SMD350"), r.get("runtime_s"))
            print("t", time.time() - t)
    else:
        importlib.import_module("sims.03_engine_cycle.track_a_box0915_report").main()
