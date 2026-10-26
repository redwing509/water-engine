"""Track B SYMMETRIC DEI rebase (Claude reply-dryevap-verdict-and-trackb-rebase-20261025-2035, Oct 25 2026).

Why: dryevap (0bdf532) showed the old dry baseline was unfair (no fuel-evaporation charge cooling). Here the fuel is
evaporated by the DEI model (intake dry-evap: all fuel enters as liquid at 298 K and evaporates in the intake air before
IVC, capped at the fuel dew point; release = vapour LHV; M03-CRN gets the same latent credit) at EVERY step including
w = 0, so the chain's w = 0 start IS the DEI dry baseline and every gain isolates the water effect.

Chains: PRF87/91/97, E10, E85, CH3OH, C2H5OH x normal (wall 450 K, T_intake 320 K, ~90 C coolant) / hot (wall 520 K,
T_intake 400 K, high-performance) x liquid / humid_evap water. Hardware = the fuel's DEI 'rule' baseline (best eligible
eta over the dryevap CR grid, LW criterion; from results/dryevap/baselines.csv where present, else the same scan here).
Flame fit: blends = Cantera w 0-0.30 fit (chains_w030); alcohols = Module 02 fit (valid w <= 0.8).
Rule = chains_w030 / run.chain_noise: 0.1-pp steps, spark re-optimised, continue while Module 03 gain > 3.3e-5 AND
M03-CRN gain > 0; cap 300 steps (w 0.30) -> 'fit-range limited'.
Points are path independent (fixed CR, T_intake), so steps are computed in look-ahead blocks across the pool and the
stop rule is applied in step order (rows computed past a stop are kept separately, never used for decisions).
Tags: Track B; both regimes; executed (2 engines); NOT validated.

    python -m sims.track_b.chains_sym baselines WORKERS      # DEI hardware + w0 check (W0_CHECK.md)
    python -m sims.track_b.chains_sym chains WORKERS [only]  # chains (only = fuel/regime/mode[/startk],...)
"""
import csv
import importlib
import json
import math
import queue
import sys
import time
from multiprocessing import get_context
from pathlib import Path

from sims.track_b import run as R

OUT = R.OUT / "symmetric_dei"
FUELS = ("PRF87", "PRF91", "PRF97", "E10", "E85", "CH3OH", "C2H5OH")
REGIMES = ("normal", "hot")
T_INTAKE = {"normal": 320.0, "hot": 400.0}
MODES = ("liquid", "humid_evap")
CAP = 300
BLOCK = 6
BASELINES_CSV = R.REPO / "results" / "dryevap" / "baselines.csv"
_S = {}


def _setup(fuel, regime):
    if "D" not in _S:
        D = importlib.import_module("sims.03_engine_cycle.dryevap_baseline")
        D._init()
        D._set("B", D.VARIANTS["DEI"])        # every run_point gets coupling fuel_evap_intake = 1.0
        _S["D"] = D
        _S["W"] = importlib.import_module("sims.track_b.chains_w030")
    W = _S["W"]
    R.module03()
    if fuel in W.BLENDS:
        W.use_fits(fuel, regime)               # Cantera w 0-0.30 flame fit at the regime state


def crn_sym(r, heat_transfer="woschni"):
    """R.crn + the DEI fuel latent credit (same as dryevap crn_case) + the CRN saturation smoothing."""
    if r.get("status") != "computed":
        return dict(crn_status="skipped")
    E = R.crn_engine()
    credit = float(r.get("fuel_evap_intake_fraction") or 0.0) + float(r.get("fuel_evap_port_fraction") or 0.0)
    t = time.time()
    try:
        res = E.run_case(E.Case(fuel=r["fuel"], cr=r["CR"], T_ivc=r["T_IVC_K"], m_fuel=r["fuel_mass_kg"],
                                m_air=r["air_mass_kg"], m_residual=r["residual_mass_kg"],
                                m_water=r["water_mass_kg"], e_intake=r["f_evap_intake_effective"],
                                ca50_deg=r["ca50_used_deg"], d1090_deg=r["burn_10_90_deg"],
                                wall_T=r["chamber_wall_K"], heat_transfer=heat_transfer,
                                sat_blend_frac=R.CRN_SAT_BLEND, fuel_latent_credit=credit))
    except Exception as exc:  # recorded, never retried blindly
        return dict(crn_status=f"failed: {type(exc).__name__}: {exc}", crn_latent_credit=credit)
    eta, pmax = res["efficiency"], res["p_max_Pa"]
    return dict(crn_status="ok", crn_sat_blend_frac=R.CRN_SAT_BLEND, crn_latent_credit=credit, crn_efficiency=eta,
                crn_p_max_Pa=pmax, crn_seconds=time.time() - t, d_eta_pp=100 * (eta - r["gross_indicated_efficiency"]),
                pmax_ratio=pmax / r["peak_pressure_Pa"],
                c1_pass=bool(abs(100 * (eta - r["gross_indicated_efficiency"])) <= 1.5
                             and abs(pmax / r["peak_pressure_Pa"] - 1) <= 0.05))


