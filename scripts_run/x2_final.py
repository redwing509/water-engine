#!/usr/bin/env python3
"""X2: Independent verification of module 08 Q_dry/Q_wet and water latent heat.

No Cantera.  Uses NIST-JANAF formation enthalpies (Chase 1998) and CoolProp
(IAPWS-95 via Wagner & Pruss 2002).

Reference: module 08 full08 run (results/full08/oxygen_bookkeeping.json),
  fuel=CH3OH, w=0.6, T=900 K, P=4 MPa.
  Q_dry = 21,508,520.355 J/kg fuel
  Q_wet = 21,508,520.355 J/kg fuel (water cancels at 298.15 K)
Tolerance: +/-0.2%
"""
import json, math, sys

# NIST-JANAF (Chase 1998) formation enthalpies, J/mol at 298.15 K
# https://janaf.nist.gov/
NIST_HF = {
    "CH3OH": -200941.5,  # CH3OH(g)
    "C2H5OH": -234800.0,  # C2H5OH(g)
    "CO2":   -393522.4,   # CO2(g)
    "H2O":   -241826.4,   # H2O(g)
    "H2O_l": -285830.0,   # H2O(l)
    "O2":    0.0,
    "N2":    0.0,
}
# IUPAC 2021 molar masses, kg/mol
C, H, O = 12.011e-3, 1.008e-3, 15.999e-3
MW = {
    "CH3OH": C + 4*H + O,        # 0.032042
    "C2H5OH": 2*C + 6*H + O,     # 0.046068
    "H2O": 2*H + O,
    "CO2": C + 2*O,
}
FUELS = {"CH3OH": (1,4,1), "C2H5OH": (2,6,1)}
T_REF, TOL = 298.15, 0.002
REF = {"CH3OH": {"Q_dry": 21508520.35547747,
                 "Q_wet": 21508520.355477475}}

def stoich_o2_bug(fuel):
    """Module 08 bug: stoich_o2 = atoms[1] (H atom count), not O2 demand."""
    c, h, o = FUELS[fuel]
    return h                      # 4.0 for CH3OH (should be 1.5)

def stoich_o2_correct(fuel):
    c, h, o = FUELS[fuel]
    return c + h/4.0 - o/2.0      # 1.5 for CH3OH

def Q_dry_int_energy_method(fuel, hf, stoich_o2, stoich_n2):
    """Reproduce module 08's exact int_energy_mole algorithm using
    formation enthalpies from `hf`.

    Module 08 uses:
      U_k(T_ref) = Hf_k(T_ref)  [independent elements in ref state -> U=0]
      Q = (U_react * n_react_total - U_prod * n_prod_total) / mol_per_kg
    where U is the mixture internal energy in J/kmol (total, not per mole).
    At T_ref with all elements in ref state, U_mix = sum of Uf of species.
    """
    c, h, o = FUELS[fuel]
    n_co2, n_h2o = float(c), h/2.0
    n_n2 = stoich_n2
    n_react_total = 1.0 + stoich_o2 + n_n2
    n_prod_total = n_co2 + n_h2o + n_n2
    U_react = (1.0*hf["CH3OH"] if fuel=="CH3OH" else hf[fuel]
               + stoich_o2*hf["O2"] + n_n2*hf["N2"])
    U_prod = (n_co2*hf["CO2"] + n_h2o*hf["H2O"] + n_n2*hf["N2"])
    Q_molar = U_react - U_prod        # J per mol fuel
    return Q_molar / MW[fuel], Q_molar

def water_hfg():
    """Water latent heat: CoolProp (IAPWS-95) vs NIST-JANAF."""
    out = {}
    # h_fg = H2O(g) - H2O(l) > 0
    nist_mol = NIST_HF["H2O"] - NIST_HF["H2O_l"]  # 44003.6 J/mol
    out["nist_j_mol"] = nist_mol
    out["nist_j_kg"] = nist_mol / MW["H2O"]
    try:
        from CoolProp.CoolProp import PropsSI
        h_l = PropsSI("Hmass","T",T_REF,"Q",0,"Water")
        h_v = PropsSI("Hmass","T",T_REF,"Q",1,"Water")
        out["coolprop_j_kg"] = h_v - h_l
        out["coolprop_j_mol"] = (h_v - h_l) * MW["H2O"]
        d = abs(out["coolprop_j_kg"] - out["nist_j_kg"]) / out["nist_j_kg"]
        out["rel_diff"] = d
        out["pass"] = d <= TOL
    except ImportError:
        out["coolprop_j_kg"] = None
    return out

def cmp(qty, indep, ref, tol=TOL):
    d = abs(indep - ref)/abs(ref)
    return {"quantity": qty, "independent_J_kg": round(indep,3),
            "reference_J_kg": round(ref,3), "rel_diff_pct": round(d*100,4),
            "tolerance_pct": tol*100, "pass": d <= tol}

def main():
    out = {"tolerance_pct": TOL*100,
           "reference_source": "results/full08/oxygen_bookkeeping.json "
                              "(fuel=CH3OH, w=0.6, T=900 K, P=4 MPa; "
                              "Q evaluated at T_ref=298.15 K)"}
    # Water latent heat
    out["water_latent_heat"] = water_hfg()
    # Q for CH3OH: (a) NIST-JANAF with module 08's buggy stoich (reproduce ref)
    # (b) NIST-JANAF with correct stoich (true value)
    fuel = "CH3OH"
    sb, sc = stoich_o2_bug(fuel), stoich_o2_correct(fuel)
    nb, nc = sb*3.76, sc*3.76
    # Note: with NIST (O2/N2 h_f = 0), excess O2/N2 do not enter the
    # energy balance, so both stoichiometries give the same Q.  With the
    # San Diego mechanism (O2/N2 h_f != 0) they differ; see diagnostics.
    q_bug, _   = Q_dry_int_energy_method(fuel, NIST_HF, sb, nb)
    q_good, qm = Q_dry_int_energy_method(fuel, NIST_HF, sc, nc)
    ref_dry, ref_wet = REF[fuel]["Q_dry"], REF[fuel]["Q_wet"]
    out["Q_dry"] = {
        "module08_stoich_o2_bug_value": sb,
        "correct_stoich_o2": sc,
        "buggy_stoich_n2": nb,
        "correct_stoich_n2": nc,
        "independent_nist_bug_stoich": q_bug,
        "independent_nist_correct_stoich": q_good,
        "q_molar_J_mol": qm,
        "comparison_vs_reference_bug_stoich":
            cmp("Q_dry", q_bug, ref_dry),
        "comparison_vs_reference_correct_stoich":
            cmp("Q_dry (correct stoich)", q_good, ref_dry),
        "Q_wet_note": "Q_wet == Q_dry exactly: water enters and leaves at "
                      "298.15 K reference temperature (identity reaction)",
        "comparison_Q_wet_vs_reference":
            cmp("Q_wet", q_bug, ref_wet),
    }
    print(json.dumps(out, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
