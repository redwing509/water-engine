"""Energy audit validation, including deterministic Monte Carlo and smoke run."""

import importlib
import json

import numpy as np
import pytest

from sims.common.fuels import FUELS, SAN_DIEGO_PATH
from sims.common.io import SUMMARY_KEYS, ordered_map


audit = importlib.import_module("sims.01_energy_audit.run")


def test_hho_loop_gain_always_below_one():
    efficiencies, gains = audit.loop_gain_samples()
    assert len(gains) == 200_000
    assert np.all(gains == efficiencies.prod(axis=1))
    stats = audit.loop_gain_statistics(gains)
    assert 0 < stats["p50"] < stats["p99"] < stats["max"] < 1
    # The uniform box has an analytic maximum, independent of Monte Carlo luck.
    assert stats["max"] <= 0.45 * 0.75 * 0.80
    assert stats["theoretical_max"] == pytest.approx(0.27)
    assert stats["gap_to_one_max"] == pytest.approx(1 - stats["max"])


def test_seed_is_repeatable_and_quick_is_full_prefix():
    _, first = audit.loop_gain_samples(audit.QUICK_SAMPLES)
    _, second = audit.loop_gain_samples(audit.QUICK_SAMPLES)
    _, full = audit.loop_gain_samples()
    np.testing.assert_array_equal(first, second)
    np.testing.assert_array_equal(first, full[:len(first)])


def test_hho_kit_is_net_loss_and_ledger_closes():
    ledger = audit.hho_kit_ledger()
    p = audit.KitParameters()
    assert ledger["electrical_input_W"] == pytest.approx(20 * 13.8)
    assert ledger["net_shaft_effect_W"] < 0
    assert ledger["additional_primary_fuel_power_W"] > 0
    assert ledger["hydrogen_recovered_shaft_W"] == pytest.approx(p.eta_engine * ledger["hydrogen_lhv_power_W"])
    assert ledger["alternator_shaft_cost_W"] == pytest.approx(276 / p.eta_alternator)
    assert ledger["baseline_fuel_power_W"] == pytest.approx(15000 / p.eta_engine)
    # Added primary fuel plus recovered hydrogen must cover alternator shaft load.
    assert (ledger["additional_primary_fuel_power_W"] * p.eta_engine
            + ledger["hydrogen_recovered_shaft_W"]) == pytest.approx(ledger["alternator_shaft_cost_W"])


def test_faraday_hydrogen_flow():
    expected_kg_s = 20 / (2 * 96485.33212) * FUELS["H2"].molar_mass
    actual = audit.hho_kit_ledger()["hydrogen_mass_flow_kg_s"]
    assert actual == pytest.approx(expected_kg_s, rel=1e-9, abs=0)


def test_impossible_kit_inputs_rejected():
    with pytest.raises(ValueError, match="missing energy source"):
        audit.hho_kit_ledger(audit.KitParameters(voltage_V=0.1))


def test_parallel_fuel_table_matches_serial():
    names = ["H2", "CH4"]
    assert ordered_map(audit.heating_value_record, names, 2) == ordered_map(audit.heating_value_record, names, 1)


def test_quick_smoke(tmp_path):
    assert audit.main(["--quick", "--out", tmp_path]) == 0
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert set(summary) == SUMMARY_KEYS
    assert summary["module"] == "01_energy_audit"
    assert summary["mode"] == "quick"
    assert summary["validation"]["passed"] is True
    assert summary["assumptions"]["monte_carlo"]["samples"] == 20_000
    assert summary["assumptions"]["mechanism_fallback"] is (not SAN_DIEGO_PATH.is_file())
    assert summary["runtime_s"] >= 0
    if not SAN_DIEGO_PATH.is_file():
        assert summary["validation"]["lhv"]["C2H5OH"]["status"] == "skipped"
    for filename in ("heating_values.csv", "loop_gain_samples.csv", "loop_gain_statistics.csv",
                     "hho_kit_ledger.csv", "loop_gain_hist.png", "hho_kit_ledger.png"):
        assert (tmp_path / filename).stat().st_size > 0
