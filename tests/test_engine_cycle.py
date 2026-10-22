"""Module 03 engine_cycle tests (SPEC sections 0, 6 and 10).

Run on the Linux simulation server, not on the code-writing laptop. The fit
fixtures below are small synthetic dictionaries in the Module 02 file
schema: software fixtures, not data, so no test depends on Module 02 results.
"""

from dataclasses import replace
from functools import lru_cache
import importlib
import json
import math

import pytest

from sims.common import fuels, io


eng = importlib.import_module("sims.03_engine_cycle.run")
QUICK = replace(eng.DEFAULTS, step_rad=eng.DEFAULTS.quick_step_rad)
COARSE = replace(eng.DEFAULTS, step_rad=2.0 * eng.RAD)


def ignition_fixture(A=1.0e10, n=1.0, E=0.0, c=0.0):
    """Module 02 schema. Default A gives tau = 1e10 s*Pa / p: never knocks."""
    return dict(mode="full", status="fitted", A=A, n=n, E_J_per_mol=E, c=c,
                valid_T_K_range=[750.0, 1100.0], valid_w_range=[0.0, 0.9],
                valid_p_Pa_range=[40e5, 40e5], rms_ln_tau=0.0, number_of_points=24,
                pressure_unit="Pa", A_unit="s*Pa", pressure_exponent_fitted=False)


def flame_fixture(coefficients=(0.0, 0.0, -0.5, 0.5), w_range=(0.0, 0.8)):
    return dict(mode="full", status="fitted", coefficients_highest_first=list(coefficients),
                polynomial_degree=3, valid_w_range=list(w_range), rms_m_s=0.0,
                number_of_points=9, T_unburned_K=400.0, p_Pa=101325.0, phi=1.0,
                S_L_unit="m/s")


FAST_IGNITION = ignition_fixture(A=1.0)  # tau = 1 s*Pa / p: knocks at any phasing


def require_fuel(fuel):
    if fuel == "C2H5OH" and not fuels.SAN_DIEGO_PATH.is_file():
        pytest.skip("C2H5OH requires mechanisms/sandiego.yaml (SPEC fallback)")


@lru_cache(maxsize=None)
def point(fuel, cr, w, T_intake=320.0, fast=False, par=QUICK):
    ignition = FAST_IGNITION if fast else ignition_fixture()
    result = eng.run_point(fuel, cr, w, T_intake, ignition, flame_fixture(), par, "full",
                           "test_fixture", False)
    return result["point"], result["evo"]


def test_geometry():
    par = eng.DEFAULTS
    vd = eng.displacement(par)
    assert vd == pytest.approx(math.pi / 4 * 0.086**3)
    for cr in (9, 14, 18):
        assert eng.volume(-math.pi, cr, par) / eng.volume(0.0, cr, par) == pytest.approx(cr)
        assert eng.volume(0.0, cr, par) == pytest.approx(vd / (cr - 1))


def test_wiebe_parametrisation():
    par = eng.DEFAULTS
    ca50, duration = 8 * eng.RAD, 25 * eng.RAD
    for x in (0.1, 0.5, 0.9):
        assert eng.wiebe(eng.burn_angle(x, ca50, duration, par), ca50, duration, par) == pytest.approx(x)
    assert eng.burn_angle(0.5, ca50, duration, par) == pytest.approx(ca50)
    assert (eng.burn_angle(0.9, ca50, duration, par)
            - eng.burn_angle(0.1, ca50, duration, par)) == pytest.approx(duration)


def test_burn_duration_scaling_and_cap():
    par = eng.DEFAULTS
    assert eng.burn_duration(0.5, 0.5, par) == pytest.approx(25 * eng.RAD)
    assert eng.burn_duration(0.125, 0.5, par) == pytest.approx(50 * eng.RAD)  # (4)^0.5
    assert eng.burn_duration(1e-4, 0.5, par) == pytest.approx(80 * eng.RAD)  # cap


@pytest.mark.parametrize("gamma", [1.4, 1.3])
@pytest.mark.parametrize("cr", [9, 12, 18])
def test_ideal_otto_matches_analytic(cr, gamma):
    # SPEC section 10: engine integrator, adiabatic, instant burn, constant gamma.
    result = eng.ideal_otto(cr, gamma)
    assert result["analytic_efficiency"] == pytest.approx(1 - cr ** (1 - gamma))
    assert abs(result["efficiency"] - result["analytic_efficiency"]) <= 0.01
    assert result["passed"]
    assert abs(result["energy_closure_error_fraction"]) < 1e-4


