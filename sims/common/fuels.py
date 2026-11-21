"""Fuel registry and complete-combustion accounting in SI units.

Heating values refer to the registered fuel phase at 298.15 K and gaseous
product water. Alcohol gas-species enthalpies are corrected to liquid fuel.
No equilibrium calculation or kinetic integration is needed for an LHV.
"""

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
import math

import cantera as ct
import CoolProp
from CoolProp.CoolProp import PropsSI


REPO_ROOT = Path(__file__).resolve().parents[2]
SAN_DIEGO_PATH = REPO_ROOT / "mechanisms" / "sandiego.yaml"
REFERENCE_T_K = 298.15  # SPEC §§4,8: standard thermochemical reference.
REFERENCE_P_PA = 101325.0  # Standard atmosphere; ideal-gas h is pressure independent.
AIR_N2_O2 = 3.76  # SPEC/user contract: dry air approximation, mol N2/mol O2.


class MechanismUnavailable(RuntimeError):
    """The requested fuel cannot be evaluated with installed mechanisms."""


@dataclass(frozen=True)
class Fuel:
    """Properties: molar mass kg/mol, liquid density kg/m3, h_fg J/kg."""

    formula: str
    atoms: tuple[int, int, int]  # C, H, O atom counts (stoichiometric identities).
    state: str
    coolprop_name: str | None
    vaporization_J_mol: float | None
    vaporization_source: str
    density_source: str

    @cached_property
    def molar_mass(self) -> float:
        """Molar mass [kg/mol], using Cantera's element-weight database."""
        return sum(n * ct.Element(e).weight for e, n in
                   zip(("C", "H", "O"), self.atoms)) / 1000.0

    @cached_property
    def liquid_density(self) -> float | None:
        """Liquid density [kg/m3] at 298.15 K, 101325 Pa; None for gases."""
        if self.state != "liquid":
            return None
        return float(PropsSI("Dmass", "T", REFERENCE_T_K, "P",
                             REFERENCE_P_PA, self.coolprop_name))

    @property
    def h_fg(self) -> float | None:
        """Vaporization enthalpy [J/kg] at 298.15 K; None above critical T."""
        if self.vaporization_J_mol is None:
            return None
        return self.vaporization_J_mol / self.molar_mass


# NIST Chemistry WebBook SRD 69, Phase change data, standard vaporization
# enthalpy tables (averages): methanol 37.6 and ethanol 42.3 kJ/mol.
# https://webbook.nist.gov/cgi/cbook.cgi?ID=C67561&Mask=4
# https://webbook.nist.gov/cgi/cbook.cgi?ID=C64175&Mask=4
# These are 298.15 K values, NOT the latent heats at normal boiling points.
# Liquid density is evaluated, not guessed: CoolProp EOS, de Reuck & Craven
# (1993), Methanol; Schroeder et al. (2014), Ethanol, doi:10.1063/1.4895394.
# https://coolprop.org/fluid_properties/fluids/Methanol.html
# https://coolprop.org/fluid_properties/fluids/Ethanol.html
# Water h_fg: Chase (1998), NIST-JANAF, H2O(l) -285830 and H2O(g)
# -241826 J/mol. Density: Wagner & Pruss (2002), IAPWS-95, CoolProp Water.
# https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=3
FUELS = {
    "H2": Fuel("H2", (0, 2, 0), "gas", None, None,
               "Not defined at 298.15 K: above critical temperature",
               "No liquid phase at 298.15 K"),
    "CH4": Fuel("CH4", (1, 4, 0), "gas", None, None,
                "Not defined at 298.15 K: above critical temperature",
                "No liquid phase at 298.15 K"),
    "CH3OH": Fuel("CH3OH", (1, 4, 1), "liquid", "Methanol", 37600.0,
                  "NIST SRD 69 methanol standard vaporization enthalpy table",
                  "CoolProp Methanol EOS: de Reuck and Craven (1993)"),
    "C2H5OH": Fuel("C2H5OH", (2, 6, 1), "liquid", "Ethanol", 42300.0,
                   "NIST SRD 69 ethanol standard vaporization enthalpy table",
                   "CoolProp Ethanol EOS: Schroeder et al. (2014)"),
    "H2O": Fuel("H2O", (0, 2, 1), "liquid", "Water", 44004.0,
                "Chase (1998), JANAF H2O(g) minus H2O(l)",
                "CoolProp Water EOS: Wagner and Pruss (2002), IAPWS-95"),
}


@dataclass(frozen=True)
class MechanismSelection:
    """Portable mechanism label and explicit fallback status."""

    name: str
    mechanism_fallback: bool = False


def select_mechanism(fuel: str) -> MechanismSelection:
    """Select the contract's mechanism; only a missing file enables fallback."""
    if fuel not in FUELS:
        raise ValueError(f"Unknown fuel: {fuel}")
    if fuel in {"CH3OH", "C2H5OH"}:
        if SAN_DIEGO_PATH.is_file():
            return MechanismSelection("mechanisms/sandiego.yaml")
        if fuel == "C2H5OH":
            raise MechanismUnavailable(
                "C2H5OH requires mechanisms/sandiego.yaml; the file is absent. "
                "Install a provenance-recorded UCSD mechanism on the execution server."
            )
        return MechanismSelection("gri30.yaml", True)
    return MechanismSelection("gri30.yaml")


def load_mechanism(fuel: str, mech: str | Path | None = None) -> ct.Solution:
    """Load gas thermo; resolve repository mechanisms independent of cwd."""
    name = str(mech) if mech is not None else select_mechanism(fuel).name
    candidate = Path(name)
    if not candidate.is_absolute() and (REPO_ROOT / candidate).is_file():
        name = str(REPO_ROOT / candidate)
    return ct.Solution(name)


