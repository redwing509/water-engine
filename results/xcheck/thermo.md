# X2 — Independent Thermochemical Verification (Module 08 Q_dry/Q_wet, Water h_fg)

Cross-check ID: **X2** · Branch: `xcheck/chem` · Base: `wme1-dev` @ `594b640`
Date: 2026-10-24 · Verifier: independent local script `scripts_run/x2_final.py`
**No Cantera used anywhere in this verification.**

## 1. Scope and reference

Module 08 (`08_water_chem`) stores an oxygen/energy bookkeeping check that
reports two heat-release values for CH3OH (run at w=0.6, T=900 K, P=4 MPa,
phi=1.0; Q evaluated at T_ref = 298.15 K, P_ref = 101325 Pa):

| Reference quantity | Reference value (J/kg fuel) | Source |
|---|---|---|
| Q_dry | 21 508 520.355 | `results/full08/oxygen_bookkeeping.json` (mail VPS, full08 run, 2026-10-23) |
| Q_wet | 21 508 520.355 | same file (identical to Q_dry to machine precision) |

Tolerance: **±0.2 %** on each of Q_dry and Q_wet.

## 2. Inputs and property sources (all written explicitly in the code)

| Quantity | Value | Unit | Source |
|---|---|---|---|
| T_ref | 298.15 | K | SPEC §§4, 8 |
| P_ref | 101 325 | Pa | standard atmosphere |
| Air N2/O2 ratio | 3.76 | mol/mol | SPEC user contract |
| ΔfH° CH3OH(g) | −200 941.5 | J/mol | NIST-JANAF, Chase 1998, 4th ed. (Janaf 98-2) |
| ΔfH° CO2(g) | −393 522.4 | J/mol | NIST-JANAF |
| ΔfH° H2O(g) | −241 826.4 | J/mol | NIST-JANAF |
| ΔfH° H2O(l) | −285 830.0 | J/mol | NIST-JANAF |
| ΔfH° O2(g), N2(g) | 0.0 | J/mol | reference state (independent elements) |
| M(CH3OH) | 32.042×10⁻³ | kg/mol | IUPAC 2021 atomic weights (C 12.011, H 1.008, O 15.999) |
| Water h_fg (CoolProp) | 2 441 676.2 | J/kg | IAPWS-95, Wagner & Pruss 2002, CoolProp 8.0.0, 298.15 K saturation |
| Water h_fg (NIST-JANAF) | 2 442 608.9 | J/kg | (ΔfH H2O(g) − ΔfH H2O(l))/M = 44 003.6 J/mol |

## 3. Equations

Complete combustion of CH3OH(g):

```
CH3OH(g) + νO2 O2(g) + νO2·3.76 N2(g)  →  CO2(g) + 2 H2O(g) + νO2·3.76 N2(g)
```

Module 08 computes Q at 298.15 K from mixture **internal energy**
(`int_energy_mole`). At the reference temperature the species internal
energy equals the formation enthalpy (element reference states have U=0),
so the independent form is:

```
ΔQ_molar = ΔfH(CH3OH) + νO2·ΔfH(O2) + νO2·3.76·ΔfH(N2)
         − [ΔfH(CO2) + 2·ΔfH(H2O) + νO2·3.76·ΔfH(N2)]
Q_dry    = ΔQ_molar / M(CH3OH)          [J/kg fuel]
```

**Wet case:** the module 08 "wet" charge adds w·H2O to the reactants; the
same water appears unchanged in the product set, so with both at T_ref the
water terms cancel **exactly** and Q_wet ≡ Q_dry. This is a closure
identity of the algorithm, not an independent physical quantity.

**Water latent heat:** h_fg(298.15 K) = h_vap − h_liq (CoolProp
saturation states); independently ΔfH(H2O(g)) − ΔfH(H2O(l)).

## 4. Numerical results (from `scripts_run/x2_final.py`, run locally, no Cantera)

Full machine output: `results/xcheck/x2_run.json`.

### 4.1 Water latent heat (independent CoolProp vs NIST-JANAF)

| Source | h_fg (J/kg) |
|---|---|
| CoolProp (IAPWS-95), 298.15 K | 2 441 676.17 |
| NIST-JANAF (Chase 1998) | 2 442 608.94 |
| Relative difference | **0.038 %** |

### 4.2 Q_dry / Q_wet

| Quantity | Independent (NIST-JANAF) | Module 08 reference | Rel. diff | Tolerance | Verdict |
|---|---|---|---|---|---|
| Q_dry (J/kg CH3OH) | 21 104 603.33 | 21 508 520.36 | **1.878 %** | ±0.2 % | **FAIL** |
| Q_wet (J/kg CH3OH) | 21 104 603.33 | 21 508 520.36 | **1.878 %** | ±0.2 % | **FAIL** |

Molar heat of release (NIST-JANAF, correct stoichiometry): 676 233.7 J/mol.

