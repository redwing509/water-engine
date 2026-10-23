"""SPEC section 7 (Module 04 six_stroke): water-injection six-stroke steam loop.

Crower (2006); Conklin & Szybist, Energy 35:1658 (2010). Runs on the Linux
simulation server; the laptop only compiles.

Cycle (crank angle theta in radians after firing TDC; CAD only in outputs;
gas-exchange TDC = 360 CAD, stroke-5 BDC = 540 CAD):
* Strokes 1-3: Module 03 design point, read ONLY from its files
  (design_point.json -> recommended_evo_state_key -> evo_states.json).
* EVO (140 CAD): blowdown. The gas that stays in the cylinder expands
  isentropically (Cantera, frozen EVO composition) to the exhaust pressure.
* Stroke 4: displacement exhaust at p_exh from BDC to EVC; the gas still in
  the cylinder at EVC is trapped (EVC sweeps the trapped fraction).
* EVC -> 360 CAD: closed recompression.
* 360 CAD: liquid water (300 K tank, pumped to 100 bar) is injected and mixed
  instantly at constant volume (open-system energy balance: + m_w h_inj).
* Stroke 5: closed expansion until the exhaust valve re-opens (EVO5).
* Stroke 6: displacement exhaust at p_exh.

Extra work. The fuel charge, strokes 1-3 and the intake stroke are those of
the four-stroke; the four-stroke exhausts its whole stroke at p_exh. All
gas-exchange work cancels except over the steam loop, so per cycle
    W_extra,gross = integral_{EVC}^{EVO5} (p - p_exh) dV,
    W_extra,net   = W_extra,gross - W_pump.
Because dW/dV_EVO5 = p - p_exh, the best EVO5 is where p falls to p_exh
(else BDC); it is taken as the argmax over the expansion nodes. Without water
and wall heat the loop is a reversible gas spring that returns to p_exh at
V_EVC, so W_extra = 0 exactly (the zero-water test).

Thermodynamics. Two components in the whole volume (Dalton, ideal mixing):
* "dry" exhaust = every EVO species except H2O, frozen ideal gas (Cantera);
* water = the exhaust's own H2O plus the injected water, real fluid
  (CoolProp IAPWS-95, Wagner & Pruss 2002), in phase equilibrium.
At every state the water density m_w/V is compared with the saturated-vapour
density at T. If it is higher the water is two-phase at p_sat(T): the liquid
mass and the latent heat follow from the lever rule, so condensation (or
incomplete evaporation) is accounted for with its latent heat, never ignored.
The mixture temperature is solved from U(T, V) = U at each node.

Energy (SPEC section 0). Water is never a source: the steam loop is fed only
by the trapped exhaust's energy (which the fuel LHV already paid for in
strokes 1-3), the pump work and, with Woschni walls, any heat the 450 K walls
return to a colder charge. Ledger per point, EVC -> EVO5:
    m_w h_inj = W_loop + Q_wall + [U(EVO5) - U(EVC)],
re-integrated with trapezoid quadrature over the node states; the closure
error is reported as a fraction of the trapped-exhaust sensible enthalpy and
must stay within 1 %. W_extra,net is also checked against the trapped exhaust's
thermo-mechanical exergy (Cantera, dead state 298.15 K, p_exh) plus the
water's tank exergy and the Carnot exergy of wall heat gained.

Literature (docs/research/02-legitimate-water-combustion.md section 4; context
only, not hard tests): Conklin & Szybist report a net steam-stroke MEP of
0.75-2.5 bar from an ideal model with conventional SI geometry; Yang et al.
(2023, via review) raised IMEP 5.89 -> 6.21 bar by injecting 97.81 mg of STEAM
at 20 bar. Both use water/steam that external exhaust or coolant heat has
already heated; here the SPEC injects 300 K liquid that only the trapped
charge heats, and summary.json compares the result with that range.
Expected sign: evaporating and heating cold liquid takes ~41 kJ/mol plus
c_v,w (T - 300 K) from the trapped gas, more than the ~c_v T per mole the
vapour adds to p V, so injection lowers p at TDC and the expansion line runs
below the recompression line. A non-positive steam-loop gain for this SPEC
configuration is therefore physics, not a model defect; the sweep reports it.
"""

from dataclasses import asdict, dataclass, replace
import hashlib
import json
import math
from pathlib import Path
import time

import cantera as ct
import CoolProp
from CoolProp.CoolProp import PropsSI
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
from scipy.optimize import brentq

from sims.common import fuels, io


MODULE = "04_six_stroke"
VERSION = "1.0.0"
RAD = math.pi / 180.0
TWO_PI = 2.0 * math.pi
T_REF = fuels.REFERENCE_T_K  # sensible-energy zero and exergy dead-state temperature
P_REF = ct.one_atm  # ideal-gas u(T) evaluation pressure (u is pressure independent)
WATER_T_CRIT = float(PropsSI("Tcrit", "Water"))
WATER_T_TRIPLE = float(PropsSI("Ttriple", "Water"))
SAT_MARGIN_K = 0.05  # no saturation call within 0.05 K of T_crit (water densities here << rho_crit)
T_MIN_K = WATER_T_TRIPLE + 1e-6
T_MAX_K = 6000.0
HEAT_MODES = ("adiabatic", "woschni")
FULL_EVC_DEG = tuple(float(a) for a in range(190, 351, 10))
FULL_WATER_MG = (0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 7.5, 10.0, 15.0, 20.0, 30.0, 45.0, 60.0)
QUICK_EVC_DEG = (220.0, 280.0, 330.0)
QUICK_WATER_MG = (0.0, 2.0, 10.0, 40.0)
PLOT_EVC_DEG = (190.0, 230.0, 270.0, 310.0, 350.0)
# SPEC section 6 default test engine; used only by the labelled synthetic fallback.
DEFAULT_ENGINE = dict(bore_m=0.086, stroke_m=0.086, rod_m=0.145, rpm=2000.0, evo_deg=140.0,
                      p_ivc_Pa=1.0e5)

LITERATURE = dict(
    conklin_szybist_2010=dict(
        steam_MEP_bar=[0.75, 2.5], combustion_MEP_bar_up_to=10.0,
        implied_extra_work_pct_of_combustion_work=[7.5, 25.0],
        basis="Ideal thermodynamic model, conventional SI geometry; EVC limited by 1 bar or by the dew "
              "point at the end of the steam expansion. Abstract also credits engine-coolant heat.",
        source="Conklin & Szybist, Energy 35(4):1658-1664 (2010); OSTI 1035139 (docs/research/02 refs 23, 24)"),
    yang_2023=dict(IMEP_bar=[5.89, 6.21], relative_gain=6.21 / 5.89 - 1.0, injected_mg=97.81,
                   injection="steam at 20 bar (externally generated)",
                   source="Yang et al. (2023) via review (docs/research/02 ref 29, secondary)"),
    crower_2006=dict(claim="~40 % better fuel efficiency", status="unverified press claim (docs/research/02 refs 26, 27)"),
    use="Context only, not hard tests (task brief)")


@dataclass(frozen=True)
class Parameters:
    """Named defaults; sources and rationales are written by assumptions()."""

    p_exhaust_Pa: float = 1.0e5
    dead_state_T_K: float = T_REF
    water_T_K: float = 300.0
    injection_p_Pa: float = 100.0e5
    tank_p_Pa: float = 101325.0
    pump_efficiency: float = 0.6
    wall_T_K: float = 450.0
    woschni_C: float = 3.26
    woschni_C1_closed: float = 2.28
    woschni_C1_exchange: float = 6.18
    step_rad: float = 0.5 * RAD
    quick_step_rad: float = 1.0 * RAD
    state_xtol_K: float = 1.0e-7
    closure_tolerance: float = 0.01
    zero_water_tolerance: float = 2.0e-3
    peak_pressure_limit_Pa: float = 120.0e5


DEFAULTS = Parameters()


class ThermoError(ValueError):
    """State outside the model domain; reported per point, never hidden."""


class Freezing(ThermoError):
    """The mixture would have to cool below the water triple point."""


# ----------------------------------------------------------------- geometry
def displacement(eng):
    """Swept volume [m3]."""
    return math.pi * eng["bore_m"] ** 2 / 4.0 * eng["stroke_m"]


def volume(theta, eng):
    """Slider-crank volume [m3]; theta [rad] after firing TDC (period 2 pi).

    Heywood (1988), Internal Combustion Engine Fundamentals, eq. 2.4-2.5; the
    SPEC section 6 geometry (re-implemented: modules share data, not code).
    """
    a = eng["stroke_m"] / 2.0
    s = a * math.cos(theta) + math.sqrt(eng["rod_m"] ** 2 - (a * math.sin(theta)) ** 2)
    return (displacement(eng) / (eng["CR"] - 1.0)
            + math.pi * eng["bore_m"] ** 2 / 4.0 * (eng["rod_m"] + a - s))


