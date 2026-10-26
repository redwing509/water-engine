"""M03-CRN: independent 0-D closed-cycle SI engine on Cantera ReactorNet (CVODES).

Written from scratch for verification job reply-verification-20261024-1430 (V1); it does not
import or copy sims/03_engine_cycle. See ACCEPTANCE.md for what is shared (problem definition)
and what is independent (integrator, heat release, heat transfer, properties).

Model (IVC -> EVO, crank angle theta [rad] after firing TDC, time t = (theta - theta_IVC)/omega):
* One ExtensibleIdealGasReactor. Its volume follows the slider-crank law through a moving
  ct.Wall whose velocity is the piston velocity (pattern of Cantera's ic_engine.py example).
* Heat release: a second ct.Wall carries heat_flux(t) = -dQ_comb/dt, the Wiebe rate
  Q_avail * dx_b/dt (external heat source). Q_avail = eta_c m_fuel LHV_liquid.
  At the same rate, eta_c of the fuel and its stoichiometric O2 are converted to CO2 + H2O
  through species source terms whose sensible energy is removed from the temperature equation,
  so the chemical energy enters only through the Wiebe wall (no double counting).
* Dissociation of the products: finite-rate H/O/C/N kinetics (GRI-Mech 3.0 reactions that do not
  involve the fuel), absolute-energy consistent through Cantera's own energy equation.
* Wall heat: a third ct.Wall with heat_flux = h A (T - T_wall); Hohenberg (1979) by default,
  Woschni (1967) as a sensitivity, both implemented here.
* Liquid water: enters the gas as H2O(g) from a reservoir at T_water through a MassFlowController,
  with a latent-heat sink m_dot h_fg(T_water) (ct.Water()); schedule IVC -> -30 CAD (uniform),
  capped at saturation x_H2O p <= p_sat(T) by a stiff relaxation with time constant tau.
* Work, wall heat, released heat, latent heat, inflow enthalpy and conversion energy are extra
  CVODES states, so energy closure is checked without quadrature error.
"""

from dataclasses import dataclass, field, replace
import math

import cantera as ct
import numpy as np

RAD = math.pi / 180.0
T_REF = 298.15
R_U = ct.gas_constant  # J/(kmol K)

# Problem definition shared with Module 03 (SPEC section 6 test engine). Not solver code.
BORE, STROKE, ROD, RPM = 0.086, 0.086, 0.145, 2000.0
THETA_IVC, THETA_EVO = -180.0 * RAD, 140.0 * RAD
EVAP_END = -30.0 * RAD
WIEBE_A, WIEBE_M = 5.0, 2.0
ETA_C = 0.98
WATER_T = 300.0
AIR_N2_PER_O2 = 3.76
# NIST Chemistry WebBook SRD 69, standard vaporisation enthalpies at 298.15 K [J/mol].
H_VAP = {"CH3OH": 37600.0, "C2H5OH": 42300.0}
ATOMS = {"CH3OH": (1, 4, 1), "C2H5OH": (2, 6, 1)}

PRODUCT_SPECIES = ["H2", "H", "O", "O2", "OH", "H2O", "HO2", "H2O2", "CO", "CO2",
                   "N", "NO", "N2O", "NO2", "HNO", "N2"]


def build_gas(kinetics=True):
    """GRI-Mech 3.0 thermo (+ C2H5OH NASA-7 from nasa_gas.yaml); fuel-free product kinetics."""
    gri = {s.name: s for s in ct.Species.list_from_file("gri30.yaml")}
    nasa = {s.name: s for s in ct.Species.list_from_file("nasa_gas.yaml")}
    species = [gri[n] for n in PRODUCT_SPECIES] + [gri["CH3OH"], nasa["C2H5OH"]]
    names = set(PRODUCT_SPECIES)
    rxns = []
    if kinetics:
        ref = ct.Solution("gri30.yaml")
        for rx in ref.reactions():
            sp = set(rx.reactants) | set(rx.products)
            eff = set(getattr(rx.third_body, "efficiencies", {}) or {}) if rx.third_body else set()
            if sp <= names:
                if eff - names - {"CH3OH", "C2H5OH"}:
                    rx = ct.Reaction(equation=rx.equation, rate=rx.rate, third_body=_trim_tb(rx.third_body, names))
                rxns.append(rx)
    return ct.Solution(thermo="ideal-gas", kinetics="gas" if kinetics else "none",
                       species=species, reactions=rxns)