def point(task):
    """task = dict(fuel, regime, CR, w, mode, crn=bool, key=...)"""
    t0 = time.time()
    _setup(task["fuel"], task["regime"])
    try:
        r = R.point(task["fuel"], task["regime"], task["CR"], T_INTAKE[task["regime"]], task["w"], task["mode"])
    except Exception as exc:
        r = dict(status="failed", reason=f"{type(exc).__name__}: {exc}", fuel=task["fuel"], CR=task["CR"], w=task["w"],
                 regime=task["regime"], water_mode=task["mode"], eligible=False)
    r.update(fuel_treatment="DEI (fuel_evap_intake=1.0)", flame_fit="cantera_w030" if task["fuel"] in R.FB.BLENDS
             else "module_02", track="B", variant="symmetric_DEI")
    if task.get("crn", True) and r.get("status") == "computed":
        r.update(crn_sym(r))
    r["m03_plus_crn_seconds"] = time.time() - t0
    r["_key"] = task.get("key")
    return {k: (float(v) if hasattr(v, "dtype") else v) for k, v in r.items()}


# ------------------------------------------------------------------ DEI hardware + w0 check
def ref_baselines():
    out = {}
    for r in csv.DictReader(open(BASELINES_CSV)):
        if r["track"] == "B" and r["variant"] == "DEI" and r["selection"] == "rule" and r["criterion"] == "LW":
            out[(r["fuel"], r["regime"])] = dict(CR=float(r["CR"]), eta=float(r["eta"]),
                                                 eta_crn=float(r["eta_crn"]) if r["eta_crn"] else None,
                                                 T_IVC_K=float(r["T_IVC_K"]), T_intake_K=float(r["T_intake_K"]))
    return out