def wall_area(V, eng):
    """Head + flat piston crown + exposed liner [m2]."""
    return 2.0 * math.pi * eng["bore_m"] ** 2 / 4.0 + 4.0 * V / eng["bore_m"]


def woschni_heat_rate(p, T, V, C1, eng, par):
    """Gas-to-wall heat rate [W]; negative when the walls heat the charge.

    Woschni (1967), SAE 670931, doi:10.4271/670931; Heywood (1988) eq. 12.19:
    h = 3.26 B^-0.2 p[kPa]^0.8 T^-0.55 w^0.8 [W/(m2 K)], motored form
    w = C1 S_p (no combustion term: the steam loop burns nothing).
    """
    speed = C1 * 2.0 * eng["stroke_m"] * eng["rpm"] / 60.0
    h = (par.woschni_C * eng["bore_m"] ** -0.2 * (p / 1000.0) ** 0.8
         * T ** -0.55 * speed ** 0.8)
    return h * wall_area(V, eng) * (T - par.wall_T_K)


# ------------------------------------------------------------ thermodynamics
class Thermo:
    """Worker-local Cantera and CoolProp objects for one frozen exhaust (never pickled)."""

    def __init__(self, fuel, mechanism, composition):
        self.full = fuels.load_mechanism(fuel, mechanism)  # whole exhaust incl. H2O vapour
        names = self.full.species_names
        unknown = sorted(k for k in composition if k not in names)
        if unknown:
            raise ValueError("EVO composition has species absent from the mechanism: " + ", ".join(unknown))
        Y = np.zeros(self.full.n_species)
        for name, y in composition.items():
            Y[self.full.species_index(name)] = float(y)
        if not Y.sum() > 0.0:
            raise ValueError("EVO composition is empty")
        self.Y = Y / Y.sum()
        self.j = self.full.species_index(fuels.species_name(self.full, "H2O"))
        self.Y_water = float(self.Y[self.j])
        dry = self.Y.copy()
        dry[self.j] = 0.0
        if not dry.sum() > 0.0:
            raise ValueError("Exhaust without non-water species is outside this model")
        self.dry = fuels.load_mechanism(fuel, mechanism)
        self.dry.TPY = T_REF, P_REF, dry / dry.sum()
        self.u_dry_ref = float(self.dry.int_energy_mass)
        self.R_dry = ct.gas_constant / float(self.dry.mean_molecular_weight)  # J/(kg K)
        self.full.TPY = T_REF, P_REF, self.Y
        self.R_full = ct.gas_constant / float(self.full.mean_molecular_weight)
        self.vap = CoolProp.AbstractState("HEOS", "Water")
        self.vap.specify_phase(CoolProp.iphase_gas)  # single-phase branch only; saturation tested first
        self.sat = CoolProp.AbstractState("HEOS", "Water")

    def dry_u(self, T):
        """Sensible internal energy of the dry exhaust [J/kg], u(T) - u(298.15 K)."""
        self.dry.TP = T, P_REF
        return float(self.dry.int_energy_mass) - self.u_dry_ref

    def p_sat(self, T):
        if T >= WATER_T_CRIT - SAT_MARGIN_K:
            return math.inf
        self.sat.update(CoolProp.QT_INPUTS, 1.0, T)
        return float(self.sat.p())

    def water(self, T, rho):
        """Water at (T, rho = m_w/V) in phase equilibrium (IAPWS-95, CoolProp).

        Returns (u [J/kg, IAPWS reference], p_water [Pa], liquid mass fraction,
        two_phase). The saturation check is made first at every call.
        """
        if T < WATER_T_CRIT - SAT_MARGIN_K:
            s = self.sat
            s.update(CoolProp.QT_INPUTS, 1.0, T)
            rho_v = float(s.rhomass())
            if rho > rho_v:
                u_v, p_s = float(s.umass()), float(s.p())
                s.update(CoolProp.QT_INPUTS, 0.0, T)
                rho_l, u_l = float(s.rhomass()), float(s.umass())
                if rho >= rho_l:
                    raise ThermoError("Water would fill the cylinder as compressed liquid")
                x = (1.0 / rho - 1.0 / rho_l) / (1.0 / rho_v - 1.0 / rho_l)  # vapour mass fraction
                return u_l + x * (u_v - u_l), p_s, 1.0 - x, True
        self.vap.update(CoolProp.DmassT_INPUTS, rho, T)
        return float(self.vap.umass()), float(self.vap.p()), 0.0, False

    def energy(self, T, V, m_d, m_w):
        """Mixture internal energy [J] (dry: sensible, Cantera; water: IAPWS reference)."""
        U = m_d * self.dry_u(T)
        if m_w > 0.0:
            U += m_w * self.water(T, m_w / V)[0]
        return U

    def evaluate(self, T, V, m_d, m_w):
        p_w, liquid, two = 0.0, 0.0, False
        U = m_d * self.dry_u(T)
        if m_w > 0.0:
            u_w, p_w, f_liq, two = self.water(T, m_w / V)
            U += m_w * u_w
            liquid = f_liq * m_w
        ps = self.p_sat(T)
        ratio = 1.0 if two else (0.0 if math.isinf(ps) else p_w / ps)
        return dict(T=T, V=V, U=U, p=m_d * self.R_dry * T / V + p_w, p_water=p_w,
                    liquid_kg=liquid, two_phase=two, saturation_ratio=ratio)

    def state(self, U, V, m_d, m_w, guess):
        """Invert U(T, V) = U for T (monotonic, incl. the two-phase branch)."""

        def f(T):
            return self.energy(T, V, m_d, m_w) - U

        lo = max(T_MIN_K, guess - 40.0)
        hi = lo + 80.0
        f_lo = f(lo)
        while f_lo > 0.0:
            if lo <= T_MIN_K:
                raise Freezing(f"Mixture would cool below the water triple point (U={U:.6g} J, V={V:.4g} m3)")
            width = hi - lo
            hi, lo = lo, max(T_MIN_K, lo - 4.0 * width)
            f_lo = f(lo)
        f_hi = f(hi)
        while f_hi < 0.0:
            width = hi - lo
            lo, hi = hi, hi + 4.0 * width
            if hi > T_MAX_K:
                raise ThermoError(f"Mixture temperature above {T_MAX_K:g} K")
            f_hi = f(hi)
        T = brentq(f, lo, hi, xtol=DEFAULTS.state_xtol_K, rtol=1e-14, maxiter=200)
        return self.evaluate(T, V, m_d, m_w)


_THERMO = {}


def thermo(ctx):
    """Per-process cache; spawned workers build their own Cantera/CoolProp objects."""
    key = (ctx["fuel"], ctx["mechanism"], tuple(sorted(ctx["composition"].items())))
    if key not in _THERMO:
        _THERMO[key] = Thermo(ctx["fuel"], ctx["mechanism"], ctx["composition"])
    return _THERMO[key]


def trapped_state(th, ctx, evc, heat, par):
    """Blowdown, stroke-4 displacement to EVC, and the trapped charge.

    Blowdown: instantaneous, adiabatic and isentropic for the gas that stays
    (Cantera SP at frozen composition), standard ideal-cycle exhaust model
    (Heywood 1988 section 5.4). Displacement BDC -> EVC at constant p_exh:
    m c_p dT = -dQ_wall (Woschni, gas-exchange C1 = 6.18) or adiabatic.
    """
    full, p_ex = th.full, par.p_exhaust_Pa
    full.TPY = ctx["T_evo_K"], ctx["p_evo_Pa"], th.Y
    blowdown = ctx["p_evo_Pa"] > p_ex
    if blowdown:
        full.SP = full.entropy_mass, p_ex
    T = T_bd = float(full.T)
    Q_exchange = 0.0
    if heat == "woschni":
        omega = ctx["rpm"] * TWO_PI / 60.0
        grid = np.linspace(math.pi, evc, max(1, math.ceil((evc - math.pi) / par.step_rad)) + 1)

        def rate(theta, T):
            V = volume(theta, ctx)
            full.TPY = T, p_ex, th.Y
            m = p_ex * V / (th.R_full * T)
            q = woschni_heat_rate(p_ex, T, V, par.woschni_C1_exchange, ctx, par)
            return -q / (m * float(full.cp_mass) * omega), q

        for a, b in zip(grid[:-1], grid[1:]):
            k1, _ = rate(a, T)
            k2, q = rate(0.5 * (a + b), T + 0.5 * (b - a) * k1)
            T += (b - a) * k2
            Q_exchange += q * (b - a) / omega
    V = volume(evc, ctx)
    Yw = th.Y_water
    m0 = p_ex * V / (th.R_full * T)

    def excess(m):
        p = (1.0 - Yw) * m * th.R_dry * T / V
        if Yw > 0.0:
            p += th.water(T, Yw * m / V)[1]
        return p - p_ex

    m = brentq(excess, 0.5 * m0, 2.0 * m0, xtol=1e-18, rtol=1e-13)
    return dict(T_blowdown_K=T_bd, T_evc_K=T, V_evc_m3=V, mass_kg=m, m_dry=(1.0 - Yw) * m,
                m_water=Yw * m, exchange_wall_heat_J=Q_exchange, blowdown=blowdown)


