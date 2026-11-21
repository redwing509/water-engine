"""Dry-evap baseline check of the PR 10 hot-regime gains (Claude job water-engine-dryevap-baseline-20261025-1420).

Question: are the PR 10 gains (Track A step 4, Track B B2/B4) partly an artefact of an unfair dry baseline, i.e. one
that never gets intake evaporative cooling while the humid_evap wet rows do?

Step-1 finding (code): humid_evap (par f_evap_intake=1, coupling liquid_sink) evaporates ONLY the water vector; the
fuel is always premixed vapour at T_intake with its latent heat debited from the release (no fuel charge cooling),
and for w = 0 _intake() returns e = base and T_IVC = T_intake. So 'run_point(w=0, f_evap_intake=1, liquid_sink)' is
bit-identical to the old dry row (variant LIT below proves it). A meaningful dry-evap baseline therefore needs the
new optional fuel-evaporation keys of Module 03 (run.py Charge, coupling 'fuel_evap_intake' / 'fuel_evap_port'):

  DEI  dry-evap, intake: all fuel enters as liquid at 298 K and evaporates in the intake air before IVC (charge
       cooling, capped at the fuel dew point at T_IVC), release = vapour LHV (latent paid by the charge). PRIMARY.
       Matches the humid_evap (f_evap_intake=1) wet-row treatment of the water.
  DEP  dry-evap, port: all fuel evaporated off the port wall (latent paid by wall/exhaust heat, no charge cooling,
       vapour at T_intake), release = vapour LHV. Matches the dryair (port-evaporation, Module 06 heat) wet rows.
  LIT  literal job wording: f_evap_intake=1.0 + liquid_sink at w=0, no fuel keys (proof that it equals old dry).

Symmetric re-runs: the PR 10 wet rows again with the SAME fuel treatment (humid_evap + DEI keys, dryair + DEP keys,
Track B liquid/humid chains + DEI keys), so 'wet-sym vs DEI/DEP' isolates the water effect.
M03-CRN gets the same latent credit (Case.fuel_latent_credit = evaporated fuel fraction).

    python -m sims.03_engine_cycle.dryevap_baseline run --workers 4
    python -m sims.03_engine_cycle.dryevap_baseline smoke
"""
import argparse
import importlib
import json
import sys
import time
from multiprocessing import get_context
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "results" / "dryevap"
VARIANTS = {"DEI": dict(fuel_evap_intake=1.0), "DEP": dict(fuel_evap_port=1.0), "LIT": {}}
EXTRA_KEEP = ["fuel_evap_intake_fraction", "fuel_evap_port_fraction", "fuel_evap_saturation_limited",
              "fuel_evaporation_intake_J", "released_lhv_J_per_kg", "fuel_vapour_saturation_ratio_IVC", "knock_limited"]
TA_FUELS = ("CH3OH", "C2H5OH")
TA_DRY_T = {"normal": (320.0, 360.0), "hot": (400.0,)}
TB_FUELS = ("CH3OH", "C2H5OH", "PRF87", "E85")
TB_T = {"normal": 320.0, "hot": 400.0}          # Track B chains: normal 320 K (sims/track_b chain files), hot 400 K
CR_DRY = tuple(float(c) for c in range(6, 25))
CR_B = tuple(sorted(set(CR_DRY) | {9.0 + 0.5 * i for i in range(15)}))
WET_SYM = {"humid_evap": "DEI", "dryair": "DEP", "liquid": "DEI"}

_W = {}


def _init():
    m = importlib.import_module("sims.03_engine_cycle.run")
    _W["m"], _W["rs"], _W["rp"] = m, m.retard_search, m.run_point
    _W["extra"] = {}

    def rp(*a, evap_profile=None, coupling=None, **k):
        if _W["extra"]:
            c = dict(coupling) if coupling else (dict(liquid_sink=True) if evap_profile is not None else {})
            c.update(_W["extra"])
            coupling = c
        return _W["rp"](*a, evap_profile=evap_profile, coupling=coupling, **k)
    m.run_point = rp


