"""Tabulated property package for Module 09 (SI units throughout).

Sources (SPEC section 0.2: every assumption named, sourced or reasoned):
* Liquid water: CoolProp IAPWS-95 (Wagner & Pruss 2002) saturated-liquid
  density, cp, enthalpy, viscosity, surface tension, saturation pressure.
* Liquid methanol: CoolProp Methanol EOS (de Reuck & Craven 1993) with its
  CoolProp transport and surface-tension correlations.
* Vapour and air ideal-gas thermo: Cantera GRI-Mech 3.0 NASA polynomials
  (Smith et al. 1999), the same thermo data sims/common/fuels.py uses.
* Dilute-gas viscosity, conductivity and vapour/air binary diffusivity:
  Cantera mixture-averaged transport with GRI-Mech 3.0 transport data.
  Diffusivity is tabulated at 1 bar and scaled with 1/p (Chapman-Enskog).
* Film mixture viscosity and conductivity: Wilke (1950) mixing rule, with
  the Mason & Saxena (1958) form for conductivity.
* Methanol(1)-water(2) liquid non-ideality: Wilson equation, a12 = 107.38
  and a21 = 469.55 cal/mol, V1 = 40.73 and V2 = 18.07 cm3/mol; NRTL
  b12 = -253.88, b21 = 845.21 cal/mol, alpha = 0.2994. Both are the values
  recommended by Gmehling et al., Vapor-Liquid Equilibrium Data Collection,
  DECHEMA Chemistry Data Series vol. I (1977-1988), as tabulated in Smith,
  Van Ness & Abbott, Introduction to Chemical Engineering Thermodynamics,
  7th ed., Table 13.10. Wilson is used; NRTL is kept as a cross-check.
* Liquid-mixture density by ideal volume additivity and cp by mass
  weighting (excess volume, about -3 %, and excess cp are neglected).
  Mixture surface tension (mole-fraction weighting) and viscosity
  (Arrhenius log mixing) are IDEAL approximations used only by the
  atomiser SMD correlations; real methanol-water surface tension falls
  faster with methanol than linear, so blend SMDs are biased high.

Enthalpy consistency: the liquid enthalpy is CoolProp's saturated-liquid
h(T) shifted so that h_vap,Cantera(298.15 K) - h_liq(298.15 K) equals
CoolProp's h_fg(298.15 K). The latent heat used by the droplet model is
then L(T) = h_vap,Cantera(T) - h_liq(T), so the gas + liquid energy ledger
closes by construction (L differs from CoolProp's real-gas h_fg by the
vapour's departure function, < 1 % below 1 bar).
"""

from dataclasses import dataclass
from functools import lru_cache
import math
from pathlib import Path
import warnings

import cantera as ct
import numpy as np
from CoolProp.CoolProp import PropsSI


R_U = 8.314462618  # J/(mol K), CODATA 2018.
R_CAL = 1.98720425864083  # cal/(mol K), R_U / 4.184.
LIQUIDS = ("H2O", "CH3OH")  # index 0 = water, 1 = alcohol (methanol by default)
ALCOHOLS = ("CH3OH", "C2H5OH")
COOLPROP = {"H2O": "Water", "CH3OH": "Methanol", "C2H5OH": "Ethanol"}
GAS_SPECIES = ("AIR", "H2O", "CH3OH")  # AIR is a frozen N2/O2 pseudo-species; index 2 = alcohol vapour
# GRI-Mech 3.0 has no ethanol; its thermo and transport come from the San Diego
# mechanism already used by Modules 02/03 (mechanisms/sandiego.yaml, PROVENANCE.md).
SANDIEGO = Path(__file__).resolve().parents[2] / "mechanisms" / "sandiego.yaml"
AIR_X = {"O2": 1.0, "N2": 3.76}  # SPEC fuels.AIR_N2_O2 dry-air approximation
REF_T = 298.15

