"""J1: second-engine check of the Module 03 hot-minus-normal efficiency trend (dual-temperature rule).

Engine 2 = sims/xcheck_cycle/x5_engine.py (X5 independent re-implementation of SPEC section 6, copied unchanged
from xcheck/cycle 0d47bc7 except the repo-path lines). Only its module-level WALL_T is set per regime
(normal 450 K / hot 520 K chamber wall, sims/dual_temp/regimes.py); intake T is a per-case input.
Engine 1 = Module 03 results committed on wme1-hiT 23f22b0 (results/dual_temp/03_engine_cycle_{normal,hot}).

Cases: every unique (fuel, CR, w) among the 12 wme1-hiT design points (best dry / overall / water-majority,
CH3OH + C2H5OH, normal + hot), run normal at T_intake 320/360 K and hot at 320/360/400 K.
Pairs: same T_intake (wall effect only) and hot 400 K vs normal 360 K (full hot regime).
PASS per pair: |d_x5 - d_m03| <= max(0.1 pp, 0.3*|d_m03|) and sign(d_x5) == sign(d_m03)
(sign test waived when |d_m03| < 0.02 pp, i.e. below the engines' numerical resolution - stated in the report).

usage (repo root): python -m sims.xcheck_cycle.dual_temp --workers 6
"""
import argparse, csv, json, math, time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
R = REPO / "results" / "dual_temp"
WALL = {"normal": 450.0, "hot": 520.0}
T_SET = {"normal": (320.0, 360.0), "hot": (320.0, 360.0, 400.0)}


def m03_rows(regime):
    rows = csv.DictReader((R / f"03_engine_cycle_{regime}" / "cycle_points.csv").open())
    return {(r["fuel"], float(r["CR"]), float(r["w"]), float(r["T_intake_K"])): r for r in rows if r["status"] == "computed"}


def run_one(args):
    regime, fuel, cr, w, T = args
    import numpy as np
    from sims.xcheck_cycle import x5_engine as X
    X.WALL_T = WALL[regime]
    fits = REPO / "results" / "02_flame_chem"
    ign = json.loads((fits / "ignition_fits.json").read_text())
    fla = json.loads((fits / "flame_speed_fits.json").read_text())
    sl = lambda ww: float(np.polyval(fla[fuel]["coefficients_highest_first"], ww))
    dur = min(X.DUR_CAP, X.DUR_REF * (sl(0.0) / sl(w)) ** X.FS_EXP)
    t0 = time.time()
    ch = X.Charge(fuel, cr, w, T)
    ca50, n = X.CA50, 0
    while True:
        r = X.integrate(ch, ca50, dur, ign[fuel])
        n += 1
        if not r["knock"] or ca50 >= X.RETARD_LIMIT - 1e-12:
            break
        ca50 = min(X.RETARD_LIMIT, ca50 + X.RETARD_STEP)
    r = {k: (bool(v) if isinstance(v, (bool, np.bool_)) else float(v) if isinstance(v, (int, float, np.floating)) else v) for k, v in r.items()}
    out = dict(regime=regime, fuel=fuel, CR=cr, w=w, T_intake_K=T, wall_T_K=X.WALL_T, eff=r["eff"], IMEP=r["IMEP"],
               pmax=r["pmax"], Tpeak=r["Tpeak"], TEVO=r["TEVO"], knock_limited=bool(n > 1), ca50=ca50 / X.RAD,
               attempts=n, closure=r["closure"], LW=r["LW"], seconds=time.time() - t0)
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--workers", type=int, default=6); ap.add_argument("--grid", action="store_true"); a = ap.parse_args()
    summ = {g: json.loads((R / "03_compare" / "summary.json").read_text())["best"] for g in [0]}[0]
    dps = []
    for fuel, regs in summ.items():
        for reg, cats in regs.items():
            for cat, p in cats.items():
                dps.append(dict(fuel=fuel, regime=reg, cat=cat, CR=p["CR"], w=p["w"], T_intake_K=p["T_intake_K"], eta=p["eta"]))
    uniq = sorted({(d["fuel"], d["CR"], d["w"]) for d in dps})
    jobs = [(reg, f, cr, w, T) for (f, cr, w) in uniq for reg in ("normal", "hot") for T in T_SET[reg]]
    if a.grid:  # every computed Module 03 point in both regimes (full 1296-pair comparison)
        jobs = sorted(set(jobs) | {(reg,) + k for reg in ("normal", "hot") for k in m03_rows(reg)})
    print(f"{len(dps)} design points -> {len(uniq)} unique (fuel,CR,w) -> {len(jobs)} X5 runs", flush=True)
    res = []
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for r in ex.map(run_one, jobs, chunksize=4):
            print(json.dumps({k: r[k] for k in ("regime", "fuel", "CR", "w", "T_intake_K", "eff", "seconds")}), flush=True)
            res.append(r)
    out = REPO / "results" / "xcheck" / "dual_temp_cycle"; out.mkdir(parents=True, exist_ok=True)
    json.dump(dict(design_points=dps, runs=res), (out / "x5_runs.json").open("w"), indent=1)
    print("wrote", out / "x5_runs.json")


if __name__ == "__main__":
    main()
