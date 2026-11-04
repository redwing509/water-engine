"""Independent end-gas knock engine for M03-CRN (job water-engine-box-20261025-1520, step 3).

Not a Livengood-Wu integral and no ignition-delay correlation: the unburned end-gas is integrated with
FULL detailed chemistry (CRECK TPRF_HT_LT_ALC_339_9781, 339 species / 9781 reactions, with the
low-temperature / NTC chemistry that end-gas autoignition needs; Ranzi et al. PECS 2012, CRECKMODELING
Kinetic-Mechanisms, Gas-Phase/Gasoline-Biogasoline) and is compressed by M03-CRN's OWN cylinder pressure
trace p(theta) (Engine.trace, recorded on the CRN sample grid).

Model: adiabatic, homogeneous end-gas parcel. Start at theta0 = min(EVAP_END, Wiebe start) with the
CRN bulk T, p at theta0 and the CRN unburned composition at the Wiebe start (fuel, air, residual, water
vapour; lumped blend species are split into IC8H18 / NC7H16 / C2H5OH by the blend's mole fractions).
March in steps of dtheta (default 0.05 CAD) to the crank angle at which the Wiebe burned fraction
x_b = 0.90. Each step: (a) chemistry at constant pressure for dt (Cantera IdealGasConstPressureReactor,
CVODES), (b) isentropic frozen-composition compression to the next trace pressure (first-order
operator splitting). Knock = chemical dT/dt > 1e7 K/s OR an OH spike (X_OH > 1e-3; pre-ignition end-gas
OH is < 1e-6, hot ignition gives 1e-3..1e-2) before x_b = 0.90.
Deviation recorded: the CRN bulk kinetics are GRI-3.0 fuel-free; the end-gas therefore uses the CRECK LT
mechanism, not "the same mechanism". The parcel is adiabatic (no end-gas wall heat loss: conservative)."""
import math
import cantera as ct
import numpy as np

MECH = "/workspace/creck-lt/tprf_ht_lt_alc.yaml"
DTDT_KNOCK = 1.0e7
XOH_KNOCK = 1.0e-3
_G = {}


def gas(mech=MECH):
    if mech not in _G:
        _G[mech] = ct.Solution(mech)
    return _G[mech]


def theta_xb(wb, xb=0.90):
    lo, hi = wb.start, wb.start + 10 * wb.D
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if wb.x(mid) < xb else (lo, mid)
    return 0.5 * (lo + hi)


def endgas_Y(crn_gas, Y, split, mech=MECH):
    """Map CRN mass fractions onto the CRECK species. split = {lumped name: {component: mass fraction}}."""
    g = gas(mech)
    out = {}
    dropped = 0.0
    for k, name in enumerate(crn_gas.species_names):
        y = float(Y[k])
        if y <= 0:
            continue
        if name in split:
            for comp, f in split[name].items():
                out[comp] = out.get(comp, 0.0) + y * f
        elif name in g.species_names:
            out[name] = out.get(name, 0.0) + y
        else:
            dropped += y
    return out, dropped


def run_endgas(trace, wb, Y0, T_override=None, theta0=None, dtheta_deg=0.05, rpm=2000.0, mech=MECH):
    """trace: array (theta rad, P, T). Returns dict with knock flag, theta, max dT/dt, max X_OH."""
    g = gas(mech)
    omega = rpm * 2 * math.pi / 60.0
    th_tr, p_tr, T_tr = trace[:, 0], trace[:, 1], trace[:, 2]
    th_end = theta_xb(wb, 0.90)
    th0 = theta0 if theta0 is not None else wb.start
    lnp = lambda th: float(np.interp(th, th_tr, np.log(p_tr)))
    T0 = T_override if T_override is not None else float(np.interp(th0, th_tr, T_tr))
    g.TPY = T0, math.exp(lnp(th0)), Y0
    r = ct.IdealGasConstPressureReactor(g, clone=False)
    net = ct.ReactorNet([r])
    net.rtol, net.atol = 1e-8, 1e-15
    i_oh = g.species_index("OH")
    d = dtheta_deg * math.pi / 180.0
    dt = d / omega
    th = th0
    max_dTdt, th_max_dTdt, max_oh, knock, th_knock, why = 0.0, th0, 0.0, False, None, None
    T_hist = []
    while th < th_end - 1e-12:
        h = min(d, th_end - th)
        T_b = r.T
        net.advance(net.time + h / omega)
        dTdt = (r.T - T_b) / (h / omega)
        xoh = float(r.phase.X[i_oh])
        if dTdt > max_dTdt:
            max_dTdt, th_max_dTdt = dTdt, th + h
        max_oh = max(max_oh, xoh)
        th += h
        T_hist.append((th / math.pi * 180.0, r.T, r.phase.P))
        if not knock and (dTdt > DTDT_KNOCK or xoh > XOH_KNOCK):
            knock, th_knock = True, th
            why = "dT/dt" if dTdt > DTDT_KNOCK else "OH"
            break
        # isentropic frozen compression to the next trace pressure
        s = r.phase.entropy_mass
        Y = r.phase.Y
        g.SPY = s, math.exp(lnp(th)), Y
        r.syncState()
        net.reinitialize()
    deg = 180.0 / math.pi
    return dict(knock=knock, knock_trigger=why, theta_knock_deg=None if th_knock is None else th_knock * deg,
                theta0_deg=th0 * deg, theta_xb90_deg=th_end * deg, T0_K=T0, p0_Pa=math.exp(lnp(th0)),
                T_end_K=float(r.T), max_dTdt_K_s=float(max_dTdt), theta_max_dTdt_deg=th_max_dTdt * deg,
                max_X_OH=max_oh, dtheta_deg=dtheta_deg, mech="CRECK TPRF_HT_LT_ALC_339_9781",
                criteria=f"dT/dt>{DTDT_KNOCK:g} K/s or X_OH>{XOH_KNOCK:g} before xb=0.90")
