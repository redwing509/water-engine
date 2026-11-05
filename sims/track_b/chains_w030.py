"""Track B: water chains past w = 0.1 for the gasoline-like blends (PRF87/91/97, E10, E85), both regimes,
liquid and humid_evap, using a Cantera free-flame S_L fit over w = 0..0.30 (job water-engine-mail-20261025-1830).

Why: every PRF/E10/E85 chain that was still gaining stopped at step 101 only because the published
Metghalchi-Keck flame fit (fuels_b.flame_fit) is valid for w <= 0.1 ("no extrapolation").
Flame fit used here: Cantera 3.2 FreeFlame, CRECK TPRF_HT_ALC mechanism, phi = 1, water vapour in the fresh
mixture, at the regime's IVC state (normal 312.35 K, hot 388.8 K, 1e5 Pa), w = 0, .05, ..., .30
(sims/track_b/flame_w030.py; data results/track_b/w030/cantera_flames/). Cubic fit, valid_w_range [0, 0.30].
Module 03 only uses S_L(w)/S_L(0) (burn duration ~ (S_L0/S_L)^0.5), so the absolute level does not matter.
Cantera slows the flame more with water than the old dilution correlation (ratio at w 0.1: ~0.968 vs ~0.986),
so ALL steps are recomputed from the dry baseline (w = 0) with the new fit - no splice of two fits.
The Douaud-Eyzat ignition correlation has no explicit w term (c = 0; water acts only through the end-gas
temperature); its valid_w_range label is widened to [0, 0.30] here (recorded as an assumption).
Rule: identical to run.chain_noise - 0.1-pp steps on the chain's dry-baseline hardware, spark re-optimised every
step, continue while Module 03 gain > 3.3e-5 AND M03-CRN gain > 0. Cap 300 steps (w 0.30 = fit edge ->
flagged "fit-range limited").
Tags: Track B; normal + hot regimes; executed (2 engines: Module 03 + M03-CRN); not validated.
"""
import json, sys, time
from multiprocessing import get_context
from pathlib import Path
import numpy as np
from sims.track_b import run as R

SRC = R.OUT
DST = R.OUT / "w030"            # variant "full": every step recomputed from w = 0 with the Cantera fit
DST_EXT = R.OUT / "w030_ext"    # variant "ext": old chain path to w 0.100 kept; step 100 recomputed with the
                                # Cantera fit (consistency row), then steps 101..300 with the Cantera fit
FL = DST / "cantera_flames"
CAP = 300
BLENDS = ("PRF87", "PRF91", "PRF97", "E10", "E85")
MODES = ("liquid", "humid_evap")


def src_file(fuel, regime, mode):
    name = f"steps_{fuel}_{regime}{'' if mode == 'liquid' else '_' + mode}__noise.jsonl"
    for d in (SRC / "h1_hot", SRC):
        if (d / name).exists() and not (regime == "normal" and d.name == "h1_hot"):
            if fuel in ("E85",) and d.name == "h1_hot":
                continue
            return d / name
    return SRC / name


def flame_fit_w030(fuel, regime):
    d = json.loads((FL / f"{fuel}_{regime}.json").read_text())
    ws = np.array([r["w"] for r in d]); sl = np.array([r["S_L_m_s"] for r in d])
    c = np.polyfit(ws, sl, 3)
    st = d[0]
    return dict(status="fitted", mode="full", S_L_unit="m/s", coefficients_highest_first=[float(v) for v in c],
                polynomial_degree=3, valid_w_range=[0.0, 0.30], phi=1.0, T_unburned_K=st["T_u_K"], p_Pa=st["p_Pa"],
                rms_m_s=float(np.sqrt(np.mean((np.polyval(c, ws) - sl) ** 2))),
                source="Cantera 3.2 FreeFlame, CRECK TPRF_HT_ALC_254_7568, phi=1, water vapour, "
                       f"{regime} IVC state {st['T_u_K']} K {st['p_Pa']:.0f} Pa, w 0..0.30 (sims/track_b/flame_w030.py)")


def use_fits(fuel, regime):
    R.module03()
    ign, fl = R._FITS
    fl[fuel] = flame_fit_w030(fuel, regime)
    ign[fuel] = dict(ign[fuel], valid_w_range=[0.0, 0.30],
                     note="valid_w_range widened 0.1 -> 0.30 (c = 0, no explicit w term): assumption, chains_w030")


def judge(r, prev):
    ok = r["status"] == "computed" and r["eligible"]
    g = (r["gross_indicated_efficiency"] - prev["gross_indicated_efficiency"]) if ok else None
    gc = (r["crn_efficiency"] - prev["crn_efficiency"]) \
        if ok and r.get("crn_status") == "ok" and prev.get("crn_status") == "ok" else None
    r.update(gain_m03=g, gain_crn=gc, rule="noise_3.3e-5")
    if not ok:
        return "not eligible / not computed"
    if g <= R.NOISE_THRESHOLD:
        return f"M03 gain {g:.2e} <= noise threshold {R.NOISE_THRESHOLD:.1e}"
    if gc is None or gc <= 0:
        return f"M03-CRN gain {gc} not positive"
    return None


def fit_limited_at_101(fuel, regime, mode):
    rows = [json.loads(l) for l in src_file(fuel, regime, mode).open()]
    return any(r.get("kind") == "step" and r.get("step") == 101 and "outside the flame-speed fit range"
               in str(r.get("reason", "")) for r in rows)