def trapped_enthalpy_exergy(th, T, m, par):
    """Trapped-exhaust sensible enthalpy and thermo-mechanical exergy [J] (Cantera).

    Frozen composition, all species ideal gas. Dead state (T0, p0) =
    (298.15 K, p_exh): X = m[(u - u0) + p0 (v - v0) - T0 (s - s0)]. Chemical
    and mixing exergy are excluded (the steam loop cannot use them).
    """
    full, p0, T0 = th.full, par.p_exhaust_Pa, par.dead_state_T_K
    full.TPY = T0, p0, th.Y
    h0, u0, v0, s0 = (float(full.enthalpy_mass), float(full.int_energy_mass),
                      1.0 / float(full.density_mass), float(full.entropy_mass))
    full.TPY = T, p0, th.Y
    h1, u1, v1, s1 = (float(full.enthalpy_mass), float(full.int_energy_mass),
                      1.0 / float(full.density_mass), float(full.entropy_mass))
    return m * (h1 - h0), m * ((u1 - u0) + p0 * (v1 - v0) - T0 * (s1 - s0))


def pump(m_w, par):
    """High-pressure water pump (CoolProp IAPWS-95).

    Tank liquid at (water_T_K, tank_p) is compressed isentropically to the
    injection pressure; the shaft work is w_s / eta_pump and the pump losses
    are rejected to ambient, so the injected water is the isentropic outlet
    state (300.0x K, 100 bar). Water tank exergy vs the dead state is tiny.
    """
    T0 = par.dead_state_T_K
    h_t = PropsSI("Hmass", "T", par.water_T_K, "P", par.tank_p_Pa, "Water")
    s_t = PropsSI("Smass", "T", par.water_T_K, "P", par.tank_p_Pa, "Water")
    h_i = PropsSI("Hmass", "P", par.injection_p_Pa, "Smass", s_t, "Water")
    T_i = PropsSI("T", "P", par.injection_p_Pa, "Smass", s_t, "Water")
    h0 = PropsSI("Hmass", "T", T0, "P", par.tank_p_Pa, "Water")
    s0 = PropsSI("Smass", "T", T0, "P", par.tank_p_Pa, "Water")
    w_s = h_i - h_t
    return dict(h_tank=h_t, h_inj=h_i, T_inj=T_i, w_isentropic=w_s,
                W_pump=m_w * w_s / par.pump_efficiency,
                X_tank=m_w * ((h_t - h0) - T0 * (s_t - s0)))


# ---------------------------------------------------------------- the loop
ROW_FIELDS = (
    "heat_transfer EVC_deg water_mg water_kg status reason trapped_mass_kg "
    "trapped_fraction_of_EVO_mass T_blowdown_K T_EVC_K exchange_wall_heat_J "
    "T_TDC_before_injection_K p_TDC_before_injection_Pa T_TDC_after_injection_K "
    "p_TDC_after_injection_Pa peak_pressure_Pa EVO5_deg p_EVO5_Pa T_EVO5_K "
    "expansion_truncated_freezing recompression_work_J expansion_work_J loop_work_J "
    "exhaust_displacement_correction_J extra_work_gross_J pump_work_J extra_work_net_J "
    "extra_work_pct_of_four_stroke four_stroke_work_J fuel_energy_J efficiency_four_stroke "
    "efficiency_six_stroke efficiency_gain_abs steam_MEP_net_Pa IMEP_four_stroke_Pa "
    "IMEP_six_stroke_cycle_Pa wall_heat_loss_J wall_heat_gained_J injection_T_K "
    "water_enthalpy_in_J water_enthalpy_above_tank_J charge_energy_change_J "
    "trapped_enthalpy_J trapped_exergy_J water_tank_exergy_J wall_heat_exergy_J "
    "exergy_bound_J extra_work_over_exergy_bound energy_closure_error_J "
    "energy_closure_error_fraction integrator_identity_error_fraction "
    "liquid_after_injection_kg max_liquid_kg condensed_kg condensed_latent_heat_J "
    "liquid_at_EVO5_kg two_phase_nodes two_phase_nodes_to_BDC max_saturation_ratio "
    "saturation_ratio_EVO5 intake_water_kg injected_water_kg combined_water_kg "
    "combined_w combined_WFR").split()


