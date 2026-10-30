"""Summary for pr10-fair-highcr (Grok Bot 2026-10-29). klCR = highest CR before first M03 LW knock (integral >= 1);
best = max eta at CR <= klCR with a CRN row; wet vs the same fuel/regime dry DEI at ITS klCR. W/F = w/(1-w); flag > 0.6 (R-WE-22).
Knock engine 2 = full CRECK end-gas (knock_sym at the row CA50) on the limit-bracket rows (BRACKET=1, full.jsonl, added 2026-10-29 20:50 PDT);
klCR stops at the first M03, LW-CRECK or end-gas knock. "EDGE" = klCR is the top of the CR scan (no knock found; true limit is higher).
Liquid dirs were not end-gas checked (humid and liquid rows are identical wherever both ran). Factory CR = klCR - 1 margin. EXECUTED, not validated."""
import json, os, sys, glob, collections
sys.path.insert(0, os.environ.get("WE_BOXQ", "/opt/water-engine/pr10-fair-highcr-20261029/we-boxq"))
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
    for x in jl(f"{d}lw.jsonl"):
        if x["status"] == "ok": crn.setdefault(K(x), {})["LW_CRECK_same_path"] = x.get("LW_CRECK_same_path")
    for x in jl(f"{d}full.jsonl"):
        if x.get("status") == "ok": crn.setdefault(K(x), {})["eg_knock"] = bool(x.get("knock"))
    G = collections.defaultdict(list)
    for l in jl(f"{d}points.jsonl"):
        for r in l["rows"]:
            if r.get("status") != "computed": continue
            r = dict(r, grp=l["grp"]); r.update({a: b for a, b in crn.get(K(r), {}).items() if a.startswith("crn_") or a in ("c1_pass", "pmax_ratio", "LW_CRECK_same_path", "eg_knock")})
            G[(r["grp"], r.get("bound") or "")].append(r)
    def best(rs):
        lim = None
        for r in sorted(rs, key=lambda r: r["CR"]):
            if r["knock_integral_at_xb90"] >= 1.0 or (r.get("LW_CRECK_same_path") or 0) >= 1.0 or r.get("eg_knock"): break
            lim = r["CR"]
        c = [r for r in rs if lim is not None and r["CR"] <= lim and r.get("crn_efficiency") is not None]
        return lim, (max(c, key=lambda r: r["gross_indicated_efficiency"]) if c else None)
    E = lambda lim, rs: f"{lim} EDGE" if rs and lim == max(r["CR"] for r in rs) else f"{lim}"
    dl, dr = best(G.get(("dry", ""), []))
    if dr: out.append(f"| {fuel} | {reg} | dry DEI | 0 | {E(dl, G.get(('dry', ''), []))} | {dr['gross_indicated_efficiency']:.4f}/{dr['crn_efficiency']:.4f} | baseline | 0 | 0 | - |")
    for g in sorted(k for k in G if k[0] != "dry"):
        lim, r = best(G[g])
        if r is None or dr is None: out.append(f"| {fuel} | {reg} | {g[0]} {g[1]} | | {lim} | - | | | | no knock-free 2-engine row |"); continue
        c = C.compare(r, dr); f = lambda k: " / ".join("%+.2f" % c[x][k] if c[x] else "-" for x in ("m03", "crn"))
        wf = r["w"] / (1 - r["w"]); pw = 100 * (r["IMEP_Pa"] / dr["IMEP_Pa"] - 1)
        v = C.verdict(c) + (" [W/F>0.6 R-WE-22]" if wf > 0.6 else "")
        out.append(f"| {fuel} | {reg} | {g[0]} {g[1]} | {wf:.2f} | {E(lim, G[g])} | {r['gross_indicated_efficiency']:.4f}/{r['crn_efficiency']:.4f} | {f('d_eta_pp')} | {pw:+.1f} | {f('cost_per_mile_pct')} | {v} |")
        if pw >= 0 and wf <= 0.6 and c["m03"] and c["m03"]["cost_per_mile_pct"] < 0: rec[fuel].append((c["m03"]["cost_per_mile_pct"], lim, g[0], reg, E(lim, G[g]).endswith("EDGE")))
out += ["", "## Recommended factory CR (cost-best wet case with power >= dry and W/F <= 0.6, klCR - 1 margin; lower of hot/normal)"]
for fuel, v in rec.items():
    v.sort(); br = {}
    for x in v: br.setdefault(x[3], x)   # CR-008: cost-best eligible row PER REGIME, then the lower klCR of those
    fcr = min(x[1] for x in br.values()) - 1; regs = "/".join(f"{k} klCR {x[1]}" for k, x in sorted(br.items()))
    out.append(f"- {fuel}: best {v[0][2]} ({v[0][3]}) klCR {v[0][1]}{' (scan edge, true limit higher)' if v[0][4] else ''} -> factory CR {fcr} (per-regime best: {regs})")
open(f"{H}/RESULT.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
