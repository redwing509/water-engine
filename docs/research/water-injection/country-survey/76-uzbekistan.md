# Uzbekistan — water in the combustion cycle (checked)

Status: DONE (checked). Hermes job 20261116-191648-we-survey-76-uzbekistan-water-in-combust (key we-survey-76-uzbekistan, profile we-research, OVH gpt-oss-120b throttled, no fallback) finished on 16 Nov 2026. The checker re-opened every source Hermes cited.

Prompt language: Russian (Hermes prompt). Report language: English.

Water is not treated as a fuel in this note. Hydrogen/"HHO" made from water by electrolysis is excluded.

## Verification (checker)

### Main finding

**Uzbekistan has one open-access paper on water injection in a diesel engine, and it is a calculation, not an engine test.** Musabekov, Ergashev, Daminov, Khushnaev, Kurbanov (Tashkent State Technical University and Tashkent State Transport University) and Kukharonok (Belarusian National Technical University, Minsk), IOP Conf. Ser.: Earth Environ. Sci. 1142, 012024 (2023), https://doi.org/10.1088/1755-1315/1142/1/012024 (CC BY 3.0). Quote: "As a result of mathematical modeling, it was found that at the nominal operating mode of the D-240 diesel engine, the introduction of 30% of water from the cycle supply of diesel fuel into the fuel-air mixture makes it possible to increase the effective power from 55.15 kW to 65.84 kW. The reduction in the specific effective consumption of diesel fuel is 45 gr/(kW/h). The thermal efficiency of the engine under study is 35.57%." The paper builds the indicator diagram "analytically using the Microsoft Excel application package"; the tables are calculated external speed characteristics (standard 55.15 kW at 2,200 rpm vs 65.84 kW with 30 % water), and the paper itself says the calculation "is approximate and does not take into account the loss of heat spent on heating the water". Those figures are predictions, not measurements. The paper's NOx figures come from its literature review (a boiler burner), not from its own D-240 work.

No Uzbek production or near-production vehicle, no product, no patent and no measured engine test of water injection or water-fuel emulsion were found in open sources. This is a negative result from limited searches (the Uzbek patent office database was not retrievable, Russian-language dissertations were not opened), not proof that none exists.

### Hermes errors corrected

- Hermes wrote "laboratory test bench" for the D-240 study. Wrong: the paper is analytical modeling in Excel; no bench test is reported.
- Hermes called it "peer-reviewed". It is a conference proceedings paper (ICECAE-2022); review level not verified, so the label was dropped.
- Hermes said "water-injection method: 30 % water blended into the diesel-fuel supply (fuel-water mixture)" and "organization TSUTU". The abstract says only "30% of water from the cycle supply of diesel fuel"; the exact delivery method is not stated. Affiliations are Tashkent State Technical University (named after Islam Karimov) and Tashkent State Transport University, plus a Belarusian coauthor. "TSUTU" dropped.
- Hermes put the bioethanol-heating paper (Khakimov et al., IOP 1231, 012017, 2023) under TIIAME. The opened PDF lists Tashkent State Transport University. It does not involve water injection and is excluded.
- Hermes listed OpenFOAM as a simulator "used by Uzbek groups" citing Jainakov and Kurbanaliev. Their dam-break paper (Andijan reservoir case) is by Kyrgyz authors (Osh), not an engine study; the venue "Procedia Engineering" was unsupported. Not counted as an Uzbek engine tool.

## Production or near-production road vehicles
NOT FOUND for Uzbekistan.

## Research, prototypes and supplier systems
Calculation only: Musabekov et al. 2023 (D-240 diesel, 30 % water, 55.15 -> 65.84 kW, thermal efficiency 35.57 %, specific fuel consumption -45 g/(kWh)); modeled, not measured, Excel-based, no emissions result of its own.

## University and institute work
Tashkent State Technical University and Tashkent State Transport University (same D-240 paper). No other measured work found.

## Industrial / power-plant, marine, aviation
NOT FOUND.

## Water-fuel emulsions and other cycles
NOT FOUND for Uzbek sources.

## Simulators and modeling tools
Simulators found: none after check. The D-240 paper used Microsoft Excel (commercial spreadsheet, not a simulator worth adding). OpenFOAM (open-source CFD, https://openfoam.com/) is only linked to Uzbekistan through a Kyrgyz-authored dam-break paper, so it is not added as a country find. Nothing was added or installed.
