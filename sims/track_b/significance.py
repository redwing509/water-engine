"""Track B cumulative-significance and knock-at-optimum addendum (Claude's guardrail, Oct 24 2026).

For each chain in results/track_b/summary_noise_rule.json:
  total gain vs dry (module 03 and M03-CRN), and a combined 1-sigma band = RSS of
    (a) per-step noise 3.3e-5 * sqrt(steps_taken)
    (b) |module 03 gain - M03-CRN gain| (engine disagreement on the gain)
    (c) heat-transfer model-form band, Woschni vs Hohenberg, 0.4 pp (low) .. 2.5 pp (high) from V1/C2,
        treated as a 1-sigma term on the gain (conservative: it is an absolute-efficiency band).
  "significant" only if gain > 2 sigma; reported for both ends of the model-form band.
Also reports CA50, MBT CA50, knock margin and spark limiter at each chain's stopping w.
"""
import json, math, pathlib
D = pathlib.Path("results/track_b")
NOISE = 3.3e-5
BANDS = {"low": 0.004, "high": 0.025}

def chain_file(c):
    mode = c.get("water_mode", "liquid")
    stem = f"steps_{c['fuel']}_{c['regime']}" + ("" if mode in (None, "", "liquid") else f"_{mode}")
    return D / f"{stem}__noise.jsonl"

def stop_row(c):
    p = chain_file(c)
    if not p.exists():
        return None
    rows = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    rows = [r for r in rows if r.get("status") == "computed" and abs(r.get("w", -1) - c["best_w"]) < 1e-9]
    return rows[-1] if rows else None

def main():
    S = json.loads((D / "summary_noise_rule.json").read_text())
    out = []
    for c in S:
        n = int(c.get("steps_taken", 0))
        g3 = c["best_eta"] - c["dry_eta"]
        gc = c["best_crn"] - c["dry_crn"]
        dis = abs(g3 - gc)
        r = stop_row(c) or {}
        e = dict(c)
        e.update(gain_m03=g3, gain_crn=gc, sigma_noise=NOISE * math.sqrt(n), engine_disagreement=dis)
        for k, b in BANDS.items():
            s = math.sqrt((NOISE * math.sqrt(n)) ** 2 + dis ** 2 + b ** 2)
            e[f"sigma_{k}"] = s
            e[f"significant_2sigma_{k}"] = bool(min(g3, gc) > 2 * s)
        e.update(stop_ca50_deg=r.get("ca50_used_deg"), stop_mbt_ca50_deg=r.get("mbt_ca50_deg"),
                 stop_knock_margin=r.get("knock_margin"), stop_spark_limited_by=r.get("spark_limited_by"),
                 stop_knock=r.get("knock"))
        out.append(e)
    (D / "summary_noise_rule_significance.json").write_text(json.dumps(out, indent=1))
    L = ["# Track B: cumulative significance and knock at the stopping point", "",
         "Combined 1-sigma = RSS(3.3e-5*sqrt(N), |M03 gain - CRN gain|, Woschni-vs-Hohenberg band 0.4 pp or 2.5 pp).",
         "Significant = both engines' gain > 2 sigma. Executed + 2-engine cross-checked only; not validated against experiment.", "",
         "| fuel | regime | water mode | best w | N | gain M03 (pp) | gain CRN (pp) | 2σ low/high (pp) | signif. low/high | CA50 / MBT CA50 | knock margin | spark limit |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    fm = lambda x, s="%.3f": "n/a" if x is None else s % x
    for e in out:
        L.append(f"| {e['fuel']} | {e['regime']} | {e.get('water_mode','liquid')} | {e['best_w']:.3f} | {e.get('steps_taken',0)} | "
                 f"{100*e['gain_m03']:.4f} | {100*e['gain_crn']:.4f} | {200*e['sigma_low']:.3f}/{200*e['sigma_high']:.3f} | "
                 f"{'yes' if e['significant_2sigma_low'] else 'no'}/{'yes' if e['significant_2sigma_high'] else 'no'} | "
                 f"{fm(e['stop_ca50_deg'],'%.1f')} / {fm(e['stop_mbt_ca50_deg'],'%.1f')} | {fm(e['stop_knock_margin'],'%.4f')} | {e['stop_spark_limited_by'] or 'n/a'} |")
    (D / "SIGNIFICANCE.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    main()
