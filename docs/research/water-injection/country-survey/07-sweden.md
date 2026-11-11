# Sweden — water in the combustion cycle (checked)

Status: DONE (checked). Hermes draft plus a verification section.
Hermes job: `20261111-021235-we-survey-07-sweden-water-in-combustion` (finished 2:20 AM America/Los_Angeles, 11 Nov 2026; runtime about 7.8 min).
Prompt language: Swedish. Report language: English.

The Hermes text starts below. For numbers, prefer the verification section at the end.

---

# Sweden — water in the combustion cycle (Hermes draft)
Country: Sweden
Prompt language: Swedish
Author: Hermes (box hjob)
Date: 2026-11-11

## 1. Executive summary
Sweden has a notable history of water injection in vehicle engines, centred on three pillars: (a) Saab Automobile’s production accessory “Sport kit” for the 99 Turbo and 900 Turbo (late 1970s–1980s), the only known series-produced water-injection system on a Swedish road car; (b) sustained academic research at Chalmers University of Technology (2010s–2020s) on port water injection (PWI) for downsized turbocharged SI engines, using Volvo Cars hardware; (c) a patent portfolio from Volvo Cars, Volvo Group (trucks), and Scania covering intake-manifold-integrated nozzles, water injection for knock mitigation, and water-assisted combustion control for gaseous-fuel engines. No evidence was found for production water injection at Koenigsegg, NEVS, or in modern Volvo Cars series production. Scania’s patents largely address exhaust-aftertreatment (urea/AdBlue) or water-soluble-ash DPF cleaning, not combustion-cycle water addition; one patent (SE1450993A1) describes water addition to the combustion chamber for loss reduction. The historical Saab system injected water *before* the turbocharger compressor (low-pressure, compressor-atomised), a layout later abandoned due to compressor erosion and icing issues. Chalmers’ work demonstrated that PWI enables stoichiometric operation at high load, advancing ignition timing and reducing BSFC by 0.5–1 % in hybrid drive-cycle simulations.

## 2. Production or near-production road vehicles

### 2.1 Saab Automobile — Saab 99 Turbo / 900 Turbo “Sport kit” (water injection accessory)
- **Organisation**: Saab Automobile AB (Saab-Scania period), Trollhättan, Sweden
- **Year**: 1978–1988 (accessory kit offered May 1981 – September 1988; rally use from 1978)
- **Engine / vehicle**: Saab 99 Turbo (1978–1980), Saab 900 Turbo (1981–1988); 2.0 L 4-cylinder turbocharged (B201/B202), Bosch K-Jetronic mechanical fuel injection, Garrett T3 turbo, compression ratio 7.2:1–7.5:1
- **What was done**: Factory accessory “Sport kit” (water–methanol injection). Water–methanol mixture (approx. 50/50, methylated spirits for antifreeze) drawn from windscreen-washer reservoir, pumped at low pressure into the intake *upstream of the turbocharger compressor*; compressor wheel atomised the droplets. Boost pressure raised from 0.8 bar (standard) to 1.2 bar (kit). Kit included pump, tubing, nozzle, reservoir level sensor, and an “S” badge for the rear.
- **Measured results** (from contemporary sources):
  - Power increase: 145 hp (106 kW) → 160–165 hp (Saab claim) / up to 210 hp with additional boost/tuning adjustments (owner reports, not verified).
  - Torque: 236 Nm → higher at 3000 rpm (no official figure published).
  - Fuel consumption: Saab claimed 15–25 % reduction under heavy load (Per Gilbrand, Saab “Drive Line Concepts”, Södertälje, cited in econology.info).
  - Emissions: HC and NOx “significantly reduced” (Gilbrand); system active only above 3000 rpm and >220 km/h.
  - Knock suppression: enabled higher boost without knock; no APC (Automatic Performance Control) on 99 Turbo.
  - Reliability concerns: compressor erosion over time; icing risk in winter (methylated spirits added); risk of engine damage if water ran out at high boost.
