"""Module 02 validation; slow chemistry tests remain part of default pytest.

Run on the Linux simulation server, not the code-writing machine. Reference
values are SPEC section 10 and research note 02 references 38 and 40.
"""

from functools import lru_cache
import importlib
import json
import math
import pickle

import cantera as ct
import numpy as np
import pytest

from sims.common import fuels, io


chem = importlib.import_module("sims.02_flame_chem.run")


def require_fuel(fuel):
    if fuel == "C2H5OH" and not fuels.SAN_DIEGO_PATH.is_file():
        pytest.skip("C2H5OH requires mechanisms/sandiego.yaml (SPEC fallback)")


@lru_cache(maxsize=None)
def flame_rows(fuel, phi, T, pressure, waters):
    return chem.flame_speed_sweep((fuel, phi, T, pressure, waters))


@lru_cache(maxsize=None)
def ignition_rows(fuel):
    return tuple(chem.ignition_delay(fuel, 1.0, w, T)
                 for T in (1000.0, 1050.0, 1100.0) for w in (0.0, 0.3))


@pytest.mark.parametrize("fuel,target,tolerance", [
    ("CH4", 2225.0, 20.0), ("H2", 2380.0, 25.0),
])
def test_adiabatic_temperature_reference(fuel, target, tolerance):
    row = chem.adiabatic_temperature(fuel, 1.0, 0.0, 300.0, ct.one_atm)
    assert row["status"] == "computed", row
    assert row["T_ad_K"] == pytest.approx(target, abs=tolerance)


@pytest.mark.slow
@pytest.mark.parametrize("fuel,lower,upper", [("CH4", 0.34, 0.42), ("H2", 1.9, 2.6)])
def test_dry_flame_speed_reference(fuel, lower, upper):
    row, = flame_rows(fuel, 1.0, 300.0, ct.one_atm, (0.0,))
    assert row["status"] == "computed", row
    assert lower <= row["S_L_m_s"] <= upper


@pytest.mark.slow
@pytest.mark.parametrize("phi,target,tolerance", [(0.7, 0.156, 0.04), (1.3, 0.247, 0.05)])
def test_research_methane_flame_speed(phi, target, tolerance):
    # Stanford FFCM-1 fls_27a/fls_27c, research note refs 38/40.
    # These model tolerances are intentionally wider than measurement errors.
    row, = flame_rows("CH4", phi, 298.0, ct.one_atm, (0.0,))
    assert row["status"] == "computed", row
    assert row["S_L_m_s"] == pytest.approx(target, abs=tolerance)


@pytest.mark.parametrize("fuel", chem.FUELS)
def test_water_reduces_adiabatic_temperature(fuel):
    require_fuel(fuel)
    rows = [chem.adiabatic_temperature(fuel, 1.0, w, 400.0, ct.one_atm)
            for w in (0.0, 0.1, 0.3)]
    assert all(r["status"] == "computed" for r in rows), rows
    assert np.all(np.diff([r["T_ad_K"] for r in rows]) < 0)


@pytest.mark.slow
@pytest.mark.parametrize("fuel", chem.FUELS)
def test_water_reduces_flame_speed(fuel):
    require_fuel(fuel)
    rows = flame_rows(fuel, 1.0, 400.0, ct.one_atm, (0.0, 0.1, 0.3))
    # Do not hide solver failures or turn extinction into fabricated zero speed.
    assert all(r["status"] == "computed" for r in rows), rows
    assert np.all(np.diff([r["S_L_m_s"] for r in rows]) < 0)


