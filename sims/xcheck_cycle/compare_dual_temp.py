"""J1 (box-queue 20261024-1230): X5 vs Module 03 hot-minus-normal efficiency delta.
Reads results/xcheck/dual_temp_cycle/x5_runs.json (sims.xcheck_cycle.dual_temp) and
results/dual_temp/03_engine_cycle_{normal,hot}/cycle_points.csv. Pairing identical to
sims/dual_temp/compare_m03.py: same (fuel, CR, w, T_intake); hot 400 K intake vs normal 360 K.
PASS per pair: |d_x5 - d_m03| <= max(0.1 pp, 0.3 |d_m03|) AND sign(d_x5) == sign(d_m03)
(sign test waived when |d_m03| < 0.02 pp, i.e. below X5/Module-03 solver noise).
Writes results/xcheck/dual_temp_cycle/{pairs.csv,summary.json}."""
import csv, json, math
from pathlib import Path
import numpy as np
REPO = Path(__file__).resolve().parents[2]
R = REPO / "results" / "dual_temp"; O = REPO / "results" / "xcheck" / "dual_temp_cycle"
TOL_ABS, TOL_REL, SIGN_FLOOR = 0.1, 0.3, 0.02
CA50_BASE = 8.0  # deg aTDC; "knock-retarded" = CA50 moved later than this in either engine (M03 knock_limited means retard limit hit)


def load_m03(reg):
    return {(r["fuel"], float(r["CR"]), float(r["w"]), float(r["T_intake_K"])): r
            for r in csv.DictReader((R / f"03_engine_cycle_{reg}" / "cycle_points.csv").open()) if r["status"] == "computed"}


def judge(dx, dm):
    tol = max(TOL_ABS, TOL_REL * abs(dm))
    sign_ok = abs(dm) < SIGN_FLOOR or (np.sign(dx) == np.sign(dm))
    return tol, bool(abs(dx - dm) <= tol and sign_ok), bool(sign_ok)