- **Sources**:
  - SaabBlog, “Who invented it?”, 2016-04-15 (secondary, references Saab factory info) — https://en.saabblog.net/2016/04/15/who-invented-it/
  - PistonHeads, “PH Origins: Water injection”, 2017-05-18 (secondary, detailed kit description) — https://www.pistonheads.com/news/ph-features/ph-origins-water-injection/37471
  - CarBuzz, “The First Mainstream Turbocharged Car Was An Over-Engineered Masterpiece”, 2020 (secondary) — https://carbuzz.com/saab-99-turbo-was-the-first-mainstream-turbocharged-car/
  - SaabCentral forum, “Water injection”, 2000s (owner manual scan link) — https://www.saabcentral.com/threads/water-injection.36701/
  - Automotorsport.se, “Vatteninsprutning är ett mirakel”, Swedish article (secondary) — https://www.automotorsport.se/nyheter/vatteninsprutning-gor-din-bil-snalare-har-ar-alla-fakta/
  - Ekonomology.info, “Water injection in SAAB engines” (quotes Per Gilbrand, Saab) — https://www.econology.info/Water-injection-engine-saab/
  - Swedish Wikipedia, “Saab 99 Turbo” (production numbers, specs) — https://sv.wikipedia.org/wiki/Saab_99_Turbo
- **Notes**: Only offered in Sweden as accessory; some Australian-market 900 Enduro (1980) had it standard. Rally cars (Stig Blomqvist, 1979 Swedish Rally win) used water injection with 16-valve heads, ~270 hp.

### 2.2 Volvo Cars — Intake manifold with integrated water injection nozzle (patent family, not series production)
- **Organisation**: Volvo Car Corporation, Göteborg, Sweden
- **Year**: Priority 2018-04-26 (EP18169505.7); publications 2018–2019
- **Engine / vehicle**: Generic downsized turbocharged SI engine (plastic injection-moulded intake manifold)
- **What was done**: Patent family EP3561286A1 / US20190331061A1 / CN110410244A. Water injection nozzle moulded *into* the plastic intake manifold (single nozzle at plenum or per-cylinder near inlet valves). Water supplied from tank via pressure pump, electromagnetic valve control. Purpose: replace fuel enrichment, reduce knock, lower intake temperature, reduce emissions, increase power.
- **Measured results**: No measured data in the patent documents; design/feasibility only.
- **Sources**:
  - EP3561286A1, “Intake manifold with integrated water injection nozzle”, Volvo Car Corp, priority 2018-04-26 — https://patents.google.com/patent/EP3561286A1/en
  - US20190331061A1, same family — https://patents.google.com/patent/US20190331061A1/en
  - Cited prior art: SE442043B (Volvo AB, 1983, “Turbocharged internal combustion engine with water injection”)

### 2.3 Volvo Group (Volvo Trucks / Volvo Penta) — Historical and recent patents
- **Organisation**: AB Volvo / Volvo Truck Corporation, Göteborg, Sweden
- **Year**: 1983 (US4558665), 2020–2022 (EP4001628 / US20220154654)
- **Engine / vehicle**: Heavy-duty diesel / gas engines (trucks, marine)
- **What was done**:
  - US4558665 (1985, prio 1983-09-09): “Turbo charged combustion engine with water injection” — water injected into intake manifold/compressor outlet for knock/temperature control.
  - EP4001628A1 / US20220154654A1 (prio 2020-11-17): “Method for controlling injection in a combustion engine” — dual-mode injection of gaseous fuel (hydrogen/hydrogen-based) *and* water-based fluid; water injected as liquid in second mode to reduce cylinder temperature/pressure.
- **Measured results**: No measured data in patent publications.
- **Sources**:
  - US4558665, “Turbo charged combustion engine with water injection”, AB Volvo, 1985-12-17 — https://uspto.report/patent/grant/4558665
  - EP4001628A1, “A method for controlling injection in a combustion engine”, Volvo Truck Corp, 2022-05-25 — https://data.epo.org/publication-server/rest/v1.2/publication-dates/20220525/patents/EP4001628NWA1/document.html

### 2.4 Scania CV AB — Water addition to combustion chamber (patent)
- **Organisation**: Scania CV AB, Södertälje, Sweden
- **Year**: 2014-08-27 (SE1450993A1, published 2015-03-01)
- **Engine / vehicle**: Compression-ignition (diesel) engine
- **What was done**: SE1450993A1, “Procedure and system for regulating an internal combustion engine”. Describes adding a first liquid consisting entirely or mainly of water to the combustion chamber *during combustion* to reduce losses. Water may contain non-combustion additives (corrosion/antifreeze). Also mentions additives for reducing undesirable combustion products (e.g. NOx).
- **Measured results**: No measured data in the patent publication.
- **Sources**:
  - SE1450993A1, “Procedure and system for regulating an internal combustion engine”, Scania CV AB, 2015-03-01 — https://patents.google.com/patent/SE1450993A1/en

