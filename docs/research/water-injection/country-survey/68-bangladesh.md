# Bangladesh — water in the combustion cycle (checked)

Status: DONE (checked). Hermes job 20261116-082142-we-survey-68-bangladesh-water-in-combust (key we-survey-68-bangladesh, profile we-research, OVH gpt-oss-120b throttled, no fallback) ran 8:21–8:52 AM America/Los_Angeles 16 Nov 2026, rc 0, and wrote a one-source draft. The checker opened that source and ran its own English searches on 16 Nov 2026, about 11:20 AM–12:00 PM America/Los_Angeles. Only open sources were used: the BUET-hosted ICME2007 conference proceedings PDF and a public MIGA (World Bank Group) environmental report. No piracy sites were used.

Prompt language: English (Bangladesh's engineering research language). Report language: English.

Water is not treated as a fuel in this note. Hydrogen/"HHO" made from water by electrolysis is excluded (it is not water injection).

## Verification (checker)

### Main finding

**No Bangladeshi production or near-production road vehicle with water injection, no Bangladeshi water-injection product, and no Bangladeshi water-injection patent were found.** One Bangladeshi bench test was confirmed: a 2007 RUET (Rajshahi University of Engineering & Technology) study of an aqueous sodium-carbonate-solution diesel emulsion in a single-cylinder DI diesel engine. It reported NOx down 66 %, CO up 20 %, BSFC down 8 % and brake thermal efficiency up 3.54 %.

Real-world industrial use was found at one power plant. The checker found it; Hermes did not. The 225 MW dual-fuel combined-cycle plant at Bhola (Nutan Bidyut (Bangladesh) Ltd) uses GE gas turbines that have a demineralised-water injection system for NOx control when firing fuel oil (HSD). They run dry low-NOx combustion on gas.

### Sources opened and usable figures

- **Beg, M. R. A.; Sarker, M. R. I.; Rahman, M.; Hoque, S. M. N. (2007)**, *Emission control in DI diesel engine using mixture of aqueous salt solution diesel emulsion*, paper ICME07-TH-38, Proceedings of the International Conference on Mechanical Engineering 2007 (ICME2007), 29–31 December 2007, Dhaka. Department of Mechanical Engineering, RUET. https://me.buet.ac.bd/public/old/icme/icme2007/Proceedings/PDF/ICME07-TH-38.pdf (full text, 4 pages; the `http://` link in the Hermes draft returns HTTP 500 and only the `https://` link works).
  - Quote (abstract): "The salt solution is prepared by mixing 0.2%,0.3%,0.4%,0.5% and 0.6% (sodium carbonate) salt by weight with 10% distilled water. To prepare the diesel emulsion 1% of the emulsifying agent (surfactant TWEEN 80) is added to the neat diesel fuel … The engine is run at 50% constant load with variable speed".
  - Quote (abstract): "formation of NOx is reduced up to 66%, CO is increased up to 20%, BSFC is reduced 8%, exhaust temperature is reduced up to 4% compared to neat diesel and the efficiency of diesel engine is increased about 4%."
  - Quote (conclusions): "(b) Brake thermal efficiency is increased 3.54% by using salt-solution diesel emulsion compared with neat diesel." "e) Exhaust temperature is reduced 3.8%".
  - Quote (Table 1): "Four stroke Diesel Engine … No. of cylinders Single … Bore 95 mm … Compression ratio 20:1 … Rated output 13.2 hp (maximum) … Type of cooling Water evaporative type … Type of starting Hand cranking".
  - Caveat: the paper is not consistent about the best blend. The text says "0.5% Na2CO3", but the abstract and conclusion (f) say "5% sodium carbonate". Its measurements cover a narrow range (one small engine at 50 % load), and no uncertainty is given.
- **ERM India for Nutan Bidyut (Bangladesh) Ltd (28 January 2020)**, *Environment and Social Impact Assessment Report (ESIA) Addendum – Change in Design (CID) of Bhola 225MW Combined Cycle Power Project*, published by MIGA. https://www.miga.org/sites/default/files/2021-09/0518816-NBBL%20ESIA%20Addendum%20Report-Final.pdf (full text, 107 pages).
  - Quote (2.2 Plant Configuration): "The gas turbine is of GE make, equipped with dual fuel (Gas/Fuel Oil) combustion system. The gas turbines will use low NOx combustor for gas fuel and do not require DM Water/ Steam injection for NOx control on gas. However, the gas turbines are equipped with DM water injection system for NOx control on Fuel Oil firing."
  - Quote (Water Systems): "production of DM water for power cycle make-up and Injection Water for Gas Turbines (during liquid fuel operation). The total consumptive water requirement for the 220 MW (Net) CCPP is estimated to be 345 m3/hour." (345 m³/h is the plant's total consumptive water use, not the injection flow.)
  - Quote (1.1): "a dual fuel combined cycle power plant (CCPP) of capacity 220 MW (Gas) / 212 MW (HSD) to be located at Bhola island in Barisal division of Bangladesh."

### Hermes errors corrected

- The Hermes link to the RUET paper used `http://`, which returns HTTP 500; corrected to `https://`.
- Hermes added "≈9.9 kW" for the 13.2 hp rating. That conversion is not in the source, so it was dropped.
- Hermes put the "5 % vs 0.5 %" best-blend figure only implicitly. The checker flags the paper's own inconsistency.
- Hermes wrote **NOT FOUND** for power-generation water injection in Bangladesh. That is corrected: the Bhola 225 MW CCPP ESIA addendum (above) documents GE gas turbines with DM-water injection for NOx control on fuel oil.
- Hermes left three stray files from failed downloads in the job folder: a 403 error page, a gas-company web page and an empty file, all saved as `.pdf`. They are not sources, were never cited, and were moved to the private archive only.

### Excluded / not used

- Foreign water-emulsion and water-injection studies returned by the searches (Malaysia UTP/UMP, Kuwait PAAET, UK Brunel, India, Turkey, Germany): not Bangladeshi.
- The ICMIME-RUET 2013 thermal-engineering programme lists RUET diesel-engine biodiesel-ester work by the same group. It is not water in combustion, so it was not used.
- The Ashuganj (APSCL) MIGA project page discusses NOx and gas-fired plants but does not mention water injection. It was not used.

## Production or near-production road vehicles

NOT FOUND for Bangladesh.

## Research, prototypes and supplier systems

- RUET (Rajshahi), ICME2007: aqueous Na2CO3-solution diesel emulsion (10 % distilled water, 1 % Tween 80) in a single-cylinder 13.2 hp DI diesel at 50 % load. NOx −66 %, CO +20 %, BSFC −8 %, brake thermal efficiency +3.54 %, exhaust temperature −3.8 % (abstract: "up to 4%").
- No Bangladeshi prototype vehicle, supplier system or direct water-injection bench test was found.

## Industrial / power-plant use

- Bhola 225 MW dual-fuel CCPP (Nutan Bidyut (Bangladesh) Ltd; sponsor Shapoorji Pallonji Infrastructure Capital, India): GE gas turbines "equipped with DM water injection system for NOx control on Fuel Oil firing", with low-NOx combustors and no water injection on gas.

## Water-fuel emulsions and other cycles

- The RUET 2007 salt-solution emulsion above.
- NOT FOUND: water-methanol, steam-injection or six-stroke work from Bangladesh.

## Marine and aviation

NOT FOUND: no Bangladeshi marine-diesel or aviation water-injection work.

## Simulators and modeling tools

Simulators found: none after check. Hermes reported NOT FOUND. The RUET paper is experimental only and names no software. A checker search for Bangladeshi water-injection simulation studies (Diesel-RK, ANSYS, Ricardo WAVE) found none. A "Not added" note went into the candidate list, and nothing was installed.
