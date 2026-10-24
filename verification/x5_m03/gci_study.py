#!/usr/bin/env python3
"""Step-convergence / closure / ideal-Otto study for module 03 and X5.

Acceptance criteria: ACCEPTANCE_CRITERIA.md (committed before the first run).
Usage:  python verification/x5_m03/gci_study.py [--procs N] [--out DIR]
Runtime: about 10-40 min on 6 cores. Needs cantera, CoolProp, scipy, numpy.
"""
import argparse, importlib, importlib.util, json, math, os, sys, tempfile, time, traceback, warnings
from multiprocessing import Pool
from pathlib import Path

warnings.filterwarnings("ignore", message="NasaPoly2::validate")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))  # parent must be able to unpickle anything from sims.*
STEPS_DEG = (2.0, 1.0, 0.5, 0.25)
FS = 1.25
POINTS = {
    "CH3OH/best_dry": ("CH3OH", 16, 0.0, 320.0),
    "CH3OH/best_overall": ("CH3OH", 23, 0.3, 320.0),
    "CH3OH/water_majority": ("CH3OH", 24, 0.5, 360.0),
    "C2H5OH/best_dry": ("C2H5OH", 24, 0.0, 320.0),
    "C2H5OH/best_overall": ("C2H5OH", 23, 0.4, 320.0),
    "C2H5OH/water_majority": ("C2H5OH", 24, 0.5, 360.0),
}
QTY = ("eff", "IMEP", "T_EVO", "pmax", "closure")


def load_x5():
    # xcheck.py reads REPO from argv[1] at import and expects REPO/code and REPO/results.
    fake = Path(tempfile.mkdtemp(prefix="x5repo-"))
    (fake / "code").symlink_to(ROOT)
    (fake / "results").symlink_to(ROOT / "results")
    argv, sys.argv = sys.argv, [sys.argv[0], str(fake)]
    try:
        spec = importlib.util.spec_from_file_location("x5", ROOT / "scripts_run" / "xcheck.py")
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    finally:
        sys.argv = argv
    return m, fake


def load_m03():
    sys.path.insert(0, str(ROOT))
    return importlib.import_module("sims.03_engine_cycle.run")


def x5_point(name):
    x5, fake = load_x5()
    import numpy as np
    fuel, cr, w, T = POINTS[name]
    ign = json.loads((fake / "results/02_flame_chem/ignition_fits.json").read_text())
    fla = json.loads((fake / "results/02_flame_chem/flame_speed_fits.json").read_text())
    sl = lambda ww: float(np.polyval(fla[fuel]["coefficients_highest_first"], ww))
    dur = min(x5.DUR_CAP, x5.DUR_REF * (sl(0.0) / sl(w)) ** x5.FS_EXP)
    ch = x5.Charge(fuel, cr, w, T)
    fit = ign[fuel]
    ca50 = x5.CA50
    while True:
        r = x5.integrate(ch, ca50, dur, fit)
        if not r["knock"] or ca50 >= x5.RETARD_LIMIT - 1e-12:
            break
        ca50 = min(x5.RETARD_LIMIT, ca50 + x5.RETARD_STEP)
    out = dict(ca50_deg=ca50 / x5.RAD, dur_deg=dur / x5.RAD, steps={})
    for s in STEPS_DEG:
        t0 = time.time()
        r = x5.integrate(ch, ca50, dur, fit, step=s * x5.RAD)
        out["steps"][str(s)] = dict(eff=r["eff"], IMEP=r["IMEP"], T_EVO=r["TEVO"], pmax=r["pmax"],
                                    closure=r["closure"], wall_s=time.time() - t0)
    return ("X5", name, out)


def m03_point(name):
    m = load_m03()
    fuel, cr, w, T = POINTS[name]
    ign, fla, _ = m.read_fits(ROOT / "results" / "02_flame_chem", "full")
    sl, ref = m.check_fits(ign, fla, w, "full")
    dur = m.burn_duration(sl, ref)
    ch = m.Charge(fuel, cr, w, T)
    res = m.retard_search(lambda c: m.integrate_cycle(ch, c, dur, ign))
    ca50 = res["ca50_used_deg"] * m.RAD
    out = dict(ca50_deg=ca50 / m.RAD, dur_deg=dur / m.RAD, steps={})
    for s in STEPS_DEG:
        t0 = time.time()
        r = m.integrate_cycle(ch, ca50, dur, ign, step_rad=s * m.RAD)
        out["steps"][str(s)] = dict(eff=r["gross_indicated_efficiency"], IMEP=r["IMEP_Pa"],
                                    T_EVO=r["EVO_T_K"], pmax=r["peak_pressure_Pa"],
                                    closure=r["energy_closure_error_fraction"], wall_s=time.time() - t0)
    return ("M03", name, out)


def otto(engine):
    res = {}
    for cr in (16, 24):
        res[f"CR{cr}"] = {}
        analytic = 1.0 - cr ** (1.0 - 1.4)
        for s in STEPS_DEG:
            if engine == "X5":
                x5, _ = load_x5()
                r = x5.integrate(x5.IdealCharge(cr), 0.0, 1.0 * x5.RAD, None, evo=math.pi,
                                 step=s * x5.RAD, wall=False)
                eff, clo = r["eff"], r["closure"]
            else:
                m = load_m03(); par = m.DEFAULTS
                r = m.integrate_cycle(m.IdealCharge(cr, 1.4, par), 0.0, par.otto_burn_duration_rad,
                                      None, evo_rad=math.pi, step_rad=s * m.RAD, wall=False, track_no=False)
                eff, clo = r["indicated_work_J"] / r["released_energy_J"], r["energy_closure_error_fraction"]
            res[f"CR{cr}"][str(s)] = dict(eff=eff, analytic=analytic, err=eff - analytic, closure=clo)
    return (engine, "otto", res)