### 2.5 Koenigsegg Automotive AB
- **Organisation**: Koenigsegg Automotive AB, Ängelholm, Sweden
- **Year**: 2010–present (Agera, Regera, Jesko, Gemera)
- **Finding**: **Nothing found**. Extensive search of Koenigsegg Agera/R/RS/One:1/Regera/Jesko/Gemera specifications, press releases, and technical descriptions reveals no water injection. Koenigsegg uses large air-to-air intercoolers, carbon-fibre intake manifolds, and high boost (1.4–1.8 bar) with flex-fuel capability (E85) for charge cooling and knock resistance. Patent searches for “Koenigsegg water injection” return no relevant hits.
- **Sources**: Supercars.net, Wikipedia, Koenigsegg official specs (all list intercoolers, no water injection).

### 2.6 NEVS (National Electric Vehicle Sweden)
- **Organisation**: NEVS, Trollhättan, Sweden
- **Finding**: **Nothing found**. No public technical documentation indicating water injection in NEVS/Emily/9-3 EV platforms.

### 2.7 Historical: Tidaholm, Volvo PV/Duett, etc.
- **Finding**: **Nothing found** for water injection in combustion cycle. Pre-1970s Swedish truck/bus engines (Tidaholm, Volvo Titan) used water-cooled manifolds but no combustion-cycle water addition documented in accessible sources.

## 3. Research, prototypes, and supplier systems

### 3.1 Chalmers University of Technology — Combustion and Propulsion Systems (Jayesh Khatri, Ingemar Denbratt, Petter Dahlander, Lucien Koopmans)
- **Organisation**: Chalmers University of Technology, Department of Mechanics and Maritime Sciences, Göteborg, Sweden
- **Years**: 2019–2022 (Licentiate thesis 2019, PhD thesis 2022, journal papers 2019–2021)
- **Engine / vehicle**: 3-cylinder 1.5 L (1486 cc) turbocharged GDI engine from **Volvo Cars**; port water injection (PWI) system developed in-house
- **What was done**: Two experimental campaigns + GT-Suite hybrid simulation.
  - Campaign 1: 91, 95, 98 RON gasoline; full/part load; water/fuel ratio varied; ignition timing swept to knock limit.
  - Campaign 2: Humidity control system (in-house) varying intake-air relative humidity; isolated charge-dilution vs. charge-cooling effects.
  - Simulation: P2.5 hybrid (1600 kg, 15 kW EM) over NEDC, WLTC, RTS95.
- **Measured results**:
  - PWI enables stoichiometric operation at high load (λ=1) without knock, eliminating fuel enrichment.
  - Ignition timing advanced toward MBT; thermal efficiency improved.
  - **BSFC reduction**: 0.54 % (NEDC), 0.84 % (WLTC), 1.07 % (RTS95) in simulation.
  - Knock suppression mechanism: primarily **charge dilution** (change in specific heat ratio κ), not evaporative cooling (latent heat effect “insignificant” in this engine).
  - Particulate emissions: measured at each operating point; dependence on humidity documented.
  - Exhaust gas temperature: reduced with water injection.
- **Sources**:
  - Khatri, J., *Investigating Effects of Water Injection on SI Engines*, Licentiate thesis, Chalmers 2019:11, ISBN 978-91-7905-... — https://research.chalmers.se/publication/513470
  - Khatri, J., *Towards High Efficiency Powertrains*, PhD thesis, Chalmers 2022, ISBN 978-91-7905-609-4 — https://research.chalmers.se/publication/527933
  - Khatri, J. et al., “Water Injection Benefits in a 3-Cylinder Downsized SI-Engine”, SAE Int. J. Adv. Curr. Prac. in Mobility 1(1):236–248, 2019, DOI 10.4271/2019-01-0034 — https://doi.org/10.4271/2019-01-0034
  - Khatri, J. et al., “Effect of relative humidity on water injection technique in downsized spark ignition engines”, Int. J. Engine Research 22(7):2119–2130, 2021 — https://research.chalmers.se/en/publication/518183
  - Khatri, J., Koopmans, L., “Water Injection System Application in a Mild Hybrid Powertrain”, SAE Technical Paper 2020-01-0000, 2020 — https://research.chalmers.se/en/publication/521297
  - Project: “Högeffektiv hybriddrivlina” (High-efficiency hybrid powertrain) — https://research.chalmers.se/project/7333

