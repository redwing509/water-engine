"""SPEC section 5, SI units throughout; execute on the simulation server.

Water supplies no chemical energy. Premixed flames start with vapour already
present; the separate evaporation ledger accounts for making that vapour.
"""

from dataclasses import asdict, dataclass
import json
import math
import time

import cantera as ct
from CoolProp.CoolProp import PropsSI
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares

from sims.common import fuels, io


MODULE = "02_flame_chem"
VERSION = "1.0.0"
FUELS = ("H2", "CH4", "CH3OH", "C2H5OH")
PHIS = (0.8, 1.0)
WATER_FRACTIONS = tuple(i / 10 for i in range(10))
ADIABATIC_STATES = ((300.0, ct.one_atm), (400.0, ct.one_atm), (750.0, 25e5))
FLAME_STATES = ((400.0, ct.one_atm), (450.0, 5e5))
IGNITION_TEMPERATURES = tuple(float(t) for t in range(750, 1101, 50))
QUICK_FUELS = ("H2", "CH4")
QUICK_WATER = (0.0, 0.3)
QUICK_IGNITION_T = (900.0, 1000.0, 1100.0)
IGNITION_PRESSURE_PA = 40e5  # kept for the single-pressure API and tests
# WME-1 checklist item 1: knock-model pressure range.  Ignition delays are
# computed at 20, 40 and 80 bar so the pressure exponent n can be fitted.
IGNITION_PRESSURES_PA = (20e5, 40e5, 80e5)
QUICK_IGNITION_PRESSURES_PA = (40e5,)
R_J_MOL_K = ct.gas_constant / 1000.0

# Targets: SPEC section 10. Research CH4 targets: research note 02,
# references 38/40 (Stanford FFCM-1 fls_27a/fls_27c); model tolerances
# explicitly widened by the task contract, not experimental uncertainties.
TAD_TARGETS = {"CH4": (2225.0, 20.0), "H2": (2380.0, 25.0)}
FLAME_TARGETS = (("CH4", 1.0, 300.0, 0.34, 0.42),
                 ("H2", 1.0, 300.0, 1.9, 2.6),
                 ("CH4", 0.7, 298.0, 0.116, 0.196),
                 ("CH4", 1.3, 298.0, 0.197, 0.297))


@dataclass(frozen=True)
class Parameters:
    """Defaults and their sources/rationales are emitted by assumptions()."""

    water_T_K: float = 300.0
    intake_T_K: float = 320.0
    cooling_p_Pa: float = ct.one_atm
    dew_margin_K: float = 0.1
    flame_width_1atm_m: float = 0.03
    flame_width_5bar_m: float = 0.01
    refine_ratio: float = 3.0
    refine_slope: float = 0.07
    refine_curve: float = 0.14
    flame_stop_m_s: float = 0.02
    robust_m_s: float = 0.15
    marginal_m_s: float = 0.08
    ignition_max_time_s: float = 0.5
    ignition_min_rise_K: float = 200.0
    ignition_max_step_s: float = 0.005
    reactor_rtol: float = 1e-9
    reactor_atol: float = 1e-15
    ignition_pressure_exponent: float = 1.0
    fit_max_evaluations: int = 2000


DEFAULTS = Parameters()


def _gas(fuel, phi, w, T_K, p_Pa):
    """Construct in the calling process; no Cantera object crosses a pool."""
    gas = fuels.load_mechanism(fuel)
    gas.TPX = T_K, p_Pa, fuels.mixture(fuel, phi, w)
    return gas


def _record(fuel, phi, w, T_K, p_Pa):
    try:
        selected = fuels.select_mechanism(fuel)
        name, fallback = selected.name, selected.mechanism_fallback
    except fuels.MechanismUnavailable:
        name, fallback = "mechanisms/sandiego.yaml", True
    return dict(fuel=fuel, phi=phi, w=w, T_unburned_K=T_K, p_Pa=p_Pa,
                mechanism=name, mechanism_fallback=fallback)


def adiabatic_temperature(fuel, phi, w, T_K, p_Pa):
    row = _record(fuel, phi, w, T_K, p_Pa)
    row.update(T_ad_K=None, status="unavailable", reason="")
    try:
        gas = _gas(fuel, phi, w, T_K, p_Pa)
        gas.equilibrate("HP")
        row.update(T_ad_K=float(gas.T), status="computed")
    except fuels.MechanismUnavailable:
        row["reason"] = "Required fuel species or mechanism unavailable"
    except ct.CanteraError:
        row.update(status="solver_error", reason="Cantera HP equilibrium failed")
    return row


