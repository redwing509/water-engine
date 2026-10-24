"""SPEC section 6 (Module 03 engine_cycle): closed-cycle SI engine with water.

Execution happens on the Linux simulation server; the laptop only compiles.

Model, SI internally (crank angle in radians; CAD only in outputs):
* 0-D closed system from IVC to EVO for the first law
      dU_s = -p dV + dQ_comb - dQ_wall - dQ_evap.
  Properties by mass fraction burned x_b (SPEC section 6): the unburned part
  is the frozen fresh charge, the burned part is Cantera TP-equilibrium
  products, both at the common bulk (T, p). Only NO uses a two-zone
  burned-gas temperature; knock uses an isentropic unburned end gas.
* Energy (SPEC section 0). Water has zero heating value. The only source is
  the prescribed Wiebe release eta_c * m_fuel * LHV, with LHV from
  sims.common.fuels.lhv (registered fuel phase, H2O(g) products, 298.15 K).
  Energies are SENSIBLE: frozen unburned u(T) - u(T_ref) and burned
  u_eq(T, p) - u_complete(T_ref). Formation energy is therefore counted once,
  by the LHV release, while equilibrium dissociation energy stays in the gas.
* Water enters as liquid at water_T_K. Isobaric intake mixing evaporates up
  to f_evap_intake of it with h_fg, limited to saturation. The rest
  evaporates in the closed cylinder on the SPEC uniform schedule
  IVC -> -30 CAD, also limited to saturation, with the closed-system latent
  heat u_fg = h_fg - p v_fg (a closed control mass does no flow work).
  CoolProp IAPWS-95 (Wagner & Pruss 2002) supplies h_fg, u_fg and p_sat.
* Liquid alcohols release their liquid-phase LHV while modelled as premixed
  vapour: the fuel's own latent heat is debited from the heat release and
  no fuel charge-cooling credit is taken (conservative; see assumptions).

Cantera's ic_engine.py example was not downloaded or run here. From its
published description it is a compression-ignition (Diesel-type) engine with
gaseous fuel injected near TDC, finite-rate chemistry, intake/exhaust valves
and a moving-wall piston over complete open four-stroke cycles. This model is
premixed SI, closed IVC->EVO, prescribed Wiebe release, Woschni walls and
liquid-water evaporation, so the two efficiencies cannot be equated. The
analytic constant-gamma Otto check (SPEC section 10) runs this integrator.
"""

from dataclasses import asdict, dataclass, replace
import hashlib
import json
import math
from pathlib import Path
import time

import cantera as ct
from CoolProp.CoolProp import PropsSI
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

from sims.common import fuels, io


MODULE = "03_engine_cycle"
VERSION = "1.0.0"
FUELS = ("CH3OH", "C2H5OH", "CH4")
# WME-1 design fuels: methanol or ethanol supply all chemical energy (README/SPEC); CH4 is a reference only
# (SPEC section 6) and is never the recommended design point handed to Modules 04 and 06.
DESIGN_FUELS = ("CH3OH", "C2H5OH")
QUICK_FUELS = ("CH4", "CH3OH")
FULL_CR = tuple(range(9, 25))  # WME-1 item 1: sweep extended to 24 (was 9..18)
QUICK_CR = (10, 14, 18)
# WME-1 item 1 sensitivity: S_L x 0.7 for w >= 0.5.
SENSITIVITY = dict(label="S_L x 0.7 for w >= 0.5", flame_speed_factor=0.7,
                   applied_for_w_ge=0.5)
FULL_W = tuple(i / 10 for i in range(9))
QUICK_W = (0.0, 0.6)
FULL_T_INTAKE = (320.0, 360.0)
QUICK_T_INTAKE = (320.0,)
EXAMPLE_CR = 14  # p-V / p-theta example; present in quick and full sweeps.
RAD = math.pi / 180.0  # Integration angles are radians; CAD is output only.
R_MOL = ct.gas_constant / 1000.0  # J/(mol K)
T_REF = fuels.REFERENCE_T_K  # Sensible-energy zero = LHV reference, 298.15 K.
WATER_T_TRIPLE = float(PropsSI("Ttriple", "Water"))
WATER_T_CRIT = float(PropsSI("Tcrit", "Water"))


@dataclass(frozen=True)
class Parameters:
    """Named defaults; sources and rationales are written by assumptions()."""

    bore_m: float = 0.086
    stroke_m: float = 0.086
    rod_m: float = 0.145
    rpm: float = 2000.0
    ivc_rad: float = -math.pi
    evo_rad: float = 140.0 * RAD
    residual_fraction: float = 0.05
    p_ivc_Pa: float = 1.0e5
    phi: float = 1.0
    wiebe_a: float = 5.0
    wiebe_m: float = 2.0
    combustion_efficiency: float = 0.98
    burn_duration_ref_rad: float = 25.0 * RAD
    burn_duration_cap_rad: float = 80.0 * RAD
    flame_speed_exponent: float = 0.5
    ca50_rad: float = 8.0 * RAD
    knock_burn_fraction: float = 0.9
    retard_step_rad: float = 2.0 * RAD
    retard_limit_rad: float = 30.0 * RAD
    endgas_anchor_xb: float = 1.0e-3
    selection_ca50_limit_rad: float = 15.0 * RAD
    flame_speed_min_m_s: float = 0.08
    peak_pressure_limit_Pa: float = 120.0e5
    wall_T_K: float = 450.0
    woschni_C: float = 3.26
    woschni_C1: float = 2.28
    woschni_C2: float = 3.24e-3
    f_evap_intake: float = 0.5
    evap_end_rad: float = -30.0 * RAD
    water_T_K: float = 300.0
    step_rad: float = 0.5 * RAD
    quick_step_rad: float = 1.0 * RAD
    equilibrium_min_T_K: float = 1000.0
    state_rtol_U: float = 1.0e-8
    state_rtol_p: float = 1.0e-8
    knock_integral_cap: float = 1.0e6
    closure_tolerance: float = 0.02
    otto_gamma: float = 1.4
    otto_tolerance_abs: float = 0.01
    otto_burn_duration_rad: float = 1.0 * RAD
    otto_step_rad: float = 0.5 * RAD
    otto_T_ivc_K: float = 300.0
    otto_gas_constant_J_kg_K: float = 287.0
    otto_heat_per_mass_J_kg: float = 1.5e6
    no_min_xb: float = 1.0e-3
    no_absolute_uncertainty_factor: float = 2.0
    plausible_efficiency_min: float = 0.30
    plausible_efficiency_max: float = 0.50
    limit_flame_temperature_K: float = 1500.0


DEFAULTS = Parameters()


class PointUnavailable(ValueError):
    """Explicit input-domain limitation, never a fabricated cycle result."""


# ----------------------------------------------------------------- geometry
def displacement(par=DEFAULTS):
    """Swept volume [m3]."""
    return math.pi * par.bore_m**2 / 4.0 * par.stroke_m


def volume(theta, cr, par=DEFAULTS):
    """Slider-crank cylinder volume [m3]; theta [rad] after TDC.

    Heywood (1988), Internal Combustion Engine Fundamentals, eq. 2.4-2.5.
    """
    a = par.stroke_m / 2.0
    s = a * math.cos(theta) + math.sqrt(par.rod_m**2 - (a * math.sin(theta))**2)
    return (displacement(par) / (cr - 1.0)
            + math.pi * par.bore_m**2 / 4.0 * (par.rod_m + a - s))


def wall_area(V, par=DEFAULTS):
    """Head + piston crown (flat) + exposed liner area [m2]."""
    return 2.0 * math.pi * par.bore_m**2 / 4.0 + 4.0 * V / par.bore_m


# -------------------------------------------------------------------- Wiebe
def _wiebe_z(x, par):
    return (-math.log1p(-x) / par.wiebe_a) ** (1.0 / (par.wiebe_m + 1.0))


def wiebe(theta, ca50, duration, par=DEFAULTS):
    """Mass fraction burned, x = 1 - exp(-a z^(m+1)); Heywood (1988) eq. 9.23.

    Parametrised by CA50 and the 10-90 % duration (exact, untruncated).
    """
    scale = duration / (_wiebe_z(0.9, par) - _wiebe_z(0.1, par))
    start = ca50 - scale * _wiebe_z(0.5, par)
    progress = max(0.0, (theta - start) / scale)
    return -math.expm1(-par.wiebe_a * progress ** (par.wiebe_m + 1.0))


def burn_angle(fraction, ca50, duration, par=DEFAULTS):
    """Crank angle [rad] at which the Wiebe curve reaches `fraction`."""
    span = _wiebe_z(0.9, par) - _wiebe_z(0.1, par)
    return ca50 + duration * (_wiebe_z(fraction, par) - _wiebe_z(0.5, par)) / span


def burn_duration(sl, sl_ref, par=DEFAULTS):
    """SPEC: 10-90 % duration = ref * (S_L,ref / S_L(w))^0.5, capped."""
    return min(par.burn_duration_cap_rad,
               par.burn_duration_ref_rad * (sl_ref / sl) ** par.flame_speed_exponent)


# --------------------------------------------------------- Module 02 fits
# QUICK-MODE FALLBACK ONLY (never used by --full): clearly labelled synthetic
# fits so --quick and CI run before Module 02 full results exist.
# Ignition: Douaud & Eyzat (1978), SAE 780080, as given by Heywood (1988)
# section 9.6: tau = 17.68 ms (ON/100)^3.402 p[atm]^-1.7 exp(3800 K / T).
# It was fitted to primary reference fuels (ON 80-100); applying it to CH4
# (RON ~120, beyond the PRF scale) and to the alcohols is an extrapolation.
# Research octane numbers: commonly tabulated values (methane 120, methanol
# 108.7, ethanol 108.6). Water enters only through end-gas temperature
# (c = 0): no chemical water effect is asserted by the fallback.
# Flame speed: linear 0.5 -> 0.1 m/s over w = 0..0.8 at 400 K, 1 atm; only
# the ratio S_L(0)/S_L(w) and the 0.08 m/s constraint use it. NOT DATA.
SYNTHETIC_RON = {"CH4": 120.0, "CH3OH": 108.7, "C2H5OH": 108.6}
SYNTHETIC_FLAME_COEFFICIENTS = [0.0, 0.0, -0.5, 0.5]
SYNTHETIC_FLAME_W_RANGE = [0.0, 0.8]


def synthetic_ignition_fit(fuel):
    """Douaud-Eyzat in the Module 02 schema: tau = A p^-n exp(E/RT)(1+c w)."""
    octane = SYNTHETIC_RON[fuel]
    return dict(status="synthetic", mode="synthetic", A=17.68e-3 * (octane / 100.0) ** 3.402
                * ct.one_atm ** 1.7, n=1.7, E_J_per_mol=3800.0 * R_MOL, c=0.0,
                pressure_unit="Pa", A_unit="s*Pa**1.7", valid_T_K_range=None,
                valid_p_Pa_range=None, valid_w_range=None, octane_number=octane,
                source="SYNTHETIC quick fallback: Douaud & Eyzat (1978) SAE 780080 form; not Module 02")


def synthetic_flame_fit(fuel):
    return dict(status="synthetic", mode="synthetic", S_L_unit="m/s",
                coefficients_highest_first=list(SYNTHETIC_FLAME_COEFFICIENTS),
                polynomial_degree=1, valid_w_range=list(SYNTHETIC_FLAME_W_RANGE),
                phi=1.0, T_unburned_K=400.0, p_Pa=ct.one_atm,
                source="SYNTHETIC quick fallback: linear placeholder; not Module 02")