def run_loop(ctx, evc_deg, water_kg, heat="adiabatic", par=DEFAULTS, keep_trace=False):
    """Strokes 4-6 for one (EVC, injected water mass, heat-transfer mode) point.

    Crank-angle RK2 (explicit midpoint) on U with p dV and Woschni heat; the
    trapezoid re-integration over node states gives the ledger closure.
    Unavailable states are returned with status 'failed' and a reason.
    """
    row = dict.fromkeys(ROW_FIELDS)
    row.update(heat_transfer=heat, EVC_deg=float(evc_deg), water_mg=water_kg * 1e6,
               water_kg=float(water_kg), status="computed", reason="")
    trace = None
    try:
        if heat not in HEAT_MODES:
            raise ValueError(f"heat must be one of {HEAT_MODES}")
        if not water_kg >= 0.0:
            raise ValueError("Injected water mass must be >= 0")
        evc = evc_deg * RAD
        if not math.pi < evc < TWO_PI:
            raise ValueError("EVC must lie inside stroke 4 (180 < EVC < 360 CAD)")
        th = thermo(ctx)
        p_ex = par.p_exhaust_Pa
        omega = ctx["rpm"] * TWO_PI / 60.0
        tr = trapped_state(th, ctx, evc, heat, par)
        m_d, m_w = tr["m_dry"], tr["m_water"]
        V_evc = tr["V_evc_m3"]
        st = th.evaluate(tr["T_evc_K"], V_evc, m_d, m_w)
        U_evc = st["U"]
        H_trap, X_trap = trapped_enthalpy_exergy(th, tr["T_evc_K"], tr["mass_kg"], par)
        pm = pump(water_kg, par)
        acc = dict(W=0.0, Wt=0.0, Q=0.0, Qt=0.0, Qgain=0.0)
        nodes = []

        def qrate(s):
            if heat != "woschni":
                return 0.0
            return woschni_heat_rate(s["p"], s["T"], s["V"], par.woschni_C1_closed, ctx, par)

        def record(theta, s, phase):
            nodes.append(dict(theta=theta, V=s["V"], p=s["p"], T=s["T"], U=s["U"],
                              liquid=s["liquid_kg"], two_phase=s["two_phase"],
                              sat=s["saturation_ratio"], phase=phase, **acc))

        def advance(s, q_left, a, b, mw):
            dt = (b - a) / omega
            Vm, Vb = volume(0.5 * (a + b), ctx), volume(b, ctx)
            U_mid = s["U"] - s["p"] * (Vm - s["V"]) - 0.5 * q_left * dt
            sm = th.state(U_mid, Vm, m_d, mw, s["T"])
            q_mid = qrate(sm)
            work = sm["p"] * (Vb - s["V"])
            sb = th.state(s["U"] - work - q_mid * dt, Vb, m_d, mw, sm["T"])
            q_right = qrate(sb)
            acc["W"] += work
            acc["Q"] += q_mid * dt
            acc["Qgain"] += max(0.0, -q_mid * dt)
            acc["Wt"] += 0.5 * (s["p"] + sb["p"]) * (Vb - s["V"])
            acc["Qt"] += 0.5 * (q_left + q_right) * dt
            return sb, q_right

        record(evc, st, "recompression")
        q_left = qrate(st)
        grid = np.linspace(evc, TWO_PI, max(2, math.ceil((TWO_PI - evc) / par.step_rad)) + 1)
        for a, b in zip(grid[:-1], grid[1:]):
            st, q_left = advance(st, q_left, a, b, m_w)
            record(b, st, "recompression")
        before = st
        W_recompression = acc["W"]
        m_w_total = m_w + water_kg
        if water_kg > 0.0:  # instantaneous constant-volume mixing at TDC
            st = th.state(st["U"] + water_kg * pm["h_inj"], st["V"], m_d, m_w_total, st["T"])
        record(TWO_PI, st, "expansion")
        i0 = len(nodes) - 1
        q_left = qrate(st)
        freezing = False
        grid = np.linspace(TWO_PI, 3.0 * math.pi, max(2, math.ceil(math.pi / par.step_rad)) + 1)
        for a, b in zip(grid[:-1], grid[1:]):
            try:
                st, q_left = advance(st, q_left, a, b, m_w_total)
            except Freezing:
                freezing = True  # valve must have opened by now; nodes so far stand
                break
            record(b, st, "expansion")
        gains = [n["W"] - p_ex * (n["V"] - V_evc) for n in nodes[i0:]]
        k = i0 + int(np.argmax(gains))  # optimal EVO5 (dW/dV = p - p_exh)
        e5 = nodes[k]
        W_gross = gains[k - i0]
        W_net = W_gross - pm["W_pump"]
        U_end = th.energy(e5["T"], e5["V"], m_d, m_w_total if k >= i0 else m_w)
        U_start = th.energy(tr["T_evc_K"], V_evc, m_d, m_w)
        E_in = water_kg * pm["h_inj"]
        closure = E_in - (e5["Wt"] + e5["Qt"] + U_end - U_start)
        identity = E_in - (e5["W"] + e5["Q"] + e5["U"] - U_evc)
        loop = nodes[:k + 1]
        run_min, condensed, T_cond = math.inf, 0.0, None
        for n in nodes[i0:k + 1]:
            run_min = min(run_min, n["liquid"])
            if n["liquid"] - run_min > condensed:
                condensed, T_cond = n["liquid"] - run_min, n["T"]
        latent = 0.0
        if condensed > 0.0 and T_cond < WATER_T_CRIT - SAT_MARGIN_K:
            latent = condensed * (PropsSI("Umass", "T", T_cond, "Q", 1, "Water")
                                  - PropsSI("Umass", "T", T_cond, "Q", 0, "Water"))
        X_wall = (1.0 - par.dead_state_T_K / par.wall_T_K) * e5["Qgain"]
        bound = X_trap + pm["X_tank"] + X_wall
        W4, Qf, Vd = ctx["four_stroke_work_J"], ctx["fuel_energy_J"], displacement(ctx)
        m_comb = ctx["intake_water_kg"] + water_kg
        row.update(
            trapped_mass_kg=tr["mass_kg"],
            trapped_fraction_of_EVO_mass=tr["mass_kg"] / ctx["gas_mass_evo_kg"],
            T_blowdown_K=tr["T_blowdown_K"], T_EVC_K=tr["T_evc_K"],
            exchange_wall_heat_J=tr["exchange_wall_heat_J"],
            T_TDC_before_injection_K=before["T"], p_TDC_before_injection_Pa=before["p"],
            T_TDC_after_injection_K=nodes[i0]["T"], p_TDC_after_injection_Pa=nodes[i0]["p"],
            peak_pressure_Pa=max(n["p"] for n in loop), EVO5_deg=e5["theta"] / RAD,
            p_EVO5_Pa=e5["p"], T_EVO5_K=e5["T"], expansion_truncated_freezing=freezing,
            recompression_work_J=W_recompression, expansion_work_J=e5["W"] - W_recompression,
            loop_work_J=e5["W"], exhaust_displacement_correction_J=-p_ex * (e5["V"] - V_evc),
            extra_work_gross_J=W_gross, pump_work_J=pm["W_pump"], extra_work_net_J=W_net,
            extra_work_pct_of_four_stroke=100.0 * W_net / W4, four_stroke_work_J=W4,
            fuel_energy_J=Qf, efficiency_four_stroke=W4 / Qf,
            efficiency_six_stroke=(W4 + W_net) / Qf, efficiency_gain_abs=W_net / Qf,
            steam_MEP_net_Pa=W_net / Vd, IMEP_four_stroke_Pa=W4 / Vd,
            IMEP_six_stroke_cycle_Pa=(W4 + W_net) / Vd,
            wall_heat_loss_J=e5["Q"], wall_heat_gained_J=e5["Qgain"], injection_T_K=pm["T_inj"],
            water_enthalpy_in_J=E_in, water_enthalpy_above_tank_J=water_kg * pm["w_isentropic"],
            charge_energy_change_J=e5["U"] - U_evc, trapped_enthalpy_J=H_trap,
            trapped_exergy_J=X_trap, water_tank_exergy_J=pm["X_tank"], wall_heat_exergy_J=X_wall,
            exergy_bound_J=bound, extra_work_over_exergy_bound=W_net / bound if bound > 0 else None,
            energy_closure_error_J=closure, energy_closure_error_fraction=closure / H_trap,
            integrator_identity_error_fraction=identity / H_trap,
            liquid_after_injection_kg=nodes[i0]["liquid"], max_liquid_kg=max(n["liquid"] for n in loop),
            condensed_kg=condensed, condensed_latent_heat_J=latent, liquid_at_EVO5_kg=e5["liquid"],
            two_phase_nodes=sum(bool(n["two_phase"]) for n in loop),
            two_phase_nodes_to_BDC=sum(bool(n["two_phase"]) for n in nodes),
            max_saturation_ratio=max(n["sat"] for n in loop), saturation_ratio_EVO5=e5["sat"],
            intake_water_kg=ctx["intake_water_kg"], injected_water_kg=water_kg,
            combined_water_kg=m_comb, combined_w=m_comb / (m_comb + ctx["fuel_mass_kg"]),
            combined_WFR=m_comb / ctx["fuel_mass_kg"])
        if keep_trace:
            trace = dict(theta_deg=[n["theta"] / RAD for n in nodes], V_m3=[n["V"] for n in nodes],
                         p_Pa=[n["p"] for n in nodes], T_K=[n["T"] for n in nodes],
                         liquid_kg=[n["liquid"] for n in nodes],
                         two_phase=[bool(n["two_phase"]) for n in nodes],
                         phase=[n["phase"] for n in nodes], evo5_index=k, injection_index=i0,
                         V_evc_m3=V_evc, p_exhaust_Pa=p_ex)
    except (ValueError, RuntimeError, ZeroDivisionError, OverflowError, ct.CanteraError) as exc:
        row.update(status="failed", reason=f"{type(exc).__name__}: {exc}")
    return dict(row=row, trace=trace)


def _task(task):
    return run_loop(*task)["row"]


HOT_DRY_VALIDATION = dict(
    label="hot-dry validation (Conklin & Szybist 2010, docs/research/02 refs 23/29)",
    fuel="CH3OH", cr=10.0, w=0.0, T_intake_K=360.0,
    key="CH3OH/CR=10/w=0/T_intake=360",
    note="Dry CR 10 point from the module 03 sweep, hot intake (360 K) so knock is not a binding "
         "constraint. SPEC item 2: 'hot-dry validation case ... or the dry CR 10 point'.",
    source="SPEC item 2 hot-dry validation")


def sweep(mode):
    return (QUICK_EVC_DEG, QUICK_WATER_MG) if mode == "quick" else (FULL_EVC_DEG, FULL_WATER_MG)


def build_tasks(ctx, mode, par=DEFAULTS, points=None):
    if points is not None:
        return [(ctx, p["EVC_deg"], p["water_mg"] * 1e-6, p["heat"], par) for p in points]
    evcs, waters = sweep(mode)
    return [(ctx, evc, mg * 1e-6, heat, par) for heat in HEAT_MODES for evc in evcs for mg in waters]


# ------------------------------------------------------------ input states
def synthetic_context(T_evo_K=1200.0, p_evo_Pa=5.0e5, cr=14.0, w=0.6, efficiency=0.40):
    """QUICK-MODE FALLBACK AND TEST FIXTURE ONLY: a labelled synthetic EVO state.

    CH4/air phi = 1, intake water w = 0.6, complete products (CO2, H2O, N2)
    at T_evo and p_evo in the SPEC section 6 engine at EVO = 140 CAD; the
    four-stroke work is efficiency * m_f * LHV. NOT Module 03 output.
    """
    fuel = "CH4"
    gas = fuels.load_mechanism(fuel)
    moles = fuels.mixture(fuel, 1.0, w)  # per mol fuel: CH4 1, O2 2, N2 7.52, H2O water
    c, h, _ = fuels.FUELS[fuel].atoms
    products = {"CO2": float(c), "H2O": h / 2.0 + moles["H2O"], "N2": moles["N2"]}
    mw = {k: float(gas.molecular_weights[gas.species_index(k)]) for k in (*products, fuel)}
    mass = {k: n * mw[k] for k, n in products.items()}
    total = sum(mass.values())
    eng = dict(DEFAULT_ENGINE, CR=float(cr))
    V = volume(eng["evo_deg"] * RAD, eng)
    gas.TPY = T_evo_K, p_evo_Pa, {k: v / total for k, v in mass.items()}
    m = float(gas.density_mass) * V
    m_f = m * mw[fuel] / total
    Q = m_f * fuels.lhv(fuel)
    return dict(
        eng, label="quick-fallback", synthetic=True, key=f"SYNTHETIC/{fuel}/CR={cr:g}/w={w:g}",
        source="SYNTHETIC fallback: complete CH4/air products, not Module 03", fuel=fuel,
        mechanism="gri30.yaml", T_evo_K=float(T_evo_K), p_evo_Pa=float(p_evo_Pa), V_evo_m3=V,
        gas_mass_evo_kg=m, liquid_water_evo_kg=0.0,
        composition={k: v / total for k, v in mass.items()}, fuel_mass_kg=m_f,
        intake_water_kg=m * moles["H2O"] * mw["H2O"] / total, fuel_energy_J=Q,
        four_stroke_work_J=efficiency * Q, upstream_mode=None, use_for_design=False,
        warning="SYNTHETIC exhaust state (quick fallback): demonstrates the software only; NOT FOR DESIGN",
        files=[], missing=[])