@pytest.mark.parametrize("fuel", chem.FUELS)
def test_evaporation_demand_and_feasibility(fuel):
    require_fuel(fuel)
    rows = [chem.evaporative_cooling(fuel, 1.0, w) for w in chem.WATER_FRACTIONS]
    assert all(r["status"] == "computed" for r in rows)
    assert rows[0]["temperature_drop_K"] == 0
    assert rows[0]["complete_evaporation_possible"] is True
    assert rows[0]["minimum_intake_T_K"] is None  # No water, no dew constraint.
    assert np.all(np.diff([r["temperature_drop_K"] for r in rows]) > 0)
    assert np.all(np.diff([r["minimum_intake_T_K"] for r in rows[1:]]) > 0)
    for row in rows:
        assert abs(row["energy_residual_J_per_kg_fuel"]) < 1e-6
        assert row["h_fg_J_kg"] > 0
        if row["complete_evaporation_possible"] and row["w"] > 0:
            assert row["water_partial_pressure_Pa"] < row["saturation_pressure_at_final_Pa"]
        elif not row["complete_evaporation_possible"]:
            assert row["final_all_vapour_T_K"] is None
            assert row["minimum_intake_T_K"] > chem.DEFAULTS.intake_T_K
    assert rows[-1]["complete_evaporation_possible"] is False


def test_minimum_intake_closes_evaporation_balance():
    from dataclasses import replace

    reference = chem.evaporative_cooling("CH4", 1.0, 0.3)
    # The reported minimum uses frozen cp at the original intake reference.
    # Independently check the stated energy equation at its dew endpoint.
    endpoint = reference["dew_point_K"] + chem.DEFAULTS.dew_margin_K
    mw = 0.3 / 0.7
    md = 1.0 + fuels.stoich_air_fuel_ratio("CH4")
    lhs = md * reference["dry_cp_J_kg_K"] * (reference["minimum_intake_T_K"] - endpoint)
    rhs = mw * (reference["reference_vapour_h_J_kg"] - reference["liquid_water_h_J_kg"]
                + reference["vapour_cp_J_kg_K"] * (endpoint - chem.DEFAULTS.water_T_K))
    assert lhs == pytest.approx(rhs, rel=1e-12)
    # A sufficiently warmer intake must be feasible even when cp is recomputed.
    heated = chem.evaporative_cooling("CH4", 1.0, 0.3,
             replace(chem.DEFAULTS, intake_T_K=reference["minimum_intake_T_K"] + 10.0))
    assert heated["complete_evaporation_possible"] is True


@pytest.mark.parametrize("fuel", chem.FUELS)
def test_added_water_cannot_increase_fuel_energy(fuel):
    """Independent complete-product reference enthalpies, per kg actual fuel.

    Absolute h_products changes when mass/reference states change. Chemical
    energy is h_reactants-h_complete_products, with the same added steam on
    both sides. Premade alcohol vapour carries separately supplied latent heat.
    HP conservation is tested separately from this LHV chemical ledger.
    """
    require_fuel(fuel)
    values = []
    for w in (0.0, 0.3, 0.6, 0.9):
        gas = fuels.load_mechanism(fuel)
        gas.TPX = fuels.REFERENCE_T_K, ct.one_atm, fuels.mixture(fuel, 1.0, w)
        Y_fuel = float(gas[fuels.species_name(gas, fuel)].Y[0])
        reactant_h = float(gas.enthalpy_mass / Y_fuel)
        composition = fuels.mixture(fuel, 1.0, w)
        c, h, _ = fuels.FUELS[fuel].atoms
        water_name = fuels.species_name(gas, "H2O")
        products = {water_name: composition[water_name] + h / 2.0,
                    fuels.species_name(gas, "N2"): composition[fuels.species_name(gas, "N2")]}
        if c:
            products[fuels.species_name(gas, "CO2")] = float(c)
        gas.TPX = fuels.REFERENCE_T_K, ct.one_atm, products
        product_h = float(gas.enthalpy_mass / Y_fuel)
        external_fuel_vaporization = fuels.FUELS[fuel].h_fg if fuels.FUELS[fuel].state == "liquid" else 0.0
        energy = reactant_h - product_h - external_fuel_vaporization
        values.append(energy)
        assert energy == pytest.approx(fuels.lhv(fuel), rel=1e-10)
        # Equilibrium cannot create total enthalpy, even though it redistributes
        # chemical and sensible terms. Normalize to the original fuel mass.
        gas.TPX = 400.0, ct.one_atm, composition
        before = gas.enthalpy_mass / Y_fuel
        gas.equilibrate("HP")
        assert gas.enthalpy_mass / Y_fuel == pytest.approx(before, rel=1e-6, abs=1.0)
    assert max(values) - min(values) < 1e-5
    assert abs(fuels.lhv("H2O")) < 1.0


