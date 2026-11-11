# Malaysia — water in the combustion cycle (checked)

Status: DONE (checked). Hermes draft plus a verification section.
Hermes job: `20261111-150315-we-survey-34-malaysia-water-in-combustion` (started 3:03 PM, ended 3:06 PM America/Los_Angeles, 11 Nov 2026; runtime about 4 min; RESULT STATUS: DONE, rc 0).
Prompt language: Malay. Report language: English.

The Hermes text starts below. For numbers, prefer the verification section at the end.

---

# Malaysia — water in the combustion cycle (Hermes draft)
Country: Malaysia
Prompt language: Malay
Author: Hermes (box hjob)
Date: 2026-11-11

---

## 1. Executive summary

This survey covers Malaysian academic and industrial research on water-in-combustion technologies for road vehicles from the earliest documented work to 2026. The search encompassed water injection (port, direct, manifold), water-diesel emulsion (WiDE), water-biodiesel emulsion (WiBE), water-methanol injection, and six-stroke engine concepts with water injection. Key institutions are Universiti Teknologi Malaysia (UTM, especially MJIIT), Universiti Teknologi PETRONAS (UTP), Universiti Malaya (UM), Universiti Putra Malaysia (UPM), Universiti Malaysia Pahang (UMP), and Universiti Teknologi MARA (UiTM). Petronas-affiliated work appears mainly through UTP and UTM MJIIT. No production road vehicle in Malaysia has been found with factory-fitted water injection or water-emulsion fuel systems. All documented work is at the research, prototype, or engine-test-bed level. The strongest measured data clusters around: (a) port water injection on turbocharged gasoline engines (UTM/UMP/UiTM simulation and test-bed), (b) water-diesel and water-biodiesel emulsions with surfactant or non-surfactant real-time emulsification (UTP, UTM MJIIT), and (c) six-stroke engine thermodynamic and experimental studies (UMP). Measured results consistently show NOx reductions of 23–79%, modest torque/IMEP gains (up to ~19% brake torque, ~10.8% IMEP), and BSFC improvements up to ~23% in simulation; however, CO and soot/particulate emissions often rise with high water fractions, and emulsion stability remains a practical challenge.

---

## 2. Production or near-production road vehicles

**No documented Malaysian production or near-production road vehicle with factory water injection, water-methanol injection, or water-fuel emulsion fuel system.**

- Proton and Perodua: no public technical disclosure, press release, or homologation document describing water injection or emulsion fuel on any production model (searches covered Proton, Perodua, water injection, water-methanol, emulsion).
- Aftermarket: no Malaysian aftermarket kit with documented Malaysian vehicle installation and measured data found.
- Petronas fuel retail: Petronas sells conventional and bio-blended diesel/petrol; no documented retail water-emulsion fuel product for road vehicles.

---

## 3. Research, prototypes, and supplier systems

### 3.1 UTM MJIIT — Non-surfactant real-time water-in-diesel emulsion (RTES)
- **Organisation**: Malaysia-Japan International Institute of Technology (MJIIT), Universiti Teknologi Malaysia (UTM), Kuala Lumpur; RTES Technology (M) Sdn. Bhd. (spin-out / industry partner).
- **Years**: 2017–2024 (ongoing).
- **Engine / vehicle**: Common-rail direct-injection diesel light-duty truck (Isuzu / Hino class), tested on roller dynamometer following modified WVU 5-Peak cycle.
- **What was done**: Real-time non-surfactant emulsion supply system (RTES) installed near fuel pump; produces water-in-diesel emulsion on-board without surfactants. Water fraction varied; optimum found at 10 wt% water.
- **Measured results** (Hasbullah Abdul Rahman et al., 2023, *International Journal of Automotive Technology* 24(5): 1349–1358, DOI 10.1007/s12239-023-0109-3):
  - 10 wt% water emulsion reduced fuel consumption, NOx, and smoke emissions simultaneously.
  - Exact percentage reductions not quoted in open abstract; paper states "capable to reduce fuel consumption as well as nitrogen oxides and smoke emissions."
  - No measured power/torque penalty reported in abstract.
- **Source**: https://doi.org/10.1007/s12239-023-0109-3 (paywalled; author preprint not located; bibliographic data verified via Crossref).
- **Notes**: UTM MJIIT has a sustained publication line on non-surfactant emulsification (2017–2024), including in-line mixer comparisons, different water sources, and nano-additive studies (Ahmad Muhsin Ithnin et al., multiple papers in *Fuel*, *Energy Conversion and Management*, *Environmental Science and Pollution Research*, *Journal of the Society of Automotive Engineers Malaysia*). All are engine-test-bed or vehicle-on-dyno; no on-road fleet trial documented.

### 3.2 UTM — Port water injection on turbocharged gasoline (CamPro CFE 1.6L) — simulation
- **Organisation**: Faculty of Mechanical Engineering, Universiti Teknologi MARA (UiTM), Shah Alam (lead author Khairul Khusairi Kamaludin); engine modelled on Proton CamPro CFE 1.6L turbocharged gasoline engine.
- **Years**: ~2022–2023 (published 2023).
- **Engine / vehicle**: 1.6L turbocharged CamPro CFE (Proton), GT-Power 1D simulation validated against test-rig data.
- **What was done**: Two injectors in intake manifold; water flow rate varied; port water injection (PWI) with charge-air cooling effect.
- **Measured results** (simulation only):
  - Brake torque improvement up to **19%**.
  - Brake power improvement up to **10%**.
  - BSFC improvement up to **23%**.
  - NOx reduction referenced from literature (up to 34–50% in cited prior work).
- **Source**: Khairul Khusairi Kamaludin, "Engine Characteristics Analysis of Turbocharged Spark Ignition Engine with Water Injection Charge Air Cooling", *Journal of Fluid Mechanics and Thermal Sciences* (Semarak Ilmu), 2023. Open access PDF: https://semarakilmu.com.my/journals/index.php/fluid_mechanics_thermal_sciences/article/download/5574/2780/28025
- **Notes**: Simulation study; no hardware test-bed data in this paper. Engine is a Malaysian production engine (CamPro CFE), but water injection is not fitted to any production Proton vehicle.