def _finite(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"Module 03 field {name} must be a finite number")
    return float(value)


def read_cycle(directory, mode, evo_key=None):
    """Module 03 design point and EVO state, from files only.

    --full: both files must exist and must not be quick-mode output.
    --quick: missing files select the labelled synthetic fallback.
    """
    d = Path(directory)
    paths = [d / "design_point.json", d / "evo_states.json"]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        if mode != "quick":
            raise FileNotFoundError("--full requires Module 03 outputs (run sims.03_engine_cycle --full "
                                    "first, or pass --cycle-dir): " + ", ".join(missing))
        return dict(synthetic_context(), missing=missing)
    design, evo = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
    if not isinstance(design, dict) or not isinstance(evo, dict):
        raise ValueError("Module 03 design_point.json and evo_states.json must be JSON objects")
    if mode == "full" and design.get("mode") == "quick":
        raise ValueError("--full refuses quick-mode Module 03 outputs (design_point.json mode = quick)")
    selection = "recommended"
    key = evo_key or design.get("recommended_evo_state_key")
    if evo_key:
        selection = "--evo-key"
    elif key is None:  # no feasible water-majority point: best eligible point overall
        best = [v.get("best_overall") for v in design.get("per_fuel", {}).values() if v.get("best_overall")]
        if not best:
            raise ValueError("Module 03 design_point.json has no selected design point")
        key = max(best, key=lambda r: r["gross_indicated_efficiency"])["key"]
        selection = "best_overall (no water-majority recommendation)"
    if key not in evo:
        raise KeyError(f"EVO state {key!r} not in evo_states.json")
    e, eng = evo[key], design["engine"]
    if e.get("composition_basis") != "mass_fraction" or not isinstance(e.get("composition"), dict):
        raise ValueError("evo_states.json composition must be mass fractions")
    ctx = dict(
        bore_m=_finite(eng["bore_m"], "bore_m"), stroke_m=_finite(eng["stroke_m"], "stroke_m"),
        rod_m=_finite(eng["rod_m"], "rod_m"), rpm=_finite(eng["rpm"], "rpm"),
        evo_deg=_finite(e["crank_angle_deg"], "crank_angle_deg"),
        p_ivc_Pa=_finite(eng["p_ivc_Pa"], "p_ivc_Pa"), CR=_finite(e["CR"], "CR"),
        label=mode, synthetic=False, key=key, selection=selection, source=f"Module 03 {d}",
        fuel=e["fuel"], mechanism=e["mechanism"], T_evo_K=_finite(e["T_K"], "T_K"),
        p_evo_Pa=_finite(e["p_Pa"], "p_Pa"), V_evo_m3=_finite(e["volume_m3"], "volume_m3"),
        gas_mass_evo_kg=_finite(e["gas_mass_kg"], "gas_mass_kg"),
        liquid_water_evo_kg=_finite(e.get("liquid_water_kg") or 0.0, "liquid_water_kg"),
        composition={str(k): _finite(v, "composition") for k, v in e["composition"].items()},
        fuel_mass_kg=_finite(e["fuel_mass_kg"], "fuel_mass_kg"),
        intake_water_kg=_finite(e["water_mass_kg"], "water_mass_kg"),
        fuel_energy_J=_finite(e["fuel_energy_J"], "fuel_energy_J"),
        four_stroke_work_J=_finite(e["indicated_work_J"], "indicated_work_J"),
        upstream_mode=design.get("mode"), use_for_design=bool(design.get("use_for_design")),
        upstream_synthetic_fits=bool(e.get("synthetic_fits", design.get("synthetic_fits"))),
        warning=design.get("warning"), mechanism_fallback=bool(e.get("mechanism_fallback")),
        files=[dict(path=str(p), sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths],
        missing=[])
    if abs(volume(ctx["evo_deg"] * RAD, ctx) / ctx["V_evo_m3"] - 1.0) > 1e-6:
        raise ValueError("Module 03 EVO volume is inconsistent with its engine geometry")
    if not ctx["four_stroke_work_J"] > 0.0 or not ctx["fuel_energy_J"] > 0.0:
        raise ValueError("Module 03 work and fuel energy must be positive")
    return ctx


# ------------------------------------------------------ selection/validation
def eligible(r, par=DEFAULTS):
    return (r["status"] == "computed" and r["peak_pressure_Pa"] <= par.peak_pressure_limit_Pa
            and abs(r["energy_closure_error_fraction"]) <= par.closure_tolerance)


POINT_KEYS = ("heat_transfer", "EVC_deg", "water_mg", "trapped_mass_kg", "trapped_fraction_of_EVO_mass",
              "T_EVC_K", "T_TDC_before_injection_K", "T_TDC_after_injection_K",
              "p_TDC_after_injection_Pa", "peak_pressure_Pa", "EVO5_deg", "p_EVO5_Pa", "T_EVO5_K",
              "extra_work_gross_J", "pump_work_J", "extra_work_net_J", "extra_work_pct_of_four_stroke",
              "efficiency_four_stroke", "efficiency_six_stroke", "efficiency_gain_abs",
              "steam_MEP_net_Pa", "trapped_enthalpy_J", "trapped_exergy_J", "exergy_bound_J",
              "extra_work_over_exergy_bound", "energy_closure_error_fraction", "condensed_kg",
              "max_liquid_kg", "two_phase_nodes", "combined_w", "combined_WFR")


def point(r):
    return None if r is None else {k: r[k] for k in POINT_KEYS}


def ledger(r):
    """Full energy ledger of one point (J per cycle)."""
    if r is None:
        return None
    keys = ("trapped_mass_kg", "T_EVC_K", "trapped_enthalpy_J", "trapped_exergy_J",
            "water_enthalpy_in_J", "water_enthalpy_above_tank_J", "pump_work_J",
            "recompression_work_J", "expansion_work_J", "loop_work_J",
            "exhaust_displacement_correction_J", "extra_work_gross_J", "extra_work_net_J",
            "wall_heat_loss_J", "wall_heat_gained_J", "charge_energy_change_J",
            "energy_closure_error_J", "energy_closure_error_fraction",
            "integrator_identity_error_fraction", "condensed_kg", "condensed_latent_heat_J",
            "exergy_bound_J", "four_stroke_work_J", "fuel_energy_J")
    out = {k: r[k] for k in keys}
    out["balance"] = ("m_w h_inj = W_loop + Q_wall + dU (EVC -> EVO5); W_extra,gross = W_loop - p_exh "
                      "(V_EVO5 - V_EVC); W_extra,net = W_extra,gross - W_pump; sources: trapped exhaust "
                      "energy (from fuel LHV in strokes 1-3), pump work, wall heat gained; water adds none")
    return out


def select(rows, ctx, par=DEFAULTS):
    """Best point per heat-transfer mode; the four-stroke (no injection) is the zero."""
    m_wi, m_f = ctx["intake_water_kg"], ctx["fuel_mass_kg"]
    out = {}
    for heat in HEAT_MODES:
        cand = [r for r in rows if r["heat_transfer"] == heat and eligible(r, par)]
        injected = [r for r in cand if r["water_kg"] > 0.0]
        best = max(injected, key=lambda r: r["extra_work_net_J"], default=None)
        gain = best is not None and best["extra_work_net_J"] > 0.0
        per_evc = {}
        for r in injected:
            k = f"EVC={r['EVC_deg']:g}"
            if k not in per_evc or r["extra_work_net_J"] > per_evc[k]["extra_work_net_J"]:
                per_evc[k] = r
        dry = [r for r in cand if r["water_kg"] == 0.0]
        slope = {}
        for d in dry:  # d W_extra / d m_water at small water (J per mg), per EVC
            wet = [r for r in injected if r["EVC_deg"] == d["EVC_deg"]]
            if wet:
                first = min(wet, key=lambda r: r["water_kg"])
                slope[f"EVC={d['EVC_deg']:g}"] = ((first["extra_work_net_J"] - d["extra_work_net_J"])
                                                  / first["water_mg"])
        out[heat] = dict(
            marginal_extra_work_J_per_mg=slope,
            injection_beneficial=bool(gain),
            optimum=point(best) if gain else dict(
                description="no injection: the four-stroke cycle is optimal (W_extra = 0)",
                extra_work_net_J=0.0, extra_work_pct_of_four_stroke=0.0, efficiency_gain_abs=0.0,
                water_mg=0.0, EVC_deg=None, combined_w=m_wi / (m_wi + m_f),
                combined_WFR=m_wi / m_f),
            best_injected=point(best), best_injected_ledger=ledger(best),
            best_injected_per_EVC={k: dict(water_mg=v["water_mg"], extra_work_net_J=v["extra_work_net_J"],
                                           extra_work_pct_of_four_stroke=v["extra_work_pct_of_four_stroke"])
                                   for k, v in per_evc.items()},
            zero_water_extra_work_J={f"EVC={r['EVC_deg']:g}": r["extra_work_net_J"] for r in dry},
            eligible_points=len(cand))
    return out


def design_points(design, ctx, par):
    """The six SPEC item 2 points: best dry, best overall and best water-majority for CH3OH and
    C2H5OH, plus the hot-dry validation case. Each is a (heat, EVC_deg, water_mg) probe."""
    out = []
    for fuel in ("CH3OH", "C2H5OH"):
        pf = design.get("per_fuel", {}).get(fuel)
        if not pf:
            continue
        for label, rec in (("best_dry", pf.get("best_dry")),
                           ("best_overall", pf.get("best_overall")),
                           ("water_majority", pf.get("water_majority"))):
            if not rec:
                continue
            out.append(dict(label=f"{fuel}/{label}", fuel=fuel, cr=rec["CR"], w=rec["w"],
                            T_intake_K=rec["T_intake_K"], key=rec["key"],
                            heat="adiabatic", EVC_deg=None, water_mg=None))
    out.append(dict(label="hot-dry validation", fuel=HOT_DRY_VALIDATION["fuel"],
                    cr=HOT_DRY_VALIDATION["cr"], w=HOT_DRY_VALIDATION["w"],
                    T_intake_K=HOT_DRY_VALIDATION["T_intake_K"], key=None,
                    heat="adiabatic", EVC_deg=None, water_mg=None))
    return out


def load_evo(directory, key, base_ctx):
    """Re-build the simulation context for a different Module 03 EVO state (same engine, different
    fuel/CR/w/T_intake). The design-point row for that key carries the full state."""
    evo = json.loads((Path(directory) / "evo_states.json").read_text(encoding="utf-8"))
    e = evo[key]
    return dict(base_ctx, key=key, fuel=e["fuel"], mechanism=e["mechanism"],
                T_evo_K=e["T_K"], p_evo_Pa=e["p_Pa"], V_evo_m3=e["volume_m3"],
                gas_mass_evo_kg=e["gas_mass_kg"], liquid_water_evo_kg=e.get("liquid_water_kg") or 0.0,
                composition={str(k): float(v) for k, v in e["composition"].items()},
                fuel_mass_kg=e["fuel_mass_kg"], intake_water_kg=e["water_mass_kg"],
                fuel_energy_J=e["fuel_energy_J"], four_stroke_work_J=e["indicated_work_J"],
                synthetic=False, label="design-point", selection="--design-points",
                use_for_design=True, upstream_mode=None,
                upstream_synthetic_fits=bool(e.get("synthetic_fits")),
                warning=None, mechanism_fallback=bool(e.get("mechanism_fallback")))


def run_design_points(design, ctx, par, directory):
    """Evaluate the item 2 points and return a table with the requested columns."""
    probes = design_points(design, ctx, par)
    rows = []
    for p in probes:
        loc = load_evo(directory, p["key"], ctx) if p["key"] else ctx
        evc = p["EVC_deg"] if p["EVC_deg"] is not None else loc["evo_deg"]
        water_mg = p["water_mg"] if p["water_mg"] is not None else 0.0
        r = run_loop(loc, evc, water_mg * 1e-6, p["heat"], par)
        row = r["row"]
        if row["status"] != "computed":
            rows.append(dict(label=p["label"], status="failed", reason=row["reason"]))
            continue
        rows.append(dict(
            label=p["label"], fuel=p["fuel"], key=p["key"], cr=p["cr"], w=p["w"],
            T_intake_K=p["T_intake_K"], EVC_deg=evc, heat=p["heat"], water_mg=water_mg,
            status="computed",
            extra_work_pct_of_four_stroke=row["extra_work_pct_of_four_stroke"],
            water_mg_per_cycle=row["water_mg"],
            combined_w=row["combined_w"],
            efficiency_four_stroke=row["efficiency_four_stroke"],
            efficiency_six_stroke=row["efficiency_six_stroke"],
            efficiency_gain_abs=row["efficiency_gain_abs"],
            peak_pressure_bar=row["peak_pressure_Pa"] / 1e5,
            steam_MEP_bar=row["steam_MEP_net_Pa"] / 1e5,
            energy_closure_error_fraction=row["energy_closure_error_fraction"]))
    return rows


def validate(rows, par=DEFAULTS):
    """In-run checks (tests/test_six_stroke.py is the unit validation)."""
    computed = [r for r in rows if r["status"] == "computed"]
    failed = [dict(heat=r["heat_transfer"], EVC_deg=r["EVC_deg"], water_mg=r["water_mg"],
                   reason=r["reason"]) for r in rows if r["status"] != "computed"]
    closure = max((abs(r["energy_closure_error_fraction"]) for r in computed), default=None)
    identity = max((abs(r["integrator_identity_error_fraction"]) for r in computed), default=None)
    closure_ok = closure is not None and closure <= par.closure_tolerance
    over_bound = [dict(heat=r["heat_transfer"], EVC_deg=r["EVC_deg"], water_mg=r["water_mg"],
                       W_net=r["extra_work_net_J"], bound=r["exergy_bound_J"])
                  for r in computed if r["extra_work_net_J"] > r["exergy_bound_J"]]
    zero = [r for r in computed if r["water_kg"] == 0.0]
    zero_err = max((abs(r["extra_work_net_J"]) / r["trapped_enthalpy_J"] for r in zero
                    if r["heat_transfer"] == "adiabatic"), default=None)
    zero_ok = zero_err is not None and zero_err <= par.zero_water_tolerance
    walls_ok = all(r["extra_work_net_J"] <= par.zero_water_tolerance * r["trapped_enthalpy_J"]
                   for r in zero if r["heat_transfer"] == "woschni")
    pump_ok = bool(computed) and all(
        r["extra_work_net_J"] == r["extra_work_gross_J"] - r["pump_work_J"]
        and ((r["pump_work_J"] > 0.0) == (r["water_kg"] > 0.0)) for r in computed)
    passed = (bool(computed) and not failed and closure_ok and not over_bound and zero_ok
              and walls_ok and pump_ok)
    return dict(
        passed=bool(passed), failed_points=failed,
        energy_closure_passed=bool(closure_ok), max_abs_energy_closure_error_fraction=closure,
        energy_closure_basis="fraction of trapped-exhaust sensible enthalpy (Cantera, vs 298.15 K)",
        energy_closure_tolerance_fraction=par.closure_tolerance,
        max_abs_integrator_identity_error_fraction=identity,
        exergy_bound_passed=not over_bound, points_over_exergy_bound=over_bound,
        max_extra_work_over_exergy_bound=max((r["extra_work_over_exergy_bound"] for r in computed
                                              if r["extra_work_over_exergy_bound"] is not None), default=None),
        zero_water_zero_work_passed=bool(zero_ok),
        max_abs_zero_water_extra_work_fraction_adiabatic=zero_err,
        zero_water_tolerance_fraction=par.zero_water_tolerance,
        woschni_zero_water_not_positive=bool(walls_ok), pump_work_subtracted=bool(pump_ok),
        energy_from_water="none: every W_extra,net <= trapped-exhaust exergy + water tank exergy + wall-heat exergy",
        points_with_condensation=sum(r["condensed_kg"] > 0.0 for r in computed),
        points_two_phase=sum(r["two_phase_nodes"] > 0 for r in computed),
        points_truncated_by_freezing=sum(bool(r["expansion_truncated_freezing"]) for r in computed),
        scope="In-run checks; tests/test_six_stroke.py on the server is the unit validation")


def literature_comparison(selection, ctx):
    """Compare with docs/research/02 section 4 (context only, not hard tests)."""
    Vd = displacement(ctx)
    out = dict(LITERATURE)
    for heat, sel in selection.items():
        best = sel["best_injected"]
        if best is None:
            continue
        mep = best["steam_MEP_net_Pa"] / 1e5
        opt = sel["optimum"]
        out[f"model_{heat}"] = dict(
            best_injected_steam_MEP_bar=mep,
            optimum_steam_MEP_bar=(opt["extra_work_net_J"] / Vd / 1e5),
            within_conklin_szybist_range=bool(0.75 <= mep <= 2.5),
            best_injected_extra_work_pct_of_four_stroke=best["extra_work_pct_of_four_stroke"],
            four_stroke_IMEP_bar=ctx["four_stroke_work_J"] / Vd / 1e5,
            six_stroke_cycle_IMEP_bar_at_optimum=(ctx["four_stroke_work_J"] + opt["extra_work_net_J"]) / Vd / 1e5,
            relative_IMEP_gain_at_optimum=opt["extra_work_net_J"] / ctx["four_stroke_work_J"],
            yang_relative_IMEP_gain=LITERATURE["yang_2023"]["relative_gain"])
    out["interpretation"] = (
        "Cold liquid injected at TDC must take q ~ 41 kJ/mol (latent heat from 300 K) plus c_v,w (T - 300 K) "
        "from the trapped gas, which lowers the gas p V by R q / c_v,gas per mole of water, more than the "
        "R T per mole the new vapour adds (q > c_v,gas T); the expansion line then lies below the "
        "recompression line (see marginal_extra_work_J_per_mg) unless heat from outside the "
        "trapped charge (external exhaust or coolant preheat, or hotter walls) feeds the water. The "
        "Conklin & Szybist MEP range and the Yang et al. gain (externally generated steam) include such "
        "heat; the SPEC configuration here (300 K liquid, trapped-exhaust heat only, walls at 450 K) "
        "does not, so a lower or non-positive steam MEP is the expected outcome, not a discrepancy.")
    return out


# -------------------------------------------------------------------- plots
def write_plots(out, rows, traces, ctx, mode):
    evcs = QUICK_EVC_DEG if mode == "quick" else PLOT_EVC_DEG
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))
    colors = plt.cm.viridis(np.linspace(0.0, 0.9, len(evcs)))
    for color, evc in zip(colors, evcs):
        for heat, style in (("adiabatic", "-"), ("woschni", "--")):
            pts = sorted((r for r in rows if r["status"] == "computed" and r["heat_transfer"] == heat
                          and abs(r["EVC_deg"] - evc) < 1e-9), key=lambda r: r["water_kg"])
            if not pts:
                continue
            x = [r["water_mg"] for r in pts]
            axes[0].plot(x, [r["extra_work_net_J"] for r in pts], style, color=color, marker="o", ms=3,
                         label=f"EVC {evc:g} CAD, {heat}")
            axes[1].plot(x, [r["extra_work_pct_of_four_stroke"] for r in pts], style, color=color,
                         marker="o", ms=3)
    for ax in axes:
        ax.axhline(0.0, color="k", lw=0.8)
        ax.set_xlabel("Injected water per cycle [mg]")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("Extra net work after pump work [J/cycle]")
    axes[1].set_ylabel("Extra net work [% of four-stroke work]")
    axes[0].legend(fontsize=6, ncol=2)
    note = " - SYNTHETIC EXHAUST STATE, NOT FOR DESIGN" if ctx["synthetic"] else ""
    fig.suptitle(f"Six-stroke steam loop, {ctx['key']}{note}", fontsize=9)
    io.save_fig(fig, out / "extra_work_vs_water.png")
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    p_ex = None
    for label, tr, style in traces:
        k = tr["evo5_index"]
        V = np.array(tr["V_m3"][:k + 1]) * 1e6
        p = np.array(tr["p_Pa"][:k + 1]) / 1e5
        p_ex = tr["p_exhaust_Pa"] / 1e5
        line, = ax.plot(V, p, style, lw=1.4, label=label)
        ax.plot([V[-1], V[-1]], [p[-1], p_ex], ":", color=line.get_color(), lw=1.0)
    if p_ex is not None:
        ax.plot([volume(TWO_PI, ctx) * 1e6, volume(math.pi, ctx) * 1e6], [p_ex, p_ex], "k:", lw=1.0,
                label="exhaust displacement at p_exh (strokes 4 and 6)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    for axis, ticks in ((ax.xaxis, (10, 20, 30, 50, 100, 200, 300, 500, 1000)),
                        (ax.yaxis, (0.5, 1, 2, 5, 10, 20, 50, 100, 200))):
        axis.set_major_locator(matplotlib.ticker.FixedLocator(ticks))
        axis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))
        axis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel("Cylinder volume [cm^3]")
    ax.set_ylabel("Cylinder pressure [bar]")
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=7)
    ax.set_title(f"Strokes 4-6: EVC -> TDC recompression, injection, stroke-5 expansion to EVO5{note}",
                 fontsize=8)
    io.save_fig(fig, out / "pv_strokes_5_6.png")
    plt.close(fig)