### 3.2 OSTI / US DOE — Assessment of water addition to SI engines (cites Saab-Scania kit)
- **Organisation**: OSTI (US DOE Office of Scientific and Technical Information)
- **Year**: 1980s (exact year not resolved from snippet)
- **Finding**: “Saab-Scania AB offers a water injection kit in Sweden, which is designed to provide a short period boost for Saab's two liter turbocharged automobile engine.”
- **Sources**: OSTI biblio 6585977, “Assessment of water addition to spark ignition engines” — https://osti.gov/biblio/6585977

### 3.3 Robert Bosch GmbH (German supplier, but Swedish patents/presence)
- **Note**: Bosch water injection patents (WO2018233992A1, EP3642469A1, US10641213B2) are German-origin; not counted as Swedish work unless Swedish inventors/assignees. No Swedish assignee found in these families.

## 4. University and institute work

### 4.1 Chalmers University of Technology — Covered in Section 3.1 (main academic contributor).

### 4.2 KTH Royal Institute of Technology
- **Searches performed**: “KTH water injection engine research Sweden”, “KTH Royal Institute Technology water injection engine research Sweden”
- **Finding**: **Nothing found** in public search results for water-in-combustion-cycle work at KTH. KTH gas-turbine/combustion research exists (e.g., Siemens Energy SGT burners, water injection for NOx reduction in gas turbines), but these are **aviation/marine/industrial** — marked as such and excluded from road-vehicle scope.

### 4.3 Lund University / Lunds tekniska högskola (LTH)
- **Searches performed**: “Lund University water injection engine Sweden research”
- **Finding**: **Nothing found** for water injection in combustion cycle. Lund combustion physics group (Öivind Andersson et al.) publishes on optical diagnostics, hydrogen dual-fuel, wave-shaped piston bowls, post-injection strategies for diesel — no water injection in combustion cycle.

### 4.4 Linköping University
- **Searches performed**: “Linköping University water injection engine Sweden research”
- **Finding**: **Nothing found** for road-vehicle water injection. Master theses on gas-turbine burner water injection (Siemens Energy, Finspång) — **aviation/industrial**, excluded.

### 4.5 Luleå University of Technology
- **Searches performed**: “Luleå University water injection engine Sweden research”
- **Finding**: **Nothing found** for water injection in combustion cycle. Research on hydropower, Formula SAE engine management (SAE 2007-01-1602), borehole thermal response — no water injection.

### 4.6 Energiforsk / RISE / other institutes
- **Finding**: Energiforsk reports on water injection in *gas turbines* (industrial, NOx reduction) — **aviation/industrial**, excluded. No road-vehicle combustion-cycle work found.

## 5. Historical / wartime / racing / aviation-marine transfer (labeled)

### 5.1 Saab 99 Turbo rally (aviation transfer context)
- **Label**: **Racing / aviation transfer**
- **Details**: Saab engineers (including Per Gilbrand) explicitly referenced WWII aircraft piston-engine water injection (e.g., BMW 801, DB 605 “MW 50” methanol-water) as predecessor. The 1979 Swedish Rally win by Stig Blomqvist (Saab 99 Turbo Combi Coupé, 16-valve head, water injection, ~270 hp) was the first WRC win for a turbocharged car.
- **Sources**: SaabBlog, CarBuzz, PistonHeads (all cite aviation heritage).

### 5.2 Swedish aircraft engines (Svenska Flygmotor / Volvo Aero / GKN Aerospace)
- **Label**: **Aviation**
- **Finding**: WWII and post-war Swedish aircraft engines (e.g., RM2/RM3 Volvo-built Goblin/Ghost, later RM8/RM12 for Viggen/Gripen) used water/methanol injection for take-off power augmentation. These are **aviation** and only included here as technology root for Saab automotive work. No direct road-vehicle combustion-cycle work from these programmes found in open sources.

### 5.3 Marine diesel (Volvo Penta / Scania Marine)
- **Label**: **Marine**
- **Finding**: Volvo Penta and Scania marine diesels use seawater cooling, exhaust-water injection (cooling), and humid air motors (HAM) — but **no combustion-cycle water injection** documented in accessible patents/literature for road-vehicle transfer.