def evaporative_cooling(fuel, phi, w, parameters=DEFAULTS):
    """Frozen-cp, adiabatic mixing balance, per kg fuel, without chemistry.

    CoolProp Water (Wagner & Pruss 2002, IAPWS-95) supplies h_l(300 K,p),
    h_v,sat(300 K), h_fg and saturation pressure. Cantera supplies dry-charge
    cp and H2O(g) cp, frozen at the specified 320 K intake reference.
    Only enthalpy DIFFERENCES are combined across their reference systems.

    The formal complete-evaporation cooling demand is reported even when
    supersaturation makes it unrealizable. It is NOT a two-phase equilibrium
    prediction. No negative absolute temperature is exposed as a gas state.
    Below the water triple point, a conservative liquid-domain bound replaces
    an unsupported dew-point calculation, explicitly flagged in the output.
    """
    p = parameters
    row = _record(fuel, phi, w, p.intake_T_K, p.cooling_p_Pa)
    row.update(temperature_drop_K=None, final_all_vapour_T_K=None,
               dew_point_K=None, dew_point_status="not_evaluated",
               minimum_intake_T_K=None, minimum_is_conservative_bound=False,
               complete_evaporation_possible=False, water_partial_pressure_Pa=None,
               saturation_pressure_at_final_Pa=None, h_fg_J_kg=None,
               liquid_water_h_J_kg=None, reference_vapour_h_J_kg=None,
               dry_cp_J_kg_K=None, vapour_cp_J_kg_K=None,
               energy_residual_J_per_kg_fuel=None, status="unavailable", reason="")
    try:
        dry = _gas(fuel, phi, 0.0, p.intake_T_K, p.cooling_p_Pa)
        wet = _gas(fuel, phi, w, p.intake_T_K, p.cooling_p_Pa)
    except fuels.MechanismUnavailable:
        row["reason"] = "Required fuel species or mechanism unavailable"
        return row
    water_name = fuels.species_name(wet, "H2O")
    idx = wet.species_index(water_name)
    cp_v = float(wet.partial_molar_cp[idx] / wet.molecular_weights[idx])
    cp_d = float(dry.cp_mass)
    dry_mass = 1.0 / float(dry[fuels.species_name(dry, fuel)].Y[0])
    water_mass = w / (1.0 - w)
    h_l = float(PropsSI("Hmass", "T", p.water_T_K, "P", p.cooling_p_Pa, "Water"))
    h_vs = float(PropsSI("Hmass", "T", p.water_T_K, "Q", 1, "Water"))
    h_ls = float(PropsSI("Hmass", "T", p.water_T_K, "Q", 0, "Water"))
    # Solve md*cpd*(Ti-Tf) = mw*(hvs(Tw)-hl(Tw,p)+cpv*(Tf-Tw)).
    drop = water_mass * (h_vs - h_l + cp_v * (p.intake_T_K - p.water_T_K))
    drop /= dry_mass * cp_d + water_mass * cp_v
    final_T = p.intake_T_K - drop
    partial_p = float(wet[water_name].X[0] * p.cooling_p_Pa)
    triple_T = float(PropsSI("Ttriple", "Water"))
    triple_p = float(PropsSI("P", "T", triple_T, "Q", 0, "Water"))
    critical_T = float(PropsSI("Tcrit", "Water"))
    if water_mass == 0:
        dew, dew_status = None, "dry_charge_no_dew_point"
        minimum, feasible, conservative = None, True, False
    else:
        conservative = partial_p < triple_p
        dew = None if conservative else float(PropsSI("T", "P", partial_p, "Q", 1, "Water"))
        dew_status = "below_liquid_water_domain" if conservative else "computed"
        endpoint = (triple_T if conservative else dew) + p.dew_margin_K
        minimum = endpoint + water_mass * (h_vs - h_l + cp_v * (endpoint - p.water_T_K)) / (dry_mass * cp_d)
        feasible = final_T >= endpoint
    saturation_p = (float(PropsSI("P", "T", final_T, "Q", 0, "Water"))
                    if triple_T <= final_T < critical_T else None)
    if water_mass and saturation_p is not None:
        feasible = feasible and partial_p < saturation_p
    residual = dry_mass * cp_d * drop - water_mass * (h_vs - h_l + cp_v * (final_T - p.water_T_K))
    row.update(temperature_drop_K=float(drop),
               final_all_vapour_T_K=float(final_T) if feasible else None,
               dew_point_K=dew, dew_point_status=dew_status,
               minimum_intake_T_K=minimum, minimum_is_conservative_bound=conservative,
               complete_evaporation_possible=bool(feasible),
               water_partial_pressure_Pa=partial_p,
               saturation_pressure_at_final_Pa=saturation_p, h_fg_J_kg=h_vs - h_ls,
               liquid_water_h_J_kg=h_l, reference_vapour_h_J_kg=h_vs,
               dry_cp_J_kg_K=cp_d, vapour_cp_J_kg_K=cp_v,
               energy_residual_J_per_kg_fuel=float(residual), status="computed",
               reason="" if feasible else "Formal all-vapour cooling demand only; complete evaporation at the specified intake is infeasible")
    return row


