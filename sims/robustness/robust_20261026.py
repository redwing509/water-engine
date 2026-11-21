"""Robustness of the dryevap verdict (Claude job water-engine-box-20261026-0040; Grok Bot box queue, Oct 26 2026).

Step 1 (R-WE-11, Track A + B): realised fraction of the thermodynamic-maximum evaporative charge cooling
  (env WE_COOL_FRAC -> Module 03 Charge.cool_frac and M03-CRN Case.cool_frac; 1.0 = legacy, bit-identical),
  applied SYMMETRICALLY to fuel and water in every row (dry DEI baselines included). Fractions 1.0 / 0.7 / 0.5
  (Kasseris & Heywood SAE 2012-01-1275: real DI ~70 %).
  Track A: sims.03_engine_cycle.track_a_sym_box with TA_WS=0.55,0.6 (run as subprocesses, see the queue script).
  Track B: PRF87 + CH3OH, both regimes (normal wall 450 K / T_in 320 K ~90 C coolant; hot wall 520 K / T_in 400 K),
           liquid + humid_evap water, w 0 / 0.05 / 0.10 / 0.20 at the symmetric-DEI chain hardware CR.
Step 2 (R-WE-13, Track B): Cantera w 0-0.30 flame fit vs measured iso-octane + H2O S_L (WE-45, Endouard et al.,
  CST 2016). Module 03 uses only the RATIO S_L(w)/S_L(0) (+ the 0.08 m/s floor), so a uniform S_L bias cannot move
  the result; the dilution-dependent bias is what matters. Measured data: CSV MEAS (cols x_H2O_mol,T_K,p_bar,
  S_L_meas_m_s,S_L0_meas_m_s[,S_L_fit_m_s]). If absent -> BRACKET: fit over-predicts the diluted S_L by +10 % / +20 %
  at w 0.20 (linear in w) -- labelled 'bracket, no measured bias'. Each PRF chain stop point re-evaluated on a 0.01
  grid around the old stop (M03 every point, CRN at w 0 and the grid points), both engines, scale 1.0 as control.
Status of everything here: EXECUTED, cross-checked (2 in-repo engines), NOT validated.
    python -m sims.robustness.robust_20261026 tb_cool WORKERS
    python -m sims.robustness.robust_20261026 sl WORKERS SYMDIR
    python -m sims.robustness.robust_20261026 report
"""
import csv
import importlib
import json
import os
import sys
import time
from multiprocessing import get_context
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
OUT = REPO / "results" / "robustness_20261026"
CFS = (1.0, 0.7, 0.5)
TB_FUELS = ("PRF87", "CH3OH")
TB_WS = (0.0, 0.05, 0.10, 0.20)
MODES = ("liquid", "humid_evap")
PRF = ("PRF87", "PRF91", "PRF97")
MEAS = Path(os.environ.get("WE45_CSV", "/workspace/self-jobs/we45/we45_measured.csv"))
M_DRY = 30.3      # g/mol, stoichiometric iso-octane/air (for x_H2O -> w mass fraction)


def _cs():
    return importlib.import_module("sims.track_b.chains_sym")


def _patch_sl(bias):
    """bias = list of (w, b): fit over-predicts S_L(w)/S_L(0) by (1+b(w))/(1+b(0)); correct the cubic accordingly."""
    W = importlib.import_module("sims.track_b.chains_w030")
    if not hasattr(W, "_orig_fit"):
        W._orig_fit = W.flame_fit_w030
    if not bias:
        W.flame_fit_w030 = W._orig_fit
        return
    bw, bb = np.array([p[0] for p in bias]), np.array([p[1] for p in bias])

    def fit(fuel, regime):
        d = W._orig_fit(fuel, regime)
        ws = np.linspace(0.0, 0.30, 31)
        b = np.interp(ws, bw, bb)
        sl = np.polyval(d["coefficients_highest_first"], ws) * (1.0 + b[0]) / (1.0 + b)
        d = dict(d, coefficients_highest_first=[float(v) for v in np.polyfit(ws, sl, 3)],
                 source=d["source"] + f" | R-WE-13 bias-corrected {list(zip(bw.tolist(), bb.tolist()))}")
        return d
    W.flame_fit_w030 = fit


def point(t):
    os.environ["WE_COOL_FRAC"] = str(t.get("cf", 1.0))
    _patch_sl(t.get("bias"))
    t0 = time.time()
    C = _cs()
    r = C.point(dict(fuel=t["fuel"], regime=t["regime"], CR=t["CR"], w=t["w"], mode=t["mode"], crn=t.get("crn", True),
                     key=t["key"]))
    r.update(cool_frac=t.get("cf", 1.0), sl_case=t.get("sl_case", "fit"), task_seconds=time.time() - t0)
    return r