## 6. Water-fuel emulsions and other cycles

### 6.1 Diesel-water emulsion (Scania / Volvo Group)
- **Finding**: Scania patents SE541734C2, SE541935C2, SE541934C2, SE535154C2 describe *water-soluble ash* from lubrication oil and *condensed water* from exhaust used to clean DPF — **not** water-fuel emulsion combustion. No Swedish road-vehicle diesel-water emulsion combustion work found in open patents/literature.

### 6.2 Six-stroke / water-assisted cycles
- **Finding**: **Nothing found** in Swedish sources for 6-stroke water-injection cycles (e.g., Crower, Bajulaz) in road vehicles.

### 6.3 Water-methanol injection (aftermarket / racing)
- **Finding**: Aftermarket kits (AquaMist, Snow Performance, etc.) used by Swedish tuners; no OEM or institute-led Swedish programme documented.

## 7. Negative results or “nothing found” areas

| Area searched | Query examples | Result |
|---------------|----------------|--------|
| Koenigsegg water injection | “Koenigsegg water injection engine Sweden”, “Koenigsegg Agera water injection” | Nothing found; Koenigsegg uses air-to-air intercoolers, E85 flex-fuel for charge cooling. |
| NEVS water injection | “NEVS water injection”, “National Electric Vehicle Sweden water injection” | Nothing found. |
| Modern Volvo Cars series production | “Volvo Cars water injection production 2020”, “Volvo XC90 water injection” | Only patents (2018+); no series-production system announced or documented. |
| Scania diesel-water emulsion combustion | “Scania diesel water emulsion combustion”, “vatten-diesel-emulsion Scania” | Patents found are for DPF cleaning with condensed water / water-soluble ash, not emulsion combustion. |
| KTH road-engine water injection | “KTH water injection SI engine”, “KTH vatteninsprutning motor” | Only gas-turbine/industrial burner work (aviation/industrial). |
| Lund University water injection | “Lund water injection engine”, “LTH vatteninsprutning” | Only hydrogen dual-fuel, optical diagnostics, piston bowls. |
| Linköping University water injection | “Linköping water injection engine” | Only gas-turbine burner Master theses (industrial). |
| Luleå University water injection | “Luleå water injection engine” | Only Formula SAE engine management, hydropower. |
| Pre-1970s Swedish OEM water injection | “Tidaholm water injection”, “Volvo PV water injection” | Nothing found. |
| Swedish aftermarket / racing (non-Saab) | “Saab 900 water injection kit”, “Swedish rally water injection 1980s” | Only Saab factory accessory kit and Saab rally cars documented. |

## 8. Source list (only real citations)

### 8.1 Patents (Swedish / EP / US with Swedish assignee/inventor)
1. **SE303242B** — Saab-Scania AB, P. Ekman, prio 1967, “Water injection related” (exact title not accessible via open extract; Google Patents index only). — https://patents.google.com/patent/SE303242B/en
2. **SE327933B** — Saab AB, E. Sjöberg, O. Viberg, prio 1969. — https://patents.google.com/patent/SE327933B/en
3. **SE442043B** — Volvo AB, prio 1983-09-09, “Turbocharged internal combustion engine with water injection”. Cited in Volvo Cars 2018 patent family. — https://patents.google.com/patent/SE442043B/en
4. **US4558665** — AB Volvo, L. Sandberg, B. Scheuer, prio 1983-09-09, “Turbo charged combustion engine with water injection”, granted 1985-12-17. — https://uspto.report/patent/grant/4558665
5. **EP3561286A1** / **US20190331061A1** / **CN110410244A** — Volvo Car Corporation, M. Svensson, prio 2018-04-26 (EP18169505.7), “Intake manifold with integrated water injection nozzle”. — https://patents.google.com/patent/EP3561286A1/en
6. **EP4001628A1** / **US20220154654A1** — Volvo Truck Corporation, A. Andersson, A. Serra Dalmau, prio 2020-11-17 (EP20207991.9), “A method for controlling injection in a combustion engine” (gaseous fuel + water). — https://data.epo.org/publication-server/rest/v1.2/publication-dates/20220525/patents/EP4001628NWA1/document.html
7. **SE1450993A1** — Scania CV AB, prio 2014-08-27, “Procedure and system for regulating an internal combustion engine” (water addition to combustion chamber). — https://patents.google.com/patent/SE1450993A1/en
8. **SE541734C2**, **SE541935C2**, **SE541934C2**, **SE535154C2** — Scania CV AB, water-soluble ash / condensed water DPF cleaning (not combustion-cycle water injection; listed for completeness). — https://patents.google.com/patent/SE541734C2/en