def flame_speed_sweep(task):
    """Task = (fuel, phi, T, p, ascending water fractions); all scalars/tuples.

    A failed solve is a numerical no_flame, not proof of physical extinction.
    Remaining requested points are retained as no_flame/not_attempted.
    """
    fuel, phi, T_K, p_Pa, waters = task
    if tuple(waters) != tuple(sorted(set(waters))):
        raise ValueError("Water fractions must be unique and increasing")
    p = DEFAULTS
    rows, stopped, previous = [], "", None
    for w in waters:
        row = _record(fuel, phi, w, T_K, p_Pa)
        row.update(S_L_m_s=None, status="no_flame", reason=stopped,
                   attempted=False, grid_points=None)
        if not stopped:
            try:
                gas = _gas(fuel, phi, w, T_K, p_Pa)
                width = p.flame_width_1atm_m if p_Pa <= ct.one_atm else p.flame_width_5bar_m
                flame = ct.FreeFlame(gas, width=width)
                flame.transport_model = "mixture-averaged"
                flame.soret_enabled = False
                flame.set_refine_criteria(ratio=p.refine_ratio, slope=p.refine_slope,
                                          curve=p.refine_curve)
                if previous is not None:
                    flame.set_initial_guess(data=previous)
                row["attempted"] = True
                flame.solve(loglevel=0, auto=True)
                speed = float(flame.velocity[0])
                row.update(S_L_m_s=speed if math.isfinite(speed) else None,
                           grid_points=len(flame.grid))
                if not math.isfinite(speed) or speed < p.flame_stop_m_s:
                    row["reason"] = "Solved speed below propagation cutoff or nonfinite"
                    stopped = "Not attempted after earlier propagation cutoff"
                else:
                    row.update(status="computed", reason="")
                    previous = flame.to_array()
            except fuels.MechanismUnavailable:
                row.update(status="unavailable", reason="Required fuel species or mechanism unavailable")
                stopped = "Required fuel species or mechanism unavailable"
            except ct.CanteraError:
                row["reason"] = "Cantera flame solver failed; physical extinction not established"
                stopped = "Not attempted after earlier Cantera solver failure"
        elif stopped == "Required fuel species or mechanism unavailable":
            row["status"] = "unavailable"
        rows.append(row)
    return rows


