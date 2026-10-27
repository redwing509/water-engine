#!/usr/bin/env python3
"""Item 1 diagnosis (verification-queue-20261024): why module 03 converges below 2nd order.

Diagnostic only. Each variant switches off / repairs ONE suspected non-smooth element of
sims/03_engine_cycle/run.py integrate_cycle (via a patched copy of its source, the module file is not changed)
and re-runs steps 2, 1, 0.5, 0.25, 0.125 deg CA at frozen CA50/duration (from results/raw.json).
Observed order p from (f(h), f(h/2), f(h/4)) for each consecutive triple.
Variants
  base      unchanged
  tol       inner state inversion rtol 1e-8 -> 1e-11 (iteration noise floor; 1e-13 does not converge: equilibrium noise)
  frozen    equilibrium_min_T_K 1000 -> 1e9 (no frozen/equilibrium switch at T = 1000 K inside a step)
  anchor    start-of-burn Woschni anchor placed on a node at x_b = endgas_anchor_xb (was: left state of the step
            whose RIGHT node first exceeds x_b, i.e. a step-dependent event position)
  nocap     evaporation saturation cap off (schedule only; removes the lagged cap)
  all       tol + frozen + anchor + nocap
  evapfix   keep the saturation cap but evaluate it on a no-evaporation predictor state at the same node
            (mid / right) instead of the left state compressed isentropically (removes the one-step lag)
usage (repo root): python verification/x5_m03/diag/diag_convergence.py [--procs 4]
"""
import argparse, importlib, inspect, json, math, sys, textwrap, warnings
from dataclasses import replace
from multiprocessing import get_context
from pathlib import Path
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
STEPS = (2.0, 1.0, 0.5, 0.25, 0.125)
POINTS = {"CH3OH/best_dry": ("CH3OH", 16, 0.0, 320.0), "CH3OH/water_majority": ("CH3OH", 24, 0.5, 360.0),
          "C2H5OH/best_overall": ("C2H5OH", 23, 0.4, 320.0)}
VARIANTS = ("base", "tol", "frozen", "anchor", "nocap", "all", "tol+anchor", "tol+anchor+frozen", "evapfix", "anchor+evapfix")


EVAP_OLD = """        em = charge.evaporate(e, mid, st, Vm)
        er = max(em, charge.evaporate(e, right, st, Vr))
"""
EVAP_NEW = """        em = charge.evaporate(e, mid, st, Vm)
        if em > e:  # corrector: cap from the no-evaporation predictor state at mid (not the left state)
            s0 = charge.state(U - st["p"] * (Vm - st["V"]) + Qa * (xm - xb) - 0.5 * q_left * dt, Vm, xm, e,
                              (st["T"], st["p"]))
            em = charge.evaporate(e, mid, s0, Vm)
        er = max(em, charge.evaporate(e, right, st, Vr))
"""
EVAP_OLD2 = """        U += -work + Qa * (xr - xb) - d_evap - q_mid * dt
"""
EVAP_NEW2 = """        U += -work + Qa * (xr - xb) - d_evap - q_mid * dt
        if er > e:  # corrector: cap from the no-evaporation right state
            s0 = charge.state(U + d_evap, Vr, xr, e, (sm["T"], sm["p"]))
            er2 = max(em, charge.evaporate(e, right, s0, Vr))
            U -= Lc * (er2 - er); er = er2; d_evap = Lc * (er - e)
"""


