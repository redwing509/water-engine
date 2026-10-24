"""J2: Module 02 dual-temperature variant (normal vs hot unburned T), with second/third chemistry engines.

James's dual-temperature rule (2026-10-24); Claude box-queue job water-engine-box-queue-20261024-1230, step J2.
Regimes (sims/dual_temp/regimes.py on wme1-hiT): normal intake charge 360 K (upper normal; 320 K is the
cold end), hot 400 K (un-intercooled boost / heated intake). p_IVC = 1 bar (Module 03), phi = 1,
w = m_water/(m_water+m_fuel) in {0, 0.3, 0.6}, water as vapour (Module 02 convention, no latent heat).

Quantities and engines (mechanism choice recorded, per Hermes's X1 note):
  T_ad   1 atm at T_u, and at the TDC-equivalent state      : San Diego (Module 02) vs AramcoMech 2.0 (full, 493 sp)
  tau_ig constant-volume adiabatic at the TDC-equivalent state: San Diego vs AramcoMech 2.0 (full) [+ CRECK HT, info]
  S_L    1 atm at T_u = 360 / 400 K                          : San Diego (Module 02; X1 run, x1_dualT_sandiego.json)
                                                               vs CRECK C1-C3 HT 114 sp (CRECKMODELING v2003)
         (full Aramco FreeFlame is too costly on the box - see results/xcheck/x1_dualT/STATUS.md; not used for S_L)
TDC-equivalent state: frozen-composition isentropic compression from (T_u, 1 bar) by the volume ratio CR
(CR 16 and 24, Module 03 design range), each mechanism with its own thermo.
tau_ig = time of max dT/dt (Module 02 definition), horizon 50 ms, rtol 1e-9 / atol 1e-15.
Tolerances (stated before the run): T_ad +-0.5 %; S_L +-10 %; tau_ig within a factor 2 (|log10 ratio| <= 0.30),
and for every quantity the hot-minus-normal change must have the same sign in both engines.

usage (repo root): python -m sims.xcheck_chem.run_j2_m02_dualT --part {tad_ign,sl} --mech {sandiego,aramco,creck} --workers N
"""
from __future__ import annotations
import argparse, json, math, os, sys, time, warnings, hashlib
from multiprocessing import Pool
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
import numpy as np  # noqa: E402
import cantera as ct  # noqa: E402
from sims.common import fuels  # noqa: E402

MECHS = {"aramco": REPO_ROOT / "mechanisms" / "aramco20.yaml",
         "sandiego": REPO_ROOT / "mechanisms" / "sandiego.yaml",
         "creck": REPO_ROOT / "mechanisms" / "creck_c1c3_ht.yaml"}
FUELS_J2 = ("CH3OH", "C2H5OH")
W = (0.0, 0.3, 0.6)
TU = {"normal": 360.0, "hot": 400.0}
CRS = (16.0, 24.0)
P_IVC = 1.0e5
PHI = 1.0
TAU_MAX = 0.05
OUT = REPO_ROOT / "results" / "xcheck" / "j2_m02_dualT"
_G = {}


def _init(mech, mem_gb):
    warnings.filterwarnings("ignore")
    if mem_gb:
        import resource
        lim = int(mem_gb * 2**30); resource.setrlimit(resource.RLIMIT_AS, (lim, lim))
    _G["mech"] = str(mech); _G["gas"] = ct.Solution(str(mech))


def tdc_state(gas, fuel, w, Tu, cr):
    gas.TPX = Tu, P_IVC, fuels.mixture(fuel, PHI, w, mech=_G["mech"])
    s, v = gas.entropy_mass, 1.0 / gas.density
    gas.SV = s, v / cr
    return float(gas.T), float(gas.P)


def ignition(gas, T, p, X):
    gas.TPX = T, p, X
    r = ct.IdealGasReactor(gas, energy="on", clone=True)
    net = ct.ReactorNet([r]); net.rtol, net.atol = 1e-9, 1e-15
    def rate():
        st = r.phase
        return float(-np.dot(st.partial_molar_int_energies, st.net_production_rates) / (st.density * st.cv_mass))
    t, q, Tmax = [0.0], [rate()], T
    while net.time < TAU_MAX:
        net.step(); t.append(net.time); q.append(rate()); Tmax = max(Tmax, r.T)
        if Tmax > T + 400 and q[-1] < 1e-3 * max(q):
            break
    k = int(np.argmax(q))
    ok = Tmax - T >= 400 and 0 < k < len(q) - 1
    return (t[k] if ok else None), Tmax - T


