"""Track B chain table + cost metric for chains_w030 (Cantera w 0-0.30 flame fit, cap 300), next to the same chains
under the old w <= 0.1 fit. $0.10/gal water = headline, $0 = secondary (sims/cost/prices_20261025.json, dated, cited).
Engine agreement = both engines' d_eta vs dry have the same sign; |M03 - CRN| reported. Failed / unavailable steps are
listed, never dropped. Hot-regime 'vs dry' numbers: pending dryevap verdict (dry baseline has no fuel-evaporation
cooling; see track-ab/box-20261025 dryevap). Tags: Track B; both regimes; executed (2 engines); not validated.
"""
import json
from sims.cost import report as REP, cost as C
from sims.track_b import chains_w030 as W

TB = REP.TB


def main():
    P = C.load_prices()
    md = ["# Track B chains past w 0.1 - Cantera w 0-0.30 flame fit (EXECUTED, 2 engines; NOT validated)", "",
          "Job water-engine-mail-20261025-1830. Rule: 0.1-pp steps, spark re-optimised, continue while Module 03 gain "
          "> 3.3e-5 AND M03-CRN gain > 0; cap 300 (w 0.30 = fit edge -> 'fit-range limited'). Each chain at its own "
          "dry-baseline hardware (CR, T_intake). 'old fit' = same chain under the w <= 0.1 Metghalchi-Keck dilution fit "
          "(stopped at w 0.101 by fit range). Hot-regime d_eta / cost vs dry: **pending dryevap verdict**.", "",
          "## Chain table", "",
          "Variants: **full** = every step recomputed from w 0 with the Cantera fit (self-consistent); **ext** = the old "
          "chain path to w 0.100 kept, step 100 recomputed with the Cantera fit (consistency row, used as prev), then "
          "steps 101..300 with the Cantera fit (the literal 'extend past w 0.1'). d_eta of any point is point-vs-dry "
          "(path independent); only the stop decision depends on the path.", "",
          "| variant | fuel | regime | mode | CR | stop w (new) | stop reason | d_eta pp M03 / CRN (new) | engines agree | "
          "old-fit stop w | old-fit d_eta pp M03 | cost/mile % @$0.10 at best-eff (M03 / CRN) | verdict | failed rows |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    cost_md = ["", "## Cost metric (best-efficiency point and cost-optimal point, equal-or-better power)", "", REP.HDR]
    out = []
    for f, g, m, v in W.jobs():
        p = (W.DST if v == "full" else W.DST_EXT) / f"steps_{f}_{g}{'' if m == 'liquid' else '_' + m}__w030.jsonl"
        if not p.exists():
            md.append(f"| {v} | {f} | {g} | {m} | - | - | NOT RUN | - | - | - | - | cost not computed yet | - | - |")
            continue
        rows = [json.loads(l) for l in p.open()]
        base = rows[0]
        st = [r for r in rows if r.get("kind") == "step"]
        acc = [r for r in st if r.get("decision") == "continue"]
        last = st[-1] if st else None
        best = acc[-1] if acc else base
        stop = last.get("stop_reason") if last and last.get("decision") == "stop" else (
            "cap 300 reached: fit-range limited" if len(st) >= W.CAP else "RUNNING / incomplete")
        fails = [f"{r['w']:.3f}:{r.get('status')}/{r.get('crn_status')}" for r in st
                 if r.get("status") != "computed" or r.get("crn_status") != "ok" or not r.get("eligible")]
        de = 100 * (best["gross_indicated_efficiency"] - base["gross_indicated_efficiency"])
        dc = 100 * ((best.get("crn_efficiency") or 0) - (base.get("crn_efficiency") or 0))
        agree = "yes" if (de > 0) == (dc > 0) else "NO"
        old = [json.loads(l) for l in W.src_file(f, g, m).open()]
        oacc = [r for r in old if r.get("kind") == "step" and r.get("decision") == "continue"]
        ob = oacc[-1] if oacc else base
        c = REP.chain_cost(p, P)
        e = c["eff"] if c else {}
        cpm = REP._two(e, "cost_per_mile_pct") if c else "cost not computed yet"
        md.append(f"| {v} | {f} | {g} | {m} | {base['CR']:.0f} | {best['w']:.3f} | {stop} | {de:+.3f} / {dc:+.3f} | {agree} "
                  f"(diff {abs(de - dc):.3f}) | {ob['w']:.3f} | {100 * (ob['gross_indicated_efficiency'] - base['gross_indicated_efficiency']):+.3f} | "
                  f"{cpm} | {C.verdict(e) if c else '-'} | {', '.join(fails) or 'none'} |")
        if c:
            s = f"{c['n_steps']} ok steps, last {c['last_step']}, {'stopped' if c['stopped'] else 'cap/running'}"
            cost_md.append(REP.line(f, g, m, f"[{v}] best-eff (last accepted)", c["eff_row"], c["eff"], s))
            if c["cost_row"] is not None:
                cost_md.append(REP.line(f, g, m, f"[{v}] cost-optimal w ($0.10)", c["cost_row"], c["cost"], s))
            if c["free_row"] is not None:
                cost_md.append(REP.line(f, g, m, f"[{v}] cost-optimal w ($0 water, secondary)", c["free_row"], c["free"], s))
        out.append(dict(variant=v, fuel=f, regime=g, mode=m, CR=base["CR"], stop_w=best["w"], stop=stop, d_eta_m03_pp=de,
                        d_eta_crn_pp=dc, agree=agree, old_w=ob["w"], failed=fails,
                        cost_eff=e, cost_w=(c or {}).get("cost_row", {}) and c["cost_row"].get("w"),
                        cost=(c or {}).get("cost"), verdict=C.verdict(e) if c else None))
    md += cost_md + ["", REP.prices_md(P) if hasattr(REP, "prices_md") else "",
                     "Caveats: single-engine knock model sets each chain's CR (CR choice: Not yet validated); S_L fit "
                     "from Cantera 1-D premixed flames at IVC state (not engine pressure); ignition correlation has no "
                     "explicit w term (valid_w_range label widened to 0.30 - assumption); hot-regime vs-dry numbers "
                     "pending dryevap verdict."]
    (W.DST / "CHAINS_W030.md").write_text("\n".join(md) + "\n")
    (W.DST / "chains_w030_table.json").write_text(json.dumps(out, indent=1, default=float))
    print("\n".join(md))


if __name__ == "__main__":
    main()
