"""Track B cumulative-significance and knock-at-optimum addendum (Claude's guardrails, Oct 24 2026).

For each chain in results/track_b/summary_noise_rule.json: total gain vs dry from Module 03 and M03-CRN,
and two significance tests (2 sigma, both engines' gain must exceed it):

PRIMARY - gain-difference test (Claude 20:15 PDT, recommended):
  1-sigma = RSS of
    (a) per-step noise 3.3e-5 * sqrt(steps_taken)
    (b) |Module 03 gain - M03-CRN gain|            (engine-to-engine gap on the gain)
    (c) |gain_CRN(Woschni) - gain_CRN(Hohenberg)|   (heat-transfer model-form error ON THE GAIN; the absolute
        Woschni-vs-Hohenberg offset largely cancels in a same-model wet-minus-dry difference)
  Term (c) re-runs the chain's dry point and stopping point in M03-CRN with heat_transfer="hohenberg".
  When the chain stopped at w = 0 the stopping point IS the dry point, so every gain and term (c) are 0 exactly.

SECONDARY - conservative absolute-band test (a478dc5):
  (c) replaced by the absolute-efficiency Woschni-vs-Hohenberg band 0.4 pp (low) / 2.5 pp (high) from V1/C2.

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


def rows_of(c):
    p = chain_file(c)
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def stop_row(rows, c):
    rr = [r for r in rows if r.get("status") == "computed" and abs(r.get("w", -1) - c["best_w"]) < 1e-9]
    return rr[-1] if rr else None


def dry_row(rows):
    rr = [r for r in rows if r.get("kind") == "dry_baseline" and r.get("status") == "computed"]
    return rr[-1] if rr else None


def ht_gain_diff(c, rows, gc_woschni):
    """|gain_CRN(Woschni) - gain_CRN(Hohenberg)|; returns (diff, gain_hohenberg, note)."""
    if abs(c["best_w"]) < 1e-12:
        return 0.0, 0.0, "stopped at w=0: stop point = dry point, gain-difference 0 exactly"
    d, s = dry_row(rows), stop_row(rows, c)
    if d is None or s is None or gc_woschni is None:
        return None, None, "dry or stopping row missing"
    from sims.track_b.run import crn
    a, b = crn(d, heat_transfer="hohenberg"), crn(s, heat_transfer="hohenberg")
    if a.get("crn_status") != "ok" or b.get("crn_status") != "ok":
        return None, None, f"Hohenberg CRN failed: {a.get('crn_status')} / {b.get('crn_status')}"
    gh = b["crn_efficiency"] - a["crn_efficiency"]
    return abs(gc_woschni - gh), gh, "M03-CRN Hohenberg re-run of dry + stop points"


def main():
    S = json.loads((D / "summary_noise_rule.json").read_text())
    out = []
    for c in S:
        n = int(c.get("steps_taken", 0))
        g3 = c["best_eta"] - c["dry_eta"]
        gc = (c["best_crn"] - c["dry_crn"]) if c.get("best_crn") is not None and c.get("dry_crn") is not None else None
        dis = abs(g3 - gc) if gc is not None else None
        rows = rows_of(c)
        r = stop_row(rows, c) or {}
        e = dict(c)
        sn = NOISE * math.sqrt(n)
        e.update(gain_m03=g3, gain_crn=gc, sigma_noise=sn, engine_disagreement=dis)
        hd, gh, note = ht_gain_diff(c, rows, gc)
        e.update(gain_crn_hohenberg=gh, ht_gain_difference=hd, ht_gain_difference_note=note)
        if hd is not None and dis is not None:
            s = math.sqrt(sn ** 2 + dis ** 2 + hd ** 2)
            e["sigma_gaindiff"] = s
            e["significant_2sigma_gaindiff"] = bool(min(g3, gc) > 2 * s)
        else:
            e["sigma_gaindiff"], e["significant_2sigma_gaindiff"] = None, None
        for k, b in BANDS.items():
            s = math.sqrt(sn ** 2 + (dis or 0) ** 2 + b ** 2)
            e[f"sigma_{k}"] = s
            e[f"significant_2sigma_{k}"] = bool(gc is not None and min(g3, gc) > 2 * s)
        e.update(stop_ca50_deg=r.get("ca50_used_deg"), stop_mbt_ca50_deg=r.get("mbt_ca50_deg"),
                 stop_knock_margin=r.get("knock_margin"), stop_spark_limited_by=r.get("spark_limited_by"),
                 stop_knock=r.get("knock"))
        out.append(e)
    (D / "summary_noise_rule_significance.json").write_text(json.dumps(out, indent=1))
    fm = lambda x, s="%.3f": "n/a" if x is None else s % x
    yn = lambda x: "n/a" if x is None else ("yes" if x else "no")
    L = ["# Track B: cumulative significance and knock at the stopping point", "",
         "Two tests; both require BOTH engines' gain > 2 sigma. Executed + 2-engine cross-checked only; not validated against experiment.", "",
         "* **PRIMARY: gain-difference test** (Claude 20:15 PDT, recommended). 1-sigma = RSS(3.3e-5*sqrt(N), |M03 gain - CRN gain|, "
         "|CRN gain (Woschni) - CRN gain (Hohenberg)|). The heat-transfer term is the model-form error on the *gain*; the absolute "
         "Woschni/Hohenberg offset mostly cancels in a same-model wet-minus-dry difference.",
         "* **SECONDARY: conservative absolute-band test** (a478dc5). Same, but the heat-transfer term is the absolute-efficiency band "
         "0.4 pp (low) / 2.5 pp (high) from V1/C2.", "",
         "| fuel | regime | water mode | best w | N | gain M03 (pp) | gain CRN W (pp) | gain CRN H (pp) | **2σ gain-diff (pp)** | **signif. (primary)** | 2σ band low/high (pp) | signif. low/high | CA50 / MBT CA50 | knock margin | spark limit |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for e in out:
        sg = e["sigma_gaindiff"]
        L.append(f"| {e['fuel']} | {e['regime']} | {e.get('water_mode','liquid')} | {e['best_w']:.3f} | {e.get('steps_taken',0)} | "
                 f"{100*e['gain_m03']:.4f} | {fm(None if e['gain_crn'] is None else 100*e['gain_crn'],'%.4f')} | "
                 f"{fm(None if e['gain_crn_hohenberg'] is None else 100*e['gain_crn_hohenberg'],'%.4f')} | "
                 f"{fm(None if sg is None else 200*sg,'%.4f')} | {yn(e['significant_2sigma_gaindiff'])} | "
                 f"{200*e['sigma_low']:.3f}/{200*e['sigma_high']:.3f} | "
                 f"{yn(e['significant_2sigma_low'])}/{yn(e['significant_2sigma_high'])} | "
                 f"{fm(e['stop_ca50_deg'],'%.1f')} / {fm(e['stop_mbt_ca50_deg'],'%.1f')} | {fm(e['stop_knock_margin'],'%.4f')} | {e['stop_spark_limited_by'] or 'n/a'} |")
    notes = sorted({e["ht_gain_difference_note"] for e in out})
    L += ["", "Heat-transfer gain-difference notes: " + "; ".join(notes)]
    (D / "SIGNIFICANCE.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
