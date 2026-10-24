#!/usr/bin/env python3
"""X2 re-check: independent NIST-JANAF Q_dry/Q_wet vs a module 08 bookkeeping
JSON file (new corrected run).  No Cantera.

Usage: python3 x2_final_new.py <path/to/oxygen_bookkeeping.json>
Tolerance +/-0.2%.  Expected residual vs San Diego mechanism: formation
enthalpy differences of ~1.3-2.5 kJ/mol per species (documented, not tuned).
"""
import json, math, sys

# NIST-JANAF (Chase 1998) formation enthalpies, J/mol at 298.15 K
NIST_HF = {
    "CH3OH": -200941.5,  # CH3OH(g)
    "C2H5OH": -234800.0,  # C2H5OH(g)
    "CO2":   -393522.4,   # CO2(g)
    "H2O":   -241826.4,   # H2O(g)
    "O2":    0.0, "N2":    0.0,
}
# IUPAC 2021 molar masses, kg/mol
C, H, O = 12.011e-3, 1.008e-3, 15.999e-3
MW = {"CH3OH": C + 4*H + O, "C2H5OH": 2*C + 6*H + O}
ATOMS = {"CH3OH": (1, 4, 1), "C2H5OH": (2, 6, 1)}
T_REF, TOL = 298.15, 0.002

def stoich_o2(fuel):
    c, h, o = ATOMS[fuel]
    return c + h/4.0 - o/2.0      # 1.5 CH3OH, 3.0 C2H5OH

def q_nist(fuel):
    c, h, o = ATOMS[fuel]
    n2 = stoich_o2(fuel) * 3.76
    H_r = NIST_HF[fuel] + stoich_o2(fuel)*NIST_HF["O2"] + n2*NIST_HF["N2"]
    H_p = c*NIST_HF["CO2"] + h/2.0*NIST_HF["H2O"] + n2*NIST_HF["N2"]
    return (H_r - H_p) / MW[fuel], (H_r - H_p)  # J/kg, J/mol

def cmp(qty, indep, ref, tol=TOL):
    d = abs(indep - ref)/abs(ref)
    return {"quantity": qty, "independent_J_kg": round(indep, 3),
            "reference_J_kg": round(ref, 3), "rel_diff_pct": round(d*100, 5),
            "tolerance_pct": tol*100, "pass": d <= tol}

def main():
    ref_path = sys.argv[1]
    ref = json.load(open(ref_path))
    fuel = ref["fuel"]
    q_kg, q_mol = q_nist(fuel)
    ref_dry, ref_wet = ref["Q_dry_J_per_kg_fuel"], ref["Q_wet_J_per_kg_fuel"]
    out = {"reference_source": ref_path,
           "tolerance_pct": TOL*100,
           "independent_nist_q_molar_J_mol": q_mol,
           "Q_dry": cmp("Q_dry", q_kg, ref_dry),
           "Q_wet": cmp("Q_wet", q_kg, ref_wet),  # water cancels at 298.15 K
           "note": "NIST-JANAF vs San Diego formation-enthalpy residual "
                   "(~1.3-2.5 kJ/mol) is expected and NOT tuned."}
    out["overall"] = out["Q_dry"]["pass"] and out["Q_wet"]["pass"]
    print(json.dumps(out, indent=2))
    return 0 if out["overall"] else 1

if __name__ == "__main__":
    sys.exit(main())