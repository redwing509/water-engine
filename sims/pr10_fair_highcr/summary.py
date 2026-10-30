"""Summary for pr10-fair-highcr (Grok Bot 2026-10-29). klCR = highest CR before first M03 LW knock (integral >= 1);
best = max eta at CR <= klCR with a CRN row; wet vs the same fuel/regime dry DEI at ITS klCR. W/F = w/(1-w); flag > 0.6 (R-WE-22).
Knock engine 2 (CRECK end-gas) NOT run here -> klCR is 1-knock-engine; factory CR = klCR - 1 margin. EXECUTED, not validated."""
import json, os, sys, glob, collections
sys.path.insert(0, os.environ.get("WE_BOXQ", "/workspace/we-boxq"))
from sims.cost import cost as C
H = os.environ.get("SUMMARY_DIR") or os.path.dirname(os.path.abspath(__file__))
jl = lambda p: [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []
out = ["# PR 10 high-CR fair rerun (dry DEI at own klCR)", "", __doc__, "",
       "| fuel | regime | case | W/F | klCR | eta M03/CRN | d_eta pp M03/CRN | power % | cost/mile % M03/CRN | verdict |", "|---|---|---|---|---|---|---|---|---|---|"]
rec = collections.defaultdict(list)
for d in sorted(glob.glob(f"{H}/*-*/")):
    fuel, reg = os.path.basename(d.rstrip("/")).split("-")[:2]
    K = lambda x: (x["grp"], x["kind"], x["w"], x["CR"], x.get("T_intake_K"), x.get("bound") or "")
    crn = {K(x): x for x in jl(f"{d}crn.jsonl") if x["status"] == "ok"}
    G = collections.defaultdict(list)
    for l in jl(f"{d}points.jsonl"):
        for r in l["rows"]:
            if r.get("status") != "computed": continue
            r = dict(r, grp=l["grp"]); r.update({a: b for a, b in crn.get(K(r), {}).items() if a.startswith("crn_") or a in ("c1_pass", "pmax_ratio")})
            G[(r["grp"], r.get("bound") or "")].append(r)
    def best(rs):
        lim = None
        for r in sorted(rs, key=lambda r: r["CR"]):
            if r["knock_integral_at_xb90"] >= 1.0: break
            lim = r["CR"]
        c = [r for r in rs if lim is not None and r["CR"] <= lim and r.get("crn_efficiency") is not None]
        return lim, (max(c, key=lambda r: r["gross_indicated_efficiency"]) if c else None)
    dl, dr = best(G.get(("dry", ""), []))
    if dr: out.append(f"| {fuel} | {reg} | dry DEI | 0 | {dl} | {dr['gross_indicated_efficiency']:.4f}/{dr['crn_efficiency']:.4f} | baseline | 0 | 0 | - |")
    for g in sorted(k for k in G if k[0] != "dry"):
        lim, r = best(G[g])
        if r is None or dr is None: out.append(f"| {fuel} | {reg} | {g[0]} {g[1]} | | {lim} | - | | | | no knock-free 2-engine row |"); continue
        c = C.compare(r, dr); f = lambda k, c=c: " / ".join("%+.2f" % c[x][k] if c[x] else "-" for x in ("m03", "crn"))
        wf = r["w"] / (1 - r["w"]); pw = 100 * (r["IMEP_Pa"] / dr["IMEP_Pa"] - 1)
        v = C.verdict(c) + (" [W/F>0.6 R-WE-22]" if wf > 0.6 else "")
        out.append(f"| {fuel} | {reg} | {g[0]} {g[1]} | {wf:.2f} | {lim} | {r['gross_indicated_efficiency']:.4f}/{r['crn_efficiency']:.4f} | {f('d_eta_pp')} | {pw:+.1f} | {f('cost_per_mile_pct')} | {v} |")
        if pw >= 0 and wf <= 0.6 and c["m03"] and c["m03"]["cost_per_mile_pct"] < 0: rec[fuel].append((c["m03"]["cost_per_mile_pct"], lim, g[0], reg, False, {"rows": G[g], "dry": dr}))
out += ["", "## Recommended factory CR (cost-best wet case per regime with power >= dry and W/F <= 0.6; factory CR = lower hot/normal klCR - 1;",
        "## both regimes required (CR-015/016) and cost/power/W-F re-tested on the rows AT the factory CR (CR-017/018), else WITHHELD)"]
for fuel, v in sorted(rec.items()):
    v.sort(key=lambda x: x[0]); br = {}
    for x in v: br.setdefault(x[3], x)   # CR-008: cost-best eligible row PER REGIME, then the lower klCR of those
    regs = "/".join(f"{k} klCR {x[1]}" for k, x in sorted(br.items()))
    miss = {"hot", "normal"} - set(br)
    if miss: out.append(f"- {fuel}: factory CR WITHHELD - no eligible row for regime(s) {'/'.join(sorted(miss))} (have: {regs})"); continue
    cap = min(x[1] for x in br.values()) - 1; fcr, ev, bad0 = None, [], None
    def chk(cr):   # cost/power/W-F evidence for every regime AT this CR (CR-017/018)
        ev, bad = [], []
        for k, x in sorted(br.items()):
            rows, dry = x[-1]["rows"], x[-1]["dry"]
            rf = [r for r in rows if r["CR"] == cr and r.get("crn_efficiency") is not None]
            if not rf: bad.append(f"{k}: no CRN row at CR {cr}"); continue
            rf = max(rf, key=lambda r: r["gross_indicated_efficiency"]); cf = C.compare(rf, dry)
            pwf = 100 * (rf["IMEP_Pa"] / dry["IMEP_Pa"] - 1); wff = rf["w"] / (1 - rf["w"])
            if not (pwf >= 0 and wff <= 0.6 and cf["m03"] and cf["m03"]["cost_per_mile_pct"] < 0):
                bad.append(f"{k}: at CR {cr} power {pwf:+.1f}% W/F {wff:.2f}"); continue
            ev.append(f"{k} {x[2]} cost {cf['m03']['cost_per_mile_pct']:+.2f}% power {pwf:+.1f}%")
        return ev, bad
    for cr in range(cap, 0, -1):   # highest CR <= klCR-1 with passing evidence in BOTH regimes (scan may skip odd CRs)
        ev, bad = chk(cr)
        if bad0 is None: bad0 = bad
        if not bad: fcr = cr; break
    bad = [] if fcr is not None else (bad0 or ["no CR"])
    if bad: out.append(f"- {fuel}: factory CR WITHHELD - no CR <= {cap} has passing evidence in both regimes ({'; '.join(bad)}) (per-regime best: {regs})"); continue
    edge = " (scan edge, true limit higher)" if v[0][4] else ""
    note = "" if fcr == cap else " (klCR-1 = %d has no passing evidence: %s)" % (cap, "; ".join(bad0))
    out.append(f"- {fuel}: best {v[0][2]} ({v[0][3]}) klCR {v[0][1]}{edge} -> factory CR {fcr}{note} (per-regime best: {regs}; at CR {fcr}: {'; '.join(ev)})")
open(f"{H}/RESULT.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
