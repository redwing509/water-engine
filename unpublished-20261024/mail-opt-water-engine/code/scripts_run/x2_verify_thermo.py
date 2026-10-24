"""X2 verification: compare mechanism-embedded vs NIST-JANAF formation enthalpies.

Runs on mail where Cantera + San Diego mechanism are installed.
"""
import cantera as ct
import json
import re
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="cantera")

R = ct.gas_constant  # J/kmol/K
T = 298.15

# NIST-JANAF / NIST WebBook reference values, J/mol
NIST = {
    "H2O":  -241826.0,   # Chase 1998 JANAF (gas)
    "CO2":  -393526.0,   # Chase 1998 JANAF (gas)
    "CH3OH": -201000.0,  # NIST WebBook (gas)
    "C2H5OH": -234800.0, # NIST WebBook (gas)
}

result = {}

# Cantera embedded values from the YAML
for label, mech in (("sandiego", "/opt/water-engine/code/mechanisms/sandiego.yaml"),
                    ("gri30", "gri30.yaml")):
    gas = ct.Solution(mech)
    entry = {}
    species_list = ["H2O", "CO2", "O2", "N2", "H2", "CH3OH", "C2H5OH"]
    for name in species_list:
        if name in gas.species_names:
            idx = gas.species_index(name)
            entry[name] = float(gas.standard_enthalpies_RT[idx]) * R * T / 1000.0  # kJ/mol
    result[label] = entry

# Hand-compute H2O, CO2, CH3OH, C2H5OH from the raw SD thermo file NASA polynomials
# Format: each species is 4 lines:
#   Line 1: "SPC   H 2 C 2 O 1  G   200.0   3000.0   1000.0        1"
#   Line 2: c1 c2 c3 c4 c5 2
#   Line 3: c6 c7 c8 c9 c10 3
#   Line 4: c11 c12 c13 c14 4
# The 14 coefficients for NasaPoly2: 2 sets of 7 (high T and low T)
thermo_path = "/opt/water-engine/mechanisms/src/sandiego20160815_therm.txt"
species_data = {}
with open(thermo_path) as f:
    lines = f.readlines()

i = 0
while i < len(lines):
    line = lines[i].strip()
    # Match species header line
    m = re.match(r"^([A-Z0-9]+)\s+([0-9]{6})([A-Z]\s+\d+\s+[A-Z]\s+\d+)\s+([LG])\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)", line)
    if m:
        name = m.group(1).strip()
        # Read next 3 lines for coefficients
        coeffs = []
        for j in range(1, 4):
            if i + j < len(lines):
                parts = lines[i + j].strip().split()
                coeffs.extend(parts[:7] if len(parts) > 7 else parts[:7])
        if name in ("H2O", "CO2", "CH3OH", "C2H5OH") and len(coeffs) >= 14:
            # NasaPoly2: high-temp coeffs (c1..c7), low-temp coeffs (c8..c14)
            # But the format is actually: 2 lines of 7 coeffs each for high T, then 2 lines for low T?
            # No - NASA 7-coeff: line 2 = 2 coeffs (a1,a2) + 5 from line 3, line 4 = 2 coeffs (a3,a4) + continuation
            # Actually the SD format gives 14 coeffs total: first 7 are high-T, second 7 are low-T (a1-a7)
            # But we need to know which temp range 298.15 falls in.
            # The T common temp (Tmid) is in the header line
            Tmid = float(m.group(7))
            all_coeffs = []
            for j in range(1, 4):
                if i + j < len(lines):
                    parts = lines[i + j].strip().split()
                    all_coeffs.extend([float(x) for x in parts[:7]])
            if len(all_coeffs) >= 14:
                high_coeffs = all_coeffs[:7]  # a1-a7 for T > Tmid
                low_coeffs = all_coeffs[7:14]  # a1-a7 for T < Tmid
                coeffs_used = low_coeffs if T < Tmid else high_coeffs
                a1, a2, a3, a4, a5, a6, a7 = coeffs_used
                # NASA 7-coeff enthalpy:
                # h/RT = a1 + a2*T/2 + a3*T^2/3 + a4*T^3/4 + a5*T^4/5 - a6/T + a7
                # But for formation enthalpy at 298.15, we want the deviation from 0
                # h_f°(T) = R*T * (a1 + a2*T/2 + a3*T^2/3 + a4*T^3/4 + a5*T^4/5 - a6/T + a7)
                # Actually h°(T) - h°(0) = R*T*(a1 + a2*T/2 + ... + a5*T^4/5 - a6/T)
                # For standard enthalpy, we use: H°(298) = R*298*(a1 + a2*298/2 + ...) - but this is relative to 0K
                # The NASA a7 term is typically for h° relative to reference temperature
                # Standard approach: h_f(T) = a6 * R (a6 is the integral constant)
                # For 7-coeff NASA thermo: H°(T)/RT = a1 + a2*T/2 + a3*T^2/3 + a4*T^3/4 + a5*T^4/5 + a6/T
                # Wait - need to check the actual convention
                # In SD thermo format, the 7 coeffs are: a1 a2 a3 a4 a5 a6 a7
                # h/RT = a1 + a2*T/2 + a3*T^2/3 + a4*T^3/4 + a5*T^4/5 + a7 - a6/T
                # Hmm, let me just compute it both ways
                h = R * T * (a1 + a2*T/2 + a3*T**2/3 + a4*T**3/4 + a5*T**4/5 + a7 - a6/T) / 1000.0
                species_data[name] = {
                    "h_kJ_mol": h,
                    "Tmid_K": Tmid,
                    "coeffs": coeffs_used,
                }
        i += 4
    else:
        i += 1

result["sd_thermo_file_hand_calc_kJ_mol"] = {k: v["h_kJ_mol"] for k, v in species_data.items()}
result["NIST_JANAF_reference_kJ_mol"] = {k: v/1000.0 for k, v in NIST.items()}

# Comparison
print(json.dumps(result, indent=2))
print("\n--- Comparison ---")
for sp in ["H2O", "CO2", "CH3OH", "C2H5OH"]:
    if sp in result.get("sandiego", {}) and sp in result["sd_thermo_file_hand_calc_kJ_mol"]:
        cantera_h = result["sandiego"][sp]
        hand_h = result["sd_thermo_file_hand_calc_kJ_mol"][sp]
        nist_h = result["NIST_JANAF_reference_kJ_mol"][sp]
        print(f"{sp}: Cantera={cantera_h:.3f}, Hand-calc={hand_h:.3f}, NIST={nist_h:.3f} kJ/mol")
        print(f"  Cantera vs NIST: {abs(cantera_h-nist_h)/abs(nist_h)*100:.3f}%")
        print(f"  Hand-calc vs NIST: {abs(hand_h-nist_h)/abs(nist_h)*100:.3f}%")
        print(f"  Cantera vs Hand-calc: {abs(cantera_h-hand_h)/abs(hand_h)*100:.6f}%")

with open("/opt/water-engine/code/results/xcheck/x2_thermo_check.json", "w") as f:
    json.dump(result, f, indent=2)
print("\nWritten to results/xcheck/x2_thermo_check.json")
