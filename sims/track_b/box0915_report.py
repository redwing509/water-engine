"""Report for sims/track_b/box0915.py (B2 second knock criterion, B4 CR re-optimisation).
Writes results/track_b/box0915/{points.csv, b2_knock_criteria.csv, b4_cr_reopt.csv, REPORT.md}.
Gain = best eligible wet point minus best eligible dry point under the SAME knock criterion, each at its own
best CR on the grid (re-optimised dry); also vs the chain's own dry baseline (original CR). Engines agree when
the M03-CRN gain has the same sign (and the M03-CRN point is ok). Cost: sims/cost compare() (prices_20261025).
"""
import csv
import json
from pathlib import Path

from sims.cost import cost as COST
from sims.track_b import box0915 as B

OUT = B.OUT


def load():
    rows = {}
    for l in open(OUT / "points.jsonl"):
        r = json.loads(l)
        rows[(r["chain"], r["w"], r["criterion"], r["CR"])] = r
    return list(rows.values())


def best(rows):
    el = [r for r in rows if r.get("eligible")]
    return max(el, key=lambda r: r["gross_indicated_efficiency"]) if el else None


def klcr(rows):
    el = [r["CR"] for r in rows if r.get("eligible")]
    return max(el) if el else None


def crn_gain(a, b):
    if not a or not b or a.get("crn_status") != "ok" or b.get("crn_status") != "ok":
        return None
    return 100 * (a["crn_efficiency"] - b["crn_efficiency"])


def agree(g, gc):
    if gc is None:
        return "no CRN"
    return "agree" if (g > 0) == (gc > 0) else "disagree"


def cost_cols(wet, dry):
    if not wet or not dry:
        return {}
    c = COST.compare(wet, dry)
    m, k = c["m03"] or {}, c["crn"] or {}
    return dict(power_change_pct=m.get("power_change_pct"), fuel_per_work_pct=m.get("fuel_energy_per_work_pct"),
                cost_per_kwh_usd=m.get("cost_usd_per_kwh"), cost_per_kwh_dry_usd=m.get("cost_usd_per_kwh_dry"),
                cost_per_mile_pct=m.get("cost_per_mile_pct"), cost_per_mile_free_pct=m.get("cost_per_mile_water_free_pct"),
                cost_per_mile_pct_crn=k.get("cost_per_mile_pct"), cost_verdict=COST.verdict(c))