# Wilson / NRTL parameters (component 1 = methanol, 2 = water), cal/mol and
# cm3/mol. Gmehling et al., DECHEMA Chem. Data Ser. vol. I, via Smith, Van
# Ness & Abbott (2005) Table 13.10.
WILSON = dict(a12=107.38, a21=469.55, V1=40.73, V2=18.07)
NRTL = dict(b12=-253.88, b21=845.21, alpha=0.2994)
ACTIVITY_SOURCE = ("Gmehling et al., Vapor-Liquid Equilibrium Data Collection, DECHEMA "
                   "Chemistry Data Series vol. I (1977-1988), via Smith, Van Ness & Abbott, "
                   "Intro. Chem. Eng. Thermodynamics 7th ed., Table 13.10")
# Ethanol(1)-water(2): DECHEMA parameters as distributed in the ChemSep interaction-
# parameter database (Kooijman & Taylor 2008; thermo package, ChemSep/wilson.json and
# nrtl.ipd). Wilson there: ln L12 = -1.17693 - 192.381/T, ln L21 = 1.17693 - 480.801/T,
# i.e. a12 = 192.381 R = 382.30 cal/mol, a21 = 480.801 R = 955.45 cal/mol and
# V2/V1 = exp(-1.17693) = 0.30819 (V1 = 58.63 cm3/mol with V2 = 18.07). NRTL (1 atm):
# b12 = -57.9601, b21 = 1241.7396 cal/mol, alpha = 0.2937.
WILSON_ETOH = dict(a12=192.38082765657816 * 1.98720425864083, a21=480.8011032813958 * 1.98720425864083,
                   V1=18.07 / math.exp(-1.1769274893976625), V2=18.07)
NRTL_ETOH = dict(b12=-57.9601, b21=1241.7396, alpha=0.2937)
ACTIVITY_SOURCE_ETOH = ("DECHEMA (Gmehling et al.) ethanol-water parameters as distributed in the ChemSep "
                        "interaction-parameter database (Kooijman & Taylor 2008), files wilson.json / nrtl.ipd "
                        "of the 'thermo' Python package (C. Bell)")
ACTIVITY = {"CH3OH": (WILSON, NRTL, ACTIVITY_SOURCE), "C2H5OH": (WILSON_ETOH, NRTL_ETOH, ACTIVITY_SOURCE_ETOH)}


def wilson_gamma(x_m, T, fuel="CH3OH"):
    """Wilson activity coefficients (gamma_water, gamma_alcohol)."""
    W = ACTIVITY[fuel][0]
    x1 = np.clip(np.asarray(x_m, float), 0.0, 1.0)
    x2 = 1.0 - x1
    T = np.asarray(T, float)
    L12 = W["V2"] / W["V1"] * np.exp(-W["a12"] / (R_CAL * T))
    L21 = W["V1"] / W["V2"] * np.exp(-W["a21"] / (R_CAL * T))
    s1 = x1 + x2 * L12
    s2 = x2 + x1 * L21
    term = L12 / s1 - L21 / s2
    lng1 = -np.log(s1) + x2 * term
    lng2 = -np.log(s2) - x1 * term
    return np.exp(lng2), np.exp(lng1)


def nrtl_gamma(x_m, T, fuel="CH3OH"):
    """NRTL activity coefficients (gamma_water, gamma_alcohol)."""
    N = ACTIVITY[fuel][1]
    x1 = np.clip(np.asarray(x_m, float), 0.0, 1.0)
    x2 = 1.0 - x1
    T = np.asarray(T, float)
    t12 = N["b12"] / (R_CAL * T)
    t21 = N["b21"] / (R_CAL * T)
    G12 = np.exp(-N["alpha"] * t12)
    G21 = np.exp(-N["alpha"] * t21)
    lng1 = x2**2 * (t21 * (G21 / (x1 + x2 * G21))**2 + t12 * G12 / (x2 + x1 * G12)**2)
    lng2 = x1**2 * (t12 * (G12 / (x2 + x1 * G12))**2 + t21 * G21 / (x1 + x2 * G21)**2)
    return np.exp(lng2), np.exp(lng1)


