"""X2 re-check: independent NIST-JANAF Q_dry vs module 08's Q_dry.

No Cantera.  Reads the oxygen_bookkeeping.json produced by the corrected
module 08 --full run and compares Q_dry_J_per_kg_fuel against an independent
computation from NIST-JANAF formation enthalpies (gas species, 298.15 K,
0 K reference).

Tolerance: +/-0.2 %.  The documented residual between San Diego mechanism
formation enthalpies and NIST-JANAF is ~1.3-2.5 kJ/mol, i.e. ~0.06 % at
21 MJ/kg for CH3OH -- well inside tolerance.  Do NOT tune to remove it.

Usage:  python3 x2_final_new.py [path/to/oxygen_bookkeeping.json]
"""
import json, sys

R = 8.31446261815324  # J/mol/K
T_REF = 298.15

# NIST-JANAF 298.15 K standard enthalpies of formation, gas species (kJ/mol).
DHF_NIST = {
    "CH3OH": -201.06,   # gas  (NIST-JANAF)
    "CO2":   -393.509,
    "H2O":   -241.818,   # gas
    "CO":    -110.521,
    "H2":       0.0,
    "O2":        0.0,
    "N2":        0.0,
    "C2H5OH":  -234.54,  # gas
    "C2H4":     52.30,
    "CH4":      -74.87,
}

# fuel: (atoms_dict, mw_g_per_mol)   atoms = (C,H,O)
FUEL = {
    "CH3OH":    (dict(C=1, H=4, O=1), 32.042),
    "C2H5OH":   (dict(C=2, H=6, O=1), 46.068),
    "CH4":      (dict(C=1, H=4, O=0), 16.043),
}


def oxygen_demand(fuel):
    f = FUEL[fuel][0]
    return f["C"] + f["H"] / 4.0 - f["O"] / 2.0


def nist_q_dry_kJ_per_kg_fuel(fuel):
    """Independent Q_dry (kJ/kg fuel) from NIST-JANAF dHf^0 (298.15 K).

    Dry stoichiometric products assumed: CO2 + H2O(g) for full combustion.
    """
    f = FUEL[fuel][0]
    co2 = f["C"]
    h2o = f["H"] / 2.0
    mw = FUEL[fuel][1]  # g/mol
    dHf_r = DHF_NIST[fuel]
    dHf_p = co2 * DHF_NIST["CO2"] + h2o * DHF_NIST["H2O"]
    Q_molar_kJ_per_mol = dHf_r - dHf_p   # fuel + O2 -> products (negative dH_rxn)
    Q_kg = Q_molar_kJ_per_mol * 1e3 / (mw / 1e3)  # J/kg = kJ/mol_fuel / (kg/mol_fuel)
    return Q_kg / 1e3  # back to kJ/kg


def main(path="results/full08/oxygen_bookkeeping.json"):
    d = json.load(open(path))
    # Accept either the module 08 bookkeeping JSON or the X2 evidence JSON
    if "Q_dry_J_per_kg_fuel" in d:
        fuel = d.get("fuel", "CH3OH")
        q_new = float(d["Q_dry_J_per_kg_fuel"])
    elif "module08" in d:
        fuel = d.get("fuel", "CH3OH")
        q_new = float(d["module08"]["Q_dry_J_kg"])
    else:
        raise KeyError("Q_dry_J_per_kg_fuel")
    q_ref = nist_q_dry_kJ_per_kg_fuel(fuel) * 1e3  # back to J/kg
    rel_pct = (q_new - q_ref) / q_ref * 100.0
    tol_pct = 0.2
    ok = abs(rel_pct) <= tol_pct
    print(f"module08 Q_dry = {q_new:.1f} J/kg  ({q_new/1e6:.6f} MJ/kg)")
    print(f"NIST-JANAF  Q = {q_ref:.1f} J/kg  ({q_ref/1e6:.6f} MJ/kg)")
    print(f"Delta = {rel_pct:+.4f}%   (tol +/-{tol_pct}%)")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "results/full08/oxygen_bookkeeping.json"))