def _pool(tasks, workers, path):
    done = set()
    if path.exists():
        done = {json.loads(l)["_key"] for l in open(path)}
    todo = [t for t in tasks if t["key"] not in done]
    print(f"{len(todo)} tasks ({len(done)} done) -> {path.name}", flush=True)
    t0 = time.time()
    with get_context("spawn").Pool(workers) as pool, open(path, "a") as fh:
        for i, r in enumerate(pool.imap_unordered(point, todo)):
            fh.write(json.dumps(r, default=float) + "\n"); fh.flush()
            print(f"{i + 1}/{len(todo)} {time.time() - t0:.0f}s {r['_key']} {r.get('status')} eta={r.get('gross_indicated_efficiency')} "
                  f"crn={r.get('crn_efficiency')}", flush=True)


def hardware(symdir):
    return json.loads((Path(symdir) / "dei_hardware.json").read_text())


def tb_cool(workers, symdir):
    OUT.mkdir(parents=True, exist_ok=True)
    hw = hardware(symdir)
    tasks = []
    for cf in CFS:
        for f in TB_FUELS:
            for g in ("normal", "hot"):
                for m in MODES:
                    for w in TB_WS:
                        if w == 0.0 and m != "liquid":
                            continue  # w 0 identical in both modes (dry DEI baseline)
                        tasks.append(dict(cf=cf, fuel=f, regime=g, CR=float(hw[f"{f}/{g}"]["CR"]), w=w, mode=m,
                                          key=f"cf{cf}/{f}/{g}/{m}/{w}"))
    _pool(tasks, workers, OUT / "tb_cool_points.jsonl")


# ------------------------------------------------------------------ step 2
def w_from_x(x):
    return x * 18.015 / (x * 18.015 + (1.0 - x) * M_DRY)


def measured_bias():
    """Per-point % error of the PRF97 fit ratio S_L(w)/S_L(0) vs measured ratio; None if no data."""
    if not MEAS.exists():
        return None, []
    W = importlib.import_module("sims.track_b.chains_w030")
    rows = list(csv.DictReader(open(MEAS)))
    out = []
    for r in rows:
        x = float(r["x_H2O_mol"]); w = w_from_x(x)
        meas = float(r["S_L_meas_m_s"]) / float(r["S_L0_meas_m_s"])
        for g in ("normal", "hot"):
            c = W.flame_fit_w030("PRF97", g)["coefficients_highest_first"]
            fitr = float(np.polyval(c, min(w, 0.30)) / np.polyval(c, 0.0))
            out.append(dict(regime_fit=g, T_K=r["T_K"], p_bar=r["p_bar"], x_H2O=x, w=w, ratio_meas=meas, ratio_fit=fitr,
                            err_pct=100 * (fitr / meas - 1), extrapolated=w > 0.30))
    errs = [o for o in out if not o["extrapolated"]]
    return out, errs


def sl(workers, symdir):
    OUT.mkdir(parents=True, exist_ok=True)
    symdir = Path(symdir)
    pts, errs = measured_bias()
    if pts:
        with open(OUT / "sl_fit_vs_we45.csv", "w", newline="") as fh:
            wr = csv.DictWriter(fh, fieldnames=list(pts[0])); wr.writeheader(); wr.writerows(pts)
        ws = sorted({round(e["w"], 4) for e in errs})
        bias = [(0.0, 0.0)] + [(w, float(np.mean([e["err_pct"] for e in errs if round(e["w"], 4) == w])) / 100) for w in ws]
        mean = float(np.mean([e["err_pct"] for e in errs])) if errs else 0.0
        cases = {"measured": bias}
        meta = dict(source=str(MEAS), mean_bias_pct=mean, flagged=mean > 10.0, mode="measured")
    else:
        cases = {"bracket+10": [(0.0, 0.0), (0.20, 0.10), (0.30, 0.15)], "bracket+20": [(0.0, 0.0), (0.20, 0.20), (0.30, 0.30)]}
        meta = dict(source=f"no measured data at {MEAS}", mean_bias_pct=None, flagged=None, mode="bracket, no measured bias")
    cases["fit"] = None
    summ = json.loads((symdir / "summary_sym.json").read_text())
    tasks = []
    for s in summ:
        if s["fuel"] not in PRF:
            continue
        sw = float(s["best_w"] or 0.0)
        grid = sorted({0.0} | {round(min(0.30, max(0.0, sw + d)), 3) for d in (-0.03, -0.02, -0.01, 0.0, 0.01, 0.02, 0.03)})
        for lab, b in cases.items():
            for w in grid:
                tasks.append(dict(fuel=s["fuel"], regime=s["regime"], CR=float(s["CR"]), w=w, mode=s["mode"], bias=b,
                                  sl_case=lab, crn=True, key=f"{lab}/{s['fuel']}/{s['regime']}/{s['mode']}/{w}"))
    (OUT / "sl_meta.json").write_text(json.dumps(dict(meta, cases={k: v for k, v in cases.items()}), indent=1))
    _pool(tasks, workers, OUT / "sl_points.jsonl")