@pytest.mark.slow
def test_computed_ignition_fit_and_water_delay():
    # CH4 is the stable reference for this dilution trend. Do not constrain
    # fits for other fuels to suppress possible kinetic water promotion.
    rows = ignition_rows("CH4")
    paired = 0
    for T in (1000.0, 1050.0, 1100.0):
        dry, wet = [r for r in rows if r["T_unburned_K"] == T]
        if dry["status"] == wet["status"] == "ignited":
            paired += 1
            assert wet["tau_s"] > dry["tau_s"]
    assert paired >= 2, rows
    fit = chem.fit_ignition(rows)["CH4"]
    assert fit["status"] == "fitted", fit
    assert fit["n"] == 1.0  # single-pressure data: n unidentifiable, kept at 1.0
    assert fit["A"] > 0
    assert all(math.isfinite(fit[key]) for key in ("A", "n", "E_J_per_mol", "c", "rms_ln_tau"))


def test_ignition_horizon_is_censored():
    row = chem.ignition_delay("CH4", 1.0, 0.0, 750.0, max_time_s=1e-8)
    assert row["status"] == "no_ignition", row
    assert row["tau_s"] is None
    assert row["simulated_time_s"] <= 1e-8 * (1 + 1e-12)


@pytest.mark.parametrize("horizon", [0.0, -1.0, float("nan"), float("inf")])
def test_invalid_ignition_horizon(horizon):
    with pytest.raises(ValueError, match="positive"):
        chem.ignition_delay("CH4", 1.0, 0.0, 1000.0, max_time_s=horizon)


def test_fit_recovers_known_parameters_and_pressure_units():
    A, E, c, pressure = 2e-3, 120000.0, 2.5, 40e5
    rows = [dict(fuel="CH4", T_unburned_K=T, w=w, p_Pa=pressure,
                 tau_s=A / pressure * math.exp(E / (chem.R_J_MOL_K * T)) * (1 + c * w),
                 status="ignited")
            for T in (900.0, 1000.0, 1100.0) for w in (0.0, 0.3, 0.6)]
    # Censored observations are not assigned the horizon as an ignition delay.
    rows.append(dict(fuel="CH4", T_unburned_K=750.0, w=0.9, p_Pa=pressure,
                     tau_s=None, status="no_ignition"))
    fit = chem.fit_ignition(rows)["CH4"]
    assert fit["status"] == "fitted"
    assert fit["A"] == pytest.approx(A, rel=1e-5)
    assert fit["E_J_per_mol"] == pytest.approx(E, rel=1e-6)
    assert fit["c"] == pytest.approx(c, rel=1e-5)
    assert fit["n"] == 1.0  # single pressure: n unidentifiable
    assert fit["rms_ln_tau"] < 1e-6
    assert fit["number_of_points"] == 9
    assert fit["valid_T_K_range"] == [900.0, 1100.0]
    assert fit["valid_w_range"] == [0.0, 0.6]
    assert fit["valid_p_Pa_range"] == [pressure, pressure]
    assert fit["pressure_exponent_fitted"] is False