@dataclass(frozen=True)
class Tables:
    """1-D tables on uniform temperature grids, evaluated with np.interp."""

    TL: np.ndarray            # liquid grid [K]
    psat: np.ndarray          # (2, n) Pa
    rho_l: np.ndarray         # (2, n) kg/m3
    cp_l: np.ndarray          # (2, n) J/(kg K)
    h_l: np.ndarray           # (2, n) J/kg (shifted, see module doc)
    mu_l: np.ndarray          # (2, n) Pa s
    sigma_l: np.ndarray       # (2, n) N/m
    TG: np.ndarray            # gas grid [K]
    h_g: np.ndarray           # (3, n) J/kg, Cantera absolute enthalpy
    cp_g: np.ndarray          # (3, n) J/(kg K)
    mu_g: np.ndarray          # (3, n) Pa s
    k_g: np.ndarray           # (3, n) W/(m K)
    D_1bar: np.ndarray        # (2, n) m2/s vapour-in-air at 1e5 Pa
    M_g: np.ndarray           # (3,) kg/mol
    Tmax_l: np.ndarray        # (2,) upper end of the liquid table [K]
    fuel: str = "CH3OH"       # alcohol in slot 1 (liquid) / 2 (gas)


def murphy_koop_psat(T):
    """Vapour pressure of (supercooled) liquid water [Pa], 123-332 K.

    Murphy & Koop (2005), Q. J. R. Meteorol. Soc. 131:1539, eq. 10. Used only
    below CoolProp's 273.16 K triple point (wet-methanol droplets can cool
    below 0 C without freezing: the blend freezing point is depressed).
    """
    T = np.asarray(T, float)
    return np.exp(54.842763 - 6763.22 / T - 4.210 * np.log(T) + 0.000367 * T
                  + np.tanh(0.0415 * (T - 218.8))
                  * (53.878 - 1331.22 / T - 9.44523 * np.log(T) + 0.014025 * T))


T_SUBZERO = 273.2  # below this, water liquid properties are extrapolated


def _liquid_grid(name, T):
    fl = COOLPROP[name]
    out = {k: [] for k in ("psat", "rho", "cp", "h", "mu", "sigma")}
    if name == "H2O":
        hi = T[T >= T_SUBZERO]
        res = _liquid_grid_cp(fl, hi)
        lo = T[T < T_SUBZERO]
        # Supercooled extrapolation: Murphy-Koop psat; cp, rho, mu, sigma held at
        # the 273.2 K value; h = h(273.2) - cp (273.2 - T). Rationale: only blend
        # droplets in strongly saturation-cooled charges reach this range.
        n = lo.size
        full = {}
        for k, v in res.items():
            full[k] = np.concatenate([np.full(n, v[0]), v])
        full["psat"][:n] = murphy_koop_psat(lo)
        full["h"][:n] = res["h"][0] - res["cp"][0] * (T_SUBZERO - lo)
        return full
    return _liquid_grid_cp(fl, T)


def _liquid_grid_cp(fl, T):
    out = {k: [] for k in ("psat", "rho", "cp", "h", "mu", "sigma")}
    for t in T:
        out["psat"].append(PropsSI("P", "T", t, "Q", 0, fl))
        out["rho"].append(PropsSI("Dmass", "T", t, "Q", 0, fl))
        out["cp"].append(PropsSI("Cpmass", "T", t, "Q", 0, fl))
        out["h"].append(PropsSI("Hmass", "T", t, "Q", 0, fl))
        out["mu"].append(PropsSI("V", "T", t, "Q", 0, fl))
        out["sigma"].append(PropsSI("I", "T", t, "Q", 0, fl))
    return {k: np.array(v) for k, v in out.items()}


def _gas_for(species):
    if species == "C2H5OH":
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return ct.Solution(str(SANDIEGO))
    return ct.Solution("gri30.yaml")


