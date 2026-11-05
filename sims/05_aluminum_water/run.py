"""SPEC §8 aluminum/water thermochemistry at 298.15 K, in SI units.

Heat plus hydrogen LHV is an ideal energy recovery bound. It is not electric
output: no heat engine, hydrogen converter, kinetics or passivation is modeled.
"""

from dataclasses import dataclass
import math
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sims.common.fuels import FUELS, REFERENCE_T_K, fuel_assumptions, lhv
from sims.common.io import argument_parser, ordered_map, save_fig, write_csv, write_summary


MODULE = "05_aluminum_water"
VERSION = "1.0.0"
# Meija et al. (2016), Atomic weights of the elements 2013 (IUPAC report),
# doi:10.1515/pac-2015-0305, standard atomic weight table: Al = 26.9815385.
M_AL_KG_MOL = 0.0269815385

# Standard molar enthalpies of formation at 298.15 K [J/mol].
# Water(l): Chase (1998), NIST-JANAF 4th ed., H2O(l), -285.830 kJ/mol.
# https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=2
# Corundum: Chase (1998), NIST-JANAF 4th ed., alpha-Al2O3(cr), -1675.690 kJ/mol.
# https://webbook.nist.gov/cgi/cbook.cgi?ID=C1344281&Mask=2
# Gibbsite and boehmite are NOT tabulated in the JANAF aluminum index:
# https://janaf.nist.gov/tables/Al-index.html
# Their values are the recommended literature comparison in Chen & Zeng
# (1996), Geochimica et Cosmochimica Acta 60(1), 1-5, respectively
# -1293.18 +/- 1.20 and -996.10 +/- 1.30 kJ/mol. These are explicitly a
# supplemental compilation, not mislabeled as JANAF data.
# https://doi.org/10.1016/0016-7037(95)00378-9
# Al(cr), H2(g), O2(g): zero by elemental standard-state formation convention.
FORMATION_ENTHALPIES_J_MOL = {
    "H2O(l)": -285830.0,
    "Al(OH)3(gibbsite)": -1293180.0,
    "AlOOH(boehmite)": -996100.0,
    "Al2O3(corundum)": -1675690.0,
    "Al(cr)": 0.0,
    "H2(g)": 0.0,
    "O2(g)": 0.0,
}
FORMATION_SOURCES = {
    "H2O(l)": "Chase (1998), NIST-JANAF 4th edition, H2O(l)",
    "Al(OH)3(gibbsite)": "Chen and Zeng (1996), recommended literature comparison, doi:10.1016/0016-7037(95)00378-9",
    "AlOOH(boehmite)": "Chen and Zeng (1996), recommended literature comparison, doi:10.1016/0016-7037(95)00378-9",
    "Al2O3(corundum)": "Chase (1998), NIST-JANAF 4th edition, alpha-Al2O3(cr)",
    "Al(cr)": "Elemental standard-state formation convention",
    "H2(g)": "Elemental standard-state formation convention",
    "O2(g)": "Elemental standard-state formation convention",
}
# International Aluminium Institute, The Aluminium Story, Power Generation
# (undated): 13-15 MWh DC per tonne molten Al, equivalent to 13-15 kWh/kg.
# https://iai.dev.interstruct.com/primary-production/power-generation/
# This is smelter DC electricity only, not cradle-to-metal energy or AC demand.
SMELTING_ELECTRICITY_LOW_J_KG = 13.0 * 3.6e6
SMELTING_ELECTRICITY_HIGH_J_KG = 15.0 * 3.6e6
BOOKKEEPING_REL_TOL = 1e-6  # User validation contract.


@dataclass(frozen=True)
class Reaction:
    """Balanced coefficients per 2 mol Al consumed, producing 3 mol H2."""

    name: str
    equation: str
    product: str
    product_mol: int
    water_mol: int
    aluminum_mol: int = 2
    hydrogen_mol: int = 3