def species_name(gas: ct.Solution, name: str) -> str:
    """Resolve common GRI/UCSD upper/lowercase species spelling."""
    matches = [s for s in gas.species_names if s.casefold() == name.casefold()]
    if len(matches) != 1:
        raise MechanismUnavailable(f"Selected mechanism lacks unique species {name}")
    return matches[0]


def oxygen_demand(fuel: str) -> float:
    """Stoichiometric mol O2 per mol fuel, from C/H/O atom balance."""
    c, h, o = FUELS[fuel].atoms
    return c + h / 4.0 - o / 2.0


def lhv(fuel: str, mech: str | Path | None = None) -> float:
    """Lower heating value [J/kg] at 298.15 K, with H2O(g) products.

    Water undergoes the identity reaction H2O(g) -> H2O(g): zero chemical
    heating value. Its phase-change heat is never booked as combustion heat.
    """
    # Cantera's heating-value method: reactant minus complete-product enthalpy.
    # https://www.cantera.org/stable/userguide/heating-value.html
    # GRI thermochemistry: Smith et al. (1999), GRI-Mech 3.0, embedded YAML
    # species thermo data; UCSD data: mechanisms/PROVENANCE.md and YAML header.
    gas = load_mechanism(fuel, mech)
    gas.TP = REFERENCE_T_K, REFERENCE_P_PA

    def enthalpy(name: str) -> float:
        # Cantera standard_enthalpies_RT * R*T is J/kmol; convert to J/mol.
        index = gas.species_index(species_name(gas, name))
        return float(gas.standard_enthalpies_RT[index] * ct.gas_constant
                     * REFERENCE_T_K / 1000.0)

    c, h, _ = FUELS[fuel].atoms
    nu_o2 = oxygen_demand(fuel)
    reactants = enthalpy(fuel) + nu_o2 * enthalpy("O2")
    products = h / 2.0 * enthalpy("H2O")
    if c:
        products += c * enthalpy("CO2")
    heat = (reactants - products) / FUELS[fuel].molar_mass
    if nu_o2 > 0 and FUELS[fuel].state == "liquid":
        heat -= FUELS[fuel].h_fg
    return float(heat)


def stoich_air_fuel_ratio(fuel: str) -> float:
    """Stoichiometric dry-air/fuel mass ratio [kg/kg]; water demand is zero."""
    # Element weights come from Cantera; N2/O2 ratio is the SPEC approximation.
    air_mass = (2 * ct.Element("O").weight
                + AIR_N2_O2 * 2 * ct.Element("N").weight) / 1000.0
    return oxygen_demand(fuel) * air_mass / FUELS[fuel].molar_mass


def mixture(fuel: str, phi: float, w: float,
            mech: str | Path | None = None) -> dict[str, float]:
    """Return unnormalised moles: fuel + dry air + added H2O vapour.

    phi is fuel/air equivalence ratio; w = m_water/(m_water + m_fuel).
    The basis is one mole of fuel. Liquid vaporization energy is not supplied
    by this composition builder and must be accounted for by its caller.
    """
    if not math.isfinite(phi) or phi <= 0:
        raise ValueError("phi must be finite and > 0")
    if not math.isfinite(w) or not 0 <= w < 1:
        raise ValueError("w must be finite and satisfy 0 <= w < 1")
    if fuel == "H2O":
        raise ValueError("Water is not a fuel; phi is undefined for H2O")
    gas = load_mechanism(fuel, mech)
    o2 = oxygen_demand(fuel) / phi
    water = w / (1.0 - w) * FUELS[fuel].molar_mass / FUELS["H2O"].molar_mass
    return {species_name(gas, fuel): 1.0, species_name(gas, "O2"): o2,
            species_name(gas, "N2"): AIR_N2_O2 * o2,
            species_name(gas, "H2O"): water}


def fuel_assumptions() -> dict:
    """Serializable defaults, phase conventions and sources for summaries."""
    return {
        "reference_temperature_K": {"value": REFERENCE_T_K, "source": "SPEC §§4,8"},
        "reference_pressure_Pa": {"value": REFERENCE_P_PA, "rationale": "Standard atmosphere; ideal-gas enthalpy is pressure independent"},
        "air_N2_per_O2_mol": {"value": AIR_N2_O2, "source": "SPEC/user contract"},
        "water_heating_value_J_kg": {"value": 0.0, "rationale": "Fully oxidised; identity reaction, not vaporization or condensation"},
        "lhv_basis": {"value": "Registered reactant phase, CO2(g) and H2O(g) products", "source": "SPEC §10 liquid-alcohol targets; Cantera heating-value method"},
        "thermo_data": {"value": "Cantera species enthalpies and element weights", "source": "Smith et al. (1999), GRI-Mech 3.0 / UCSD YAML thermodynamic data; mechanisms/PROVENANCE.md", "cantera_version": ct.__version__, "coolprop_version": CoolProp.__version__},
        "temperature_evaluation_policy": {"value": "Evaluate species thermo at 298.15 K even if a polynomial lower bound is 300 K", "rationale": "SPEC standard-state LHV reference; short polynomial extrapolation is explicit, without changing the reference temperature"},
        "fuel_registry": {name: {
            "formula": f.formula, "state": f.state,
            "molar_mass_kg_mol": f.molar_mass,
            "liquid_density_kg_m3": f.liquid_density,
            "density_source": f.density_source,
            "h_fg_J_kg": f.h_fg, "h_fg_source": f.vaporization_source,
        } for name, f in FUELS.items()},
    }
