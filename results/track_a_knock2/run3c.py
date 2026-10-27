"""Track A cool_frac step 3c (follow-up of step 3, Claude reply 1235): close the gaps in knock engine 2 on the hot
cf0.5/cf0.7 rows so the dry and wet knock-limited CRs are bracketed in BOTH knock engines, then get the second
efficiency engine (M03-CRN) on every row near the limits. Read-only on step 3 data; own outputs here.
  full : full CRECK end-gas chemistry on dry C2H5OH CR 8-12, dry CH3OH CR 18-20, wet humid w 0.55 CR 25-26
  lw   : CRECK-tau/D-E LW on dry C2H5OH CR 8-11 and wet humid w 0.55/0.6 CR 26
  crn  : M03-CRN efficiency/p_max (sims.track_b.run.crn) on dry CR 8-20 and wet w 0.55/0.6 CR 18-26
Each row run once, failures recorded, never retried. Usage: run3c.py <full|lw|crn> <n_workers>"""
import json, os, sys, time
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, "/workspace/we-boxq"); sys.path.insert(0, "/workspace/self-jobs/coolfrac-step3")
from sims.track_b import knock_diag as KD
from sims.track_b import run as R
from sims.track_b.chains_sym import crn_sym
KD.ON.setdefault("CH3OH", 108.7); KD.ON.setdefault("C2H5OH", 108.6)
S3 = "/workspace/self-jobs/coolfrac-step3"; HERE = os.path.dirname(os.path.abspath(__file__))

def allrows():
    out = []
    for cf in ("05", "07"):
        for l in open(f"{S3}/cf{cf}.points.jsonl"):
            for r in json.loads(l)["rows"]:
                if r["regime"] == "hot" and r["status"] == "computed" and r["fuel"] in ("CH3OH", "C2H5OH") and (
                        r["kind"] == "dry" or (r["w"] in (0.55, 0.6) and "humid" in str(r.get("intake")))):
                    out.append(dict(r, cf=cf))
    return out

def sel(mode, r):
    dry, c, f = r["kind"] == "dry", r["CR"], r["fuel"]
    if mode == "full":
        return (dry and f == "C2H5OH" and 8 <= c <= 12) or (dry and f == "CH3OH" and 18 <= c <= 20) or (not dry and r["w"] == 0.55 and c in (25, 26))
    if mode == "lw":
        return (dry and f == "C2H5OH" and 8 <= c <= 11) or (not dry and c == 26)
    return (dry and 8 <= c <= 20) or (not dry and 18 <= c <= 26)

KEEP = ("cf", "bound", "fuel", "kind", "intake", "w", "CR", "ca50_used_deg", "knock", "knock_limited", "knock_integral_at_xb90",
        "gross_indicated_efficiency", "IMEP_Pa", "peak_pressure_Pa")

def one(a):
    mode, r = a; keep = {k: r.get(k) for k in KEEP}; t = time.time()
    try:
        keep.update(crn_sym(r) if mode == "crn" else KD.endgas(r, r["ca50_used_deg"], 0.0, full=(mode == "full"), creck=True))
        keep["status"] = "ok" if keep.get("crn_status", "ok") == "ok" else keep["crn_status"]
    except Exception as e:
        keep["status"] = f"failed: {type(e).__name__}: {e}"
    keep["seconds"] = time.time() - t
    return keep

if __name__ == "__main__":
    mode, n = sys.argv[1], int(sys.argv[2]); outp = f"{HERE}/{mode}.jsonl"
    todo = [r for r in allrows() if sel(mode, r)]
    if os.environ.get("SMOKE"): todo = todo[:1]
    done = {(x["cf"], x["fuel"], x["w"], x["CR"], x.get("intake"), x.get("bound")) for x in KD.jl(outp)}
    todo = [r for r in todo if (r["cf"], r["fuel"], r["w"], r["CR"], r.get("intake"), r.get("bound")) not in done]
    todo.sort(key=lambda r: -r["CR"])  # longest (high CR) first
    print(mode, len(todo), "rows", flush=True)
    with ProcessPoolExecutor(n, max_tasks_per_child=1) as ex, open(outp, "a") as fh:
        for x in ex.map(one, [(mode, r) for r in todo]):
            fh.write(json.dumps(x, default=str) + "\n"); fh.flush()
            print(mode, x["cf"], x["fuel"], x["w"], x["CR"], x.get("knock"), x.get("crn_efficiency"), x["status"][:80], round(x["seconds"]), flush=True)
