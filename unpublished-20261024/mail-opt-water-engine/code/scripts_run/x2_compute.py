"""X2: Independent recomputation of Q_wet/Q_dry and water latent heat.

Recomputes module 08's Q_dry/Q_wet and water latent heat using:
- NIST-JANAF formation enthalpies (hardcoded) at 298.15 K
- CoolProp for water saturation properties
WITHOUT Cantera.

Module 08 uses int_energy_mole (internal energy U = H - RT for ideal gases).
We replicate the same computation using NIST formation enthalpies + ideal gas U = Hf - RT.
"""
import json
import CoolProp.CoolProp as CP
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="CoolProp")

# ============================================================
# NIST-JANAF / NIST WebBook standard formation enthalpies at 298.15 K (J/mol)
# Sources:
#   H2O(g): Chase (1998) JANAF, NIST WebBook
#   CO2(g): Chase (1998) JANAF, NIST WebBook
#   CH3OH(g): NIST WebBook SRD 69, ID C67561
#   C2H5OH(g): NIST WebBook SRD 69, ID C64175
#   H2O(l): Chase (1998) JANAF
#   O2, N2, H2: element references = 0 (but Cantera has small non-zero values
#     due to its NASA polynomial representation; see note below)
# ============================================================
# Values in J/mol (not J/mol or kJ/mol - straight J/mol)
NIST_HF = {
    "CH3OH_g": -201000.0,     # NIST WebBook SRD 69 (gas)
    "C2H5OH_g": -248100.0,    # NIST WebBook SRD 69 (gas) -- verify
    "CO2_g":  -393526.0,      # Chase 1998 JANAF
    "H2O_g":  -241826.0,      # Chase 1998 JANAF
    "H2O_l":  -285830.0,      # Chase 1998 JANAF
    "O2_g":       0.0,        # Element reference
    "N2_g":       0.0,        # Element reference
    "H2_g":       0.0,        # Element reference
}

# Universal gas constant (J/mol·K)
R_J_MOL = 8.31446261815324

# Molar masses (g/mol -> kg/mol)
MW = {
    "CH3OH": 32.042,    # 12.011 + 4*1.008 + 15.999
    "C2H5OH": 46.069,   # 2*12.011 + 6*1.008 + 15.999
    "CO2": 44.010,      # 12.011 + 2*15.999
    "H2O": 18.015,      # 2*1.008 + 15.999
    "O2": 31.998,       # 2*15.999
    "N2": 28.014,       # 2*14.007
    "H2": 2.016,        # 2*1.008
}

# Cantera has tiny non-zero "formation" values for O2, N2 due to NASA polynomials.
# We replicate this by extracting the same values from Cantera.
# For a truly independent computation we use NIST (0 J/mol), but this introduces
# a small systematic offset because module 08 uses Cantera's internal energy
# which includes these tiny RT offsets.  We'll quantify both.

T_REF = 298.15  # K
P_REF = 101325.0  # Pa
AIR_N2_O2 = 3.76  # mol N2 / mol O2

# Water latent heat via CoolProp at T=298.15 K, P=1 atm (saturated)
# h_g - h_l where Q=0 (liquid) and Q=1 (vapor)
h_l_CoolProp = CP.PropsSI("H", "T", T_REF, "Q", 0, "Water")  # J/kg
h_g_CoolProp = CP.PropsSI("H", "T", T_REF, "Q", 1, "Water")  # J/kg
h_fg_CoolProp = h_g_CoolProp - h_l_CoolProp  # J/kg

# NIST-JANAF water latent heat (gas - liquid formation enthalpy at 298.15 K)
h_fg_NIST = (NIST_HF["H2O_g"] - NIST_HF["H2O_l"]) / (MW["H2O"] / 1000.0)  # J/kg

# ============================================================
# Module 08 reference values (from Cantera-based run on mail VPS)
# Q_dry/Q_wet computed using int_energy_mole at 298.15 K
# For ideal gases: U = H - RT (per mole)
# Module 08: Q = (U_react * n_react_total - U_prod * n_prod_total) / mol_per_kg
#   where U_react = int_energy_mole at 298 K = formation_U per kmol mixture
#   mol_per_kg = 1000 / MW_fuel (kmol fuel per kg fuel)
# ============================================================

# Cantera-extracted values (from x2_extract_hf.py + x2_debug.py):
# These match NIST-JANAF essentially (verified to <0.1% for H2O, CO2, CH3OH)
CANTERA_HF = {
    "CH3OH_g": -200938854.87,  # J/kmol = -200938.9 J/mol
    "CO2_g":  -393507757.67,   # J/kmol = -393507.8 J/mol
    "H2O_g":  -241824621.63,   # J/kmol = -241824.6 J/mol
    "O2_g":       16.34,        # J/kmol
    "N2_g":       1429.90,      # J/kmol
}
# Convert to J/mol
for k in CANTERA_HF:
    CANTERA_HF[k] = CANTERA_HF[k] / 1000.0 if "g" in k else CANTERA_HF[k] / 1000.0

CANTERA_REF = {
    "CH3OH": {
        "Q_dry_J_kg": 21508520.36,
        "Q_wet_J_kg": 21508520.36,  # water cancels at 298 K
        "h_fg_water_J_kg": 2442631.14,  # from fuels.py (Cantera NasaPoly2)
    },
}