def ignition_delay(fuel, phi, w, T_K, p_Pa=IGNITION_PRESSURE_PA,
                   max_time_s=DEFAULTS.ignition_max_time_s):
    """Adiabatic constant-volume ignition; tau is the sampled max dT/dt.

    Evaluate dT/dt directly from the constant-volume energy equation at each
    adaptive CVODES step: -sum(u_k * omega_k)/(rho*cv). This avoids noisy
    finite differences on an uneven time grid. Require a resolved interior
    peak and a named temperature-rise criterion; censor at the time horizon.
    """
    if not math.isfinite(max_time_s) or max_time_s <= 0:
        raise ValueError("max_time_s must be finite and positive")
    p = DEFAULTS
    row = _record(fuel, phi, w, T_K, p_Pa)
    row.update(tau_s=None, peak_dT_dt_K_s=None, temperature_rise_K=None,
               simulated_time_s=0.0, max_time_s=max_time_s,
               status="no_ignition", reason="")
    try:
        gas = _gas(fuel, phi, w, T_K, p_Pa)
        reactor = ct.IdealGasReactor(gas, energy="on", clone=True)
        network = ct.ReactorNet([reactor])
        network.rtol, network.atol = p.reactor_rtol, p.reactor_atol
        times, rates = [0.0], []

        def rate():
            state = reactor.phase
            return float(-np.dot(state.partial_molar_int_energies,
                                 state.net_production_rates) / (state.density * state.cv_mass))

        rates.append(rate())
        max_T = T_K
        while network.time < max_time_s:
            remaining = max_time_s - network.time
            if remaining <= np.finfo(float).eps * max_time_s:
                break
            if remaining <= p.ignition_max_step_s:
                # Land exactly on the censoring horizon: ReactorNet.step() may overshoot it.
                network.advance(max_time_s)
            else:
                network.max_time_step = p.ignition_max_step_s
                network.step()
            times.append(float(network.time))
            rates.append(rate())
            max_T = max(max_T, reactor.T)
        peak = int(np.argmax(rates))
        rise = float(max_T - T_K)
        row.update(peak_dT_dt_K_s=rates[peak], temperature_rise_K=rise,
                   simulated_time_s=float(network.time))
        if rise >= p.ignition_min_rise_K and 0 < peak < len(rates) - 1:
            row.update(tau_s=times[peak], status="ignited")
        else:
            row["reason"] = "No resolved interior heat-release peak with required temperature rise within horizon"
    except fuels.MechanismUnavailable:
        row.update(status="unavailable", reason="Required fuel species or mechanism unavailable")
    except ct.CanteraError:
        row["reason"] = "Cantera reactor solver failed; ignition not established"
    return row


def fit_ignition(rows, mode="full"):
    """Least squares in ln(tau); p is in Pa, A in s*Pa**n.

    tau = A p**-n exp(E/(R T)) (1 + c w)
    ln tau = ln A - n ln p - (E/R) (1000/T) + ln(1 + c w)

    n is FREE whenever the data span at least two distinct pressures; with a
    single pressure it is unidentifiable and stays fixed at 1.0.  The fit is
    centred on the mean 1000/T and the mean ln p for conditioning.  c is
    allowed either sign (1+c*w must stay positive): water can affect
    chemistry as well as dilute it, so a fit must not manufacture monotonic
    ignition delays.
    """
    fits = {}
    for fuel in FUELS:
        data = [r for r in rows if r["fuel"] == fuel and r["status"] == "ignited"
                and r["tau_s"] is not None and math.isfinite(r["tau_s"]) and r["tau_s"] > 0]
        result = dict(mode=mode, status="insufficient_data", A=None, n=1.0,
                      E_J_per_mol=None, c=None, valid_T_K_range=None,
                      valid_w_range=None, valid_p_Pa_range=None,
                      rms_ln_tau=None, rms_log10_tau=None, number_of_points=len(data),
                      pressure_unit="Pa", A_unit="s*Pa", pressure_exponent_fitted=False)
        fits[fuel] = result
        if not data:
            continue
        T, w, pressure, tau = (np.array([r[key] for r in data], dtype=float)
                               for key in ("T_unburned_K", "w", "p_Pa", "tau_s"))
        result.update(valid_T_K_range=[float(T.min()), float(T.max())],
                      valid_w_range=[float(w.min()), float(w.max())],
                      valid_p_Pa_range=[float(pressure.min()), float(pressure.max())])
        if len(data) < 3 or len(set(T)) < 2 or len(set(w)) < 2:
            continue
        x = 1000.0 / T
        centre_x = float(x.mean())
        lp = np.log(pressure)
        centre_p = float(lp.mean())
        y = np.log(tau)
        n_free = len(set(pressure)) >= 2
        if n_free:
            design = np.column_stack((np.ones(len(x)), x - centre_x, lp - centre_p, w))
            if np.linalg.matrix_rank(design) < 4:
                result["status"] = "rank_deficient"
                continue
            initial = np.linalg.lstsq(design, y, rcond=None)[0]
            lower_c = -1.0 / float(w.max())
            initial[3] = max(initial[3], lower_c / 2.0)
            # Bounds: n unconstrained; c above the singularity floor.
            bounds = ([-np.inf, -np.inf, -np.inf, np.nextafter(lower_c, np.inf)],
                      [np.inf, np.inf, np.inf, np.inf])

            def residual(v):
                return (v[0] + v[1] * (x - centre_x) + v[2] * (lp - centre_p)
                        + np.log1p(v[3] * w) - y)
        else:
            design = np.column_stack((np.ones(len(x)), x - centre_x, w))
            if np.linalg.matrix_rank(design) < 3:
                result["status"] = "rank_deficient"
                continue
            initial = np.linalg.lstsq(design, y, rcond=None)[0]
            lower_c = -1.0 / float(w.max())
            initial[2] = max(initial[2], lower_c / 2.0)
            bounds = ([-np.inf, -np.inf, np.nextafter(lower_c, np.inf)],
                      [np.inf, np.inf, np.inf])

            def residual(v):
                return v[0] + v[1] * (x - centre_x) + np.log1p(v[2] * w) - y

        fit = least_squares(residual, initial, bounds=bounds,
                            max_nfev=DEFAULTS.fit_max_evaluations)
        if not fit.success or np.linalg.matrix_rank(fit.jac) < (4 if n_free else 3):
            result["status"] = "fit_failed"
            continue
        # v0 = ln A - (E/R) centre_x - n centre_p for the free-n design and
        # ln A - (E/R) centre_x - n ln p for the single-pressure design, so
        # the single-pressure reconstruction ADDS n*centre_p back.
        if n_free:
            log_A = float(fit.x[0] - (fit.x[1] * centre_x + fit.x[2] * centre_p))
        else:
            log_A = float(fit.x[0] - fit.x[1] * centre_x + 1.0 * centre_p)
        if not math.log(np.finfo(float).tiny) < log_A < math.log(np.finfo(float).max):
            result["status"] = "fit_nonfinite"
            continue
        resid = fit.fun
        result.update(status="fitted", A=math.exp(log_A),
                      n=float(-fit.x[2]) if n_free else 1.0,
                      E_J_per_mol=float(fit.x[1] * 1000.0 * R_J_MOL_K),
                      c=float(fit.x[-1]),
                      rms_ln_tau=float(np.sqrt(np.mean(resid**2))),
                      rms_log10_tau=float(np.sqrt(np.mean((resid / math.log(10.0))**2))),
                      pressure_exponent_fitted=bool(n_free))
    return fits