def _set(track, extra):
    m = _W["m"]
    _W["extra"] = dict(extra)
    if track == "A":
        m.retard_search = _W["rs"]
    else:
        R = importlib.import_module("sims.track_b.run")
        R.module03()
        m.retard_search = R.spark_optimise
        if not getattr(R, "_dryevap_keep", False):
            R.KEEP = list(R.KEEP) + [k for k in EXTRA_KEEP if k not in R.KEEP]
            R._dryevap_keep = True


def crn_case(r, track):
    """M03-CRN case from a Module 03 row with the same fuel latent credit."""
    E = importlib.import_module("sims.track_b.run").crn_engine() if track == "B" else importlib.import_module("engines.m03_cantera.engine")
    f = lambda k: float(r[k])
    kw = {}
    if track == "A" and r.get("kind") == "coupled":
        kw = dict(evap_mode="coupled", spark_deg=f("liquid_freeze_deg"), f_ivc=min(1.0, f("f_evap_intake_effective")),
                  f_spark=min(1.0, f("evaporated_fraction_spark")))
    credit = float(r.get("fuel_evap_intake_fraction") or 0.0) + float(r.get("fuel_evap_port_fraction") or 0.0)
    t = time.time()
    try:
        c = E.run_case(E.Case(fuel=r["fuel"], cr=f("CR"), T_ivc=f("T_IVC_K"), m_fuel=f("fuel_mass_kg"), m_air=f("air_mass_kg"),
                              m_residual=f("residual_mass_kg"), m_water=f("water_mass_kg"),
                              e_intake=f("f_evap_intake_effective"), ca50_deg=f("ca50_used_deg"),
                              d1090_deg=f("burn_10_90_deg"), wall_T=f("chamber_wall_K"), heat_transfer="woschni",
                              fuel_latent_credit=credit, **kw))
        out = dict(crn_status="ok", crn_efficiency=c["efficiency"], crn_p_max_Pa=c["p_max_Pa"], crn_latent_credit=credit)
    except Exception as exc:  # recorded, never retried blindly
        out = dict(crn_status=f"failed: {type(exc).__name__}: {exc}", crn_latent_credit=credit)
    out["crn_seconds"] = time.time() - t
    if out["crn_status"] == "ok":
        d = 100 * (out["crn_efficiency"] - r["gross_indicated_efficiency"])
        pr = out["crn_p_max_Pa"] / r["peak_pressure_Pa"]
        out.update(d_eta_pp_crn=d, pmax_ratio_crn=pr, c1_pass=bool(abs(d) <= 1.5 and abs(pr - 1) <= 0.05))
    return out


