"""Module 04 six_stroke tests (SPEC sections 0 and 7).

Run on the Linux simulation server, not on the code-writing laptop. The
exhaust states are the module's labelled synthetic fixtures (complete CH4/air
products), so no test depends on Module 03 results.
"""

from dataclasses import replace
from functools import lru_cache
import importlib
import json
import math

import cantera as ct
from CoolProp.CoolProp import PropsSI
import pytest

from sims.common import fuels, io


six = importlib.import_module("sims.04_six_stroke.run")
PAR = replace(six.DEFAULTS, step_rad=six.DEFAULTS.quick_step_rad)
CONTEXTS = {"default": six.synthetic_context(),
            "cold": six.synthetic_context(T_evo_K=650.0, p_evo_Pa=1.3e5)}


@lru_cache(maxsize=None)
def loop(evc_deg, water_mg, heat="adiabatic", ctx="default"):
    return six.run_loop(CONTEXTS[ctx], evc_deg, water_mg * 1e-6, heat, PAR, keep_trace=True)


def row(*args):
    r = loop(*args)["row"]
    assert r["status"] == "computed", r["reason"]
    return r


def test_geometry_is_periodic():
    ctx = CONTEXTS["default"]
    vc = six.volume(six.TWO_PI, ctx)
    assert six.volume(0.0, ctx) == pytest.approx(vc)
    assert six.volume(3 * math.pi, ctx) / vc == pytest.approx(ctx["CR"])
    assert six.volume(math.pi, ctx) - vc == pytest.approx(six.displacement(ctx))


@pytest.mark.parametrize("evc", [220.0, 300.0])
def test_zero_water_gives_zero_extra_work(evc):
    r = row(evc, 0.0)
    assert r["pump_work_J"] == 0.0
    assert abs(r["extra_work_net_J"]) <= 2e-3 * r["trapped_enthalpy_J"]
    # The reversible gas spring returns to p_exh at the mirror angle 720 - EVC.
    assert r["EVO5_deg"] == pytest.approx(720.0 - evc, abs=8.0)
    # Wall heat loss can only cost work.
    w = row(evc, 0.0, "woschni")
    assert w["extra_work_net_J"] <= 2e-3 * w["trapped_enthalpy_J"]
    assert w["wall_heat_loss_J"] > 0.0


@pytest.mark.parametrize("case", [(220.0, 10.0, "adiabatic"), (220.0, 10.0, "woschni"),
                                  (300.0, 40.0, "adiabatic"), (260.0, 5.0, "woschni"),
                                  (200.0, 80.0, "adiabatic", "cold")])
def test_energy_ledger_closes(case):
    r = row(*case)
    assert abs(r["energy_closure_error_fraction"]) <= 0.01
    assert abs(r["integrator_identity_error_fraction"]) <= 1e-6
    # Ledger terms add up: water enthalpy in = loop work + wall heat + charge energy change.
    assert r["water_enthalpy_in_J"] == pytest.approx(
        r["loop_work_J"] + r["wall_heat_loss_J"] + r["charge_energy_change_J"],
        abs=1e-6 * r["trapped_enthalpy_J"])


def cantera_exergy(ctx, T, m, p0, T0=fuels.REFERENCE_T_K):
    gas = fuels.load_mechanism(ctx["fuel"], ctx["mechanism"])
    gas.TPY = T0, p0, ctx["composition"]
    u0, v0, s0 = gas.int_energy_mass, 1 / gas.density_mass, gas.entropy_mass
    gas.TPY = T, p0, ctx["composition"]
    return m * (gas.int_energy_mass - u0 + p0 * (1 / gas.density_mass - v0) - T0 * (gas.entropy_mass - s0))


@pytest.mark.parametrize("heat", ["adiabatic", "woschni"])
def test_extra_work_below_trapped_exergy(heat):
    ctx = CONTEXTS["default"]
    for evc in (200.0, 260.0, 320.0):
        for mg in (0.0, 1.0, 5.0, 20.0):
            r = row(evc, mg, heat)
            X = cantera_exergy(ctx, r["T_EVC_K"], r["trapped_mass_kg"], PAR.p_exhaust_Pa)
            assert r["trapped_exergy_J"] == pytest.approx(X, rel=1e-9)
            assert 0.0 < X < r["trapped_enthalpy_J"]
            assert r["extra_work_net_J"] <= r["exergy_bound_J"]
            assert r["extra_work_net_J"] <= X + r["water_tank_exergy_J"] + r["wall_heat_exergy_J"]


def test_water_state_saturation_branch():
    th = six.thermo(CONTEXTS["default"])
    u, p, f_liq, two = th.water(350.0, 1.0)  # rho_v,sat(350 K) ~ 0.26 kg/m3
    assert two and 0.0 < f_liq < 1.0
    assert p == pytest.approx(PropsSI("P", "T", 350.0, "Q", 1, "Water"), rel=1e-6)
    u_l = PropsSI("Umass", "T", 350.0, "Q", 0, "Water")
    u_v = PropsSI("Umass", "T", 350.0, "Q", 1, "Water")
    assert u == pytest.approx(u_l + (1 - f_liq) * (u_v - u_l), rel=1e-9)  # latent heat carried
    u1, p1, f1, two1 = th.water(350.0, 0.1)
    assert not two1 and f1 == 0.0 and p1 < p


