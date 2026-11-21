"""PR 11 review item 2 (Claude reply-selfdir-1410-review-20261025-1725): independent fresh-process check that the
CH3OH normal 'liquid' and 'humid_evap' Track B chains are computed with their own intake-mode flag, and that their
coincidence from w 0.140 on is physical (both intake-saturation-limited -> identical charge), not a resume bug.

Each mode runs in its own fresh spawned process (no shared caches with the other mode), at the chain's own dry
baseline hardware (CR 17, T_intake 320 K, normal regime), spark re-optimised, M03-CRN with the fixed sat_blend.
Compares with the stored crnfix chain rows. Tags: Track B; normal regime; executed (2 engines); not validated.
"""
import json, sys, time
from multiprocessing import get_context
from pathlib import Path

WS = (0.080, 0.081, 0.132, 0.133, 0.139, 0.140, 0.141, 0.227, 0.228)
OUT = Path("results/track_b/crnfix/mode_check_CH3OH_normal.json")


def run_mode(mode):
    from sims.track_b import run as R
    name = R.OUT / "crnfix" / f"steps_CH3OH_normal{'' if mode == 'liquid' else '_' + mode}__noise.jsonl"
    rows = [json.loads(l) for l in name.open()]
    base = next(r for r in rows if r["kind"] == "dry_baseline")
    stored = {round(r["w"], 6): r for r in rows if r["kind"] == "step"}
    res = []
    for w in WS:
        t = time.time()
        r = R.point("CH3OH", "normal", base["CR"], base["T_intake_K"], w, mode)
        r.update(R.crn(r))
        s = stored[w]
        res.append(dict(mode=mode, w=w, water_mode_row=r["water_mode"], f_evap=r["f_evap_intake_effective"],
                        sat_limited=r["intake_saturation_limited"], eta_m03=r["gross_indicated_efficiency"],
                        eta_crn=r.get("crn_efficiency"), crn_status=r.get("crn_status", "")[:40],
                        stored_eta_m03=s["gross_indicated_efficiency"], stored_eta_crn=s.get("crn_efficiency"),
                        stored_f_evap=s["f_evap_intake_effective"], stored_mode=s.get("water_mode"),
                        d_m03_vs_stored=r["gross_indicated_efficiency"] - s["gross_indicated_efficiency"],
                        seconds=time.time() - t))
        print(json.dumps(res[-1], default=float), flush=True)
    return res


if __name__ == "__main__":
    ctx = get_context("spawn")
    allr = []
    for mode in ("liquid", "humid_evap"):        # one worker, one fresh process per mode
        with ctx.Pool(1) as p:
            allr += p.apply(run_mode, (mode,))
    L = {r["w"]: r for r in allr if r["mode"] == "liquid"}
    H = {r["w"]: r for r in allr if r["mode"] == "humid_evap"}
    cmp = [dict(w=w, f_evap_liquid=L[w]["f_evap"], f_evap_humid=H[w]["f_evap"], sat_liquid=L[w]["sat_limited"],
                sat_humid=H[w]["sat_limited"], d_eta_m03_liquid_minus_humid=L[w]["eta_m03"] - H[w]["eta_m03"])
           for w in WS]
    OUT.write_text(json.dumps(dict(points=allr, compare=cmp,
                                   max_abs_diff_vs_stored=max(abs(r["d_m03_vs_stored"]) for r in allr)),
                              indent=1, default=float))
    print("mode_check done", flush=True)