# SPEC §8 stoichiometric identities (not empirical fit parameters).
REACTIONS = (
    Reaction("gibbsite", "2Al + 6H2O(l) -> 2Al(OH)3(cr) + 3H2(g)",
             "Al(OH)3(gibbsite)", 2, 6),
    Reaction("boehmite", "2Al + 4H2O(l) -> 2AlOOH(cr) + 3H2(g)",
             "AlOOH(boehmite)", 2, 4),
    Reaction("corundum", "2Al + 3H2O(l) -> Al2O3(cr) + 3H2(g)",
             "Al2O3(corundum)", 1, 3),
)


def reaction_ledger(reaction: Reaction) -> dict:
    """Return reaction energy [J/kg Al] and masses [kg/kg Al].

    A Hess cycle splits the process into oxidation/hydration of aluminum and
    splitting liquid water. The latter COSTS energy. Recombining H2 with O2
    recovers less than this cost on an LHV basis, because water exits as vapour.
    """
    hf = FORMATION_ENTHALPIES_J_MOL
    basis_mass = reaction.aluminum_mol * M_AL_KG_MOL
    reactant_h = (reaction.aluminum_mol * hf["Al(cr)"]
                  + reaction.water_mol * hf["H2O(l)"])
    product_h = (reaction.product_mol * hf[reaction.product]
                 + reaction.hydrogen_mol * hf["H2(g)"])
    heat = (reactant_h - product_h) / basis_mass
    hydrogen_mass = reaction.hydrogen_mol * FUELS["H2"].molar_mass / basis_mass
    water_mass = reaction.water_mol * FUELS["H2O"].molar_mass / basis_mass
    hydrogen_lhv = lhv("H2")
    hydrogen_energy = hydrogen_mass * hydrogen_lhv

    # Use the same Cantera combustion enthalpy for both branches of the Hess
    # cycle. Do not mix rounded JANAF H2O(g) and GRI H2O(g) and then call the
    # resulting database discrepancy a numerical closure error.
    # With elemental reference enthalpies zero, this is the equivalent H2O(g)
    # formation enthalpy implied by H2 + 1/2 O2 -> H2O(g) in Cantera.
    h_water_vapor = -hydrogen_lhv * FUELS["H2"].molar_mass
    combined_products_h = reaction.product_mol * hf[reaction.product] + reaction.hydrogen_mol * h_water_vapor
    direct_combined_heat = (reactant_h - combined_products_h) / basis_mass
    total = heat + hydrogen_energy

    retained_water_mol = reaction.water_mol - reaction.hydrogen_mol
    aluminum_oxidation_energy = (
        reaction.aluminum_mol * hf["Al(cr)"]
        + retained_water_mol * hf["H2O(l)"]
        - reaction.product_mol * hf[reaction.product]
    ) / basis_mass
    water_splitting_cost = -reaction.hydrogen_mol * hf["H2O(l)"] / basis_mass
    vaporization_penalty = reaction.hydrogen_mol * (h_water_vapor - hf["H2O(l)"]) / basis_mass
    closure = abs(total - direct_combined_heat) / max(abs(direct_combined_heat), 1.0)
    return {
        "reaction": reaction.name, "equation": reaction.equation,
        "heat_released_J_kg_Al": heat,
        "hydrogen_kg_per_kg_Al": hydrogen_mass,
        "hydrogen_lhv_J_kg_H2": hydrogen_lhv,
        "hydrogen_lhv_energy_J_kg_Al": hydrogen_energy,
        "total_energy_J_kg_Al": total,
        "water_consumed_kg_per_kg_Al": water_mass,
        "water_mass_fraction_reactants": water_mass / (1.0 + water_mass),
        "reactant_formation_enthalpy_J_kg_Al": reactant_h / basis_mass,
        "product_formation_enthalpy_J_kg_Al": product_h / basis_mass,
        "direct_combined_heat_J_kg_Al": direct_combined_heat,
        "aluminum_oxidation_energy_J_kg_Al": aluminum_oxidation_energy,
        "water_splitting_cost_J_kg_Al": water_splitting_cost,
        "water_vaporization_penalty_J_kg_Al": vaporization_penalty,
        "water_cycle_net_energy_J_kg_Al": hydrogen_energy - water_splitting_cost,
        "water_heating_value_J_kg": lhv("H2O"),
        "closure_relative_error": closure,
        "round_trip_energy_efficiency_min": total / SMELTING_ELECTRICITY_HIGH_J_KG,
        "round_trip_energy_efficiency_max": total / SMELTING_ELECTRICITY_LOW_J_KG,
        "hydrogen_only_efficiency_min": hydrogen_energy / SMELTING_ELECTRICITY_HIGH_J_KG,
        "hydrogen_only_efficiency_max": hydrogen_energy / SMELTING_ELECTRICITY_LOW_J_KG,
    }