def patched_integrate(m, anchor_fix, evap_fix=False):
    src = textwrap.dedent(inspect.getsource(m.integrate_cycle))
    if evap_fix:
        assert EVAP_OLD in src and EVAP_OLD2 in src
        src = src.replace(EVAP_OLD, EVAP_NEW).replace(EVAP_OLD2, EVAP_NEW2)
    if anchor_fix:
        a = "    theta90 = burn_angle(par.knock_burn_fraction, ca50, duration, par)\n"
        assert a in src
        src = src.replace(a, a + "    theta_a = burn_angle(par.endgas_anchor_xb, ca50, duration, par)\n")
        b = "for a in (par.evap_end_rad, theta90)"
        assert b in src; src = src.replace(b, "for a in (par.evap_end_rad, theta90, theta_a)")
        c = "if anchor is None and not charge.ideal and xr >= par.endgas_anchor_xb:"
        assert c in src; src = src.replace(c, "if anchor is None and not charge.ideal and left >= theta_a - 1e-12:")
    ns = dict(vars(m)); exec(compile(src, "integrate_cycle(patched)", "exec"), ns)
    return ns["integrate_cycle"]


def task(arg):
    name, var = arg
    m = importlib.import_module("sims.03_engine_cycle.run")
    raw = json.loads((ROOT / "verification/x5_m03/results/raw.json").read_text())["M03"][name]
    fuel, cr, w, T = POINTS[name]
    ign_all, _, _ = m.read_fits(ROOT / "results" / "02_flame_chem", "full")
    par = m.DEFAULTS
    on = lambda k: var == k or var == "all" or k in var.split("+")
    if on("tol"): par = replace(par, state_rtol_U=1e-11, state_rtol_p=1e-11)
    if on("frozen"): par = replace(par, equilibrium_min_T_K=1e9)
    ch = m.Charge(fuel, cr, w, T, par)
    if on("nocap"):
        ch.evaporate = lambda e_left, theta, left, V: max(e_left, ch.scheduled_fraction(theta))
    integ = patched_integrate(m, on("anchor"), on("evapfix")) if (on("anchor") or on("evapfix")) else m.integrate_cycle
    ca50, dur = raw["ca50_deg"] * m.RAD, raw["dur_deg"] * m.RAD
    out = {}
    for s in STEPS:
        try:
            r = integ(ch, ca50, dur, ign_all[fuel], step_rad=s * m.RAD)
        except Exception as e:
            out[str(s)] = dict(eff=float("nan"), IMEP=float("nan"), T_EVO=float("nan"), pmax=float("nan"),
                               closure=float("nan"), error=str(e)[:200]); continue
        out[str(s)] = dict(eff=r["gross_indicated_efficiency"], IMEP=r["IMEP_Pa"], T_EVO=r["EVO_T_K"],
                           pmax=r["peak_pressure_Pa"], closure=r["energy_closure_error_fraction"])
    return name, var, out


def orders(v):
    f = [v[str(s)] for s in STEPS]; res = []
    for i in range(len(f) - 2):
        d1, d2 = f[i + 1] - f[i], f[i + 2] - f[i + 1]
        res.append(None if d2 == 0 or d1 == 0 or d1 != d1 or d2 != d2 else (math.log(abs(d1 / d2)) / math.log(2), bool(d1 * d2 > 0)))
    return res


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--procs", type=int, default=4)
    ap.add_argument("--variants", default=",".join(VARIANTS)); a = ap.parse_args()
    jobs = [(n, v) for n in POINTS for v in a.variants.split(",")]
    with get_context("spawn").Pool(a.procs) as pool:
        got = pool.map(task, jobs, chunksize=1)
    rep = {}
    for n, v, out in got:
        rep.setdefault(n, {})[v] = dict(values=out, p={q: orders({s: out[s][q] for s in out}) for q in ("eff", "IMEP", "T_EVO")})
    od = ROOT / "verification/x5_m03/diag"; (od / "diag_results.json").write_text(json.dumps(rep, indent=1, default=float))
    for n in rep:
        for v, d in rep[n].items():
            for q in ("eff", "T_EVO"):
                vals = " ".join(f"{d['values'][str(s)][q]:.10g}" for s in STEPS)
                ps = " ".join("  None" if x is None else f"{x[0]:5.2f}{'' if x[1] else '*'}" for x in d["p"][q])
                print(f"{n:22s} {v:18s} {q:5s} {vals}  p(2,1,.5)(1,.5,.25)(.5,.25,.125)= {ps}")


if __name__ == "__main__":
    main()
