## Findings so far (hand-written; numbers from the tables above)

0. **Continuation rule changed by James after seeing the first data (2026-10-24 19:01 PDT).** Old rule (pre-stated):
   step gain > 1e-4 absolute in Module 03 plus positive M03-CRN gain. New rule: gain > numerical noise,
   **3.3e-5 absolute** (largest measured shift of the 0.5-CAD production-step efficiency, verification/x5_m03/RESULTS_FIX.md,
   X5 C2H5OH/best_overall +0.0073 % of 0.45618; the pure 0.5 vs 0.25 CAD refinement difference is only <= 6.1e-6 and
   the spark-bisection tolerance is ~2e-5, so 3.3e-5 is a conservative noise floor). Both engines must still gain on
   every step, the step is still 0.1 pp, the cap is 100 steps, raised to 200 only for chains still gaining at 100 (recorded per
   chain). Old-rule results are kept as the variant `rule_1e-4` (files without `__noise`).
1. **Under the old rule** gasoline / E-blends / CH4 / ethanol-normal stopped at step 1 (first-step gains 2-8e-5,
   both engines within 0.001 pp of each other); methanol-normal stopped at w = 0.041 (liquid) / 0.049 (humid_evap), and
   ethanol-hot stopped at w = 0.040 / 0.045, when per-step gains fell just under 1e-4.
2. **Under the noise rule** every gasoline, E10, E85 (normal and hot), CH4-hot and ethanol-normal chain passes
   step 1 in liquid and humid_evap mode, and the chains are walking on (see the current-rule table for live best w and
   d_eta). CH4-normal stops at step 0 in both modes (first-step gain 1.9e-5 liquid / 2.4e-5 humid_evap: CA50 is already MBT-limited,
   so there is little knock relief to collect). **humid_ambient stops at step 0 for every fuel** (gain -3.4e-6 to +9.3e-6:
   vapour at intake temperature dilutes and lowers O2 partial pressure without the cooling that relieves knock).
   The labelled probes (not steps) suggest near-linear gains up to w = 10 %: PRF87 +0.53 pp, PRF91 +0.38,
   PRF97 +0.40, E10 +0.44, E85 +0.72 / +0.42 (hot), C2H5OH-normal +0.45, CH4-hot +0.42. So many chains are expected
   to reach cap 100 still gaining and be extended to 200.
3. **Mechanism (Module 03, both engines agree on efficiency):** knock relief lets the knock-limited CA50 advance
   (e.g. CH3OH 14.6 -> ~11 deg, C2H5OH-hot 14.9 -> ~12.3 deg), the NO proxy falls (-4 to -9 % at the alcohol chains so far,
   10-25 % at the 10 % probes), and p_max rises (+9 to +18 % on the alcohol chains so far). That p_max rise is the cost to watch against hardware limits.
4. **Humid intake (Track B):** per 0.1-pp step, fully-evaporated intake water (humid_evap) gives ~85-110 %
   of the liquid-mode gain (evaporative cooling -> denser, cooler charge, knock relief); water vapour already
   at intake temperature (humid_ambient, no cooling) gives only ~10 % (dilution + lower O2 partial pressure
   roughly cancel the small knock relief). So the benefit of humid air is cooling- and knock-limited - it
   only helps where spark is knock-limited and is re-optimised.
5. **Humid intake (Track A):** water-majority water cannot be carried as vapour. With intake evaporative
   cooling the charge saturates after ~5 % of the water (q ~ 12-13 g/kg dry air at 320 K intake); without
   cooling ~34 %. The rest would condense in the runners/ports (liquid film/droplets), i.e. it reverts to the
   liquid-injection case. See the Track A humid grid table for both engines.
6. **Hot regime:** PRF87/91/97, E10 and CH3OH have no eligible dry point (knock-limited CA50 > 15 deg even at
   CR 9), so there is no Track B hot chain for them; E85, C2H5OH and CH4 have hot chains.

## Literature check (humid intake)

* mail:/opt/knowledge/water-engine has **no intake-humidity entries** (grep "humid": none). Literature used:
  - Gasoline FAQ s7.12 / CRC data (refs [27,28,38] there): +1 g H2O/kg dry air lowers octane requirement by
    0.25-0.32 MON. One Track B gasoline step (w += 0.001) = q ~ 0.067 g/kg -> ~0.02 MON per step - consistent
    with the tiny per-step gains; w = 10 % (q ~ 7 g/kg) -> ~2 MON, consistent with the 0.4-0.5 pp probe gains.
  - ASTM D2699/D2700 hold CFR intake humidity at 3.6-7.2 g/kg because humidity shifts knock ratings.
  - SAE J1349 power correction uses dry-air pressure: vapour displaces O2 and lowers power/IMEP - the model
    captures this through fixed p_IVC (vapour replaces air).
  - Khatri et al., Int. J. Engine Res. 2021 (doi:10.1177/1468087420940854): knock suppression scales with
    total in-cylinder water (kappa effect), not relative humidity per se - supports comparing modes by w.
  - J. Eng. Gas Turbines Power 139(5) 051501 (SACI, 32 -> 60 % RH at fixed controls): CA50 retarded, BSFC
    288 -> 301 g/kWh, NOx down - humidity hurts efficiency when spark is NOT re-optimised; the benefit is
    knock-limited.
  - Library entries already in use: WE-14 Hoppe 2016 (water injection +3.3-3.8 % near min BSFC, up to +16 %
    at full knock-limited load), WE-20 Skippon (port vaporisation fraction), WE-21 Lauer (E85 film).

## What each track can borrow from the other

* **A -> B:** Track A shows water lets CR rise (alcohol optima at CR 23, w 0.3-0.4). Track B holds CR at the
  dry optimum; next Track B step: re-optimise CR at the best/probe w (hardware + water co-optimisation),
  and use Track A's w ~ 0.3 optimum as the expected far end of the methanol chain.
* **A -> B:** Track A's Module 09 film/retained-liquid coupling (PR 8) is the right model for any water above
  the intake saturation limit found here.
* **B -> A:** Track B's continuous spark optimiser gives better dry references (CH3OH 0.4238 vs Track A's
  0.4207 with the 2-CAD retard search) - quote Track A gains against these and port the optimiser.
* **B -> A:** humid-intake saturation (~5 % of water-majority water as vapour) means Track A water-majority
  cases must be treated as liquid/film delivery; humid intake only helps the first few % of water.
* **Both:** gasoline surrogates now exist in mechanisms/trackb_fuels.yaml for comparisons.

## Caveats

* Gasoline/E-blend knock uses the Douaud & Eyzat 1978 (SAE 780080) octane correlation; alcohol and CH4 knock
  uses Module 02 kinetic fits - different methodologies, compare across families with care. E85 octane
  (108.5) is extrapolated beyond the correlation range.
* Knock margin, CA50 limit and NO proxy are Module 03 only; M03-CRN has no knock/NOx model.
* Fixed p_IVC; no gas-exchange model, so volumetric-efficiency effects beyond charge density are not modelled.
* Liquid mode uses legacy Module 03 water handling (half evaporates in the intake); no Module 09 film profile
  for these points.
* Not yet peer-review verified (2+ independent engines pending).