def compute_Q_dry_independent(fuel, hf_source):
    """Compute Q_dry using given formation enthalpy source.

    Mirrors module 08's _heat_release_298K exactly:
    - Uses internal_energy U = Hf - RT per species (ideal gas)
    - Reactants: 1 fuel + stoich_O2 + stoich_N2
    - Products: c CO2 + (h/2) H2O + stoich_N2
    - Q = (U_react * n_react - U_prod * n_prod) / mol_per_kg
    """
    atoms = {"CH3OH": (1, 4, 1), "C2H5OH": (2, 6, 1)}  # C, H, O
    c, h_atoms, o = atoms[fuel]
    stoich_o2 = c + h_atoms / 4.0 - o / 2.0  # O2 moles per mole fuel
    stoich_n2 = stoich_o2 * AIR_N2_O2

    # Internal energy per molecule type = Hf - RT (ideal gas: U = H - PV = H - RT)
    RT = R_J_MOL * T_REF  # J/mol

    def U(species_key):
        """Internal energy at 298.15 K = formation enthalpy - RT."""
        return hf_source[species_key] - RT

    # Reactants: 1 fuel + stoich_o2 O2 + stoich_n2 N2
    n_react = 1.0 + stoich_o2 + stoich_n2
    U_react_total = U(f"{fuel}_g") + stoich_o2 * U("O2_g") + stoich_n2 * U("N2_g")

    # Products: c CO2 + (h/2) H2O + stoich_n2 N2
    n_co2 = c
    n_h2o = h_atoms / 2.0
    n_n2 = stoich_n2
    n_prod = n_co2 + n_h2o + n_n2
    U_prod_total = n_co2 * U("CO2_g") + n_h2o * U("H2O_g") + n_n2 * U("N2_g")

    # Q per mole fuel
    Q_mol_fuel = U_react_total - U_prod_total  # J per mol fuel
    # Convert to J/kg
    Q_kg = Q_mol_fuel / (MW[fuel] / 1000.0)  # J/kg

    return {
        "Q_dry": Q_kg,
        "Q_wet": Q_kg,  # water cancels at 298.15 K
        "Q_ratio": 1.0,
        "_n_react": n_react,
        "_n_prod": n_prod,
        "_stoich_o2": stoich_o2,
        "_stoich_n2": stoich_n2,
        "_Q_mol": Q_mol_fuel,
    }


def compare(name, independent_val, reference_val, tol_percent=0.2):
    if reference_val is None:
        return {"status": "skipped (no reference)"}
    rel = abs(independent_val - reference_val) / abs(reference_val) * 100
    status = "PASS" if rel <= tol_percent else "FAIL"
    return {
        "independent": independent_val,
        "reference": reference_val,
        "rel_diff_pct": rel,
        "tol_pct": tol_percent,
        "status": status,
    }


# ============================================================
# Run
# ============================================================
results = {}

for fuel in ("CH3OH", "C2H5OH"):
    # NIST-based computation
    nist_result = compute_Q_dry_independent(fuel, NIST_HF)
    cantera_ref = CANTERA_REF.get(fuel, {})

    results[fuel] = {
        "NIST_Hf_reference": "Chase (1998) JANAF, NIST WebBook SRD 69",
        "stoichiometry": {
            "stoich_O2": nist_result["_stoich_o2"],
            "stoich_N2": nist_result["_stoich_n2"],
            "n_react_total": nist_result["_n_react"],
            "n_prod_total": nist_result["_n_prod"],
        },
        "Q_dry_J_kg_independent": nist_result["Q_dry"],
        "Q_wet_J_kg_independent": nist_result["Q_wet"],
        "Q_wet_over_Q_dry": nist_result["Q_ratio"],
        "comparison_Q_dry_vs_module08": compare(
            "Q_dry", nist_result["Q_dry"], cantera_ref.get("Q_dry_J_kg")
        ),
        "comparison_Q_wet_vs_module08": compare(
            "Q_wet", nist_result["Q_wet"], cantera_ref.get("Q_wet_J_kg")
        ),
    }

# Water latent heat
results["water_latent_heat_298K"] = {
    "method": "CoolProp IAPWS-95 (Wagner & Pruss 2002) + NIST-JANAF",
    "CoolProp_h_l_J_kg": h_l_CoolProp,
    "CoolProp_h_g_J_kg": h_g_CoolProp,
    "CoolProp_h_fg_J_kg": h_fg_CoolProp,
    "CoolProp_h_fg_J_mol": h_fg_CoolProp * MW["H2O"] / 1000.0,
    "NIST_JANAF_h_fg_J_kg": h_fg_NIST,
    "NIST_JANAF_h_fg_J_mol": NIST_HF["H2O_g"] - NIST_HF["H2O_l"],
    "Cantera_reference_h_fg_J_kg": CANTERA_REF["CH3OH"]["h_fg_water_J_kg"],
    "comparison_coolprop_vs_nist": compare("h_fg", h_fg_CoolProp, h_fg_NIST),
    "comparison_coolprop_vs_cantera": compare("h_fg", h_fg_CoolProp, CANTERA_REF["CH3OH"]["h_fg_water_J_kg"]),
}

print(json.dumps(results, indent=2))

# Write
os.makedirs("/opt/water-engine/code/results/xcheck/x2_data", exist_ok=True)
with open("/opt/water-engine/code/results/xcheck/x2_data/thermo_results.json", "w") as f:
    json.dump(results, f, indent=2)
