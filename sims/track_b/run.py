"""Track B driver: normal fuels, dry baseline, then +0.1 pp water steps while efficiency improves.

Run:  python -m sims.track_b.run [--workers 6] [--fuels PRF91,...] [--smoke]

Rule (James, 2026-10-24, "two tracks"): about 50% of Water Engine jobs start from normal fuels
(regular/premium gasoline, alcohols, every fuel already tested) and add water content in the fuel mix in
steps of at most 0.1 percentage point, adding more only while efficiency gains are seen.

Per fuel x temperature regime (normal: wall 450 K, dry T_intake 320/360 K; hot: wall 520 K,
T_intake 400 K - same regimes as sims/03_engine_cycle/coupled_dual_temp.py):
 1. Dry baseline, Module 03: integer CR 9..24 x regime T_intake, spark optimised continuously
    (CA50 = max(MBT, knock/p_max limit)); best eligible point (Module 03 SPEC eligibility).
 2. Same hardware (CR, T_intake), w = 0.001, 0.002, ... (w = water / (water + fuel) mass), spark
    re-optimised at every step. Continue only if Module 03 gain > GAIN_THRESHOLD and the M03-CRN
    second engine gives a gain of the same sign; otherwise stop and record the best w.
 3. Every baseline/step point is re-run in M03-CRN (Woschni, like-for-like, ACCEPTANCE.md C1).
 4. Labelled exploratory probes (w = 1, 2, 5, 10 %; NOT Track B steps) on the same hardware.
Water handling: legacy Module 03 intake/in-cylinder evaporation (no Module 09 film profile exists
for these points; at w <= 1 % the PR 8 retained-liquid coupling has no measurable effect).
"""
import argparse
import importlib
import json
import math
import sys
import time
import warnings
from dataclasses import replace
from multiprocessing import get_context
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
warnings.filterwarnings("ignore")

from sims.track_b import fuels_b as FB  # noqa: E402

OUT = REPO / "results" / "track_b"
FUELS = ("PRF87", "PRF91", "PRF97", "E10", "E85", "CH3OH", "C2H5OH", "CH4")
REGIMES = {"normal": dict(wall_T_K=450.0, T_intake=(320.0, 360.0)),
           "hot": dict(wall_T_K=520.0, T_intake=(400.0,))}
CRS = tuple(range(9, 25))
STEP = 0.001             # 0.1 percentage point of water content
MAX_STEPS = 100          # hard cap (10 %); the gain rule stops far earlier
# Numerical-uncertainty threshold, stated before any step was run (verification/x5_m03/RESULTS_FIX.md):
# Module 03 efficiency GCI_fine <= 1.4e-5 relative, 0.5-CAD production step error <= 0.007 % relative
# (~3e-5 absolute at eta ~ 0.45). Threshold = 1e-4 absolute (0.01 percentage point) ~ 3x the step
# error, ~15x the GCI, ~5x the knock-limited bisection tolerance (0.005 CAD x ~4e-3/CAD).
GAIN_THRESHOLD = 1.0e-4
PROBES = (0.01, 0.02, 0.05, 0.10)
RAD = math.pi / 180.0
MBT_LO, MBT_HI, MBT_TOL = 0.0, 16.0, 0.1     # CAD aTDC
FEAS_TOL = 0.005                               # CAD

_m = None
_FITS = None


def module03():
    global _m, _FITS
    if _m is None:
        FB.register()
        _m = importlib.import_module("sims.03_engine_cycle.run")
        fd = REPO / "results" / "02_flame_chem"
        ign = json.loads((fd / "ignition_fits.json").read_text())
        fl = json.loads((fd / "flame_speed_fits.json").read_text())
        eth = fl["C2H5OH"]["coefficients_highest_first"][-1]
        for b in FB.BLENDS:
            ign[b] = FB.ignition_fit(b)
            fl[b] = FB.flame_fit(b, ethanol_SL0=eth)
        _FITS = (ign, fl)
        _m.retard_search = spark_optimise
    return _m


