"""Module 08 equilibrium benchmark (queue item 5). Tolerances: verification/m08/ACCEPTANCE.md (pre-registered).
Usage (repo root): OMP_NUM_THREADS=1 python -m verification.m08.bench_m08 --out verification/m08/results
"""
import argparse, importlib, json, math, time
from pathlib import Path
import numpy as np
import cantera as ct
from scipy.optimize import brentq, root

M8 = importlib.import_module("sims.08_water_chem.run")
from sims.common import fuels

FUELS = ("CH3OH", "C2H5OH", "CH4")
WS = (0.0, 0.3, 0.6, 0.8)
TU = {"normal": 360.0, "hot": 400.0}
PS = {"1atm": ct.one_atm, "40bar": 40e5}
SUBSET = ["CO2", "CO", "H2O", "H2", "O2", "OH", "H", "O", "N2", "NO", "HO2", "H2O2"]
ELEM = ["C", "H", "O", "N"]
RU = 8.31446261815324  # J/mol/K (CODATA 2018, same as Cantera)
P0 = ct.one_atm

# ---------------- independent thermo evaluation + Gibbs solver (E2)
class Nasa7:
    def __init__(self, mech, names):
        # coefficients read through Cantera's YAML parser; evaluation below is independent code
        sp = {s.name: s for s in ct.Species.list_from_file(mech)}
        self.names = names
        self.A = np.array([[sp[n].composition.get(e, 0) for e in ELEM] for n in names], float)
        self.th = []
        for n in names:
            c = np.asarray(sp[n].thermo.coeffs)   # NasaPoly2: [T_mid, high(7), low(7)]
            assert sp[n].thermo.n_coeffs == 15
            self.th.append((c[0], c[8:15], c[1:8]))

    def _c(self, k, T):
        tmid, lo, hi = self.th[k]
        return lo if T < tmid else hi

    def h_RT(self, T):
        out = []
        for k in range(len(self.names)):
            a = self._c(k, T)
            out.append(a[0] + a[1] * T / 2 + a[2] * T**2 / 3 + a[3] * T**3 / 4 + a[4] * T**4 / 5 + a[5] / T)
        return np.array(out)

    def s_R(self, T):
        out = []
        for k in range(len(self.names)):
            a = self._c(k, T)
            out.append(a[0] * math.log(T) + a[1] * T + a[2] * T**2 / 2 + a[3] * T**3 / 3 + a[4] * T**4 / 4 + a[6])
        return np.array(out)

    def g_RT(self, T):
        return self.h_RT(T) - self.s_R(T)


def gibbs_TP(th, b, T, P, lam0=None):
    """Element-potential equilibrium at fixed T, P. b: element moles. Returns n_k (mol)."""
    g = th.g_RT(T); A = th.A; lp = math.log(P / P0)
    if lam0 is None:
        # guess from complete-combustion majors: H2O, CO2, N2, O2
        idx = [th.names.index(s) for s in ("H2O", "CO2", "N2", "O2")]
        nH2O = b[1] / 2; nCO2 = b[0]; nN2 = b[3] / 2; nO2 = max((b[2] - 2 * nCO2 - nH2O) / 2, 1e-3 * (nH2O + nCO2 + nN2))
        ntot = nH2O + nCO2 + nN2 + nO2
        x = np.array([nH2O, max(nCO2, 1e-12), nN2, nO2]) / ntot
        lam0 = np.linalg.lstsq(A[idx], np.log(x) + lp + g[idx], rcond=None)[0]
        lnn0 = math.log(ntot)
    else:
        lam0, lnn0 = lam0
    active = np.array([b[j] > 0 for j in range(len(ELEM))])
    def nk(z):
        lam = np.zeros(len(ELEM)); lam[active] = z[:-1]
        lam[~active] = -1e3
        return np.exp(z[-1] - lp + A @ lam - g)
    def F(z):
        n = nk(z); ntot = math.exp(z[-1])
        r = [(A[:, j] @ n - b[j]) / b.sum() for j in range(len(ELEM)) if active[j]]
        r.append((n.sum() - ntot) / ntot)
        return r
    z0 = np.concatenate([lam0[active], [lnn0]])
    sol = root(F, z0, method="hybr", options=dict(xtol=1e-14))
    if not sol.success or max(abs(np.array(F(sol.x)))) > 1e-11:
        sol = root(F, z0, method="lm", options=dict(xtol=1e-15, ftol=1e-15))
    lam = np.zeros(len(ELEM)); lam[active] = sol.x[:-1]
    return nk(sol.x), (lam, sol.x[-1]), max(abs(np.array(F(sol.x))))