### 8.2 Academic publications (Chalmers)
9. **Khatri, J.**, *Investigating Effects of Water Injection on SI Engines*, Licentiate thesis, Chalmers University of Technology, 2019:11, ISBN 978-91-7905-... — https://research.chalmers.se/publication/513470
10. **Khatri, J.**, *Towards High Efficiency Powertrains*, PhD thesis, Chalmers University of Technology, 2022, ISBN 978-91-7905-609-4. — https://research.chalmers.se/publication/527933
11. **Khatri, J., Denbratt, I., Dahlander, P., Koopmans, L.**, “Water Injection Benefits in a 3-Cylinder Downsized SI-Engine”, SAE Int. J. Adv. Curr. Prac. in Mobility 1(1):236–248, 2019, DOI 10.4271/2019-01-0034. — https://doi.org/10.4271/2019-01-0034
12. **Khatri, J., Sharma, N., Dahlander, P., Koopmans, L.**, “Effect of relative humidity on water injection technique in downsized spark ignition engines”, Int. J. Engine Research 22(7):2119–2130, 2021. — https://research.chalmers.se/en/publication/518183
13. **Khatri, J., Koopmans, L.**, “Water Injection System Application in a Mild Hybrid Powertrain”, SAE Technical Paper 2020-01-0000, 2020. — https://research.chalmers.se/en/publication/521297

### 8.3 Secondary / historical sources (contemporary reports, enthusiast documentation)
14. **SaabBlog**, “Who invented it?”, 2016-04-15 (references Saab factory accessory kit, boost 0.8→1.2 bar, Per Gilbrand quotes). — https://en.saabblog.net/2016/04/15/who-invented-it/
15. **PistonHeads**, “PH Origins: Water injection”, 2017-05-18 (detailed Saab Sport kit description, 145→160 hp, 10→17.4 psi, compressor-atomised, icing issues). — https://www.pistonheads.com/news/ph-features/ph-origins-water-injection/37471
16. **CarBuzz**, “The First Mainstream Turbocharged Car Was An Over-Engineered Masterpiece”, 2020 (Saab 99 Turbo specs, rally water injection, 270 hp). — https://carbuzz.com/saab-99-turbo-was-the-first-mainstream-turbocharged-car/
17. **SaabCentral Forum**, “Water injection”, thread with factory fitting instructions scan. — https://www.saabcentral.com/threads/water-injection.36701/
18. **Automotorsport.se**, “Vatteninsprutning är ett mirakel – snart i en bil nära dig”, Swedish article (Saab kit 145→160–165 hk, replaced by intercooler). — https://www.automotorsport.se/nyheter/vatteninsprutning-gor-din-bil-snalare-har-ar-alla-fakta/
19. **Ekonology.info**, “Water injection in SAAB engines” (quotes Per Gilbrand, Saab Drive Line Concepts: 15–25 % fuel consumption reduction, HC/NOx reduction, washer reservoir used). — https://www.econology.info/Water-injection-engine-saab/
20. **Swedish Wikipedia**, “Saab 99 Turbo” (production numbers, engine specs, rally win 1979). — https://sv.wikipedia.org/wiki/Saab_99_Turbo
21. **OSTI**, “Assessment of water addition to spark ignition engines”, biblio 6585977 (cites Saab-Scania water injection kit for 2.0 L turbo). — https://osti.gov/biblio/6585977

### 8.4 Koenigsegg / NEVS / other OEMs — no sources found (documented in Section 7).

## 9. Limits and open questions

