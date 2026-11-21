"""Two-engine check of the item-B coupled design points: M03-CRN vs Module 03.

Reads results/03_engine_cycle/coupled/coupled_points.csv (Module 03 rows: problem
definition = trapped masses, T_IVC, intake-evaporated fraction incl. bound-(i)
port vapour, CA50 used, 10-90 duration, wall T; Module 09 IVC/spark fractions)
and reruns every computed design-point row in M03-CRN with its own
formulation (engine.py evap_mode="coupled": CVODES ReactorNet, GRI/NASA
thermo, ct.Water latent heat, H2O(g) MFC inflow; single zone, so the
burned-zone allocation of the vaporised liquid is not replicated - only its
energy and mass enter, at the burn rate).

Tolerance (ACCEPTANCE.md C1, Woschni in both engines): |d_eta| <= 1.5 pp and
|pmax ratio - 1| <= 5 % at every point. Writes
results/engines/m03_cantera/compare_coupled.{csv,json}.
"""
import csv
import json
import math
import sys
import time
import warnings
from multiprocessing import get_context
from pathlib import Path

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engines.m03_cantera import engine as E  # noqa: E402

SRC = ROOT / "results" / "03_engine_cycle" / "coupled" / "coupled_points.csv"
OUT = ROOT / "results" / "engines" / "m03_cantera"
TOL_ETA_PP, TOL_PMAX = 1.5, 0.05


def design_rows():
    rows = [r for r in csv.DictReader(open(SRC)) if r["status"] == "computed"]
    best = {}
    for r in rows:
        if r["kind"] == "dry":
            k = (r["regime"], r["fuel"])
            if eligible(r) and (k not in best or float(r["gross_indicated_efficiency"]) >
                                float(best[k]["gross_indicated_efficiency"])):
                best[k] = r
    out = [dict(r, role="best_dry_regime") for r in best.values()]
    out += [r for r in rows if r["kind"] in ("legacy", "coupled")]
    return out


def eligible(r):
    return (r["status"] == "computed" and r["knock"] == "False" and r["knock_limited"] == "False"
            and float(r["ca50_used_deg"]) <= 15 + 1e-9 and float(r["S_L_m_s"]) >= 0.08
            and float(r["peak_pressure_Pa"]) <= 120e5)


def case(r):
    f = lambda k: float(r[k])
    kw = {}
    if r["kind"] == "coupled":
        port = f("port_evap_fraction") if r.get("port_evap_fraction") not in (None, "") else 0.0
        kw = dict(evap_mode="coupled", spark_deg=f("m09_spark_deg"),
                  f_ivc=min(1.0, port + f("m09_frac_ivc")), f_spark=min(1.0, port + f("m09_frac_evap_spark")))
    return E.Case(fuel=r["fuel"], cr=f("CR"), T_ivc=f("T_IVC_K"), m_fuel=f("fuel_mass_kg"), m_air=f("air_mass_kg"),
                  m_residual=f("residual_mass_kg"), m_water=f("water_mass_kg"),
                  e_intake=f("f_evap_intake_effective"), ca50_deg=f("ca50_used_deg"),
                  d1090_deg=f("burn_10_90_deg"), wall_T=f("chamber_wall_K"), heat_transfer="woschni",
                  label="|".join(r[k] for k in ("regime", "kind", "fuel", "point", "atomiser", "variant", "bound")),
                  **kw)


def _run(r):
    t = time.time()
    try:
        res = E.run_case(case(r))
        res["status"] = "ok"
    except Exception as exc:  # reported, not hidden
        res = dict(status=f"failed: {type(exc).__name__}: {exc}")
    res["runtime_s"] = time.time() - t
    return r, res


def main(workers=4):
    rows = design_rows()
    table = []
    with get_context("spawn").Pool(min(4, workers)) as pool:
        for r, c in pool.imap_unordered(_run, rows):
            eta_m, pm = float(r["gross_indicated_efficiency"]), float(r["peak_pressure_Pa"])
            t = dict(regime=r["regime"], kind=r["kind"], role=r.get("role", r.get("point", "")),
                     fuel=r["fuel"], CR=r["CR"], w=r["w"], T_intake_K=r["T_intake_K"],
                     atomiser=r["atomiser"], variant=r["variant"], bound=r["bound"],
                     eta_m03=eta_m, pmax_m03_MPa=pm / 1e6, crn_status=c["status"], runtime_s=c["runtime_s"])
            if c["status"] == "ok":
                t.update(eta_crn=c["efficiency"], d_eta_pp=100 * (c["efficiency"] - eta_m),
                         pmax_crn_MPa=c["p_max_Pa"] / 1e6, d_pmax_rel=c["p_max_Pa"] / pm - 1,
                         Tmax_m03=float(r["peak_temperature_K"]), Tmax_crn=c["T_max_K"],
                         TEVO_m03=float(r["EVO_T_K"]), TEVO_crn=c["T_EVO_K"],
                         Qwall_m03_J=float(r["wall_heat_J"]), Qwall_crn_J=c["wall_heat_J"],
                         liquid_spark_m03=r.get("liquid_fraction_spark"),
                         liquid_spark_crn=(c["liquid_at_spark_kg"] / float(r["water_mass_kg"])
                                           if c.get("liquid_at_spark_kg") is not None else None),
                         liquid_EVO_crn_kg=c["liquid_left_kg"], closure_crn=c["energy_closure"],
                         NO_bulk_crn=c["NO_mol_per_J_fuel_bulk"], NO_m03=float(r["NO_mol_per_J_fuel"]))
                t["within_tol"] = abs(t["d_eta_pp"]) <= TOL_ETA_PP and abs(t["d_pmax_rel"]) <= TOL_PMAX
            else:
                t["within_tol"] = False
            table.append(t)
            print(t["regime"], t["kind"], t["fuel"], t["role"], t["atomiser"], t["variant"], t["bound"],
                  "d_eta_pp=%s" % (round(t.get("d_eta_pp", float("nan")), 3)),
                  "d_pmax=%s" % (round(t.get("d_pmax_rel", float("nan")), 4)), t["crn_status"][:40],
                  "%.0fs" % t["runtime_s"], flush=True)
    table.sort(key=lambda t: (t["regime"], t["fuel"], t["kind"], t["role"], t["atomiser"], t["variant"], t["bound"]))
    cols = []
    for t in table:
        cols += [k for k in t if k not in cols]
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "compare_coupled.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(table)
    ok = [t for t in table if t["crn_status"] == "ok"]
    summary = dict(n=len(table), n_ok=len(ok), all_within_tol=all(t["within_tol"] for t in table),
                   max_abs_d_eta_pp=max(abs(t["d_eta_pp"]) for t in ok) if ok else None,
                   max_abs_d_pmax_rel=max(abs(t["d_pmax_rel"]) for t in ok) if ok else None,
                   tolerance=dict(eta_pp=TOL_ETA_PP, pmax_rel=TOL_PMAX, basis="ACCEPTANCE.md C1 (Woschni both)"))
    (OUT / "compare_coupled.json").write_text(json.dumps(dict(summary=summary, rows=table), indent=1, default=str))
    print(json.dumps(summary, indent=1), flush=True)


if __name__ == "__main__":
    main()
