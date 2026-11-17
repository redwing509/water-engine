# North Macedonia — water in the combustion cycle (checked)

Status: DONE (checked). Hermes job 20261116-152145-we-survey-72-north-macedonia-water-in-co (key we-survey-72-north-macedonia-r2, profile we-research, OVH gpt-oss-120b throttled, no fallback) finished rc 0 on 16 Nov 2026. Its draft was all NOT FOUND with zero sources opened. The checker ran its own searches and opened the sources below.

Prompt language: Macedonian (Hermes prompt). Report language: English.

Water is not treated as a fuel in this note. Hydrogen/"HHO" made from water by electrolysis is excluded.

## Verification (checker)

### Main finding

**NOT FOUND for road vehicles: no North Macedonian production or near-production road vehicle with water injection, no North Macedonian water-injection product or patent, and no university or institute test of water injection or a water-fuel emulsion in an engine was found in open sources.** This is a negative result from the checker's searches, not proof that none exists.

**One real North Macedonian water-injection application was found, in power generation (not road vehicles):** TE-TO AD Skopje fitted a MeeFog inlet-fogging system to its gas turbine, put into operation at the beginning of September 2023. It is a power-augmentation system using a foreign (Mee Industries) product; it is not a NOx-control or vehicle system.

### Sources opened

- **TE-TO AD Skopje, "Project for installation of fogging system on Gas Turbine - MeeFog"**, https://te-to.com.mk/project-for-installation-of-fogging-system-on-gas-turbine-meefog/ (opened, HTTP 200, full page).
  - Quote: "Fogging system is a gas turbine power augmentation method that consists of injecting atomized water droplets (fog) directly into the gas turbine compressor to improve output and heat rate".
  - Quote: "In 2021, TE-TO AD Skopje launched an initiative to implement a power augmentation systems Fogging system on the gas turbine, which in the summer months would contribute to increasing the power of the turbine by about 13 MW".
  - Quote: "The system was put into operation at the beginning of September 2023 ... an additional 600 MWh of energy was produced in the most unfavorable months. In 2024, only in the summer months, i.e. June, July and August, the power plant with the integrated MeeFog system produced an additional 4000 MWh of electricity."
  - Also lists "Reduced NOx emissions (only for inlet fogging)" as a benefit; no NOx number is given. The page states plant output of 205 to 239 MW depending on ambient conditions, and a 2-year estimated payback.
  - Equipment listed: demineralized-water feed pump, pump skid with filters and solenoid valves, piping and sprinklers placed in the air stream after the fine filters, PLC. Water quality requirement: below 1.5 mS/cm.
- **LinkedIn post by John Mee (Mee Industries), 2023**, https://www.linkedin.com/posts/john-mee-184a94b_thank-you-sasho-activity-7105235948656893952-ZMf7 (opened, HTTP 200). Quote: "we have successfully commissioned the fogging power augmentation system on our GT13E2 gas turbine ... we are proud to have achieved 10 MW power boost on 11,8 deg wet-bulb temperature depression." This is a supplier's own post, not an independent measurement. It names the turbine model (GT13E2) and the supplier; the TE-TO page itself names neither.
- **Manev N., doctoral dissertation, "Моделирање на управувањето на дизел-мотор со внатрешно согорување за намалување на штетната издувна емисија", Faculty of Mechanical Engineering, Ss. Cyril and Methodius University, Skopje, 2023** (defence 17.11.2023), https://www.mf.ukim.edu.mk/sites/default/files/PhD_NM.pdf (open PDF, full text downloaded and text-searched). Diesel engine control and virtual test cell in MATLAB/Simulink with a neural-network emission model. Searched for water injection, water emulsion and "вбризгување вода": **no match**; "water" appears only in a symbols table and a wastewater reference. NOx-reduction discussion covers exhaust gas recirculation (EGR) only. **Adjacent work, no water injection.**
- **Manev N., Jovchevski I., Dimitrovski D., Nikolov E., "Implications for the environmental-engineering compromise as a result of power and economy tuning a diesel engine", ETIMA (Goce Delčev University, Štip)**, https://js.ugd.edu.mk/index.php/etima/en/article/view/6450 (record page opened, HTTP 200; the abstract does not mention water). Quote: "The POWER/PERFORMANCE optimization led to a 36% increase in engine power (78 to 106 kW)", with increased PM and NOx. **Engine-tuning paper; no water.**
- **Manev N. et al., "Economy and power tuning an IC engine for lower CO2 footprint", Mechanical Engineering – Scientific Journal**, https://mesj.ukim.edu.mk/journals/en/article/view/24 (record page opened). The abstract shown there is about Lattice Boltzmann free-surface flow, not engines or water injection; the page record looks mismatched to the title. Not used.

### Hermes errors corrected

- Hermes's Pass 1 lists "No sources opened", and its claimed systematic search of repositories, patents and official publications "from 1926-2026" is not backed by any source. NOT FOUND stands only as "not found by the checker's searches".
- Hermes missed the real TE-TO Skopje MeeFog gas-turbine fogging project (section below).
- Hermes's "Simulators" NOT FOUND is accepted (see below).

## Production or near-production road vehicles
NOT FOUND for North Macedonia.

## Research, prototypes and supplier systems
NOT FOUND for engines. No Skopje, Bitola, Štip or Ohrid study of water injection in engines was found. The Skopje mechanical faculty's visible engine-emissions work (Manev, Dimitrovski, Jovchevski) is calibration, tuning and EGR.

## Industrial / power-plant use
FOUND (one item): TE-TO AD Skopje, gas-turbine inlet fogging (MeeFog), commissioned early September 2023; planned gain "about 13 MW" in summer; plant reports about 600 MWh extra in Sept 2023 and 4000 MWh extra in June–August 2024 (operator's figures); Mee Industries' post quotes 10 MW at 11.8 degrees wet-bulb depression. Context only: the technology and patents are foreign.

## Water-fuel emulsions and other cycles
NOT FOUND for North Macedonian work.

## Marine and aviation
NOT FOUND.

## Simulators and modeling tools
Simulators found: none after check. Hermes reported NOT FOUND. The only modeling tool linked to North Macedonia is the Manev thesis's MATLAB/Simulink virtual engine test cell (MATLAB is commercial, and no download of the thesis model was seen). A "Not added" note went into the candidate list, and nothing was installed.