def baselines(workers):
    OUT.mkdir(parents=True, exist_ok=True)
    D = importlib.import_module("sims.03_engine_cycle.dryevap_baseline")
    refs = ref_baselines()
    scan_f = OUT / "dei_cr_scan.jsonl"
    have = {}
    if scan_f.exists():
        for l in scan_f.open():
            r = json.loads(l); have[r["_key"]] = r
    tasks = [dict(fuel=f, regime=g, CR=float(c), w=0.0, mode="liquid", crn=False, key=f"scan/{f}/{g}/{c}")
             for f in FUELS for g in REGIMES if (f, g) not in refs for c in D.CR_B]
    tasks = [t for t in tasks if t["key"] not in have]
    print(f"CR scan: {len(tasks)} points", flush=True)
    ctx = get_context("spawn")
    with ctx.Pool(workers) as pool, scan_f.open("a") as fh:
        for r in pool.imap_unordered(point, tasks):
            have[r["_key"]] = r; fh.write(json.dumps(r, default=float) + "\n"); fh.flush()
            print(r["_key"], r.get("status"), r.get("eligible"), r.get("gross_indicated_efficiency"), flush=True)
    hw = {}
    for f in FUELS:
        for g in REGIMES:
            if (f, g) in refs:
                hw[f"{f}/{g}"] = dict(refs[(f, g)], source="results/dryevap/baselines.csv (DEI, rule, LW)")
            else:
                rows = [r for k, r in have.items() if k.startswith(f"scan/{f}/{g}/")]
                el = [r for r in rows if r.get("eligible")]
                b = max(el, key=lambda r: r["gross_indicated_efficiency"]) if el else None
                hw[f"{f}/{g}"] = dict(CR=b["CR"] if b else None, eta=b and b["gross_indicated_efficiency"], eta_crn=None,
                                      klCR=max((r["CR"] for r in el), default=None), n_eligible=len(el), n_scan=len(rows),
                                      source="new DEI scan here (dryevap CR grid, LW, rule = best eligible eta)")
    (OUT / "dei_hardware.json").write_text(json.dumps(hw, indent=1, default=float))
    # w0 check at the chosen hardware, both water modes (w = 0 -> mode must not matter), both engines
    t2 = [dict(fuel=f, regime=g, CR=hw[f"{f}/{g}"]["CR"], w=0.0, mode=m, crn=True, key=f"w0/{f}/{g}/{m}")
          for f in FUELS for g in REGIMES for m in MODES if hw[f"{f}/{g}"]["CR"] is not None]
    res = {}
    with ctx.Pool(workers) as pool:
        for r in pool.imap_unordered(point, t2):
            res[r["_key"]] = r
    (OUT / "w0_rows.json").write_text(json.dumps(res, indent=1, default=float))
    md = ["# w 0 start vs DEI baseline (symmetric DEI rebase)", "",
          "| fuel | regime | CR | mode | eta M03 (w0) | ref eta M03 | diff | eta CRN (w0) | ref eta CRN | diff | eligible | ref source |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    worst = 0.0; worst_crn = 0.0
    for f in FUELS:
        for g in REGIMES:
            h = hw[f"{f}/{g}"]
            if h["CR"] is None:
                md.append(f"| {f} | {g} | - | - | no eligible DEI dry point on the CR grid -> no chain | | | | | | | |")
                continue
            for m in MODES:
                r = res.get(f"w0/{f}/{g}/{m}", {})
                e, c = r.get("gross_indicated_efficiency"), r.get("crn_efficiency")
                re_, rc = h.get("eta"), h.get("eta_crn")
                d = (e - re_) if None not in (e, re_) else None
                dc = (c - rc) if None not in (c, rc) else None
                if d is not None and "baselines.csv" in h["source"]:
                    worst = max(worst, abs(d))
                if dc is not None and "baselines.csv" in h["source"]:
                    worst_crn = max(worst_crn, abs(dc))
                fm = lambda x, s="%.6f": "-" if x is None else s % x
                md.append(f"| {f} | {g} | {h['CR']} | {m} | {fm(e)} | {fm(re_)} | {fm(d, '%+.2e')} | {fm(c)} | {fm(rc)} | "
                          f"{fm(dc, '%+.2e')} | {r.get('eligible')} | {h['source']} |")
    md += ["", f"Max |diff| vs baselines.csv: M03 {worst:.2e}, CRN {worst_crn:.2e}."]
    (OUT / "W0_CHECK.md").write_text("\n".join(md) + "\n")
    (OUT / "w0_check.json").write_text(json.dumps(dict(max_abs_diff_m03=worst, max_abs_diff_crn=worst_crn), indent=1))
    print("\n".join(md), flush=True)


# ------------------------------------------------------------------ chains (look-ahead block scheduler)
def judge(r, prev):
    ok = r.get("status") == "computed" and r.get("eligible")
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


def chain_name(f, g, m, start=0):
    return f"steps_{f}_{g}{'' if m == 'liquid' else '_' + m}__sym{'' if not start else f'_from{start}'}.jsonl"


def chains(workers, only=None):
    OUT.mkdir(parents=True, exist_ok=True)
    hw = json.loads((OUT / "dei_hardware.json").read_text())
    w0 = json.loads((OUT / "w0_rows.json").read_text())
    if only:
        specs = [tuple(s.split("/")) for s in only.split(",")]
    else:
        specs = [(f, g, m) for f in FUELS for g in REGIMES for m in MODES]
    cache_f = OUT / "points_raw.jsonl"
    cache = {}
    if cache_f.exists():
        for l in cache_f.open():
            try:
                r = json.loads(l); cache[r["_key"]] = r
            except Exception:
                pass
    C = {}
    summary = []
    for s in specs:
        f, g, m = s[:3]
        start = int(s[3]) if len(s) > 3 else 0
        h = hw[f"{f}/{g}"]
        name = chain_name(f, g, m, start)
        if h["CR"] is None or not w0.get(f"w0/{f}/{g}/{m}", {}).get("eligible"):
            summary.append(dict(fuel=f, regime=g, mode=m, start=start, status="no eligible DEI dry baseline -> not run"))
            continue
        base = dict(w0[f"w0/{f}/{g}/{m}"], kind="dry_baseline", step=0, hardware=h)
        C[name] = dict(f=f, g=g, m=m, CR=h["CR"], base=base, start=start, prev=base, judged=start, next=start + 1 if start else 1,
                       res={}, rows=[base], stop=None, inflight=0)
        if start:   # consistency row at the start step: computed in DEI mode, used as prev (decisions before it: old path)
            C[name]["next"] = start
            C[name]["judged"] = start - 1
    ctx = get_context("spawn")
    q = queue.Queue()
    pending = 0
    t0 = time.time()
    raw = cache_f.open("a")
    beyond = (OUT / "beyond_stop.jsonl").open("a")

    def key(name, k):
        c = C[name]
        return f"{c['f']}/{c['g']}/{c['m']}/CR{c['CR']}/k{k}"

    def flush(name):
        c = C[name]
        (OUT / name).write_text("".join(json.dumps(r, default=float) + "\n" for r in c["rows"]))

    def advance(name):
        c = C[name]
        while c["stop"] is None and (c["judged"] + 1) in c["res"]:
            k = c["judged"] + 1
            r = dict(c["res"].pop(k))
            r.update(kind="step", step=k)
            if c["start"] and k == c["start"]:
                r.update(decision="continue", stop_reason=None, recomputed_consistency_row=True,
                         note=f"start of continuation at w {k * R.STEP:.3f} in symmetric DEI mode (old-path decisions "
                              f"before this step); used as prev for step {k + 1}")
            else:
                s = judge(r, c["prev"])
                r["decision"] = "stop" if s else "continue"
                r["stop_reason"] = s
                if s:
                    c["stop"] = s
            c["rows"].append(r)
            c["judged"] = k
            if r["decision"] == "continue":
                c["prev"] = r
            if c["stop"] is None and k >= CAP:
                c["stop"] = f"cap {CAP} steps reached (w {CAP * R.STEP:.2f} = flame-fit edge): fit-range limited"
        flush(name)

    with ctx.Pool(workers) as pool:
        def submit(name):
            nonlocal pending
            c = C[name]
            n = 0
            for k in range(c["next"], min(c["next"] + BLOCK, CAP + 1)):
                kk = key(name, k)
                if kk in cache:
                    c["res"][k] = cache[kk]
                else:
                    t = dict(fuel=c["f"], regime=c["g"], CR=c["CR"], w=round(k * R.STEP, 6), mode=c["m"], crn=True, key=kk)
                    pool.apply_async(point, (t,), callback=lambda r, nm=name, kx=k: q.put((nm, kx, r)),
                                     error_callback=lambda e, nm=name, kx=k: q.put((nm, kx, dict(status="failed", eligible=False, reason=repr(e)))))
                    c["inflight"] += 1; pending += 1
                n += 1
            c["next"] += n
            advance(name)

        def active():
            return [n for n, c in C.items() if c["stop"] is None and c["next"] <= CAP]

        while True:
            # keep 2x workers tasks queued; give look-ahead to the chain with the least of it
            while pending < 2 * workers and active():
                name = min(active(), key=lambda n: (C[n]["next"] - C[n]["judged"], C[n]["next"]))
                before = pending
                submit(name)
                if pending == before and not active():
                    break
            if pending == 0 and not active():
                break
            try:
                name, k, r = q.get(timeout=600)
            except queue.Empty:
                print(f"{time.time() - t0:.0f}s waiting, pending {pending}", flush=True)
                continue
            pending -= 1
            c = C[name]; c["inflight"] -= 1
            r["_key"] = key(name, k)
            raw.write(json.dumps(r, default=float) + "\n"); raw.flush()
            if c["stop"] is not None:
                beyond.write(json.dumps(dict(r, chain=name, step=k, note="computed past the stop; never used for decisions"),
                                        default=float) + "\n"); beyond.flush()
                continue
            c["res"][k] = r
            advance(name)
            prog = {n: dict(judged=cc["judged"], w=round(cc["judged"] * R.STEP, 3), stop=cc["stop"],
                            d_eta_m03_pp=100 * (cc["prev"]["gross_indicated_efficiency"] - cc["base"]["gross_indicated_efficiency"]),
                            d_eta_crn_pp=100 * ((cc["prev"].get("crn_efficiency") or 0) - (cc["base"].get("crn_efficiency") or 0)))
                    for n, cc in C.items()}
            (OUT / "PROGRESS.json").write_text(json.dumps(dict(elapsed_s=time.time() - t0, pending=pending, chains=prog,
                                                               updated=time.strftime("%Y-%m-%dT%H:%M:%S%z")), indent=1))
            if c["stop"] is not None:
                print(f"[sym] {name} CR{c['CR']} stop at step {c['judged']} best_w={c['prev'].get('w')} "
                      f"d_eta={100 * (c['prev']['gross_indicated_efficiency'] - c['base']['gross_indicated_efficiency']):+.3f}pp "
                      f"stop={c['stop']} {time.time() - t0:.0f}s", flush=True)
    for name, c in C.items():
        b, p = c["base"], c["prev"]
        summary.append(dict(fuel=c["f"], regime=c["g"], mode=c["m"], start=c["start"], CR=c["CR"], best_w=p.get("w") or 0.0,
                            steps=c["judged"], stop_reason=c["stop"], dry_eta=b["gross_indicated_efficiency"],
                            best_eta=p["gross_indicated_efficiency"], dry_crn=b.get("crn_efficiency"),
                            best_crn=p.get("crn_efficiency"), file=name))
    tag = "" if not only else "_" + only.replace("/", "-").replace(",", "+")[:60]
    (OUT / f"summary_sym{tag}.json").write_text(json.dumps(summary, indent=1, default=float))
    print("sym chains done", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    if cmd == "baselines":
        baselines(n)
    elif cmd == "chains":
        chains(n, sys.argv[3] if len(sys.argv) > 3 else None)