def gibbs_HP(th, b, H_target, P):
    """T such that sum n_k h_k(T) = H_target [J]."""
    state = {}
    def f(T):
        n, lam, res = gibbs_TP(th, b, T, P)
        state["n"], state["res"] = n, res
        return (n @ th.h_RT(T)) * RU * T - H_target
    T = brentq(f, 600.0, 4500.0, xtol=1e-9, rtol=1e-14)
    f(T)
    return T, state["n"], state["res"]


# ---------------- helpers
def full_gas(fuel, w, Tu, P):
    return M8._gas(fuel, "real", 1.0, w, Tu, P)


def majors(gas, thr):
    return {n: float(x) for n, x in zip(gas.species_names, gas.X) if x > thr}


def e1_e2_e4(fuel, w, regime, pkey):
    Tu, P = TU[regime], PS[pkey]
    mech = M8._mechanism_path(fuel, "real")
    row = dict(fuel=fuel, w=w, regime=regime, T_u_K=Tu, p=pkey)
    # E1: module 08 function + alternative Cantera solvers
    r = M8.adiabatic_temperature(fuel, "real", 1.0, w, Tu, P)
    row["T_ad_module08_K"] = r["T_ad_K"]
    g_def = full_gas(fuel, w, Tu, P); g_def.equilibrate("HP")
    sols = {"element_potential": g_def}
    for s in ("gibbs", "vcs"):
        g = full_gas(fuel, w, Tu, P)
        try:
            g.equilibrate("HP", solver=s); sols[s] = g
        except ct.CanteraError as ex:
            row[f"{s}_error"] = str(ex)[:200]
    Ts = {k: float(v.T) for k, v in sols.items()}
    row["T_ad_by_solver_K"] = Ts
    ref = sols["element_potential"]; mj = [k for k, x in enumerate(ref.X) if x > 1e-4]
    row["E1_T_spread_K"] = max(Ts.values()) - min(Ts.values()) if len(Ts) == 3 else None
    row["E1_T_vs_module08_K"] = abs(Ts["element_potential"] - r["T_ad_K"])
    row["E1_max_major_absdiff"] = max(float(np.max(np.abs(v.X[mj] - ref.X[mj]))) for v in sols.values())
    row["E1_pass"] = bool(len(Ts) == 3 and row["E1_T_spread_K"] <= 0.1 and row["E1_T_vs_module08_K"] <= 0.1
                          and row["E1_max_major_absdiff"] <= 1e-6)
    # E2: subset
    g0 = full_gas(fuel, w, Tu, P)
    H_J_per_kg = g0.enthalpy_mass
    b = np.array([g0.elemental_mole_fraction(e) if False else 0.0 for e in ELEM])
    # element moles per kg of mixture, from Cantera composition (mol/kg)
    nmol = g0.X / (g0.mean_molecular_weight / 1000.0)  # mol species per kg
    b = np.array([sum(g0.n_atoms(k, e) * nmol[k] for k in range(g0.n_species)) for e in ELEM])
    # independent reactant enthalpy (own NASA eval) as a sub-check
    thR = Nasa7(mech, [n for n in g0.species_names if g0.X[g0.species_index(n)] > 0])
    nR = np.array([nmol[g0.species_index(n)] for n in thR.names])
    H_own = float(nR @ thR.h_RT(Tu)) * RU * Tu
    row["E2_H_react_own_vs_cantera_rel"] = abs(H_own - H_J_per_kg) / abs(H_J_per_kg)
    allsp = {s.name for s in ct.Species.list_from_file(mech)}
    SUB = [n for n in SUBSET if n in allsp]   # sandiego has no NO (disclosed)
    row['subset_species'] = SUB
    th = Nasa7(mech, SUB)
    T_own, n_own, res = gibbs_HP(th, b, H_own, P)
    x_own = n_own / n_own.sum()
    spc = [s for s in ct.Species.list_from_file(mech) if s.name in SUB]
    gs = ct.Solution(thermo="ideal-gas", species=spc)
    # start subset gas at complete-combustion composition, same elements
    comp = {"H2O": b[1] / 2, "CO2": b[0], "N2": b[3] / 2, "O2": (b[2] - 2 * b[0] - b[1] / 2) / 2}
    comp = {k: max(v, 0.0) for k, v in comp.items()}
    gs.TPX = 2000.0, P, comp
    gs.HP = H_J_per_kg, P
    gs.equilibrate("HP")
    xs = np.array([gs.X[gs.species_index(n)] for n in SUB])
    sel = xs > 1e-6
    row.update(T_ad_subset_own_K=T_own, T_ad_subset_cantera_K=float(gs.T), E2_solver_residual=res,
               E2_T_absdiff_K=abs(T_own - gs.T), E2_X_max_reldiff=float(np.max(np.abs(x_own[sel] - xs[sel]) / xs[sel])),
               X_subset_own={n: float(x) for n, x in zip(SUB, x_own)})
    row["E2_pass"] = bool(row["E2_T_absdiff_K"] <= 0.05 and row["E2_X_max_reldiff"] <= 1e-5)
    # E4 report
    row["E4_full_minus_subset_K"] = Ts["element_potential"] - float(gs.T)
    if w > 0:
        for v in ("fh2o_a", "fh2o_b"):
            try:
                rr = M8.adiabatic_temperature(fuel, v, 1.0, w, Tu, P)
                row[f"E4_T_ad_{v}_K"] = rr["T_ad_K"]
            except Exception as ex:
                row[f"E4_T_ad_{v}_K"] = None; row[f"E4_{v}_error"] = repr(ex)[:200]
    return row