def test_fit_recovers_free_pressure_exponent():
    """n is genuinely free when data span >=2 distinct pressures.

    Fit form is tau = A p**-n exp(E/RT)(1+cw), so a data generator with
    tau = A p**N ... corresponds to fit n = -N.
    """
    A, n, E, c = 2e-3, 1.7, 120000.0, 2.5
    rows = [dict(fuel="CH4", T_unburned_K=T, w=w, p_Pa=p,
                 tau_s=A * p**(-n) * math.exp(E / (chem.R_J_MOL_K * T)) * (1 + c * w),
                 status="ignited")
            for p in (20e5, 40e5, 80e5)
            for T in (900.0, 1000.0, 1100.0) for w in (0.0, 0.3, 0.6)]
    fit = chem.fit_ignition(rows)["CH4"]
    assert fit["status"] == "fitted"
    assert fit["pressure_exponent_fitted"] is True
    assert fit["n"] == pytest.approx(n, rel=1e-4)
    assert fit["A"] == pytest.approx(A, rel=1e-4)
    assert fit["E_J_per_mol"] == pytest.approx(E, rel=1e-5)
    assert fit["c"] == pytest.approx(c, rel=1e-4)
    assert fit["rms_log10_tau"] < 1e-6
    assert fit["valid_p_Pa_range"] == [20e5, 80e5]


def test_insufficient_fits_are_null_not_fabricated():
    for fit in chem.fit_ignition([]).values():
        assert fit["status"] == "insufficient_data"
        assert fit["A"] is fit["E_J_per_mol"] is fit["c"] is None
    fits, limits = chem.fit_flame_speeds([])
    for fuel in chem.FUELS:
        assert fits[fuel]["coefficients_highest_first"] is None
        assert limits[fuel] == {"w_SI_robust": None, "w_SI_marginal": None}


def test_flame_cubic_fit_limits_and_quick_degree():
    # Synthetic fit validation is separate from physical flame validation.
    coeff = [-0.1, 0.2, -0.5, 0.4]
    rows = [dict(fuel="CH4", phi=1.0, T_unburned_K=400.0, p_Pa=ct.one_atm,
                 w=w, S_L_m_s=float(np.polyval(coeff, w)), status="computed")
            for w in chem.WATER_FRACTIONS]
    fit, limits = chem.fit_flame_speeds(rows)
    assert fit["CH4"]["coefficients_highest_first"] == pytest.approx(coeff)
    assert fit["CH4"]["rms_m_s"] < 1e-12
    assert limits["CH4"]["w_SI_robust"] == max(r["w"] for r in rows if r["S_L_m_s"] >= 0.15)
    assert limits["CH4"]["w_SI_marginal"] == max(r["w"] for r in rows if r["S_L_m_s"] >= 0.08)
    sparse = [r for r in rows if r["w"] in chem.QUICK_WATER]
    quick, _ = chem.fit_flame_speeds(sparse, "quick")
    assert quick["CH4"]["mode"] == "quick"
    assert quick["CH4"]["status"] == "quick_linear"
    assert quick["CH4"]["polynomial_degree"] == 1
    assert quick["CH4"]["coefficients_highest_first"][:2] == [0.0, 0.0]
    full, _ = chem.fit_flame_speeds(sparse, "full")
    assert full["CH4"]["status"] == "insufficient_data"


@pytest.mark.parametrize("failure", ["exception", "slow"])
def test_flame_stop_retains_all_points(monkeypatch, failure):
    calls = []

    class FakeFlame:
        grid = [0.0, 0.03]
        velocity = [0.01]

        def __init__(self, gas, width):
            calls.append(width)

        def set_refine_criteria(self, **kwargs):
            pass

        def solve(self, **kwargs):
            if failure == "exception":
                raise ct.CanteraError("Deliberate test failure")

    monkeypatch.setattr(chem, "_gas", lambda *args: object())
    monkeypatch.setattr(chem.ct, "FreeFlame", FakeFlame)
    rows = chem.flame_speed_sweep(("CH4", 1.0, 400.0, ct.one_atm, (0.0, 0.1, 0.2)))
    assert len(calls) == 1
    assert [r["w"] for r in rows] == [0.0, 0.1, 0.2]
    assert all(r["status"] == "no_flame" for r in rows)
    assert rows[0]["attempted"] is True
    assert all(not r["attempted"] for r in rows[1:])
    assert all(r["reason"] for r in rows)
    assert all(r["S_L_m_s"] is None for r in rows[1:])


