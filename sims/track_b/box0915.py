"""Track B, Claude job water-engine-box-20261025-0915, steps B2 (second knock criterion) and B4 (CR re-optimisation).

Run:  python -m sims.track_b.box0915 run [--workers 4] [--chains NAME,...]
      python -m sims.track_b.box0915 report

Chains (best points of the top-4 Track B chains, noise rule 3.3e-5; results/track_b/*.jsonl):
  C2H5OH hot humid_evap (CR 12, T 400), CH3OH hot humid_evap (CR 8, T 400; H1 low-CR chain, results/track_b/h1_hot),
  CH3OH normal liquid (CR 17, T 320), PRF87 normal liquid (CR 9, T 320; best gasoline chain).
Grid: CR 9.0 .. 16.0 in 0.5 steps (job spec) plus the chain's own CR; w in {0 (dry), w_best}; knock criterion in
  LW  = the existing Track B criterion: Livengood-Wu integral to x_b = 0.9 with the Track B ignition fit
        (alcohols: Module 02 Cantera fit tau = A p^-n exp(E/RT)(1 + c w); PRF/E-blends: Douaud-Eyzat, c = 0)
  DE  = Livengood-Wu integral with the Douaud & Eyzat (1978) SAE 780080 correlation (Heywood 1988 s. 9.6),
        tau = 17.68 ms (ON/100)^3.402 p[atm]^-1.7 exp(3800 K/T), no water term (c = 0); ON = Module 03's RON
        (CH3OH 108.7, C2H5OH 108.6, run.py provenance) or the Track B blend ON (fuels_b). ON > 100 is an
        extrapolation of a PRF-fitted correlation. For the PRF/E blends LW and DE are the SAME correlation, so the
        gasoline chain has no independent second criterion here (no Cantera PRF ignition fit in the repo).
Spark re-optimised at every point (Track B spark_optimise: MBT golden section, knock/p_max bisection 0.005 CAD).
Every computed point is re-run in M03-CRN (Woschni; CA50/burn duration from Module 03 - the knock criterion is a
Module 03 phasing decision, M03-CRN has no knock model).
Status: EXECUTED; second engine = verification of the cycle efficiency only; NOT validated against experiment.
"""
import argparse
import csv
import json
import math
import sys
import time
from multiprocessing import get_context
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from sims.track_b import run as R  # noqa: E402
from sims.track_b import fuels_b as FB  # noqa: E402

OUT = REPO / "results" / "track_b" / "box0915"
TB = REPO / "results" / "track_b"
CHAINS = {
    "C2H5OH_hot_humid_evap": dict(fuel="C2H5OH", regime="hot", mode="humid_evap", file=TB / "steps_C2H5OH_hot_humid_evap__noise.jsonl"),
    "CH3OH_hot_humid_evap": dict(fuel="CH3OH", regime="hot", mode="humid_evap", file=TB / "h1_hot" / "steps_CH3OH_hot_humid_evap__noise.jsonl"),
    "CH3OH_normal_liquid": dict(fuel="CH3OH", regime="normal", mode="liquid", file=TB / "steps_CH3OH_normal__noise.jsonl"),
    "PRF87_normal_liquid": dict(fuel="PRF87", regime="normal", mode="liquid", file=TB / "steps_PRF87_normal__noise.jsonl"),
}
CR_GRID = tuple(9.0 + 0.5 * i for i in range(15))
RON_M03 = {"CH3OH": 108.7, "C2H5OH": 108.6, "CH4": 120.0}   # sims/03_engine_cycle/run.py provenance (ignition)


def chain_best(name):
    """(dry row, best accepted step row, n_steps) of a chain file: best = highest w with decision 'continue'."""
    rows = [json.loads(l) for l in open(CHAINS[name]["file"])]
    dry = next(r for r in rows if r.get("kind") == "dry_baseline")
    acc = [r for r in rows if r.get("kind") == "step" and r.get("decision") == "continue"]
    best = max(acc, key=lambda r: r["w"]) if acc else dry
    last = max((r for r in rows if r.get("kind") == "step"), key=lambda r: r["w"])
    return dry, best, last


def de_fit(fuel):
    on = FB.BLENDS[fuel]["ON"] if fuel in FB.BLENDS else RON_M03[fuel]

    import cantera as ct
    Rk = ct.gas_constant / 1000.0
    return dict(status="fitted", mode="full", A=17.68e-3 * (on / 100.0) ** 3.402 * ct.one_atm ** 1.7, n=1.7,
                E_J_per_mol=3800.0 * Rk, c=0.0, pressure_unit="Pa", A_unit="s*Pa**1.7", valid_T_K_range=None,
                valid_p_Pa_range=None, valid_w_range=None, octane_number=on,
                source="Douaud & Eyzat (1978) SAE 780080 (Heywood 1988 s.9.6); B2 second knock criterion")


def task(t):
    name, w, crit, cr = t
    c = CHAINS[name]
    dry, best, _ = chain_best(name)
    T = float(dry["T_intake_K"])
    R.module03()
    ign = R._FITS[0]
    saved = ign.get(c["fuel"])
    if crit == "DE":
        ign[c["fuel"]] = de_fit(c["fuel"])
    t0 = time.time()
    try:
        r = R.point(c["fuel"], c["regime"], cr, T, w, c["mode"] if w > 0 else "liquid")
    finally:
        ign[c["fuel"]] = saved
    r.update(chain=name, criterion=crit, m03_seconds=time.time() - t0)
    r.update(R.crn(r))
    return {k: (float(v) if hasattr(v, "dtype") else v) for k, v in r.items()}


def tasks(names):
    out = []
    for n in names:
        dry, best, _ = chain_best(n)
        crs = sorted(set(CR_GRID) | {float(dry["CR"])})
        for w in (0.0, float(best["w"])):
            for crit in ("LW", "DE"):
                for cr in crs:
                    out.append((n, w, crit, cr))
    return sorted(out, key=lambda t: -t[3])


def run(workers, names):
    OUT.mkdir(parents=True, exist_ok=True)
    tk = tasks(names)
    path = OUT / "points.jsonl"
    done = set()
    if path.exists():
        for l in open(path):
            r = json.loads(l)
            done.add((r["chain"], r["w"], r["criterion"], r["CR"]))
    tk = [t for t in tk if (t[0], t[1], t[2], t[3]) not in done]
    print(f"{len(tk)} tasks ({len(done)} already done)", flush=True)
    with get_context("spawn").Pool(workers) as pool, open(path, "a") as fh:
        for i, r in enumerate(pool.imap_unordered(task, tk)):
            fh.write(json.dumps(r, default=float) + "\n"); fh.flush()
            print(f"{i + 1}/{len(tk)} {r['chain']} {r['criterion']} w={r['w']} CR={r['CR']} "
                  f"eta={r.get('gross_indicated_efficiency')} crn={r.get('crn_efficiency')} ca50={r.get('ca50_used_deg')} "
                  f"{r.get('spark_limited_by')} elig={r.get('eligible')} {r['m03_seconds']:.0f}s", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "report"])
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--chains", default=",".join(CHAINS))
    a = ap.parse_args()
    if a.cmd == "run":
        run(min(4, a.workers), a.chains.split(","))
    else:
        from sims.track_b import box0915_report
        box0915_report.main()
