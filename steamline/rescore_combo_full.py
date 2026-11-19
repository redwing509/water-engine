"""Score R31 groups before/after adding the R32 CR-midpoint rows (same rule as rescore_r28.py). Claude 2026-11-10.
Model arithmetic only; NOT validation; factory CR WITHHELD. R32 complete."""
import collections, contextlib, io, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
with contextlib.redirect_stdout(io.StringIO()):
    import rlib as R
def rows(stage):
    d = collections.defaultdict(list)
    for f in sorted(HERE.glob(f"points_{stage}*.jsonl")):
        for r in R.load(f):
            d[R.gk(r)].append(r)
    return d
a, b = rows("R31"), rows("R32")
flips = collections.Counter(); out = []
for k in sorted(a, key=str):
    x, y = R.best(a[k]), R.best(a[k] + b.get(k, []))
    gx, gy = bool(R.gain(x)), bool(R.gain(y)); flips[(gx, gy)] += 1
    out.append(dict(group=list(k), n_r32=len(b.get(k, [])), before=x, after=y, gain_before=gx, gain_after=gy))
(HERE / "rescore_R31_R32_full.json").write_text(json.dumps(out, indent=1, default=float))
cov = sum(1 for o in out if o["n_r32"])
top = sorted([o for o in out if o["gain_after"] and o["n_r32"]], key=lambda o: o["after"]["cost"])[:12]
md = ["# R31 + R32 rescore (R32 complete, finished 12:40 PM PST Nov 10)", "Claude 2026-11-10. Model cost arithmetic only, NOT validation; factory CR WITHHELD.", "",
      f"R31 groups: {len(out)}; groups with R32 midpoint rows: {cov}",
      f"gain before -> after: kept {flips[(True, True)]}, lost {flips[(True, False)]}, new {flips[(False, True)]}, none {flips[(False, False)]}", "",
      "| fuel | regime | bore x stroke | rpm | mode | dry->wet CR (w) after | cost/mi % after | power % | before |", "|---|---|---|---|---|---|---|---|---|"]
for o in top:
    g, y, x = o["group"], o["after"], o["before"] or {}
    md.append(f"| {g[0]} | {g[1]} | {g[2]}x{g[3]} | {g[4]} | {g[5]} | {y['dry_CR']}->{y['wet_CR']} ({y['wet_w']}) | {y['cost']:.3f} | {y['power']:.2f} | {x.get('cost', float('nan')):.3f} |")
(HERE / "RESULT_R31_R32_full.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
