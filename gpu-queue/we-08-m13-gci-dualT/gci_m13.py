#!/usr/bin/env python3
"""Celik et al. 2008 GCI (Fs=1.25, r=sqrt2) on M13 metrics from post_m13.py JSON, per regime."""
import json, math, sys, glob, os
R = sys.argv[1]; r = math.sqrt(2.0); Q = ("film_pct_at_ivc", "evaporated_pct_at_ivc", "airborne_drops_pct_at_ivc")
def load(n):
    p = os.path.join(R, "runs", n, "post.json")
    try: return json.loads(open(p).read().strip().splitlines()[-1])
    except Exception: return None
def gci(f1, f2, f3, r21=r, r32=r):
    """Celik et al. 2008 with unequal refinement ratios (actual background-cell ratios, ~1.38-1.40)."""
    e21, e32 = f2 - f1, f3 - f2
    if e21 == 0 or e32 == 0: return {"note": "zero difference"}
    s = 1 if e32 / e21 > 0 else -1; p = 2.0
    for _ in range(500):
        p_new = abs(math.log(abs(e32 / e21)) + math.log((r21 ** p - s) / (r32 ** p - s))) / math.log(r21)
        if abs(p_new - p) < 1e-12: break
        p = p_new
    g = 1.25 * abs(e21 / f1) / (r21 ** p - 1) if f1 and r21 ** p > 1 else None
    return {"p": p, "r21": r21, "r32": r32, "monotone": e32 / e21 > 0, "GCI_fine_pct": None if g is None else 100 * g}
def ncell(n):
    try:
        b = json.load(open(os.path.join(R, "runs", n, "case_meta.json")))["background_cells"]; return b[0] * b[1] * b[2]
    except Exception: return None
out = {"runs": {}, "gci": {}}
for d in sorted(glob.glob(os.path.join(R, "runs", "M13G-*/"))):
    n = os.path.basename(d.rstrip("/")); out["runs"][n] = load(n)
for reg in ("normal", "hot"):
    f = [out["runs"].get("M13G-US20-%s-%s" % (l, reg)) for l in ("fine", "med", "coarse")]
    if all(x and x.get("complete") for x in f):
        N = [ncell("M13G-US20-%s-%s" % (l, reg)) for l in ("fine", "med", "coarse")]
        r21, r32 = ((N[0] / N[1]) ** (1 / 3.0), (N[1] / N[2]) ** (1 / 3.0)) if all(N) else (r, r)
        out["gci"][reg] = {q: gci(f[0][q], f[1][q], f[2][q], r21, r32) for q in Q if all(q in x for x in f)}
    else: out["gci"][reg] = "incomplete runs - no GCI"
json.dump(out, open(os.path.join(R, "gci_summary.json"), "w"), indent=2)
print(json.dumps(out["gci"]))
