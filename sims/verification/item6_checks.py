"""Verification-queue item 6 (2026-10-24, Grok Bot): analytic / limit-case checks and step-convergence (GCI) where it
applies, for modules 01, 04, 05, 06, 10, 11 and dual_temp. Each check states its reference and tolerance BEFORE it is
evaluated (constants below). The reference is independent of the module code path wherever possible: hand formulas,
NIST/JANAF/CODATA numbers, closed-form limits or an alternative formulation. Writes
results/verification/item6/checks.json. Status of everything here: code VERIFICATION only (not validation).

usage: python -m sims.verification.item6_checks [--skip-m04-steps]
"""
import importlib, json, math, sys, time
from dataclasses import replace
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "results" / "verification" / "item6"
R = {}


def chk(module, cid, desc, actual, reference, tol, kind="rel"):
    if kind == "rel":
        err = abs(actual / reference - 1.0) if reference != 0 else abs(actual)
    elif kind == "abs":
        err = abs(actual - reference)
    else:  # "bool"
        err = 0.0 if actual == reference else 1.0
    R.setdefault(module, []).append(dict(id=cid, check=desc, actual=actual, reference=reference, tol=tol,
                                         kind=kind, err=err, passed=bool(err <= tol)))


def gci(f1, f2, f3, r):
    """Roache GCI, fine solution f1, refinement ratio r (constant)."""
    e32, e21 = f3 - f2, f2 - f1
    if e21 == 0 or e32 == 0 or (e32 / e21) <= 0:
        return dict(p=None, gci_fine=None, note="non-monotone or exact")
    p = math.log(e32 / e21) / math.log(r)
    gci_f = 1.25 * abs(e21 / f1) / (r ** p - 1)
    return dict(p=p, gci_fine=gci_f, f_extrap=f1 + (f1 - f2) / (r ** p - 1))


# ------------------------------------------------------------------ Module 01 energy audit
def m01():
    m = importlib.import_module("sims.01_energy_audit.run")
    from sims.common import fuels
    k = m.hho_kit_ledger()
    # Faraday: n_H2 = I/(2F); M_H2 = 2.01588e-3 kg/mol (IUPAC); CODATA F = 96485.33212
    ref = 20.0 / (2 * 96485.33212) * 2.01588e-3
    chk("01", "F1", "H2 mass flow 20 A, Faraday law, IUPAC M_H2", k["hydrogen_mass_flow_kg_s"], ref, 1e-4)
    # LHVs vs NIST WebBook-derived values (Cantera thermo is the module path): H2 119.96, CH4 50.03,
    # CH3OH(l) 19.93, C2H5OH(l) 26.81 MJ/kg (NIST Chemistry WebBook combustion enthalpies, liquid alcohols).
    for f, ref in (("H2", 119.96e6), ("CH4", 50.03e6), ("CH3OH", 19.93e6), ("C2H5OH", 26.81e6)):
        chk("01", f"L-{f}", f"LHV {f} vs NIST-derived value", fuels.lhv(f), ref, 0.01)
    chk("01", "L-H2O", "water LHV is exactly 0 (limit)", fuels.lhv("H2O"), 0.0, 1.0, "abs")
    # Monte Carlo: mean of product of independent uniforms = product of means (analytic)
    _, g = m.loop_gain_samples(200_000)
    mean_ref = np.prod([sum(r) / 2 for r in (m.ENGINE_RANGE, m.ALTERNATOR_RANGE, m.ELECTROLYSER_RANGE)])
    # E[X^2] for U(a,b) = (a^2+ab+b^2)/3 -> analytic variance of the product
    ex2 = np.prod([(a * a + a * b + b * b) / 3 for a, b in (m.ENGINE_RANGE, m.ALTERNATOR_RANGE, m.ELECTROLYSER_RANGE)])
    se = math.sqrt((ex2 - mean_ref ** 2) / len(g))
    chk("01", "MC1", "loop gain MC mean vs analytic product of means (tol = 4 standard errors)", float(np.mean(g)),
        float(mean_ref), 4 * se, "abs")
    chk("01", "MC2", "loop gain sample max <= analytic max 0.45*0.75*0.80 = 0.27", float(np.max(g)) <= 0.27, True, 0, "bool")
    # Convergence of the MC mean: n = 2e4, 2e5 errors scale ~ n^-1/2 (report only, seed fixed)
    # Limit: ideal kit (all efficiencies 1, faradaic 1) -> net shaft = H2 LHV power - electrical power <= 0
    p = m.KitParameters(eta_engine=1.0, eta_alternator=1.0)
    kk = m.hho_kit_ledger(p)
    chk("01", "K1", "ideal-efficiency kit: net shaft = H2 LHV power - electric (closed form)", kk["net_shaft_effect_W"],
        kk["hydrogen_lhv_power_W"] - kk["electrical_input_W"], 1e-9)
    chk("01", "K2", "ideal-efficiency kit is still a net loss (no free energy)", kk["net_shaft_effect_W"] < 0, True, 0, "bool")
    # Thermoneutral limit: H2 LHV power / electric = LHV*M/(2F V) -> at V = LHV*M_H2/(2F) = 1.253 V ratio = 1
    v_lhv = fuels.lhv("H2") * 2.01588e-3 / (2 * 96485.33212)
    chk("01", "K3", "LHV voltage of H2 = 1.25 V (textbook 1.253 V)", v_lhv, 1.253, 0.005)


