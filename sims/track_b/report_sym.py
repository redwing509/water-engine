"""Report for the Track B symmetric DEI rebase (results/track_b/symmetric_dei/).
Baseline for every chain = its own w0 row (DEI dry, same fuel/regime/hardware). Cost metric: sims/cost.
Output: SYMMETRIC_DEI.md + symmetric_dei_table.csv. Executed, numerically cross-checked, not validated."""
import csv, json, sys
from pathlib import Path

from sims.cost import cost as C
from sims.cost import report as CR
from sims.track_b import chains_sym as CS

OUT = CS.OUT


def _g(c, eng, k):
    v = (c.get(eng) or {}).get(k)
    return None if v is None else round(v, 3)


def build(knock_file=None):
    knock = {}
    if knock_file and Path(knock_file).exists():
        for l in open(knock_file):
            e = json.loads(l)
            knock[(e["fuel"], e["regime"], e.get("water_mode"), round(float(e["w"] or 0), 3))] = e
    hw = json.loads((OUT / "dei_hardware.json").read_text())
    rows, notes = [], []
    for f in CS.FUELS:
        for g in CS.REGIMES:
            for m in CS.MODES:
                p = OUT / CS.chain_name(f, g, m, 0)
                if not p.exists():
                    notes.append(f"{f} {g} {m}: not run (no eligible DEI dry baseline or not reached)")
                    continue
                cc = CR.chain_cost(p)
                if cc is None:
                    notes.append(f"{f} {g} {m}: no dry_baseline row"); continue
                stop = next((r.get("stop_reason") for r in CR.read_jsonl(p) if r.get("decision") == "stop"), None)
                e, cr_ = cc["eff"], cc["cost"]
                ew = round(float(cc["eff_row"].get("w") or 0), 3)
                k = knock.get((f, g, m, ew))
                rows.append(dict(
                    track="B", fuel=f, regime=g, mode=m, CR=hw[f"{f}/{g}"]["CR"],
                    T_intake_K=CS.T_INTAKE[g], wall_K=cc["dry"].get("chamber_wall_K"),
                    steps=cc["last_step"], stop_w=ew, stop_reason=stop or ("running" if not cc["stopped"] else ""),
                    d_eta_pp_m03=_g(e, "m03", "d_eta_pp"), d_eta_pp_crn=_g(e, "crn", "d_eta_pp"),
                    power_pct_m03=_g(e, "m03", "power_change_pct"), power_pct_crn=_g(e, "crn", "power_change_pct"),
                    fuel_per_work_pct_m03=_g(e, "m03", "fuel_volume_per_work_pct"),
                    cost_kwh_pct_m03=_g(e, "m03", "cost_per_kwh_pct"),
                    cost_mile_pct_m03=_g(e, "m03", "cost_per_mile_pct"), cost_mile_pct_crn=_g(e, "crn", "cost_per_mile_pct"),
                    cost_mile_free_pct_m03=_g(e, "m03", "cost_per_mile_water_free_pct"),
                    cost_mile_free_pct_crn=_g(e, "crn", "cost_per_mile_water_free_pct"),
                    verdict=C.verdict(e), cost_min_w=round(float(cc["cost_row"].get("w") or 0), 3),
                    cost_min_pct_m03=_g(cr_, "m03", "cost_per_mile_pct"), cost_min_verdict=C.verdict(cr_),
                    endgas_knock=None if k is None else k.get("knock"),
                    both_knock_engines_pass=None if k is None else k.get("row_pass")))
    with open(OUT / "symmetric_dei_table.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ["none"])
        w.writeheader(); [w.writerow(r) for r in rows]
    P = lambda a, b: f"{'-' if a is None else f'{a:+.3f}'} / {'-' if b is None else f'{b:+.3f}'}"
    md = ["# Track B symmetric DEI rebase (fuel evaporated by DEI at every step incl. w0)", "",
          "Executed, numerically cross-checked (Module 03 + M03-CRN), not validated. Baseline = each chain's own "
          "w0 DEI dry row at the fuel/regime DEI rule CR. normal = wall 450 K, T_intake 320 K (~90 C coolant); "
          "hot = wall 520 K, T_intake 400 K. Cost: $0.10/gal water headline, $0 secondary.", "",
          "| fuel | regime | mode | CR | stop w | gain vs DEI pp (M03/CRN) | power % (M03/CRN) | cost/mile % $0.10 (M03/CRN) | "
          "cost/mile % $0 (M03/CRN) | cost-min w | verdict | knock 2-engine |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['fuel']} | {r['regime']} | {r['mode']} | {r['CR']} | {r['stop_w']:.3f} | "
                  f"{P(r['d_eta_pp_m03'], r['d_eta_pp_crn'])} | {P(r['power_pct_m03'], r['power_pct_crn'])} | "
                  f"{P(r['cost_mile_pct_m03'], r['cost_mile_pct_crn'])} | {P(r['cost_mile_free_pct_m03'], r['cost_mile_free_pct_crn'])} | "
                  f"{r['cost_min_w']:.3f} | {r['verdict']} | "
                  f"{'-' if r['both_knock_engines_pass'] is None else ('pass' if r['both_knock_engines_pass'] else 'FAIL')} |")
    md += [""] + [f"- {n}" for n in notes]
    (OUT / "SYMMETRIC_DEI.md").write_text("\n".join(md) + "\n")
    return rows, notes


if __name__ == "__main__":
    rows, notes = build(sys.argv[1] if len(sys.argv) > 1 else None)
    print((OUT / "SYMMETRIC_DEI.md").read_text())
