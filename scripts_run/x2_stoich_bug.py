"""Verify module 08's actual Q_dry computation with stoich_o2=atoms[1]=4."""
import warnings
warnings.filterwarnings("ignore")
import cantera as ct

gas = ct.Solution("/opt/water-engine/code/mechanisms/sandiego.yaml")
R = ct.gas_constant  # J/kmol/K
T = 298.15

# Module 08: stoich_o2 = atoms[1] = 4 for CH3OH (BUG: should be 1.5)
stoich_o2 = 4.0
stoich_n2 = stoich_o2 * 3.76  # = 15.04

c_atoms = 1.0
h_atoms = 4.0
o_atoms = 1.0

mw_fuel = gas.molecular_weights[gas.species_index("CH3OH")]  # kg/kmol
mol_per_kg = 1000.0 / mw_fuel

# Reactants
gas.TPX = T, 101325.0, {"CH3OH": 1.0, "O2": stoich_o2, "N2": stoich_n2}
h_react = float(gas.int_energy_mole)  # J/kmol mix
n_react_total = 1.0 + stoich_o2 + stoich_n2

# Products
n_co2 = c_atoms  # = 1
n_h2o = h_atoms / 2.0  # = 2
n_n2 = stoich_n2  # = 15.04
n_total = n_co2 + n_h2o + n_n2  # = 18.04
gas.TPX = T, 101325.0, {"CO2": n_co2/n_total, "H2O": n_h2o/n_total,
                        "N2": n_n2/n_total}
h_prod = float(gas.int_energy_mole)

Q = (h_react * n_react_total - h_prod * n_total) / mol_per_kg
print(f"stoich_o2 = {stoich_o2} (atoms[1])")
print(f"stoich_n2 = {stoich_n2}")
print(f"n_react_total = {n_react_total}, n_prod_total = {n_total}")
print(f"h_react = {h_react:.3f} J/kmol mix")
print(f"h_prod = {h_prod:.3f} J/kmol mix")
print(f"Q_dry = {Q:.3f} J/kg")
print(f"Reference = 21508520.355 J/kg")
print(f"Diff = {abs(Q-21508520.355):.3f} J/kg ({abs(Q-21508520.355)/21508520.355*100:.4f}%)")

# Also check with proper stoich_o2 = 1.5
stoich_o2_p = 1.5
stoich_n2_p = stoich_o2_p * 3.76
n_react_p = 1.0 + stoich_o2_p + stoich_n2_p
n_total_p = 1.0 + 2.0 + stoich_n2_p
gas.TPX = T, 101325.0, {"CH3OH": 1.0, "O2": stoich_o2_p, "N2": stoich_n2_p}
h_react_p = float(gas.int_energy_mole)
gas.TPX = T, 101325.0, {"CO2": 1.0/n_total_p, "H2O": 2.0/n_total_p,
                        "N2": stoich_n2_p/n_total_p}
h_prod_p = float(gas.int_energy_mole)
Q_p = (h_react_p * n_react_p - h_prod_p * n_total_p) / mol_per_kg
print(f"\nWith stoich_o2=1.5: Q_dry = {Q_p:.3f} J/kg")

# What if we use enthalpy instead of int_energy with the buggy stoich?
gas.TPX = T, 101325.0, {"CH3OH": 1.0, "O2": stoich_o2, "N2": stoich_n2}
h_react_h = float(gas.enthalpy_mole)
gas.TPX = T, 101325.0, {"CO2": n_co2/n_total, "H2O": n_h2o/n_total,
                        "N2": n_n2/n_total}
h_prod_h = float(gas.enthalpy_mole)
Q_h = (h_react_h * n_react_total - h_prod_h * n_total) / mol_per_kg
print(f"With stoich_o2=4, enthalpy method: Q_dry = {Q_h:.3f} J/kg")