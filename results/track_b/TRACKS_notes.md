## Findings so far (hand-written; numbers from the tables above)

1. **Pre-stated 0.1-pp rule stops gasoline / E-blends / CH4 / ethanol-normal at step 1.** Each first step
   gains 2-8e-5 absolute (both engines agree to < 0.001 pp on the gain), below the 1e-4 threshold, so the
   Track B best stays w = 0 for those chains. The threshold was NOT changed after seeing data.
2. **But the gain is real and steady:** the labelled probes (not Track B steps) at the same hardware show a
   near-linear rise in both engines up to w = 10 %: PRF87 +0.53 pp, PRF91 +0.38, PRF97 +0.40, E10 +0.44,
   E85 +0.72 (normal) / +0.42 (hot), C2H5OH-normal +0.45, CH4 +0.22 (normal, MBT-limited) / +0.42 (hot).
   Mechanism (Module 03): knock relief lets CA50 advance towards MBT (e.g. E85 14.8 -> 11.7 deg); NO proxy
   falls 10-25 %; p_max rises 1-13 %. **Decision for James:** keep the per-step 0.01-pp rule (strict), or
   judge gains per 1-pp block (10 steps) / at the 3e-5 step-error level, which would let these chains walk on.
3. **Methanol (normal) and ethanol (hot) pass the rule** (~1.5e-4 and ~1.2e-4 per step, CRN gain positive
   each step) and are still stepping; MAX_STEPS = 100 caps them at w = 0.10.
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
