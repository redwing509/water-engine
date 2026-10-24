import cantera as ct
import json

gas = ct.Solution("/opt/water-engine/code/mechanisms/sandiego.yaml")
R = ct.gas_constant
T = 298.15

result = {}
for name in ["CH3OH", "C2H5OH", "CO2", "H2O", "O2", "N2", "H2"]:
    idx = gas.species_index(name)
    h_std = float(gas.standard_enthalpies_RT[idx]) * R * T  # J/kmol
    result[name] = h_std / 1000.0  # kJ/mol

print(json.dumps(result, indent=2))