### 3.3 UMP — Six-stroke engine with water injection (thermodynamic + experimental)
- **Organisation**: Faculty of Mechanical Engineering, Universiti Malaysia Pahang (UMP), Pekan.
- **Years**: 2009–2012 (cluster of final-year projects and theses).
- **Engine / vehicle**: Modified single-cylinder four-stroke gasoline engine converted to six-stroke (additional 5th stroke = water injection / steam expansion; 6th stroke = steam exhaust). Camshaft modified (3:1 gear ratio), water injector and metering pump added.
- **What was done**: Thermodynamic analysis (Ahmad Azril Azmi, 2012), experimental prototype (Lukman Nul-Hakem Mohd Yusop, 2012), water injection system design (Muhamad Nurzami Ab Sota, 2012), FEA of crankshaft (Muhammad Nasiruddin Anidin, 2009).
- **Measured results**:
  - Thermodynamic analysis: identified water quantity needed for 2nd power stroke and cylinder pressure profiles (two modes: with/without residual exhaust gas).
  - Experimental prototype: "engine is not running as well as expected when some problems occur at few part of the engine" (Lukman Nul-Hakem, 2012). Follower/camshaft issues noted; no validated performance data published.
  - Water injection system: fabricated successfully; pump pressure and injector opening pressure characterised (Nurzami, 2012).
- **Sources** (all UMP IR, open access):
  - Thermodynamic analysis: http://umpir.ump.edu.my/id/eprint/4564
  - Experimental study: http://umpir.ump.edu.my/id/eprint/4558
  - Water injection system design: http://umpir.ump.edu.my/id/eprint/4492
  - FEA crankshaft: http://umpir.ump.edu.my/id/eprint/247 (approx.)
- **Notes**: Academic prototypes only; no further development or road-vehicle integration documented after 2012.

### 3.4 UMP — Water injection on diesel engine (intake manifold, 2017)
- **Organisation**: Faculty of Mechanical Engineering, Universiti Malaysia Pahang (UMP).
- **Years**: 2017 (research report).
- **Engine / vehicle**: Single-cylinder diesel engine (make/model not specified in abstract).
- **What was done**: Single-point water injection into intake manifold; three injection orientations (with airflow, against airflow, sideways); water-to-fuel ratio 0–100% at part load (BMEP 2, 3.5, 5 bar, 2000 rpm).
- **Measured results** (Aziz Amir, Mamat Rizalman, Abdullah Abdul Adam, Hagos Ftwi Yohaness, Ali Obed Majeed, 2017):
  - **63% NOx decrease** at BMEP 5 bar, water-to-fuel ratio 100%.
  - Particulate matter increase at high water-to-fuel ratio.
  - Combustion process and performance parameters (efficiency, torque, fuel consumption) "marginally influenced".
- **Source**: UMP IR: https://umpir.ump.edu.my/id/eprint/36394 (research report, non-peer-reviewed, open PDF).
- **Notes**: Single-cylinder test bed; no multi-cylinder or vehicle data.

### 3.5 UMP — Water-emulsified biodiesel (WiBE) and biodiesel-butanol-water blends
- **Organisation**: Faculty of Mechanical Engineering, Universiti Malaysia Pahang (UMP).
- **Years**: 2020–2022.
- **Engine / vehicle**: Multi-cylinder direct-injection diesel engine (Wan Nor Maawa, 2020); Yanmar TF120M single-cylinder water-cooled diesel engine (Mohamad Izuan Izzudin, 2022).
- **What was done**: 
  - Wan Nor Maawa (2020): B20 biodiesel (palm oil methyl ester) emulsified with 10–30% water; stability and droplet size measured; engine test at varying loads.
  - Mohamad Izuan Izzudin (2022): Blends B10Bu5W5 (5% butanol + 5% water) and B10Bu10W5 (10% butanol + 5% water) vs D100.
- **Measured results**:
  - Wan Nor Maawa (2020): **Highest NOx reduction at 30% water, 40% load** (exact % not in abstract; "reduced significantly"). HC and CO2 emissions increased vs conventional diesel. Emulsion stability decreased with higher water content; droplet size increased.
  - Mohamad Izuan Izzudin (2022): Water addition produced better NOx results vs non-water blends; higher peak cylinder pressure with increasing rpm/load; combustion improved vs D100.
- **Sources**:
  - Wan Nor Maawa: http://umpir.ump.edu.my/id/eprint/30380 (Masters thesis, open access).
  - Mohamad Izuan Izzudin: http://umpir.ump.edu.my/id/eprint/36839 (Masters thesis, open access).