# ------------------------------------------------------------------ Module 05 aluminium / water
def m05():
    m = importlib.import_module("sims.05_aluminum_water.run")
    rows = {r.name: m.reaction_ledger(r) for r in m.REACTIONS}
    M = 26.9815385e-3
    # Hand Hess sums per mol Al (kJ/mol): gibbsite 3*285.83 - 1293.18 ; boehmite 2*285.83 - 996.10 ;
    # corundum (1.5*285.83 - 1675.69/2)
    for name, dh in (("gibbsite", 3 * 285.83 - 1293.18), ("boehmite", 2 * 285.83 - 996.10),
                     ("corundum", 1.5 * 285.83 - 1675.69 / 2)):
        chk("05", f"H-{name}", f"heat released {name}, hand Hess sum [J/kg Al]", rows[name]["heat_released_J_kg_Al"],
            -dh * 1e3 / M, 1e-6)
    chk("05", "Y1", "H2 yield 1.5 mol/mol Al = 0.11207 kg/kg Al", rows["gibbsite"]["hydrogen_kg_per_kg_Al"],
        1.5 * 2.01588e-3 / M, 1e-4)
    # Literature: Al + water total (heat + H2 HHV) ~ 31 MJ/kg Al, heat alone 15-16 MJ/kg (e.g. Shkolnikov et al.,
    # Renew. Sust. Energy Rev. 15 (2011) 4611); check heat within 15-16.5 MJ/kg for all products
    for name in rows:
        chk("05", f"Lit-{name}", f"{name} heat inside literature band 15.0-16.5 MJ/kg Al",
            15.0e6 <= rows[name]["heat_released_J_kg_Al"] <= 16.5e6, True, 0, "bool")
    chk("05", "Z1", "zero aluminium -> zero energy (limit)", m.batch_energy(m.REACTIONS[0], 0.0, 1.0), 0.0, 0.0, "abs")
    e1 = m.batch_energy(m.REACTIONS[0], 1.0, 100.0)
    chk("05", "Z2", "excess water: energy = 1 kg Al x total ledger (Al-limited)", e1,
        rows["gibbsite"]["total_energy_J_kg_Al"], 1e-12)
    for name, r in rows.items():
        chk("05", f"C-{name}", f"Hess closure {name} (module identity)", r["closure_relative_error"], 0.0, 1e-6, "abs")


