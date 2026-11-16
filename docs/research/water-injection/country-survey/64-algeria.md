# Algeria — water in the combustion cycle (checked)

Status: DONE (checked). Hermes job 20261115-203413-we-survey-64-algeria-water-in-combustion (key we-survey-64-algeria, profile we-research, OVH gpt-oss-120b throttled, no fallback) ran 8:34–8:51 PM America/Los_Angeles 15 Nov 2026, rc 0, and produced a short draft built on **two** Algerian university-repository records (abstracts only). The checker opened both full texts from the university repositories, corrected what Hermes said about them, and added Algerian sources from its own search (French and English) on 15 Nov 2026, about 11:17–11:23 PM America/Los_Angeles. Only university repositories, publisher/journal metadata, OpenAlex and the HAL API were used. No piracy sites were used.

Prompt language: French (with an Arabic citation-honesty block). Report language: English.

Water is not treated as a fuel in this note. Hydrogen/“HHO” made from water by electrolysis is excluded (it is not water injection).

## Verification (checker)

### Main finding

**No Algerian production or near-production road vehicle with water injection, no Algerian water-injection product and no Algerian water-injection patent were found.** Algerian water-in-combustion work found is **calculation and modelling only**, and it is mostly about **steam/water injection in industrial gas turbines for hot Saharan conditions** (oil-and-gas and power use): an ENP Algiers 1978 final-year project proposed by SONATRACH, a 2008 CRNB/Boumerdes journal paper, a 2019 Béjaïa master thesis on the MS-5002C turbine, and a 2023 Annaba study of evaporative inlet cooling for SONATRACH MS 3002 turbines. The only Algerian piston-engine water-injection work found is a 2020 Béjaïa master thesis (calculation on a D-245 turbo-diesel: +8 % effective power at 6.8 kg/h water, modelled), plus a 2023 French–Algerian dual-fuel knock model that uses water injection (Fuel 358). No Algerian engine bench test with water was found.

### Sources opened and usable figures

- **Sellah A., Slimane A. (supervisor Hamtache B.), 2020**, master thesis “Amelioration des performances d'un moteur diesel suralimente par injection d'eau dans la tubulaire d'admission”, Université Abderrahmane Mira de Béjaïa, Faculté de Technologie, Génie mécanique (option Installation énergétique et turbomachine). Open record and full PDF: https://www.univ-bejaia.dz/xmlui/handle/123456789/14846
  - Engine data table (thesis): D-245, 4 cylinders, bore 110 mm, stroke 125 mm, 4.75 l, compression ratio 15.1, 77 kW at 2200 tr/min, 384 N·m, ge 220 g/kWh, boost 0.170 MPa.
  - Quote (conclusion): “on obtient une augmentation de la puissance effective de 8% en injectant un débit de (6.8 kg/h) … par conséquent on aura une croissance lente de la consommation spécifique effective du combustible de 0.3%.”
  - Quote: “l’injection d’eau semble augmente la quantité des imbrûlés par la formation du CO ce qui entraine une diminution du rendement indiquée de 1.6%” and “la température à la fin de la combustion diminue de (6%)”.
  - Quote (chosen point): “un débit optimal de 4 Kg/h d’eau, d’où la puissance est de 81 KW et la consommation spécifique est de 222.18 g/KWh.”
  - Calculation (“modèle de calcul”) only; no engine test. NOx effect stated only qualitatively (“a pour effet de diminuer les oxydes d’azote”), no NOx number.
- **Hazi A. (directed by Y. Boussard), 1978**, ENP final-year project “Interet de l'injection d'eau dans une turbine à gaz”, Université d'Alger / École Nationale Polytechnique, Département Mécanique, “Proposé par: SONATRACH”, “Promotion Janvier 1978”. Record and scanned PDF (113 pages): https://repository.enp.edu.dz/handle/123456789/4374 (title page and conclusion pages read by eye; the scan has no text layer).
  - Quote (p. 97, advantages): “l'injection d'eau augmente considérablement la puissance de la T.A.G.” and “pour que le groupe, fonctionnant sans injection d'eau, puisse fournir une puissance de 36800 KW, le débit d'air absorbé par le compresseur devrait être égal à 312 Kg/s contre 108,3 Kg/s dans le cas du cycle combiné.”
  - Quote (p. 98, drawbacks): “Le cycle combiné nécessite une installation de traitement de l'eau (distillation)” and “l'injection d'eau augmente la température des gaz d'échappement ce qui compromet la durée de vie du rotor.”
  - Quote (p. 99, conclusion): the comparison should be between two different turbines, one adapted to water injection, “particulièrement justifiée dans le cas d'une T.A.G. destinée à la production d'énergie de pointe.”
  - Calculation study, industrial/power gas turbine, not aviation.
