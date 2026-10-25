"""Track B B1 sign test (R-WE-09): re-run each positive optimum with CA50 held at the dry setting.

Split of the gain: fixed-spark share (charge cooling / dilution / gamma, "I3") vs knock-relief /
spark-advance share (= total - fixed-spark). Module 03 + M03-CRN (Woschni), same hardware/regime.
Labels: executed, 2-engine (M03 + M03-CRN). Not literature-compared or validated.
"""
import glob, json, math, sys
from pathlib import Path
from sims.track_b import run as R

import os
OUT = Path(os.environ.get("SIGN_OUT", "results/track_b/sign_test.json"))


def positives(min_pp=0.05):
    rows = []
    for f in sorted(glob.glob("results/track_b/steps_*__noise.jsonl")):
        recs = [json.loads(l) for l in open(f) if l.strip()]
        recs = [r for r in recs if r.get("status") == "computed" and r.get("eligible") and r.get("kind") in ("dry_baseline", "step")]
        dry = [r for r in recs if r.get("w", 0) == 0]
        if not dry:
            continue
        dry = dry[0]
        best = max(recs, key=lambda r: r["gross_indicated_efficiency"])
        gain = 100 * (best["gross_indicated_efficiency"] - dry["gross_indicated_efficiency"])
        if best["w"] > 0 and gain >= min_pp:
            rows.append((f, dry, best, gain))
    return rows


def fixed_point(fuel, regime, cr, T, w, mode, ca50_deg):
    m = R.module03()
    saved = m.retard_search

    def fixed(evaluate, par):
        r = dict(evaluate(ca50_deg * R.RAD))
        R.spark_optimise.last = dict(mbt_ca50_deg=None, spark_limited_by="held_at_dry",
                                     mbt_efficiency=None)
        return r
    m.retard_search = fixed
    try:
        return R.point(fuel, regime, cr, T, w, mode)
    finally:
        m.retard_search = saved


def main():
    out = []
    for f, dry, best, gain in positives():
        mode = best.get("water_mode") or "liquid"
        r = fixed_point(best["fuel"], best["regime"], best["CR"], best["T_intake_K"], best["w"], mode,
                        dry["ca50_used_deg"])
        r.update(R.crn(r))
        fx = 100 * (r["gross_indicated_efficiency"] - dry["gross_indicated_efficiency"])
        fx_crn = 100 * (r["crn_efficiency"] - dry["crn_efficiency"]) if r.get("crn_status") == "ok" else None
        tot_crn = 100 * (best["crn_efficiency"] - dry["crn_efficiency"])
        row = dict(file=f, fuel=best["fuel"], regime=best["regime"], mode=mode, w_best=best["w"],
                   ca50_dry=dry["ca50_used_deg"], ca50_best=best["ca50_used_deg"],
                   gain_total_pp_m03=gain, gain_total_pp_crn=tot_crn,
                   gain_fixed_spark_pp_m03=fx, gain_fixed_spark_pp_crn=fx_crn,
                   knock_relief_share_m03=(gain - fx) / gain if gain else None,
                   knock_at_fixed_spark=r["knock"], knock_margin_fixed=r.get("knock_margin"),
                   label="knock-relief / spark-advance gain" if fx <= 3.3e-3 else "partly charge cooling / I3",
                   tags="Track B; executed; 2-engine")
        out.append(row)
        print(json.dumps(row), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
