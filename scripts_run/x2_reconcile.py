"""One-shot reconciliation: load the mail sandiego.yaml ONCE, print formation
enthalpies, and compute Q_dry for CH3OH with several independent methods.
Purpose: pin down exactly which numbers the current mechanism gives."""
import warnings, sys
warnings.filterwarnings("ignore")
import cantera as ct

mech = "/opt/water-engine/code/mechanisms/sandiego.yaml"
gas = ct.Solution(mech)
R_J_kmolK = ct.gas_constant   # 8314.462618
R_J_molK = R_J_kmolK / 1000.0 # 8.314462618
T = 298.15
print("mechanism:", mech)
print("cantera version:", ct.__version__)

# --- formation enthalpies, J/mol ---
hf = {}
for name in ["CH3OH", "CO2", "H2O", "O2", "N2"]:
    i = gas.species_index(name)
    hf[name] = float(gas.standard_enthalpies_RT[i]) * R_J_molK * T
    print(f"h_f({name}) = {hf[name]:.3f} J/mol")

mw = gas.molecular_weights[gas.species_index("CH3OH")]  # kg/kmol = g/mol
print("MW CH3OH = %.6f kg/kmol" % mw)

# --- stoichiometry (module 08: stoich_o2 = atoms[1] = 1.5 for CH3OH) ---
c, h, o = 1, 4, 1
stoich_o2 = 1.5           # as in module 08 (atoms[1])
o2_proper = c + h/4 - o/2  # = 1.5 same
stoich_n2 = stoich_o2 * 3.76
print("stoich_o2=%.3f (module08), stoich_n2=%.4f" % (stoich_o2, stoich_n2))

n_react_total = 1.0 + stoich_o2 + stoich_n2
n_co2, n_h2o = 1.0, 2.0
n_n2 = stoich_n2
n_prod_total = n_co2 + n_h2o + n_n2

# Method 1: int_energy_mole (module 08's method), J/kmol mixture
gas.TPX = T, 101325.0, {"CH3OH": 1.0, "O2": stoich_o2, "N2": stoich_n2}
u_react = float(gas.int_energy_mole)
gas.TPX = T, 101325.0, {"CO2": n_co2/n_prod_total, "H2O": n_h2o/n_prod_total,
                        "N2": n_n2/n_prod_total}
u_prod = float(gas.int_energy_mole)
Q1 = (u_react * n_react_total - u_prod * n_prod_total) / (mw)
print("M1 int_energy:  Q_dry = %.3f J/kg  (u_react=%.1f u_prod=%.1f J/kmol)" % (Q1, u_react, u_prod))

# Method 2: H_f basis, J/mol -> J/kg (proper oxygen demand)
H_r = hf["CH3OH"] + o2_proper*hf["O2"] + stoich_n2*hf["N2"]
H_p = c*hf["CO2"] + 2.0*hf["H2O"] + n_n2*hf["N2"]
Q2 = (H_r - H_p) / (mw/1000.0)
print("M2 H_f(o2=1.5): Q_dry = %.3f J/kg  (dH=%.1f J/mol)" % (Q2, H_r - H_p))

# Method 3: U_f basis (H_f - RT), J/mol -> J/kg
RT = R_J_molK * T
U_r = (hf["CH3OH"]-RT) + o2_proper*(hf["O2"]-RT) + stoich_n2*(hf["N2"]-RT)
U_p = (c*hf["CO2"]-RT) + (2.0*hf["H2O"]-RT) + n_n2*(hf["N2"]-RT)
Q3 = (U_r - U_p) / (mw/1000.0)
print("M3 U_f(o2=1.5): Q_dry = %.3f J/kg" % Q3)

# Method 4: NIST-JANAF independent (Chase 1998)
nist = {"CH3OH": -200938.0, "CO2": -393522.4, "H2O": -241826.4, "O2": 0.0, "N2": 0.0}
nH_r = nist["CH3OH"] + o2_proper*nist["O2"] + stoich_n2*nist["N2"]
nH_p = nist["CO2"] + 2.0*nist["H2O"] + n_n2*nist["N2"]
Q4 = (nH_r - nH_p) / (mw/1000.0)
print("M4 NIST-JANAF : Q_dry = %.3f J/kg  (dH=%.1f J/mol)" % (Q4, nH_r - nH_p))

print()
print("REFERENCE (module08 full08): Q_dry = 21508520.355 J/kg")
for label, q in [("M1", Q1), ("M2", Q2), ("M3", Q3), ("M4", Q4)]:
    d = abs(q - 21508520.355) / 21508520.355 * 100
    print(f"  {label}: {q:14.3f}  diff = {d:.4f}%")

# delta mechanism-vs-NIST per species
print()
print("mechanism h_f - NIST h_f (J/mol):")
for name in ["CH3OH", "CO2", "H2O"]:
    print(f"  {name}: {hf[name] - nist[name]:+10.2f}")