- **Bouam A., Aïssani S., Kadi R. (2008)**, “Gas Turbine Performances Improvement using Steam Injection in the Combustion Chamber under Sahara Conditions”, *Oil & Gas Science and Technology – Rev. IFP* 63(2), 251–261, DOI 10.2516/ogst:2007076 (open access; also HAL hal-02001998). Affiliations: Nuclear Research Center of Birine (CRNB), Djelfa, and Faculty of Hydrocarbons and Chemistry, University M’Hamed Bougara Boumerdes. Abstract read via OpenAlex (journal PDF and HAL PDF blocked the checker).
  - Quote: “The objective of the present work is to improve the performances of gas turbine used under Sahara conditions by injecting suitable quantities of steam in the upstream of combustion chamber.” “Efficiency, however, is held constant when the ambient temperature increases from iso conditions to 50C.” “Data from the performance testing of an industrial gas turbine, computer model and theoretical study are used to check the validity of the proposed model.”
  - Power/efficiency gains: NOT FOUND in an opened source (full text not read).
- **Bouanani O., Bachioua N. (supervisor Hamtache B.), 2019**, master thesis “Amélioration des performances énergétiques de la turbine à gaz MS-5002C par injection de la vapeur d'eau en amont de la chambre de combustion”, Université de Béjaïa. Open record and full PDF: https://www.univ-bejaia.dz/xmlui/handle/123456789/14802
  - At 45 °C, calculated tables (V.1, V.2): without steam ηg = 26.46 %, PU = 23.433 MW, Qcc = 88.55 MW; with steam (raised from exhaust heat) ηg = 28.78 %, PU = 23.474 MW, Qcc = 81.550 MW.
  - Quote (conclusion): “nous recommandons à utiliser le cycle avec injection de la vapeur d’eau pendant les saisons chaudes.” Thermodynamic calculation only.
- **Mzad H., Bennour F. (2023)**, “Industrial gas turbine performance prediction and improvement – a case study”, *Energy Harvesting and Systems* 11(1), DOI 10.1515/ehs-2022-0094 (open). Badji Mokhtar University of Annaba. Related (water evaporated into compressor intake air, not into the combustor).
  - Quote: GE MS 3002 turbines of “SONATRACH’s pipeline transport of hydrocarbons activity”, “the number of these turbines exceeds 80 units”; “a mathematical model was implemented under Matlab R16”; “gains in terms of power and efficiency of the order of 1.361 MW and 3.4 % at a temperature of 47 °C.” Simulation only.
- **Sehili Y., Loubar K., Lounici M. S., Tarabet L., Cerdoun M., Lacroix C. (2023)**, “Development of knock prediction technique in dual fuel engines and its mitigation with direct water injection”, *Fuel* 358 Part B, 130297, DOI 10.1016/j.fuel.2023.130297 (paywalled; HAL hal-04804347 record, abstract via HAL API). Algerian co-authors at Université M’Hamed Bougara Boumerdes (LEMI) and École Militaire Polytechnique, Algiers; other authors at IMT Atlantique Nantes (France).
  - Quote: the knock model, “After validation of the model using experimental results, it is coupled with a CFD calculation model”; “Water injection technique is therefore used for this objective. Accurate prediction was useful for knock avoidance via water injection strategy.” Joint French–Algerian modelling; numbers NOT FOUND (abstract has none).

### Hermes sources checked