def safe(f, n):
    """Run one task; never let an exception object cross the process boundary."""
    try:
        return f(n)
    except Exception:
        eng = "X5" if f is x5_point else "M03" if f is m03_point else n
        return (eng, "otto" if f is otto else n, {"error": traceback.format_exc()})


def gci(f1, f2, f3, r=2.0):
    """f1 finest. Celik 2008, constant r."""
    d21, d32 = f2 - f1, f3 - f2
    if d21 == 0.0:
        return dict(p=None, f_ext=f1, gci=0.0, monotone=True, ea=0.0)
    ratio = d32 / d21
    monotone = ratio > 0
    p = math.log(abs(ratio)) / math.log(r) if ratio != 0 else None
    if p is None or p <= 0:
        return dict(p=p, f_ext=None, gci=None, monotone=monotone, ea=abs(d21 / f1))
    f_ext = f1 + (f1 - f2) / (r ** p - 1.0)
    ea = abs((f1 - f2) / f1)
    return dict(p=p, f_ext=f_ext, gci=FS * ea / (r ** p - 1.0), monotone=monotone, ea=ea)


def evaluate(raw):
    rep, ok = {"points": {}, "otto": {}, "criteria": {}}, {k: True for k in ("A1", "A1-pmax", "A2", "A3", "A4", "A5")}
    fails = {k: [] for k in ok}
    for name in POINTS:
        rep["points"][name] = {}
        for eng in ("M03", "X5"):
            d = raw[eng][name]; S = d["steps"]
            e = dict(ca50_deg=d["ca50_deg"], dur_deg=d["dur_deg"], qty={})
            for q in ("eff", "IMEP", "T_EVO", "pmax"):
                g = gci(S["0.25"][q], S["0.5"][q], S["1.0"][q])
                g_coarse = gci(S["0.5"][q], S["1.0"][q], S["2.0"][q])
                err05 = abs(S["0.5"][q] - g["f_ext"]) / abs(g["f_ext"]) if g["f_ext"] else None
                e["qty"][q] = dict(values={s: S[s][q] for s in S}, **g, p_coarse=g_coarse["p"], rel_err_at_0p5=err05)
                tag = f"{eng} {name} {q}"
                if q == "pmax":
                    if g["gci"] is None or g["gci"] > 0.01: ok["A1-pmax"] = False; fails["A1-pmax"].append(tag)
                else:
                    if g["gci"] is None or g["gci"] > 1e-3 or err05 is None or err05 > 5e-3:
                        ok["A1"] = False; fails["A1"].append(tag)
                    if g["p"] is None or not (1.5 <= g["p"] <= 2.5) or not g["monotone"]:
                        ok["A2"] = False; fails["A2"].append(f"{tag} p={g['p']}")
            c = S["0.25"]["closure"]
            e["closure"] = {s: S[s]["closure"] for s in S}
            if abs(c) > 1e-3: ok["A3"] = False; fails["A3"].append(f"{eng} {name} closure={c:.3e}")
            rep["points"][name][eng] = e
        cross = {}
        for q in ("eff", "IMEP", "T_EVO", "pmax"):
            a = rep["points"][name]["M03"]["qty"][q]; b = rep["points"][name]["X5"]["qty"][q]
            per_step = {s: (b["values"][s] - a["values"][s]) / a["values"][s] for s in a["values"]}
            ext = (b["f_ext"] - a["f_ext"]) / a["f_ext"] if a["f_ext"] and b["f_ext"] else None
            cross[q] = dict(rel_diff_per_step=per_step, rel_diff_extrapolated=ext)
            if ext is None or abs(ext) > 0.01: ok["A5"] = False; fails["A5"].append(f"{name} {q} {ext}")
        rep["points"][name]["X5_minus_M03"] = cross
    for eng in ("M03", "X5"):
        rep["otto"][eng] = raw[eng]["otto"]
        for crk, v in raw[eng]["otto"].items():
            errs = [abs(v[s]["err"]) for s in ("2.0", "1.0", "0.5", "0.25")]
            if errs[2] > 1e-3 or errs[3] > errs[2] * 1.0001:
                ok["A4"] = False; fails["A4"].append(f"{eng} {crk} err={errs}")
    rep["criteria"] = {k: dict(passed=ok[k], failures=fails[k]) for k in ok}
    return rep


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--procs", type=int, default=6)
    ap.add_argument("--out", default=str(ROOT / "verification" / "x5_m03" / "results"))
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    jobs = [(x5_point, n) for n in POINTS] + [(m03_point, n) for n in POINTS] + [(otto, "X5"), (otto, "M03")]
    with Pool(a.procs) as pool:
        res = [pool.apply_async(safe, (f, n)) for f, n in jobs]
        got = [r.get() for r in res]
    raw = {"X5": {}, "M03": {}}
    for eng, name, d in got:
        raw[eng][name] = d
    (out / "raw.json").write_text(json.dumps(raw, indent=1))
    errors = {f"{e}/{n}": d["error"] for e in raw for n, d in raw[e].items() if "error" in d}
    if errors:
        (out / "errors.json").write_text(json.dumps(errors, indent=1))
        print("TASK ERRORS:", "\n".join(f"{k}: {v.splitlines()[-1]}" for k, v in errors.items()))
        sys.exit(2)
    rep = evaluate(raw); rep["wall_s"] = time.time() - t0
    import cantera, CoolProp
    rep["env"] = dict(python=sys.version.split()[0], cantera=cantera.__version__, coolprop=CoolProp.__version__, procs=a.procs)
    (out / "report.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep["criteria"], indent=1))


if __name__ == "__main__":
    main()