def e3(w, regime):
    T0 = {"normal": 900.0, "hot": 1000.0}[regime]
    P = M8.IGNITION_P_PA; p = M8.DEFAULTS
    gas = M8._gas("CH3OH", "real", 1.0, w, T0, P)
    geq = M8._gas("CH3OH", "real", 1.0, w, T0, P); geq.equilibrate("UV")
    reactor = ct.IdealGasReactor(gas, energy="on", clone=True)
    net = ct.ReactorNet([reactor]); net.rtol, net.atol = p.reactor_rtol, p.reactor_atol
    # same stepping loop as run.py ignition_delay / oxygen_bookkeeping
    tmax = p.ignition_max_time_s
    while net.time < tmax:
        rem = tmax - net.time
        if rem <= np.finfo(float).eps * tmax: break
        if rem <= p.ignition_max_step_s: net.advance(tmax)
        else:
            net.max_time_step = p.ignition_max_step_s; net.step()
    st = reactor.phase
    mj = [k for k, x in enumerate(geq.X) if x > 1e-3]
    rel = float(np.max(np.abs(st.X[mj] - geq.X[mj]) / geq.X[mj]))
    row = dict(fuel="CH3OH", w=w, regime=regime, T0_K=T0, p_Pa=P, T_reactor_K=float(st.T), T_eq_UV_K=float(geq.T),
               p_reactor_Pa=float(st.P), p_eq_Pa=float(geq.P), E3_T_absdiff_K=abs(st.T - geq.T), E3_X_major_max_rel=rel,
               majors_eq={geq.species_names[k]: float(geq.X[k]) for k in mj})
    row["E3_pass"] = bool(row["E3_T_absdiff_K"] <= 0.5 and rel <= 1e-3)
    return row


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="verification/m08/results")
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    rows = [e1_e2_e4(f, w, rg, pk) for f in FUELS for w in WS for rg in TU for pk in PS]
    r3 = [e3(w, rg) for w in (0.0, 0.6) for rg in ("normal", "hot")]
    rep = dict(E1_pass=all(r["E1_pass"] for r in rows), E2_pass=all(r["E2_pass"] for r in rows),
               E3_pass=all(r["E3_pass"] for r in r3),
               E1_max_T_spread_K=max(r["E1_T_spread_K"] or 0 for r in rows),
               E1_max_major_absdiff=max(r["E1_max_major_absdiff"] for r in rows),
               E2_max_T_absdiff_K=max(r["E2_T_absdiff_K"] for r in rows),
               E2_max_X_reldiff=max(r["E2_X_max_reldiff"] for r in rows),
               E2_max_H_own_vs_cantera_rel=max(r["E2_H_react_own_vs_cantera_rel"] for r in rows),
               E3_max_T_absdiff_K=max(r["E3_T_absdiff_K"] for r in r3),
               E3_max_X_rel=max(r["E3_X_major_max_rel"] for r in r3),
               failures=[(r["fuel"], r["w"], r["regime"], r["p"], k) for r in rows for k in ("E1_pass", "E2_pass") if not r[k]]
                        + [("CH3OH", r["w"], r["regime"], "E3") for r in r3 if not r["E3_pass"]])
    rep["overall_pass"] = rep["E1_pass"] and rep["E2_pass"] and rep["E3_pass"]
    rep["runtime_s"] = time.perf_counter() - t0
    (out / "report.json").write_text(json.dumps(dict(summary=rep, hp_rows=rows, uv_rows=r3), indent=1, default=float))
    print(json.dumps(rep, indent=1, default=float))


if __name__ == "__main__":
    main()