def test_missing_ethanol_is_not_no_flame(monkeypatch, tmp_path):
    monkeypatch.setattr(fuels, "SAN_DIEGO_PATH", tmp_path / "missing.yaml")
    rows = chem.flame_speed_sweep(("C2H5OH", 1.0, 400.0, ct.one_atm, (0.0, 0.1)))
    assert all(r["status"] == "unavailable" for r in rows)
    assert all(r["mechanism_fallback"] for r in rows)
    methanol = chem.adiabatic_temperature("CH3OH", 1.0, 0.0, 400.0, ct.one_atm)
    assert methanol["mechanism"] == "gri30.yaml"
    assert methanol["mechanism_fallback"] is True
    assert chem.assumptions("full", 1, 0.5)["mechanism_fallback"] is True


def test_full_task_grid_and_picklable_payloads():
    tasks = chem.build_tasks("full", 0.5)
    assert pickle.loads(pickle.dumps(tasks)) == tasks
    counts = {kind: sum(task[0] == kind for task in tasks)
              for kind in ("adiabatic", "cooling", "flame", "ignition")}
    # Ignition: 4 fuels x 3 pressures x 10 w x 8 T = 960 (was 320 at 40 bar only).
    assert counts == {"adiabatic": 240, "cooling": 80, "flame": 20, "ignition": 960}
    for kind, arguments in tasks:
        assert isinstance(arguments, tuple)
        if kind == "flame" and arguments[2] in (400.0, 450.0):
            assert arguments[-1] == chem.WATER_FRACTIONS
    quick = chem.build_tasks("quick", 0.5)
    assert {args[0] for _, args in quick} == {"H2", "CH4"}
    assert {args[3] for kind, args in quick if kind == "ignition"} == set(chem.QUICK_IGNITION_T)
    assert {args[4] for kind, args in quick if kind == "ignition"} == set(chem.QUICK_IGNITION_PRESSURES_PA)


def test_parallel_equilibrium_matches_serial():
    tasks = [("adiabatic", (fuel, 1.0, 0.0, 300.0, ct.one_atm)) for fuel in chem.QUICK_FUELS]
    assert io.ordered_map(chem._task, tasks, 2, chunksize=1) == io.ordered_map(chem._task, tasks, 1)


@pytest.mark.slow
def test_quick_smoke(tmp_path):
    assert chem.main(["--quick", "--workers", "2", "--out", tmp_path]) == 0
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert set(summary) == io.SUMMARY_KEYS
    assert summary["module"] == chem.MODULE
    assert summary["mode"] == "quick"
    assert summary["validation"]["passed"] is True
    assert summary["assumptions"]["water_heating_value_J_kg"]["value"] == 0.0
    assert summary["assumptions"]["mechanism_fallback"] is False
    assert summary["runtime_s"] < 120.0, "Quick mode exceeded SPEC two-core runtime budget"
    keys = summary["key_results"]
    assert {"w_SI_robust", "w_SI_marginal", "ignition_fits", "flame_speed_fits",
            "no_flame", "no_ignition", "validation_values"} <= keys.keys()
    assert keys["validation_values"]["CH4_T_ad"]["actual_K"] is not None
    for filename in ("ignition_fits.json", "flame_speed_fits.json"):
        fits = json.loads((tmp_path / filename).read_text(encoding="utf-8"))
        assert set(fits) == set(chem.FUELS)
        assert all(f["mode"] == "quick" for f in fits.values())
    for fuel in chem.QUICK_FUELS:
        assert keys["flame_speed_fits"][fuel]["status"] == "quick_linear"
        assert keys["ignition_fits"][fuel]["status"] == "fitted"
    for filename in ("adiabatic_flame_T.csv", "evaporative_cooling.csv", "flame_speed.csv",
                     "ignition_delay.csv", "adiabatic_flame_T.png", "evaporative_cooling.png",
                     "flame_speed.png", "ignition_delay.png"):
        assert (tmp_path / filename).stat().st_size > 0