def _trim_tb(tb, names):
    eff = {k: v for k, v in tb.efficiencies.items() if k in names}
    return ct.ThirdBody(tb.name if tb.name != "M" else "M", efficiencies=eff,
                        default_efficiency=tb.default_efficiency)


def ideal_gas_constant_cp(gamma=1.4, R=287.0):
    """Single-species constant-cp ideal gas for the analytic Otto check."""
    mw = R_U / R
    cp = gamma / (gamma - 1.0) * R_U  # J/(kmol K)
    yaml = f"""
units: {{energy: J, quantity: kmol}}
elements:
- symbol: Xx
  atomic-weight: {mw}
phases:
- name: ideal
  thermo: ideal-gas
  elements: [Xx]
  species: [A]
  kinetics: none
  state: {{T: 300.0, P: 1.0e5}}
species:
- name: A
  composition: {{Xx: 1}}
  thermo:
    model: constant-cp
    T0: 298.15
    h0: 0.0
    s0: 0.0
    cp0: {cp}
    T-min: 50.0
    T-max: 10000.0
"""
    return ct.Solution(yaml=yaml)


# ------------------------------------------------------------------ geometry
def piston_area():
    return math.pi * BORE ** 2 / 4.0


def swept_volume():
    return piston_area() * STROKE


def theta_to_volume(theta, cr):
    a = STROKE / 2.0
    s = a * math.cos(theta) + math.sqrt(ROD ** 2 - (a * math.sin(theta)) ** 2)
    return swept_volume() / (cr - 1.0) + piston_area() * (ROD + a - s)


def dvolume_dtheta(theta):
    a = STROKE / 2.0
    root = math.sqrt(ROD ** 2 - (a * math.sin(theta)) ** 2)
    return piston_area() * a * math.sin(theta) * (1.0 + a * math.cos(theta) / root)


def heat_area(V):
    """Head + flat piston crown + liner exposed by the gas column V/A_p."""
    return 2.0 * piston_area() + math.pi * BORE * V / piston_area()


# ------------------------------------------------------------------ Wiebe
class Wiebe:
    """x_b = 1 - exp(-a ((theta - theta_s)/D)^(m+1)), parametrised by CA50 and 10-90 % duration."""

    def __init__(self, ca50, d1090, a=WIEBE_A, m=WIEBE_M):
        self.a, self.m = a, m
        q = lambda x: (math.log(1.0 / (1.0 - x)) / a) ** (1.0 / (m + 1.0))
        self.D = d1090 / (q(0.9) - q(0.1))
        self.start = ca50 - self.D * q(0.5)

    def x(self, theta):
        if theta <= self.start:
            return 0.0
        z = (theta - self.start) / self.D
        return 1.0 - math.exp(-self.a * z ** (self.m + 1.0))

    def dx(self, theta):
        """dx_b/dtheta [1/rad]."""
        if theta <= self.start:
            return 0.0
        z = (theta - self.start) / self.D
        return self.a * (self.m + 1.0) * z ** self.m * math.exp(-self.a * z ** (self.m + 1.0)) / self.D


