"""Track B cost metric for the chains resumed after the M03-CRN fix (results/track_b/crnfix), compared with the
same chains as they stood before the fix (stopped on CRN failure).  $0.10/gal water = headline, $0 = secondary.
Uses sims.cost.report.chain_cost / sims.cost.cost (prices_20261025.json).  Tags: Track B; executed; not validated.
"""
import json
from pathlib import Path
from sims.cost import report as REP, cost as C

TB = REP.TB
NAMES = [("C2H5OH", "normal", "liquid", ""), ("CH3OH", "normal", "liquid", ""),
         ("CH3OH", "normal", "humid_evap", ""), ("CH3OH", "hot", "humid_evap", "h1_hot")]


def fname(f, r, m):
    return f"steps_{f}_{r}{'' if m == 'liquid' else '_' + m}__noise.jsonl"


def main():
    P = C.load_prices()
    md = ["# Track B chains resumed after the M03-CRN fix - cost metric (EXECUTED, 2 engines; NOT validated)", "",
          "Headline water $0.10/gal, secondary $0. Each row vs the chain's own dry baseline (same fuel, same regime, "
          "same hardware). 'before' = chain as stopped by the CRN failure; 'after' = resumed with the fix.", "",
          REP.HDR]
    out = []
    for f, r, m, sub in NAMES:
        for label, path in (("before", TB / sub / fname(f, r, m)), ("after", TB / "crnfix" / fname(f, r, m))):
            if not path.exists():
                continue
            c = REP.chain_cost(path, P)
            if c is None:
                continue
            st = f"{label}: {c['n_steps']} steps, last {c['last_step']}, {'stopped' if c['stopped'] else 'running/cap'}"
            md.append(REP.line(f, r, m, f"{label} best-eff (last accepted)", c["eff_row"], c["eff"], st))
            if c["cost_row"] is not None:
                md.append(REP.line(f, r, m, f"{label} cost-optimal w ($0.10)", c["cost_row"], c["cost"], st))
            out.append(dict(fuel=f, regime=r, mode=m, label=label, eff_w=c["eff_row"].get("w"), eff=c["eff"],
                            cost_w=(c["cost_row"] or {}).get("w"), cost=c["cost"], n_steps=c["n_steps"],
                            last_step=c["last_step"], stopped=c["stopped"]))
    md += ["", "Note (PR 11 review item 2, VERIFIED by fresh-process recompute in mode_check_CH3OH_normal.json): the CH3OH "
           "normal liquid and humid_evap 'after' rows are identical by physics, not by a resume bug. Intake evaporation "
           "is wet-bulb (saturation) limited; from w 0.140 the liquid mode's 0.5*w also exceeds the intake capacity, so "
           "both modes evaporate the same water and give the same charge (M03 eta diff < 1e-12). Below w 0.140 they "
           "differ (humid_evap up to +0.084 pp better at w 0.080). The 'before' best w (0.132 vs 0.080) were where each "
           "chain hit the CRN failure, not optima. Count the two chains as ONE result.",
           "", "Track B chains run at the fuel/regime dry-baseline CR chosen by the Module 03 knock model only "
           "(single-engine knock); CR choice: Not yet (single-engine knock) validated."]
    (TB / "crnfix" / "COST.md").write_text("\n".join(md) + "\n")
    (TB / "crnfix" / "cost_crnfix.json").write_text(json.dumps(out, indent=1, default=float))
    print("\n".join(md))


if __name__ == "__main__":
    main()