def batch_energy(reaction: Reaction, aluminum_mass_kg: float, water_mass_kg: float) -> float:
    """Ideal heat + H2 LHV [J] for a batch limited by available Al and water.

    Zero aluminum means zero reaction extent and zero released energy,
    irrespective of water inventory. Excess reactants contribute no energy.
    """
    if not all(math.isfinite(x) and x >= 0 for x in (aluminum_mass_kg, water_mass_kg)):
        raise ValueError("Reactant masses must be finite and nonnegative")
    extent = min(aluminum_mass_kg / (reaction.aluminum_mol * M_AL_KG_MOL),
                 water_mass_kg / (reaction.water_mol * FUELS["H2O"].molar_mass))
    if extent == 0:
        return 0.0
    return extent * reaction.aluminum_mol * M_AL_KG_MOL * reaction_ledger(reaction)["total_energy_J_kg_Al"]


def validate_ledgers(rows: list[dict]) -> dict:
    """Check stoichiometry, Hess closure, source attribution and energy order."""
    expected_h2 = 3 * FUELS["H2"].molar_mass / (2 * M_AL_KG_MOL)
    checks = {
        "same_stoichiometric_hydrogen_yield": all(math.isclose(r["hydrogen_kg_per_kg_Al"], expected_h2, rel_tol=1e-12) for r in rows),
        "energies_positive": all(r["heat_released_J_kg_Al"] > 0 and r["hydrogen_lhv_energy_J_kg_Al"] > 0 for r in rows),
        "heat_order_gibbsite_boehmite_corundum": rows[0]["heat_released_J_kg_Al"] > rows[1]["heat_released_J_kg_Al"] > rows[2]["heat_released_J_kg_Al"],
        "total_order_gibbsite_boehmite_corundum": rows[0]["total_energy_J_kg_Al"] > rows[1]["total_energy_J_kg_Al"] > rows[2]["total_energy_J_kg_Al"],
        "enthalpy_bookkeeping_closes": all(r["closure_relative_error"] < BOOKKEEPING_REL_TOL for r in rows),
        "water_cycle_consumes_energy": all(r["water_cycle_net_energy_J_kg_Al"] < 0 for r in rows),
        "water_alone_releases_no_energy": all(batch_energy(r, 0.0, 1.0) == 0 for r in REACTIONS),
        "smelting_energy_exceeds_ideal_recovery": all(0 < r["round_trip_energy_efficiency_max"] < 1 for r in rows),
    }
    return {"passed": all(checks.values()), "checks": checks,
            "bookkeeping_relative_tolerance": BOOKKEEPING_REL_TOL}