def plot_traces(ctx, selection, mode, par):
    """Traces of the best injected point (with its zero-water and Woschni twins) and,
    for a large trapped mass, the earliest EVC of the sweep with and without 30 mg."""
    best = selection["adiabatic"]["best_injected"] or selection["woschni"]["best_injected"]
    cases = []
    if best is not None:
        evc, mg = best["EVC_deg"], best["water_mg"]
        cases += [(evc, mg, "adiabatic", "-", "best injected point"),
                  (evc, 0.0, "adiabatic", "--", "no water (gas spring)"),
                  (evc, mg, "woschni", "-.", "Woschni walls")]
    early = sweep(mode)[0][0]
    cases += [(early, 30.0, "adiabatic", "-", "large trapped mass"),
              (early, 0.0, "adiabatic", "--", "large trapped mass, no water"),
              (early, 30.0, "woschni", "-.", "large trapped mass")]
    out = []
    for evc, mg, heat, style, what in cases:
        res = run_loop(ctx, evc, mg * 1e-6, heat, par, keep_trace=True)
        if res["trace"] is not None:
            out.append((f"EVC {evc:g} CAD, {mg:g} mg, {heat} ({what})", res["trace"], style))
    return out


# -------------------------------------------------------------- assumptions
def assumptions(par, ctx, mode, workers):
    result = fuels.fuel_assumptions()
    sources = {
        "p_exhaust_Pa": "Exhaust back pressure = Module 03 p_IVC (1 bar, WOT), so four-stroke pumping work is zero; also the Conklin & Szybist end-of-expansion limit (1 bar)",
        "dead_state_T_K": "Exergy dead state and sensible-energy zero: 298.15 K, the fuels.py LHV reference; dead-state pressure = p_exhaust_Pa",
        "water_T_K,injection_p_Pa": "Task brief / SPEC section 7: liquid water at 300 K and 100 bar injected at TDC",
        "tank_p_Pa": "Water tank at 1 atm; the pump raises it to injection_p_Pa",
        "pump_efficiency": "ASSUMPTION (no source): small high-pressure plunger pump incl. drive; shaft work = isentropic work / 0.6, losses rejected to ambient. Pump work is ~0.017 J per mg of water, so the choice barely moves W_extra",
        "wall_T_K": "Task brief / SPEC section 6: 450 K",
        "woschni_C,woschni_C1_closed,woschni_C1_exchange": "Woschni (1967), SAE 670931; Heywood (1988) eq. 12.19: C = 3.26, C1 = 2.28 compression/expansion, 6.18 gas exchange; no combustion (C2) term in the steam loop",
        "step_rad,quick_step_rad": "Fixed crank step: 0.5 CAD full, 1 CAD quick; the trapezoid-vs-midpoint closure error reports the discretisation error",
        "state_xtol_K": "Numerical: Brent temperature tolerance of the U(T, V) inversion",
        "closure_tolerance": "Task brief: ledger must close within 1 % of the trapped-exhaust enthalpy",
        "zero_water_tolerance": "Numerical: |W_extra| at zero water <= 0.2 % of the trapped-exhaust enthalpy (exact zero for a reversible gas spring; discretisation only)",
        "peak_pressure_limit_Pa": "SPEC section 6 design constraint (120 bar), applied to the steam loop",
    }
    result.update({
        "parameters": {"defaults": asdict(par), "sources": sources, "used_step_deg": par.step_rad / RAD,
                       "angles": "radians internally; outputs in CAD after firing TDC (gas-exchange TDC 360, stroke-5 BDC 540)"},
        "mode": {"value": mode, "sweep": dict(zip(("EVC_deg", "water_mg"), sweep("quick" if mode != "full" else "full"))),
                 "heat_transfer": list(HEAT_MODES)},
        "workers": {"value": workers, "rationale": "Spawned point tasks (io.ordered_map, chunksize 1); Cantera/CoolProp objects built inside each worker"},
        "upstream": {k: ctx.get(k) for k in ("key", "selection", "source", "fuel", "mechanism", "CR", "files",
                                            "missing", "upstream_mode", "use_for_design", "warning",
                                            "upstream_synthetic_fits", "mechanism_fallback", "synthetic")},
        "four_stroke_reference": {"value": "Module 03 gross indicated work IVC -> EVO and fuel energy m_f LHV of the same cycle; the six-stroke adds strokes 5-6 with the same fuel charge",
                                  "four_stroke_work_J": ctx["four_stroke_work_J"], "fuel_energy_J": ctx["fuel_energy_J"],
                                  "intake_water_kg": ctx["intake_water_kg"], "fuel_mass_kg": ctx["fuel_mass_kg"]},
        "extra_work_definition": {"value": "W_extra,net = integral_EVC^EVO5 (p - p_exh) dV - W_pump; relative to the four-stroke with the same fuel; gas-exchange work cancels elsewhere",
                                  "efficiency_gain": "W_extra,net / (m_f LHV): fuel energy unchanged",
                                  "steam_MEP": "W_extra,net / V_d (per six-stroke cycle)"},
        "evo5_policy": {"value": "Stroke-5 exhaust valve opens at the expansion node that maximises W_extra (where p falls to p_exh, else at BDC)",
                        "rationale": "dW_extra/dV_EVO5 = p - p_exh; a fixed cam would be timed for the design point"},
        "blowdown_model": {"value": "Instantaneous, adiabatic, isentropic blowdown at EVO of the gas that stays (Cantera SP, frozen composition); displacement exhaust at p_exh",
                           "source": "Standard ideal-cycle exhaust model, Heywood (1988) section 5.4",
                           "limitation": "Valve flow, pressure waves and blowdown heat transfer not modelled; liquid water present at EVO (Module 03 liquid_water_kg) is assumed to leave in blowdown"},
        "thermodynamics": {"value": "Dalton mixture in the full volume: dry exhaust (EVO species except H2O) frozen ideal gas from Cantera; all H2O (exhaust + injected) real fluid from CoolProp IAPWS-95 in phase equilibrium (lever rule below T_crit when m_w/V > rho_v,sat(T))",
                           "source": "Cantera species thermo (mechanism of the Module 03 point); CoolProp IAPWS-95, Wagner & Pruss (2002)",
                           "condensation": "Checked at every node; two-phase water sits at p_sat(T) with its liquid mass and latent heat in u; liquid volume counted for water only (dry gas sees the whole volume); the vapour-liquid split is equilibrium (no droplet kinetics)",
                           "extrapolation": "IAPWS-95 is used above 2000 K (CoolProp Tmax) where trapped exhaust is hottest at TDC; the IAPWS release states reasonable extrapolation to 5000 K",
                           "injection": "Instantaneous adiabatic constant-volume mixing at TDC to equilibrium (optimistic: no evaporation delay)"},
        "heat_transfer": {"value": "adiabatic, or Woschni (motored form) to walls at 450 K during stroke-4 displacement and the closed steam loop",
                          "limitation": "No spray/wall-film impingement; Woschni was correlated for combusting/motored dry gas"},
        "pump_model": {"value": "CoolProp isentropic compression 1 atm -> 100 bar of 300 K liquid; shaft work w_s/eta; injected at the isentropic outlet state"},
        "energy_ledger": {"value": "m_w h_inj = W_loop + Q_wall + [U(EVO5) - U(EVC)] (EVC -> EVO5), re-integrated by the trapezoid rule over node states with U re-evaluated from (T, V)",
                          "normalisation": "closure error / trapped-exhaust sensible enthalpy (Cantera, frozen composition, vs 298.15 K)",
                          "sources_of_work": "trapped exhaust energy (paid by fuel LHV in strokes 1-3), pump work, heat from 450 K walls when the charge is colder; water has zero heating value"},
        "exergy_bound": {"value": "W_extra,net <= X_trap + X_water,tank + (1 - T0/T_wall) Q_wall,gained",
                         "X_trap": "Cantera thermo-mechanical exergy of the trapped exhaust at EVC, frozen composition, dead state (298.15 K, p_exh); chemical, mixing and exhaust-water condensation exergy excluded (makes the bound stricter)"},
        "not_modelled": ["water preheating by external exhaust/coolant heat exchangers (Conklin & Szybist patent: ~100 C water)",
                         "evaporation and condensation kinetics, wall films", "valve flow losses and residual-gas change for the next intake",
                         "friction of the extra two strokes", "power density: one power cycle per 3 revolutions"],
        "literature": LITERATURE,
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


def write_summary(out_dir, mode, settings, key_results, checks, runtime_s):
    """SPEC section 3 summary; 'quick-fallback' (task brief) is not in io's {quick, full}."""
    if mode in {"quick", "full"}:
        return io.write_summary(out_dir, MODULE, VERSION, mode, clean_json(settings),
                                clean_json(key_results), clean_json(checks), runtime_s)
    if mode != "quick-fallback":
        raise ValueError("mode must be quick, full or quick-fallback")
    payload = dict(module=MODULE, version=VERSION, git_sha=io.git_sha(), mode=mode,
                   assumptions=clean_json(settings), key_results=clean_json(key_results),
                   validation=clean_json(checks), runtime_s=runtime_s)
    if set(payload) != io.SUMMARY_KEYS:
        raise RuntimeError("summary keys drifted from SPEC section 3")
    path = Path(out_dir) / "summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return path


def main(argv=None):
    start = time.perf_counter()
    parser = io.argument_parser(MODULE)
    parser.add_argument("--cycle-dir", type=Path, default=Path("results") / "03_engine_cycle",
                        help="Directory with Module 03 design_point.json and evo_states.json")
    parser.add_argument("--evo-key", default=None,
                        help="Use this evo_states.json key instead of the Module 03 recommendation")
    parser.add_argument("--design-points", action="store_true",
                        help="SPEC item 2: evaluate the six-stroke at the real Module 03 design "
                             "points (best dry/overall/water-majority for CH3OH and C2H5OH, plus the "
                             "hot-dry validation case) and write six_stroke_design_points.csv")
    args = parser.parse_args(None if argv is None else list(map(str, argv)))
    ctx = read_cycle(args.cycle_dir, args.mode, args.evo_key)  # --full: raises if missing
    label = "quick-fallback" if ctx["synthetic"] else args.mode
    par = replace(DEFAULTS, step_rad=DEFAULTS.quick_step_rad) if args.mode == "quick" else DEFAULTS
    args.out.mkdir(parents=True, exist_ok=True)
    if args.design_points:
        if ctx["synthetic"]:
            raise SystemExit("--design-points requires real Module 03 outputs (not the quick fallback)")
        design = json.loads((args.cycle_dir / "design_point.json").read_text(encoding="utf-8"))
        dp = run_design_points(design, ctx, par, args.cycle_dir)
        io.write_csv(args.out / "six_stroke_design_points.csv", dp)
        summary = json.loads((args.cycle_dir / "summary.json").read_text(encoding="utf-8"))
        summary.setdefault("key_results", {}).setdefault("six_stroke_design_points", dp)
        io.write_json(args.cycle_dir / "summary.json", summary)
        print("six_stroke_design_points.csv written: " + ", ".join(
            f"{r['label']} = {r['extra_work_pct_of_four_stroke']:+.4f} %"
            for r in dp if r.get("status") == "computed"))
        return 0
    rows = io.ordered_map(_task, build_tasks(ctx, args.mode, par), args.workers, chunksize=1)
    selection = select(rows, ctx, par)
    checks = validate(rows, par)
    io.write_csv(args.out / "six_stroke_sweep.csv", rows)
    write_plots(args.out, rows, plot_traces(ctx, selection, args.mode, par), ctx, args.mode)
    adi, wos = selection["adiabatic"], selection["woschni"]
    key_results = dict(
        run_label=label, synthetic_exhaust_state=ctx["synthetic"], warning=ctx.get("warning"),
        design_point_key=ctx["key"], design_point_selection=ctx.get("selection"),
        four_stroke=dict(work_J=ctx["four_stroke_work_J"], fuel_energy_J=ctx["fuel_energy_J"],
                         efficiency=ctx["four_stroke_work_J"] / ctx["fuel_energy_J"],
                         IMEP_Pa=ctx["four_stroke_work_J"] / displacement(ctx),
                         EVO_T_K=ctx["T_evo_K"], EVO_p_Pa=ctx["p_evo_Pa"],
                         intake_water_kg=ctx["intake_water_kg"], fuel_mass_kg=ctx["fuel_mass_kg"]),
        injection_beneficial=dict(adiabatic=adi["injection_beneficial"], woschni=wos["injection_beneficial"]),
        optimum=dict(adiabatic=adi["optimum"], woschni=wos["optimum"]),
        best_injected=dict(adiabatic=adi["best_injected"], woschni=wos["best_injected"]),
        ledger_best_injected=dict(adiabatic=adi["best_injected_ledger"], woschni=wos["best_injected_ledger"]),
        best_injected_per_EVC=dict(adiabatic=adi["best_injected_per_EVC"], woschni=wos["best_injected_per_EVC"]),
        zero_water_extra_work_J=dict(adiabatic=adi["zero_water_extra_work_J"], woschni=wos["zero_water_extra_work_J"]),
        marginal_extra_work_J_per_mg=dict(adiabatic=adi["marginal_extra_work_J_per_mg"],
                                          woschni=wos["marginal_extra_work_J_per_mg"]),
        literature_comparison=literature_comparison(selection, ctx),
        max_abs_energy_closure_error_fraction=checks["max_abs_energy_closure_error_fraction"],
        computed_points=sum(r["status"] == "computed" for r in rows),
        failed_points=sum(r["status"] != "computed" for r in rows),
        energy_source="Trapped exhaust energy (already paid for by fuel LHV in strokes 1-3) plus pump work; water has zero heating value")
    settings = assumptions(par, ctx, label, args.workers)
    write_summary(args.out, label, settings, key_results, checks, time.perf_counter() - start)
    return 0 if checks["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