def job(t):
    if not _W:
        _init()
    t0 = time.time()
    if t["track"] == "A":
        A = importlib.import_module("sims.03_engine_cycle.track_a_box0915")
        C = importlib.import_module("sims.03_engine_cycle.coupled_dual_temp")
        if not getattr(C, "_dryevap_keep", False):
            C.KEEP = list(C.KEEP) + [k for k in EXTRA_KEEP if k not in C.KEEP]
            C._dryevap_keep = True
        _set("A", VARIANTS[t["variant"]])
        spec = dict(t["spec"])
        par_patch = None
        if t["variant"] == "LIT":
            # literal job wording: humid_evap settings (f_evap_intake=1, liquid_sink) on the w=0 point
            m, ign_fl = _W["m"], C._fits(_W["m"])
            from dataclasses import replace
            par = replace(C.regime_par(m, spec["regime"]), f_evap_intake=1.0)
            res = m.run_point(spec["fuel"], spec["CR"], 0.0, spec["T_intake_K"], ign_fl[0][spec["fuel"]], ign_fl[1][spec["fuel"]],
                              par, "full", coupling=dict(liquid_sink=True))
            p = res["point"]
            rows = [dict({k: p.get(k) for k in C.KEEP}, kind="dry", regime=spec["regime"], step=4, intake="", bound="",
                         chamber_wall_K=par.wall_T_K, eligible=bool(p["status"] == "computed" and m.eligible(p, par)))]
        else:
            rows = A.task(spec)
        for r in rows:
            r.update(track="A", variant=t["variant"], job_seconds=time.time() - t0)
        return [{k: (float(v) if hasattr(v, "dtype") else v) for k, v in r.items()} for r in rows]
    # Track B
    R = importlib.import_module("sims.track_b.run")
    B = importlib.import_module("sims.track_b.box0915")
    _set("B", VARIANTS[t["variant"]])
    ign = R._FITS[0]
    saved = ign.get(t["fuel"])
    if t["crit"] == "DE":
        ign[t["fuel"]] = B.de_fit(t["fuel"])
    try:
        r = R.point(t["fuel"], t["regime"], t["CR"], t["T"], t["w"], t["mode"])
    except Exception as exc:
        r = dict(status="failed", reason=f"{type(exc).__name__}: {exc}", fuel=t["fuel"], CR=t["CR"], w=t["w"])
    finally:
        ign[t["fuel"]] = saved
    r.update(track="B", variant=t["variant"], criterion=t["crit"], chain=t.get("chain", ""), kind=t["kind"],
             m03_seconds=time.time() - t0)
    if r.get("status") == "computed":
        r.update(crn_case(r, "B"))
    return [{k: (float(v) if hasattr(v, "dtype") else v) for k, v in r.items()}]


def jobs():
    A = importlib.import_module("sims.03_engine_cycle.track_a_box0915")
    B = importlib.import_module("sims.track_b.box0915")
    j = []
    # 0) LIT proof points (old dry best rows)
    for fuel, regime, cr, T in (("CH3OH", "hot", 8, 400.0), ("C2H5OH", "hot", 11, 400.0), ("CH3OH", "normal", 16, 320.0)):
        j.append(dict(track="A", variant="LIT", phase=0, spec=dict(step=4, kind="dry", fuel=fuel, regime=regime, CR=cr,
                                                                   w=0.0, T_intake_K=T)))
    # 1) Track A dry-evap baselines
    for v in ("DEI", "DEP"):
        for regime in ("hot", "normal"):
            for fuel in TA_FUELS:
                for T in TA_DRY_T[regime]:
                    for cr in CR_DRY:
                        j.append(dict(track="A", variant=v, phase=1, spec=dict(step=4, kind="dry", fuel=fuel, regime=regime,
                                                                               CR=int(cr), w=0.0, T_intake_K=T)))
    # 2) Track B dry-evap baselines (DEI both criteria for alcohols, LW only for blends (LW = DE fits there);
    #    DEP LW only)
    for v in ("DEI", "DEP"):
        for regime in ("hot", "normal"):
            for fuel in TB_FUELS:
                crits = ("LW", "DE") if (v == "DEI" and fuel in ("CH3OH", "C2H5OH")) else ("LW",)
                for crit in crits:
                    for cr in CR_B:
                        chain_combo = (fuel, regime) in (("CH3OH", "hot"), ("C2H5OH", "hot"), ("CH3OH", "normal"),
                                                         ("PRF87", "normal"))
                        j.append(dict(track="B", variant=v, phase=2 if (v == "DEI" and chain_combo) else 6, kind="dry", fuel=fuel, regime=regime, T=TB_T[regime],
                                      CR=cr, w=0.0, crit=crit, mode="liquid"))
    # 3) symmetric wet re-runs, hot first: Track A step-4 rows, Track B chain best-w rows
    specs = [s for s in A.specs() if s["step"] == 4 and s["kind"] == "coupled"]
    for regime in ("hot", "normal"):
        for s in specs:
            if s["regime"] == regime:
                j.append(dict(track="A", variant=WET_SYM[s["intake"]], phase=3 if regime == "hot" else 7, spec=s))
        if regime == "hot":
            for name, ch in B.CHAINS.items():
                dry, best, _ = B.chain_best(name)
                crits = ("LW", "DE") if ch["fuel"] in ("CH3OH", "C2H5OH") else ("LW",)
                for crit in crits:
                    for cr in B.CR_GRID:
                        j.append(dict(track="B", variant=WET_SYM[ch["mode"]], phase=4, kind="wet", chain=name, fuel=ch["fuel"],
                                      regime=ch["regime"], T=float(dry["T_intake_K"]), CR=cr, w=float(best["w"]),
                                      crit=crit, mode=ch["mode"]))
    return sorted(j, key=lambda t: (t["phase"], -(t.get("CR") or t.get("spec", {}).get("CR"))))