def fit_flame_speeds(rows, mode="full"):
    """Four coefficients, highest power first; never extrapolate their range.

    Full mode requires four resolved points for a cubic. Quick mode explicitly
    uses a line through its two points, zero-padded to the same file schema.
    """
    fits, limits = {}, {}
    for fuel in FUELS:
        data = [r for r in rows if r["fuel"] == fuel and r["phi"] == 1.0
                and r["T_unburned_K"] == 400.0 and r["p_Pa"] == ct.one_atm
                and r["status"] == "computed"]
        limits[fuel] = {name: max((r["w"] for r in data if r["S_L_m_s"] >= cutoff), default=None)
                        for name, cutoff in (("w_SI_robust", DEFAULTS.robust_m_s),
                                             ("w_SI_marginal", DEFAULTS.marginal_m_s))}
        result = dict(mode=mode, status="insufficient_data", coefficients_highest_first=None,
                      polynomial_degree=None, valid_w_range=None, rms_m_s=None,
                      number_of_points=len(data), T_unburned_K=400.0,
                      p_Pa=ct.one_atm, phi=1.0, S_L_unit="m/s")
        fits[fuel] = result
        if data:
            result["valid_w_range"] = [min(r["w"] for r in data), max(r["w"] for r in data)]
        degree = 1 if mode == "quick" else 3
        if len(data) < degree + 1:
            continue
        w = np.array([r["w"] for r in data])
        speed = np.array([r["S_L_m_s"] for r in data])
        coeff = np.polyfit(w, speed, degree)
        result.update(status="quick_linear" if mode == "quick" else "fitted",
                      coefficients_highest_first=np.pad(coeff, (3 - degree, 0)).tolist(),
                      polynomial_degree=degree,
                      rms_m_s=float(np.sqrt(np.mean((np.polyval(coeff, w) - speed)**2))))
    return fits, limits


def _task(task):
    """Small picklable task dispatch; construction happens inside each worker."""
    kind, arguments = task
    if kind == "adiabatic":
        return kind, [adiabatic_temperature(*arguments)]
    if kind == "cooling":
        return kind, [evaporative_cooling(*arguments)]
    if kind == "flame":
        return kind, flame_speed_sweep(arguments)
    if kind == "ignition":
        return kind, [ignition_delay(*arguments)]
    raise ValueError("Unknown task kind")