def synthetic_fits(names=FUELS):
    return ({f: synthetic_ignition_fit(f) for f in names},
            {f: synthetic_flame_fit(f) for f in names})


def _usable(ignition, flame):
    return (isinstance(ignition, dict) and isinstance(flame, dict)
            and ignition.get("status") in {"fitted", "quick_linear"}
            and flame.get("status") in {"fitted", "quick_linear"})


def read_fits(directory, mode, names=FUELS):
    """Return (ignition, flame, provenance) keyed by fuel.

    --full: both Module 02 files must exist and must not be quick-mode fits.
    --quick: missing files, or unusable per-fuel entries, are replaced by the
    labelled synthetic fallback and recorded per fuel.
    """
    paths = [Path(directory) / name for name in ("ignition_fits.json", "flame_speed_fits.json")]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing and mode != "quick":
        raise FileNotFoundError("--full requires Module 02 fit files (run sims.02_flame_chem "
                                "--full first, or pass --fits-dir): " + ", ".join(missing))
    ignition, flame, files = {}, {}, []
    if not missing:
        ignition, flame = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
        if not isinstance(ignition, dict) or not isinstance(flame, dict):
            raise ValueError("Module 02 fit files must be JSON objects keyed by fuel")
        files = [dict(path=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths]
        if mode == "full":
            quick = [f for f in names for d in (ignition, flame)
                     if isinstance(d.get(f), dict) and d[f].get("mode") == "quick"]
            if quick:
                raise ValueError("--full refuses quick-mode Module 02 fits for: " + ", ".join(sorted(set(quick))))
    per_fuel = {}
    for fuel in names:
        if _usable(ignition.get(fuel), flame.get(fuel)):
            per_fuel[fuel] = "module_02"
        elif mode == "quick":
            ignition[fuel], flame[fuel] = synthetic_ignition_fit(fuel), synthetic_flame_fit(fuel)
            per_fuel[fuel] = "synthetic_fallback"
        else:
            per_fuel[fuel] = "unusable_module_02_fit"
    synthetic = any(v == "synthetic_fallback" for v in per_fuel.values())
    return ignition, flame, dict(
        label="mode-quick-fallback" if synthetic else mode, synthetic=synthetic,
        missing=missing, files=files, per_fuel=per_fuel,
        warning=("SYNTHETIC fallback fits (Douaud-Eyzat ignition form, linear S_L) were used: "
                 "results demonstrate the software only and are NOT for design") if synthetic else None)


def check_fits(ignition, flame, w, mode="full"):
    """Validate fit schema/units; return (S_L(w), S_L(0)) [m/s]. No extrapolation in w."""
    allowed = {"fitted"} if mode == "full" else {"fitted", "quick_linear", "synthetic"}
    if not isinstance(ignition, dict) or not isinstance(flame, dict):
        raise PointUnavailable("Missing Module 02 fit for this fuel")
    if ignition.get("status") not in allowed or flame.get("status") not in allowed:
        raise PointUnavailable(f"Module 02 fit status not usable in {mode} mode: "
                               f"ignition={ignition.get('status')}, flame={flame.get('status')}")
    if ignition.get("pressure_unit") != "Pa":
        raise PointUnavailable("Ignition fit pressure_unit must be Pa (A in s*Pa**n, E in J/mol)")
    for key in ("A", "n", "E_J_per_mol", "c"):
        value = ignition.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise PointUnavailable("Invalid ignition fit parameter: " + key)
    if ignition["A"] <= 0 or 1.0 + ignition["c"] * w <= 0:
        raise PointUnavailable("Ignition fit gives a nonpositive delay")
    coeff = flame.get("coefficients_highest_first")
    bounds = flame.get("valid_w_range")
    if (not isinstance(coeff, list) or len(coeff) != 4
            or not all(isinstance(c, (int, float)) and math.isfinite(c) for c in coeff)):
        raise PointUnavailable("Flame-speed cubic unavailable")
    if flame.get("S_L_unit") != "m/s" or flame.get("phi") != 1.0:
        raise PointUnavailable("Flame-speed fit must be in m/s at fuel-air phi = 1")
    if not bounds or not bounds[0] <= 0.0 <= w <= bounds[1] + 1e-12:
        raise PointUnavailable(f"w = {w:g} outside the flame-speed fit range {bounds}; no extrapolation")
    sl, ref = float(np.polyval(coeff, w)), float(np.polyval(coeff, 0.0))
    if min(sl, ref) <= 0:
        raise PointUnavailable("Flame-speed fit gives a nonpositive speed")
    return sl, ref


def ignition_rate(T, p, w, fit):
    """1/tau [1/s] with tau = A p^-n exp(E/(R T)) (1 + c w); p in Pa, E in J/mol."""
    log_rate = (-math.log(fit["A"]) + fit["n"] * math.log(p)
                - fit["E_J_per_mol"] / (R_MOL * T) - math.log1p(fit["c"] * w))
    return math.exp(min(700.0, max(-700.0, log_rate)))


def outside_fit(fit, T, p, w):
    """True if (T, p, w) lies outside a fit's stated calibration ranges."""
    for key, value in (("valid_T_K_range", T), ("valid_p_Pa_range", p), ("valid_w_range", w)):
        bounds = fit.get(key)
        if bounds and not bounds[0] <= value <= bounds[1]:
            return True
    return False


def water_p_sat(T):
    """Saturation pressure of water [Pa]; 0 below the triple point, inf above Tc."""
    if T >= WATER_T_CRIT:
        return math.inf
    if T < WATER_T_TRIPLE:
        return 0.0
    return float(PropsSI("P", "T", T, "Q", 1, "Water"))


# ------------------------------------------------------------ thermodynamics
class Phases:
    """Worker-local Cantera objects for one fuel's mechanism (never pickled)."""

    def __init__(self, fuel):
        self.fuel = fuel
        self.selection = fuels.select_mechanism(fuel)
        self.gas = fuels.load_mechanism(fuel)     # species thermo
        self.burned = fuels.load_mechanism(fuel)  # TP equilibrium of the burned part
        self.endgas = fuels.load_mechanism(fuel)  # frozen unburned isentrope
        self.flame = fuels.load_mechanism(fuel)   # flame temperature and NO radical pool
        g = self.gas
        self.n = g.n_species
        self.MW = np.array(g.molecular_weights, dtype=float)  # kg/kmol
        self.inv_MW = 1.0 / self.MW
        names = ["O2", "N2", "H2O", "O", "OH", "H"]
        if fuels.FUELS[fuel].atoms[0]:
            names.append("CO2")
        self.i = {name: g.species_index(fuels.species_name(g, name)) for name in names}
        self.i_fuel = g.species_index(fuels.species_name(g, fuel))
        self.lhv = fuels.lhv(fuel)
        self._T = None
        self.u_ref = self.species_u(T_REF).copy()
        self.h_ref = self.species_h(T_REF).copy()

    def _set(self, T):
        if T != self._T:
            self.gas.TP = T, ct.one_atm
            self._h_RT = np.array(self.gas.standard_enthalpies_RT)
            self._cp_R = np.array(self.gas.standard_cp_R)
            self._T = T

    def species_h(self, T):
        """Ideal-gas species enthalpy [J/kg], formation-inclusive (Cantera)."""
        self._set(T)
        return self._h_RT * (ct.gas_constant * T) * self.inv_MW

    def species_u(self, T):
        """Ideal-gas species internal energy u = h - RT [J/kg]."""
        self._set(T)
        return (self._h_RT - 1.0) * (ct.gas_constant * T) * self.inv_MW

    def species_cv(self, T):
        self._set(T)
        return (self._cp_R - 1.0) * ct.gas_constant * self.inv_MW

    def equilibrium_masses(self, masses, T, p):
        """Species masses [kg] after TP equilibrium at fixed elements and mass."""
        total = float(masses.sum())
        b = self.burned
        b.TPY = T, p, masses / total
        b.equilibrate("TP")
        return np.array(b.Y) * total


_PHASES = {}


def phases(fuel):
    """Per-process cache; spawned workers build their own Cantera objects."""
    if fuel not in _PHASES:
        _PHASES[fuel] = Phases(fuel)
    return _PHASES[fuel]


class Charge:
    """Trapped charge for one (fuel, CR, w, T_intake) point, Cantera properties.

    Mass basis vectors are kg of each species per kg of fuel; `scale` [kg fuel
    per cycle] converts them to the trapped amounts. Droplets have negligible
    volume, stay at water_T_K, and contribute only their latent heat.
    """

    ideal = False

    def __init__(self, fuel, cr, w, T_intake, par=DEFAULTS):
        if not 0.0 <= w < 1.0:
            raise PointUnavailable("w must satisfy 0 <= w < 1")
        if not 0.0 < par.phi <= 1.0:
            raise PointUnavailable("Complete-product reference is defined for 0 < phi <= 1 only")
        self.fuel, self.cr, self.w = fuel, float(cr), float(w)
        self.T_intake, self.par = float(T_intake), par
        ph = self.ph = phases(fuel)
        i, MW = ph.i, ph.MW
        self.j = j = i["H2O"]
        # Fresh fuel + dry air and its complete products (element balance).
        nf = 1.0 / MW[ph.i_fuel]
        demand = fuels.oxygen_demand(fuel) * nf
        o2 = demand / par.phi
        fresh = np.zeros(ph.n)
        fresh[ph.i_fuel] = 1.0
        fresh[i["O2"]] = o2 * MW[i["O2"]]
        fresh[i["N2"]] = fuels.AIR_N2_O2 * o2 * MW[i["N2"]]
        c, h, _ = fuels.FUELS[fuel].atoms
        complete = np.zeros(ph.n)
        if c:
            complete[i["CO2"]] = c * nf * MW[i["CO2"]]
        complete[j] = h / 2.0 * nf * MW[j]
        complete[i["N2"]] = fresh[i["N2"]]
        complete[i["O2"]] = (o2 - demand) * MW[i["O2"]]
        if abs(complete.sum() / fresh.sum() - 1.0) > 1e-9:
            raise RuntimeError("Complete-product reference does not conserve mass")
        r = par.residual_fraction
        residual = complete * r / (1.0 - r)  # r of the dry trapped mass
        self.dry = fresh + residual
        self.burned_ref = complete + residual
        self.water = np.zeros(ph.n)
        self.water[j] = w / (1.0 - w)
        self.m_dry = float(self.dry.sum())
        self.m_water_basis = float(self.water.sum())
        self.air_basis = float(fresh.sum() - 1.0)
        self.residual_basis = float(residual.sum())
        # Latent heats: liquid at T_water -> ideal-gas vapour at T_REF (J/kg).
        Tw = par.water_T_K
        self.h_fg = float(PropsSI("Hmass", "T", Tw, "Q", 1, "Water")
                          - PropsSI("Hmass", "T", Tw, "Q", 0, "Water"))
        self.u_fg = float(PropsSI("Umass", "T", Tw, "Q", 1, "Water")
                          - PropsSI("Umass", "T", Tw, "Q", 0, "Water"))
        self.h_latent = self.h_fg - float(ph.species_h(Tw)[j] - ph.h_ref[j])
        self.u_latent = self.u_fg - float(ph.species_u(Tw)[j] - ph.u_ref[j])
        self._intake()
        vec = self.dry + self.e_intake * self.water
        self.V_ivc = volume(par.ivc_rad, cr, par)
        n_ivc = par.p_ivc_Pa * self.V_ivc / (ct.gas_constant * self.T_ivc)  # kmol
        self.scale = n_ivc / float(vec @ ph.inv_MW)
        self.fuel_mass = self.scale
        self.water_mass = self.scale * self.m_water_basis
        self.air_mass = self.scale * self.air_basis
        self.residual_mass = self.scale * self.residual_basis
        self.gas_mass_ivc = self.scale * float(vec.sum())
        self.Q_fuel = self.fuel_mass * ph.lhv
        self.Q_avail = par.combustion_efficiency * self.Q_fuel
        self.L_cyl = self.water_mass * self.u_latent  # J per unit evaporated fraction
        self.Q_evap_intake = self.water_mass * self.e_intake * self.h_latent
        self.intake_closure_J = (self.scale * (self._H(self.dry, self.T_intake)
                                 - self._H(vec, self.T_ivc)) - self.Q_evap_intake)
        self.U_ivc = self.scale * float(vec @ (ph.species_u(self.T_ivc) - ph.u_ref))
        self.fuel_saturation_ratio_ivc = None
        props = fuels.FUELS[fuel]
        if props.state == "liquid":
            x_fuel = (vec[ph.i_fuel] / MW[ph.i_fuel]) / float(vec @ ph.inv_MW)
            p_fuel = float(PropsSI("P", "T", self.T_ivc, "Q", 1, props.coolprop_name))
            self.fuel_saturation_ratio_ivc = float(x_fuel * par.p_ivc_Pa / p_fuel)

    # Intake: isobaric adiabatic mixing (steady flow), so enthalpy and h_fg.
    def _H(self, vec, T):
        return float(vec @ (self.ph.species_h(T) - self.ph.h_ref))

    def _x_water(self, vec):
        moles = vec * self.ph.inv_MW
        return float(moles[self.j] / moles.sum())

    def _intake_T(self, e):
        """Mixed-charge temperature [K]; None if the latent demand needs T < 150 K."""
        if e <= 0.0:
            return self.T_intake
        target = self._H(self.dry, self.T_intake) - e * self.m_water_basis * self.h_latent
        vec = self.dry + e * self.water

        def balance(T):
            return self._H(vec, T) - target

        if balance(150.0) >= 0.0:
            return None
        return brentq(balance, 150.0, self.T_intake, xtol=1e-10)

    def _intake(self):
        p, f = self.par.p_ivc_Pa, self.par.f_evap_intake

        def excess(e):
            T = self._intake_T(e)
            if T is None or T < WATER_T_TRIPLE:
                return p  # physically impossible: treat as supersaturated
            return self._x_water(self.dry + e * self.water) * p - water_p_sat(T)

        if excess(0.0) > 0.0:
            raise PointUnavailable("Residual water vapour alone is supersaturated at T_intake")
        if self.w == 0.0 or f <= 0.0:
            e = 0.0
        elif excess(f) <= 0.0:
            e = f
        else:
            # f_evap_intake is infeasible: evaporate only up to saturation (wet bulb).
            e = brentq(excess, 0.0, f, xtol=1e-12)
        self.e_intake = float(e)
        self.T_ivc = float(self._intake_T(e))
        self.intake_saturation_limited = bool(self.w > 0.0 and e < f - 1e-9)
        if self.T_ivc < WATER_T_TRIPLE:
            raise PointUnavailable("Intake evaporation would cool the charge below 273.16 K")

    # Closed cylinder: mixture properties by mass fraction burned.
    def masses(self, xb, e):
        unburned = self.scale * (1.0 - xb) * (self.dry + e * self.water)
        burned = self.scale * xb * (self.burned_ref + e * self.water)
        return unburned, burned

    def evaluate(self, T, p, xb, e):
        """Sensible U [J], total kmol and species masses [kg] at (T, p)."""
        mu, mb = self.masses(xb, e)
        mb_eq = mb
        if xb > 0.0 and T > self.par.equilibrium_min_T_K:
            mb_eq = self.ph.equilibrium_masses(mb, T, p)
        total = mu + mb_eq
        U = float(total @ self.ph.species_u(T) - (mu + mb) @ self.ph.u_ref)
        return U, float(total @ self.ph.inv_MW), total

    def state(self, U, V, xb, e, guess):
        """Invert U_s(T, p) = U with p = n R T / V (equilibrium depends on p).

        Secant iteration on T (first slope: frozen cv), p updated each step.
        """
        par = self.par
        T, p = float(guess[0]), float(guess[1])
        tol_U = par.state_rtol_U * self.Q_fuel
        T_old = F_old = None
        for _ in range(80):
            Us, n, masses = self.evaluate(T, p, xb, e)
            p_new = n * ct.gas_constant * T / V
            F = Us - U
            if abs(F) <= tol_U and abs(p_new - p) <= par.state_rtol_p * p_new:
                return dict(T=T, p=p_new, U=Us, V=V, n=n, masses=masses,
                            mass=float(masses.sum()), xb=xb, e=e)
            p = p_new
            slope = (F - F_old) / (T - T_old) if T_old is not None and T != T_old else 0.0
            if not slope > 0.0:
                slope = float(masses @ self.ph.species_cv(T))
            T_old, F_old = T, F
            T = min(6000.0, max(150.0, T - F / slope))
        raise RuntimeError(f"State inversion did not converge (U={U:.6g} J, V={V:.4g} m3, xb={xb:.4g})")

    # Evaporation schedule (SPEC: uniform IVC -> evap_end), saturation capped.
    def scheduled_fraction(self, theta):
        if self.water_mass <= 0.0:
            return 0.0
        p = self.par
        frac = min(1.0, max(0.0, (theta - p.ivc_rad) / (p.evap_end_rad - p.ivc_rad)))
        return self.e_intake + (1.0 - self.e_intake) * frac

    def evaporate(self, e_left, theta, left, V):
        """Evaporated fraction at node (theta, V): schedule, capped at saturation.

        The cap uses the left-node state compressed isentropically to V and
        cooled by the latent heat taken (lagged by one step; the supersaturation
        actually reached is reported as a diagnostic).
        """
        target = self.scheduled_fraction(theta)
        if target <= e_left:
            return e_left
        T_left = left["T"]
        cv = float(left["masses"] @ self.ph.species_cv(T_left))
        gamma = 1.0 + left["n"] * ct.gas_constant / cv
        T_est = T_left * (left["V"] / V) ** (gamma - 1.0)
        if T_est >= WATER_T_CRIT:
            return target
        cooling = self.L_cyl / cv
        n_w0 = float(left["masses"][self.j] / self.ph.MW[self.j])
        dn = self.water_mass / self.ph.MW[self.j]

        def excess(de):
            T = T_est - cooling * de
            if T < WATER_T_TRIPLE:
                return 1e30  # would freeze: certainly beyond saturation (finite for brentq)
            return (n_w0 + dn * de) * ct.gas_constant * T / V - water_p_sat(T)

        span = target - e_left
        if excess(0.0) >= 0.0:
            return e_left
        if excess(span) <= 0.0:
            return target
        return e_left + brentq(excess, 0.0, span, xtol=1e-13)

    def saturation_ratio(self, st):
        """p_H2O / p_sat(T) of the gas (diagnostic; meaningful while liquid remains)."""
        ps = water_p_sat(st["T"])
        if math.isinf(ps):
            return 0.0
        x = float(st["masses"][self.j] / self.ph.MW[self.j]) / st["n"]
        return math.inf if ps == 0.0 else x * st["p"] / ps

    # End gas (knock) and burned-zone temperature (NO).
    def endgas_anchor(self, st):
        """Freeze the unburned composition at a node just before x_b reaches the anchor."""
        eg = self.ph.endgas
        Y = self.dry + st["e"] * self.water
        eg.TPY = st["T"], st["p"], Y / Y.sum()
        return dict(s=float(eg.entropy_mass), gamma=float(eg.cp_mass / eg.cv_mass),
                    p=st["p"], V=st["V"], T=st["T"], e=st["e"])

    def endgas_T(self, anchor, p):
        """Frozen-composition, variable-cp isentrope from the anchor state."""
        eg = self.ph.endgas
        eg.SP = anchor["s"], p
        return float(eg.T)

    def reanchor(self, anchor, p, e_bulk, mass):
        """End-gas droplets evaporate toward the bulk fraction, within saturation.

        The end gas carries the same droplet loading per kg as the bulk. Its
        own droplets evaporate (cooling it by L dE/(m cv_u)) only as far as its
        own saturation allows, i.e. wet compression. Water the bulk evaporates
        beyond that is enabled by combustion heat and is attributed to the
        flame/burned zone; liquid still in the end gas is debited in flame_T.
        A new frozen isentrope starts from the updated end-gas state.
        """
        e0 = anchor["e"]
        if e_bulk <= e0:
            return anchor
        eg = self.ph.endgas
        T_iso = self.endgas_T(anchor, p)
        cooling = self.L_cyl / (mass * float(eg.cv_mass))  # K per unit evaporated fraction
        inv = self.ph.inv_MW

        def excess(e):
            T = T_iso - cooling * (e - e0)
            if T < WATER_T_TRIPLE:
                return 1e30
            moles = (self.dry + e * self.water) * inv
            return float(moles[self.j] / moles.sum()) * p - water_p_sat(T)

        if excess(e_bulk) <= 0.0:
            e_new = e_bulk
        elif excess(e0) >= 0.0:
            e_new = e0
        else:
            e_new = brentq(excess, e0, e_bulk, xtol=1e-13)
        Y = self.dry + e_new * self.water
        eg.TPY = T_iso - cooling * (e_new - e0), p, Y / Y.sum()
        return dict(anchor, s=float(eg.entropy_mass), e=float(e_new))

    def flame_T(self, anchor, T_u, p):
        """Model-consistent HP flame temperature of the current end gas [K].

        Products (all water as vapour) carry the end-gas sensible enthalpy plus
        eta_c LHV (the same prescribed release as the cycle, not the vapour-fuel
        chemistry) minus the latent heat of droplets still liquid in the end gas,
        with equilibrium dissociation at constant p. Basis: per kg of fuel.
        """
        ph = self.ph
        e = anchor["e"]
        Yu = self.dry + e * self.water
        Yc = self.burned_ref + self.water
        mass = float(Yc.sum())
        H = (float(Yc @ ph.h_ref) + float(Yu @ (ph.species_h(T_u) - ph.h_ref))
             + self.par.combustion_efficiency * ph.lhv
             - (1.0 - e) * self.m_water_basis * self.h_latent)
        fl = ph.flame
        fl.HPY = H / mass, p, Yc / mass
        fl.equilibrate("HP")
        return float(fl.T)


class IdealCharge:
    """Constant-gamma ideal gas for the SPEC section 10 Otto check (same integrator)."""

    ideal = True

    def __init__(self, cr, gamma, par=DEFAULTS):
        self.cr, self.gamma, self.par = float(cr), float(gamma), par
        self.w, self.e_intake, self.water_mass, self.L_cyl = 0.0, 0.0, 0.0, 0.0
        self.R = par.otto_gas_constant_J_kg_K
        self.cv = self.R / (gamma - 1.0)
        self.T_ivc = par.otto_T_ivc_K
        self.V_ivc = volume(par.ivc_rad, cr, par)
        self.mass = par.p_ivc_Pa * self.V_ivc / (self.R * self.T_ivc)
        self.Q_fuel = self.Q_avail = self.mass * par.otto_heat_per_mass_J_kg
        self.U_ivc = 0.0  # U = m cv (T - T_ivc)

    def state(self, U, V, xb, e, guess):
        T = self.T_ivc + U / (self.mass * self.cv)
        return dict(T=T, p=self.mass * self.R * T / V, U=U, V=V, n=None,
                    masses=None, mass=self.mass, xb=xb, e=e)

    def evaporate(self, e_left, theta, left, V):
        return e_left


# ---------------------------------------------------------- heat and NO
def wall_heat_rate(st, charge, anchor):
    """Woschni (1967), SAE 670931, doi:10.4271/670931; Heywood (1988) eq. 12.19.

    h = 3.26 B^-0.2 p[kPa]^0.8 T^-0.55 w^0.8 [W/(m2 K)], with
    w = C1 S_p + C2 V_d T_r / (p_r V_r) (p - p_mot); C1 = 2.28 for compression
    and expansion, C2 = 3.24e-3 m/(s K) once combustion starts. Reference r =
    IVC; p_mot is the polytrope (anchor gamma) from the start-of-burn anchor.
    """
    if charge.ideal:
        return 0.0
    par = charge.par
    speed = par.woschni_C1 * 2.0 * par.stroke_m * par.rpm / 60.0
    if anchor is not None:
        p_mot = anchor["p"] * (anchor["V"] / st["V"]) ** anchor["gamma"]
        speed += (par.woschni_C2 * displacement(par) * charge.T_ivc
                  / (par.p_ivc_Pa * charge.V_ivc) * max(0.0, st["p"] - p_mot))
    h = (par.woschni_C * par.bore_m ** -0.2 * (st["p"] / 1000.0) ** 0.8
         * st["T"] ** -0.55 * speed ** 0.8)
    return h * wall_area(st["V"], par) * (st["T"] - par.wall_T_K)


# Extended Zeldovich: N2+O<=>NO+N (1), N+O2<=>NO+O (2), N+OH<=>NO+H (3).
# k = A T^b exp(-Ta/T), A in m3/(mol s). Hanson & Salimian (1984), in
# Gardiner (ed.), Combustion Chemistry, Springer, pp. 361-421, as tabulated
# by Turns, An Introduction to Combustion, ch. 5 (m3/(kmol s) there; /1000).
NO_RATES = {"k1f": (1.8e8, 0.0, 38370.0), "k1r": (3.8e7, 0.0, 425.0),
            "k2f": (1.8e4, 1.0, 4680.0), "k2r": (3.81e3, 1.0, 20820.0),
            "k3f": (7.1e7, 0.0, 450.0), "k3r": (1.7e8, 0.0, 24560.0)}


def _k(name, T):
    A, b, Ta = NO_RATES[name]
    return A * T ** b * math.exp(-Ta / T)


def no_step(n_NO, dt, st, T_u, anchor, charge):
    """Advance NO [mol] in the burned zone by dt (implicit, quasi-steady N atom).

    Two-zone estimate: T = (1 - x_b) T_u + x_b T_b (equal cp), bounded above by
    the model-consistent flame temperature of the current end gas and below by
    the bulk temperature. O, O2, N2, OH, H from TP equilibrium at (T_b, p).
    NO is a trace diagnostic with no feedback on the energy solution.
    """
    xb, T, p = st["xb"], st["T"], st["p"]
    if xb < 0.999:
        T_ad = charge.flame_T(anchor, T_u, p)
        T_b = max(T, min(T_ad, T_u + (T - T_u) / xb))
    else:  # burn-out: the burned zone is the whole charge
        T_ad = None
        T_b = T
    ph = charge.ph
    Y = charge.burned_ref + st["e"] * charge.water
    fl = ph.flame
    fl.TPY = T_b, p, Y / Y.sum()
    fl.equilibrate("TP")
    conc = np.array(fl.concentrations) * 1000.0  # mol/m3
    O, N2, O2, OH, H = (float(conc[ph.i[k]]) for k in ("O", "N2", "O2", "OH", "H"))
    k1f, k1r, k2f, k2r, k3f, k3r = (_k(k, T_b) for k in ("k1f", "k1r", "k2f", "k2r", "k3f", "k3r"))
    V_b = xb * st["mass"] / float(fl.density)

    def production(amount):
        NO = amount / V_b
        N = (k1f * O * N2 + k2r * NO * O + k3r * NO * H) / max(
            k1r * NO + k2f * O2 + k3f * OH, np.finfo(float).tiny)
        return 2.0 * (k1f * O * N2 - k1r * NO * N) * V_b

    # Reverse reactions only lower NO, so old NO + forward production brackets
    # the root; widen by 1e-9 so round-off cannot hide the sign change.
    upper = (n_NO + dt * 2.0 * k1f * O * N2 * V_b) * (1.0 + 1e-9)
    if upper <= 0.0:
        return 0.0, T_b, T_ad

    def residual(x):
        return x - n_NO - dt * production(x)

    if residual(upper) <= 0.0:  # reverse rates negligible at this precision
        return float(upper), T_b, T_ad
    value = brentq(residual, 0.0, upper, xtol=1e-30, rtol=1e-12)
    return float(value), T_b, T_ad


# ------------------------------------------------------------ integrator
def integrate_cycle(charge, ca50, duration, ignition=None, *, evo_rad=None,
                    step_rad=None, wall=True, track_no=True, keep_trace=False):
    """Crank-angle RK2 (explicit midpoint) on sensible U from IVC to EVO.

    Wiebe release and evaporation enter as exact increments between nodes.
    The nodes include x_b = 0.9 and the end of scheduled evaporation, so the
    knock integral stops exactly at x_b = 0.9. Independent quadratures
    (trapezoidal p dV and wall heat over node states) and the Cantera
    re-evaluated EVO energy give the energy-closure check.
    """
    par = charge.par
    evo = par.evo_rad if evo_rad is None else evo_rad
    step = par.step_rad if step_rad is None else step_rad
    omega = par.rpm * 2.0 * math.pi / 60.0
    theta90 = burn_angle(par.knock_burn_fraction, ca50, duration, par)
    # Start-of-burn anchor on a grid node at x_b = endgas_anchor_xb (verification item 1, 2026-10-24):
    # a step-dependent anchor position made the Woschni combustion term O(h).
    theta_a = burn_angle(par.endgas_anchor_xb, ca50, duration, par)
    nodes = list(np.linspace(par.ivc_rad, evo, max(2, math.ceil((evo - par.ivc_rad) / step)) + 1))
    nodes += [a for a in (par.evap_end_rad, theta90, theta_a) if par.ivc_rad < a < evo]
    grid = np.unique(np.array(nodes, dtype=float))
    Qa, Lc = charge.Q_avail, charge.L_cyl
    xb = x_ivc = wiebe(grid[0], ca50, duration, par)
    e = charge.e_intake
    st = charge.state(charge.U_ivc, volume(grid[0], charge.cr, par), xb, e,
                      (charge.T_ivc, par.p_ivc_Pa))
    U = charge.U_ivc
    anchor = None
    W = Q_wall = Q_evap = W_trap = Q_wall_trap = 0.0
    LW = LW_extrapolated = 0.0
    LW90 = None
    n_NO = 0.0
    peak_Tb = peak_Tad = None
    q_left = wall_heat_rate(st, charge, anchor) if wall else 0.0
    peak = dict(p=st["p"], theta=grid[0], T=st["T"])
    track_sat = not charge.ideal and charge.water_mass > 0.0
    max_sat = charge.saturation_ratio(st) if track_sat else None
    evap_done = grid[0] if (charge.water_mass <= 0.0 or e >= 1.0) else None
    trace = {k: [] for k in ("theta_deg", "V_m3", "p_Pa", "T_K", "T_unburned_K", "xb", "evaporated")}

    def record(theta, s, T_u):
        if keep_trace:
            for key, value in (("theta_deg", theta / RAD), ("V_m3", s["V"]), ("p_Pa", s["p"]),
                               ("T_K", s["T"]), ("T_unburned_K", T_u), ("xb", s["xb"]),
                               ("evaporated", s["e"])):
                trace[key].append(float(value))

    record(grid[0], st, st["T"])
    for left, right in zip(grid[:-1], grid[1:]):
        mid = 0.5 * (left + right)
        dt = (right - left) / omega
        Vm, Vr = volume(mid, charge.cr, par), volume(right, charge.cr, par)
        xm, xr = wiebe(mid, ca50, duration, par), wiebe(right, ca50, duration, par)
        em = charge.evaporate(e, mid, st, Vm)
        if em > e:  # saturation cap on the no-evaporation predictor state at mid, not the lagged left state
            s0 = charge.state(U - st["p"] * (Vm - st["V"]) + Qa * (xm - xb) - 0.5 * q_left * dt, Vm, xm, e,
                              (st["T"], st["p"]))
            em = charge.evaporate(e, mid, s0, Vm)
        er = max(em, charge.evaporate(e, right, st, Vr))
        U_mid = U - st["p"] * (Vm - st["V"]) + Qa * (xm - xb) - Lc * (em - e) - 0.5 * q_left * dt
        sm = charge.state(U_mid, Vm, xm, em, (st["T"], st["p"]))
        if anchor is None and not charge.ideal and left >= theta_a - 1e-12:
            anchor = charge.endgas_anchor(st)
        q_mid = wall_heat_rate(sm, charge, anchor) if wall else 0.0
        work = sm["p"] * (Vr - st["V"])
        d_evap = Lc * (er - e)
        U += -work + Qa * (xr - xb) - d_evap - q_mid * dt
        if er > e:  # corrector: saturation cap on the no-evaporation right state
            s0 = charge.state(U + d_evap, Vr, xr, e, (sm["T"], sm["p"]))
            er2 = max(em, charge.evaporate(e, right, s0, Vr))
            U -= Lc * (er2 - er)
            er, d_evap = er2, Lc * (er2 - e)
        W += work
        Q_wall += q_mid * dt
        Q_evap += d_evap
        # End gas exists until burn-out; afterwards the burned zone is the whole charge.
        endgas = anchor is not None and xm < 0.999
        T_u = charge.endgas_T(anchor, sm["p"]) if endgas else sm["T"]
        if ignition is not None and mid < theta90:
            increment = ignition_rate(T_u, sm["p"], charge.w, ignition) * dt
            LW = min(par.knock_integral_cap, LW + increment)
            if outside_fit(ignition, T_u, sm["p"], charge.w):
                LW_extrapolated = min(par.knock_integral_cap, LW_extrapolated + increment)
        if track_no and anchor is not None and xm > par.no_min_xb:
            n_NO, T_b, T_ad = no_step(n_NO, dt, sm, T_u, anchor, charge)
            peak_Tb = T_b if peak_Tb is None else max(peak_Tb, T_b)
            if T_ad is not None:
                peak_Tad = T_ad if peak_Tad is None else max(peak_Tad, T_ad)
        sr = charge.state(U, Vr, xr, er, (sm["T"], sm["p"]))
        if anchor is not None and xr < 0.999 and er > anchor["e"]:
            anchor = charge.reanchor(anchor, sr["p"], er, sr["mass"])
        q_right = wall_heat_rate(sr, charge, anchor) if wall else 0.0
        W_trap += 0.5 * (st["p"] + sr["p"]) * (Vr - st["V"])
        Q_wall_trap += 0.5 * (q_left + q_right) * dt
        if abs(right - theta90) < 1e-12:
            LW90 = LW
        for s, theta in ((sm, mid), (sr, right)):
            if s["p"] > peak["p"]:
                peak.update(p=s["p"], theta=theta)
            peak["T"] = max(peak["T"], s["T"])
        if track_sat and er < 1.0:
            max_sat = max(max_sat, charge.saturation_ratio(sr))
        if evap_done is None and er >= 1.0 - 1e-12:
            evap_done = right
        st, xb, e, q_left = sr, xr, er, q_right
        record(right, st, charge.endgas_T(anchor, st["p"])
               if anchor is not None and xb < 0.999 else st["T"])
    if LW90 is None:
        LW90 = LW  # x_b = 0.9 not reached before EVO: integral up to EVO
    released = Qa * (xb - x_ivc)
    dU = st["U"] - charge.U_ivc
    closure = released - (W_trap + Q_wall_trap + Q_evap + dU)
    identity = released - (W + Q_wall + Q_evap + dU)
    result = dict(
        indicated_work_J=W, wall_heat_J=Q_wall, evaporation_cylinder_J=Q_evap,
        released_energy_J=released, unreleased_wiebe_tail_J=Qa * (1.0 - xb + x_ivc),
        charge_energy_change_J=dU, indicated_work_trapezoid_J=W_trap,
        wall_heat_trapezoid_J=Q_wall_trap, energy_closure_error_J=closure,
        energy_closure_error_fraction=closure / charge.Q_fuel,
        integrator_identity_error_fraction=identity / charge.Q_fuel,
        gross_indicated_efficiency=W / charge.Q_fuel, IMEP_Pa=W / displacement(par),
        peak_pressure_Pa=peak["p"], peak_pressure_angle_deg=peak["theta"] / RAD,
        peak_temperature_K=peak["T"], peak_burned_temperature_K=peak_Tb,
        peak_flame_temperature_K=peak_Tad, ca50_used_deg=ca50 / RAD,
        burn_10_90_deg=duration / RAD, theta_xb90_deg=theta90 / RAD,
        knock_integral_at_xb90=LW90, knock=bool(LW90 >= 1.0),
        knock_integral_extrapolated_fraction=(LW_extrapolated / LW) if LW > 0 else 0.0,
        NO_mol=n_NO, NO_mol_per_J_fuel=n_NO / charge.Q_fuel,
        EVO_T_K=st["T"], EVO_p_Pa=st["p"], xb_EVO=xb, evaporated_fraction_EVO=e,
        evaporation_complete_deg=None if evap_done is None else evap_done / RAD,
        liquid_water_at_EVO_kg=charge.water_mass * (1.0 - e),
        max_vapour_saturation_ratio=max_sat)
    result["_state"] = st
    result["_trace"] = trace if keep_trace else None
    return result


def retard_search(evaluate, par=DEFAULTS):
    """SPEC: CA50 = default, then +2 CAD steps up to 30 CAD aTDC while knocking."""
    ca50 = par.ca50_rad
    first = None
    attempts = 0
    while True:
        result = evaluate(ca50)
        attempts += 1
        first = first or dict(efficiency=result["gross_indicated_efficiency"],
                              knock_integral=result["knock_integral_at_xb90"])
        if not result["knock"] or ca50 >= par.retard_limit_rad - 1e-12:
            break
        ca50 = min(par.retard_limit_rad, ca50 + par.retard_step_rad)
    result.update(knock_limited=bool(result["knock"]), retard_attempts=attempts,
                  efficiency_at_default_ca50=first["efficiency"],
                  knock_integral_at_default_ca50=first["knock_integral"])
    return result


# ------------------------------------------------------------ sweep points
POINT_FIELDS = (
    "S_L_m_s S_L_ref_m_s burn_10_90_deg ca50_used_deg theta_xb90_deg knock knock_limited "
    "retard_attempts knock_integral_at_xb90 knock_integral_at_default_ca50 "
    "knock_integral_extrapolated_fraction gross_indicated_efficiency efficiency_at_default_ca50 "
    "IMEP_Pa peak_pressure_Pa peak_pressure_angle_deg peak_temperature_K "
    "peak_burned_temperature_K peak_flame_temperature_K low_flame_temperature EVO_T_K EVO_p_Pa xb_EVO NO_mol "
    "NO_mol_per_J_fuel relative_NO T_IVC_K f_evap_intake_effective intake_saturation_limited "
    "evaporated_fraction_EVO evaporation_complete_deg liquid_water_at_EVO_kg "
    "max_vapour_saturation_ratio fuel_vapour_saturation_ratio_IVC fuel_mass_kg water_mass_kg "
    "air_mass_kg residual_mass_kg gas_mass_IVC_kg fuel_energy_J combustion_loss_J "
    "released_energy_J unreleased_wiebe_tail_J indicated_work_J indicated_work_trapezoid_J "
    "wall_heat_J wall_heat_trapezoid_J evaporation_intake_J evaporation_cylinder_J "
    "charge_energy_change_J energy_closure_error_J energy_closure_error_fraction "
    "integrator_identity_error_fraction intake_closure_error_J").split()


def point_key(row):
    return f"{row['fuel']}/CR={row['CR']:g}/w={row['w']:g}/T_intake={row['T_intake_K']:g}"


def run_point(fuel, cr, w, T_intake, ignition, flame, par=DEFAULTS, mode="full",
              fits_source=None, keep_trace=False, flame_speed_factor=1.0):
    """One sweep point; unavailable/failed points are kept with a reason."""
    row = dict(fuel=fuel, CR=cr, w=w, WFR=w / (1.0 - w), T_intake_K=T_intake, phi=par.phi,
               status="computed", reason="", mechanism=None, mechanism_fallback=False,
               fits_source=fits_source, **{key: None for key in POINT_FIELDS})
    try:
        selection = fuels.select_mechanism(fuel)
        row.update(mechanism=selection.name, mechanism_fallback=selection.mechanism_fallback)
        sl, ref = check_fits(ignition, flame, w, mode)
        if w >= SENSITIVITY["applied_for_w_ge"]:
            sl *= flame_speed_factor
        duration = burn_duration(sl, ref, par)
        charge = Charge(fuel, cr, w, T_intake, par)
        result = retard_search(lambda ca50: integrate_cycle(
            charge, ca50, duration, ignition, keep_trace=keep_trace), par)
        state, trace = result.pop("_state"), result.pop("_trace")
        row.update({k: v for k, v in result.items() if k in row})
        row.update(S_L_m_s=sl, S_L_ref_m_s=ref, T_IVC_K=charge.T_ivc,
                   f_evap_intake_effective=charge.e_intake,
                   intake_saturation_limited=charge.intake_saturation_limited,
                   fuel_vapour_saturation_ratio_IVC=charge.fuel_saturation_ratio_ivc,
                   fuel_mass_kg=charge.fuel_mass, water_mass_kg=charge.water_mass,
                   air_mass_kg=charge.air_mass, residual_mass_kg=charge.residual_mass,
                   gas_mass_IVC_kg=charge.gas_mass_ivc, fuel_energy_J=charge.Q_fuel,
                   combustion_loss_J=charge.Q_fuel - charge.Q_avail,
                   evaporation_intake_J=charge.Q_evap_intake,
                   intake_closure_error_J=charge.intake_closure_J,
                   low_flame_temperature=bool(row["peak_flame_temperature_K"] is not None and
                                              row["peak_flame_temperature_K"] < par.limit_flame_temperature_K))
        names = charge.ph.gas.species_names
        Y = state["masses"] / state["mass"]
        evo = dict(key=point_key(row), fuel=fuel, CR=cr, w=w, T_intake_K=T_intake,
                   crank_angle_deg=par.evo_rad / RAD, volume_m3=volume(par.evo_rad, cr, par),
                   T_K=state["T"], p_Pa=state["p"], gas_mass_kg=state["mass"],
                   liquid_water_kg=row["liquid_water_at_EVO_kg"],
                   composition_basis="mass_fraction", mechanism=selection.name,
                   mechanism_fallback=selection.mechanism_fallback,
                   composition={n: float(y) for n, y in zip(names, Y) if y > 1e-14},
                   sensible_energy_reference=f"u_eq(T,p) - u_complete({T_REF} K); unburned u(T) - u({T_REF} K)",
                   unburned_mass_fraction=1.0 - state["xb"], fuel_mass_kg=charge.fuel_mass,
                   water_mass_kg=charge.water_mass, fuel_energy_J=charge.Q_fuel,
                   indicated_work_J=row["indicated_work_J"], ca50_used_deg=row["ca50_used_deg"])
        return dict(point=row, evo=evo, trace=trace)
    except (PointUnavailable, fuels.MechanismUnavailable) as exc:
        row.update(status="unavailable", reason=str(exc))
        if isinstance(exc, fuels.MechanismUnavailable):
            row["mechanism_fallback"] = True
    except (ct.CanteraError, RuntimeError, ValueError, ZeroDivisionError, OverflowError) as exc:
        row.update(status="failed", reason=f"{type(exc).__name__}: {exc}")
    return dict(point=row, evo=None, trace=None)


def _task(task):
    return run_point(*task)


def sweep(mode):
    if mode == "quick":
        return QUICK_FUELS, QUICK_CR, QUICK_W, QUICK_T_INTAKE
    return FUELS, FULL_CR, FULL_W, FULL_T_INTAKE


def build_tasks(mode, ignition, flame, provenance, par=DEFAULTS):
    names, crs, waters, temperatures = sweep(mode)
    tasks = []
    for f in names:
        for cr in crs:
            for w in waters:
                for T in temperatures:
                    trace = cr == EXAMPLE_CR and T == temperatures[0] and w in (0.0, 0.6)
                    tasks.append((f, cr, w, T, ignition.get(f), flame.get(f), par, mode,
                                  provenance["per_fuel"].get(f), trace))
    # Wet/high-CR points are slower (knock retard, saturation); schedule first.
    return sorted(tasks, key=lambda t: -(t[1] + 10 * t[2]))


def add_relative_no(rows):
    """NO per J of fuel energy relative to w = 0 at the same fuel, CR, T_intake."""
    dry = {(r["fuel"], r["CR"], r["T_intake_K"]): r for r in rows
           if r["status"] == "computed" and r["w"] == 0}
    for r in rows:
        base = dry.get((r["fuel"], r["CR"], r["T_intake_K"]))
        if (r["status"] == "computed" and base and base["NO_mol_per_J_fuel"]
                and base["NO_mol_per_J_fuel"] > 0):
            r["relative_NO"] = r["NO_mol_per_J_fuel"] / base["NO_mol_per_J_fuel"]


def ideal_otto(cr, gamma=None, par=DEFAULTS):
    """SPEC section 10: engine integrator, adiabatic, ~instant burn at TDC, constant gamma."""
    gamma = par.otto_gamma if gamma is None else gamma
    charge = IdealCharge(cr, gamma, par)
    result = integrate_cycle(charge, 0.0, par.otto_burn_duration_rad, None, evo_rad=math.pi,
                             step_rad=par.otto_step_rad, wall=False, track_no=False)
    efficiency = result["indicated_work_J"] / result["released_energy_J"]
    analytic = 1.0 - cr ** (1.0 - gamma)
    return dict(CR=cr, gamma=gamma, efficiency=efficiency, analytic_efficiency=analytic,
                error_abs=efficiency - analytic,
                passed=bool(abs(efficiency - analytic) <= par.otto_tolerance_abs),
                energy_closure_error_fraction=result["energy_closure_error_fraction"])


# ------------------------------------------------------ water-majority map
def eligible(r, par=DEFAULTS):
    """SPEC selection: knock-free at CA50 <= 15 CAD, S_L >= 0.08 m/s, p_max <= 120 bar."""
    return (r["status"] == "computed" and not r["knock"] and not r["knock_limited"]
            and r["ca50_used_deg"] <= par.selection_ca50_limit_rad / RAD + 1e-9
            and r["S_L_m_s"] >= par.flame_speed_min_m_s
            and r["peak_pressure_Pa"] <= par.peak_pressure_limit_Pa
            and abs(r["energy_closure_error_fraction"]) <= par.closure_tolerance)


def cr_limiting_constraint(fuel, rows, par=DEFAULTS):
    """For each fuel: which constraint (knock or P_max) limits the CR sweep.

    Walks the eligible computed rows in CR order.  A fuel is knock-limited if
    the best eligible point still knocks at the default CA50 (retard_attempts > 1)
    or is knock_limited at the top CR.  It is P_max-limited if the peak pressure
    hits the 120 bar ceiling before knock does.  Returns a dict per fuel with
    the limiting constraint, the CR at which it binds, and the best CR found.
    """
    computed = [r for r in rows if r["fuel"] == fuel and r["status"] == "computed"]
    if not computed:
        return dict(fuel=fuel, constraint="none", binding_CR=None, best_eligible_CR=None,
                    reason="no computed points")
    by_cr = {}
    for r in computed:
        by_cr.setdefault(r["CR"], []).append(r)
    crs = sorted(by_cr)
    best_eligible = max((r for r in computed if eligible(r, par)),
                        key=lambda r: r["gross_indicated_efficiency"], default=None)
    best_cr = best_eligible["CR"] if best_eligible else None
    # Walk upward: knock binds first, or pressure ceiling binds first.
    knock_binds_at = None
    pmax_binds_at = None
    for cr in crs:
        group = by_cr[cr]
        if any(r["knock_limited"] or r["retard_attempts"] > 1 for r in group):
            knock_binds_at = cr
            break
        if any(r["peak_pressure_Pa"] >= par.peak_pressure_limit_Pa * (1 - 1e-6) for r in group):
            pmax_binds_at = cr
            break
    if knock_binds_at is not None and (pmax_binds_at is None or knock_binds_at <= pmax_binds_at):
        constraint = "knock"
        binding = knock_binds_at
    elif pmax_binds_at is not None:
        constraint = "P_max"
        binding = pmax_binds_at
    else:
        constraint = "neither"
        binding = None
    return dict(fuel=fuel, constraint=constraint, binding_CR=binding,
                best_eligible_CR=best_cr, sweep_bound=FULL_CR[-1],
                at_sweep_bound=bool(best_cr is not None and best_cr >= FULL_CR[-1] - 1e-9))


def point_summary(r, par=DEFAULTS):
    if r is None:
        return None
    keys = ("fuel", "CR", "w", "WFR", "T_intake_K", "phi", "ca50_used_deg", "burn_10_90_deg",
            "gross_indicated_efficiency", "IMEP_Pa", "peak_pressure_Pa", "peak_temperature_K",
            "peak_burned_temperature_K", "peak_flame_temperature_K", "low_flame_temperature",
            "EVO_T_K", "EVO_p_Pa", "relative_NO",
            "NO_mol_per_J_fuel", "knock_integral_at_xb90", "S_L_m_s", "T_IVC_K",
            "f_evap_intake_effective", "liquid_water_at_EVO_kg", "fuel_mass_kg",
            "water_mass_kg", "air_mass_kg", "residual_mass_kg", "fuel_energy_J",
            "indicated_work_J", "energy_closure_error_fraction")
    summary = {k: r[k] for k in keys}
    summary.update(key=point_key(r), evo_state_key=point_key(r), rpm=par.rpm,
                   knock_margin_integral=r["knock_integral_at_xb90"])
    return summary


def select_designs(rows, provenance, validation_passed=True, par=DEFAULTS):
    """Best dry / overall / water-majority (w > 0.5) eligible point per fuel."""
    synthetic = bool(provenance["synthetic"])
    maps, per_fuel = [], {}

    def best(subset):
        return max(subset, key=lambda r: r["gross_indicated_efficiency"], default=None)

    for fuel in dict.fromkeys(r["fuel"] for r in rows):
        candidates = [r for r in rows if r["fuel"] == fuel and eligible(r, par)]
        dry = best([r for r in candidates if r["w"] == 0])
        chosen = {"best_dry": dry, "best_overall": best(candidates),
                  "best_water_majority": best([r for r in candidates if r["w"] > 0.5])}
        for category, sel in chosen.items():
            row = dict(fuel=fuel, category=category,
                       status="selected" if sel else "no_feasible_point",
                       key=point_key(sel) if sel else None, synthetic_fits=synthetic)
            for k in ("CR", "w", "T_intake_K", "gross_indicated_efficiency", "ca50_used_deg",
                      "peak_pressure_Pa", "relative_NO", "knock_integral_at_xb90", "S_L_m_s",
                      "peak_flame_temperature_K", "low_flame_temperature"):
                row[k] = sel[k] if sel else None
            row.update(best_dry_key=point_key(dry) if dry else None,
                       best_dry_CR=dry["CR"] if dry else None,
                       best_dry_efficiency=dry["gross_indicated_efficiency"] if dry else None,
                       efficiency_change_vs_best_dry=None, CR_change_vs_best_dry=None,
                       NO_ratio_vs_best_dry=None,
                       knock_margin_change_vs_best_dry=None)
            if sel and dry:
                row.update(efficiency_change_vs_best_dry=sel["gross_indicated_efficiency"]
                           - dry["gross_indicated_efficiency"],
                           CR_change_vs_best_dry=sel["CR"] - dry["CR"],
                           knock_margin_change_vs_best_dry=sel["knock_integral_at_xb90"]
                           - dry["knock_integral_at_xb90"])
                if dry["NO_mol_per_J_fuel"]:
                    row["NO_ratio_vs_best_dry"] = sel["NO_mol_per_J_fuel"] / dry["NO_mol_per_J_fuel"]
            maps.append(row)
        wet = chosen["best_water_majority"]
        per_fuel[fuel] = dict(
            status="selected" if wet else "no_feasible_water_majority_point",
            water_majority=point_summary(wet, par), best_overall=point_summary(chosen["best_overall"], par),
            best_dry=point_summary(dry, par),
            comparison_vs_best_dry=next(m for m in maps if m["fuel"] == fuel
                                        and m["category"] == "best_water_majority"))
    feasible = [v["water_majority"] for f, v in per_fuel.items() if v["water_majority"] and f in DESIGN_FUELS]
    recommended = max(feasible, key=lambda r: r["gross_indicated_efficiency"], default=None)
    use = not synthetic and validation_passed
    design = dict(
        module=MODULE, version=VERSION, synthetic_fits=synthetic, validation_passed=validation_passed,
        use_for_design=use,
        warning=None if use else "NOT FOR DESIGN: " + "; ".join(
            reason for reason, active in (("synthetic fallback fits", synthetic),
                                          ("Module 03 validation failed", not validation_passed)) if active),
        engine=dict(bore_m=par.bore_m, stroke_m=par.stroke_m, rod_m=par.rod_m, rpm=par.rpm,
                    ivc_deg=par.ivc_rad / RAD, evo_deg=par.evo_rad / RAD,
                    residual_fraction=par.residual_fraction, p_ivc_Pa=par.p_ivc_Pa, phi=par.phi,
                    displacement_m3=displacement(par)),
        selection_constraints=dict(
            knock_free_at_ca50_max_deg=par.selection_ca50_limit_rad / RAD,
            flame_speed_min_m_s=par.flame_speed_min_m_s,
            peak_pressure_max_Pa=par.peak_pressure_limit_Pa,
            energy_closure_max_fraction=par.closure_tolerance, water_majority="w > 0.5"),
        per_fuel=per_fuel, recommended=recommended,
        recommended_evo_state_key=recommended["key"] if recommended else None,
        recommendation_status=("selected" if recommended else "no_feasible_water_majority_point"),
        recommendation_basis="highest gross indicated efficiency among feasible w > 0.5 points of the design fuels "
                             + "/".join(DESIGN_FUELS) + " (CH4 is reference-only)",
        cr_limiting_constraints=[cr_limiting_constraint(fuel, rows, par)
                                 for fuel in dict.fromkeys(r["fuel"] for r in rows)],
        at_sweep_bound=bool(recommended and recommended["CR"] >= FULL_CR[-1] - 1e-9),
        sensitivity=SENSITIVITY, evo_states_file="evo_states.json")
    return maps, design


def sensitivity_summary(rows, ignition, flame, provenance, par, mode):
    """Re-evaluate water-majority candidates with S_L reduced by 30 percent."""
    candidates = [r for r in rows if r["status"] == "computed" and r["w"] >= SENSITIVITY["applied_for_w_ge"]]
    baseline = max(candidates, key=lambda r: r["gross_indicated_efficiency"], default=None)
    changed = []
    for r in candidates:
        result = run_point(r["fuel"], r["CR"], r["w"], r["T_intake_K"],
                           ignition[r["fuel"]], flame[r["fuel"]], par, mode,
                           provenance["per_fuel"].get(r["fuel"]), False,
                           SENSITIVITY["flame_speed_factor"])["point"]
        if result["status"] == "computed":
            changed.append(result)
    sensitive = max(changed, key=lambda r: r["gross_indicated_efficiency"], default=None)
    return dict(case=SENSITIVITY, baseline_best_water_majority=point_summary(baseline, par),
                sensitivity_best_water_majority=point_summary(sensitive, par),
                efficiency_change=(None if not baseline or not sensitive else
                                   sensitive["gross_indicated_efficiency"] - baseline["gross_indicated_efficiency"]))


# --------------------------------------------------------------- validation
def validate(rows, otto, par=DEFAULTS):
    computed = [r for r in rows if r["status"] == "computed"]
    max_error = max((abs(r["energy_closure_error_fraction"]) for r in computed), default=None)
    closure_ok = max_error is not None and max_error <= par.closure_tolerance
    trends = []
    for fuel, T in sorted({(r["fuel"], r["T_intake_K"]) for r in computed}):
        dry = sorted((r for r in computed if r["fuel"] == fuel and r["T_intake_K"] == T
                      and r["w"] == 0), key=lambda r: r["CR"])
        # Trend at the default CA50 (before knock retard): the Otto-like CR effect.
        effs = [r["efficiency_at_default_ca50"] for r in dry]
        increasing = len(dry) >= 2 and all(b > a for a, b in zip(effs[:-1], effs[1:]))
        below = bool(dry) and all(r["efficiency_at_default_ca50"] < 1.0 - r["CR"] ** (1.0 - par.otto_gamma)
                                  for r in dry)
        trends.append(dict(fuel=fuel, T_intake_K=T, monotonic_increase=increasing,
                           below_air_standard_otto=below, passed=bool(increasing and below),
                           points=[dict(CR=r["CR"], efficiency_at_default_ca50=r["efficiency_at_default_ca50"],
                                        efficiency_used=r["gross_indicated_efficiency"],
                                        ca50_used_deg=r["ca50_used_deg"]) for r in dry]))
    failed = [dict(key=point_key(r), reason=r["reason"]) for r in rows if r["status"] == "failed"]
    water_source = all(r["released_energy_J"] <= par.combustion_efficiency * r["fuel_energy_J"] * (1 + 1e-12)
                       for r in computed)
    plausible = [dict(key=point_key(r), efficiency=r["efficiency_at_default_ca50"])
                 for r in computed if r["w"] == 0 and not (
                     par.plausible_efficiency_min <= r["efficiency_at_default_ca50"] <= par.plausible_efficiency_max)]
    passed = (bool(computed) and closure_ok and not failed and water_source
              and all(o["passed"] for o in otto) and all(t["passed"] for t in trends))
    return dict(
        passed=bool(passed), energy_closure_passed=bool(closure_ok),
        max_abs_energy_closure_error_fraction=max_error,
        max_abs_integrator_identity_error_fraction=max(
            (abs(r["integrator_identity_error_fraction"]) for r in computed), default=None),
        energy_closure_tolerance_fraction=par.closure_tolerance,
        energy_from_fuel_only=bool(water_source),
        ideal_otto=otto, ideal_otto_passed=all(o["passed"] for o in otto),
        max_abs_ideal_otto_error=max(abs(o["error_abs"]) for o in otto),
        dry_otto_trend=trends, failed_points=failed,
        dry_efficiency_outside_plausible_range=plausible,
        plausible_dry_efficiency_range=[par.plausible_efficiency_min, par.plausible_efficiency_max],
        unavailable_points=[dict(key=point_key(r), reason=r["reason"])
                            for r in rows if r["status"] == "unavailable"],
        cantera_ic_engine_example="documented difference only; not numerically reproduced (see assumptions)",
        scope="In-run checks; tests/test_engine_cycle.py on the server is the unit validation")


# -------------------------------------------------------------------- plots
def _status(r, par=DEFAULTS):
    if r["status"] != "computed":
        return "unavailable"
    if r["knock_limited"]:
        return "knock-limited at 30 CAD"
    if r["retard_attempts"] == 1:
        return "no knock at CA50 8"
    if r["ca50_used_deg"] <= par.selection_ca50_limit_rad / RAD + 1e-9:
        return "retarded, CA50 <= 15"
    return "retarded, CA50 > 15"


def write_plots(out, rows, results, par=DEFAULTS):
    computed = [r for r in rows if r["status"] == "computed"]
    names = list(dict.fromkeys(r["fuel"] for r in rows))
    temps = sorted({r["T_intake_K"] for r in rows})
    fig, axes = plt.subplots(1, len(names), figsize=(6 * len(names), 4.5), squeeze=False)
    for ax, fuel in zip(axes[0], names):
        for T, style in zip(temps, ("-", "--")):
            for w in sorted({r["w"] for r in computed if r["fuel"] == fuel}):
                group = sorted((r for r in computed if r["fuel"] == fuel and r["T_intake_K"] == T
                                and r["w"] == w), key=lambda r: r["CR"])
                if group:
                    ax.plot([r["CR"] for r in group], [r["gross_indicated_efficiency"] for r in group],
                            style, marker="o", color=plt.get_cmap("viridis")(w / 0.8),
                            label=f"w={w:g}, {T:g} K")
        ax.set(xlabel="Compression ratio [-]", ylabel="Gross indicated efficiency (CA50 used) [-]",
               title=fuel)
        if ax.lines:
            ax.legend(fontsize="x-small", ncol=2)
        ax.grid(alpha=0.3)
    fig.tight_layout()
    io.save_fig(fig, out / "efficiency_vs_CR.png")
    plt.close(fig)

    styles = {"no knock at CA50 8": ("o", "tab:blue"), "retarded, CA50 <= 15": ("^", "tab:green"),
              "retarded, CA50 > 15": ("v", "tab:orange"), "knock-limited at 30 CAD": ("x", "tab:red"),
              "unavailable": (".", "grey")}
    fig, axes = plt.subplots(len(names), len(temps), squeeze=False,
                             figsize=(6 * len(temps), 3.6 * len(names)))
    for i, fuel in enumerate(names):
        for k, T in enumerate(temps):
            ax = axes[i, k]
            for status, (marker, color) in styles.items():
                group = [r for r in rows if r["fuel"] == fuel and r["T_intake_K"] == T
                         and _status(r, par) == status]
                if group:
                    ax.scatter([r["w"] for r in group], [r["CR"] for r in group], marker=marker,
                               color=color, label=status)
            ax.set(xlabel="Water mass fraction w [-]", ylabel="Compression ratio [-]",
                   title=f"{fuel}, T_intake {T:g} K")
            ax.legend(fontsize="x-small")
    fig.tight_layout()
    io.save_fig(fig, out / "knock_limited_map.png")
    plt.close(fig)

    fig, axes = plt.subplots(1, len(names), figsize=(6 * len(names), 4.5), squeeze=False)
    for ax, fuel in zip(axes[0], names):
        for T, style in zip(temps, ("-", "--")):
            for cr in sorted({r["CR"] for r in computed if r["fuel"] == fuel}):
                group = sorted((r for r in computed if r["fuel"] == fuel and r["T_intake_K"] == T
                                and r["CR"] == cr and r["relative_NO"] is not None), key=lambda r: r["w"])
                if group:
                    ax.semilogy([r["w"] for r in group], [r["relative_NO"] for r in group], style,
                                marker="o", label=f"CR {cr}, {T:g} K")
        ax.set(xlabel="Water mass fraction w [-]", ylabel="NO per J fuel / dry value [-]",
               title=f"{fuel} (absolute NO: factor-2 uncertainty)")
        if ax.lines:
            ax.legend(fontsize="xx-small", ncol=2)
        ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    io.save_fig(fig, out / "relative_NO_vs_w.png")
    plt.close(fig)

    examples = [r for r in results if r["trace"]]
    fuel = next((f for f in names if any(r["point"]["fuel"] == f for r in examples)), None)
    examples = [r for r in examples if r["point"]["fuel"] == fuel]
    for name, xkey, xlabel in (("p_V_example", "V_m3", "Cylinder volume [m3]"),
                               ("p_theta_example", "theta_deg", "Crank angle [deg aTDC]")):
        fig, ax = plt.subplots(figsize=(7, 4.5))
        for r in examples:
            t = r["trace"]
            ax.plot(t[xkey], np.array(t["p_Pa"]) / 1e5,
                    label=f"{point_key(r['point'])}, CA50 {r['point']['ca50_used_deg']:g}")
        if name == "p_V_example" and examples:
            ax.set_xscale("log")
            ax.set_yscale("log")
        ax.set(xlabel=xlabel, ylabel="Cylinder pressure [bar]",
               title="Closed cycle IVC-EVO" if examples else "No computed example cycle")
        if ax.lines:
            ax.legend(fontsize="x-small")
        ax.grid(alpha=0.3, which="both")
        io.save_fig(fig, out / f"{name}.png")
        plt.close(fig)


# -------------------------------------------------------------- assumptions
def assumptions(mode, workers, provenance, par=DEFAULTS):
    result = fuels.fuel_assumptions()
    sources = {
        "bore_m,stroke_m,rod_m,rpm,ivc_rad,evo_rad,residual_fraction,p_ivc_Pa,phi": "SPEC section 6 default test engine (WOT, IVC at BDC, EVO 140 CAD aTDC)",
        "wiebe_a,wiebe_m,combustion_efficiency,burn_duration_ref_rad,burn_duration_cap_rad,flame_speed_exponent,ca50_rad": "SPEC section 6: Wiebe a=5, m=2; eta_c 0.98; 10-90 % duration 25 CAD*(S_L,ref/S_L)^0.5, cap 80 CAD; CA50 8 CAD aTDC (MBT proxy). Wiebe form: Heywood (1988) eq. 9.23",
        "knock_burn_fraction,retard_step_rad,retard_limit_rad": "SPEC section 6 Livengood-Wu knock criterion and retard rule",
        "endgas_anchor_xb": "Numerical: end gas is the bulk charge until x_b = 1e-3, then a frozen isentrope (standard two-zone practice); also the Woschni motored-pressure reference",
        "selection_ca50_limit_rad,flame_speed_min_m_s,peak_pressure_limit_Pa": "SPEC section 6 water-majority map constraints",
        "wall_T_K": "SPEC section 6",
        "woschni_C,woschni_C1,woschni_C2": "Woschni (1967), SAE 670931, doi:10.4271/670931; Heywood (1988) eq. 12.19; p in kPa inside the correlation only",
        "f_evap_intake,evap_end_rad": "SPEC section 6 (f_evap_intake is treated as an upper bound limited by saturation; see water_model)",
        "water_T_K": "300 K liquid water, as Module 02 evaporative-cooling convention",
        "step_rad,quick_step_rad": "Fixed crank step: 0.5 CAD full, 1 CAD quick; the closure error vs trapezoid quadrature reports the discretisation error",
        "equilibrium_min_T_K": "Burned part frozen as complete products below 1000 K (dissociation energy there < 1e-6 of LHV); avoids needless equilibrium solves",
        "state_rtol_U,state_rtol_p": "Numerical state-inversion tolerances (fraction of fuel energy; relative pressure)",
        "knock_integral_cap": "Floating-point guard only; any value >= 1 is knock",
        "closure_tolerance": "Task contract: |energy closure error| <= 2 % of fuel LHV",
        "otto_gamma,otto_tolerance_abs,otto_burn_duration_rad,otto_step_rad,otto_T_ivc_K,otto_gas_constant_J_kg_K,otto_heat_per_mass_J_kg": "SPEC section 10 ideal-Otto check: gamma 1.4, +/-1 % abs; 1 CAD burn centred on TDC approximates an instant burn; EVO moved to BDC; R, T_IVC and heat input do not affect 1-CR^(1-gamma)",
        "no_min_xb,no_absolute_uncertainty_factor": "NO integrated once x_b > 1e-3; task: absolute NO +/- factor 2",
        "plausible_efficiency_min,plausible_efficiency_max": "Task plausibility band for 0-D gross indicated efficiency at w = 0 (diagnostic, not validation)",
        "limit_flame_temperature_K": "Diagnostic flag only: adiabatic flame temperatures at hydrocarbon lean flammability limits are commonly quoted near 1500 K (limit flame temperature rule of thumb, e.g. Glassman, Combustion); not a SPEC selection constraint",
    }
    result.update({
        "parameters": {"defaults": asdict(par), "angles": "radians internally; *_deg outputs in CAD aTDC",
                       "used_step_deg": par.step_rad / RAD, "sources": sources},
        "mode": {"value": mode, "run_label": provenance["label"],
                 "sweep": dict(zip(("fuels", "CR", "w", "T_intake_K"), sweep(mode)))},
        "workers": {"value": workers, "rationale": "Spawned point tasks (io.ordered_map, chunksize 1); Cantera objects built inside each worker"},
        "fits": provenance,
        "synthetic_fallback": {"used": bool(provenance["synthetic"]),
                               "ignition": "Douaud & Eyzat (1978) SAE 780080 form (Heywood 1988 section 9.6), RON CH4 120 / CH3OH 108.7 / C2H5OH 108.6, c = 0",
                               "flame_speed": "linear 0.5 -> 0.1 m/s over w 0..0.8",
                               "policy": "quick mode only, labelled mode-quick-fallback; --full errors without Module 02 files"},
        "ignition_fit_units": {"value": "tau = A p^-n exp(E/(R T)) (1 + c w); p in Pa, A in s*Pa**n, E in J/mol, R = 8.314 J/(mol K)",
                               "source": "Module 02 ignition_fits.json schema (pressure_unit Pa)",
                               "extrapolation": "Allowed for the knock integral; the fraction of the integral outside the fit's T/p/w calibration ranges is reported per point"},
        "flame_speed_fit": {"value": "Module 02 cubic S_L(w) at 400 K, 1 atm, phi 1 (coefficients_highest_first); only the ratio S_L(0)/S_L(w) and the 0.08 m/s constraint use it",
                            "extrapolation": "None: w outside valid_w_range makes the point unavailable"},
        "energy_ledger": {"value": "eta_c m_f LHV (x_EVO - x_IVC) = W(IVC-EVO) + Q_wall + Q_evap,cylinder + [U_s(EVO) - U_s(IVC)]",
                          "closure_check": "W and Q_wall re-integrated by the trapezoid rule over node states, U_s(EVO) re-evaluated by Cantera; error reported per point as fraction of m_f LHV",
                          "intake_ledger": "H_s,dry(T_intake) = H_s(T_IVC) + m_w,evap h_latent (isobaric mixing); closes separately (intake_closure_error_J)",
                          "exhaust_term": "Closed system: the charge internal-energy change replaces the steady-flow 'exhaust enthalpy change'; U_s and the EVO state are written for Module 04",
                          "not_counted": "Fuel combustion loss (1-eta_c) m_f LHV and the Wiebe tail after EVO leave as chemical energy; water contributes no source term"},
        "sensible_reference": {"value": f"Unburned frozen u(T) - u({T_REF} K); burned u_eq(T,p) - u_complete_products({T_REF} K)",
                               "rationale": "LHV release counts formation energy once; dissociation energy of equilibrium products is retained"},
        "mixture_model": {"value": "Single bulk T and p; unburned frozen fresh charge + burned TP-equilibrium products mixed by mass fraction burned", "source": "SPEC section 6"},
        "residual_model": {"value": "5 % of the dry trapped mass as complete products of the fresh charge at T_intake (before water cooling)",
                           "rationale": "Keeps the per-cycle ledger self-contained: no residual heat or residual water is credited"},
        "water_model": {"value": "Liquid at 300 K. Intake: isobaric adiabatic mixing evaporates min(f_evap_intake, saturation limit) with h_fg. Cylinder: remainder on the SPEC uniform schedule IVC -> -30 CAD, capped at saturation (lagged one step), then as soon as saturation allows; closed-system latent heat u_fg",
                        "source": "SPEC section 6; CoolProp IAPWS-95 (Wagner & Pruss 2002) h_fg, u_fg, p_sat",
                        "deviation": "SPEC says 'h_fg' for the cylinder: a closed control mass needs u_fg = h_fg - p v_fg (about 5.7 % smaller at 300 K); using h_fg there would destroy energy. f_evap_intake is an upper bound: at w > ~0.1 the intake air cannot evaporate half the water above its dew point, so the intake fraction is saturation-limited and reported (f_evap_intake_effective)",
                        "limitations": "No droplet heating, spray kinetics or wall film; droplets have zero volume; liquid remaining at EVO is reported, not hidden"},
        "fuel_phase": {"value": "Premixed fuel vapour in the charge; heat release uses the registered-phase (liquid alcohol) LHV",
                       "rationale": "Never credits more than LHV(liquid); the alcohol latent heat is debited from the release, so no fuel charge-cooling benefit is claimed (conservative for efficiency and knock)",
                       "diagnostic": "fuel_vapour_saturation_ratio_IVC > 1 means the premixed-vapour assumption is optimistic at IVC"},
        "knock_model": {"value": "Livengood-Wu integral of 1/tau(T_u, p) from IVC to x_b = 0.9; T_u = bulk T before x_b = 1e-3, then frozen variable-cp isentrope (Cantera SP)",
                        "limitation": "Evaporation after the anchor does not cool the end gas (conservative)"},
        "burned_zone": {"value": "T_b = max(T, min(T_flame, T_u + (T - T_u)/x_b)); T_flame = HP flame temperature of the end gas with the same eta_c*LHV release (model-consistent)",
                        "rationale": "Two-zone NO diagnostic only; not used in the energy equation"},
        "NO_model": {"value": "Thermal NO, extended Zeldovich, quasi-steady N, implicit integration in the burned zone; equilibrium O, O2, N2, OH, H at (T_b, p)",
                     "rate_coefficients_m3_mol_s": {k: list(v) for k, v in NO_RATES.items()},
                     "source": "Hanson & Salimian (1984) via Turns, An Introduction to Combustion, ch. 5",
                     "absolute_uncertainty": f"+/- factor {par.no_absolute_uncertainty_factor:g}",
                     "relative_basis": "mol NO per J fuel LHV relative to w = 0 at the same fuel, CR and T_intake (CA50 as used at each point); prompt and N2O-route NO and NOx after EVO excluded"},
        "gross_efficiency_boundary": {"value": "Integral p dV from IVC to EVO divided by m_f LHV",
                                      "rationale": "SPEC closed cycle; no gas exchange, friction or blowdown work after EVO"},
        "cantera_ic_engine_comparison": {"status": "documented_only_not_numerically_reproduced",
                                         "value": "ic_engine.py (Cantera examples; not downloaded per task rules): Diesel-type compression ignition, gaseous fuel injected near TDC, finite-rate chemistry, valves and moving-wall piston over open four-stroke cycles. This module: premixed SI, closed IVC-EVO, Wiebe, Woschni, water evaporation, equilibrium thermo. Different combustion mode and system boundary, so no numeric efficiency agreement is claimed; the analytic Otto check and the dry CR trend replace it",
                                         "deviation": "SPEC section 6 asks for a reproduction of the example's settings; not done (offline rule, CI vs SI mismatch)"},
    })
    return result


def clean_json(value):
    """Convert numpy scalars and non-finite floats so json allow_nan=False succeeds."""
    if isinstance(value, dict):
        return {str(k): clean_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean_json(v) for v in value]
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    if isinstance(value, (int, np.integer)):
        return int(value)
    if isinstance(value, (float, np.floating)):
        return float(value) if math.isfinite(value) else None
    return value


def _write_json(path, payload):
    path.write_text(json.dumps(clean_json(payload), indent=2, allow_nan=False) + "\n", encoding="utf-8")


def efficiency_table(rows):
    table = {}
    for r in rows:
        if r["status"] != "computed":
            continue
        cell = dict(efficiency=r["gross_indicated_efficiency"],
                    efficiency_at_default_ca50=r["efficiency_at_default_ca50"],
                    ca50_used_deg=r["ca50_used_deg"], knock_at_default_ca50=r["retard_attempts"] > 1,
                    knock_limited=r["knock_limited"], relative_NO=r["relative_NO"],
                    peak_temperature_K=r["peak_temperature_K"], peak_pressure_bar=r["peak_pressure_Pa"] / 1e5,
                    closure=r["energy_closure_error_fraction"])
        table.setdefault(r["fuel"], {}).setdefault(f"T_intake={r['T_intake_K']:g}", {}).setdefault(
            f"w={r['w']:g}", {})[f"CR={r['CR']:g}"] = cell
    return table


def main(argv=None):
    start = time.perf_counter()
    parser = io.argument_parser(MODULE)
    parser.add_argument("--fits-dir", type=Path, default=Path("results") / "02_flame_chem",
                        help="Directory with Module 02 ignition_fits.json and flame_speed_fits.json")
    args = parser.parse_args(None if argv is None else list(map(str, argv)))
    names = sweep(args.mode)[0]
    ignition, flame, provenance = read_fits(args.fits_dir, args.mode, names)  # --full: raises if missing
    par = replace(DEFAULTS, step_rad=DEFAULTS.quick_step_rad) if args.mode == "quick" else DEFAULTS
    args.out.mkdir(parents=True, exist_ok=True)
    tasks = build_tasks(args.mode, ignition, flame, provenance, par)
    results = io.ordered_map(_task, tasks, args.workers, chunksize=1)
    order = {f: i for i, f in enumerate(FUELS)}
    results.sort(key=lambda r: (order[r["point"]["fuel"]], r["point"]["CR"], r["point"]["w"],
                                r["point"]["T_intake_K"]))
    rows = [r["point"] for r in results]
    add_relative_no(rows)
    otto = [ideal_otto(cr, par=par) for cr in FULL_CR]
    checks = validate(rows, otto, par)
    maps, design = select_designs(rows, provenance, checks["passed"], par)
    design["mode"] = args.mode
    design["sensitivity"] = sensitivity_summary(rows, ignition, flame, provenance, par, args.mode)
    io.write_csv(args.out / "cycle_points.csv", rows)
    io.write_csv(args.out / "water_majority_map.csv", maps)
    io.write_csv(args.out / "ideal_otto.csv", otto)
    evo = {r["evo"]["key"]: dict(r["evo"], synthetic_fits=provenance["synthetic"])
           for r in results if r["evo"]}
    _write_json(args.out / "design_point.json", design)
    _write_json(args.out / "evo_states.json", evo)
    write_plots(args.out, rows, results, par)
    settings = assumptions(args.mode, args.workers, provenance, par)
    settings["mechanism_fallback"] = any(r["mechanism_fallback"] for r in rows)
    settings["mechanisms"] = {r["fuel"]: {"name": r["mechanism"], "mechanism_fallback": r["mechanism_fallback"]}
                              for r in rows}
    computed = [r for r in rows if r["status"] == "computed"]
    key_results = dict(
        run_label=provenance["label"], synthetic_fits=provenance["synthetic"],
        warning=provenance["warning"], efficiency_table=efficiency_table(rows),
        water_majority_map=maps, design_point=design,
        max_abs_energy_closure_error_fraction=checks["max_abs_energy_closure_error_fraction"],
        max_abs_ideal_otto_error=checks["max_abs_ideal_otto_error"],
        computed_points=len(computed),
        unavailable_points=sum(r["status"] == "unavailable" for r in rows),
        failed_points=sum(r["status"] == "failed" for r in rows),
        knocking_at_default_ca50=[point_key(r) for r in computed if r["retard_attempts"] > 1],
        knock_limited_points=[point_key(r) for r in computed if r["knock_limited"]],
        saturation_limited_intake_points=sum(bool(r["intake_saturation_limited"]) for r in computed),
        liquid_water_at_EVO_points=[point_key(r) for r in computed if r["liquid_water_at_EVO_kg"] > 1e-12],
        low_flame_temperature_points=[point_key(r) for r in computed if r["low_flame_temperature"]],
        low_flame_temperature_note=(f"Diagnostic, not a SPEC constraint: model-consistent end-gas flame "
                                    f"temperature (droplet latent heat included) below "
                                    f"{par.limit_flame_temperature_K:g} K; Module 02 S_L(w) is for an "
                                    f"all-vapour charge and may overstate flame propagation there"),
        no_relative_uncertainty="Relative NO only; absolute NO +/- factor 2",
        energy_source="Fuel LHV only (eta_c m_f LHV); water has zero heating value and only absorbs latent heat")
    io.write_summary(args.out, MODULE, VERSION, args.mode, clean_json(settings), clean_json(key_results),
                     clean_json(checks), time.perf_counter() - start)
    return 0 if checks["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
