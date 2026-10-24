"""Module 09 verification (queue item 4). Criteria: verification/m09/ACCEPTANCE.md
(committed before this script was first run). Production code is NOT modified;
integrator rtol is threaded via a wrapper around Spray.run, classes via
dataclasses.replace(DEF, rr_classes=n).
Usage: python -m verification.m09.verify_m09 --procs 4 --out verification/m09/results
"""
import argparse, dataclasses, json, math, time
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
from pathlib import Path
import numpy as np
import importlib

R = importlib.import_module("sims.09_spray_evaporation.run")
M = importlib.import_module("sims.09_spray_evaporation.model")

_ORIG_RUN = M.Spray.run
def set_rtol(rtol):
    def run(self, duration, mode="p", u_g=0.0, Vfun=None, n_out=50, rtol_=None, **kw):
        return _ORIG_RUN(self, duration, mode=mode, u_g=u_g, Vfun=Vfun, n_out=n_out, rtol=rtol)
    M.Spray.run = run

# ---------------- V1 d2-law
def d2_case(d0, Ys, Yinf, rtol):
    c = M.ConstProps(Ys=Ys, Yinf=Yinf)
    sp = M.Spray(m_air=1.0, T_gas=350.0, p=1e5, m_ref=1e-12, const=c, fixed_Td=True, infinite_gas=True)
    sp.add_classes([d0], [1.0], 0.0, 300.0, 0.0)
    K = 8.0 * c.rho_g * c.D * math.log1p((c.Ys - c.Yinf) / (1.0 - c.Ys)) / c.rho_l
    tl = d0**2 / K
    snaps = _ORIG_RUN(sp, 0.9 * tl, n_out=90, rtol=rtol)
    t = np.array([s["t_s"] for s in snaps]); m = np.array([s["liquid_kg"] for s in snaps])
    d2 = (6 * m / (math.pi * c.rho_l))**(2 / 3)
    ex = d0**2 - K * t
    sel = t >= 0.1 * tl - 1e-18
    err = float(np.max(np.abs(d2[sel] - ex[sel]) / ex[sel]))
    A = np.vstack([np.ones(t.size), t]).T
    coef, res, *_ = np.linalg.lstsq(A, d2, rcond=None)
    r2 = 1 - float(np.sum((A @ coef - d2)**2)) / float(np.sum((d2 - d2.mean())**2))
    return dict(d0_um=d0 * 1e6, Ys=Ys, Yinf=Yinf, rtol=rtol, K=K, lifetime_s=tl, max_rel_err=err,
                fit_slope_rel_err=abs(-coef[1] - K) / K, R2=r2)

def v1():
    out = []
    for d0 in (20e-6, 50e-6, 100e-6):
        for Ys, Yi in ((0.05, 0.0), (0.20, 0.02)):
            for rt in (1e-5, 1e-6, 1e-7, 1e-8, 1e-9):
                out.append(d2_case(d0, Ys, Yi, rt))
    f = [o for o in out if o["rtol"] == 1e-9]
    a = all(o["max_rel_err"] <= 1e-4 for o in f)
    b = all(o9["max_rel_err"] <= o6["max_rel_err"] for o9 in f for o6 in out
            if o6["rtol"] == 1e-6 and (o6["d0_um"], o6["Ys"]) == (o9["d0_um"], o9["Ys"]))
    cc = all(o["R2"] >= 0.999999 and o["fit_slope_rel_err"] <= 1e-4 for o in f)
    return dict(rows=out, V1a=a, V1b=b, V1c=cc,
                max_err_rtol1e9=max(o["max_rel_err"] for o in f))

# ---------------- run_case jobs
CASES = [dict(R.REFERENCE, atomiser="carb_venturi", w=0.6),
         dict(R.REFERENCE, atomiser="psi_3bar", w=0.6),
         dict(R.REFERENCE, atomiser="ultrasonic_120kHz", w=0.0)]
QTY = ("evaporated_IVC_pct", "evaporated_spark_pct", "wall_impinged_pct", "SMD_spark_um", "T_spark_K")

def job_case(args):
    ci, rtol, ncls = args
    set_rtol(rtol)
    par = dataclasses.replace(R.DEF, rr_classes=ncls)
    t0 = time.perf_counter()
    row = R.run_case(CASES[ci], par)
    return dict(ci=ci, rtol=rtol, classes=ncls, runtime=time.perf_counter() - t0, **{q: row[q] for q in QTY})

def job_chamber(args):
    name, packets = args
    set_rtol(1e-7)
    meta = META[name]
    snaps = R.chamber_run(meta, 30e-6, 0.010, "wilson", packets=packets, classes=8)
    t = np.array([s["t_s"] for s in snaps]); e = np.array([100 * s["evaporated_frac"] for s in snaps])
    # value at EOI: last snapshot at/after final packet addition (t <= dur) -> interpolate at dur
    j = np.searchsorted(t, meta["dur"], side="right") - 1
    e_eoi = float(e[j]) if abs(t[j] - meta["dur"]) < 1e-15 else float(np.interp(meta["dur"], t, e))
    return dict(case=name, packets=packets, evap_eoi_pct=e_eoi, evap_end_pct=float(e[-1]))

# Phase-A chamber metadata (copied from xcheck/x4-spray sims/xcheck_x4/cases/X4-*-RD.case_meta.json, refine 1.0)
META0 = {
    "A1-H2O": dict(p=1.0e5, T=360.0, dur=0.005, massTotal_kg=6.974771618101984e-06,
                   U_bernoulli_m_s=28.50328598487914, composition={"H2O": 1.0}),
    "A2-BLEND": dict(p=2.0e6, T=700.0, dur=0.002, massTotal_kg=4.2695860442487045e-06,
                     U_bernoulli_m_s=134.1008835945568, composition={"H2O": 0.6, "CH3OH": 0.4}),
}
META = dict(META0)