def build_tasks(mode, max_time_s):
    names = QUICK_FUELS if mode == "quick" else FUELS
    waters = QUICK_WATER if mode == "quick" else WATER_FRACTIONS
    pressures = QUICK_IGNITION_PRESSURES_PA if mode == "quick" else IGNITION_PRESSURES_PA
    ignition_Ts = QUICK_IGNITION_T if mode == "quick" else IGNITION_TEMPERATURES
    tasks = []
    for fuel in names:
        for phi in PHIS:
            for w in waters:
                tasks.extend(("adiabatic", (fuel, phi, w, T, pressure))
                             for T, pressure in ADIABATIC_STATES)
                tasks.append(("cooling", (fuel, phi, w)))
        for phi in ((1.0,) if mode == "quick" else PHIS):
            for T, pressure in (FLAME_STATES[:1] if mode == "quick" else FLAME_STATES):
                tasks.append(("flame", (fuel, phi, T, pressure, waters)))
        for T in ignition_Ts:
            tasks.extend(("ignition", (fuel, 1.0, w, T, p, max_time_s))
                         for p in pressures for w in waters)
    if mode == "full":
        tasks.extend(("flame", (fuel, phi, T, ct.one_atm, (0.0,)))
                     for fuel, phi, T, _, _ in FLAME_TARGETS)
    # Schedule expensive sweeps first; ordered_map retains deterministic order.
    return sorted(tasks, key=lambda task: task[0] != "flame")


def validation(adiabatic, flames):
    checks = {}
    for fuel, (target, tolerance) in TAD_TARGETS.items():
        row = next((r for r in adiabatic if r["fuel"] == fuel and r["phi"] == 1
                    and r["w"] == 0 and r["T_unburned_K"] == 300 and r["p_Pa"] == ct.one_atm), None)
        actual = row["T_ad_K"] if row else None
        checks[f"{fuel}_T_ad"] = dict(actual_K=actual, target_K=target, tolerance_K=tolerance,
            status="passed" if actual is not None and abs(actual - target) <= tolerance else "failed")
    for fuel, phi, T, lower, upper in FLAME_TARGETS:
        row = next((r for r in flames if r["fuel"] == fuel and r["phi"] == phi
                    and r["w"] == 0 and r["T_unburned_K"] == T and r["p_Pa"] == ct.one_atm), None)
        actual = row["S_L_m_s"] if row else None
        status = ("not_computed_in_quick" if row is None else
                  "passed" if row["status"] == "computed" and lower <= actual <= upper else "failed")
        checks[f"{fuel}_S_L_phi_{phi}_T_{T}"] = dict(actual_m_s=actual,
            allowed_range_m_s=[lower, upper], status=status)
    return dict(passed=all(c["status"] != "failed" for c in checks.values()),
                scope="In-run reference points only; server pytest required for full validation",
                checks=checks)


