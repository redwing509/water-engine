"""Track A reconcile (2026-10-25): the Module 03 dual-temperature rerun vs the PR 8 coupled verdict.

Run:  python -m sims.03_engine_cycle.reconcile_dualtemp [--workers 2]

Question (Claude job water-engine-box-20261025-0700, steps 1-2): the dual-temperature rerun
(wme1-hiT sims/dual_temp/run_m03.py -> results/dual_temp/03_engine_cycle_{normal,hot}_fixed, single
engine) reported water-majority beating best dry: CH3OH +1.04 pp normal / +2.05 pp hot, CH4 +1.36 / +0.95.
PR 8 (coupled retained-liquid / wall-film model) found water-majority wins in 0/16 cases.

Finding before any run (code read): run_m03.py calls sims.03_engine_cycle.run main() WITHOUT
--evap-profile, so Charge(evap_profile=None, coupling=None) = the LEGACY (uncoupled) water schedule:
no retained liquid, no wall film.  Its water-majority etas (CH3OH 0.4311 normal / 0.4385 hot) are
identical to PR 8's "legacy schedule" rows, i.e. the superseded uncoupled numbers.

This script recomputes, at the SAME points:
  * the uncoupled ("legacy", superseded) water-majority row (reproduction check),
  * the PR 8 coupled rows, bound (i) port-evaporated and bound (ii) film-carried, for every Module 09
    atomiser x variant (sims/03_engine_cycle/coupled_dual_temp.task, unchanged),
  * the best-dry baselines under BOTH definitions:
      PR8   : dry CR 9..24, normal T_intake 320/360 K, hot 400 K (coupled_dual_temp.REGIMES)
      DT    : the dual-temperature rerun's best dry (hot regime also at intercooled 320/360 K intake,
              wme1-hiT HOT T_intake_K = (320, 360, 400)); recomputed here at that CR/T.
  * every row again in M03-CRN (engines/m03_cantera, compare_coupled.case: evap_mode="coupled" for the
    coupled rows; Woschni in both engines; C1 tolerance |d_eta| <= 1.5 pp, |p_max ratio - 1| <= 5 %).
CH4: Module 09 has no CH4 spray profile and the Module 06 heat budget has no CH4 latent data, so no
coupled CH4 number can be made; the CH4 rows are uncoupled (superseded) only.

Regimes: normal coolant 363.15 K / chamber wall 450 K / port wall 363.15 K; hot 388.15 / 520 / 388.15 K
(MAHLE/VW SSP 222, SAE 960271, Heywood 1988 ch. 12; docs/DUAL_TEMPERATURE_RULE.md).
Status: executed, two in-repo engines; NOT validated against experiment.
"""
import argparse
import csv
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
OUT = REPO / "results" / "03_engine_cycle" / "reconcile_dualtemp"
# Dual-temperature rerun best-dry points (results/dual_temp/03_engine_cycle_*_fixed/design_point.json on
# the box clone of m4/m03-dualT-full-20261024; copied into OUT/dualtemp_rerun_design_points.json).
DT_BEST_DRY = {("normal", "CH3OH"): (16, 320.0), ("normal", "C2H5OH"): (24, 320.0), ("normal", "CH4"): (22, 320.0),
               ("hot", "CH3OH"): (15, 320.0), ("hot", "C2H5OH"): (22, 320.0), ("hot", "CH4"): (24, 320.0)}
DT_WM = {("normal", "CH3OH"): (24, 0.6, 360.0), ("normal", "C2H5OH"): (24, 0.6, 360.0), ("normal", "CH4"): (23, 0.6, 320.0),
         ("hot", "CH3OH"): (24, 0.6, 400.0), ("hot", "C2H5OH"): (24, 0.6, 400.0), ("hot", "CH4"): (23, 0.6, 320.0)}
TOL_ETA_PP, TOL_PMAX = 1.5, 0.05


def specs():
    from importlib import import_module
    cd = import_module("sims.03_engine_cycle.coupled_dual_temp")
    out = []
    for regime in ("normal", "hot"):
        for fuel in ("CH3OH", "C2H5OH", "CH4"):
            cr, w, T = DT_WM[(regime, fuel)]
            out.append(dict(kind="legacy", fuel=fuel, regime=regime, point="water_majority", CR=cr, w=w, T_intake_K=T))
            dcr, dT = DT_BEST_DRY[(regime, fuel)]
            out.append(dict(kind="dry", fuel=fuel, regime=regime, point="best_dry_DT", CR=dcr, w=0.0, T_intake_K=dT))
            if fuel == "CH4":
                continue
            for a in cd.ATOMISERS:
                for v in cd.VARIANTS:
                    out.append(dict(kind="coupled", fuel=fuel, regime=regime, point="water_majority", CR=cr, w=w,
                                    T_intake_K=T, atomiser=a, variant=v))
    out.sort(key=lambda s: {"coupled": 0, "legacy": 1, "dry": 2}[s["kind"]])
    return out


def task(spec):
    from importlib import import_module
    cd = import_module("sims.03_engine_cycle.coupled_dual_temp")
    if spec["fuel"] == "CH4":  # coupled_dual_temp.REGIMES has the same walls; dry/legacy path needs no Module 09
        pass
    t0 = time.time()
    rows = cd.task(spec)
    for r in rows:
        r["point"] = spec["point"]
        r.update(crn_check(r))
    return rows


def crn_check(r):
    from engines.m03_cantera import compare_coupled as CC
    from engines.m03_cantera import engine as E
    if r.get("status") != "computed":
        return dict(crn_status="skipped")
    s = {k: ("" if v is None else str(v)) for k, v in r.items()}
    t = time.time()
    try:
        c = E.run_case(CC.case(s))
    except Exception as exc:  # recorded, not retried
        return dict(crn_status=f"failed: {type(exc).__name__}: {exc}"[:300])
    eta, pm = float(r["gross_indicated_efficiency"]), float(r["peak_pressure_Pa"])
    return dict(crn_status="ok", crn_efficiency=c["efficiency"], crn_p_max_Pa=c["p_max_Pa"],
                crn_IMEP_Pa=c["IMEP_Pa"], crn_d_eta_pp=100 * (c["efficiency"] - eta),
                crn_pmax_ratio=c["p_max_Pa"] / pm, crn_seconds=time.time() - t,
                crn_liquid_at_spark_kg=c.get("liquid_at_spark_kg"), crn_closure=c["energy_closure"],
                c1_pass=bool(abs(100 * (c["efficiency"] - eta)) <= TOL_ETA_PP and abs(c["p_max_Pa"] / pm - 1) <= TOL_PMAX))


def main(workers):
    OUT.mkdir(parents=True, exist_ok=True)
    sp = specs()
    rows = []
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers, mp_context=get_context("spawn")) as ex:
        for i, rr in enumerate(ex.map(task, sp, chunksize=1)):
            rows.extend(rr)
            print(f"{i + 1}/{len(sp)} {sp[i]['kind']} {sp[i]['fuel']} {sp[i]['regime']} {sp[i].get('atomiser', '')} "
                  f"{sp[i].get('variant', '')} " + " ".join(
                      f"{r.get('bound') or r['kind']}:{(r.get('gross_indicated_efficiency') or 0):.4f}/crn "
                      f"{(r.get('crn_efficiency') or 0):.4f}" for r in rr) + f" {time.time() - t0:.0f}s", flush=True)
    cols = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    with open(OUT / "points.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print("wrote", OUT / "points.csv", len(rows), f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=2)
    main(ap.parse_args().workers)