### 3.6 UTP — Water-in-diesel emulsion (WiDE) and water-in-biodiesel emulsion (WiBE) — extensive programme
- **Organisation**: Department of Mechanical Engineering, Universiti Teknologi PETRONAS (UTP), Seri Iskandar, Perak. Collaboration with University of Brighton (UK) and SIT Schiffs & Industrie Technik (M) Sdn Bhd (emulsion samples).
- **Years**: 2011–2025 (continuous).
- **Engine / vehicle**: Single-cylinder diesel engine test beds (various); optical/spray diagnostics for micro-explosion.
- **Key works**:
  - **2011**: Ahmad Nizar Yunus, BEng thesis — surfactant-stabilised WiDE stability study (http://utpedia.utp.edu.my/id/eprint/319).
  - **2013**: Muhammad Iskandar Ismail, BEng thesis — surfactant effect on combustion characteristics of emulsified diesel, 5% water (http://utpedia.utp.edu.my/id/eprint/10521).
  - **2014**: Z.A. Abdul Karim et al., *MATEC Web of Conferences* — WiDE characterisation (5%, 10%, 20% water by volume, mechanical homogenizer); droplet size <2 µm; density/viscosity higher than diesel; actual water content lower than mixed (https://www.matec-conferences.org/articles/matecconf/pdf/2014/04/matecconf_icper2014_02006.pdf).
  - **2018**: Z.A. Abdul Karim et al., *Applied Energy* (with Brighton) — effect of fuel injection equipment on dispersed phase of WiDE; micro-explosion droplet size smaller than in unused emulsion (preprint: https://cris.brighton.ac.uk/ws/files/496916/APEN-D-18-00209%20Revised%20manuscript%20-%20Published.pdf).
  - **2019**: Z.A. Abdul Karim et al., *Platform: A Journal of Engineering (PAJE)* 3(2):1 — **WiBE (water-in-biodiesel emulsion) on single-cylinder diesel engine at 2000 rpm, B5 diesel base (5% POME). 36 blends: 9/12/15% water, HLB 6–9, surfactant 5/10/15%. Results: 11.7% lower engine power with WiBE vs B5; up to 15.2% higher peak cylinder pressure at high load; up to 79% NOx reduction and 23% smoke opacity reduction at 15% water, optimum HLB (https://journal.utp.edu.my/paje/vol3/iss2/1/).
  - **2018**: Z.A. Abdul Karim et al., *MATEC Web of Conferences* — ultrasonic homogenizer for WiBE; viscosity issues at high surfactant (https://www.matec-conferences.org/articles/matecconf/pdf/2018/84/matecconf_ses2018_01012.pdf).
  - **2025**: Asghar Ali, PhD thesis — biosurfactant concentration and injection pressure effects on micro-explosion and emissions in water-in-B10 diesel emulsion (http://utpedia.utp.edu.my/id/eprint/32156).
- **Measured results summary**: Consistent NOx reductions (up to 79%), smoke/opacity reductions (up to 23%), but power penalty (~11–12%) and viscosity/stability challenges. Micro-explosion confirmed as key mechanism. All single-cylinder test bed.
- **Notes**: UTP is the most sustained Malaysian centre for water-diesel/biodiesel emulsion research, with Petronas-linked funding (FRGS, industry samples from SIT). No vehicle-level or multi-cylinder engine data published.

### 3.7 UPM — Water-in-diesel nanoemulsion with cerium oxide (2014)
- **Organisation**: Universiti Putra Malaysia (UPM), Serdang.
- **Years**: 2014 (Masters thesis).
- **Engine / vehicle**: Engine test bed (single-cylinder, details not in abstract).
- **What was done**: Triton X-100 surfactant, ultrasonication (20–35% amplitude, 10 min), water 0.80–1.15% w/w, CeO2 nano-additive. Droplet size 1.5–74 nm (TEM).
- **Measured results** (Bidita Binte Salahuddin, 2014):
  - Neat diesel: exhaust temp 290 °C, CO2 21784 ppm, CO 766 ppm, NO 276 ppm.
  - CeO2-enriched nanoemulsion: **exhaust temperature reduction up to 33%**, **NOx reduction up to 61%** vs neat diesel.
  - Physico-chemical properties (density, viscosity, flash point, pour point, acid number, calorific value, cetane number) characterised.
- **Source**: UPM IR: http://psasir.upm.edu.my/id/eprint/48104 (open access thesis).

### 3.8 UPM — Micro jet engine / gas turbine with ultrasonic atomization (2019)
- **Organisation**: Universiti Putra Malaysia (UPM).
- **Years**: 2019 (PhD thesis).
- **Engine / vehicle**: Micro jet engine (gas turbine) — **aviation/marine label**.
- **What was done**: Ultrasonic atomizer (4 components, 5 L/hr each) for biodiesel blends; not water injection per se, but ultrasonic fuel atomization.
- **Measured results**: 1% efficiency gain at three load levels; CO2 exhaust reduction ~25% at low load; NO reduction at low load.
- **Source**: UPM IR: http://psasir.upm.edu.my/id/eprint/84369.
- **Notes**: Gas turbine / aviation; included for completeness as same lab does combustion research.

### 3.9 UM — Water injection on hydrogen-fuelled compression ignition engine (HFCI) (2012)
- **Organisation**: Faculty of Engineering, University of Malaya (UM), Kuala Lumpur.
- **Years**: 2012 (PhD thesis).
- **Engine / vehicle**: Single-cylinder 4-stroke direct-injection YANMAR L100AE compression ignition engine.
- **What was done**: Timed port injection for hydrogen (0–20°CA ATDC, 3 LPH); timed manifold water injection (20°BTDC to 20°ATDC, duration 20°CA or 40°CA). ECU-controlled. Experimental + numerical simulation (equilibrium constant method, MATLAB).
- **Measured results** (Adnan Roseli, 2012):
  - **Optimum water injection: 20°ATDC, 20°CA duration** — increased gross indicated work, indicated thermal efficiency, lower indicated specific energy consumption (especially at 2000 rpm).
  - **Lowest HC and EGT**: 20°ATDC, 20°CA duration.
  - **Lowest CO2**: 0°CA, 40°CA duration.
  - **Lowest SO2**: 20°BTDC, 20°CA duration.
  - **Lowest CO (high speed)**: 0°CA, 20°CA duration.
  - **All water injection timings**: lower NOx across entire speed range.
  - Experimental emissions validated against numerical model (good agreement).
- **Source**: UM Students' Repository: http://studentsrepo.um.edu.my/8103 (open access PhD thesis).
- **Notes**: Hydrogen dual-fuel CI engine; water injection used for emission control and power augmentation. Relevant as a Malaysian university study of manifold water injection with detailed timing sweep.

### 3.10 UiTM — Water injection on diesel engine with hydrogen (2016–2021)
- **Organisation**: Universiti Teknologi MARA (UiTM), Shah Alam / Johor.
- **Years**: 2016 (conference paper), 2021 (Masters thesis).
- **Engine / vehicle**: Diesel engine with hydrogen and water injection at variable timing.
- **What was done**: Hydrogen (30 ml/s) + water mist injected at intake valve opening (20°CA ATDC); variable crank-angle duration for hydrogen and water.
- **Measured results** (eprints.utem.edu.my / Md. Farid Md. Boizi, 2021):
  - Lowest NOx with diesel-hydrogen-water.
  - CO reduction significant (trend).
  - Water injection slightly decreased performance (power) but improved thermal efficiency vs diesel alone.
  - "Water port injection will lead higher percentage of fuel to complete combustion compare to diesel alone."
- **Sources**:
  - 2016 conference paper: http://eprints.utem.edu.my/id/eprint/20833/2/182801-9797-IJMME-IJENS.pdf
  - 2021 Masters thesis (ethanol-methanol-gasoline blends, includes water injection context): https://ir.uitm.edu.my/id/eprint/46584

### 3.11 UTM — HCCI / RCCI conversion with water injection context (2011–2024)
- **Organisation**: UTM (main campus, Johor Bahru) and MJIIT.
- **Years**: 2011–2024 (RUG grants).
- **What was done**: Conversion of CI engine to HCCI for range-extender EV (UTM-TDR 26.1, 2018); ethanol fumigation in HCCI (2011); knock mitigation for hydrogen ICE (2024, Mohd Rozi Mohd Perang).
- **Water injection**: Not the primary focus; appears as knock mitigation strategy in HCCI/hydrogen contexts. No dedicated water injection test data published in these grant summaries.
- **Source**: UTM Scholar profiles (Dr. Zulkarnain Abdul Latiff, Mohd Rozi Mohd Perang).

---

## 4. University and institute work (summary table)

| Institution | Focus | Key researchers / labs | Years | Engine level | Open access |
|-------------|-------|------------------------|-------|--------------|-------------|
| UTM MJIIT | Non-surfactant WiDE (RTES), vehicle on dyno | Ahmad Muhsin Ithnin, Wira Jazair Yahya, Hasbullah Abdul Rahman | 2017–2024 | Light-duty truck (common-rail DI diesel) | Partial (abstracts, some preprints) |
| UTM (JB) | HCCI conversion, knock mitigation | Zulkarnain Abdul Latiff, Mohd Rozi Mohd Perang | 2011–2024 | Single-cylinder research engine | Grant summaries only |
| UTP | WiDE / WiBE emulsion characterisation, micro-explosion, engine test | Z.A. Abdul Karim, M.Y. Khan, A.R.A. Aziz, F.Y. Hagos | 2011–2025 | Single-cylinder diesel | Yes (theses, PAJE, MATEC) |
| UM | HFCI + timed manifold water injection | Adnan Roseli | 2012 | Single-cylinder Yanmar L100AE | Yes (PhD thesis) |
| UPM | WiDE nanoemulsion + CeO2; micro jet ultrasonic | Bidita Binte Salahuddin, Amer Alajmi | 2014, 2019 | Single-cylinder diesel; micro jet (aviation) | Yes (theses) |
| UMP | Six-stroke water injection; WiBE; diesel water injection | Lukman Nul-Hakem, Muhamad Nurzami, Wan Nor Maawa, Mohamad Izuan Izzudin, Aziz Amir | 2009–2022 | Single-cylinder gasoline/diesel; six-stroke prototype | Yes (theses, IR) |
| UiTM | Diesel-hydrogen-water injection; GT-Power SI water injection | Khairul Khusairi Kamaludin, Md. Farid Md. Boizi | 2016–2023 | Single-cylinder diesel; 1.6L CamPro CFE simulation | Yes (conference, journal, thesis) |

---

## 5. Historical / racing / aviation-marine transfer (labelled)

- **Aviation / gas turbine**: UPM micro jet engine (2019, PhD) — ultrasonic atomization for biodiesel, not water injection. **Label: aviation**.
- **Six-stroke concept**: UMP 2009–2012 prototypes based on Crower/Dyer six-stroke principle (water injection for 5th stroke steam expansion). Academic only; no racing or production link. **Label: historical concept**.
- **WWII reference**: Multiple Malaysian theses (UM, UMP) cite WWII aircraft water injection (MW50, ADI) as historical background; no Malaysian aviation engine production.
- **Petronas offshore**: Water injection facilities for enhanced oil recovery (Uzma Berhad, Petronas Carigali) — **not combustion cycle**; excluded from scope.
- **No Malaysian motorsport / racing water injection programme documented** (searches covered Sepang, Proton Motorsports, Petronas Syntium racing, etc.).

---

## 6. Water-fuel emulsions and other cycles

### 6.1 Water-in-diesel emulsion (WiDE) — surfactant-stabilised
- **UTP**: 5–20% water by volume, mechanical homogenizer, commercial surfactants (Span/Tween, Triton). Droplet size <2 µm. Stability days to weeks. Engine tests: NOx ↓, smoke ↓, power ↓ ~10–12%, viscosity ↑.
- **UPM**: Nanoemulsion (0.8–1.15% water, Triton X-100, ultrasonication, CeO2). Droplet 1.5–74 nm. NOx ↓ 61%, exhaust temp ↓ 33%.
- **UMP**: B20 biodiesel + 10–30% water (Wan Nor Maawa, 2020). NOx ↓ significantly (max at 30% water, 40% load). HC, CO2 ↑. Stability ↓ with water %.

### 6.2 Water-in-biodiesel emulsion (WiBE)
- **UTP**: B5 base (5% POME), 9–15% water, HLB 6–9 surfactants. 79% NOx ↓, 23% smoke ↓ at 15% water, optimum HLB. Power ↓ 11.7%. Peak pressure ↑ 15.2%.
- **UMP**: B10 + butanol + 5% water (Mohamad Izuan, 2022). NOx better than non-water blends.

### 6.3 Non-surfactant real-time emulsification (RTES)
- **UTM MJIIT**: On-board device (RTES) produces WiDE without surfactant. Tested on light-duty truck, modified WVU 5-Peak cycle. **Optimum 10 wt% water** — reduces fuel consumption, NOx, smoke simultaneously. Most advanced Malaysian system towards vehicle application.

### 6.4 Water-methanol injection
- **No dedicated Malaysian water-methanol injection study found**. Bosch water-methanol (MW50-type) referenced in literature reviews (UiTM, UMP theses) but no Malaysian experimental work. Searches for "water methanol injection Malaysia thesis" returned only general reviews.

### 6.5 Direct water injection (DWI) — gasoline
- **UiTM (simulation)**: GT-Power, CamPro CFE 1.6L turbo, port water injection (not direct). Torque ↑ 19%, power ↑ 10%, BSFC ↑ 23%.
- **UTP (with Brighton)**: Optical/spray studies of DWI vs PWI for micro-explosion; no engine performance data.
- **General**: Multiple theses cite DWI literature (Boretti, BMW, Bosch) but no Malaysian DWI hardware test.

### 6.6 Six-stroke (water injection for steam cycle)
- **UMP 2009–2012**: Thermodynamic analysis + prototype. Prototype did not run reliably. No performance data.

---

## 7. Negative results or "nothing found" areas

| Area | Search performed | Result |
|------|------------------|--------|
| Production vehicle with water injection (Proton, Perodua) | Proton/Perodua water injection, water-methanol, emulsion fuel | No homologation doc, press release, technical paper, or patent assignment to Proton/Perodua for production water injection |
| Petronas retail water-emulsion fuel | Petronas water diesel emulsion retail, Petronas WiDE pump | Petronas sells conventional/bio diesel; no water-emulsion retail product |
| Malaysian aftermarket water injection kit with vehicle data | Malaysia aftermarket water injection kit dyno | No documented Malaysian kit with measured vehicle data |
| Water-methanol injection (MW50-type) Malaysian test | Malaysia water methanol injection engine thesis | Only literature citations; no Malaysian experiment |
| Direct water injection (DWI) hardware test in Malaysia | Malaysia direct water injection gasoline engine test | Simulation only (UiTM); no DWI hardware test bed publication |
| Multi-cylinder diesel engine water injection (Malaysia) | Malaysia multi-cylinder diesel water injection | All engine tests single-cylinder |
| On-road fleet trial (water injection or emulsion) | Malaysia water injection fleet trial, Malaysia emulsion fleet trial | None |
| Malaysian patent for water injection in road vehicle | MY patent water injection engine, MY patent water diesel emulsion | Found international patents (US, EP, WO) with Malaysian inventors (UTP, UTM) but no granted MY patent for road vehicle water injection system located in search |

---

## 8. Source list (only real citations; legitimate open copies preferred)

1. **Hasbullah Abdul Rahman et al.** (2023) "Implementation of a Non-Surfactant Water-in-Diesel Emulsion Fuel in a Common Rail Direct Injection Diesel Vehicle", *International Journal of Automotive Technology* 24(5): 1349–1358. DOI: 10.1007/s12239-023-0109-3. (Paywalled; bibliographic data verified via Crossref; author affiliations: UTM MJIIT, RTES Technology, UiTM, Heriot-Watt Malaysia, Okayama Univ, Kagoshima Univ.)

2. **Khairul Khusairi Kamaludin** (2023) "Engine Characteristics Analysis of Turbocharged Spark Ignition Engine with Water Injection Charge Air Cooling", *Journal of Fluid Mechanics and Thermal Sciences*. Open access: https://semarakilmu.com.my/journals/index.php/fluid_mechanics_thermal_sciences/article/download/5574/2780/28025

3. **Ahmad Azril Azmi** (2012) "Thermodynamic analysis for a six stroke engine for heat recovery", UMP IR: http://umpir.ump.edu.my/id/eprint/4564 (open access thesis)

4. **Lukman Nul-Hakem Mohd Yusop** (2012) "Experimental study of six-stroke engine for heat recovery", UMP IR: http://umpir.ump.edu.my/id/eprint/4558 (open access thesis)

5. **Muhamad Nurzami Ab Sota** (2012) "Water injection system design for six stroke engine", UMP IR: http://umpir.ump.edu.my/id/eprint/4492 (open access thesis)

6. **Aziz Amir, Mamat Rizalman, Abdullah Abdul Adam, Hagos Ftwi Yohaness, Ali Obed Majeed** (2017) "Performance and NOx emissions of a diesel engine with water injection", UMP IR: https://umpir.ump.edu.my/id/eprint/36394 (open access research report)

7. **Wan Nor Maawa Wan Ghazali** (2020) "Performance, combustion and emissions analysis of water emulsified biodiesel in a diesel engine", UMP IR: http://umpir.ump.edu.my/id/eprint/30380 (open access Masters thesis)

8. **Mohamad Izuan Izzudin** (2022) "Investigation on performance, combustion and emission characteristics using biodiesel-butanol-water blends in diesel engine", UMP IR: http://umpir.ump.edu.my/id/eprint/36839 (open access Masters thesis)

9. **Z.A. Abdul Karim, M.Y. Khan, A.R.A. Aziz, F.Y. Hagos** (2019) "Attaining Simultaneous Reduction in NOx and Smoke by Using Water-in-Biodiesel Emulsion Fuels for Diesel Engine", *Platform: A Journal of Engineering (PAJE)* 3(2): Article 1. Open access: https://journal.utp.edu.my/paje/vol3/iss2/1/

10. **Z.A. Abdul Karim et al.** (2014) "Characterization of Water in Diesel Emulsion", *MATEC Web of Conferences* ICPE 2014, 02006. Open access: https://www.matec-conferences.org/articles/matecconf/pdf/2014/04/matecconf_icper2014_02006.pdf

11. **Muhammad Iskandar Ismail** (2013) "The Effects of Surfactant on Combustion Characteristics of Emulsified Diesel Fuel", UTPedia: http://utpedia.utp.edu.my/id/eprint/10521 (open access BEng thesis)

12. **Ahmad Nizar Yunus** (2011) "Study of Water-in-Diesel Emulsion Stabilized by Surfactant", UTPedia: http://utpedia.utp.edu.my/id/eprint/319 (open access BEng thesis)

13. **Z.A. Abdul Karim et al.** (2018) "The effect of fuel injection equipment on the dispersed phase of water-in-diesel emulsions", *Applied Energy* (with University of Brighton). Preprint: https://cris.brighton.ac.uk/ws/files/496916/APEN-D-18-00209%20Revised%20manuscript%20-%20Published.pdf

14. **Asghar Ali** (2025) "Effect Of Biosurfactant Concentration and Injection Pressure on Micro-explosion and Emissions in Water-in-b10 Diesel Emulsion", UTPedia: http://utpedia.utp.edu.my/id/eprint/32156 (open access PhD thesis)

15. **Bidita Binte Salahuddin** (2014) "Preparation and characterization of triton-water-diesel nanoemulsion with and without cerium oxide", UPM IR: http://psasir.upm.edu.my/id/eprint/48104 (open access Masters thesis)

16. **Adnan Roseli** (2012) "Water injection system for power augmentation and emission control for hydrogen-fuelled compression ignition engine", UM Students' Repository: http://studentsrepo.um.edu.my/8103 (open access PhD thesis)

17. **Md. Farid Md. Boizi** (2021) "The improvements of spark ignition (SI) engine's performance and emissions using different research octane number (RON) gasoline blend with ethanol - methanol", UiTM IR: https://ir.uitm.edu.my/id/eprint/46584 (open access Masters thesis; includes water injection context)

18. **eprints.utem.edu.my** (2016) "Effects of Equivalence Ratio on Performance and Emissions of Diesel Engine with Hydrogen and Water Injection System at Variable Injection Timing", open access conference paper: http://eprints.utem.edu.my/id/eprint/20833/2/182801-9797-IJMME-IJENS.pdf

19. **UTM Scholar profiles** (2011–2024) — grant summaries for Zulkarnain Abdul Latiff, Mohd Rozi Mohd Perang, Ahmad Muhsin Ithnin. https://utmscholar.utm.my/

---

## 9. Limits and open questions

- **No production vehicle data**: All Malaysian work is academic (theses, journal papers) or engine-test-bed. No OEM integration, durability, or on-road fleet data.
- **Single-cylinder dominance**: 17 of 18 engine-test entries are single-cylinder. Multi-cylinder interactions, aftertreatment compatibility, and transient response untested in Malaysia.
- **Emulsion stability vs. real-world**: Surfactant-stable emulsions last days/weeks; non-surfactant RTES solves this but only demonstrated on one light-duty truck over a chassis dyno cycle. Long-term injector/fuel-system wear, cold-start, water freezing, and microbial growth not studied.
- **Water-methanol gap**: Despite frequent citation of MW50/ADI and Bosch WaterBoost, no Malaysian lab has published water-methanol injection hardware tests.
- **Direct water injection (DWI) gap**: Only simulation (UiTM) and optical diagnostics (UTP/Brighton). No Malaysian DWI hardware on gasoline or diesel.
- **Six-stroke dead end**: UMP prototypes (2009–2012) did not run reliably; no follow-up publications after 2012.
- **Petronas role unclear**: Petronas funds UTP (FRGS, samples via SIT) and UTM MJIIT (industry partner RTES), but no Petronas-authored combustion-cycle water injection paper found. Petronas water injection patents are for reservoir/EOR, not engines.
- **Regulatory / halal / standards**: No Malaysian standard (SIRIM) for water-emulsion fuel quality, water purity, or on-board emulsification device certification.
- **Open question**: Can RTES non-surfactant emulsification meet Euro 6/7 equivalent (Euro 4M/5M in Malaysia) durability and OBD requirements? No data.
- **Open question**: Will any Malaysian OEM (Proton, Perodua, or new EV-range-extender startup) adopt water injection for knock-limited downsized turbo engines? No public indication.

---

*End of draft report.*

---

# Verification (checker, not Hermes)

Checked 2026-11-11, about 3:15 PM America/Los_Angeles, after the first Malaysia job. Paywall rule (James t880u): legitimate open copies only; no piracy sites.

The draft correctly found **no Malaysian series-production road vehicle** (Proton, Perodua, or aftermarket kit with measured data) and no Petronas retail water-emulsion fuel. It correctly pointed to sustained university work at UTM MJIIT (RTES), UTP, UMP, UiTM, UM, and UPM. It mixed a 2020 GT-Power simulation with measured maps, took an abstract “BSFC improvement” that the official body contradicts, quoted a 63% NOx figure that is not in the official Aziz 2017 abstract, treated Bidita’s 33%/61% cuts as a water-versus-diesel map, missed the Malaysia-led Khathri et al. 2022 Isuzu 4JJ1 paper, and wrongly said all engine tests were single-cylinder.

## Confirmed (spot-checked)

- **No Malaysian OEM series-production passenger car, truck, or motorcycle** with factory combustion-cycle water injection was found. Proton CamPro CFE appears only as the modelled engine in a simulation. Petronas retail water-emulsion diesel was not found.

- **Abdul Karim, Z.A., Khan, M.Y., A. Aziz, A. Rashid, and Hagos, Ftwi Y., 2019**, *Attaining Simultaneous Reduction in NOx and Smoke by Using Water-in-Biodiesel Emulsion Fuels for Diesel Engine*, *Platform: A Journal of Engineering* 3(2), Article 1, DOI **10.61762/pajevol3iss2art6683**, publication date 30 Oct 2019. Official UTP journal abstract. Single-cylinder diesel, constant **2000 rpm**, various loads, versus B5 (5% POME). 36 blends: **9/12/15%** water by volume, HLB **6–9**, surfactant **5/10/15%** of the added water. Official abstract: **11.7% lower engine power** with WiBE versus B5; up to **15.2% higher peak pressure** at high load with higher water content; WiBE with **15% water** and optimum HLB “is capable of reducing up to **79% NOx** and **23% smoke opacity** simultaneously.” https://journal.utp.edu.my/paje/vol3/iss2/1/

- **Khathri, A.M., Ismail, M.Y., Abdullah, A.A., Mamat, R., and Sutiman, 2022**, *Performance, Exhaust Emissions and Optimization Using Response Surface Methodology of a Water in Diesel Emulsion on Diesel Engine*, *J. Adv. Res. Fluid Mech. Therm. Sci.* 93(1), 1–12, DOI **10.37934/arfmts.93.1.112**. Official Semarak Ilmu abstract, already opened during the Indonesia check. Lead authors are Malaysian (Politeknik Sultan Mizan Zainal Abidin; Universiti Malaysia Pahang); Sutiman is at Universitas Negeri Yogyakarta. Official abstract: WD5 / WD10 on an **Isuzu 4JJ1** 4-cylinder 3000 cc; diesel and WD5 “comparable” in power, BTE and BSFC; NOx and CO “slightly decreased” with water; optimum **5%** water, **50%** load, **2446 rpm**, with **103.7 Nm**, **26.3 kW**, **43.8% BTE**, **172 g/kWh BSFC**, **521.8 ppm NOx**, **3.1% CO**. **Malaysia-led collaboration**, not a UNY-only map. The Malaysia draft did not cite this paper. https://semarakilmu.com.my/journals/index.php/fluid_mechanics_thermal_sciences/article/view/291

- **Abdul Rahman, Hasbullah, et al., 2023**, *Implementation of a Non-Surfactant Water-in-Diesel Emulsion Fuel in a Common Rail Direct Injection Diesel Vehicle*, *International Journal of Automotive Technology* 24(5), 1349–1358, DOI **10.1007/s12239-023-0109-3**. Official UTM eprints abstract (full text not available from that repository; Springer is paywalled). RTES (real-time non-surfactant emulsion fuel supply system) installed near the diesel fuel pump on a CRDI diesel vehicle, roller dynamometer, modified West Virginia University (WVU) 5-Peak cycle. Official abstract: optimum water percentage **10 wt%**, “capable to reduce fuel consumption as well as nitrogen oxides and smoke emissions.” **No percentages** in the opened official abstract; none were taken. https://eprints.utm.my/105466/

- **Kamaludin, Khairul Khusairi, Mamat, Aman Mohd Ihsan, and Mohamed, Zulkifli, 2020**, *Engine Characteristics Analysis of Turbocharged Spark Ignition Engine with Water Injection Charge Air Cooling*, *Journal of Advanced Research in Fluid Mechanics and Thermal Sciences* **68(1), 133–142** (received 22 Nov 2019, available 25 Mar 2020). Official open PDF (Semarak/Akademi Baru). **GT-Power simulation** of a 1.6 L Proton CamPro CFE PFI turbo engine; the model was validated against published industrial torque data **without water** (squares residuals of 99%). Port water injection in the intake manifold, two injectors, rates varied; 1000–6500 rpm. Official body: torque “raised to maximum with **12 g/s** flowrate by **19.6%** from the maximum torque generated by the engine without water injection”; rates **higher than 12 g/s** per injector “proved not to give any improvement,” and lower RPM with water can give **negative** brake torque. Highest brake power **113.89 kW** versus **102.78 kW** at **5000 rpm** (**10.8%**). Official body §3.3 and the conclusions: BSFC **increased** as water injection increased; at **6500 rpm / 12 g/s**, BSFC **0.4629 kg/kWh** versus base **0.3755 kg/kWh**, an **increment of 23.3%**. The official abstract’s “improved the brake specific fuel consumption as much as 23%” **contradicts** the body and is not taken. This is not a hardware test-bed map. NOx 34–50–70% figures in the draft are **literature citations**, not this paper’s results. https://semarakilmu.com.my/journals/index.php/fluid_mechanics_thermal_sciences/article/download/5574/2780/28025

- **Aziz, Amir, Mamat, Rizalman, Abdullah, Abdul Adam, Hagos, Ftwi Yohaness, and Ali, Obed Majeed, 2017**, *Performance and NOx emissions of a diesel engine with water injection*, unpublished UMP research report. Official UMPSA-IR abstract. Intake-manifold water injection at three orientations; water/fuel ratio **0–100%** in **20%** steps; simulation compared with test-bed measurements. Official test-bed wording: temperature and NOx “decrease drastically”; particulate matter increases; combustion “slightly affected”; “a little decrease of the efficiency and torque”; “fuel consumption is constant.” The draft’s **63% NOx at BMEP 5 bar / 100% water-to-fuel** is **not in the official abstract** and was not taken. https://umpir.ump.edu.my/id/eprint/36394/

- **Adnan, Roseli, 2012**, *Water injection system for power augmentation and emission control for hydrogen-fuelled compression ignition engine*, PhD thesis, University of Malaya. Official UM KNOVA abstract. Single-cylinder 4-stroke DI **Yanmar L100AE**; timed port hydrogen (0–20°CA, 3 LPH) plus timed manifold water injection (20°BTDC to 20°ATDC, duration 20° or 40°CA), compared with diesel-alone and diesel-hydrogen. Official abstract: optimum water injection **20° ATDC, duration 20°CA** — increased gross indicated work and indicated thermal efficiency, lower indicated specific energy consumption, especially at **2000 rpm**; that same timing also lowest HC and EGT; **all water-injection timings** indicated lower NOx across the entire speed range. **No percentages** in the opened official abstract. https://knova.um.edu.my/student_works_2010s/1448/

- **Salahuddin, Bidita Binte, 2014**, *Preparation and characterization of triton-water-diesel nanoemulsion with and without cerium oxide*, Masters thesis, Universiti Putra Malaysia. Official UPM IR abstract, opened from the Internet Archive snapshot of the official record (live psasir.upm.edu.my timed out in this pass). Water **0.80–1.15% w/w**, Triton X-100 **0.31–0.49% w/w**, with and without CeO2, engine-test-bed screening of CO2, CO and NOx. Official abstract: neat diesel exhaust temperature **290 °C**, CO2 **21784 ppm**, CO **766 ppm**, NO **276 ppm**. “A significant reduction of exhaust temperature (up to **33%**) as well as NOx emission (up to **61%**) was obtained during the combustion of **cerium oxide enriched nanoemulsions compared to those without**.” Those 33%/61% figures are **CeO2 versus no CeO2**, not water-versus-diesel, and were not taken as a water-injection map. The abstract only says qualitatively that nanoemulsion fuels can reduce exhaust emissions compared with neat diesel. http://psasir.upm.edu.my/id/eprint/48104 (archived official page: https://web.archive.org/web/20200203155423/http://psasir.upm.edu.my:80/id/eprint/48104/)

- **Mohd Yusop, Lukman Nul-Hakem, 2012**, *Experimental study of six-stroke engine for heat recovery*, UMP. Official UMPSA-IR abstract: the modified six-stroke prototype “did not run as expected” because of problems in several engine components, mainly the followers. **No validated performance map.** https://umpir.ump.edu.my/id/eprint/4558/

## Errors and unverified claims in the Hermes draft

- **Kamaludin misdated and mis-titled.** Official paper is *J. Adv. Res. Fluid Mech. Therm. Sci.* **68(1) 2020**, 133–142, not a 2023 Semarak “Journal of Fluid Mechanics and Thermal Sciences” article. It is a **simulation**, which the draft did note, but the executive-summary “torque ~19%, IMEP ~10.8%, BSFC ~23%” bundle must not be recycled as one measured map. Official body power is **10.8% at 5000 rpm**, not IMEP 10.8%. Official body **BSFC increased 23.3%** at 6500 rpm / 12 g/s; the abstract’s “improved … 23%” is contradicted by §3.3 and the conclusions.

- **Aziz 2017 “63% NOx.”** Not in the official UMP IR abstract. Official wording is qualitative (“decrease drastically”), with a slight torque/efficiency penalty and constant fuel consumption.

- **Bidita 2014 “exhaust temp −33%, NOx −61%.”** Official abstract compares **CeO2-enriched nanoemulsions with those without CeO2**. Water content is only **0.80–1.15% w/w**. Do not take those percentages as a water-versus-diesel map.

- **“All engine tests single-cylinder” / “no multi-cylinder diesel.”** Contradicted by Hasbullah 2023 (CRDI vehicle on a chassis dynamometer) and by Khathri 2022 (Isuzu 4JJ1 four-cylinder), which the draft missed. Wan Nor Maawa 2020 is also described in the draft as a multi-cylinder DI diesel; the official UMP IR page was down in this pass, so that thesis was not re-opened.

- **Md. Farid Md. Boizi 2021** official title is a UiTM Masters thesis on **RON gasoline with ethanol-methanol**, not a water-injection study. The 2016 hydrogen-and-water paper the draft mixed with it is on **eprints.utem.edu.my** (UTeM, Melaka), not UiTM. That official PDF was not opened in this pass (repository 500); those NOx/power claims were not taken.

- **Executive-summary “NOx 23–79%, torque ~19%, IMEP ~10.8%, BSFC ~23%”** stitches together a UTP emulsion smoke/NOx pair, a CamPro simulation torque, a mislabelled power figure, and a BSFC number whose official sign is the opposite of “improvement.” Do not use that bundle.

- **Wan Nor Maawa 2020 / Mohamad Izuan 2022 / Asghar Ali 2025** official records were not opened in this pass (UMP/UTP IR failed or were not fetched). Draft percentages from those theses were not taken.

## Water Engine — what can actually be used

| Source | Open copy | What is usable |
| --- | --- | --- |
| Abdul Karim et al. 2019, official UTP PAJE abstract (DOI 10.61762/pajevol3iss2art6683) | Yes (abstract) | Single-cylinder WiBE versus B5 at 2000 rpm. **11.7% lower engine power**; up to **15.2% higher peak pressure** at high load; **15% water** with optimum HLB, up to **79% NOx** and **23% smoke opacity** simultaneously. |
| Khathri et al. 2022, official Semarak abstract (DOI 10.37934/arfmts.93.1.112) | Yes (abstract) | Malaysia-led Isuzu 4JJ1 WD5/WD10 study (one UNY co-author). Diesel and WD5 “comparable” in power, BTE and BSFC; NOx and CO slightly down. Optimum **5% water, 50% load, 2446 rpm**: **103.7 Nm**, **26.3 kW**, **43.8% BTE**, **172 g/kWh**, **521.8 ppm NOx**, **3.1% CO**. |
| Hasbullah et al. 2023, official UTM eprints abstract (DOI 10.1007/s12239-023-0109-3) | Yes (abstract only) | RTES non-surfactant emulsion on a CRDI vehicle, roller dyno, modified WVU 5-Peak. Optimum **10 wt%** water; fuel consumption, NOx and smoke reduced. **No percentages** in the opened abstract. |
| Kamaludin et al. 2020, official OA PDF (JARFMTS 68(1)) | Yes (PDF) | **Simulation only** of CamPro CFE 1.6 L port WI. Torque **+19.6%** at 12 g/s versus maximum without water; brake power **+10.8%** at 5000 rpm (113.89 vs 102.78 kW); BSFC **+23.3%** (worse) at 6500 rpm / 12 g/s (0.4629 vs 0.3755 kg/kWh). Abstract “improved BSFC 23%” not taken. Not a hardware map. |
| Aziz et al. 2017, official UMP IR abstract | Yes (abstract) | Intake-manifold WI, 0–100% water/fuel. Test bed: NOx and temperature decrease drastically; PM up; slight efficiency/torque decrease; fuel consumption constant. **63% NOx not taken**. |
| Adnan 2012, official UM KNOVA abstract | Yes (abstract) | Yanmar L100AE hydrogen dual-fuel CI plus manifold WI. Optimum **20° ATDC / 20°CA**; all timings lower NOx. No percentages in the opened abstract. |
| Bidita 2014, official UPM IR abstract (archived official page) | Yes (abstract) | Nanoemulsion water only **0.80–1.15% w/w**. Neat-diesel baseline EGT 290 °C / NO 276 ppm. Official **33% / 61%** are **CeO2 versus no CeO2**, not water versus diesel. |
| Yusop 2012, official UMP IR abstract | Yes (abstract) | UMP six-stroke prototype did not run as expected. No performance map. |

Do not use: the draft executive-summary bundle; Kamaludin “BSFC improvement 23%” or “IMEP 10.8%”; Aziz 63% NOx; Bidita 33%/61% as a water-versus-diesel map; Boizi 2021 as a water-injection thesis; “all tests were single-cylinder”; unopened UMP/UTP thesis percentages.

## Link-check notes

Opened: official UTP PAJE abstract for Abdul Karim et al. 2019 (full PDF returned 403); official Semarak Ilmu abstract for Khathri et al. 2022 (previously opened); official UTM eprints abstract for Hasbullah et al. 2023; official Semarak/Akademi Baru open PDF for Kamaludin et al. 2020; official UMPSA-IR abstracts for Aziz 2017 and Yusop 2012 (via the official IR pages; live umpir.ump.edu.my did not respond to a direct fetch in this pass); official UM KNOVA abstract for Adnan 2012; Internet Archive snapshot of the official UPM IR abstract for Bidita 2014 (live psasir.upm.edu.my timed out or returned 500). Springer, MATEC, and some university IR hosts failed or were paywalled; no piracy sites were used. The Kamaludin official PDF was saved only to the private archive, not to the public GitHub repository.
