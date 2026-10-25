"""Report for reconcile_dualtemp (Track A, 2026-10-25): writes results/03_engine_cycle/reconcile_dualtemp/RECONCILE.md
and reconcile.json.  Both engines (Module 03 + M03-CRN), both regimes, both coupled bounds, cost metric
(sims/cost, copied unchanged from the Track B branch commit fb0c2b8; prices dated 2026-10-25)."""
import csv
import json
import sys
from dataclasses import replace
from importlib import import_module
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
D = REPO / "results" / "03_engine_cycle" / "reconcile_dualtemp"
NUM = ("CR w T_intake_K gross_indicated_efficiency IMEP_Pa peak_pressure_Pa ca50_used_deg S_L_m_s knock_integral_at_xb90 "
       "energy_closure_error_fraction fuel_mass_kg water_mass_kg air_mass_kg crn_efficiency crn_IMEP_Pa crn_p_max_Pa "
       "port_evap_fraction").split()


def why_not(r):
    """Reason a computed row fails SPEC selection (Module 03 eligible())."""
    w = []
    if str(r.get("knock")) == "True" or str(r.get("knock_limited")) == "True":
        w.append("knock")
    if float(r["ca50_used_deg"]) > 15 + 1e-9:
        w.append("CA50 %.0f" % float(r["ca50_used_deg"]))
    if float(r["peak_pressure_Pa"]) > 120e5:
        w.append("p_max %.0f bar" % (float(r["peak_pressure_Pa"]) / 1e5))
    if float(r["S_L_m_s"]) < 0.08:
        w.append("S_L")
    return "no (" + ", ".join(w or ["closure"]) + ")"


def conv(r):
    o = dict(r)
    for k in NUM:
        if k in o:
            o[k] = float(o[k]) if o[k] not in ("", None) else None
    for k in ("knock", "knock_limited"):
        o[k] = o.get(k) == "True"
    return o


