"""Two-engine comparison M03-CRN vs Module 03 (ACCEPTANCE.md C1/C2), both temperature regimes.
Writes results/engines/m03_cantera/compare.{json,csv}."""
import csv
import json
import sys
import time
import warnings
from multiprocessing import Pool
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from engines.m03_cantera import engine as E, points as P  # noqa: E402

OUT = ROOT / "results" / "engines" / "m03_cantera"
VARIANTS = {
    "C1_woschni": dict(heat_transfer="woschni"),
    "C2_hohenberg": dict(heat_transfer="hohenberg"),
    "S_woschni_frozen": dict(heat_transfer="woschni", kinetics=False),
    "S_adiabatic": dict(heat_transfer="none"),
}
TOL_ETA_PP = 1.5
TOL_PMAX = 0.05


def _run(args):
    rk, var = args
    d = P.load_rows()
    regime = rk.split("|")[0]
    c = P.case_from_row(d["rows"][rk], regime, **VARIANTS[var])
    c.label = rk
    t = time.time()
    r = E.run_case(c)
    r["runtime_s"] = time.time() - t
    return rk, var, r


def main(workers=6):
    OUT.mkdir(parents=True, exist_ok=True)
    d = P.load_rows()
    tasks = [(rk, v) for rk in d["rows"] for v in VARIANTS]
    with Pool(workers) as pool:
        res = pool.map(_run, tasks)
    table = []
    for rk, var, r in res:
        m = d["rows"][rk]
        regime, key = rk.split("|")
        eta_m, pmax_m = float(m["gross_indicated_efficiency"]), float(m["peak_pressure_Pa"])
        table.append(dict(
            regime=regime, point=key, variant=var,
            design_roles=";".join(k for k, v in d["designs"].items() if v == key and k.startswith(regime)),
            eta_m03=eta_m, eta_crn=r["efficiency"], d_eta_pp=100 * (r["efficiency"] - eta_m),
            pmax_m03_MPa=pmax_m / 1e6, pmax_crn_MPa=r["p_max_Pa"] / 1e6, d_pmax_rel=r["p_max_Pa"] / pmax_m - 1,
            Tmax_m03=float(m["peak_temperature_K"]), Tmax_crn=r["T_max_K"],
            TEVO_m03=float(m["EVO_T_K"]), TEVO_crn=r["T_EVO_K"],
            Qwall_m03_J=float(m["wall_heat_J"]), Qwall_crn_J=r["wall_heat_J"],
            Qwall_frac_crn=r["wall_heat_J"] / r["Q_fuel_J"],
            IMEP_m03_bar=float(m["IMEP_Pa"]) / 1e5, IMEP_crn_bar=r["IMEP_Pa"] / 1e5,
            burn_10_90_deg=float(m["burn_10_90_deg"]), ca50_deg=float(m["ca50_used_deg"]),
            burn_rate_peak_J_per_deg=r["peak_burn_rate_J_per_deg"],
            T_endgas_pmax_crn=r["T_endgas_at_pmax_K"],
            NO_bulk_crn=r["NO_mol_per_J_fuel_bulk"], NO_m03=float(m["NO_mol_per_J_fuel"] or "nan"),
            knock_integral_m03=float(m["knock_integral_at_xb90"] or "nan"),
            closure_crn=r["energy_closure"], runtime_s=r["runtime_s"],
            within_tol=abs(r["efficiency"] - eta_m) * 100 <= TOL_ETA_PP and abs(r["p_max_Pa"] / pmax_m - 1) <= TOL_PMAX,
        ))
    table.sort(key=lambda x: (x["variant"], x["point"], x["regime"]))
    with open(OUT / "compare.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(table[0]))
        w.writeheader(); w.writerows(table)
    summary = {}
    for var in VARIANTS:
        rows = [t for t in table if t["variant"] == var]
        summary[var] = dict(n=len(rows), n_within=sum(t["within_tol"] for t in rows),
                            max_abs_d_eta_pp=max(abs(t["d_eta_pp"]) for t in rows),
                            max_abs_d_pmax_rel=max(abs(t["d_pmax_rel"]) for t in rows),
                            max_abs_d_Tmax_K=max(abs(t["Tmax_crn"] - t["Tmax_m03"]) for t in rows))
    # hot vs normal, same point, both engines (C1 and C2)
    hvn = []
    for var in ("C1_woschni", "C2_hohenberg"):
        by = {(t["regime"], t["point"]): t for t in table if t["variant"] == var}
        for (rg, pt), t in by.items():
            if rg == "hot" and ("normal", pt) in by:
                n = by[("normal", pt)]
                hvn.append(dict(variant=var, point=pt, d_eta_pp_m03=100 * (t["eta_m03"] - n["eta_m03"]),
                                d_eta_pp_crn=100 * (t["eta_crn"] - n["eta_crn"]),
                                d_Qwall_J_crn=t["Qwall_crn_J"] - n["Qwall_crn_J"],
                                d_pmax_MPa_crn=t["pmax_crn_MPa"] - n["pmax_crn_MPa"],
                                d_Tmax_K_crn=t["Tmax_crn"] - n["Tmax_crn"],
                                d_NO_rel_crn=(t["NO_bulk_crn"] / n["NO_bulk_crn"] - 1) if n["NO_bulk_crn"] else None,
                                same_sign=(t["eta_m03"] - n["eta_m03"]) * (t["eta_crn"] - n["eta_crn"]) > 0))
    out = dict(tolerances=dict(eta_pp=TOL_ETA_PP, pmax_rel=TOL_PMAX), summary=summary,
               C1_pass=summary["C1_woschni"]["n_within"] == summary["C1_woschni"]["n"],
               C2_pass=summary["C2_hohenberg"]["n_within"] == summary["C2_hohenberg"]["n"],
               hot_vs_normal=hvn, provenance=d["provenance"], rows=table)
    (OUT / "compare.json").write_text(json.dumps(out, indent=1, default=float))
    print(json.dumps({k: out[k] for k in ("summary", "C1_pass", "C2_pass")}, indent=1, default=str))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