def main():
    rows = load()
    keys = sorted({k for r in rows for k in r})
    with open(OUT / "points.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, keys); w.writeheader(); w.writerows(sorted(rows, key=lambda r: (r["chain"], r["criterion"], r["w"], r["CR"])))
    b2, b4 = [], []
    for name, ch in B.CHAINS.items():
        cr_rows = [r for r in rows if r["chain"] == name]
        if not cr_rows:
            continue
        dry0, wb, last = B.chain_best(name)
        wbest = float(wb["w"])
        for crit in ("LW", "DE"):
            D = [r for r in cr_rows if r["criterion"] == crit and r["w"] == 0.0]
            W = [r for r in cr_rows if r["criterion"] == crit and r["w"] == wbest]
            bd, bw = best(D), best(W)
            own_d = next((r for r in D if r["CR"] == float(dry0["CR"])), None)
            g = 100 * (bw["gross_indicated_efficiency"] - bd["gross_indicated_efficiency"]) if bd and bw else None
            gc = crn_gain(bw, bd)
            row = dict(track="B", chain=name, fuel=ch["fuel"], regime=ch["regime"], intake=ch["mode"], criterion=crit,
                       w=wbest, dry_best_CR=bd and bd["CR"], dry_klCR=klcr(D), dry_eta=bd and bd["gross_indicated_efficiency"],
                       dry_eta_crn=bd and bd.get("crn_efficiency"), dry_ca50=bd and bd["ca50_used_deg"],
                       wet_best_CR=bw and bw["CR"], wet_klCR=klcr(W), wet_eta=bw and bw["gross_indicated_efficiency"],
                       wet_eta_crn=bw and bw.get("crn_efficiency"), wet_ca50=bw and bw["ca50_used_deg"],
                       wet_limited_by=bw and bw.get("spark_limited_by"), gain_pp=g, gain_pp_crn=gc,
                       engines=agree(g, gc) if g is not None else "n/a",
                       gain_vs_own_dry_pp=(100 * (bw["gross_indicated_efficiency"] - own_d["gross_indicated_efficiency"])
                                           if bw and own_d and own_d.get("eligible") else None))
            row.update(cost_cols(bw, bd))
            (b2 if True else None).append(row)
            if crit == "LW":
                b4.append(dict(row, n_eligible_wet=sum(1 for r in W if r.get("eligible")),
                               chain_CR=float(dry0["CR"]), chain_gain_pp=100 * (wb["gross_indicated_efficiency"] - dry0["gross_indicated_efficiency"]),
                               chain_last_step_w=last["w"], chain_last_decision=last.get("decision")))
    for fn, data in (("b2_knock_criteria.csv", b2), ("b4_cr_reopt.csv", b4)):
        if data:
            with open(OUT / fn, "w", newline="") as fh:
                w = csv.DictWriter(fh, list(dict.fromkeys(k for d in data for k in d))); w.writeheader(); w.writerows(data)
    f = lambda v, d=4: "-" if v is None else (f"{v:.{d}f}" if isinstance(v, float) else str(v))
    md = ["# Track B box0915: B2 knock criteria, B4 CR re-optimisation (EXECUTED; CRN = verification; NOT validated)", "",
          "| chain | crit | w | dry CR/klCR | dry eta | wet CR/klCR | wet CA50 | wet eta | gain pp M03/CRN | engines | power % | cost/mile % ($0.10 / $0) | verdict |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in b2:
        md.append(f"| {r['chain']} | {r['criterion']} | {r['w']} | {f(r['dry_best_CR'],1)}/{f(r['dry_klCR'],1)} | {f(r['dry_eta'])} | "
                  f"{f(r['wet_best_CR'],1)}/{f(r['wet_klCR'],1)} | {f(r['wet_ca50'],1)} | {f(r['wet_eta'])} | {f(r['gain_pp'],3)}/{f(r['gain_pp_crn'],3)} | "
                  f"{r['engines']} | {f(r.get('power_change_pct'),1)} | {f(r.get('cost_per_mile_pct'),2)} / {f(r.get('cost_per_mile_free_pct'),2)} | {r.get('cost_verdict','-')} |")
    grid_top = max(B.CR_GRID)
    capped = sorted({r["chain"] for r in b2 if r["wet_klCR"] is not None and r["wet_klCR"] >= grid_top})
    md += ["", "**How to read this (labels added 2026-10-25 PM, no number changed):**",
           "* B4 gain = best wet point at its OWN knock-limited CR minus best dry point at the dry knock-limited CR, same knock "
           "criterion. Most of the gain comes from RAISING CR (knock relief by the water), not from water at fixed CR "
           "(fixed-CR chain gains: see `chain_gain_pp` in b4_cr_reopt.csv, +0.8 to +1.8 pp).",
           "* power % = IMEP change; in humid_evap it also includes evaporative charge cooling (T_IVC ~400 -> ~312 K hot, "
           "~+18-20 % trapped mass at fixed p_IVC; no gas-exchange model). Indicated upper bounds, not brake power.",
           f"* CR grid 9-{grid_top:g} (job spec): wet klCR = {grid_top:g} means grid-capped, the true klCR may be higher "
           f"({', '.join(capped) or 'none'}).",
           "* CH3OH_hot_humid_evap LW: the dry knock-limited CR under Livengood-Wu is 8 (vs 10.5 under Douaud-Eyzat), so its "
           "+7.7 pp is mostly CR 8 -> 16; the DE row (+3.0 pp) is the conservative number.",
           "* Status: EXECUTED in Module 03 and cross-checked by M03-CRN (two in-repo engines, same toolchain; M03-CRN has no "
           "knock model, knock limit is Module 03 only). NOT validated against experiment."]
    (OUT / "REPORT.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