def spark_optimise(evaluate, par):
    """Replaces Module 03's 2-CAD retard search: MBT by golden section, then knock/p_max limit by bisection."""
    cache = {}

    def ev(deg):
        k = round(deg, 6)
        if k not in cache:
            cache[k] = evaluate(deg * RAD)
        return cache[k]

    def feasible(r):
        return (not r["knock"]) and r["peak_pressure_Pa"] <= par.peak_pressure_limit_Pa

    g = (math.sqrt(5) - 1) / 2
    a, b = MBT_LO, MBT_HI
    c, d = b - g * (b - a), a + g * (b - a)
    while b - a > MBT_TOL:
        if ev(c)["gross_indicated_efficiency"] >= ev(d)["gross_indicated_efficiency"]:
            b, d = d, c
            c = b - g * (b - a)
        else:
            a, c = c, d
            d = a + g * (b - a)
    mbt = max(cache, key=lambda k: cache[k]["gross_indicated_efficiency"])
    r_mbt = cache[mbt]
    limited_by = "MBT"
    chosen = mbt
    if not feasible(r_mbt):
        lim = par.retard_limit_rad / RAD
        if not feasible(ev(lim)):
            chosen, limited_by = lim, "infeasible_at_30CAD"
        else:
            lo, hi = mbt, lim
            while hi - lo > FEAS_TOL:
                mid = 0.5 * (lo + hi)
                if feasible(ev(mid)):
                    hi = mid
                else:
                    lo = mid
            chosen = hi
            limited_by = "knock" if ev(lo)["knock"] else "p_max"
    res = dict(ev(chosen))
    res.update(knock_limited=bool(res["knock"]), retard_attempts=len(cache),
               efficiency_at_default_ca50=r_mbt["gross_indicated_efficiency"],
               knock_integral_at_default_ca50=r_mbt["knock_integral_at_xb90"],
               mbt_ca50_deg=mbt, spark_limited_by=limited_by)
    spark_optimise.last = dict(mbt_ca50_deg=mbt, spark_limited_by=limited_by,
                               mbt_efficiency=r_mbt["gross_indicated_efficiency"])
    return res


KEEP = ("status reason fuel CR w T_intake_K gross_indicated_efficiency ca50_used_deg knock "
        "knock_integral_at_xb90 peak_pressure_Pa peak_pressure_angle_deg peak_burned_temperature_K "
        "NO_mol_per_J_fuel IMEP_Pa S_L_m_s burn_10_90_deg T_IVC_K f_evap_intake_effective fuel_mass_kg "
        "water_mass_kg air_mass_kg residual_mass_kg energy_closure_error_fraction mechanism").split()


# Water delivery modes (James 2026-10-24 18:22 PDT added the humid-intake cases):
#  liquid        legacy Module 03: liquid water at 300 K with the fuel; isobaric intake mixing evaporates
#                up to f_evap_intake = 0.5 (saturation-capped), the rest evaporates in-cylinder IVC -> -30 CAD.
#  humid_evap    water aerosolised into the intake air and fully evaporated before IVC (f_evap_intake = 1):
#                the latent heat cools the intake charge (higher trapped density at fixed p_IVC), capped at
#                saturation at the cooled (wet-bulb) temperature; any excess would condense / stay liquid and
#                then evaporates in-cylinder (flagged intake_saturation_limited).
#  humid_ambient humid-air reference: the water is already vapour at T_intake (specific humidity, no
#                evaporative cooling of the charge), capped at saturation at T_intake (Module 03 bound-(i)
#                port-vapour path, no liquid sink); water above saturation stays liquid and evaporates
#                in-cylinder on the legacy schedule (flagged port_evap_saturation_limited).
MODES = ("liquid", "humid_evap", "humid_ambient")


def point(fuel, regime, cr, T, w, mode="liquid"):
    m = module03()
    par = replace(m.DEFAULTS, wall_T_K=REGIMES[regime]["wall_T_K"])
    coupling = None
    if mode == "humid_evap":
        par = replace(par, f_evap_intake=1.0)
    elif mode == "humid_ambient":
        coupling = dict(port_evap_frac=1.0)
        par = replace(par, f_evap_intake=0.0)  # excess over saturation stays liquid -> in-cylinder schedule
    ign, fl = _FITS
    spark_optimise.last = {}
    out = m.run_point(fuel, float(cr), float(w), float(T), ign.get(fuel), fl.get(fuel), par, "full",
                      fits_source="module_02" if fuel not in FB.BLENDS else "track_b_published",
                      coupling=coupling)
    r = {k: out["point"].get(k) for k in KEEP}
    r.update(regime=regime, chamber_wall_K=par.wall_T_K, water_mode=mode,
             intake_saturation_limited=out["point"].get("intake_saturation_limited"),
             port_evap_fraction=out["point"].get("port_evap_fraction"),
             port_evap_saturation_limited=out["point"].get("port_evap_saturation_limited"),
             **spark_optimise.last)
    if r["status"] == "computed" and w > 0:
        e = r["f_evap_intake_effective"] or 0.0
        r["water_vapour_at_IVC_fraction"] = e
        r["specific_humidity_kg_per_kg_dry_air"] = e * r["water_mass_kg"] / r["air_mass_kg"]
    r["eligible"] = bool(r["status"] == "computed" and m.eligible(out["point"], par))
    if r["knock_integral_at_xb90"] is not None:
        r["knock_margin"] = 1.0 - r["knock_integral_at_xb90"]
    return r


# ------------------------------------------------------------- M03-CRN
_E = None