# ------------------------------------------------------------------ cases
@dataclass
class Case:
    fuel: str
    cr: float
    T_ivc: float
    m_fuel: float
    m_air: float
    m_residual: float
    m_water: float
    e_intake: float
    ca50_deg: float
    d1090_deg: float
    wall_T: float = 450.0
    heat_transfer: str = "hohenberg"   # hohenberg | woschni | none
    kinetics: bool = True              # product dissociation kinetics
    max_steps: int = 500000            # CVODES steps per output interval
    rtol: float = 1e-9
    atol: float = 1e-17
    tau_evap_deg: float = 0.05
    sample_deg: float = 0.05
    label: str = ""
    meta: dict = field(default_factory=dict)
    # Retained-liquid coupling extension (2026-10-24, M03-CRN's own formulation).
    # "legacy": uniform schedule IVC -> -30 CAD (V1 engine, unchanged).
    # "coupled": Module 09 problem definition - evaporated fraction of the total
    # water rises linearly from f_ivc (IVC) to f_spark (spark_deg), capped at
    # saturation; from min(spark, Wiebe start) on, nothing evaporates from the
    # charge and the liquid then left enters the gas in proportion to the
    # burned mass, dm/dtheta = m_liq_spark * (dx_b/dtheta) / (1 - x_b,spark),
    # as H2O(g) inflow with the h_fg(T_water) sink (no saturation cap: it is
    # vaporised by the flame).
    evap_mode: str = "legacy"
    spark_deg: float = None
    f_ivc: float = None
    f_spark: float = None
    # Saturation-switch smoothing (2026-10-25, self-directed job grokbot-selfdirected-20261025-1410).
    # 0.0 = legacy hard switch: the scheduled feed-forward rate is added only while the charge is NOT
    # saturation-limited (target_sat >= target_sched). When the saturation ceiling and the schedule
    # cross with nearly equal slopes (cool, near-saturated charge early in compression), this makes
    # the RHS discontinuous and CVODES chatters on the switch until max_steps (Track B CH3OH/C2H5OH
    # normal chain failures). > 0: the feed-forward term is ramped linearly to zero over a band of
    # width sat_blend_frac * m_liq0 around the switch, so the RHS is continuous. Outside the band the
    # equations are identical to the legacy ones.
    sat_blend_frac: float = 0.0
    # Dry-evap baseline check (2026-10-25): fraction of the fuel whose latent heat was paid before IVC (intake air
    # or port wall). Its release is the vapour LHV (LHV_liquid + H_VAP); the efficiency denominator stays
    # m_fuel LHV_liquid. 0 = legacy (bit-for-bit).
    fuel_latent_credit: float = 0.0


def lhv_liquid(fuel, gas):
    """LHV [J/kg] of the liquid fuel at 298.15 K: own GRI/NASA reaction enthalpy, H2O(g) products."""
    c, h, o = ATOMS[fuel]
    gas.TP = T_REF, ct.one_atm
    hm = dict(zip(gas.species_names, gas.standard_enthalpies_RT * R_U * T_REF))  # J/kmol
    o2 = c + h / 4.0 - o / 2.0
    dh = c * hm["CO2"] + h / 2.0 * hm["H2O"] - hm[fuel] - o2 * hm["O2"]
    mw = gas.molecular_weights[gas.species_index(fuel)]
    return (-dh - H_VAP[fuel] * 1000.0) / mw


