"""H1 (Track B, hot regime): find a SPEC-eligible dry baseline for the fuels that have none at CR 9..24
(PRF87, PRF91, PRF97, E10, CH3OH; every knock-free point needs CA50 > 15 CAD there) by extending the
compression-ratio grid down to CR 6, then run the same noise-rule water chains (0.1-pp steps, continue
while the Module 03 gain > 3.3e-5 AND the M03-CRN gain is positive, cap 100 -> 200) in all three water
modes. Same physics, eligibility and spark optimiser as run.py; only the CR grid is extended.
Also extends the C2H5OH/hot/humid_evap chain (still gaining at the 200-step cap) to 400 steps.
Tags: Track B; hot regime; executed; 2-engine (Module 03 + M03-CRN). Grok Bot, 2026-10-25.
"""
import json, sys, time
from multiprocessing import get_context
from pathlib import Path
from sims.track_b import run as R

ORIG = R.OUT
H1 = ORIG / "h1_hot"
FUELS = ("PRF87", "PRF91", "PRF97", "E10", "CH3OH")
LOW_CRS = (6, 7, 8)
MODES = ("liquid", "humid_evap", "humid_ambient")
T_HOT = R.REGIMES["hot"]["T_intake"][0]


def _dry(task):
    return R.point(*task)


def _chain(job):
    fuel, mode = job
    R.OUT = H1
    return R.chain_noise_full((fuel, "hot", mode))


def _ext(_):
    R.OUT = ORIG
    return dict(R.chain_noise(("C2H5OH", "hot", "humid_evap", 400)), cap_raised_to=400)


def main(workers=6):
    H1.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    ctx = get_context("spawn")
    old = json.loads((R.OUT / "dry_sweep.json").read_text())
    tasks = [(f, "hot", cr, T_HOT, 0.0) for f in FUELS for cr in LOW_CRS]
    with ctx.Pool(workers) as pool:
        ext = pool.apply_async(_ext, (None,))
        new = list(pool.imap_unordered(_dry, tasks))
        (H1 / "dry_low_cr.json").write_text(json.dumps(new, indent=1, default=float))
        print(f"[h1 dry] {len(new)} low-CR points {time.time() - t0:.0f}s", flush=True)
        jobs, summary = [], dict(fuels={}, rule="noise_3.3e-5", low_crs=LOW_CRS)
        for f in FUELS:
            rows = [r for r in old + new if r["fuel"] == f and r["regime"] == "hot"]
            el = [r for r in rows if r["eligible"]]
            kf = [r for r in rows if r["status"] == "computed" and not r["knock"]]
            ref = max(kf, key=lambda r: r["gross_indicated_efficiency"]) if kf else None
            if not el:
                summary["fuels"][f] = dict(eligible=False, best_knock_free_reference=ref)
                print(f"[h1 dry] {f}: still no eligible hot dry point down to CR {LOW_CRS[0]}", flush=True)
                continue
            base = dict(max(el, key=lambda r: r["gross_indicated_efficiency"]), kind="dry_baseline", step=0)
            base.update(R.crn(base))
            summary["fuels"][f] = dict(eligible=True, base_CR=base["CR"], base_eta=base["gross_indicated_efficiency"],
                                       base_crn=base.get("crn_efficiency"), base_ca50=base["ca50_used_deg"])
            print(f"[h1 dry] {f}: eligible base CR {base['CR']} eta {base['gross_indicated_efficiency']:.4f}", flush=True)
            for m in MODES:
                p = H1 / (f"steps_{f}_hot.jsonl" if m == "liquid" else f"steps_{f}_hot_{m}.jsonl")
                p.write_text(json.dumps(dict(base, water_mode=m), default=float) + "\n")
                jobs.append((f, m))
        (H1 / "summary_h1.json").write_text(json.dumps(summary, indent=1, default=float))
        res = []
        for r in pool.imap_unordered(_chain, jobs):
            res.append(r)
            print(f"[h1 chain] {r['fuel']}/hot/{r['water_mode']} best_w={r['best_w']} steps={r['steps_taken']} "
                  f"d_eta={r['best_eta'] - r['dry_eta']:+.5f} stop={r['stop_reason']} {time.time() - t0:.0f}s", flush=True)
            summary["chains"] = res
            (H1 / "summary_h1.json").write_text(json.dumps(summary, indent=1, default=float))
        e = ext.get()
        print(f"[ext] C2H5OH/hot/humid_evap best_w={e['best_w']} steps={e['steps_taken']} "
              f"d_eta={e['best_eta'] - e['dry_eta']:+.5f} stop={e['stop_reason']} {time.time() - t0:.0f}s", flush=True)
        summary["c2h5oh_hot_humid_evap_ext"] = e
        (H1 / "summary_h1.json").write_text(json.dumps(summary, indent=1, default=float))
    print("h1 done", time.time() - t0, flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 6)