def test_ignition_rate_units():
    fit = ignition_fixture(A=2.0, n=1.0, E=50000.0, c=1.0)
    T, p, w = 1000.0, 40e5, 0.5
    tau = 2.0 * p**-1.0 * math.exp(50000.0 / (8.314462618 * T)) * (1 + w)
    assert eng.ignition_rate(T, p, w, fit) == pytest.approx(1.0 / tau, rel=1e-6)


def _write_fits(directory, mode="full", **changes):
    ignition, flame = ignition_fixture(), flame_fixture()
    ignition.update(mode=mode, **changes)
    flame["mode"] = mode
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "ignition_fits.json").write_text(json.dumps({"CH4": ignition}), encoding="utf-8")
    (directory / "flame_speed_fits.json").write_text(json.dumps({"CH4": flame}), encoding="utf-8")


def test_reads_module02_fit_schema(tmp_path):
    _write_fits(tmp_path)
    ignition, flame, provenance = eng.read_fits(tmp_path, "full", ("CH4",))
    assert provenance["synthetic"] is False and provenance["per_fuel"]["CH4"] == "module_02"
    assert len(provenance["files"]) == 2 and all(len(f["sha256"]) == 64 for f in provenance["files"])
    sl, ref = eng.check_fits(ignition["CH4"], flame["CH4"], 0.6, "full")
    assert (sl, ref) == pytest.approx((0.2, 0.5))
    with pytest.raises(eng.PointUnavailable):  # no extrapolation of S_L(w)
        eng.check_fits(ignition["CH4"], flame["CH4"], 0.85, "full")
    with pytest.raises(eng.PointUnavailable):
        eng.check_fits(dict(ignition["CH4"], pressure_unit="bar"), flame["CH4"], 0.0, "full")
    with pytest.raises(eng.PointUnavailable):  # synthetic fits are quick-mode only
        eng.check_fits(eng.synthetic_ignition_fit("CH4"), flame["CH4"], 0.0, "full")


def test_full_refuses_quick_module02_fits(tmp_path):
    _write_fits(tmp_path, mode="quick")
    with pytest.raises(ValueError):
        eng.read_fits(tmp_path, "full", ("CH4",))


def test_full_mode_errors_without_fit_files(tmp_path):
    with pytest.raises(FileNotFoundError):
        eng.main(["--full", "--fits-dir", tmp_path / "missing", "--out", tmp_path / "out"])
    assert not (tmp_path / "out" / "summary.json").exists()


def test_quick_fallback_is_labelled(tmp_path):
    ignition, flame, provenance = eng.read_fits(tmp_path / "missing", "quick", eng.QUICK_FUELS)
    assert provenance["synthetic"] and provenance["label"] == "mode-quick-fallback"
    assert all(ignition[f]["status"] == "synthetic" == flame[f]["status"] for f in eng.QUICK_FUELS)
    assert "NOT for design" in provenance["warning"]


def test_retard_logic_steps_and_limit():
    par = eng.DEFAULTS

    def fake(knock_below_deg):
        def evaluate(ca50):
            return dict(gross_indicated_efficiency=0.4 - ca50, knock_integral_at_xb90=2.0,
                        knock=ca50 < knock_below_deg * eng.RAD - 1e-12)
        return evaluate

    never = eng.retard_search(fake(-100.0), par)
    assert never["retard_attempts"] == 1 and not never["knock_limited"]
    some = eng.retard_search(fake(13.0), par)  # 8 -> 10 -> 12 -> 14 CAD
    assert some["retard_attempts"] == 4 and not some["knock_limited"]
    assert some["efficiency_at_default_ca50"] == pytest.approx(0.4 - 8 * eng.RAD)
    always = eng.retard_search(fake(1000.0), par)  # 8 .. 30 in 2-CAD steps
    assert always["retard_attempts"] == 12 and always["knock_limited"]


def test_fast_ignition_fit_forces_knock_limit():
    row, _ = point("CH4", 10, 0.0, fast=True, par=COARSE)
    assert row["status"] == "computed", row["reason"]
    assert row["knock"] and row["knock_limited"]
    assert row["ca50_used_deg"] == pytest.approx(30.0)
    assert row["retard_attempts"] == 12
    assert not eng.eligible(row)