class Engine:
    """Runs one closed cycle IVC -> EVO for a Case; returns a result dict."""

    def __init__(self, case, gas=None):
        self.c = case
        self.gas = gas if gas is not None else build_gas(case.kinetics)
        self.water = ct.Water()

    # --------------------------------------------------------------- run
    def run(self):
        c, gas = self.c, self.gas
        omega = RPM * 2.0 * math.pi / 60.0
        self.omega = omega
        th = lambda t: THETA_IVC + omega * t
        tt = lambda theta: (theta - THETA_IVC) / omega
        idx = {n: gas.species_index(n) for n in gas.species_names}
        MW = gas.molecular_weights
        cnum, hnum, onum = ATOMS[c.fuel]
        mw_f = MW[idx[c.fuel]]
        # Trapped charge at IVC (boundary condition from the Module 03 row).
        masses = np.zeros(gas.n_species)
        n_f = c.m_fuel / mw_f
        n_o2_st = (cnum + hnum / 4.0 - onum / 2.0) * n_f
        n_air_o2 = c.m_air / (MW[idx["O2"]] + AIR_N2_PER_O2 * MW[idx["N2"]])
        masses[idx[c.fuel]] += c.m_fuel
        masses[idx["O2"]] += n_air_o2 * MW[idx["O2"]]
        masses[idx["N2"]] += n_air_o2 * AIR_N2_PER_O2 * MW[idx["N2"]]
        # Residual: complete products of the stoichiometric fresh charge (phi = 1), same mass basis.
        prod = np.zeros(gas.n_species)
        prod[idx["CO2"]] = cnum * MW[idx["CO2"]]
        prod[idx["H2O"]] = hnum / 2.0 * MW[idx["H2O"]]
        excess_o2 = n_air_o2 / n_f - (cnum + hnum / 4.0 - onum / 2.0)
        prod[idx["O2"]] = max(0.0, excess_o2) * MW[idx["O2"]]
        prod[idx["N2"]] = n_air_o2 / n_f * AIR_N2_PER_O2 * MW[idx["N2"]]
        if c.m_residual > 0:
            masses += prod / prod.sum() * c.m_residual
        masses[idx["H2O"]] += c.e_intake * c.m_water
        m0 = masses.sum()
        V0 = theta_to_volume(THETA_IVC, c.cr)
        gas.TDY = c.T_ivc, m0 / V0, masses / m0
        self.p_ivc = gas.P
        # Energies
        self.lhv = lhv_liquid(c.fuel, gas)
        self.Q_fuel = c.m_fuel * self.lhv
        Qa = ETA_C * (self.Q_fuel + c.fuel_latent_credit * c.m_fuel * H_VAP[c.fuel] * 1000.0 / mw_f)
        wb = Wiebe(c.ca50_deg * RAD, c.d1090_deg * RAD)
        self.wiebe = wb
        gas.TP = T_REF, ct.one_atm
        u_ref = (gas.standard_int_energies_RT * R_U * T_REF) / MW  # J/kg, formation-inclusive
        gas.TDY = c.T_ivc, m0 / V0, masses / m0
        # Conversion stoichiometry per kg fuel burned [kg_k / kg_fuel]
        nu = np.zeros(gas.n_species)
        nu[idx[c.fuel]] = -1.0
        nu[idx["O2"]] = -(cnum + hnum / 4.0 - onum / 2.0) * MW[idx["O2"]] / mw_f
        nu[idx["CO2"]] = cnum * MW[idx["CO2"]] / mw_f
        nu[idx["H2O"]] = hnum / 2.0 * MW[idx["H2O"]] / mw_f
        # Water
        self.water.TQ = WATER_T, 0.0
        h_l = self.water.h
        self.water.TQ = WATER_T, 1.0
        self.h_fg = self.water.h - h_l
        T_crit = self.water.critical_temperature
        mw_w = MW[idx["H2O"]]
        m_liq0 = (1.0 - c.e_intake) * c.m_water
        res_gas = ct.Solution(thermo="ideal-gas", species=gas.species())
        res_gas.TPX = WATER_T, 1.0e5, "H2O:1"
        h_in = res_gas.enthalpy_mass
        tau = c.tau_evap_deg * RAD / omega
        evap_rate_sched = m_liq0 / (EVAP_END - THETA_IVC) * omega  # kg/s while active
        self.anchor = None
        eng = self
        coupled = c.evap_mode == "coupled"
        if c.evap_mode not in ("legacy", "coupled"):
            raise ValueError(c.evap_mode)
        flame = dict(on=False, L=0.0, xs=0.0, m_ev=0.0)
        if coupled:
            theta_sp = c.spark_deg * RAD
            theta_freeze = min(theta_sp, wb.start)
            span = theta_sp - THETA_IVC
            # in-cylinder evaporation target [kg] beyond the intake vapour
            def target_cyl(theta):
                fr = c.f_spark if theta >= theta_sp else c.f_ivc + (c.f_spark - c.f_ivc) * (theta - THETA_IVC) / span
                return max(0.0, fr - c.e_intake) * c.m_water
            slope = max(0.0, (c.f_spark - c.f_ivc)) * c.m_water / span * omega

        def psat(T):
            if T >= T_crit:
                return math.inf
            self.water.TQ = T, 0.0
            return self.water.P

        def evap_mdot(t, r):
            if m_liq0 <= 0.0:
                return 0.0
            theta = th(t)
            if coupled and flame["on"]:
                return flame["L"] * wb.dx(theta) * omega / (1.0 - flame["xs"])
            m_ev = r.mass - m0  # evaporated so far (only inflow changes mass)
            left = m_liq0 - m_ev
            if left <= 0.0:
                return 0.0
            if coupled:
                target_sched = min(m_liq0, target_cyl(theta))
            else:
                frac = min(1.0, max(0.0, (theta - THETA_IVC) / (EVAP_END - THETA_IVC)))
                target_sched = frac * m_liq0
            ph = r.phase
            T, V = ph.T, r.volume
            ps = psat(T)
            if math.isinf(ps):
                target = target_sched
                sat_limited = False
            else:
                m_h2o_max = ps * V * mw_w / (R_U * T)
                m_h2o = ph.Y[idx["H2O"]] * r.mass
                target_sat = m_ev + (m_h2o_max - m_h2o)
                sat_limited = target_sat < target_sched
                target = min(target_sched, target_sat)
            rate = (target - m_ev) / tau
            if c.sat_blend_frac > 0.0:
                if math.isinf(ps):
                    sigma = 1.0
                else:
                    band = c.sat_blend_frac * m_liq0
                    sigma = min(1.0, max(0.0, 0.5 + (target_sat - target_sched) / band))
            else:
                sigma = 0.0 if sat_limited else 1.0
            if coupled:
                if theta < theta_sp and target_sched > 0.0:
                    rate += sigma * slope
            elif theta < EVAP_END:
                rate += sigma * evap_rate_sched
            return max(0.0, rate)

        def q_wall(t, r):
            if c.heat_transfer == "none":
                return 0.0
            ph = r.phase
            T, p, V = ph.T, ph.P, r.volume
            sp = 2.0 * STROKE * RPM / 60.0
            if c.heat_transfer == "hohenberg":
                # Hohenberg (1979), SAE 790825: h = 130 V^-0.06 p[bar]^0.8 T^-0.4 (S_p + 1.4)^0.8
                h = 130.0 * V ** -0.06 * (p / 1e5) ** 0.8 * T ** -0.4 * (sp + 1.4) ** 0.8
            elif c.heat_transfer == "woschni":
                # Woschni (1967), SAE 670931; Heywood (1988) eq. 12.19
                wgas = 2.28 * sp
                a = eng.anchor
                if a is not None:
                    p_mot = a["p"] * (a["V"] / V) ** a["gamma"]
                    wgas += 3.24e-3 * swept_volume() * eng.ref["T"] / (eng.ref["p"] * eng.ref["V"]) * max(0.0, p - p_mot)
                h = 3.26 * BORE ** -0.2 * (p / 1e3) ** 0.8 * T ** -0.55 * wgas ** 0.8
            else:
                raise ValueError(c.heat_transfer)
            return h * heat_area(V) * (T - c.wall_T)

        class Cyl(ct.ExtensibleIdealGasReactor):
            def after_initialize(self, t0):
                self.i0 = self.n_vars
                self.n_vars += 6  # W, Qw, Qc, Qlat, Hin, Econv

            def after_get_state(self, y):
                # keep the running integrals across net.reinitialize() (coupled mode)
                prev = getattr(self, "aux", None)
                y[self.i0:self.i0 + 6] = 0.0 if prev is None else prev

            def after_update_state(self, y):
                self.aux = np.array(y[self.i0:self.i0 + 6])

            def after_eval(self, t, LHS, RHS):
                theta = th(t)
                ph = self.phase
                T = ph.T
                mf_dot = ETA_C * c.m_fuel * wb.dx(theta) * omega  # kg fuel/s converted
                if mf_dot > 0.0:
                    mdot = nu * mf_dot
                    u = ph.standard_int_energies_RT * R_U * T / MW
                    RHS[3:3 + len(mdot)] += mdot
                    RHS[2] -= float(np.dot(mdot, u - u_ref))
                    RHS[self.i0 + 5] = float(np.dot(mdot, u_ref))
                else:
                    RHS[self.i0 + 5] = 0.0
                me = evap_mdot(t, self)
                RHS[2] -= me * eng.h_fg
                RHS[self.i0 + 0] = ph.P * dvolume_dtheta(theta) * omega
                RHS[self.i0 + 1] = q_wall(t, self)
                RHS[self.i0 + 2] = Qa * wb.dx(theta) * omega
                RHS[self.i0 + 3] = me * eng.h_fg
                RHS[self.i0 + 4] = me * h_in
                for k in range(6):
                    LHS[self.i0 + k] = 1.0

        r = Cyl(gas, clone=False)
        r.volume = V0
        r.chemistry_enabled = bool(c.kinetics)
        env = ct.Reservoir(ct.Solution(thermo="ideal-gas", species=gas.species()))
        res = ct.Reservoir(res_gas)
        piston = ct.Wall(r, env, A=piston_area())
        piston.velocity = lambda t: dvolume_dtheta(th(t)) * omega / piston_area()
        comb = ct.Wall(r, env, A=1.0)
        comb.heat_flux = lambda t: -Qa * wb.dx(th(t)) * omega
        htw = ct.Wall(r, env, A=1.0)
        htw.heat_flux = lambda t: q_wall(t, r)
        mfc = ct.MassFlowController(res, r)
        mfc.mass_flow_rate = lambda t: evap_mdot(t, r)
        net = ct.ReactorNet([r])
        net.rtol, net.atol = c.rtol, c.atol
        net.max_time_step = 1.0 * RAD / omega
        net.max_steps = c.max_steps
        self.ref = dict(T=c.T_ivc, p=self.p_ivc, V=V0)
        U0 = r.phase.int_energy_mass * r.mass

        # Output grid with break points at kinks (end of evaporation schedule, Wiebe start).
        bset = (EVAP_END, wb.start) if not coupled else (theta_freeze, wb.start, theta_sp)
        breaks = sorted(x for x in set(bset) if THETA_IVC < x < THETA_EVO)
        n = int(round((THETA_EVO - THETA_IVC) / (c.sample_deg * RAD)))
        base_grid = np.linspace(THETA_IVC, THETA_EVO, n + 1)[1:]
        if c.sat_blend_frac > 0.0:
            # (2026-10-25 fix, same switch as the saturation smoothing) a break point that lands within
            # floating-point distance of a sample point (e.g. spark at -41.0 CAD on the 0.05-CAD grid gives
            # -40.99999999999999) produced an output time ~1e-17 s after the previous one -> CVODES error -27
            # "tout too close to t0". Drop sample points closer than 1e-9 rad to a break (the break is kept).
            base_grid = [x for x in base_grid if all(abs(x - b) > 1e-9 for b in breaks)]
        grid = list(base_grid) + breaks
        grid = np.unique(np.array(grid))
        rec = []
        for theta in grid:
            net.advance(tt(theta))
            if coupled and not flame["on"] and theta >= theta_freeze - 1e-12:
                m_ev_s = r.mass - m0
                flame.update(on=True, L=max(0.0, m_liq0 - m_ev_s), xs=wb.x(theta), m_ev=m_ev_s,
                             theta=theta)
                if m_liq0 > 0.0:
                    net.reinitialize()  # RHS switches from spray schedule to flame vaporisation
            ph = r.phase
            if abs(theta - wb.start) < 1e-12 and self.anchor is None:
                self.anchor = dict(p=ph.P, V=r.volume, gamma=ph.cp_mass / ph.cv_mass, T=ph.T,
                                   s=ph.entropy_mass, Y=ph.Y.copy())
            rec.append((theta, ph.P, ph.T, r.volume, r.mass, ph.Y[idx["NO"]]))
        if self.anchor is None:  # Wiebe start before IVC (never at design points)
            raise RuntimeError("Wiebe start outside IVC..EVO")
        rec = np.array(rec)
        aux = r.aux
        W, Qw, Qc, Qlat, Hin, Econv = aux
        U1 = r.phase.int_energy_mass * r.mass
        closure = (U1 - U0 + W + Qw - Qc + Qlat - Hin - Econv) / self.Q_fuel
        wiebe_err = Qc / (Qa * (wb.x(THETA_EVO) - wb.x(THETA_IVC))) - 1.0
        # Peaks (quadratic refinement on the sample grid)
        def peak(col):
            i = int(np.argmax(rec[:, col]))
            if 0 < i < len(rec) - 1:
                y0, y1, y2 = rec[i - 1:i + 2, col]
                x0, x1, x2 = rec[i - 1:i + 2, 0]
                den = (y0 - 2 * y1 + y2)
                if den < 0:
                    d = 0.5 * (y0 - y2) / den
                    return y1 - 0.25 * (y0 - y2) * d, x1 + d * (x1 - x0)
            return rec[i, col], rec[i, 0]
        pmax, th_pmax = peak(1)
        Tmax, th_Tmax = peak(2)
        # End-gas (unburned, frozen composition at Wiebe start) isentrope to p_max: knock indicator.
        eg = ct.Solution(thermo="ideal-gas", species=gas.species())
        eg.TPY = self.anchor["T"], self.anchor["p"], self.anchor["Y"]
        eg.SP = eg.entropy_mass, pmax
        T_endgas = eg.T
        m_ev = r.mass - m0
        n_no = rec[-1, 5] * r.mass / gas.molecular_weights[idx["NO"]]  # kmol
        return dict(
            label=c.label, fuel=c.fuel, CR=c.cr, wall_T_K=c.wall_T, heat_transfer=c.heat_transfer,
            kinetics=c.kinetics, rtol=c.rtol, tau_evap_deg=c.tau_evap_deg,
            p_ivc_Pa=self.p_ivc, LHV_liquid_J_kg=self.lhv, Q_fuel_J=self.Q_fuel,
            efficiency=W / self.Q_fuel, IMEP_Pa=W / swept_volume(), work_J=W,
            p_max_Pa=pmax, theta_pmax_deg=th_pmax / RAD, T_max_K=Tmax, theta_Tmax_deg=th_Tmax / RAD,
            T_EVO_K=rec[-1, 2], p_EVO_Pa=rec[-1, 1], wall_heat_J=Qw, wall_heat_fraction=Qw / self.Q_fuel,
            heat_released_J=Qc, latent_J=Qlat, evaporated_kg=m_ev, liquid_left_kg=m_liq0 - m_ev,
            T_endgas_at_pmax_K=T_endgas, NO_mol_per_J_fuel_bulk=n_no * 1000.0 / self.Q_fuel,
            ca50_deg=c.ca50_deg, burn_10_90_deg=c.d1090_deg, wiebe_start_deg=wb.start / RAD,
            peak_burn_rate_J_per_deg=float(Qa * max(wb.dx(x) for x in grid) * RAD),
            energy_closure=closure, wiebe_integral_error=wiebe_err, meta=c.meta,
            evap_mode=c.evap_mode,
            liquid_at_spark_kg=flame["L"] if coupled else None,
            evaporated_fraction_spark=((c.e_intake * c.m_water + flame["m_ev"]) / c.m_water
                                       if coupled and c.m_water > 0 else None))


