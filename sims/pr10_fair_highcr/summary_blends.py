"""PRF91/E85 Track B (symmetric DEI) CR scan, Grok Bot 2026-10-29. klCR_M03 = highest CR before first M03 knock/ineligible;
klCR_EG = highest CR before first CRECK end-gas knock (knock_sym endgas_check at the row's own CA50, bracket rows only);
klCR = min. Best = row at klCR vs dry DEI (w0) at ITS klCR. EXECUTED, not validated."""
import json, sys, collections
sys.path.insert(0, "/workspace/we-boxq")
from sims.cost import cost as C
H = "/workspace/self-jobs/pr10-blends"
rows = [json.loads(l) for l in open(f"{H}/points.jsonl")]
EG = {e["_key"]: e for e in map(json.loads, open(f"{H}/endgas.jsonl"))}
G = collections.defaultdict(list)
for r in rows:
    f, reg, m, w, cr = r["_key"].split("|"); G[(f, reg, m, float(w))].append(r)
def kl(rs):
    rs = sorted(rs, key=lambda r: r["CR"]); lm = le = None; top = rs[-1]["CR"]; egk = False
    for r in rs:
        if r["knock_integral_at_xb90"] >= 1 or not r.get("eligible"): break
        lm = r["CR"]
    for r in rs:
        e = EG.get(r["_key"])
        if e and e["knock"]: egk = True; break
        if e or (lm is not None and r["CR"] <= lm): le = r["CR"]
    lim = lm if le is None else min(lm, le)
    return lim, lm, le, egk, lm == top, next((r for r in rs if r["CR"] == lim), None)
out = []
for f in ("PRF91", "E85"):
    for reg in ("hot", "normal"):
        dl, dm, de, dk, dedge, dr = kl(G[(f, reg, "liquid", 0.0)])
        out.append(dict(fuel=f, regime=reg, case="dry DEI", wf=0, kl=dl, klm=dm, edge=dedge, eta=dr["gross_indicated_efficiency"], etac=dr["crn_efficiency"]))
        for m in ("humid_evap", "liquid"):
            for w in (0.1, 0.2, 0.3):
                l, lm, le, k, edge, r = kl(G[(f, reg, m, w)])
                c = C.compare(r, dr); pw = 100 * (r["IMEP_Pa"] / dr["IMEP_Pa"] - 1)
                out.append(dict(fuel=f, regime=reg, case=f"{m} w{w}", wf=w / (1 - w), kl=l, klm=lm, edge=edge, eta=r["gross_indicated_efficiency"],
                                etac=r["crn_efficiency"], d=[c[e]["d_eta_pp"] if c[e] else None for e in ("m03", "crn")], pw=pw,
                                cpm=[c[e]["cost_per_mile_pct"] if c[e] else None for e in ("m03", "crn")], v=C.verdict(c)))
json.dump(out, open(f"{H}/summary.json", "w"), indent=1)
for o in out: print(o)
