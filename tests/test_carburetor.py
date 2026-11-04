"""Module 06: physical limits, rounded jet design, source contract and heat ledger."""

from dataclasses import replace
import importlib
import json
import math
from pathlib import Path

import pytest

carb = importlib.import_module("sims.06_carburetor.run")
ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT/"results/03_engine_cycle"


@pytest.fixture(scope="module")
def design():
    return carb.build_design(INPUT)


@pytest.mark.parametrize("option", ["A", "B"])
def test_rounded_jets_meet_three_percent_afr(design, option):
    row = next(r for r in carb.operating_point(design, 2000, 1) if r["option"] == option)
    # Independent stoichiometry: CH3OH + 1.5*(O2 + 3.76 N2).
    afr = 1.5*(31.998+3.76*28.014)/32.042
    assert abs(row["AFR"]/afr-1) <= 0.03
    assert row["WFR"] == pytest.approx(1.5, rel=0.03)
    assert row["idle_fuel_mass_flow_kg_s"] == 0


def test_air_demand_scales_exactly_500cc_and_four_stroke(design):
    point, _, engine, _ = carb.read_inputs(INPUT)
    expected = point["air_mass_kg"]*(500e-6/engine["displacement_m3"])*2000/120
    assert design["design_point"]["air_mass_flow_kg_s"] == pytest.approx(expected)
    peak = design["venturi"]["maximum_event_air_mass_flow_kg_s"]
    assert peak == pytest.approx(expected*2/0.25)
    assert 0 < design["venturi"]["maximum_mach"] <= 0.30


def test_isentropic_venturi_matches_incompressible_limit_and_chokes():
    p = carb.DEFAULTS
    d, m = 0.03, 0.001
    state = carb.venturi_state(m, d)
    rho = p.ambient_Pa/(carb.R_AIR*p.tank_T_K)
    bernoulli = 0.5/rho*(m/(p.venturi_Cd*carb.area(d)))**2
    assert state["signal_Pa"] == pytest.approx(bernoulli, rel=0.001)
    with pytest.raises(ValueError, match="sonic"):
        carb.venturi_state(1.01*carb.area(d)*carb.mass_flux(1), d)


def test_float_lift_stops_flow_and_viscosity_reduces_flow():
    liquid = carb.LIQUIDS["blend"]
    threshold = liquid["density_kg_m3"]*carb.G*0.006
    assert carb.jet_flow(0.002, threshold, liquid, 0.006) == 0
    assert carb.jet_flow(0.002, threshold/2, liquid, 0.006) == 0
    m = carb.jet_flow(0.002, 1000, liquid, 0.006)
    inviscid = carb.jet_flow(0.002, 1000, dict(liquid, viscosity_Pa_s=0), 0.006)
    expected = 0.75*carb.area(0.002)*math.sqrt(2*liquid["density_kg_m3"]*(1000-threshold))
    assert inviscid == pytest.approx(expected)
    assert 0 < m < inviscid


@pytest.mark.parametrize("signal", [100, 500, 1500, 6000])
@pytest.mark.parametrize("opened", [0, 0.5, 1])
def test_option_b_matches_jet_area_formula(design, signal, opened):
    f, w, power = [design["option_B"][k] for k in ("fuel", "water", "water_power_valve")]
    fd, wd, pd = f["main_jet_diameter_m"], w["main_jet_diameter_m"], power["jet_diameter_m"]
    hf, hw = f["float_level_below_throat_m"], w["float_level_below_throat_m"]
    mass_f = carb.jet_flow(fd, signal, carb.LIQUIDS["fuel"], hf)
    mass_w = (carb.jet_flow(wd, signal, carb.LIQUIDS["water"], hw)
              +opened*carb.jet_flow(pd, signal, carb.LIQUIDS["water"], hw))
    formula = carb.wfr_area_formula(fd, [(wd, 1), (pd, opened)], signal, hf, hw)
    assert mass_w/mass_f == pytest.approx(formula, rel=1e-12)
    # Independently check the equal-pressure-head reduction using sized effective Cds.
    cf = carb.effective_cd(fd, signal, carb.LIQUIDS["fuel"], hf)
    cw = carb.effective_cd(wd, signal, carb.LIQUIDS["water"], hw)
    cp = carb.effective_cd(pd, signal, carb.LIQUIDS["water"], hw)
    equal_head = (cw*wd**2+opened*cp*pd**2)/(cf*fd**2)*math.sqrt(996.5/785)
    assert formula == pytest.approx(equal_head, rel=1e-12)


def test_unequal_geometric_heads_require_pressure_correction():
    # Identical 6 mm levels are NOT equal pressure lifts for different densities.
    fd, wd, signal, head = 0.002, 0.002, 100, 0.006
    general = carb.wfr_area_formula(fd, [(wd, 1)], signal, head, head)
    cf = carb.effective_cd(fd, signal, carb.LIQUIDS["fuel"], head)
    cw = carb.effective_cd(wd, signal, carb.LIQUIDS["water"], head)
    equal_head = cw/cf*math.sqrt(996.5/785)
    assert abs(general/equal_head-1) > 0.1


def test_power_valve_opens_as_vacuum_falls():
    assert carb.valve_opening(70000) == carb.valve_opening(25000) == 0
    assert carb.valve_opening(20000) == 0.5
    assert carb.valve_opening(15000) == carb.valve_opening(1325) == 1


def test_idle_and_wot_circuit_routing(design):
    idle = carb.operating_point(design, 1000, 0.3)
    for row in idle:
        assert row["main_fuel_mass_flow_kg_s"] == 0
        assert row["idle_fuel_mass_flow_kg_s"] > 0
        assert abs(row["AFR"]/design["design_point"]["stoichiometric_AFR"]-1) < 0.03
    assert idle[1]["water_power_valve_open_fraction"] == 0
    assert idle[1]["WFR"] == pytest.approx(0.5, rel=0.05)
    assert carb.operating_point(design, 2000, 1)[1]["water_power_valve_open_fraction"] == 1