def jkey(t):
    return json.dumps({k: v for k, v in t.items() if k != "phase"}, sort_keys=True)


def run(workers, phases=None, out="points.jsonl"):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / out
    done = set()
    for f in OUT.glob("points*.jsonl"):
        for l in open(f):
            done.add(json.loads(l)["_job"])
    todo = [t for t in jobs() if jkey(t) not in done and (phases is None or t["phase"] in phases)]
    print(f"{len(todo)} jobs ({len(done)} done)", flush=True)
    t0 = time.time()
    with get_context("spawn").Pool(workers) as pool, open(path, "a") as fh:
        for i, (t, rows) in enumerate(zip(todo, pool.imap(job, todo))):
            fh.write(json.dumps(dict(_job=jkey(t), phase=t["phase"], rows=rows), default=float) + "\n"); fh.flush()
            r = rows[-1]
            print(f"{i + 1}/{len(todo)} {time.time() - t0:.0f}s ph{t['phase']} {t['track']} {t['variant']} {r.get('fuel')} "
                  f"{r.get('regime')} CR={r.get('CR')} w={r.get('w')} T_IVC={r.get('T_IVC_K')} "
                  f"g={r.get('fuel_evap_intake_fraction')} eta={r.get('gross_indicated_efficiency')} ca50={r.get('ca50_used_deg')} "
                  f"elig={r.get('eligible')} {r.get('status')} {r.get('reason') or ''}", flush=True)


def smoke():
    for t in (dict(track="A", variant="LIT", spec=dict(step=4, kind="dry", fuel="CH3OH", regime="hot", CR=8, w=0.0, T_intake_K=400.0)),
              dict(track="A", variant="DEI", spec=dict(step=4, kind="dry", fuel="CH3OH", regime="hot", CR=12, w=0.0, T_intake_K=400.0)),
              dict(track="A", variant="DEP", spec=dict(step=4, kind="dry", fuel="CH3OH", regime="hot", CR=8, w=0.0, T_intake_K=400.0)),
              dict(track="B", variant="DEI", kind="dry", fuel="PRF87", regime="normal", T=320.0, CR=9.0, w=0.0, crit="LW", mode="liquid"),
              dict(track="B", variant="DEI", kind="dry", fuel="E85", regime="hot", T=400.0, CR=12.0, w=0.0, crit="LW", mode="liquid")):
        s = time.time()
        for r in job(t):
            print(t["track"], t["variant"], r.get("fuel"), r.get("CR"), r.get("status"), r.get("reason"), "T_IVC", r.get("T_IVC_K"),
                  "g", r.get("fuel_evap_intake_fraction"), r.get("fuel_evap_saturation_limited"), "eta", r.get("gross_indicated_efficiency"),
                  "ca50", r.get("ca50_used_deg"), "knock", r.get("knock"), "elig", r.get("eligible"),
                  "clos", r.get("energy_closure_error_fraction"), "crn", r.get("crn_status"), r.get("crn_efficiency"))
        print("t", round(time.time() - s, 1), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "smoke", "count"])
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--phases", type=str, default=None)
    ap.add_argument("--out", type=str, default="points.jsonl")
    a = ap.parse_args()
    if a.cmd == "run":
        run(min(4, a.workers), None if a.phases is None else {int(x) for x in a.phases.split(",")}, a.out)
    elif a.cmd == "count":
        from collections import Counter
        print(Counter(t["phase"] for t in jobs()))
    else:
        smoke()
