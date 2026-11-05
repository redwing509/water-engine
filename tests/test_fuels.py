"""SPEC §10 LHV targets and §1 mixture/phase conventions."""

import cantera as ct
import pytest

from sims.common import fuels


@pytest.mark.parametrize("fuel,target_MJ_kg", [
    ("H2", 120.0), ("CH4", 50.0), ("CH3OH", 19.9), ("C2H5OH", 26.8),
])
def test_lhv_published_targets(fuel, target_MJ_kg):
    if fuel == "C2H5OH" and not fuels.SAN_DIEGO_PATH.is_file():
        pytest.skip("C2H5OH requires mechanisms/sandiego.yaml; file is absent")
    assert fuels.lhv(fuel) / 1e6 == pytest.approx(target_MJ_kg, rel=0.02)


def test_water_has_zero_heating_value():
    assert abs(fuels.lhv("H2O")) / 1e6 < 1e-6


def test_liquid_methanol_correction():
    gas = ct.Solution("gri30.yaml")
    gas.TP = 298.15, ct.one_atm
    h = gas.standard_enthalpies_RT * ct.gas_constant * gas.T
    gas_heat_J_kg = (h[gas.species_index("CH3OH")] + 1.5 * h[gas.species_index("O2")]
                    - h[gas.species_index("CO2")] - 2 * h[gas.species_index("H2O")]) / gas.molecular_weights[gas.species_index("CH3OH")]
    assert gas_heat_J_kg - fuels.lhv("CH3OH", "gri30.yaml") == pytest.approx(fuels.FUELS["CH3OH"].h_fg, rel=1e-12)


@pytest.mark.parametrize("fuel,oxygen", [("H2", 0.5), ("CH4", 2.0), ("CH3OH", 1.5)])
@pytest.mark.parametrize("phi", [0.8, 1.0, 1.2])
@pytest.mark.parametrize("water_fraction", [0.0, 0.5, 0.9])
def test_mixture_preserves_phi_and_mass_definition(fuel, oxygen, phi, water_fraction):
    composition = fuels.mixture(fuel, phi, water_fraction, "gri30.yaml")
    gas = ct.Solution("gri30.yaml")
    gas.TPX = 298.15, ct.one_atm, composition
    assert oxygen * composition[fuel] / composition["O2"] == pytest.approx(phi)
    assert composition["N2"] / composition["O2"] == pytest.approx(3.76)
    fuel_mass = gas[fuel].Y[0]
    water_mass = gas["H2O"].Y[0]
    assert water_mass / (water_mass + fuel_mass) == pytest.approx(water_fraction)
    dry_air_mass = gas["O2"].Y[0] + gas["N2"].Y[0]
    assert dry_air_mass / fuel_mass * phi == pytest.approx(fuels.stoich_air_fuel_ratio(fuel))


@pytest.mark.parametrize("phi,w", [(0, 0), (-1, 0), (float("nan"), 0),
                                  (1, -0.1), (1, 1), (1, float("inf"))])
def test_invalid_mixture_parameters(phi, w):
    with pytest.raises(ValueError):
        fuels.mixture("CH4", phi, w)


def test_water_cannot_be_used_as_mixture_fuel():
    with pytest.raises(ValueError, match="Water is not a fuel"):
        fuels.mixture("H2O", 1, 0)


def test_missing_mechanism_fallback(monkeypatch, tmp_path):
    monkeypatch.setattr(fuels, "SAN_DIEGO_PATH", tmp_path / "absent.yaml")
    assert fuels.select_mechanism("CH3OH").mechanism_fallback is True
    assert fuels.select_mechanism("CH3OH").name == "gri30.yaml"
    assert fuels.select_mechanism("H2").mechanism_fallback is False
    with pytest.raises(fuels.MechanismUnavailable, match="file is absent"):
        fuels.lhv("C2H5OH")


def test_present_san_diego_selected_for_both_alcohols(monkeypatch, tmp_path):
    path = tmp_path / "sandiego.yaml"
    path.write_text("test presence only", encoding="utf-8")
    monkeypatch.setattr(fuels, "SAN_DIEGO_PATH", path)
    for fuel in ("CH3OH", "C2H5OH"):
        selected = fuels.select_mechanism(fuel)
        assert selected.name == "mechanisms/sandiego.yaml"
        assert selected.mechanism_fallback is False


def test_registry_phase_properties():
    for fuel in ("H2", "CH4"):
        assert fuels.FUELS[fuel].state == "gas"
        assert fuels.FUELS[fuel].liquid_density is None
        assert fuels.FUELS[fuel].h_fg is None
    for fuel in ("CH3OH", "C2H5OH"):
        assert fuels.FUELS[fuel].liquid_density > 0
        assert fuels.FUELS[fuel].h_fg > 0