def load_meta():
    return dict(META0)

def gci(f1, f2, f3, r=2.0, Fs=1.25):
    e21, e32 = f2 - f1, f3 - f2   # f1 finest
    res = dict(f_fine=f1, f_mid=f2, f_coarse=f3)
    if e21 == 0:
        res.update(p=None, f_ext=f1, gci_fine_rel=0.0, note="fine==mid"); return res
    s = e32 / e21
    if s <= 0:
        res.update(p=None, f_ext=None, gci_fine_rel=None, note="oscillatory"); return res
    p = math.log(s) / math.log(r)
    fext = f1 + (f1 - f2) / (r**p - 1)
    g = Fs * abs((f1 - f2) / f1) / (r**p - 1) if f1 != 0 else float("inf")
    res.update(p=p, f_ext=fext, gci_fine_rel=g); return res

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--procs", type=int, default=4); ap.add_argument("--out", default="verification/m09/results")
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    global META; META = load_meta()
    t0 = time.perf_counter()
    rep = {"V1": v1()}
    jobs = [(ci, rt, 8) for ci in range(3) for rt in (1e-5, 1e-6, 1e-7, 1e-8, 1e-9)]
    jobs += [(ci, 1e-7, n) for ci in range(3) for n in (16, 32, 64)]
    cj = [(nm, pk) for nm in META for pk in (5, 10, 20, 40)]
    ctx = mp.get_context("spawn")
    with ProcessPoolExecutor(a.procs, mp_context=ctx, initializer=_init, initargs=(META,)) as ex:
        rc = list(ex.map(job_case, jobs)); ch = list(ex.map(job_chamber, cj))
    raw = dict(cases=CASES, run_case=rc, chamber=ch)
    (out / "raw.json").write_text(json.dumps(raw, indent=1, default=float))
    # V2
    v2 = []; ok2 = True
    for ci in range(3):
        g = {r["rtol"]: r for r in rc if r["ci"] == ci and r["classes"] == 8}
        for q in QTY:
            d = g[1e-7][q] - g[1e-9][q]
            if q.endswith("_pct"): passed = abs(d) <= 0.05; metric = abs(d)
            elif g[1e-9][q] == 0.0:  # SMD undefined (no airborne liquid at spark): require exact agreement
                metric = abs(d); passed = metric == 0.0
            else: metric = abs(d) / abs(g[1e-9][q]); passed = metric <= 1e-3
            ok2 &= passed
            v2.append(dict(case=ci, qty=q, values={str(k): g[k][q] for k in sorted(g)}, metric=metric, passed=passed))
    rep["V2"] = dict(rows=v2, passed=ok2)
    # V3
    v3 = []; ok3 = True; w3 = []
    for nm in META:
        g = {r["packets"]: r for r in ch if r["case"] == nm}
        for q in ("evap_eoi_pct", "evap_end_pct"):
            G = gci(g[40][q], g[20][q], g[10][q])
            absd = abs(g[40][q] - g[20][q])
            passed = (G["gci_fine_rel"] is not None and G["gci_fine_rel"] <= 0.01) or absd <= 0.05
            ok3 &= passed
            prod_err = abs(g[10][q] - G["f_ext"]) if G["f_ext"] is not None else abs(g[10][q] - g[40][q])
            v3b = prod_err <= 1.0
            if not v3b: w3.append(f"{nm} {q} production err {prod_err:.3f} pp")
            v3.append(dict(case=nm, qty=q, values={k: g[k][q] for k in sorted(g)}, gci=G, abs_40_20=absd, passed=passed,
                           production_err_pp=prod_err, V3b=v3b))
    rep["V3"] = dict(rows=v3, V3a=ok3, V3b_flags=w3)
    # V4
    v4 = []; ok4 = True; w4 = []
    for ci in range(3):
        g = {r["classes"]: r for r in rc if r["ci"] == ci and r["rtol"] == 1e-7}
        for q in ("evaporated_spark_pct", "SMD_spark_um"):
            G = gci(g[64][q], g[32][q], g[16][q])
            applies = not (q == "evaporated_spark_pct" and g[64][q] <= 1.0) and not (q == "SMD_spark_um" and (not np.isfinite(g[64][q]) or g[64][q] == 0.0))
            passed = (not applies) or (G["gci_fine_rel"] is not None and G["gci_fine_rel"] <= 0.01)
            ok4 &= passed
            pe = None
            if q == "evaporated_spark_pct":
                ref = G["f_ext"] if G["f_ext"] is not None else g[64][q]
                pe = abs(g[8][q] - ref)
                if pe > 2.0: w4.append(f"case {ci} production(8 classes) err {pe:.3f} pp")
            v4.append(dict(case=ci, qty=q, values={k: g[k][q] for k in sorted(g)}, gci=G, applies=applies, passed=passed, production_err_pp=pe))
    rep["V4"] = dict(rows=v4, V4a=ok4, V4b_flags=w4)
    V = rep["V1"]
    rep["overall_pass"] = bool(V["V1a"] and V["V1b"] and V["V1c"] and ok2 and ok3 and ok4)
    rep["runtime_s"] = time.perf_counter() - t0
    (out / "raw.json").write_text(json.dumps(raw, indent=1, default=float))
    (out / "report.json").write_text(json.dumps(rep, indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o)))
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "rows"}) for k, v in rep.items()}, indent=1, default=float))

def _init(meta):
    global META; META = meta

if __name__ == "__main__":
    main()