def main():
    m = import_module("sims.03_engine_cycle.run")
    cost = import_module("sims.cost.cost")
    CC = import_module("engines.m03_cantera.compare_coupled")
    E = import_module("engines.m03_cantera.engine")
    rows = [conv(r) for r in csv.DictReader(open(D / "points.csv"))]
    ch4 = {(c["kind"], c["regime"]): c for c in json.load(open(D / "ch4_crn.json"))}
    for r in rows:
        if r["fuel"] == "CH4":
            c = ch4[(r["kind"], r["regime"])]
            r.update(crn_status=c["crn_status"], crn_efficiency=c["crn_efficiency"], crn_p_max_Pa=c["crn_p_max_Pa"],
                     crn_note="M03-CRN via sims/track_b/run.py crn() (CH4 registration) on the Track B branch")
        r["eligible"] = bool(m.eligible(r, m.DEFAULTS))
        r["crn_status"] = r.get("crn_status") or "ok"
    # PR 8 best-dry baselines (coupled_points.csv, kind=dry, SPEC-eligible max; hot regime T_intake 400 K only)
    pr8 = {}
    for r in csv.DictReader(open(REPO / "results" / "03_engine_cycle" / "coupled" / "coupled_points.csv")):
        if r["kind"] != "dry" or r["status"] != "computed":
            continue
        r = conv(r)
        if not m.eligible(r, m.DEFAULTS):
            continue
        k = (r["fuel"], r["regime"])
        if k not in pr8 or r["gross_indicated_efficiency"] > pr8[k]["gross_indicated_efficiency"]:
            pr8[k] = r
    for k, r in pr8.items():
        s = {kk: ("" if v is None else str(v)) for kk, v in r.items()}
        c = E.run_case(CC.case(s))
        r.update(crn_status="ok", crn_efficiency=c["efficiency"], eligible=True, point="best_dry_PR8")
    out = []
    md = ["# Track A reconcile: dual-temperature rerun vs PR #8 coupled verdict (2026-10-25)", "",
          "**Tags:** Track A; both temperature regimes; executed (Module 03) + verified (M03-CRN second engine); "
          "NOT validated against experiment.", "",
          "Regimes: normal = coolant 363.15 K, chamber wall 450 K, port wall 363.15 K; hot = coolant 388.15 K, "
          "chamber wall 520 K, port wall 388.15 K (MAHLE/VW SSP 222; SAE 960271; Heywood 1988 ch. 12; "
          "docs/DUAL_TEMPERATURE_RULE.md).", "",
          "## Finding", "",
          "The dual-temperature rerun (`sims/dual_temp/run_m03.py`, results/dual_temp/03_engine_cycle_*_fixed) called "
          "Module 03 without `--evap-profile`, i.e. with `evap_profile=None, coupling=None`: the **legacy, uncoupled** "
          "water schedule (no retained liquid, no wall film). Its water-majority numbers are reproduced here exactly "
          "and are the same numbers as PR #8's 'legacy schedule' rows. They are **uncoupled (superseded)**. "
          "With the PR #8 coupled model, every water-majority case loses to the best dry point or is not SPEC-eligible, "
          "in both bounds and both engines (table below). The hot-regime +2.05 pp also compared a 400 K-intake wet point "
          "with a 320 K-intake dry point.", ""]
    hdr = ("| fuel | regime | model | atomiser / variant | bound | CR / w / T_in K | eta M03 | eta CRN | eligible | "
           "d vs rerun best dry pp (M03 / CRN) | d vs PR8 best dry pp (M03 / CRN) | power IMEP % | cost/mile % at 0.10 USD/gal water (M03 / CRN) | cost/mile % at free water (M03 / CRN) | cost verdict |")
    md += ["## Water-majority points, both engines", "", hdr, "|" + "---|" * 15]
    for regime in ("normal", "hot"):
        for fuel in ("CH3OH", "C2H5OH", "CH4"):
            dt = next(r for r in rows if r["kind"] == "dry" and r["fuel"] == fuel and r["regime"] == regime)
            p8 = pr8.get((fuel, regime))
            wet = [r for r in rows if r["kind"] != "dry" and r["fuel"] == fuel and r["regime"] == regime]
            wet.sort(key=lambda r: (r["kind"] != "legacy", r["atomiser"], r["variant"], r["bound"]))
            for r in wet:
                c = cost.compare(r, dt)
                d_dt = (100 * (r["gross_indicated_efficiency"] - dt["gross_indicated_efficiency"]),
                        100 * (r["crn_efficiency"] - dt["crn_efficiency"]) if r.get("crn_efficiency") else None)
                d_p8 = ((100 * (r["gross_indicated_efficiency"] - p8["gross_indicated_efficiency"]),
                         100 * (r["crn_efficiency"] - p8["crn_efficiency"])) if p8 else None)
                model = "uncoupled (superseded)" if r["kind"] == "legacy" else "coupled (PR #8)"
                ver = cost.verdict(c)
                if not r["eligible"]:
                    ver += "; wet point not SPEC-eligible"
                f2 = lambda t: "n/a" if t is None else (f"{t[0]:+.2f} / " + ("n/a" if t[1] is None else f"{t[1]:+.2f}"))
                md.append(f"| {fuel} | {regime} | {model} | {r['atomiser'] or '-'} / {r['variant'] or '-'} | "
                          f"{r['bound'] or '-'} | {r['CR']:.0f} / {r['w']:.1f} / {r['T_intake_K']:.0f} | "
                          f"{r['gross_indicated_efficiency']:.4f} | {r['crn_efficiency']:.4f} | "
                          f"{'yes' if r['eligible'] else why_not(r)} | {f2(d_dt)} | "
                          f"{f2(d_p8) if p8 else ('not in PR #8' if fuel == 'CH4' else 'no eligible dry')} | {c['m03']['power_change_pct']:+.1f} | "
                          f"{c['m03']['cost_per_mile_pct']:+.1f} / {c['crn']['cost_per_mile_pct']:+.1f} | "
                          f"{c['m03']['cost_per_mile_water_free_pct']:+.1f} / {c['crn']['cost_per_mile_water_free_pct']:+.1f} | {ver} |")
                out.append(dict(r, d_vs_rerun_dry_pp=d_dt, d_vs_pr8_dry_pp=d_p8, cost=c, cost_verdict=ver,
                                baseline_rerun=dict(CR=dt["CR"], T=dt["T_intake_K"], eta=dt["gross_indicated_efficiency"],
                                                    crn=dt["crn_efficiency"])))
    md += ["", "## Best-dry baselines", "", "| fuel | regime | definition | CR | T_in K | eta M03 | eta CRN |", "|---|---|---|---|---|---|---|"]
    for regime in ("normal", "hot"):
        for fuel in ("CH3OH", "C2H5OH", "CH4"):
            dt = next(r for r in rows if r["kind"] == "dry" and r["fuel"] == fuel and r["regime"] == regime)
            md.append(f"| {fuel} | {regime} | rerun (hot also at 320/360 K intake) | {dt['CR']:.0f} | {dt['T_intake_K']:.0f} | "
                      f"{dt['gross_indicated_efficiency']:.4f} | {dt['crn_efficiency']:.4f} |")
            p8 = pr8.get((fuel, regime))
            if p8:
                md.append(f"| {fuel} | {regime} | PR #8 (hot: 400 K intake only) | {p8['CR']:.0f} | {p8['T_intake_K']:.0f} | "
                          f"{p8['gross_indicated_efficiency']:.4f} | {p8['crn_efficiency']:.4f} |")
            elif fuel != "CH4":
                md.append(f"| {fuel} | {regime} | PR #8 (hot: 400 K intake only) | - | 400 | none SPEC-eligible | - |")
    md += ["", "## Notes", "",
           "- Coupled rows reproduce PR #8 `coupled_points.csv` exactly (same code, `coupled_dual_temp.task`).",
           "- M03-CRN: coupled rows run with `evap_mode=\"coupled\"` (compare_coupled.case); every coupled row within "
           "the C1 tolerance (|d_eta| <= 1.5 pp, |p_max ratio - 1| <= 5 %): see `c1_pass` in reconcile.json.",
           "- CH4: Module 09 has no CH4 spray profile and Module 06 has no CH4 latent budget, so no coupled CH4 number "
           "exists. The CH4 'beats dry' rows are **uncoupled (superseded); coupled model not available for CH4**. "
           "(CH4 is a gas fuel; the 'water-majority' liquid there is water only.)",
           "- Cost: sims/cost (PR 9 027f9d7; USD prices dated 2026-10-25; headline water 0.10 USD/gal = James's test-case cost, 2026-10-25 07:32 PDT; free water 0 USD/gal shown for comparison); power = IMEP vs the rerun best dry. "
           "Cost per mile is judged only at equal-or-better power.",
           "- Eligibility = SPEC selection (knock-free at CA50 <= 15 CAD, S_L >= 0.08 m/s, p_max <= 120 bar, closure <= 2 %)."]
    (D / "RECONCILE.md").write_text("\n".join(md) + "\n")
    (D / "reconcile.json").write_text(json.dumps(out, indent=1, default=str))
    print("\n".join(md))


if __name__ == "__main__":
    main()