def crn_engine():
    global _E
    if _E is None:
        import cantera as ct
        FB.register()
        E = importlib.import_module("engines.m03_cantera.engine")
        nasa = {s.name: s for s in ct.Species.list_from_file("nasa_gas.yaml")}
        gri = {s.name: s for s in ct.Species.list_from_file("gri30.yaml")}
        orig = E.build_gas

        def build_gas(kinetics=True):
            g = orig(kinetics)
            extra = [FB.lumped_species(b, nasa) for b in FB.BLENDS] + [gri["CH4"]]
            return ct.Solution(thermo="ideal-gas", kinetics="gas" if kinetics else "none",
                               species=g.species() + extra, reactions=g.reactions())
        E.build_gas = build_gas
        for b in FB.BLENDS:
            E.ATOMS[b] = FB.blend_atoms(b)
            E.H_VAP[b] = FB.blend_hvap(b)
        E.ATOMS["CH4"], E.H_VAP["CH4"] = (1, 4, 0), 0.0
        _E = E
    return _E


def crn(r):
    if r.get("status") != "computed":
        return dict(crn_status="skipped")
    E = crn_engine()
    t = time.time()
    try:
        res = E.run_case(E.Case(fuel=r["fuel"], cr=r["CR"], T_ivc=r["T_IVC_K"], m_fuel=r["fuel_mass_kg"],
                                m_air=r["air_mass_kg"], m_residual=r["residual_mass_kg"],
                                m_water=r["water_mass_kg"], e_intake=r["f_evap_intake_effective"],
                                ca50_deg=r["ca50_used_deg"], d1090_deg=r["burn_10_90_deg"],
                                wall_T=r["chamber_wall_K"], heat_transfer="woschni"))
    except Exception as exc:  # recorded, never retried blindly
        return dict(crn_status=f"failed: {type(exc).__name__}: {exc}")
    eta, pmax = res["efficiency"], res["p_max_Pa"]
    return dict(crn_status="ok", crn_efficiency=eta, crn_p_max_Pa=pmax, crn_T_max_K=res.get("T_max_K"),
                crn_seconds=time.time() - t, d_eta_pp=100 * (eta - r["gross_indicated_efficiency"]),
                pmax_ratio=pmax / r["peak_pressure_Pa"],
                c1_pass=bool(abs(100 * (eta - r["gross_indicated_efficiency"])) <= 1.5
                             and abs(pmax / r["peak_pressure_Pa"] - 1) <= 0.05))


# ------------------------------------------------------------- stages
def _dry(task):
    return point(*task)


