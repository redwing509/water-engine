"""CAD input validation plus actual solid/export checks when CadQuery exists."""

from dataclasses import replace
import importlib
import json
import struct
import xml.etree.ElementTree as ET

import pytest

cad = importlib.import_module("sims.07_cad.run")


@pytest.fixture
def sizing_input(tmp_path):
    # Deliberately synthetic unit-test dimensions, never a production fallback.
    circuit = dict(main_jet_diameter_m=0.0017, idle_jet_diameter_m=0.0005,
                   needle_seat_diameter_m=0.0025, float_level_m=-0.006,
                   jet_length_m=0.002, vacuum_power_valve=False)
    air = dict(venturi_throat_diameter_m=0.0247, venturi_inlet_diameter_m=0.036,
               throttle_bore_diameter_m=0.034)
    water = dict(circuit, liquid="water", idle_jet_diameter_m=0.0, vacuum_power_valve=True)
    data = dict(schema_version=1, design_point=dict(fuel="CH3OH"),
                assumptions=dict(parameters=dict(power_valve_starts_vacuum_Pa=30000,
                                                 power_valve_full_vacuum_Pa=10000)),
                options=dict(A=dict(air, circuits=[dict(circuit, liquid="wet_methanol_w0.6")]),
                             B=dict(air, circuits=[dict(circuit, liquid="methanol"), water])))
    path = tmp_path / "carb_design.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path, data


def test_dimensions_convert_metres_to_mm(sizing_input):
    d = cad.load_design(sizing_input[0])
    assert d.throat_mm == pytest.approx(24.7)
    assert d.wet_methanol.main_jet_mm == pytest.approx(1.7)
    assert d.water.float_head_mm == pytest.approx(6)


@pytest.mark.parametrize("value", [None, True, "0.025", 0, -1, float("nan"), float("inf")])
def test_rejects_bad_dimension(value):
    with pytest.raises(ValueError):
        cad.dimension({"throat_diameter_m": value}, "throat_diameter")


def test_explicit_units_and_conflicts():
    assert cad.dimension({"d_mm": 24.7}, "d") == 24.7
    assert cad.dimension({"d_m": 0.0247, "d_mm": 24.7}, "d") == pytest.approx(24.7)
    with pytest.raises(ValueError, match="Conflicting"):
        cad.dimension({"d_m": 0.0247, "d_mm": 25.7}, "d")
    with pytest.raises(ValueError, match="Missing dimension"):
        cad.dimension({"d": 24.7}, "d")


def test_missing_input_does_not_invent_design(tmp_path):
    with pytest.raises(FileNotFoundError, match="Run Module 06"):
        cad.load_design(tmp_path / "missing.json")


@pytest.mark.parametrize("field", ["validation_passed", "use_for_design"])
def test_rejects_unvalidated_design(sizing_input, field):
    path, data = sizing_input
    data[field] = False
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="unsuitable"):
        cad.load_design(path)


def test_requires_wet_methanol(sizing_input):
    path, data = sizing_input
    data["design_point"]["fuel"] = "C2H5OH"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="CH3OH"):
        cad.load_design(path)


def test_requires_all_sized_features(sizing_input):
    path, data = sizing_input
    del data["options"]["B"]["circuits"][1]["vacuum_power_valve"]
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="schema"):
        cad.load_design(path)


@pytest.fixture(scope="module")
def cq():
    return pytest.importorskip("cadquery", reason="Install requirements-cad.txt for CAD geometry checks")


@pytest.mark.parametrize("option", ["A", "B"])
def test_exports_and_step_reimport(cq, sizing_input, tmp_path, option):
    d = cad.load_design(sizing_input[0])
    result = cad.export_option(d, option, tmp_path)
    assert result["passed"]
    assert result["step_reimport_valid"]
    assert result["step_throat_mm"] == pytest.approx(d.throat_mm, abs=0.1)
    assert result["solid_count"] == result["step_solid_count"]
    assert result["step_volume_relative_error"] < 1e-6
    svg = ET.parse(tmp_path / f"carb_option{option}.svg").getroot()
    assert svg.tag.endswith("svg")
    assert any(node.tag.endswith("path") for node in svg.iter())
    stl = (tmp_path / f"carb_option{option}.stl").read_bytes()
    facets = struct.unpack_from("<I", stl, 80)[0]
    assert facets > 100
    assert len(stl) == 84 + facets * 50


def test_throat_is_measured_from_geometry_not_input(cq, sizing_input):
    original = cad.load_design(sizing_input[0])
    changed = replace(original, throat_mm=original.throat_mm+1.25)
    parts = cad.build_model(changed, "A")
    shape = cq.Compound.makeCompound(list(parts.values()))
    actual = cad.measure_throat(shape, cad.layout(changed)["throat_z_mm"])
    assert actual == pytest.approx(changed.throat_mm, abs=0.1)
    assert abs(actual-original.throat_mm) > 0.1


def test_option_b_has_separate_bowls_and_vacuum_valve(cq, sizing_input):
    parts = cad.build_model(cad.load_design(sizing_input[0]), "B")
    assert {"fuel_float", "water_float", "fuel_bowl_lid", "water_bowl_lid",
            "water_power_valve_diaphragm", "vacuum_signal_tube",
            "water_power_valve_poppet_open"} <= parts.keys()
    assert all(shape.isValid() and shape.Volume() > 0 for shape in parts.values())


def test_no_throat_measurement_on_unrelated_geometry(cq):
    with pytest.raises(ValueError, match="No analytic throat"):
        cad.measure_throat(cq.Workplane("XY").box(30, 30, 30).val(), 20)