def write_plot(out, rows):
    """Plot energies [MJ/kg Al] and ideal energy recovery ratios [1]."""
    names = [r["reaction"] for r in rows]
    heat = [r["heat_released_J_kg_Al"] / 1e6 for r in rows]
    hydrogen = [r["hydrogen_lhv_energy_J_kg_Al"] / 1e6 for r in rows]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].bar(names, heat, label="Reaction heat")
    axes[0].bar(names, hydrogen, bottom=heat, label="Hydrogen LHV")
    axes[0].axhspan(SMELTING_ELECTRICITY_LOW_J_KG / 1e6,
                   SMELTING_ELECTRICITY_HIGH_J_KG / 1e6,
                   alpha=0.15, color="firebrick", label="Smelting DC electricity input")
    axes[0].set(xlabel="Aluminum product [1]", ylabel="Energy [MJ/kg Al]",
                title="Energy stored in aluminum; water is not fuel")
    axes[0].legend()
    lows = [r["round_trip_energy_efficiency_min"] for r in rows]
    highs = [r["round_trip_energy_efficiency_max"] for r in rows]
    mids = [(a + b) / 2 for a, b in zip(lows, highs)]
    errors = [(b - a) / 2 for a, b in zip(lows, highs)]
    axes[1].bar(names, mids, yerr=errors, capsize=5, color="steelblue")
    axes[1].set(ylim=(0, 1), xlabel="Aluminum product [1]",
                ylabel="Ideal recovered energy / smelting electricity [1]",
                title="Heat + H2 LHV upper bound; not electrical efficiency")
    fig.tight_layout()
    save_fig(fig, out / "aluminum_water_energy.png")
    plt.close(fig)


def main(argv=None) -> int:
    """Write three reaction ledgers; quick and full both cover all reactions."""
    start = time.perf_counter()
    args = argument_parser(MODULE).parse_args(None if argv is None else list(map(str, argv)))
    rows = ordered_map(reaction_ledger, REACTIONS, args.workers)
    write_csv(args.out / "aluminum_water_reactions.csv", rows)
    write_plot(args.out, rows)
    assumptions = fuel_assumptions()
    assumptions.update({
        "mechanism_fallback": False,
        "mechanism": {"value": "gri30.yaml", "rationale": "Only H2 and H2O thermochemistry is required"},
        "temperature_K": {"value": REFERENCE_T_K, "source": "SPEC §8 standard state"},
        "aluminum_molar_mass_kg_mol": {"value": M_AL_KG_MOL, "source": "Meija et al. (2016), IUPAC atomic weights 2013"},
        "formation_enthalpies": {s: {"value_J_mol": value, "source": FORMATION_SOURCES[s]} for s, value in FORMATION_ENTHALPIES_J_MOL.items()},
        "hydroxide_source_substitution": {"value": True, "rationale": "JANAF aluminum index lacks gibbsite and boehmite. Chen and Zeng (1996) recommended values supplement JANAF, as identified per species."},
        "water_vapor_thermo": {"value": "Equivalent formation enthalpy = -Cantera H2 LHV * H2 molar mass", "rationale": "One internally consistent combustion enthalpy in both Hess-cycle branches; elemental reference states have zero formation enthalpy"},
        "smelting_electricity_J_kg_Al": {"low": SMELTING_ELECTRICITY_LOW_J_KG,
                                       "high": SMELTING_ELECTRICITY_HIGH_J_KG,
                                       "source": "International Aluminium Institute, The Aluminium Story, Power Generation (undated), 13-15 MWh DC/tonne"},
        "energy_recovery_fraction": {"value": 1.0, "rationale": "Ideal upper bound: all reaction heat and H2 LHV recoverable; no conversion losses modeled"},
        "reaction_completion_fraction": {"value": 1.0, "rationale": "Stoichiometric thermodynamic limit; no passivation, activation or rate prediction"},
        "round_trip_boundary": {"value": "Heat plus H2 chemical energy divided by smelting DC electricity", "rationale": "Energy ratio, not electrical round-trip efficiency; excludes refining, anodes, activation and other upstream inputs"},
        "reaction_stoichiometry": {"value": [r.equation for r in REACTIONS], "source": "SPEC §8"},
        "workers": {"value": args.workers, "rationale": "Independent reactions; at most three active processes"},
        "mode_scope": {"value": "All three reactions in both modes", "rationale": "No expensive sweep to reduce in quick mode"},
    })
    validation = validate_ledgers(rows)
    write_summary(args.out, MODULE, VERSION, args.mode, assumptions,
                  {"reactions": rows,
                   "energy_source": "Oxidation of aluminum pays for water splitting; water has zero heating value",
                   "efficiency_interpretation": "Ideal thermal plus chemical recovery, not electrical output"},
                  validation, time.perf_counter() - start)
    return 0 if validation["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