def chain(args):
    """Dry best -> 0.1 pp steps -> probes for one fuel x regime (sequential: each step depends on the last)."""
    fuel, regime, best = args[:3]
    mode = args[3] if len(args) > 3 else "liquid"
    log = OUT / (f"steps_{fuel}_{regime}.jsonl" if mode == "liquid" else f"steps_{fuel}_{regime}_{mode}.jsonl")
    log.unlink(missing_ok=True)

    def write(row):
        with log.open("a") as fh:
            fh.write(json.dumps(row, default=float) + "\n")

    base = dict(best, kind="dry_baseline", step=0, **crn(best))
    write(base)
    prev, best_row, stop = base, base, None
    for k in range(1, MAX_STEPS + 1):
        w = round(k * STEP, 6)
        r = point(fuel, regime, best["CR"], best["T_intake_K"], w, mode)
        r.update(kind="step", step=k, **crn(r))
        ok = r["status"] == "computed" and r["eligible"]
        r["gain_m03"] = (r["gross_indicated_efficiency"] - prev["gross_indicated_efficiency"]) if ok else None
        r["gain_crn"] = (r["crn_efficiency"] - prev["crn_efficiency"]) \
            if ok and r.get("crn_status") == "ok" and prev.get("crn_status") == "ok" else None
        gained = ok and r["gain_m03"] > GAIN_THRESHOLD and (r["gain_crn"] is None or r["gain_crn"] > 0)
        r["decision"] = "continue" if gained else "stop"
        write(r)
        if not gained:
            stop = ("not eligible" if not ok else
                    f"gain {r['gain_m03']:.2e} <= threshold {GAIN_THRESHOLD:.0e}" if r["gain_m03"] <= GAIN_THRESHOLD
                    else "M03-CRN disagrees on sign")
            break
        prev = best_row = r
    probes = []
    for w in PROBES:
        r = point(fuel, regime, best["CR"], best["T_intake_K"], w, mode)
        r.update(kind="exploratory_probe_not_a_track_b_step", step=None, **crn(r))
        write(r)
        probes.append(r)
    return dict(fuel=fuel, regime=regime, water_mode=mode, baseline=base, best_w=best_row["w"], best=best_row,
                steps_taken=best_row["step"], stop_reason=stop, probes=probes)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--fuels", default=",".join(FUELS))
    ap.add_argument("--from-dry", action="store_true", help="reuse results/track_b/dry_sweep.json")
    ap.add_argument("--smoke", action="store_true", help="one CR/T per fuel-regime (pipeline test only)")
    ap.add_argument("--stage", choices=("main", "humid"), default="main")
    a = ap.parse_args(argv)
    fuels = a.fuels.split(",")
    if a.stage == "humid":
        OUT.mkdir(parents=True, exist_ok=True)
        return humid_main(a.workers)
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    crs = (12,) if a.smoke else CRS
    tasks = [(f, g, cr, T, 0.0) for f in fuels for g, R in REGIMES.items() for cr in crs
             for T in (R["T_intake"][:1] if a.smoke else R["T_intake"])]
    ctx = get_context("spawn")
    with ctx.Pool(a.workers) as pool:
        dry = json.loads((OUT / "dry_sweep.json").read_text()) if a.from_dry else []
        for i, r in enumerate(pool.imap_unordered(_dry, [] if a.from_dry else tasks), 1):
            dry.append(r)
            if i % 20 == 0 or i == len(tasks):
                print(f"[dry] {i}/{len(tasks)} {time.time() - t0:.0f}s", flush=True)
        if not a.from_dry:
            (OUT / "dry_sweep.json").write_text(json.dumps(dry, indent=1, default=float))
        bests = []
        for f in fuels:
            for g in REGIMES:
                el = [r for r in dry if r["fuel"] == f and r["regime"] == g and r["eligible"]]
                if el:
                    bests.append((f, g, max(el, key=lambda r: r["gross_indicated_efficiency"])))
                else:
                    print(f"[dry] {f}/{g}: no eligible dry point", flush=True)
        chains = []
        for c in pool.imap_unordered(chain, bests):
            chains.append(c)
            print(f"[chain] {c['fuel']}/{c['regime']} best_w={c['best_w']} steps={c['steps_taken']} "
                  f"stop={c['stop_reason']} {time.time() - t0:.0f}s", flush=True)
    summary = dict(rule="Track B (pt78u)", gain_threshold_abs=GAIN_THRESHOLD, step=STEP, regimes=REGIMES,
                   crs=list(crs), fuels=fuels, wall_seconds=time.time() - t0, chains=chains,
                   fits={f: dict(ignition=_src(f, 0), flame=_src(f, 1)) for f in fuels})
    (OUT / ("summary_smoke.json" if a.smoke else "summary.json")).write_text(json.dumps(summary, indent=1, default=float))
    print("done", time.time() - t0, flush=True)


TRACK_A_FUELS = ("CH3OH", "C2H5OH", "CH4")
TRACK_A_W = (0.5, 0.6, 0.7, 0.8)
TRACK_A_CR = (12, 15, 18, 20, 22, 23, 24)


def _pt(t):
    return point(*t)


def humid_main(workers):
    """Humid-intake stage: Track B humid chains from the dry baselines + Track A water-majority 3-mode grid."""
    t0 = time.time()
    dry = json.loads((OUT / "dry_sweep.json").read_text())
    bests = []
    for f in FUELS:
        for g in REGIMES:
            el = [r for r in dry if r["fuel"] == f and r["regime"] == g and r["eligible"]]
            if el:
                b = max(el, key=lambda r: r["gross_indicated_efficiency"])
                bests += [(f, g, b, "humid_evap"), (f, g, b, "humid_ambient")]
    grid = [(f, g, cr, T, w, mode) for f in TRACK_A_FUELS for g, R in REGIMES.items() for cr in TRACK_A_CR
            for T in R["T_intake"] for w in TRACK_A_W for mode in MODES]
    ctx = get_context("spawn")
    with ctx.Pool(workers) as pool:
        chains = []
        for c in pool.imap_unordered(chain, bests):
            chains.append(c)
            print(f"[humid chain] {c['fuel']}/{c['regime']}/{c['water_mode']} best_w={c['best_w']} "
                  f"steps={c['steps_taken']} stop={c['stop_reason']} {time.time() - t0:.0f}s", flush=True)
        (OUT / "summary_humid_trackb.json").write_text(json.dumps(dict(chains=chains), indent=1, default=float))
        rows = []
        for i, r in enumerate(pool.imap_unordered(_pt, grid), 1):
            rows.append(r)
            if i % 40 == 0 or i == len(grid):
                print(f"[trackA humid grid] {i}/{len(grid)} {time.time() - t0:.0f}s", flush=True)
                (OUT / "trackA_humid_grid.json").write_text(json.dumps(rows, indent=1, default=float))
    print("humid done", time.time() - t0, flush=True)


def _src(f, i):
    module03()
    d = _FITS[i].get(f, {})
    return d.get("source", "Module 02 results/02_flame_chem (kinetics)")


if __name__ == "__main__":
    main()
