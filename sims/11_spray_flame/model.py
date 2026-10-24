"""Module 11 spray_flame: Ballal-Lefebvre spray-flame speed and minimum ignition energy (SPEC 12.3).

Pure functions, SI units. All empirical constants are named with their source.

Gas-phase laminar burning velocity
  S_L,g(w) comes from Module 02 (results/02_flame_chem/flame_speed_fits.json; Cantera/San Diego
  free flames at T0 = 400 K, p0 = 1 atm, phi = 1, cubic in w). It is moved to the spark state with the
  Metghalchi & Keck (1982) power law S_L = S_L0 (T/T0)^a (p/p0)^b, a = 2.18 - 0.8(phi-1),
  b = -0.16 + 0.22(phi-1) (Combust. Flame 48:191; fitted for methanol, isooctane, propane up to
  ~50 atm and ~700 K). Water-vapour dilution is already in the Module 02 w dependence.

Liquid water still airborne at spark is a heat sink: it is assumed to evaporate inside the preheat
zone (upper bound on the penalty), lowering the adiabatic flame temperature by Y_wl*h_fg/cp. The
burning velocity follows the Zeldovich/Frank-Kamenetskii scaling
  S_L ~ exp(-E_a / (2 R T_ad)),  overall E_a = E_A_J_MOL (named parameter, see below).

Spray flame speed (Ballal & Lefebvre 1981, 18th Symp. (Int.) Combust., 321-328), quiescent mists:
  S_BL = sqrt( alpha / ( tau_e + alpha / S_L'^2 ) ),
  tau_e = (1 - Omega) rho_F D32^2 / (8 phi rho_g alpha ln(1 + B))      (d2-law evaporation time
          per unit equivalence ratio; alpha = k/(rho cp) of the gas),
  Omega = vapour fraction of the alcohol. With no liquid alcohol tau_e = 0 and S_BL = S_L' exactly.

Vapour-flame floor (physics bound, documented as a correction of the B-L additive-time form): the
pre-vaporised part of the charge is itself a premixed mixture of equivalence ratio Omega*phi. If it
is flammable, a gas-phase flame propagates through it at S_L,g(Omega*phi) whatever the droplets do,
so S_eff = max(S_BL, S_L,g(Omega*phi)). The phi dependence uses the Metghalchi & Keck (1982)
methanol form S ~ B_m + B_phi (phi - phi_m)^2 as a RATIO to its phi = 1 value (B_m = 36.9 cm/s,
B_phi = -140.5 cm/s, phi_m = 1.11). Both S_BL and S_eff are reported.

Minimum ignition energy (Ballal & Lefebvre 1979, Proc. R. Soc. Lond. A 364:277-294; Lefebvre,
Atomization and Sprays, 1989, ch. 9; gas-phase quench distance from Ballal & Lefebvre 1975,
Proc. R. Soc. Lond. A 344:217):
  d_q^2 = (1 - Omega) rho_F D32^2 / (rho_g phi ln(1 + B))  +  (C_Q alpha / S_L')^2,   C_Q = 10
  MIE   = cp rho_g dT_ad (pi/6) d_q^3
The evaporation-limited and reaction-limited quench distances are combined in quadrature; with no
liquid MIE reduces to the gas-phase value.

VALIDITY: the B-L correlations were fitted to quiescent or low-turbulence mists of hydrocarbon
fuels at 0.1-1 atm, ~290-300 K, SMD ~ 20-200 um. The engine spark state here (25-35 bar, 650-820 K,
turbulent) is far outside that range: results are an EXTRAPOLATED, model-only screening estimate,
NOT validated.
"""

from dataclasses import dataclass, asdict
import math

import numpy as np

R_U = 8.314462618  # J/(mol K)


@dataclass(frozen=True)
class Params:
    T0_K: float = 400.0          # Module 02 fit reference
    p0_Pa: float = 101325.0
    phi: float = 1.0             # Module 03 design points run at phi = 1
    C_Q: float = 10.0            # Ballal & Lefebvre (1975): gas quench distance d_q = 10 alpha / S_L
    C_EVAP: float = 8.0          # d2-law evaporation constant (K = 8 rho_g alpha ln(1+B) / rho_F, Le = 1)
    E_A_J_MOL: float = 1.25e5    # overall activation energy, typical 25-40 kcal/mol for alcohol/HC flames
                                 # (Law, Combustion Physics, 2006, ch. 7); sensitivity reported
    MK_Bm: float = 0.369         # Metghalchi & Keck (1982) methanol, m/s
    MK_Bphi: float = -1.405      # m/s
    MK_phim: float = 1.11
    E_SPARK_LOW_J: float = 0.050   # SPEC 12.3: typical spark 50-100 mJ
    E_SPARK_HIGH_J: float = 0.100
    S_RATIO_MIN: float = 0.90    # flame-speed criterion for the recommended SMD: <= 10 % slow-down
    D_MAX_SEARCH_m: float = 1.0e-3


DEF = Params()


def poly_SL(fit: dict, w: float) -> float:
    """Module 02 cubic fit S_L(w) at T0, p0, phi = 1 [m/s]."""
    lo, hi = fit["valid_w_range"]
    if not (lo - 1e-12 <= w <= hi + 1e-12):
        raise ValueError(f"w = {w} outside Module 02 fit range {fit['valid_w_range']}")
    return float(np.polyval(fit["coefficients_highest_first"], w))


def mk_exponents(phi: float) -> tuple[float, float]:
    return 2.18 - 0.8 * (phi - 1.0), -0.16 + 0.22 * (phi - 1.0)