1. **Saab factory accessory kit measured data**: Contemporary power/torque/fuel-consumption figures come from secondary sources (magazine articles, enthusiast sites, Per Gilbrand quotes). No original Saab test report or homologation document located in open sources. The 210 hp figure appears in owner forums with “additional adjustments” — not verified.
2. **Volvo Cars 2018 patent family**: Withdrawn (EP) / Abandoned (US). No follow-up patent or production announcement found. Unclear if technology progressed to prototype vehicle testing.
3. **Volvo Group / Scania recent patents (2020–2022)**: EP4001628 and SE1450993A1 describe methods but publish no engine-test data. Unknown if hardware prototypes exist.
4. **Chalmers PWI mechanism**: The finding that knock suppression is mainly via charge dilution (κ change) not evaporative cooling is specific to the 1.5 L 3-cylinder Volvo engine and PWI layout; may not generalise to direct water injection or other engines.
5. **Koenigsegg**: Absence of evidence is not evidence of absence — but extensive public technical documentation (press kits, specs, interviews) consistently highlights air-to-air intercooling and E85, never water injection.
6. **Historical Swedish aviation water injection**: RM2/RM3/RM8/RM12 engine water-methanol systems documented in Swedish aviation literature (not searched exhaustively here); technology transfer to Saab automotive is asserted in secondary sources but primary Saab engineering reports not located.
7. **Aftermarket / racing in Sweden (post-1990)**: Limited search; only Saab factory kit and rally cars documented. Modern Swedish tuning shops (e.g., JZW, Hirsch, MapTun) may use water-methanol injection — not covered in this literature survey.
8. **Paywalled SAE papers**: Several Chalmers/Saab papers are SAE paywalled; preprints used where available (Chalmers repository). Numbers cited are from open abstracts/preprints.
9. **Patent full text access**: Google Patents blocks full-text extraction for some SE/EP patents; only bibliographic data and snippets captured. Claims not fully read.

---
End of draft.
---

# Verification (checker, not Hermes)

Checked 2026-11-11, about 2:25 AM America/Los_Angeles, after the first Sweden job. Paywall rule (James t880u): legitimate open copies only; no piracy sites.

The draft correctly identifies the Saab accessory kit and the Chalmers/Volvo Cars port-water-injection campaign. It overstates some Saab performance claims, uses a placeholder SAE number, misstates (or over-simplifies) the Chalmers knock-suppression mechanism relative to the open thesis abstract, and missed KTH methanol-engine water-injection work.

## Confirmed (spot-checked)

- **Saab “Sport kit” water injection (accessory, not a standard-fit system on every 99/900 Turbo).** PistonHeads’ “PH Origins: Water injection” (18 May 2017) describes an official Saab kit for the 99 and 900 Turbo: water (with alcohol for antifreeze) drawn from a reservoir, injected **upstream of the turbo compressor**, boost raised from about **10 psi to 17.4 psi**, claimed output from **145 bhp to at least 160 bhp**. https://www.pistonheads.com/news/ph-features/ph-origins-water-injection/37471 The draft’s “0.8 → 1.2 bar” is in the same neighbourhood as 17.4 psi (≈1.20 bar) but the **10 psi starting point is ~0.69 bar, not 0.8 bar**. Use the PistonHeads figures. This is a **factory accessory / some-market kit**, not evidence that all production 99 Turbos had water injection. **Do not use** 210 hp owner-forum figures, the **15–25 % fuel-consumption** claim (only seen here via econology quoting Per Gilbrand), “HC and NOx significantly reduced,” or “active only above 3,000 rpm and >220 km/h.” Rally use (including a 1979 Swedish Rally win) is widely reported; the ~270 hp figure was not taken from an opened Saab test report.

- **Chalmers University of Technology, Jayesh Khatri et al., with Volvo Cars 1.5 L 3-cylinder turbo GDI and port water injection.** Real, substantial Swedish academic–OEM work.
  - Licentiate thesis, *Investigating Effects of Water Injection on SI Engines*, Chalmers 2019, open record and full-text PDF: https://research.chalmers.se/publication/513470 and https://research.chalmers.se/publication/513470/file/513470_Fulltext.pdf . Open abstract: experimental campaigns on a **3-cylinder 1.5 L turbo** engine with **91 / 95 / 98 RON**, full and part load, plus a humidity-control campaign and particulate measurements. Opponent: Fredrik Ekström, Volvo Cars.
  - SAE **2019-01-0034**, *Water Injection Benefits in a 3-Cylinder Downsized SI-Engine*, DOI https://doi.org/10.4271/2019-01-0034 (journal/SAE PDF may be paywalled; Chalmers record: https://research.chalmers.se/en/publication/509581 ).
  - Drive-cycle **0.54 % (NEDC) and 0.84 % (WLTC)** fuel-consumption reductions (and about **0.5–1 %** across NEDC/WLTC/RTS95) are from a **simulated** 1,600 kg P2 mild-hybrid with a 15 kW motor, as reported in the thesis / SAE **2020-01-0798** (*Water Injection System Application in a Mild Hybrid Powertrain* — **not** “2020-01-0000”). Treat them as **cycle-simulation results**, not a measured BSFC map. Enabling λ=1 at high load and more advanced spark is the qualitative experimental story in the open abstract.
  - **Do not use the draft’s mechanism claim** that knock suppression is “primarily charge dilution” and that latent-heat cooling is “insignificant.” The open licentiate abstract says water injection “mainly suppresses knock by reducing local in-cylinder mixture temperatures.” Resolve the mechanism only after reading the open PDF.