@pytest.mark.parametrize("fuel,cr,w", [("CH4", 10, 0.0), ("CH3OH", 14, 0.6), ("C2H5OH", 12, 0.4)])
def test_energy_closure_and_fuel_only_source(fuel, cr, w):
    require_fuel(fuel)
    row, evo = point(fuel, cr, w)
    assert row["status"] == "computed", row["reason"]
    assert abs(row["energy_closure_error_fraction"]) <= 0.02
    assert abs(row["integrator_identity_error_fraction"]) < 1e-5
    assert abs(row["intake_closure_error_J"]) < 1e-6 * row["fuel_energy_J"]
    # The only source is eta_c * m_fuel * LHV; water only absorbs latent heat.
    lhv = fuels.lhv(fuel)
    assert row["fuel_energy_J"] == pytest.approx(row["fuel_mass_kg"] * lhv)
    assert row["released_energy_J"] <= 0.98 * row["fuel_energy_J"] * (1 + 1e-12)
    assert row["evaporation_cylinder_J"] >= 0 and row["evaporation_intake_J"] >= 0
    sinks = (row["indicated_work_J"] + row["wall_heat_J"] + row["evaporation_cylinder_J"]
             + row["charge_energy_change_J"])
    assert sinks == pytest.approx(row["released_energy_J"], rel=1e-5)
    assert 0 < row["gross_indicated_efficiency"] < 1 - cr ** -0.4
    assert evo["T_K"] == pytest.approx(row["EVO_T_K"])
    assert sum(evo["composition"].values()) == pytest.approx(1.0, abs=1e-9)
    if w > 0:
        assert row["T_IVC_K"] < 320.0 and row["water_mass_kg"] > 0
        assert row["f_evap_intake_effective"] <= 0.5 + 1e-12


def test_water_lowers_peak_temperature_and_relative_no():
    rows = [point("CH3OH", 12, w)[0] for w in (0.0, 0.3, 0.6)]
    assert all(r["status"] == "computed" for r in rows), [r["reason"] for r in rows]
    rows = [dict(r) for r in rows]
    eng.add_relative_no(rows)
    for key in ("peak_temperature_K", "peak_burned_temperature_K", "NO_mol_per_J_fuel"):
        values = [r[key] for r in rows]
        assert values[0] > values[1] > values[2], (key, values)
    assert rows[0]["relative_NO"] == pytest.approx(1.0)
    assert rows[1]["relative_NO"] < 1.0 and rows[2]["relative_NO"] < rows[1]["relative_NO"]
    assert rows[0]["low_flame_temperature"] is False
    # Liquid water lowers the model-consistent flame temperature as well.
    assert rows[0]["peak_flame_temperature_K"] > rows[2]["peak_flame_temperature_K"]


def test_dry_efficiency_rises_with_compression_ratio():
    effs = [point("CH4", cr, 0.0)[0]["efficiency_at_default_ca50"] for cr in (9, 13, 17)]
    assert effs[0] < effs[1] < effs[2]
    assert all(0.30 <= e <= 0.50 for e in effs), effs


@pytest.mark.slow
def test_quick_run_outputs(tmp_path):
    out = tmp_path / "quick"
    code = eng.main(["--quick", "--workers", "2", "--out", out, "--fits-dir", tmp_path / "missing"])
    assert code == 0
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert set(summary) == io.SUMMARY_KEYS
    assert summary["module"] == eng.MODULE and summary["mode"] == "quick"
    assert summary["key_results"]["run_label"] == "mode-quick-fallback"
    assert summary["assumptions"]["fits"]["synthetic"] is True
    validation = summary["validation"]
    assert validation["passed"] and validation["ideal_otto_passed"] and validation["energy_closure_passed"]
    assert validation["max_abs_energy_closure_error_fraction"] <= 0.02
    for name in ("cycle_points.csv", "water_majority_map.csv", "ideal_otto.csv", "design_point.json",
                 "evo_states.json", "efficiency_vs_CR.png", "knock_limited_map.png",
                 "relative_NO_vs_w.png", "p_V_example.png", "p_theta_example.png"):
        assert (out / name).is_file(), name
    design = json.loads((out / "design_point.json").read_text(encoding="utf-8"))
    evo = json.loads((out / "evo_states.json").read_text(encoding="utf-8"))
    assert design["synthetic_fits"] and not design["use_for_design"]
    for fuel, entry in design["per_fuel"].items():
        if entry["water_majority"]:
            assert entry["water_majority"]["w"] > 0.5
            assert entry["water_majority"]["evo_state_key"] in evo
    assert all({"T_K", "p_Pa", "composition", "gas_mass_kg"} <= set(v) for v in evo.values())
    assert summary["runtime_s"] < 120