# ------------------------------------------------------------------ Module 06 carburettor
def m06():
    m = importlib.import_module("sims.06_carburetor.run")
    par, g = m.DEFAULTS, 1.4
    rho0 = par.ambient_Pa / (m.R_AIR * par.tank_T_K)
    Ts = par.tank_T_K * 2 / (g + 1)
    rhos = rho0 * (2 / (g + 1)) ** (1 / (g - 1))
    ref = par.venturi_Cd * rhos * math.sqrt(g * m.R_AIR * Ts)
    chk("06", "N1", "choked flux = Cd rho* a* (independent isentropic-relation form)", m.mass_flux(1.0), ref, 1e-10)
    d = 0.02
    mdot = 0.5 * m.area(d) * m.mass_flux(1.0)
    st = m.venturi_state(mdot, d)
    chk("06", "N2", "venturi mass conservation: Cd A rho V = mdot", par.venturi_Cd * m.area(d) * st["density_kg_m3"]
        * st["velocity_m_s"], mdot, 1e-6)
    chk("06", "N3", "venturi stagnation enthalpy: T + V^2/(2cp) = T0",
        st["pressure_Pa"] / (m.R_AIR * st["density_kg_m3"]) + st["velocity_m_s"] ** 2 / (2 * g * m.R_AIR / (g - 1)),
        par.tank_T_K, 1e-9)
    inviscid = dict(m.LIQUIDS["fuel"], viscosity_Pa_s=1e-15)
    dj, dp = 1.0e-3, 2000.0
    chk("06", "J1", "jet mu->0 limit = Bernoulli Cd A sqrt(2 rho dp)", m.jet_flow(dj, dp, inviscid),
        par.jet_Cd_inviscid * m.area(dj) * math.sqrt(2 * 785.0 * dp), 1e-6)
    visc = dict(m.LIQUIDS["fuel"], viscosity_Pa_s=50.0)
    chk("06", "J2", "jet viscous limit = Hagen-Poiseuille pi rho d^4 dp/(128 mu L)", m.jet_flow(dj, dp, visc),
        math.pi * 785.0 * dj ** 4 * dp / (128 * 50.0 * par.jet_length_m), 1e-3)
    liq = m.LIQUIDS["fuel"]
    q = m.jet_flow(dj, dp, liq)
    a = 1 / (2 * 785.0 * par.jet_Cd_inviscid ** 2 * m.area(dj) ** 2)
    b = 128 * liq["viscosity_Pa_s"] * par.jet_length_m / (math.pi * 785.0 * dj ** 4)
    chk("06", "J3", "jet residual: a mdot^2 + b mdot = dp", a * q * q + b * q, dp, 1e-10)
    chk("06", "J4", "float head >= signal -> zero flow (limit)", m.jet_flow(dj, 785.0 * 9.80665 * 0.01, liq, 0.0101), 0.0,
        0.0, "abs")
    dsz = m.size_jet(1e-4, 2000.0, liq, 0.0)
    chk("06", "J5", "sized jet (0.01 mm drill rounding) delivers requested flow within rounding",
        m.jet_flow(dsz, 2000.0, liq), 1e-4, 0.03)
    ev = m.evaporation(50e-6, m.LIQUIDS["water"], 2.437e6, 400.0)
    B = par.gas_cp_J_kg_K * (400 - par.droplet_surface_T_K) / 2.437e6
    kref = 8 * par.gas_conductivity_W_m_K / (996.5 * par.gas_cp_J_kg_K) * math.log(1 + B)
    chk("06", "E1", "d2-law lifetime = D0^2/K, K = 8k ln(1+B)/(rho_l cp)", ev["evaporation_time_s"], (50e-6) ** 2 / kref, 1e-12)
    chk("06", "V1", "WFR valve: fully open at 15 kPa, closed at 25 kPa, linear midpoint 0.5",
        (m.valve_opening(15000.0), m.valve_opening(25000.0), m.valve_opening(20000.0)) == (1, 0, 0.5), True, 0, "bool")