- **Volvo Cars / Volvo Group / Scania patents** exist as bibliographic records (e.g. EP 3561286A1 intake-manifold-integrated nozzle, US 4,558,665 / SE 442043B 1980s turbo + water injection, SE1450993A1). **No measured maps** were opened. No modern Volvo Cars series-production WI system was found.

- **Koenigsegg and NEVS:** nothing found for combustion-cycle water injection, accepted for this pass.

- **No current Swedish series-production passenger car** with factory combustion-cycle water injection was found. The Saab kit is the historical accessory/racing case.

## Errors and unverified claims in the Hermes draft

- **Saab 15–25 % fuel saving, 210 hp, 0.8 bar baseline, “>220 km/h” activation:** not supported by the opened PistonHeads account. Omit.

- **SAE 2020-01-0000:** placeholder. The mild-hybrid paper is **SAE 2020-01-0798**.

- **KTH “nothing found”:** incorrect. KTH has published heavy-duty **methanol** SI work with **direct water injection**, including *Experimental and chemical-kinetic evaluation of a heavy-duty methanol PFI engine with direct water injection*, *Fuel*, 2023, DOI https://doi.org/10.1016/j.fuel.2023.130326 , DIVA http://kth.diva-portal.org/smash/record.jsf?pid=diva2%3A1819136 , and related in-cycle knock-suppression records (e.g. diva2:1912884). Open abstracts describe knock and NOx benefits with a combustion-efficiency penalty on a single-cylinder research engine. **Specific percentages were not extracted in this pass.**

- **SE303242B / SE327933B** as Saab water-injection patents: titles were not confirmed. Do not cite until opened.

- **Aviation RM2/RM3/RM8/RM12 water-methanol and a documented transfer into the Saab kit:** not verified from a primary source here. The kit’s aviation analogy in magazine articles is secondary.

- **OSTI biblio 6585977:** a US assessment that *mentions* the Saab-Scania kit; not Swedish measured data. Check the open record before quoting it.

## Water Engine — what can actually be used

| Source | Open copy | What is usable |
| --- | --- | --- |
| PistonHeads / period kit descriptions of the Saab Sport kit | Open article | Historical accessory: upstream-of-compressor WI, ~10→17.4 psi, claimed 145→≥160 bhp. Not a BSFC/NOx map. Do not use 15–25 % economy or 210 hp. |
| Khatri licentiate 2019 (Chalmers) | Open PDF | Experimental PWI on a Volvo Cars 1.5 L 3-cyl turbo GDI, 91–98 RON, load curves, humidity and PN work. Read the PDF for map points. Cycle % figures are simulations. |
| SAE 2019-01-0034 / 2020-01-0798 | Chalmers records; SAE PDFs may be paywalled | Same campaign; hybrid-cycle **~0.5–1 %** FC (simulation). Use SAE **2020-01-0798**. |
| KTH methanol + DWI papers (2023–) | DIVA records; journal may be paywalled | Swedish HD methanol SI + direct WI exists. Extract numbers only from an opened open copy. |
| Volvo/Scania patents | Open patent text | Qualitative hardware/control intent only. |

Do not use: Saab 15–25 % / 210 hp / 0.8 bar baseline; SAE 2020-01-0000; “latent heat insignificant” without reading the Chalmers PDF; unverified SE303242B; KTH as a negative result.

## Link-check notes

Opened or search-confirmed in this pass: PistonHeads Saab kit article; Chalmers licentiate record/abstract and full-text URL; SAE 2019-01-0034 and 2020-01-0798 records; KTH DIVA/Fuel 2023 records. Volvo/Scania patents, SaabBlog, and the Chalmers humidity journal article were not fully read.