@lru_cache(maxsize=4)
def tables(fuel: str = "CH3OH") -> Tables:
    """Build (once per process and alcohol) the property tables."""
    if fuel not in ALCOHOLS:
        raise ValueError(f"unsupported alcohol {fuel!r}")
    liquids = ("H2O", fuel)
    # Liquid grid: 223.2 K .. 505 K (critical points: methanol 512.6 K, ethanol 514.7 K).
    TL = np.arange(223.2, 505.01, 0.5)
    gri = ct.Solution("gri30.yaml")
    TG = np.arange(200.0, 1500.01, 2.0)
    names = {"AIR": AIR_X, "H2O": {"H2O": 1.0}, fuel: {fuel: 1.0}}
    h_g = np.zeros((3, TG.size)); cp_g = np.zeros_like(h_g)
    mu_g = np.zeros_like(h_g); k_g = np.zeros_like(h_g)
    D = np.zeros((2, TG.size)); M = np.zeros(3)
    for j, (key, comp) in enumerate(names.items()):
        gas = _gas_for(key)
        for i, t in enumerate(TG):
            gas.TPX = t, 1e5, comp
            h_g[j, i] = gas.enthalpy_mass
            cp_g[j, i] = gas.cp_mass
            mu_g[j, i] = gas.viscosity
            k_g[j, i] = gas.thermal_conductivity
        M[j] = gas.mean_molecular_weight / 1000.0
    for j, sp in enumerate(liquids):
        gas = _gas_for(sp)
        isp = gas.species_index(sp); iN2 = gas.species_index("N2")
        for i, t in enumerate(TG):
            gas.TPX = t, 1e5, AIR_X
            D[j, i] = gas.binary_diff_coeffs[isp, iN2]
    liq = [_liquid_grid(n, TL) for n in liquids]
    h_l = []
    for j, n in enumerate(liquids):
        gas = _gas_for(n)
        gas.TPX = REF_T, 1e5, {n: 1.0}
        hv_ref = gas.enthalpy_mass
        fl = COOLPROP[n]
        hfg_ref = PropsSI("Hmass", "T", REF_T, "Q", 1, fl) - PropsSI("Hmass", "T", REF_T, "Q", 0, fl)
        h0 = PropsSI("Hmass", "T", REF_T, "Q", 0, fl)
        h_l.append(liq[j]["h"] - h0 + hv_ref - hfg_ref)  # CoolProp h_l already in J/kg
    st = lambda k: np.vstack([liq[0][k], liq[1][k]])
    return Tables(TL=TL, psat=st("psat"), rho_l=st("rho"), cp_l=st("cp"), h_l=np.vstack(h_l),
                  mu_l=st("mu"), sigma_l=st("sigma"), TG=TG, h_g=h_g, cp_g=cp_g, mu_g=mu_g,
                  k_g=k_g, D_1bar=D, M_g=M, Tmax_l=np.array([TL[-1], TL[-1]]), fuel=fuel)


def interp(table_row, grid, T):
    return np.interp(T, grid, table_row)


def liquid(tab: Tables, k: int, T):
    """Dict of pure-liquid k properties at T (array)."""
    TL = tab.TL
    return dict(psat=np.interp(T, TL, tab.psat[k]), rho=np.interp(T, TL, tab.rho_l[k]),
                cp=np.interp(T, TL, tab.cp_l[k]), h=np.interp(T, TL, tab.h_l[k]))


def gas_h(tab: Tables, j: int, T):
    return np.interp(T, tab.TG, tab.h_g[j])


def gas_cp(tab: Tables, j: int, T):
    return np.interp(T, tab.TG, tab.cp_g[j])