def chain(job):
    fuel, regime, mode = job[:3]
    variant = job[3] if len(job) > 3 else "full"
    t0 = time.time()
    use_fits(fuel, regime)
    src = src_file(fuel, regime, mode)
    rows = [json.loads(l) for l in src.open()]
    base = next(r for r in rows if r["kind"] == "dry_baseline")
    old_steps = {r["step"]: r for r in rows if r["kind"] == "step"}
    name = f"steps_{fuel}_{regime}{'' if mode == 'liquid' else '_' + mode}__w030.jsonl"
    out = (DST if variant == "full" else DST_EXT) / name
    out.parent.mkdir(parents=True, exist_ok=True)
    done = [json.loads(l) for l in out.open()] if out.exists() else []
    if not done:
        out.write_text(json.dumps(dict(base, source_file=str(src.relative_to(R.REPO))), default=float) + "\n")
        done = [base]
        if variant == "ext":
            o = old_steps[100]
            r = R.point(fuel, regime, base["CR"], base["T_intake_K"], o["w"], mode)
            r.update(kind="step", step=100, flame_fit="cantera_w030", recomputed_consistency_row=True,
                     old_fit_eta=o["gross_indicated_efficiency"], old_fit_crn=o.get("crn_efficiency"),
                     decision="continue", stop_reason=None,
                     note="old-fit chain path w 0.001..0.100 (decisions under the w<=0.1 fit); this row = same point "
                          "recomputed with the Cantera fit, used as prev for step 101", **R.crn(r))
            with out.open("a") as fh:
                fh.write(json.dumps(r, default=float) + "\n")
            done.append(r)
    steps = [r for r in done if r["kind"] == "step"]
    prev = steps[-1] if steps else base
    k = prev.get("step", 0) if steps else 0
    stop = prev.get("decision") == "stop" and prev.get("stop_reason")
    if steps and steps[-1].get("decision") == "stop":
        stop, prev = steps[-1]["stop_reason"], (steps[-2] if len(steps) > 1 else base)
    while not stop and k < CAP:
        k += 1
        w = round(k * R.STEP, 6)
        r = R.point(fuel, regime, base["CR"], base["T_intake_K"], w, mode)
        r.update(kind="step", step=k, flame_fit="cantera_w030", **R.crn(r))
        o = old_steps.get(k)
        if o:
            r["old_fit_eta"] = o.get("gross_indicated_efficiency"); r["old_fit_crn"] = o.get("crn_efficiency")
        s = judge(r, prev)
        r["decision"] = "stop" if s else "continue"
        r["stop_reason"] = s
        with out.open("a") as fh:
            fh.write(json.dumps(r, default=float) + "\n")
        if s:
            stop = s
            break
        prev = r
    if not stop:
        stop = f"cap {CAP} steps reached (w {CAP * R.STEP:.2f} = flame-fit edge): fit-range limited"
    best = prev
    old_best = max((r for r in old_steps.values() if r.get("decision") == "continue"), key=lambda r: r["step"],
                   default=None)
    return dict(variant=variant, fuel=fuel, regime=regime, water_mode=mode, CR=base["CR"], T_intake_K=base["T_intake_K"],
                best_w=best["w"], steps_taken=best.get("step", 0), stop_reason=stop,
                fit_range_limited=stop.startswith("cap"),
                dry_eta=base["gross_indicated_efficiency"], best_eta=best["gross_indicated_efficiency"],
                dry_crn=base.get("crn_efficiency"), best_crn=best.get("crn_efficiency"),
                old_fit_best_w=old_best["w"] if old_best else 0.0,
                old_fit_best_eta=old_best["gross_indicated_efficiency"] if old_best else base["gross_indicated_efficiency"],
                seconds=time.time() - t0)


def jobs(variants=("full", "ext")):
    j = [(f, g, m) for g in ("normal", "hot") for f in BLENDS for m in MODES]
    out = [x + ("full",) for x in j] if "full" in variants else []
    if "ext" in variants:
        out += [x + ("ext",) for x in j if fit_limited_at_101(*x)]
    # longest first: ext (start at 101, run to stop), then normal full chains
    return sorted(out, key=lambda x: (x[3] != "ext", x[1] != "normal", x))


def main(workers=2, only=None):
    DST.mkdir(parents=True, exist_ok=True)
    js = jobs() if not only else [tuple(s.split("/")) for s in only.split(",")]
    DST_EXT.mkdir(parents=True, exist_ok=True)
    res = []
    ctx = get_context("spawn")
    with ctx.Pool(workers) as pool:
        for r in pool.imap_unordered(chain, js):
            res.append(r)
            print(f"[w030 {r['variant']}] {r['fuel']}/{r['regime']}/{r['water_mode']} CR{r['CR']} best_w={r['best_w']} "
                  f"d_eta={r['best_eta'] - r['dry_eta']:+.5f} d_crn={(r['best_crn'] or 0) - (r['dry_crn'] or 0):+.5f} "
                  f"stop={r['stop_reason']} {r['seconds']:.0f}s", flush=True)
            (DST / "summary_w030.json").write_text(json.dumps(res, indent=1, default=float))
    print("w030 done", flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2, sys.argv[2] if len(sys.argv) > 2 else None)