def run_case(case):
    return Engine(case).run()


def ideal_otto(cr, d1090_deg=1.0, gamma=1.4, R=287.0, q=1.5e6, rtol=1e-10, T0=300.0, p0=1e5):
    """Adiabatic constant-gamma cycle on the same ReactorNet + Wiebe heat-flux wall machinery."""
    gas = ideal_gas_constant_cp(gamma, R)
    omega = RPM * 2.0 * math.pi / 60.0
    th = lambda t: THETA_IVC + omega * t
    V0 = theta_to_volume(THETA_IVC, cr)
    gas.TP = T0, p0
    r = ct.IdealGasReactor(gas, clone=False)
    r.volume = V0
    m = r.mass
    Qa = m * q
    wb = Wiebe(0.0, d1090_deg * RAD)
    env = ct.Reservoir(ideal_gas_constant_cp(gamma, R))
    piston = ct.Wall(r, env, A=piston_area())
    piston.velocity = lambda t: dvolume_dtheta(th(t)) * omega / piston_area()
    comb = ct.Wall(r, env, A=1.0)
    comb.heat_flux = lambda t: -Qa * wb.dx(th(t)) * omega
    net = ct.ReactorNet([r])
    net.rtol, net.atol = rtol, 1e-20
    net.max_time_step = 0.05 * RAD / omega
    # Work by energy balance (adiabatic, constant cv): W = Q_in - m cv (T_end - T0) ... integrate p dV directly too
    thetas = np.linspace(THETA_IVC, math.pi, 72001)
    W = 0.0
    prev = None
    for theta in thetas:
        net.advance((theta - THETA_IVC) / omega)
        cur = (r.phase.P, r.volume)
        if prev is not None:
            W += 0.5 * (cur[0] + prev[0]) * (cur[1] - prev[1])
        prev = cur
    cv = R / (gamma - 1.0)
    Q_in = Qa * (wb.x(math.pi) - wb.x(THETA_IVC))
    W_energy = Q_in - m * cv * (r.phase.T - T0)
    analytic = 1.0 - cr ** (1.0 - gamma)
    return dict(CR=cr, burn_deg=d1090_deg, eta_energy=W_energy / Q_in, eta_trapezoid=W / Q_in,
                analytic=analytic, error=W_energy / Q_in - analytic)
