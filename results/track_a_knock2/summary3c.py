"""Step 3c summary: two-knock-engine klCR (M03 LW and full CRECK end-gas; conservative = min) and the wet-vs-dry
efficiency + cost per mile at those CRs in BOTH efficiency engines (M03, M03-CRN with DEI credit). Hot regime only."""
import json, sys, collections
sys.path.insert(0, "/workspace/we-boxq")
import run3c as M
from sims.cost import cost as C
def jl(p):
    try: return [json.loads(l) for l in open(p) if l.strip()]
    except FileNotFoundError: return []
S3, H = M.S3, M.HERE
K = lambda x: (x["cf"], x["fuel"], x["w"], x["CR"], x.get("intake") or "", x.get("bound") or "")
full = {}
for x in jl(f"{S3}/endgas_full.jsonl") + jl(f"{H}/full.jsonl"):
    if x["status"] == "ok": full.setdefault(K(x)[:4], []).append(bool(x["knock"]))  # step 3 has no bound key
crn = {K(x): x for x in jl(f"{H}/crn.jsonl") if x["status"] == "ok"}
rows = [dict(r, **{k: v for k, v in crn[K(r)].items() if k.startswith("crn_") or k in ("d_eta_pp", "pmax_ratio", "c1_pass")})
        for r in M.allrows() if K(r) in crn]
def klcr(rs, bad):
    ok, lim = sorted(rs, key=lambda r: r["CR"]), None
    for r in ok:
        b = bad(r)
        if b is None: continue
        if b: break
        lim = r["CR"]
    return lim
out = ["# Track A cool_frac step 3c: two knock engines + two efficiency engines, hot cf0.5/cf0.7 (box)", "",
       "klCR M03 = highest CR before the first M03 LW >= 1; klCR E2 = highest CR before the first full CRECK end-gas knock "
       "(rows not run are skipped); used CR = min (both knock engines must agree it is knock-free). Best row = highest M03 eta "
       "with CR <= used CR. Cost at 0.10 USD/gal water (0 USD/gal in brackets), both efficiency engines (M03 / M03-CRN, DEI "
       "latent credit). EXECUTED, not validated. CAVEAT: knock engine 2 is ranking-validated only (absolute +2-2.5 CR offset vs M03 on PRF), so a dry klCR lowered by engine 2 alone makes the dry baseline conservative; do not headline until the offset is resolved. C1 = |d_eta| <= 1.5 pp and |p_max ratio - 1| <= 5 %.", "",
       "| cf | fuel | case | klCR M03 | klCR E2 | used CR | eta M03 / CRN | C1 | d_eta vs dry pp M03 / CRN | power % M03 / CRN | cost/mile % M03 / CRN ($0) | verdict |",
       "|---|---|---|---|---|---|---|---|---|---|---|---|"]
G = collections.defaultdict(list)
for r in rows: G[(r["cf"], r["fuel"], r["kind"] == "dry", r["w"], r.get("intake") or "", r.get("bound") or "")].append(r)
for (cf, fuel) in sorted({g[:2] for g in G}):
    drykey = (cf, fuel, True, 0.0, "", "")
    def best(g):
        rs = G[g]; a = klcr(rs, lambda r: r["knock_integral_at_xb90"] >= 1.0)
        b = klcr(rs, lambda r: None if (cf, fuel, r["w"], r["CR"]) not in full else any(full[(cf, fuel, r["w"], r["CR"])]))
        u = None if a is None or b is None else min(a, b)
        cand = [r for r in rs if u is not None and r["CR"] <= u]
        return a, b, u, (max(cand, key=lambda r: r["gross_indicated_efficiency"]) if cand else None)
    da, db, du, d = best(drykey)
    for g in sorted(k for k in G if k[:2] == (cf, fuel)):
        a, b, u, r = best(g); case = "dry DEI" if g[2] else f"{g[4]} w {g[3]} bound {g[5]}"
        if r is None:
            out.append(f"| {cf} | {fuel} | {case} | {a} | {b} | - | - | - | - | - | - | no knock-free row in both engines |"); continue
        e = f"{r['gross_indicated_efficiency']:.4f} / {r['crn_efficiency']:.4f} (CR {r['CR']})"
        if g[2] or d is None:
            out.append(f"| {cf} | {fuel} | {case} | {a} | {b} | {u} | {e} | {'pass' if r.get('c1_pass') else 'FAIL'} | baseline | | | |"); continue
        c = C.compare(r, d); f = lambda k, s="%+.2f": " / ".join(s % c[x][k] if c[x] else "-" for x in ("m03", "crn"))
        out.append(f"| {cf} | {fuel} | {case} | {a} | {b} | {u} | {e} | {'pass' if r.get('c1_pass') else 'FAIL'} | {f('d_eta_pp')} | "
                   f"{f('power_change_pct', '%+.1f')} | {f('cost_per_mile_pct')} ({f('cost_per_mile_water_free_pct')}) | {C.verdict(c) + ('' if r.get('c1_pass') and d.get('c1_pass') else ' - NOT 2-engine (C1 fail)')} |")
open(f"{H}/RESULT.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))