# ------------------------------------------------------------------ report
def _load(p):
    return [json.loads(l) for l in open(p)] if p.exists() else []


def report():
    RP = importlib.import_module("sims.03_engine_cycle.dryevap_report")
    OUT.mkdir(parents=True, exist_ok=True)
    NOISE = 3.3e-5 / 0.001  # chain rule: gain per 0.001 step <= 3.3e-5 -> slope per unit w
    rows = []
    # Track B cooling table
    tb = {r["_key"]: r for r in _load(OUT / "tb_cool_points.jsonl")}
    for k, r in tb.items():
        cf, f, g, m, w = k.split("/")
        if float(w) == 0.0:
            continue
        base = tb.get(f"{cf}/{f}/{g}/liquid/0.0")
        ok = r.get("status") == "computed" and base and base.get("status") == "computed"
        c = {}
        if ok:
            try:
                c = RP.compare(r, base)
            except Exception as exc:
                c = dict(verdict=f"cost failed: {exc}")
        rows.append(dict(table="B_cool", cool_frac=cf, fuel=f, regime=g, mode=m, w=w, CR=r.get("CR"),
                         status=r.get("status") if ok else f"FAILED: {r.get('reason') or base and base.get('reason')}",
                         T_IVC_K=r.get("T_IVC_K"), g_fuel=r.get("fuel_evap_intake_fraction"), eta=r.get("gross_indicated_efficiency"),
                         eta_crn=r.get("crn_efficiency"), crn_status=r.get("crn_status"), **{k2: c.get(k2) for k2 in
                         ("d_eta", "d_eta_crn", "power_pct", "cost_mile_pct", "cost_mile_free_pct", "engines", "verdict", "verdict_free")}))
    # Step 2 table
    sp = _load(OUT / "sl_points.jsonl")
    meta = json.loads((OUT / "sl_meta.json").read_text()) if (OUT / "sl_meta.json").exists() else {}
    grp = {}
    for r in sp:
        lab, f, g, m, w = r["_key"].split("/")
        grp.setdefault((f, g, m), {}).setdefault(lab, {})[float(w)] = r
    for (f, g, m), d in sorted(grp.items()):
        for lab, pts in d.items():
            ws = sorted(pts)
            good = [w for w in ws if pts[w].get("status") == "computed" and pts[w].get("eligible")]
            base = pts.get(0.0)
            if not base or base.get("status") != "computed":
                rows.append(dict(table="B_SL", fuel=f, regime=g, mode=m, sl_case=lab, status="FAILED w0")); continue
            # estimated stop: first grid interval (above w 0) whose M03 slope <= chain noise rule, or CRN slope <= 0
            stop, best = None, 0.0
            gw = [w for w in good if w > 0.0]
            prev = 0.0 if not gw or gw[0] > 0.031 else None
            seq = ([0.0] if prev is not None else []) + gw
            best = seq[0] if seq else 0.0
            for a, b in zip(seq, seq[1:]):
                s = (pts[b]["gross_indicated_efficiency"] - pts[a]["gross_indicated_efficiency"]) / (b - a)
                ca, cb = pts[a].get("crn_efficiency"), pts[b].get("crn_efficiency")
                if s <= NOISE or (ca is not None and cb is not None and cb <= ca):
                    stop = a; break
                best = b
            stop = best if stop is None else stop
            r = pts[stop]
            g_m03 = 100 * (r["gross_indicated_efficiency"] - base["gross_indicated_efficiency"])
            g_crn = (100 * (r["crn_efficiency"] - base["crn_efficiency"])
                     if r.get("crn_efficiency") is not None and base.get("crn_efficiency") is not None else None)
            rows.append(dict(table="B_SL", fuel=f, regime=g, mode=m, sl_case=lab, CR=base.get("CR"), stop_w_est=stop,
                             gain_pp_m03=g_m03, gain_pp_crn=g_crn, grid_max=max(ws), n_failed=len(ws) - len(good),
                             status="computed" if len(good) == len(ws) else f"{len(ws) - len(good)} grid points failed/ineligible"))
    keys = sorted({k for r in rows for k in r})
    with open(OUT / "robustness_rows.csv", "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=keys); wr.writeheader(); wr.writerows(rows)
    (OUT / "sl_meta_report.json").write_text(json.dumps(meta, indent=1))
    print(f"{len(rows)} rows -> {OUT / 'robustness_rows.csv'}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    sd = sys.argv[3] if len(sys.argv) > 3 else "/workspace/we-tbmail/results/track_b/symmetric_dei"
    {"tb_cool": lambda: tb_cool(n, sd), "sl": lambda: sl(n, sd), "report": report}[cmd]()
