"""Port-wall film evaporation capacity per cycle - VENDORED copy of capacity() from wme1-hiT
sims/dual_temp/port_film_wall_T.py (as carried on wme1-spray11 63815e6, sims/dual_temp/port_film_wall_T.py),
unchanged physics, so Track A can evaluate the bound-(i) port-wall capacity and the Module 11 misfire flag at any
port-wall temperature (job water-engine-box-20261025-0915 step 5: 363/375/388 K) and at w != the design point.

STATUS: executed estimate only -- NOT verified by a second engine and NOT validated against experiment.
Capacity = min(gas-side Spalding/Gilliland mass transfer while the intake valve is open, wall heat supply
h_film (T_wall - T_bubble) capped at CHF); Raoult bubble point of the deposited film (see the source docstring).
"""
import math
from CoolProp.CoolProp import PropsSI
from scipy.optimize import brentq

CP_NAME = {"CH3OH": "Methanol", "C2H5OH": "Ethanol", "H2O": "Water"}
MW = {"CH3OH": 0.03204, "C2H5OH": 0.04607, "H2O": 0.018015}
D_AIR_300 = {"CH3OH": 1.6e-5, "C2H5OH": 1.2e-5, "H2O": 2.5e-5}   # binary diffusivity in air at 300 K, 1 atm [m2/s]
RPM, P_PORT, D_RUN, U_RUN = 2000.0, 1.0e5, 0.035, 30.0           # Module 03 / Module 09 reference values
DUTY = 230.0 / 720.0
CHF = 1.0e6
def psat(sp, T):
    Tc = PropsSI("Tcrit", CP_NAME[sp])
    return PropsSI("P", "T", min(T, Tc - 1), "Q", 0, CP_NAME[sp])

def hfg(sp, T):
    n = CP_NAME[sp]
    T = min(T, PropsSI("Tcrit", n) - 5)
    return PropsSI("H", "T", T, "Q", 1, n) - PropsSI("H", "T", T, "Q", 0, n)

def bubble_T(x, alc):
    f = lambda T: x[alc] * psat(alc, T) + x["H2O"] * psat("H2O", T) - P_PORT
    return brentq(f, 250.0, 600.0)

def capacity(m_a, m_w, alc, T_wall, T_gas, L_wet, h_film):
    """kg/cycle (alcohol, water) the wetted patch can evaporate; regime label."""
    A = math.pi * D_RUN * L_wet
    t_cyc = 120.0 / RPM
    n_a, n_w = m_a / MW[alc], m_w / MW["H2O"]
    if n_a + n_w <= 0:
        return 0.0, 0.0, "no_film"
    x = {alc: n_a / (n_a + n_w), "H2O": n_w / (n_a + n_w)}
    Tb = bubble_T(x, alc)
    wa, ww = m_a / (m_a + m_w), m_w / (m_a + m_w)
    L_mix = wa * hfg(alc, min(T_wall, Tb)) + ww * hfg("H2O", min(T_wall, Tb))
    # (b) heat supply: superheat over bubble point if boiling, else drive to wet-bulb ~ keep 5 K minimum
    dT = max(T_wall - Tb, 5.0)
    q = min(CHF, h_film * dT)
    m_heat = q * A * t_cyc / L_mix
    if T_wall >= Tb:
        regime, m_tot = "boiling (heat-limited)", m_heat
    else:
        T_f = 0.5 * (T_wall + T_gas)
        rho = P_PORT / (287.0 * T_f)
        mu = PropsSI("V", "T", T_f, "P", P_PORT, "Air")
        p_a, p_w = x[alc] * psat(alc, T_wall), x["H2O"] * psat("H2O", T_wall)
        Mv = (p_a * MW[alc] + p_w * MW["H2O"]) / (p_a + p_w)
        Xv = (p_a + p_w) / P_PORT
        Ys = Xv * Mv / (Xv * Mv + (1 - Xv) * 0.02897)
        B = Ys / (1.0 - Ys)
        D = (wa * D_AIR_300[alc] + ww * D_AIR_300["H2O"]) * (T_f / 300.0) ** 1.75
        Re, Sc = rho * U_RUN * D_RUN / mu, mu / (rho * D)
        h_m = 0.023 * Re ** 0.83 * Sc ** 0.44 * D / D_RUN
        m_gas = rho * h_m * math.log1p(B) * A * t_cyc * DUTY
        regime = "gas-side mass transfer" if m_gas < m_heat else "heat-limited"
        m_tot = min(m_gas, m_heat)
    # split: deposited composition (methanol-first preference ignored -> conservative for the alcohol)
    return m_tot * wa, m_tot * ww, regime