def test_needle_seats_have_mean_flow_capacity(design):
    ref = design["design_point"]
    for circuit, demand in ((design["option_A"], ref["fuel_mass_flow_kg_s"]+ref["water_mass_flow_kg_s"]),
                             (design["option_B"]["fuel"], ref["fuel_mass_flow_kg_s"]),
                             (design["option_B"]["water"], ref["water_mass_flow_kg_s"])):
        assert circuit["needle_capacity_kg_s"] >= demand*2*1.5


def test_heat_ledger_and_evo_reference(design):
    heat = design["heat_balance"]
    assert heat["recovered_exhaust_heat_kW"] == pytest.approx(0.6*heat["exhaust_sensible_available_kW"])
    assert heat["intake_heating_needed_kW"] == pytest.approx(sum(heat[k] for k in (
        "air_sensible_kW", "methanol_vaporization_and_sensible_kW", "water_vaporization_and_sensible_kW")))
    assert heat["margin_kW"] == pytest.approx(heat["recovered_exhaust_heat_kW"]-heat["intake_heating_needed_kW"])
    assert heat["passed"] is False and heat["status"] == "FAIL"
    assert heat["module03_compatible"]["passed"] is True
    # Independent broad physical sanity bounds, not golden implementation output.
    assert 6 < heat["intake_heating_needed_kW"] < 8
    assert 4 < heat["recovered_exhaust_heat_kW"] < 6
    assert 850 < heat["EVO_T_K"] < 900


def test_hx_zero_and_ideal_effectiveness_switch_result():
    point, evo, engine, _ = carb.read_inputs(INPUT)
    zero = carb.heat_balance(point, evo, engine, replace(carb.DEFAULTS, hx_effectiveness=0))
    ideal = carb.heat_balance(point, evo, engine, replace(carb.DEFAULTS, hx_effectiveness=1))
    assert zero["recovered_exhaust_heat_kW"] == 0 and not zero["passed"]
    assert ideal["passed"]
    assert ideal["intake_heating_needed_kW"] == zero["intake_heating_needed_kW"]


def test_thermodynamic_integration_and_bounds():
    mechanism = ROOT/"mechanisms/sandiego.yaml"
    cp = carb.sensible_h("N2", 300, 301, mechanism)
    assert 1030 < cp < 1050  # N2 near 300 K, J/(kg K)
    low = carb.sensible_h("N2", 300, 1000, mechanism)
    high = carb.sensible_h("N2", 1000, 1200, mechanism)
    assert carb.sensible_h("N2", 300, 1200, mechanism) == pytest.approx(low+high)
    assert carb.sensible_h("N2", 301, 300, mechanism) == -cp
    with pytest.raises(ValueError, match="range"):
        carb.sensible_h("N2", 100, 301, mechanism)


def test_nukiyama_tanasawa_units_against_water_example():
    # EPA report example: water, velocity 80.6 m/s, Ql/Qg=1.33e-3,
    # predicts approximately 0.0107 cm = 107 um (rounded source properties).
    water = dict(density_kg_m3=1000, viscosity_Pa_s=0.001, surface_tension_N_m=0.072)
    assert carb.smd(80.6, water, 1.33e-3, 1) == pytest.approx(107e-6, rel=0.03)


def test_d_squared_evaporation_scaling():
    small = carb.evaporation(50e-6, carb.LIQUIDS["water"], 2437000, 360)
    big = carb.evaporation(100e-6, carb.LIQUIDS["water"], 2437000, 360)
    assert big["evaporation_time_s"] == 4*small["evaporation_time_s"]
    assert carb.evaporation(50e-6, carb.LIQUIDS["water"], 2437000, 300)["evaporation_time_s"] is None


@pytest.mark.parametrize("field", ["use_for_design", "validation_passed", "synthetic_fits"])
def test_rejects_unsuitable_module03_input(tmp_path, field):
    for name in ("design_point.json", "evo_states.json"):
        (tmp_path/name).write_bytes((INPUT/name).read_bytes())
    path = tmp_path/"design_point.json"
    data = json.loads(path.read_text())
    data[field] = field == "synthetic_fits"
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="validated"):
        carb.build_design(tmp_path)


def test_rejects_wrong_design_point(tmp_path):
    for name in ("design_point.json", "evo_states.json"):
        (tmp_path/name).write_bytes((INPUT/name).read_bytes())
    path = tmp_path/"design_point.json"
    data = json.loads(path.read_text())
    data["per_fuel"]["CH3OH"]["water_majority"]["CR"] = 18
    path.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="mismatch"):
        carb.build_design(tmp_path)


def test_full_output_schema_and_cad_handoff(tmp_path):
    assert carb.main(["--full", "--out", str(tmp_path)]) == 0
    result = json.loads((tmp_path/"carb_design.json").read_text())
    assert result["operating_map"]["rows"] == 210
    assert result["operating_map"]["full_map_AFR_within_3pct"] is False
    # option_A_premix, option_B_fuel, option_B_water, option_B_water_power
    assert len(result["design_table"]) == 4
    for name in ("phi_map.png", "WFR_map.png"):
        assert (tmp_path/name).read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert set(json.loads((tmp_path/"summary.json").read_text())) == carb.io.SUMMARY_KEYS
    cad = importlib.import_module("sims.07_cad.run")
    loaded = cad.load_design(tmp_path/"carb_design.json")
    assert loaded.throat_mm == pytest.approx(1000*result["venturi"]["throat_diameter_m"])