def assumptions(mode, workers, max_time_s):
    result = fuels.fuel_assumptions()
    selections = {}
    for fuel in FUELS:
        row = _record(fuel, 1.0, 0.0, 300.0, ct.one_atm)
        selections[fuel] = {"name": row["mechanism"], "mechanism_fallback": row["mechanism_fallback"],
                            "selected_in_mode": mode == "full" or fuel in QUICK_FUELS}
    result.update({
        "mechanisms": selections,
        "mechanism_fallback": any(r["mechanism_fallback"] and r["selected_in_mode"] for r in selections.values()),
        "parameters": {"defaults": asdict(DEFAULTS), "ignition_max_time_s_used": max_time_s,
            "sources": {
                "water_T_K,intake_T_K,refine_ratio,refine_slope,refine_curve,flame_stop_m_s,robust_m_s,marginal_m_s,ignition_max_time_s,ignition_pressure_exponent": "SPEC section 5 and task contract",
                "cooling_p_Pa": "Standard atmosphere: unboosted intake model",
                "dew_margin_K": "0.1 K numerical margin to remain strictly above saturation",
                "flame_width_1atm_m,flame_width_5bar_m": "Task suggested 0.03 m at 1 atm; 0.01 m for thinner elevated-pressure flames; auto domain expansion allowed",
                "ignition_min_rise_K": "200 K operational ignition criterion to reject slow preignition drift; not an experimental ignition threshold",
                "ignition_max_step_s": "5 ms maximum adaptive step; resolves horizon and post-peak evolution; CVODES resolves fast chemistry internally",
                "reactor_rtol,reactor_atol": "Explicit tight integration error tolerances; convergence must be assessed on server",
                "fit_max_evaluations": "Numerical nonlinear least-squares iteration budget"}},
        "sweeps": {"full_fuels": FUELS, "phi": PHIS, "full_w": WATER_FRACTIONS,
                    "adiabatic_states_K_Pa": ADIABATIC_STATES, "flame_states_K_Pa": FLAME_STATES,
                    "ignition_T_K": IGNITION_TEMPERATURES, "ignition_p_Pa": list(IGNITION_PRESSURES_PA),
                    "ignition_phi": 1.0, "quick_fuels": QUICK_FUELS, "quick_w": QUICK_WATER,
                    "quick_ignition_T_K": QUICK_IGNITION_T,
                    "quick_ignition_p_Pa": list(QUICK_IGNITION_PRESSURES_PA),
                    "quick_flame_state_K_Pa_phi": [400.0, ct.one_atm, 1.0],
                    "source": "SPEC section 5; quick subset selected to target <120 s on two cores"},
        "unburned_phase": {"value": "All fuel and added water are vapour for equilibrium, flame and ignition calculations, including liquid alcohols",
            "rationale": "Specified premixed states, even if supersaturated; external vaporization/preheat energy is not chemical fuel energy"},
        "evaporation": {"value": "Adiabatic mixing; dry ideal gas and H2O vapour cp frozen at 320 K; dry fuel already vaporized; no reactions, heat loss, pressure loss or fuel latent heat",
            "source": "CoolProp Water / IAPWS-95 (Wagner & Pruss, 2002); Cantera mechanism species cp",
            "enthalpy_reference": "CoolProp h_v,sat(300)-h_l(300,p) plus Cantera vapour sensible heat; absolute enthalpy references never mixed",
            "feasibility": "temperature_drop_K is hypothetical full-evaporation demand when infeasible; final_all_vapour_T_K is null then; no two-phase state inferred",
            "dew_domain": "CoolProp saturation at water partial pressure; below triple pressure use triple T plus margin as conservative minimum bound; dry minimum is undefined",
            "limitation": "Frozen cp extrapolation is an engineering estimate, especially at high w; minimum intake temperatures are within this same model"},
        "flame_model": {"value": "FreeFlame, mixture-averaged transport, Soret disabled, auto=True, previous converged profile for upward continuation",
            "rationale": "SPEC transport model; failed solver is not evidence of physical extinction; unattempted later points retain no_flame and reason"},
        "ignition_model": {"value": "Adiabatic constant-volume IdealGasReactor; direct energy-equation dT/dt at adaptive steps; entire time horizon integrated",
            "rationale": "SPEC ignition definition; resolved interior maximum and minimum rise reject censored or non-igniting trajectories"},
        "fits": {"value": "Unweighted least squares in ln(tau); n FREE when >=2 distinct pressures are computed (20/40/80 bar), fixed at 1.0 for single-pressure data; unconstrained E and c except 1+c*w>0; no extrapolation beyond observed ranges",
                    "rationale": "Ignition delays are now computed at 20, 40 and 80 bar so the pressure exponent is identifiable; the fit reports rms_ln_tau and rms_log10_tau",
            "flame_polynomial": "Cubic requires >=4 points; quick mode uses explicit degree-1 surrogate padded to four coefficients; insufficient data gives null parameters",
            "limits": "Largest sampled qualifying w, not interpolated extinction limits; quick values apply only to sparse subset"},
        "workers": {"value": workers, "chunksize": 1,
            "rationale": "io.ordered_map spawn pool, per-task gas construction, no pickled Cantera objects; one task per chunk balances long flame sweeps"},
        "validation_targets": {"T_ad_K": TAD_TARGETS, "flame_ranges": FLAME_TARGETS,
            "source": "SPEC section 10; research note 02 references 38/40 with user-specified model tolerances"},
    })
    return result


