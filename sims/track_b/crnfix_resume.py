"""Track B: resume the chains that stopped only because the M03-CRN second engine failed (CVODES
'maximum number of timesteps'), after fixing the cause (saturation-switch chattering, see
engines/m03_cantera/engine.py Case.sat_blend_frac and results/track_b/crnfix/REPORT.md).

Same rule as run.chain_noise: 0.1-pp steps on the chain's dry-baseline hardware, spark re-optimised every
step, continue while Module 03 gain > 3.3e-5 AND M03-CRN gain > 0. Cap 400 steps (same extension as the
C2H5OH/CH3OH hot humid_evap chains, recorded). The failed CRN row is archived, not edited.
Before resuming, the last OK step's CRN is recomputed with the fix and compared with the stored value
(consistency check: the gain at the first new step compares like with like).
Tags: Track B; normal + hot regimes; executed (2 engines); not validated. Grok Bot self-directed job
grokbot-selfdirected-20261025-1410.
"""
import json, sys, time
from multiprocessing import get_context
from pathlib import Path
from sims.track_b import run as R

SRC = R.OUT
DST = R.OUT / "crnfix"
CAP = 400
CHAINS = [("C2H5OH", "normal", "liquid", ""), ("CH3OH", "normal", "liquid", ""),
          ("CH3OH", "normal", "humid_evap", ""), ("CH3OH", "hot", "humid_evap", "h1_hot")]


def prepare(fuel, regime, mode, sub):
    name = f"steps_{fuel}_{regime}{'' if mode == 'liquid' else '_' + mode}__noise.jsonl"
    rows = [json.loads(l) for l in (SRC / sub / name).open()]
    failed = [r for r in rows if r["kind"] == "step" and str(r.get("crn_status", "")).startswith("failed")]
    keep = [r for r in rows if r not in failed]
    DST.mkdir(parents=True, exist_ok=True)
    out = DST / name
    if not out.exists():
        out.write_text("".join(json.dumps(r, default=float) + "\n" for r in keep))
        (DST / name.replace(".jsonl", ".failed_crn_rows.jsonl")).write_text(
            "".join(json.dumps(r, default=float) + "\n" for r in failed))
    last = max((r for r in keep if r["kind"] == "step"), key=lambda r: r["step"])
    chk = R.crn(last)
    return dict(chain=name, archived_failed_steps=[r["step"] for r in failed], last_ok_step=last["step"],
                stored_crn=last.get("crn_efficiency"), recomputed_crn=chk.get("crn_efficiency"),
                diff=(chk.get("crn_efficiency") or float("nan")) - last.get("crn_efficiency"))


def job(j):
    fuel, regime, mode, sub = j
    R.OUT = DST
    t = time.time()
    c = prepare(fuel, regime, mode, sub)
    r = R.chain_noise((fuel, regime, mode, CAP))
    r.update(consistency=c, cap=CAP, seconds=time.time() - t)
    return r


def main(workers=3):
    res = []
    ctx = get_context("spawn")
    with ctx.Pool(workers) as pool:
        for r in pool.imap_unordered(job, CHAINS):
            res.append(r)
            print(f"[crnfix] {r['fuel']}/{r['regime']}/{r['water_mode']} best_w={r['best_w']} steps={r['steps_taken']} "
                  f"d_eta={r['best_eta'] - r['dry_eta']:+.5f} stop={r['stop_reason']} "
                  f"chk_diff={r['consistency']['diff']:.2e} {r['seconds']:.0f}s", flush=True)
            (DST / "summary_crnfix.json").write_text(json.dumps(res, indent=1, default=float))
    print("crnfix done", flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