def film_transport(tab: Tables, T, X):
    """Wilke mixture viscosity and Mason-Saxena conductivity.

    T: (n,), X: (n, 3) mole fractions of (AIR, H2O, CH3OH). Returns mu, k.
    """
    mu = np.stack([np.interp(T, tab.TG, tab.mu_g[j]) for j in range(3)], axis=1)
    kk = np.stack([np.interp(T, tab.TG, tab.k_g[j]) for j in range(3)], axis=1)
    M = tab.M_g
    # Phi_ij = [1 + (mu_i/mu_j)^0.5 (M_j/M_i)^0.25]^2 / [8 (1 + M_i/M_j)]^0.5
    mr = mu[:, :, None] / mu[:, None, :]
    Mr = M[None, :, None] / M[None, None, :]  # M_i / M_j
    phi = (1.0 + np.sqrt(mr) * Mr**-0.25)**2 / np.sqrt(8.0 * (1.0 + Mr))
    denom = np.einsum("nij,nj->ni", phi, X)
    mu_mix = np.sum(X * mu / denom, axis=1)
    k_mix = np.sum(X * kk / denom, axis=1)
    return mu_mix, k_mix


def diffusivity(tab: Tables, j: int, T, p):
    """Binary diffusivity of vapour j (0 water, 1 methanol) in air [m2/s]."""
    return np.interp(T, tab.TG, tab.D_1bar[j]) * (1e5 / p)


def blend_physical(tab: Tables, Y_m: float, T: float = 300.0):
    """Liquid density, viscosity, surface tension of a methanol-water blend.

    Density: ideal volume additivity. Viscosity: Arrhenius log mixing on mole
    fraction. Surface tension: mole-fraction weighting. The latter two are
    ideal approximations (see module docstring) used by SMD correlations.
    """
    Mw, Mm = tab.M_g[1], tab.M_g[2]
    Y = np.array([1.0 - Y_m, Y_m])
    x = (Y / np.array([Mw, Mm])); x = x / x.sum()
    rho = 1.0 / sum(Y[k] / np.interp(T, tab.TL, tab.rho_l[k]) for k in range(2))
    mu = math.exp(sum(x[k] * math.log(np.interp(T, tab.TL, tab.mu_l[k])) for k in range(2)))
    sigma = float(sum(x[k] * np.interp(T, tab.TL, tab.sigma_l[k]) for k in range(2)))
    return dict(rho=float(rho), mu=float(mu), sigma=sigma, x_m=float(x[1]))


def property_assumptions(fuels=("CH3OH",)) -> dict:
    extra = {}
    if "C2H5OH" in fuels:
        extra = {
            "ethanol_liquid": {"value": "CoolProp Ethanol EOS (Schroeder et al. 2014) saturated liquid incl. CoolProp transport/surface tension"},
            "ethanol_vapour": {"value": "San Diego mechanism NASA7 thermo + transport (mechanisms/sandiego.yaml), GRI-Mech 3.0 has no ethanol",
                               "caveat": "NASA7 low range starts at 300 K; 200-300 K gas values are polynomial extrapolation"},
            "activity_model_ethanol": {"value": "Wilson", "parameters_cal_mol": WILSON_ETOH, "source": ACTIVITY_SOURCE_ETOH,
                                       "cross_check": {"model": "NRTL", "parameters_cal_mol": NRTL_ETOH}},
        }
    return extra | {
        "liquid_properties": {"value": "CoolProp saturated liquid (water IAPWS-95; methanol de Reuck & Craven 1993)", "coolprop": True},
        "gas_thermo_transport": {"value": "Cantera GRI-Mech 3.0 NASA polynomials and mixture-averaged transport", "cantera_version": ct.__version__},
        "film_mixing_rule": {"value": "Wilke (1950) viscosity, Mason & Saxena (1958) conductivity"},
        "activity_model": {"value": "Wilson", "parameters_cal_mol": WILSON, "source": ACTIVITY_SOURCE,
                           "cross_check": {"model": "NRTL", "parameters_cal_mol": NRTL}},
        "liquid_mixture_density": {"value": "ideal volume additivity", "rationale": "excess volume of methanol-water about -3 %, neglected"},
        "blend_sigma_mu_for_SMD": {"value": "ideal mole-fraction sigma, Arrhenius log-mole mu", "caveat": "approximation; real blend sigma is lower, so blend SMD is biased high"},
    }