def write_plots(out, tables):
    specifications = (
        ("adiabatic", "T_ad_K", "Adiabatic flame temperature [K]", "adiabatic_flame_T.png"),
        ("flame", "S_L_m_s", "Laminar flame speed [m/s]", "flame_speed.png"),
        ("cooling", "temperature_drop_K", "Formal complete-evaporation cooling [K]", "evaporative_cooling.png"),
        ("ignition", "tau_s", "Ignition delay [s]", "ignition_delay.png"),
    )
    for kind, quantity, label, filename in specifications:
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        for ax, fuel in zip(axes.flat, FUELS):
            rows = [r for r in tables[kind] if r["fuel"] == fuel and r[quantity] is not None
                    and r["status"] in {"computed", "ignited"}]
            keys = sorted({(r["w"],) if kind == "ignition" else
                           (r["phi"], r["T_unburned_K"], r["p_Pa"]) for r in rows})
            for key in keys:
                group = [r for r in rows if ((r["w"],) if kind == "ignition" else
                         (r["phi"], r["T_unburned_K"], r["p_Pa"])) == key]
                group.sort(key=lambda r: 1000.0 / r["T_unburned_K"] if kind == "ignition" else r["w"])
                x = [1000.0 / r["T_unburned_K"] if kind == "ignition" else r["w"] for r in group]
                legend = (f"w={key[0]:g}" if kind == "ignition" else
                          f"phi={key[0]:g}, {key[1]:g} K, {key[2]/1e5:g} bar")
                color = plt.get_cmap("viridis")(key[0] / WATER_FRACTIONS[-1]) if kind == "ignition" else None
                ax.plot(x, [r[quantity] for r in group], "o-", label=legend, color=color)
            if kind == "ignition":
                ax.set_yscale("log")
            ax.set(title=fuel, xlabel="1000 / initial temperature [1/K]" if kind == "ignition" else "Water mass fraction w [1]", ylabel=label)
            if keys:
                ax.legend(fontsize="small")
            else:
                ax.text(0.5, 0.5, "No computed points", transform=ax.transAxes, ha="center")
            ax.grid(alpha=0.25)
        fig.tight_layout()
        io.save_fig(fig, out / filename)
        plt.close(fig)


def _positive_time(value):
    import argparse
    try:
        number = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Time must be a positive finite number") from exc
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("Time must be a positive finite number")
    return number


def main(argv=None):
    start = time.perf_counter()
    parser = io.argument_parser(MODULE)
    parser.add_argument("--ignition-max-time-s", type=_positive_time,
                        default=DEFAULTS.ignition_max_time_s,
                        help="Maximum simulated ignition time [s] (default: 0.5)")
    args = parser.parse_args(None if argv is None else list(map(str, argv)))
    tables = {name: [] for name in ("adiabatic", "cooling", "flame", "ignition")}
    for kind, rows in io.ordered_map(_task, build_tasks(args.mode, args.ignition_max_time_s),
                                     args.workers, chunksize=1):
        tables[kind].extend(rows)
    for kind, filename in (("adiabatic", "adiabatic_flame_T.csv"),
                           ("cooling", "evaporative_cooling.csv"),
                           ("flame", "flame_speed.csv"), ("ignition", "ignition_delay.csv")):
        io.write_csv(args.out / filename, tables[kind])
    ignition_fits = fit_ignition(tables["ignition"], args.mode)
    flame_fits, limits = fit_flame_speeds(tables["flame"], args.mode)
    for filename, payload in (("ignition_fits.json", ignition_fits), ("flame_speed_fits.json", flame_fits)):
        (args.out / filename).write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    write_plots(args.out, tables)
    checks = validation(tables["adiabatic"], tables["flame"])
    counts = {kind: {status: sum(r["status"] == status for r in rows)
                     for status in sorted({r["status"] for r in rows})}
              for kind, rows in tables.items()}
    results = dict(w_SI_robust={f: v["w_SI_robust"] for f, v in limits.items()},
                   w_SI_marginal={f: v["w_SI_marginal"] for f, v in limits.items()},
                   ignition_fits=ignition_fits, flame_speed_fits=flame_fits,
                   counts=counts, no_flame=counts["flame"].get("no_flame", 0),
                   no_ignition=counts["ignition"].get("no_ignition", 0),
                   validation_values=checks["checks"],
                   energy_source="Fuel LHV only; water heating value is zero")
    io.write_summary(args.out, MODULE, VERSION, args.mode,
                     assumptions(args.mode, args.workers, args.ignition_max_time_s),
                     results, checks, time.perf_counter() - start)
    return 0 if checks["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