def SL_at_state(SL0: float, T_K: float, p_Pa: float, p: Params = DEF) -> float:
    a, b = mk_exponents(p.phi)
    return SL0 * (T_K / p.T0_K) ** a * (p_Pa / p.p0_Pa) ** b


def mk_phi_ratio(phi_v: float, p: Params = DEF) -> float:
    """S_L(phi_v)/S_L(phi) from the Metghalchi-Keck parabola, floored at 0 (non-flammable)."""
    s = lambda f: p.MK_Bm + p.MK_Bphi * (f - p.MK_phim) ** 2
    return max(0.0, s(phi_v)) / s(p.phi)


def heat_sink_factor(dT_sink: float, T_ad: float, p: Params = DEF) -> float:
    """S_L'/S_L for a flame-temperature drop dT_sink (Zeldovich scaling)."""
    if dT_sink <= 0:
        return 1.0
    T2 = T_ad - dT_sink
    if T2 <= 0:
        return 0.0
    return math.exp(-p.E_A_J_MOL / (2 * R_U) * (1.0 / T2 - 1.0 / T_ad))


@dataclass
class State:
    """Unburned gas state at spark plus liquid properties."""
    T_K: float
    p_Pa: float
    rho_g: float       # kg/m3
    cp_g: float        # J/(kg K)
    alpha: float       # m2/s
    T_ad_K: float      # adiabatic flame temperature of the fully vaporised charge
    rho_F: float       # liquid alcohol density
    B: float           # Spalding transfer number of the alcohol
    h_fg_w: float      # water latent heat J/kg
    SL_gas: float      # S_L at spark state, fully vaporised charge, m/s


def spray_point(st: State, f_liq_fuel: float, Y_wl: float, D32: float, p: Params = DEF) -> dict:
    """Ballal-Lefebvre evaluation for liquid alcohol fraction f_liq_fuel (= 1 - Omega, of the alcohol),
    liquid-water mass fraction of the charge Y_wl and SMD D32 [m]."""
    if not (0.0 <= f_liq_fuel <= 1.0) or Y_wl < 0 or D32 < 0:
        raise ValueError("invalid spray state")
    dT_ad = st.T_ad_K - st.T_K
    dT_sink = Y_wl * st.h_fg_w / st.cp_g
    SLp = st.SL_gas * heat_sink_factor(dT_sink, st.T_ad_K, p)
    lnB = math.log1p(st.B)
    tau_c = st.alpha / SLp ** 2 if SLp > 0 else math.inf
    tau_e = f_liq_fuel * st.rho_F * D32 ** 2 / (p.C_EVAP * p.phi * st.rho_g * st.alpha * lnB)
    S_BL = math.sqrt(st.alpha / (tau_e + tau_c)) if math.isfinite(tau_c) else 0.0
    S_vap = SLp * mk_phi_ratio((1.0 - f_liq_fuel) * p.phi, p)
    S_eff = max(S_BL, S_vap)
    dq_e2 = f_liq_fuel * st.rho_F * D32 ** 2 / (st.rho_g * p.phi * lnB)
    dq_g = p.C_Q * st.alpha / SLp if SLp > 0 else math.inf
    dq = math.sqrt(dq_e2 + dq_g ** 2)
    dT_eff = max(dT_ad - dT_sink, 0.0)
    MIE = st.cp_g * st.rho_g * dT_eff * math.pi / 6.0 * dq ** 3
    return dict(S_L_gas_m_s=st.SL_gas, S_L_heat_sink_m_s=SLp, S_BL_m_s=S_BL, S_vapour_floor_m_s=S_vap,
                S_eff_m_s=S_eff, S_BL_over_SL=S_BL / st.SL_gas, S_eff_over_SL=S_eff / st.SL_gas,
                tau_evap_s=tau_e, tau_chem_s=tau_c, d_q_m=dq, d_q_gas_m=dq_g, MIE_J=MIE,
                dT_heat_sink_K=dT_sink)


def _bisect_max_D(pred, Dmax: float) -> float | None:
    """Largest D in [0, Dmax] with pred(D) True, assuming monotonic; Dmax if always true, 0 if never."""
    if pred(Dmax):
        return Dmax
    if not pred(1e-9):
        return 0.0
    lo, hi = 1e-9, Dmax
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        lo, hi = (mid, hi) if pred(mid) else (lo, mid)
    return lo


def max_smd(st: State, f_liq_fuel: float, Y_wl: float, p: Params = DEF) -> dict:
    """Maximum SMD at spark for: MIE <= 50 mJ, MIE <= 100 mJ, S_BL/S_L >= S_RATIO_MIN, S_eff/S_L >= S_RATIO_MIN."""
    f = lambda D: spray_point(st, f_liq_fuel, Y_wl, D, p)
    return {
        "D_max_MIE_50mJ_m": _bisect_max_D(lambda D: f(D)["MIE_J"] <= p.E_SPARK_LOW_J, p.D_MAX_SEARCH_m),
        "D_max_MIE_100mJ_m": _bisect_max_D(lambda D: f(D)["MIE_J"] <= p.E_SPARK_HIGH_J, p.D_MAX_SEARCH_m),
        "D_max_SBL_ratio_m": _bisect_max_D(lambda D: f(D)["S_BL_over_SL"] >= p.S_RATIO_MIN, p.D_MAX_SEARCH_m),
        "D_max_Seff_ratio_m": _bisect_max_D(lambda D: f(D)["S_eff_over_SL"] >= p.S_RATIO_MIN, p.D_MAX_SEARCH_m),
    }


def params_dict(p: Params = DEF) -> dict:
    return asdict(p)