# ------------------------------------------------------------------ Module 10 QD burn
def m10():
    m = importlib.import_module("sims.10_qd_burn.run")
    par = m.DEFAULTS
    chk("10", "Q1", "calibration point: CH3OH CR10 w0 S_L 0.72099 -> 25.0 CAD (Module 03 CA10-90)",
        m.estimate_burn_duration(10.0, 0.7209888530581408), 25.0, 1e-6)
    # hand formula, m_fuel = 0: CAD = C * lambda/S_L * rpm/60*360
    th = -math.pi / 2
    up = m.C_T * 2 * par.stroke_m * par.rpm / 60
    Li = m.C_L * m.M03.volume(th, 10.0, par) / (math.pi * par.bore_m ** 2 / 4)
    lam = m.C_LAM * math.sqrt(1.5e-5 * Li / up)
    chk("10", "Q2", "hand evaluation of the Tabaczynski chain at CR 16, S_L 0.5", m.estimate_burn_duration(16.0, 0.5),
        m.CALIBRATION * (lam * (math.sqrt(m.M03.volume(th, 16.0, par) / m.M03.volume(th, 10.0, par)))) / 0.5
        * par.rpm / 60 * 360, 1e-9)
    chk("10", "Q3", "scaling: duration proportional to 1/S_L (m_fuel = 0)",
        m.estimate_burn_duration(10.0, 0.36) / m.estimate_burn_duration(10.0, 0.72), 2.0, 1e-12)
    par2 = replace(par, rpm=2 * par.rpm)
    chk("10", "Q4", "scaling: duration_CAD proportional to rpm^0.5 (u' ~ rpm, lambda ~ rpm^-0.5)",
        m.estimate_burn_duration(10.0, 0.72, par2) / m.estimate_burn_duration(10.0, 0.72), math.sqrt(2), 1e-12)
    chk("10", "Q5", "flame area pi B^2 xb^(2/3) (docstring) == code 4 A_bore xb^(2/3)", m.flame_area(0, 10, par, 0.5),
        math.pi * par.bore_m ** 2 * 0.5 ** (2 / 3), 1e-12)
    chk("10", "Q6", "S_L -> 0 limit: burn-up time infinite", math.isinf(m.burn_up_time(1e-4, 0.0)), True, 0, "bool")
    M3 = m.M03
    ca50, dur = math.radians(8.0), math.radians(25.0)
    a10, a90 = M3._qd_burn_angle(0.1, ca50, dur, par), M3._qd_burn_angle(0.9, ca50, dur, par)
    chk("10", "Q7", "Module 03 QD ramp: CA90 - CA10 = duration", a90 - a10, dur, 1e-12)
    chk("10", "Q8", "Module 03 QD ramp: x(CA50) = 0.5", M3._qd_burn(ca50, ca50, dur, par), 0.5, 1e-12)


# ------------------------------------------------------------------ Module 11 spray flame
def m11():
    M = importlib.import_module("sims.11_spray_flame.model")
    st = M.State(T_K=700.0, p_Pa=30e5, rho_g=14.0, cp_g=1200.0, alpha=3.0e-6, T_ad_K=2400.0, rho_F=650.0, B=2.0,
                 h_fg_w=2.0e6, SL_gas=1.2)
    s0 = M.spray_point(st, 0.0, 0.0, 30e-6)
    chk("11", "S1", "no liquid: S_BL = S_L exactly (tau_e = 0)", s0["S_BL_m_s"], st.SL_gas, 1e-12)
    dq = M.DEF.C_Q * st.alpha / st.SL_gas
    chk("11", "S2", "no liquid: MIE = cp rho dT_ad pi/6 (C_Q alpha/S_L)^3", s0["MIE_J"],
        st.cp_g * st.rho_g * (st.T_ad_K - st.T_K) * math.pi / 6 * dq ** 3, 1e-12)
    chk("11", "S3", "heat-sink factor = 1 at zero sink", M.heat_sink_factor(0.0, 2400.0), 1.0, 0.0, "abs")
    chk("11", "S4", "Zeldovich factor exp(-E/2R (1/T2 - 1/Tad)) at 100 K sink", M.heat_sink_factor(100.0, 2400.0),
        math.exp(-1.25e5 / (2 * 8.314462618) * (1 / 2300.0 - 1 / 2400.0)), 1e-12)
    chk("11", "S5", "Metghalchi-Keck ratio = 1 at phi = 1 and floored at 0 when non-flammable",
        (M.mk_phi_ratio(1.0), M.mk_phi_ratio(0.0)) == (1.0, 0.0), True, 0, "bool")
    chk("11", "S6", "S_L(T0,p0) = S_L0 (power-law identity)", M.SL_at_state(0.5, 400.0, 101325.0), 0.5, 1e-15)
    # closed-form inverse of the MIE criterion vs the module bisection (step-convergence analogue)
    f, E = 0.5, 0.050
    dq_t = (6 * E / (math.pi * st.cp_g * st.rho_g * (st.T_ad_K - st.T_K))) ** (1 / 3)
    D_ref = math.sqrt((dq_t ** 2 - dq ** 2) * st.rho_g * M.DEF.phi * math.log1p(st.B) / (f * st.rho_F))
    D_mod = M.max_smd(st, f, 0.0)["D_max_MIE_50mJ_m"]
    chk("11", "S7", "max SMD for MIE = 50 mJ: bisection vs closed-form inverse", D_mod, D_ref, 1e-9)
    sizes = [M.spray_point(st, 0.5, 0.0, D)["MIE_J"] for D in (10e-6, 30e-6, 60e-6, 120e-6)]
    chk("11", "S8", "MIE monotone increasing in SMD", all(np.diff(sizes) > 0), True, 0, "bool")