- Béjaïa 2020 thesis: exists, title, year and abstract quotes confirmed. Hermes said “laboratory test-bench”; the thesis is a calculation study with no engine test. Hermes said the quantitative figures were not available; the open PDF gives them (above). “Over-boosted” is a mistranslation of *suralimenté* (turbocharged).
- ENP 1978 study: exists, title, year and abstract quote confirmed (record text says “puissances”). Hermes labelled it “industrial / aviation-related” and “conceptual” with no numbers; the scan shows it is a SONATRACH-proposed industrial gas-turbine calculation (peaking power, combined/steam cycle) with numbers (36 800 kW, 312 vs 108.3 kg/s air flow). Author A. Hazi and director Y. Boussard were not named by Hermes.

### Hermes errors corrected

- “Laboratory test-bench” for the D-245 thesis → calculation only.
- “Quantitative figures are not provided” → +8 % power at 6.8 kg/h, +0.3 % specific consumption, −1.6 % indicated efficiency, −6 % end-of-combustion temperature (thesis conclusion).
- ENP 1978 “aviation-related” → industrial gas turbine, proposed by SONATRACH, peaking-power context.
- “The two sources above represent the only Algerian university-level work” → wrong: Bouam et al. 2008 (OGST), Béjaïa 2019 MS-5002C thesis, Annaba 2023, Boumerdes/EMP 2023 dual-fuel water-injection model also exist.
- “No Algerian … conference papers, or industrial reports on water-injection systems” → wrong for gas turbines; right that none was found for automotive engines.

### Excluded

- Water injection into oil reservoirs/wells (e.g., Hassi R’mel desalting/gas-lift theses): not combustion.
- Jijel 2017 master thesis “Analyse de cycles à combustion avec injection d'eau” (Lakrioui, Feniza; supervisor Laouir) is listed in a search result, but the repository returned errors to the checker; content NOT FOUND, not used.
- Search-engine summary crediting the 2023 Fuel paper to “Algeria’s Centre National de la Recherche Scientifique”: wrong (the CNRS unit is French, GEPEA UMR CNRS 6144, Nantes).
- Foreign water-injection and emulsion papers returned by searches (Malaysia, Pakistan, Portugal, India) with no Algerian author.

## Production or near-production road vehicles

None found for Algeria.

## Research, prototypes and supplier systems

- Béjaïa 2020: D-245 turbo-diesel intake water injection, calculation only (+8 % power at 6.8 kg/h; 4 kg/h “optimal” point 81 kW, 222.18 g/kWh).
- Boumerdes/EMP with IMT Atlantique 2023: dual-fuel knock prediction with direct water injection, model validated on experiments (numbers NOT FOUND).
- No Algerian supplier of water-injection or emulsion systems was found.

## Water-fuel emulsions and other cycles

- No Algerian water-in-diesel emulsion engine test was found.
- Steam/water-injected industrial gas turbines (the main Algerian thread): ENP/SONATRACH 1978; CRNB/Boumerdes 2008 (OGST, “Sahara conditions”, ISO to 50 °C); Béjaïa 2019 MS-5002C (26.46 % → 28.78 % at 45 °C, calculated). Related: Annaba 2023 evaporative inlet cooling of SONATRACH MS 3002 units (+1.361 MW, +3.4 % at 47 °C, simulated).
- No aviation, water–methanol or marine water-injection work from Algeria was found.

## Simulators and modeling tools

Simulators found: none added after check. Matlab (used by Annaba 2023) is a commercial general-purpose tool. The CRNB/Boumerdes 2008 “computer program” and the Béjaïa thesis calculation models have no public release or name in an opened source. The 2023 Fuel paper’s CFD software is NOT FOUND in the opened abstract. Hermes's “NOT FOUND” for simulators stands.

## Limits and open questions

- Bouam et al. 2008 full text (open access) could not be fetched (journal and HAL bot checks); only the abstract was read, so its gains are NOT FOUND here.
- The ENP 1978 scan has no text layer; only the title page and pp. 97–99 were read by eye.
- The 2023 Fuel paper is paywalled; HAL has only the record.
- Algerian master theses are spread over many university DSpace servers, several of which were unreachable (e.g., Jijel); unpublished bench work may exist.
- The Algerian patent office (INAPI) register was not searched directly; web searches found no Algerian water-injection patent.