def case_tad_ign(c):
    fuel, w, reg, cr = c
    gas = _G["gas"]; Tu = TU[reg]; t0 = time.time()
    row = dict(fuel=fuel, w=w, regime=reg, T_u_K=Tu, CR=cr)
    gas.TPX = Tu, ct.one_atm, fuels.mixture(fuel, PHI, w, mech=_G["mech"]); gas.equilibrate("HP")
    row["T_ad_1atm_K"] = float(gas.T)
    Tt, pt = tdc_state(gas, fuel, w, Tu, cr)
    X = fuels.mixture(fuel, PHI, w, mech=_G["mech"])
    gas.TPX = Tt, pt, X; gas.equilibrate("HP")
    row.update(T_TDC_K=Tt, p_TDC_bar=pt / 1e5, T_ad_TDC_K=float(gas.T))
    try:
        tau, rise = ignition(gas, Tt, pt, X)
        row.update(tau_ig_s=tau, ign_rise_K=float(rise), ign_status="ignited" if tau else f"no ignition in {TAU_MAX*1e3:g} ms")
    except ct.CanteraError as e:
        row.update(tau_ig_s=None, ign_status=f"CanteraError: {str(e)[:200]}")
    row["secs"] = round(time.time() - t0, 1)
    print(f"[{Path(_G['mech']).stem}] {fuel} w={w} {reg} CR{cr:g}: T_TDC={Tt:.0f} K p={pt/1e5:.1f} bar tau={row['tau_ig_s']} ({row['secs']} s)", flush=True)
    return row


def case_sl(c):
    fuel, w, reg = c
    gas = _G["gas"]; Tu = TU[reg]; t0 = time.time()
    row = dict(fuel=fuel, w=w, regime=reg, T_u_K=Tu, S_L_m_s=None, status="solver_error")
    try:
        gas.TPX = Tu, ct.one_atm, fuels.mixture(fuel, PHI, w, mech=_G["mech"])
        f = ct.FreeFlame(gas, width=0.03); f.transport_model = "mixture-averaged"; f.soret_enabled = False
        f.max_grid_points = 600
        f.set_refine_criteria(ratio=3.0, slope=0.1, curve=0.2); f.solve(loglevel=0, auto=True); s1 = float(f.velocity[0])
        f.set_refine_criteria(ratio=2.0, slope=0.05, curve=0.1, prune=0.01); f.solve(loglevel=0, refine_grid=True)
        s2 = float(f.velocity[0])
        row.update(S_L_m_s=s2, S_L_coarse_m_s=s1, grid_rel_change=abs(s2 - s1) / s2, grid_points=len(f.grid),
                   T_max_K=float(max(f.T)), status="computed")
    except Exception as e:
        row["reason"] = f"{type(e).__name__}: {e}"[:300]
    row["secs"] = round(time.time() - t0, 1)
    print(f"[{Path(_G['mech']).stem}] S_L {fuel} w={w} {reg}: {row['S_L_m_s']} ({row['secs']} s)", flush=True)
    return row


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", choices=("tad_ign", "sl"), required=True)
    ap.add_argument("--mech", choices=sorted(MECHS), required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--mem-gb", type=float, default=0.0)
    a = ap.parse_args(argv)
    mech = MECHS[a.mech]; OUT.mkdir(parents=True, exist_ok=True); t0 = time.time()
    if a.part == "tad_ign":
        cases = [(f, w, r, cr) for cr in CRS for r in TU for f in FUELS_J2 for w in W]; fn = case_tad_ign
    else:
        cases = [(f, w, r) for r in TU for f in FUELS_J2 for w in W]; fn = case_sl
    with Pool(a.workers, initializer=_init, initargs=(mech, a.mem_gb), maxtasksperchild=4) as pool:
        rows = pool.map(fn, cases, chunksize=1)
    payload = dict(part=a.part, mechanism=str(mech.relative_to(REPO_ROOT)),
                   mechanism_sha256=hashlib.sha256(mech.read_bytes()).hexdigest(), cantera=ct.__version__,
                   phi=PHI, p_IVC_Pa=P_IVC, T_u_K=TU, CR=CRS, tau_max_s=TAU_MAX, rows=rows,
                   runtime_s=round(time.time() - t0, 1), workers=a.workers)
    (OUT / f"{a.part}_{a.mech}.json").write_text(json.dumps(payload, indent=1) + "\n")
    print("done", a.part, a.mech, payload["runtime_s"], "s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