def main():
    d = json.loads((O / "x5_runs.json").read_text())
    x5 = {(r["regime"], r["fuel"], r["CR"], r["w"], r["T_intake_K"]): r for r in d["runs"]}
    m = {g: load_m03(g) for g in ("normal", "hot")}
    pairs = []
    for k, h in m["hot"].items():
        n = m["normal"].get(k) or m["normal"].get(k[:3] + (360.0,))
        if n is None: continue
        kn = (n["fuel"], float(n["CR"]), float(n["w"]), float(n["T_intake_K"]))
        xh, xn = x5.get(("hot",) + k), x5.get(("normal",) + kn)
        if xh is None or xn is None: continue
        dm = 100 * (float(h["gross_indicated_efficiency"]) - float(n["gross_indicated_efficiency"]))
        dx = 100 * (xh["eff"] - xn["eff"])
        tol, ok, sok = judge(dx, dm)
        pairs.append(dict(fuel=k[0], CR=k[1], w=k[2], T_intake_hot_K=k[3], T_intake_normal_K=kn[3],
                          eta_m03_normal=float(n["gross_indicated_efficiency"]), eta_m03_hot=float(h["gross_indicated_efficiency"]),
                          eta_x5_normal=xn["eff"], eta_x5_hot=xh["eff"], d_m03_pp=dm, d_x5_pp=dx, diff_pp=dx - dm, tol_pp=tol,
                          sign_ok=sok, PASS=ok,
                          knock_m03_n=float(n["ca50_used_deg"]) > CA50_BASE + 1e-9, knock_m03_h=float(h["ca50_used_deg"]) > CA50_BASE + 1e-9,
                          knock_x5_n=xn["knock_limited"], knock_x5_h=xh["knock_limited"],
                          pmax_bar_m03_n=float(n["peak_pressure_Pa"]) / 1e5, pmax_bar_m03_h=float(h["peak_pressure_Pa"]) / 1e5,
                          pmax_bar_x5_n=xn["pmax"] / 1e5, pmax_bar_x5_h=xh["pmax"] / 1e5,
                          Tpk_m03_n=float(n["peak_temperature_K"]), Tpk_m03_h=float(h["peak_temperature_K"]),
                          Tpk_x5_n=xn["Tpeak"], Tpk_x5_h=xh["Tpeak"],
                          wall_heat_J_m03_n=float(n["wall_heat_J"]), wall_heat_J_m03_h=float(h["wall_heat_J"]),
                          relNO_m03_n=float(n["relative_NO"]), relNO_m03_h=float(h["relative_NO"]),
                          ca50_m03_n=float(n["ca50_used_deg"]), ca50_m03_h=float(h["ca50_used_deg"]),
                          ca50_x5_n=xn["ca50"], ca50_x5_h=xh["ca50"], burn_10_90_m03=float(n["burn_10_90_deg"])))
    with (O / "pairs.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(pairs[0])); w.writeheader(); w.writerows(pairs)
    S = dict(criterion=f"|d_x5-d_m03| <= max({TOL_ABS} pp, {TOL_REL}|d_m03|) and same sign (waived if |d_m03|<{SIGN_FLOOR} pp)",
             n_pairs=len(pairs), n_pass=sum(p["PASS"] for p in pairs), groups={}, design_points=[])
    for fuel in sorted({p["fuel"] for p in pairs}):
        for Th in (320.0, 360.0, 400.0):
            ps = [p for p in pairs if p["fuel"] == fuel and p["T_intake_hot_K"] == Th]
            if not ps: continue
            a = lambda k: np.array([p[k] for p in ps], float)
            S["groups"][f"{fuel} hot_T={Th:g}"] = dict(n=len(ps), n_pass=sum(p["PASS"] for p in ps),
                d_m03_mean=a("d_m03_pp").mean(), d_x5_mean=a("d_x5_pp").mean(), diff_mean=a("diff_pp").mean(),
                diff_absmax=np.abs(a("diff_pp")).max(), sign_fail=sum(not p["sign_ok"] for p in ps),
                knock_m03_n=int(a("knock_m03_n").sum()), knock_m03_h=int(a("knock_m03_h").sum()),
                knock_x5_n=int(a("knock_x5_n").sum()), knock_x5_h=int(a("knock_x5_h").sum()))
    # design points: (a) same-point pairs at every design (fuel,CR,w); (b) best-vs-best per category
    idx = {(p["fuel"], p["CR"], p["w"], p["T_intake_hot_K"]): p for p in pairs}
    dps = d["design_points"]
    for fuel in sorted({q["fuel"] for q in dps}):
        for cat in ("dry", "overall", "water_majority"):
            dn = next(q for q in dps if q["fuel"] == fuel and q["cat"] == cat and q["regime"] == "normal")
            dh = next(q for q in dps if q["fuel"] == fuel and q["cat"] == cat and q["regime"] == "hot")
            xn = x5[("normal", fuel, dn["CR"], dn["w"], dn["T_intake_K"])]; xh = x5[("hot", fuel, dh["CR"], dh["w"], dh["T_intake_K"])]
            dm, dx = 100 * (dh["eta"] - dn["eta"]), 100 * (xh["eff"] - xn["eff"])
            tol, ok, sok = judge(dx, dm)
            same = [idx[k] for k in idx if k[0] == fuel and ((k[1], k[2]) in {(dn["CR"], dn["w"]), (dh["CR"], dh["w"])})]
            S["design_points"].append(dict(fuel=fuel, cat=cat, normal=dict(CR=dn["CR"], w=dn["w"], T=dn["T_intake_K"], eta_m03=dn["eta"], eta_x5=xn["eff"]),
                hot=dict(CR=dh["CR"], w=dh["w"], T=dh["T_intake_K"], eta_m03=dh["eta"], eta_x5=xh["eff"]),
                best_vs_best=dict(d_m03_pp=dm, d_x5_pp=dx, tol_pp=tol, PASS=ok),
                same_point_pairs=[dict(CR=p["CR"], w=p["w"], T_hot=p["T_intake_hot_K"], T_norm=p["T_intake_normal_K"],
                                       d_m03_pp=p["d_m03_pp"], d_x5_pp=p["d_x5_pp"], tol_pp=p["tol_pp"], PASS=p["PASS"]) for p in same]))
    dpp = [p for q in S["design_points"] for p in q["same_point_pairs"]] + [q["best_vs_best"] for q in S["design_points"]]
    S["design_point_checks"] = dict(n=len(dpp), n_pass=sum(p["PASS"] for p in dpp))
    S["offset_normal_pp_mean"] = float(np.mean([100 * (p["eta_x5_normal"] - p["eta_m03_normal"]) for p in pairs]))
    S["offset_hot_pp_mean"] = float(np.mean([100 * (p["eta_x5_hot"] - p["eta_m03_hot"]) for p in pairs]))
    (O / "summary.json").write_text(json.dumps(S, indent=1, default=float))
    print(json.dumps({k: S[k] for k in ("n_pairs", "n_pass", "design_point_checks", "offset_normal_pp_mean", "offset_hot_pp_mean")}, indent=1))
    for g, v in S["groups"].items(): print(g, {k: (round(x, 3) if isinstance(x, float) else x) for k, x in v.items()})
    for q in S["design_points"]:
        print(q["fuel"], q["cat"], {k: round(v, 3) if isinstance(v, float) else v for k, v in q["best_vs_best"].items()},
              [(p["CR"], p["w"], p["T_hot"], round(p["d_m03_pp"], 3), round(p["d_x5_pp"], 3), p["PASS"]) for p in q["same_point_pairs"]])


if __name__ == "__main__":
    main()