# ------------------------------------------------------------------ dual_temp
def dualT():
    from sims.dual_temp.regimes import NORMAL, HOT
    chk("dual_temp", "R1", "normal coolant 90 C = 363.15 K (MAHLE/VW SSP 222 85-95 C band)", NORMAL["coolant_K"], 363.15, 0, "abs")
    chk("dual_temp", "R2", "hot coolant 115 C = 388.15 K (inside 95-110 C mapped + pressurised margin; SAE 960271)",
        HOT["coolant_K"], 388.15, 0, "abs")
    chk("dual_temp", "R3", "port wall = coolant in both regimes (stated assumption)",
        (NORMAL["port_wall_K"] == NORMAL["coolant_K"]) and (HOT["port_wall_K"] == HOT["coolant_K"]), True, 0, "bool")
    chk("dual_temp", "R4", "hot >= normal for coolant, chamber wall, port wall, max intake",
        all(HOT[k] >= NORMAL[k] for k in ("coolant_K", "chamber_wall_K", "port_wall_K"))
        and max(HOT["T_intake_K"]) > max(NORMAL["T_intake_K"]), True, 0, "bool")
    chk("dual_temp", "R5", "chamber wall in Heywood ch.12 gas-side band 400-600 K",
        all(400 <= x <= 600 for x in (NORMAL["chamber_wall_K"], HOT["chamber_wall_K"])), True, 0, "bool")
    # run_m03 patch reaches Module 03 default-argument functions (same DEFAULTS instance)
    m3 = importlib.import_module("sims.03_engine_cycle.run")
    old = m3.DEFAULTS.wall_T_K
    chk("dual_temp", "P0", "normal regime chamber wall equals unpatched Module 03 default (normal = baseline)",
        old, NORMAL["chamber_wall_K"], 0, "abs")
    object.__setattr__(m3.DEFAULTS, "wall_T_K", 520.0)
    import inspect
    seen = [fn for name, fn in inspect.getmembers(m3, inspect.isfunction)
            if any(p.default is m3.DEFAULTS for p in inspect.signature(fn).parameters.values())]
    ok = all(next(p.default for p in inspect.signature(fn).parameters.values() if p.default is m3.DEFAULTS).wall_T_K == 520.0
             for fn in seen)
    object.__setattr__(m3.DEFAULTS, "wall_T_K", old)
    chk("dual_temp", "P1", f"run_m03 wall_T patch seen by all {len(seen)} Module 03 functions defaulting to DEFAULTS",
        ok and len(seen) > 0, True, 0, "bool")
    pf = importlib.import_module("sims.dual_temp.port_film_wall_T")
    for alc, Tb in (("CH3OH", 337.69), ("C2H5OH", 351.44)):   # NIST WebBook normal boiling points (1 atm)
        Tb_mod = pf.bubble_T({alc: 1.0, "H2O": 0.0}, alc)
        # module uses P_PORT = 1.0e5 Pa, not 1 atm: Clausius-Clapeyron shift dT = R Tb^2/hfg * ln(101325/1e5)
        h = pf.hfg(alc, Tb) * pf.MW[alc]
        chk("dual_temp", f"B-{alc}", f"pure {alc} bubble point at 1.0 bar vs NIST Tb(1 atm) shifted by Clausius-Clapeyron",
            Tb_mod, Tb - 8.314462618 * Tb ** 2 / h * math.log(101325 / 1e5), 0.2, "abs")
    Tw = pf.bubble_T({"CH3OH": 0.0, "H2O": 1.0}, "CH3OH")
    chk("dual_temp", "B-H2O", "pure water bubble point at 1.0 bar = 372.76 K (IAPWS)", Tw, 372.76, 0.1, "abs")
    chk("dual_temp", "H-H2O", "water h_fg at 373.124 K = 2256.4 kJ/kg (IAPWS-95)", pf.hfg("H2O", 373.124), 2256.4e3, 1e-3)