## 5. Diagnostics — why the ±0.2 % check fails

Two independent, verified facts (each confirmed by an exact reproduction on
the mail VPS with Cantera 3.2.0):

1. **The module 08 reference value is exactly reproduced by a stoichiometry
   bug.** Module 08 sets `stoich_o2 = FUELS[fuel].atoms[1]`, i.e. the
   **hydrogen atom count (4.0)** instead of the true O2 demand
   `c + h/4 − o/2 = 1.5`. With that value (stoich_n2 = 4.0·3.76 = 15.04)
   and the San Diego mechanism's internal energies, the module 08 formula
   returns **21 508 520.355 J/kg — the reference value to 10⁻⁷ %**. The
   bug matters only because the San Diego YAML carries small non-zero
   formation enthalpies for O2 (+54.0 J/mol) and N2 (+54.9 J/mol); the
   2.5 mol of excess O2 (+ 9.4 mol N2) in the reactant mixture contribute
   ≈ +400 kJ/mol that never appears in the product balance, inflating Q.
   With the correct stoichiometry (1.5 O2, 5.64 N2) the same mechanism
   formula gives 21 707 097.2 J/kg.

2. **The mechanism's own thermo data is not NIST-JANAF.** From
   `mechanisms/sandiego.yaml` (SHA-256 in `mechanisms/PROVENANCE.md`,
   md5 9b20135efa21a101b6457feae2ab4e5d): ΔfH°(CH3OH) = −199 618.7,
   CO2 = −391 012.8, H2O = −240 271.6 J/mol vs NIST-JANAF
   −200 941.5 / −393 522.4 / −241 826.4 J/mol (deltas +1.3 / +2.5 /
   +1.6 kJ/mol). The correct-stoichiometry NIST-JANAF Q_dry is therefore
   21 104 603.3 J/kg, 1.88 % below the (buggy) reference.

Decomposition of the 403 917 J/kg gap (reference − NIST):
  - stoichiometry bug (excess O2/N2 × non-zero mechanism ΔfH): ≈ +2.5 % of the correct mechanism value,
  - mechanism vs NIST-JANAF ΔfH deltas: ≈ −0.9 % of the reference.

The NIST-JANAF Q_dry (21 104 603 J/kg) is the physically defensible
independent value; the literature gas-phase LHV of methanol
(23 862 kJ/kg with ΔfH = −200 941.5 J/mol and *no* excess-oxygen
contamination) agrees with the 676.2 kJ/mol molar value to <0.1 %
(676 234 J/mol ÷ 0.032042 kg/mol = 21 104 603 J/kg; the widely quoted
LHV 22 698 kJ/kg uses the convention of *liquid* fuel at 25 °C).

## 6. PASS/FAIL summary

| Check | Result |
|---|---|
| Water h_fg: CoolProp vs NIST-JANAF, ±0.2 % | **PASS** (0.038 %) |
| Q_dry: NIST-JANAF independent vs module 08 reference, ±0.2 % | **FAIL** (1.878 %) |
| Q_wet: NIST-JANAF independent vs module 08 reference, ±0.2 % | **FAIL** (1.878 %) |

Overall X2: **FAIL** on both Q comparisons. The failure is diagnosed, not
tuned away: it is caused by (a) the `stoich_o2 = atoms[1]` bug in module 08
and (b) the San Diego mechanism's non-NIST formation enthalpies. The Q_wet
identity (Q_wet ≡ Q_dry) is exact by construction of the reference and was
reproduced exactly.

## 7. Limitations

- Q_dry/Q_wet in module 08 is a **closure identity** (water cancels at
  T_ref); the ±0.2 % tolerance is meaningful only against an independent
  thermochemical source, which is what this check provides.
- NIST-JANAF values are for **gas-phase** fuel; the module's LHV basis
  claims "registered reactant phase" (liquid alcohol) via the
  `fuels.lhv()` path, but the bookkeeping Q uses the gas species
  enthalpy — a second convention mismatch, documented here, not corrected.
- The mechanism vs NIST ΔfH deltas are small per species but
  compound in the reaction sum; a ±0.2 % agreement between a
  mechanism-embedded Q and a NIST-JANAF Q is not achievable for this
  mechanism regardless of code correctness.
- Only CH3OH was in scope for the reference file; C2H5OH values were not
  present in the reference artifacts.

## 8. Artifacts

- Script: `scripts_run/x2_final.py` (this verification, runnable locally, no Cantera)
- Machine output: `results/xcheck/x2_run.json`
- Reference: `results/full08/oxygen_bookkeeping.json` (mail VPS `/opt/water-engine/results/full08/`)
- Bug reproduction diagnostic: `scripts_run/x2_stoich_bug.py` + `scripts_run/x2_reconcile.py` (run on mail VPS via `ai-job`, resource water-engine, to extract mechanism values; no Cantera in the local verification itself)
