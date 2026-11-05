"""Independent stoichiometry and Hess-cycle checks for all aluminum products."""

import importlib
import json

import pytest

from sims.common.fuels import FUELS, lhv
from sims.common.io import SUMMARY_KEYS


aluminum = importlib.import_module("sims.05_aluminum_water.run")


@pytest.mark.parametrize("reaction", aluminum.REACTIONS, ids=lambda r: r.name)
def test_hydrogen_yield_and_positive_energies(reaction):
    row = aluminum.reaction_ledger(reaction)
    expected = 3 * FUELS["H2"].molar_mass / (2 * aluminum.M_AL_KG_MOL)
    assert row["hydrogen_kg_per_kg_Al"] == pytest.approx(expected, rel=1e-12)
    assert row["heat_released_J_kg_Al"] > 0
    assert row["hydrogen_lhv_energy_J_kg_Al"] > 0
    assert row["total_energy_J_kg_Al"] > row["heat_released_J_kg_Al"]
    water = reaction.water_mol * FUELS["H2O"].molar_mass / (2 * aluminum.M_AL_KG_MOL)
    assert row["water_consumed_kg_per_kg_Al"] == pytest.approx(water)
    assert row["water_mass_fraction_reactants"] == pytest.approx(water / (1 + water))


def test_energy_order():
    rows = [aluminum.reaction_ledger(r) for r in aluminum.REACTIONS]
    for key in ("heat_released_J_kg_Al", "total_energy_J_kg_Al"):
        assert rows[0][key] > rows[1][key] > rows[2][key] > 0


@pytest.mark.parametrize("reaction", aluminum.REACTIONS, ids=lambda r: r.name)
def test_enthalpy_bookkeeping_and_water_is_not_energy_source(reaction):
    row = aluminum.reaction_ledger(reaction)
    # Independent formation-enthalpy balance per mol of reaction, including
    # the oxygen supplied when the produced H2 is subsequently burned.
    basis = 2 * aluminum.M_AL_KG_MOL
    hf = aluminum.FORMATION_ENTHALPIES_J_MOL
    reactants = reaction.water_mol * hf["H2O(l)"]
    products = reaction.product_mol * hf[reaction.product]
    expected_heat = (reactants - products) / basis
    assert row["heat_released_J_kg_Al"] == pytest.approx(expected_heat, rel=1e-12)
    hydrogen_combustion = 3 * FUELS["H2"].molar_mass * lhv("H2")
    expected_combined = (reactants - products + hydrogen_combustion) / basis
    assert abs(row["total_energy_J_kg_Al"] - expected_combined) / expected_combined < 1e-6
    assert row["closure_relative_error"] < 1e-6
    # The oxidation energy must pay BOTH the heat output and water splitting.
    assert row["heat_released_J_kg_Al"] + row["water_splitting_cost_J_kg_Al"] == pytest.approx(row["aluminum_oxidation_energy_J_kg_Al"], rel=1e-12)
    assert row["total_energy_J_kg_Al"] + row["water_vaporization_penalty_J_kg_Al"] == pytest.approx(row["aluminum_oxidation_energy_J_kg_Al"], rel=1e-12)
    assert row["water_cycle_net_energy_J_kg_Al"] < 0
    assert abs(row["water_heating_value_J_kg"]) < 1.0
    assert aluminum.batch_energy(reaction, aluminum_mass_kg=0, water_mass_kg=1000) == 0
    assert aluminum.batch_energy(reaction, aluminum_mass_kg=1, water_mass_kg=0) == 0
    assert aluminum.batch_energy(reaction, 1, row["water_consumed_kg_per_kg_Al"]) == pytest.approx(row["total_energy_J_kg_Al"])
    assert aluminum.batch_energy(reaction, 1, row["water_consumed_kg_per_kg_Al"] / 2) == pytest.approx(row["total_energy_J_kg_Al"] / 2)


@pytest.mark.parametrize("reaction", aluminum.REACTIONS, ids=lambda r: r.name)
def test_smelting_comparison(reaction):
    row = aluminum.reaction_ledger(reaction)
    total = row["total_energy_J_kg_Al"]
    assert row["round_trip_energy_efficiency_min"] == pytest.approx(total / (15 * 3.6e6))
    assert row["round_trip_energy_efficiency_max"] == pytest.approx(total / (13 * 3.6e6))
    assert 0 < row["round_trip_energy_efficiency_min"] < row["round_trip_energy_efficiency_max"] < 1


def test_quick_smoke(tmp_path):
    assert aluminum.main(["--quick", "--out", tmp_path]) == 0
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert set(summary) == SUMMARY_KEYS
    assert summary["module"] == "05_aluminum_water"
    assert summary["mode"] == "quick"
    assert summary["validation"]["passed"] is True
    assert summary["assumptions"]["formation_enthalpies"]
    assert len(summary["key_results"]["reactions"]) == 3
    assert (tmp_path / "aluminum_water_reactions.csv").stat().st_size > 0
    assert (tmp_path / "aluminum_water_energy.png").stat().st_size > 0