# ------------------------------------------------------------------ Module 04 six-stroke
def m04(steps=True):
    six = importlib.import_module("sims.04_six_stroke.run")
    from CoolProp.CoolProp import PropsSI
    par = six.DEFAULTS
    pm = six.pump(1.0, par)
    v = 1 / PropsSI("Dmass", "T", 300.0, "P", par.tank_p_Pa, "Water")
    chk("04", "P1", "isentropic pump work ~ v dp (incompressible estimate, 0.5 %)", pm["w_isentropic"],
        v * (par.injection_p_Pa - par.tank_p_Pa), 5e-3)
    chk("04", "P2", "shaft work = w_s/eta_pump", pm["W_pump"], pm["w_isentropic"] / par.pump_efficiency, 1e-12)
    ctx = six.synthetic_context()
    vc = six.volume(six.TWO_PI, ctx)
    chk("04", "G1", "geometry V(BDC)/V(TDC) = CR", six.volume(3 * math.pi, ctx) / vc, ctx["CR"], 1e-12)
    out = {}
    if steps:
        for case in ((220.0, 10e-6, "adiabatic"), (260.0, 10e-6, "woschni")):
            vals = []
            for deg in (2.0, 1.0, 0.5):
                r = six.run_loop(ctx, case[0], case[1], case[2], replace(par, step_rad=deg * six.RAD))["row"]
                vals.append(r["extra_work_net_J"] if r["status"] == "computed" else None)
            key = f"EVC{case[0]:g}_{case[1]*1e6:g}mg_{case[2]}"
            if None not in vals:
                gg = gci(vals[2], vals[1], vals[0], 2.0)
                out[key] = dict(steps_deg=(2.0, 1.0, 0.5), extra_work_net_J=vals, **gg)
                chk("04", f"GCI-{key}", f"RK2 crank-step GCI (fine 0.5 deg) on net extra work, {key}: GCI_fine <= 1 %",
                    gg["gci_fine"] if gg["gci_fine"] is not None else abs(vals[2] - vals[1]) / abs(vals[2]), 0.0, 0.01, "abs")
            else:
                out[key] = dict(vals=vals, note="a step size failed")
                chk("04", f"GCI-{key}", "step study ran at all steps", False, True, 0, "bool")
    r0 = six.run_loop(ctx, 220.0, 0.0, "adiabatic", replace(par, step_rad=par.quick_step_rad))["row"]
    chk("04", "Z1", "zero water, adiabatic: |net extra work| <= 0.2 % of trapped enthalpy (reversible gas spring)",
        abs(r0["extra_work_net_J"]) / r0["trapped_enthalpy_J"], 0.0, 2e-3, "abs")
    chk("04", "Z2", "zero water: EVO5 at mirror angle 720 - EVC (+-8 deg)", r0["EVO5_deg"], 500.0, 8.0, "abs")
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    t0 = time.time()
    m01(); m05(); m06(); m10(); m11(); dualT()
    steps = m04(steps="--skip-m04-steps" not in argv)
    summary = {k: dict(n=len(v), passed=sum(c["passed"] for c in v), failed=[c["id"] for c in v if not c["passed"]])
               for k, v in R.items()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "checks.json").write_text(json.dumps(dict(date="2026-10-24", status="code VERIFICATION only; not validation",
                                                     summary=summary, checks=R, m04_step_study=steps,
                                                     runtime_s=time.time() - t0), indent=1, default=str))
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