def test_condensation_branch_triggers_cold_wet_case():
    res = loop(200.0, 80.0, "adiabatic", "cold")
    r, trace = res["row"], res["trace"]
    assert r["status"] == "computed", r["reason"]
    assert any(trace["two_phase"]), "cold wet expansion must reach saturation"
    assert r["two_phase_nodes"] > 0 and r["max_liquid_kg"] > 0.0
    assert r["condensed_kg"] > 0.0 and r["condensed_latent_heat_J"] > 0.0
    assert r["max_saturation_ratio"] == pytest.approx(1.0)
    assert abs(r["energy_closure_error_fraction"]) <= 0.01
    assert r["extra_work_net_J"] <= r["exergy_bound_J"]


def test_pump_work_is_subtracted():
    r = row(240.0, 10.0)
    v = 1.0 / PropsSI("Dmass", "T", PAR.water_T_K, "P", PAR.tank_p_Pa, "Water")
    expected = 10e-6 * v * (PAR.injection_p_Pa - PAR.tank_p_Pa) / PAR.pump_efficiency
    assert r["pump_work_J"] == pytest.approx(expected, rel=0.01)
    assert r["extra_work_net_J"] == r["extra_work_gross_J"] - r["pump_work_J"]
    assert r["extra_work_net_J"] < r["extra_work_gross_J"]
    # Better pump -> less work subtracted, same gross loop work.
    better = six.run_loop(CONTEXTS["default"], 240.0, 10e-6, "adiabatic", replace(PAR, pump_efficiency=1.0))["row"]
    assert better["extra_work_gross_J"] == pytest.approx(r["extra_work_gross_J"], rel=1e-12)
    assert better["pump_work_J"] == pytest.approx(r["pump_work_J"] * PAR.pump_efficiency, rel=1e-9)


def test_water_never_a_net_source():
    """W_extra never exceeds the energy the trapped exhaust brought in (SPEC section 0)."""
    for mg in (0.5, 2.0, 10.0, 40.0):
        r = row(220.0, mg)
        assert r["extra_work_net_J"] < r["trapped_enthalpy_J"]
        assert r["efficiency_six_stroke"] < 1.0
        assert r["combined_w"] > r["intake_water_kg"] / (r["intake_water_kg"] + CONTEXTS["default"]["fuel_mass_kg"])


def module03_files(directory, ctx):
    """Minimal files in the Module 03 writer schema (design_point.json, evo_states.json)."""
    key = "CH4/CR=14/w=0.6/T_intake=320"
    evo = {key: dict(key=key, fuel="CH4", CR=14, w=0.6, T_intake_K=320.0, crank_angle_deg=140.0,
                     volume_m3=ctx["V_evo_m3"], T_K=ctx["T_evo_K"], p_Pa=ctx["p_evo_Pa"],
                     gas_mass_kg=ctx["gas_mass_evo_kg"], liquid_water_kg=0.0,
                     composition_basis="mass_fraction", mechanism="gri30.yaml", mechanism_fallback=False,
                     composition=ctx["composition"], unburned_mass_fraction=0.0,
                     fuel_mass_kg=ctx["fuel_mass_kg"], water_mass_kg=ctx["intake_water_kg"],
                     fuel_energy_J=ctx["fuel_energy_J"], indicated_work_J=ctx["four_stroke_work_J"],
                     ca50_used_deg=8.0, synthetic_fits=False)}
    design = dict(module="03_engine_cycle", mode="full", synthetic_fits=False, validation_passed=True,
                  use_for_design=True, warning=None,
                  engine=dict(bore_m=0.086, stroke_m=0.086, rod_m=0.145, rpm=2000.0, ivc_deg=-180.0,
                              evo_deg=140.0, residual_fraction=0.05, p_ivc_Pa=1e5, phi=1.0),
                  per_fuel={}, recommended=dict(key=key), recommended_evo_state_key=key,
                  evo_states_file="evo_states.json")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "design_point.json").write_text(json.dumps(design), encoding="utf-8")
    (directory / "evo_states.json").write_text(json.dumps(evo), encoding="utf-8")
    return key


def test_reads_module03_schema(tmp_path):
    ctx = CONTEXTS["default"]
    key = module03_files(tmp_path / "m03", ctx)
    got = six.read_cycle(tmp_path / "m03", "full")
    assert got["key"] == key and not got["synthetic"] and got["label"] == "full"
    assert got["four_stroke_work_J"] == ctx["four_stroke_work_J"]
    assert got["composition"] == pytest.approx(ctx["composition"])
    assert len(got["files"]) == 2


def test_full_requires_module03_files(tmp_path):
    with pytest.raises(FileNotFoundError):
        six.main(["--full", "--cycle-dir", tmp_path / "missing", "--out", tmp_path / "out"])


def test_design_points_table(tmp_path, capsys):
    """SPEC item 2: the six-stroke is evaluated at the real Module 03 design points and the
    requested table (point | extra work % | water mg/cycle | combined w) is written."""
    ctx = CONTEXTS["default"]
    key = module03_files(tmp_path / "m03", ctx)
    # The synthetic fixture is a CH4/CR=14/w=0.6 point; per_fuel must carry the three categories
    # the item 2 table reads (best dry, best overall, water majority) for CH3OH and C2H5OH.
    dp = tmp_path / "m03" / "design_point.json"
    evo = json.loads((tmp_path / "m03" / "evo_states.json").read_text(encoding="utf-8"))
    design = json.loads(dp.read_text(encoding="utf-8"))
    for fuel in ("CH3OH", "C2H5OH"):
        for label, rec in (("best_dry", dict(CR=14, w=0.0, T_intake_K=320.0)),
                           ("best_overall", dict(CR=14, w=0.3, T_intake_K=320.0)),
                           ("water_majority", dict(CR=14, w=0.6, T_intake_K=320.0))):
            k = f"{fuel}/CR={rec['CR']}/w={rec['w']}/T_intake={rec['T_intake_K']:.0f}"
            evo[k] = dict(key=k, fuel=fuel, CR=rec["CR"], w=rec["w"], T_intake_K=rec["T_intake_K"],
                          crank_angle_deg=140.0, volume_m3=ctx["V_evo_m3"], T_K=ctx["T_evo_K"],
                          p_Pa=ctx["p_evo_Pa"], gas_mass_kg=ctx["gas_mass_evo_kg"],
                          liquid_water_kg=0.0, composition_basis="mass_fraction",
                          mechanism="gri30.yaml", mechanism_fallback=False,
                          composition=ctx["composition"], unburned_mass_fraction=0.0,
                          fuel_mass_kg=ctx["fuel_mass_kg"], water_mass_kg=ctx["intake_water_kg"],
                          fuel_energy_J=ctx["fuel_energy_J"],
                          indicated_work_J=ctx["four_stroke_work_J"], ca50_used_deg=8.0,
                          synthetic_fits=False)
            design.setdefault("per_fuel", {}).setdefault(fuel, {})[label] = dict(
                key=k, fuel=fuel, CR=rec["CR"], w=rec["w"], T_intake_K=rec["T_intake_K"],
                gross_indicated_efficiency=0.40, peak_pressure_Pa=90e5,
                EVO_T_K=1200.0, EVO_p_Pa=5.0e5)
    dp.write_text(json.dumps(design), encoding="utf-8")
    (tmp_path / "m03" / "evo_states.json").write_text(json.dumps(evo), encoding="utf-8")
    out = tmp_path / "out"
    assert six.main(["--full", "--workers", "1", "--out", out, "--cycle-dir", tmp_path / "m03",
                     "--design-points"]) == 0
    csv_path = out / "six_stroke_design_points.csv"
    assert csv_path.is_file()
    rows = list(csv.DictReader(csv_path.open(encoding="utf-8")))
    labels = {r["label"] for r in rows}
    assert {"CH3OH/best_dry", "CH3OH/best_overall", "CH3OH/water_majority",
            "C2H5OH/best_dry", "C2H5OH/best_overall", "C2H5OH/water_majority",
            "hot-dry validation"} <= labels
    for r in rows:
        assert r["status"] == "computed", r
        assert r["extra_work_pct_of_four_stroke"] != ""
        assert r["water_mg_per_cycle"] != ""
        assert r["combined_w"] != ""
    # The hot-dry validation case is a dry point: injected water is zero, so extra work is zero.
    hd = next(r for r in rows if r["label"] == "hot-dry validation")
    assert float(hd["water_mg_per_cycle"]) == 0.0
    assert abs(float(hd["extra_work_pct_of_four_stroke"])) < 1e-9
    # The table is also carried into the module 03 summary.json (SPEC item 2 report).
    s = json.loads((tmp_path / "m03" / "summary.json").read_text(encoding="utf-8"))
    assert s["key_results"]["six_stroke_design_points"]


@pytest.mark.slow
def test_quick_smoke(tmp_path):
    out = tmp_path / "quick"
    assert six.main(["--quick", "--workers", "2", "--out", out, "--cycle-dir", tmp_path / "missing"]) == 0
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert set(summary) == io.SUMMARY_KEYS
    assert summary["mode"] == "quick-fallback"
    assert summary["validation"]["passed"]
    assert summary["key_results"]["synthetic_exhaust_state"]
    for name in ("six_stroke_sweep.csv", "extra_work_vs_water.png", "pv_strokes_5_6.png"):
        assert (out / name).is_file()
