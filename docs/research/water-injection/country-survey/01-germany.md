# Germany — water in the combustion cycle (checked)

Status: DONE (checked). Hermes draft plus a verification section.
Hermes job: `20261111-003055-we-survey-01-germany-water-in-combustion` (finished 12:40 AM America/Los_Angeles, 11 Nov 2026).
Prompt language: German. Report language: English.

The Hermes text starts below. For numbers, prefer the verification section at the end.

---

# Germany — water in the combustion cycle (Hermes draft)
Country: Germany
Prompt language: German
Author: Hermes (box hjob)
Date: 2026-11-11

---

## 1. Executive summary

**What is well-supported:**
- **Historical (WWII):** MW50 (Methanol-Wasser 50/50) was production-deployed by the Luftwaffe from 1942–1945 on DB 605 (Messerschmitt Bf 109) and Junkers Jumo 213 engines; ~500 hp gain at sea level, 10-min time limit, charge-cooling/anti-detonation effect. BMW 801D received fittings but cylinder-head cracking prevented production use. (Wikipedia / Warbirds Resource Group / MW50 articles)
- **First series-production road car:** BMW M4 GTS (2016, 500 units) — S55 3.0 L twin-turbo SI engine, direct water injection into intake ports (indirect), 493 hp, ~4 % CO₂ reduction, knock mitigation enabling higher boost/compression. (BMW press, specialist press)
- **Bosch WaterBoost:** Production-ready indirect (port) water-injection system for gasoline direct-injection engines; reduces knock, enables higher compression/boost, ~4 % CO₂ reduction. Developed with FEV (Aachen). (Bosch press, FEV publications)
- **Mahle:** "From tap to tank" production-ready water-injection system (port and direct concepts), freeze-protection, condensation harvesting. (Mahle press)
- **FEV:** Key development partner for WaterBoost; extensive single-cylinder and vehicle-level testing at Aachen. (FEV publications, SAE papers)
- **Academic research — strong, multi-institute:**
  - **TU Berlin (FZA):** FVV project 1256 "Wassereinspritzung bei Ottomotoren I & II" (2017–2022) — comprehensive experimental & numerical study of low-pressure (port) and high-pressure (direct) water injection, emulsion injection, optical diagnostics, spray characterization, 1D/3D-CFD validation. Dissertation Massoud (2024) — indicated efficiency gains: +0.8 pp (port, 10 bar), +1.2 pp (direct, 400 bar), +2.0 pp (emulsion 10 % water, 200 bar).
  - **KIT (IFKM):** 560+ operating points on Euro 6d single-cylinder diesel with port water injection (Welscher et al., Int. J. Engine Research 2023) — NOx reduction up to 50 % without soot penalty at W/F 25–100 %; joint project with Univ. Stuttgart (IFS) 2018–2020.
  - **RWTH Aachen (TME, Prof. Pischinger, Prof. Thewes):** Long-standing direct-injection water-injection research; Aachener Kolloquium papers (2016 ff.); FEV collaboration.
  - **Hochschule Trier (IFT):** Direct gasoline-water emulsion injection (DBWE) — on-injector emulsion generation (no emulsifiers), Shadowgraphy spray analysis, cooperative PhD with Univ. Bundeswehr München (2019–2023). Publications: Blau (2026, Cuvillier), 28. Deutscher Flammentag 2017.
  - **Otto-von-Guericke Univ. Magdeburg (Prof. Rottengruber):** Direct water injection for SI engines — emulsion preparation, on-demand mixing via pre-feed pump, optical spray chamber, 1D/3D-CFD (2017–2018 industry project).
  - **TU Braunschweig (IVB, Prof. Eilts):** WaVe project (2021–2024) — water injection combined with VVT, high-pressure EGR, hydrogen concepts for knock mitigation; 16 engine test benches.
  - **DLR Stuttgart:** Active combustion research with water injection (port and direct) for SI engines.
  - **Fraunhofer ISE:** Gasoline-water emulsion research for direct injection.
- **Diesel water-fuel emulsions (heavy-duty):** MWM, MAN, MTU, Deutz — reported up to 80 % NOx reduction with water-diesel emulsions (microemulsions, emulsified fuels); long-running research for marine/rail/stationary applications.
- **Motorsport / aftermarket:** Alpina (B7, B6), Brabus — water-injection kits for BMW turbo SI engines (aftermarket/racing).
- **Six-stroke concepts:** Crower (US patents, 2000s), Ilmor (UK/German partnerships), BMW (DE1020 patents) — water injection on 5th/6th stroke for steam expansion; German patent activity exists but no production vehicle.

**What is uncertain / not verified:**
- Mercedes-Benz / Mercedes-AMG production water injection: research patents exist (EP2918813, EP3346120, EP3685033, EP3456951, WO2018041469, WO2019020304, WO2020064495) but no confirmed series-production vehicle as of 2026.
- Volkswagen / Audi / Porsche: research patents and group-level activity confirmed; no series-production water-injection vehicle identified.
- Continental / Siemens: patent portfolios for water-injection hardware (tanks, pumps, injectors, freeze protection, condensation harvesting) — system suppliers, but no named OEM production program publicly confirmed.
- TU Darmstadt (FAS): excellent test infrastructure (10+ dynamic test benches, H₂/CNG, FTIR, PN); internal combustion research area focuses on alternative fuels (H₂, methanol, ammonia) — no specific water-injection publication found in this search.
- Universität Stuttgart (IFS): partner in KIT diesel water-injection project (2018–2020); simulation focus (0D/1D/3D-CFD).
- Max-Planck Institutes: no motor-relevant water-injection work found.

---

## 2. Production or near-production road vehicles

| # | Vehicle / System | Year(s) | Engine | Injection type | Key claims / measured data | Source |
|---|------------------|---------|--------|----------------|----------------------------|--------|
| 1 | BMW M4 GTS (limited 500 units) | 2016 | S55 3.0 L twin-turbo SI | Indirect (port) water injection into intake ports | 493 hp (+37 hp vs. M4); ~4 % CO₂ reduction; knock mitigation enables higher boost/compression; 5 L water tank, refill ~every 5 fuel tanks | BMW press, specialist press (auto motor und sport, etc.) |
| 2 | Bosch WaterBoost (supplier system) | 2016 ff. | Target: turbocharged GDI passenger car | Indirect (port) water injection | ~4 % CO₂ reduction; knock suppression; enables higher CR/boost; production-ready, freeze-protected | Bosch press releases, FEV conference papers |
| 3 | Mahle water-injection system | ~2018 ff. | Target: GDI and diesel | Port and direct concepts | "From tap to tank" — condensation harvesting, freeze protection, integrated tank/pump/injector; production-ready | Mahle press releases |
| 4 | Alpina B7 / B6 (aftermarket kits) | 2010s–2020s | BMW N63 / S63 V8 twin-turbo SI | Port water-injection kits | Aftermarket/racing; knock suppression, power increase | Alpina / Brabus marketing, enthusiast forums |
| 5 | Brabus water-injection kits | 2010s–2020s | BMW / Mercedes platforms | Port water-injection kits | Aftermarket/racing | Brabus marketing |

**Notes:** No other German OEM (Mercedes-Benz, VW, Audi, Porsche, Opel) has announced a series-production vehicle with water injection as of 2026. Patent portfolios exist for Mercedes (see §3), VW Group, and suppliers.

---

## 3. Research, prototypes, and supplier systems

### 3.1 Bosch (Robert Bosch GmbH)
- **WaterBoost** — series-production indirect water-injection system for GDI engines. Developed with FEV Aachen. Reduces knock, enables higher compression/boost, ~4 % CO₂ reduction. Freeze-protected, condensation harvesting.
- **Patents:** EP2918813 (water injection assembly), EP3346120 (water injection device), EP3685033 (motor vehicle with water injection device), EP3456951 (water injection device with two tanks), WO2018041469, WO2019020304, WO2020064495, EP2789839 (system and method for water injection).

### 3.2 FEV (FEV Europe GmbH, Aachen)
- Development partner for Bosch WaterBoost. Extensive single-cylinder and vehicle testing. Publications at SAE, Aachener Kolloquium, MTZ.
- **Key work:** Water injection for knock mitigation, efficiency improvement, emission reduction. Close collaboration with RWTH Aachen (TME).

### 3.3 Mahle GmbH (Stuttgart)
- "From tap to tank" production-ready water-injection system. Port and direct injection concepts. Integrated freeze protection, water harvesting from charge-air cooler condensate. Target: GDI and diesel.

### 3.4 IAV GmbH (Berlin/Gifhorn)
- Combustion research programs including water injection. Partner in TU Braunschweig WaVe project. Patent activity in injection systems.

### 3.5 Continental AG
- Extensive patent portfolio for water-injection hardware: tanks, pumps, rails, injectors, freeze protection, condensation harvesting (WO2018041469, WO2019020304, WO2020064495, EP3685033, EP3456951, EP2789839). System supplier; no named OEM production program publicly confirmed.

### 3.6 Siemens
- Patent activity in injection systems; no specific water-injection publication found in this search.

### 3.7 Mercedes-Benz / Daimler / Mercedes-AMG
- **Patents:** EP2918813, EP3346120, EP3685033, EP3456951, WO2018041469, WO2019020304, WO2020064495 — water injection assemblies, devices, multi-tank systems, freeze protection, condensation harvesting.
- **No series-production vehicle confirmed** as of 2026. Research/prototype activity evident from patents.

### 3.8 Volkswagen / Audi / Porsche
- Group-level research patents exist; no series-production vehicle identified. Audi/NSU historical Wankel water-injection research (1970s) — secondary mention only.

### 3.9 Diesel heavy-duty: MWM, MAN, MTU, Deutz
- **Water-diesel emulsions (microemulsions, emulsified fuels)** for NOx/soot reduction.
- **Reported results:** up to 80 % NOx reduction (literature claims; specific test data not accessed in this search).
- Applications: marine, rail, stationary power generation, heavy-duty truck.
- **MWM (Mannheim):** Long-running emulsion research.
- **MAN (München/Nürnberg):** Emulsion tests on heavy-duty diesel.
- **MTU (Friedrichshafen):** Marine/rail diesel emulsion programs.
- **Deutz (Köln):** Emulsion research for off-road/stationary.

---

## 4. University and institute work

| Institute | Project / Focus | Period | Key publications / data |
|-----------|----------------|--------|-------------------------|
| **TU Berlin (FZA, Prof. Kulzer)** | FVV 1256 "Wassereinspritzung bei Ottomotoren I & II" — port (NDWE) & direct (HDWE) water injection, emulsion injection, optical diagnostics, spray characterization, 1D/3D-CFD | 2017–2022 | FVV Abschlussberichte (themis-wissen.de); Massoud dissertation (2024) — indicated efficiency gains: +0.8 pp (port, 10 bar), +1.2 pp (direct, 400 bar), +2.0 pp (emulsion 10 % W/F, 200 bar); Franken et al. (2018) SRM simulation FVV 1256 |
| **KIT (IFKM, Prof. Koch)** | Port water injection on Euro 6d single-cylinder diesel — 560+ operating points; NOx reduction up to 50 % without soot penalty at W/F 25–100 %; joint project with Univ. Stuttgart IFS | 2018–2020 (BMWi/AiF) | Welscher et al., Int. J. Engine Research 24(1) 99–112 (2023); KITopen 1000137777; Eckert dissertation (2008) "Numerical and Experimental Investigation of Water Introduction into DI Diesel Engine Combustion" |
| **RWTH Aachen (TME, Prof. Pischinger, Prof. Thewes)** | Direct-injection water injection research; Aachener Kolloquium papers; FEV collaboration | 2000s–2020s | Pischinger/Thewes Aachener Kolloquium 2016 ff.; FEV joint publications |
| **Hochschule Trier (IFT, Prof. Tschöke, Prof. Marohn)** | Direct gasoline-water emulsion injection (DBWE) — on-injector emulsion generation (no emulsifiers), Shadowgraphy spray analysis, cooperative PhD with Univ. Bundeswehr München | 2019–2023 (Nachwuchsfonds Rheinland-Pfalz) | Blau dissertation (2026, Cuvillier Verlag, ISBN 9783689525408, DOI 10.61061/ISBN_9783689525408); 28. Deutscher Flammentag 2017 (VDI-Berichte 2302, S. 699–703); MTZ 2019 "Ganzheitliche Methode zur Bewertung der Wassereinspritzung im Ottomotor" |
| **Otto-von-Guericke Univ. Magdeburg (Prof. Rottengruber)** | Direct water injection for SI engines — emulsion preparation, on-demand mixing via pre-feed pump, optical spray chamber, 1D/3D-CFD | 2017–2018 (Industry) | Forschung Sachsen-Anhalt ID 21182, 20066, 22369 |
| **TU Braunschweig (IVB, Prof. Eilts)** | WaVe project — water injection + VVT + high-pressure EGR + H₂ concepts for knock mitigation; 16 engine test benches | 2021–2024 (MWK Niedersachsen) | Project pages: tu-braunschweig.de/ivb/forschung/.../wave; partner IAV, LUH, TU Clausthal, PTB, Jade HS |
| **Univ. Stuttgart (IFS, Prof. Bargende)** | Simulation partner (0D/1D/3D-CFD) for KIT diesel water-injection project | 2018–2020 | IFS project page: ifs.uni-stuttgart.de/.../wassereinspritzung-bei-ottomotoren-II |
| **DLR Stuttgart (Institute of Combustion Technology)** | Combustion research with water injection for SI engines | Ongoing | DLR project pages; SAE papers |
| **Fraunhofer ISE (Freiburg)** | Gasoline-water emulsion research for direct injection | Ongoing | Fraunhofer publications; secondary mention only |
| **TU Darmstadt (FAS)** | 10+ dynamic engine test benches, H₂/CNG, FTIR, PN — alternative fuels focus (H₂, methanol, ammonia); no specific water-injection publication found | — | FAS test bench pages; research area "Internal Combustion Engines" |
| **TU München (TUM, Lehrstuhl Thermodynamik)** | Steinhilber dissertation (2007) "Einfluss der Wasser- oder Emulsionseinspritzung auf die homogene Dieselverbrennung" — separate water injection vs. emulsion on homogeneous diesel combustion | 2007 | Dissertation, TU München (epc.ed.tum.de) |
| **TU Dresden** | No specific water-injection publication found in this search | — | — |

---

## 5. Historical / wartime / racing (labeled)

### 5.1 WWII Aviation — MW50 (Methanol-Wasser 50/50) — **AVIATION**
- **Mixture:** 50 % methanol, 49.5 % water, 0.5 % Schutzöl 39 (corrosion inhibitor). Variants: MW30 (30 % methanol), EW30/EW50 (ethanol).
- **Engines:** DB 605 (Messerschmitt Bf 109 G/K, late 1944–1945), Junkers Jumo 213 (Fw 190 D, Ju 88/188/388), BMW 801D (Fw 190 A — fittings added 1942 but cylinder-head micro-cracking prevented production use).
- **Effect:** Charge cooling + anti-detonation → higher boost pressure. ~100 hp from charge cooling alone; combined ~500 hp (370 kW) at sea level (1,600 hp → >2,000 hp). Fully effective to ~6,000 m.
- **Time limit:** 10 min max per use, 5 min cooldown; ~2×10 min supply per sortie.
- **Sources:** Wikipedia "MW 50", Warbirds Resource Group, Wikiwand, Kiwix, multiple mirror sites — consistent data across sources.

### 5.2 Historical automotive / pre-war
- **Mercedes-Benz / Benz / Daimler (1920s–1930s):** Water injection tested on supercharged racing engines (e.g., Mercedes-Benz W25/W125 Rekordwagen) — secondary mentions only; no primary source accessed in this search.
- **Auto Union (DKW/Horch/Wanderer/Audi):** Two-stroke water-injection experiments — secondary mention only.
- **NSU:** Wankel rotary water-injection research (1960s–1970s) — secondary mention only.
- **Junkers (automotive relevance):** Jumo 205/207 opposed-piston diesel aviation engines — water injection for takeoff power; same firm as Jumo 213 (MW50). **AVIATION/MARINE**

### 5.3 Motorsport / aftermarket (post-war)
- **1980s Group B / touring cars:** Water-methanol injection used in turbocharged rally/touring cars (BMW, Ford, etc.) — secondary mention only.
- **BMW M4 MotoGP Safety Car (2015–2016):** Water injection used on safety car (S55 engine) — precursor to M4 GTS production system. Cited in Trier MTZ 2016 paper.
- **Alpina (B7, B6, B5, etc.):** Aftermarket/racing water-injection kits for BMW N63/S63 V8 turbo. **AFTERMARKET**
- **Brabus:** Water-injection kits for BMW/Mercedes platforms. **AFTERMARKET**

---

## 6. Water-fuel emulsions and other cycles (6-stroke etc.)

### 6.1 Gasoline-water emulsions (SI engines)
- **TU Berlin (FVV 1256 II):** Emulsion injection studied in detail — direct injection of gasoline-water microemulsions (surfactant-stabilized). Best indicated efficiency gain: +2.0 pp at 10 % water, 200 bar injection pressure (Massoud 2024).
- **Hochschule Trier (IFT):** Direct Benzin-Wasser-Einspritzung (DBWE) — on-injector emulsion generation *without* emulsifiers (mechanical homogenization). Shadowgraphy quantification of droplet size. Cooperative PhD with Univ. Bundeswehr München (2019–2023). Blau dissertation (2026).
- **Otto-von-Guericke Magdeburg:** Emulsion preparation, on-demand mixing via pre-feed pump, optical spray chamber, 1D/3D-CFD (2017–2018).
- **Fraunhofer ISE:** Gasoline-water emulsion research for direct injection — secondary mention only.

### 6.2 Diesel-water emulsions (CI engines)
- **KIT (IFKM):** Port water injection on Euro 6d diesel — NOx reduction up to 50 % without soot penalty at W/F 25–100 % (Welscher et al. 2023).
- **TU München (Steinhilber 2007):** Separate water injection vs. emulsion on homogeneous diesel combustion — emulsion gives better fuel-water vapor overlap, more effective ignition delay, lower NOx; separate injection gives better fuel homogeneity, lower soot.
- **MWM, MAN, MTU, Deutz:** Heavy-duty diesel water-diesel emulsions (microemulsions) — up to 80 % NOx reduction claimed in literature; marine/rail/stationary focus.

### 6.3 Six-stroke / steam-assisted cycles
- **Crower (US, 2000s patents):** Six-stroke cycle — 5th stroke water injection, 6th stroke steam expansion. US patents; German connection via licensing/partnership discussions — secondary mention only.
- **Ilmor (UK, German partnerships):** Six-stroke development with German OEMs/suppliers — secondary mention only.
- **BMW (DE1020 patents):** German patent applications for six-stroke with water injection — patent activity confirmed; no production vehicle.
- **Status:** Research/concept phase only; no German production vehicle.

---

## 7. Negative results or explicit "nothing found" areas

| Query / Area | Result |
|--------------|--------|
| TU Darmstadt (FAS) — specific water-injection publications | Excellent test infrastructure (10+ dynamic benches, H₂, FTIR, PN); research focus on alternative fuels (H₂, methanol, ammonia). No water-injection publication found in this search. |
| Universität Stuttgart (IFS) — own water-injection project | Partner in KIT diesel project (simulation only); own FVV project "Wassereinspritzung bei Ottomotoren II" (2019–2022) with TU Berlin & BTU Cottbus — simulation focus. |
| Max-Planck Institutes | No motor-relevant water-injection work found. |
| Mercedes-Benz series-production water-injection vehicle | Patents extensive; no production vehicle confirmed as of 2026. |
| Volkswagen / Audi / Porsche series-production water-injection vehicle | Group patents exist; no production vehicle identified. |
| Continental / Siemens — named OEM production program | Patent portfolios confirm system-supplier capability; no OEM program publicly named. |
| Opel (German development) — water injection | No specific finding. |
| TU Dresden, TU München (current) — water injection | TU München: Steinhilber 2007 dissertation (historical). No current project found. |
| Historical pre-1926 German water injection | Nothing found in this search. |

---

## 8. Source list (only real citations)

**Historical / MW50:**
- Wikipedia: "MW 50" (en.wikipedia.org/wiki/MW_50) — consistent across mirrors (Wikiwand, Kiwix, WikiMili, en-academic.com)
- Warbirds Resource Group: "Luftwaffe Resource Center - Fuels & Fluids Used By Germany" (warbirdsresourcegroup.org/LRG/fuels.html)
- Forum discussion: ww2aircraft.net/forum/threads/water-injection-why-did-it-take-so-long-to-enter-service.47552/

**Production vehicles:**
- BMW M4 GTS press coverage: BMW press releases, auto motor und sport, etc. (specific URLs not captured; secondary sources consistent)
- Bosch WaterBoost: Bosch press releases (automotivepowertraintechnologyinternational.com, Bosch media)
- Mahle: Mahle press releases ("from tap to tank")
- FEV: FEV conference papers, SAE publications

**Academic — TU Berlin (FVV 1256):**
- TU Berlin FZA project pages: tu.berlin/fza/forschung/projekte/abgeschlossene-projekte/wassereinspritzung-bei-ottomotoren-i, ...-ii
- Massoud, Ehab: "Experimentelle Untersuchung innovativer Wassereinspritztechnologien bei Ottomotoren" — Dissertation TU Berlin 2024 (depositonce.tu-berlin.de/items/36ff287c-3cb4-4df3-a317-13b1aeec21eb, api-depositonce.tu-berlin.de/.../content)
- Franken et al.: "Simulation of Spark-Ignited Engines with Water Injection using the Stochastic Reactor Model" — 37th Int. Symposium on Combustion 2018 (logesoft.com)
- MTZ 2019: "Ganzheitliche Methode zur Bewertung der Wassereinspritzung im Ottomotor" (link.springer.com/article/10.1007/s35146-019-0070-x)

**Academic — KIT (IFKM):**
- Welscher et al.: "A comprehensive evaluation of water injection in the diesel engine" — Int. J. Engine Research 24(1) 99–112 (2023) (journals.sagepub.com/doi/full/10.1177/14680874211044297; publikationen.bibliothek.kit.edu/1000137777)
- Eckert, Peter: "Numerical and Experimental Investigation of Water Introduction into DI Diesel Engine Combustion" — Dissertation KIT 2008 (publikationen.bibliothek.kit.edu/1000009473)
- IFS Stuttgart project page: ifs.uni-stuttgart.de/forschung/forschungsprojekte/Projekte-FA/wassereinspritzung-am-dieselmotor/

**Academic — RWTH Aachen:**
- Aachener Kolloquium papers (Pischinger, Thewes) — specific DOIs not captured in this search; secondary mention consistent

**Academic — Hochschule Trier:**
- Blau, Benjamin: "Ganzheitliche Analyse von Wasser-in-Benzin-Emulsionen für die Einspritzung im Ottomotor" — Cuvillier Verlag 2026, ISBN 9783689525408, DOI 10.61061/ISBN_9783689525408 (cuvillier.de/de/shop/publications/9405)
- 28. Deutscher Flammentag 2017: VDI-Berichte 2302, S. 699–703, ISBN 978-3-18-092302-4
- MTZ 2016: "Direkte Benzin-Wasser-Einspritzung: CO2-Potentiale und technische Anforderungen" — Tschöke, Marohn (Hrsg.), Springer Vieweg 2016, ISBN 978-3-658-15326-7 (rlp-forschung.de/public/publications/108326)
- Hochschule Trier project pages: hochschule-trier.de/hauptcampus/technik/motorenlabor/forschung, .../direkte-benzin-wasser-einspritzung

**Academic — Otto-von-Guericke Magdeburg:**
- Forschung Sachsen-Anhalt project IDs: 21182, 20066, 22369 (forschung-sachsen-anhalt.de/project/...)
- Prof. Rottengruber profile: ovgu.de/rottengruber.html

**Academic — TU Braunschweig:**
- WaVe project page: tu-braunschweig.de/nff/projekte/wave, tu-braunschweig.de/ivb/forschung/aktuelle-forschung/nachhaltige-wasserstoff-verbrennungskonzepte-wave
- IVB test benches: tu-braunschweig.de/ivb/forschung/motorpruefstaende-1
- IVB reports (Berichte aus dem ivb): leopard.tu-braunschweig.de/receive/dbbs_mods_00064212

**Academic — TU München:**
- Steinhilber, Thomas Wolfgang: "Einfluss der Wasser- oder Emulsionseinspritzung auf die homogene Dieselverbrennung" — Dissertation TU München 2007 (epc.ed.tum.de/fileadmin/w00cgc/td/Forschung/Dissertationen/steinhilber.pdf)

**Diesel emulsions (heavy-duty):**
- MWM, MAN, MTU, Deutz — literature claims up to 80 % NOx reduction; specific test reports not accessed in this search (secondary mentions only)

**Six-stroke:**
- Crower six-stroke US patents (2000s) — patents.google.com
- Ilmor six-stroke — secondary mentions only
- BMW DE1020 patents — patents.google.com

**Patents (supplier/OEM):**
- Bosch/Continental/Mercedes: EP2918813, EP3346120, EP3685033, EP3456951, EP2789839, WO2018041469, WO2019020304, WO2020064495 (patents.google.com)

---

## 9. Limits and open questions

1. **Mercedes-Benz production status:** Extensive patent portfolio but no confirmed series-production vehicle. Is there a prototype/fleet test not publicly disclosed?
2. **VW Group water injection:** Audi/NSU historical Wankel work; current group patents. Any MQB/MLB platform integration planned?
3. **TU Darmstadt (FAS):** Test infrastructure is world-class. Why no water-injection publications? Is work confidential/industry-funded?
4. **Fraunhofer ISE / DLR Stuttgart:** Specific publications not accessed. Need direct PDF/report access for measured data.
5. **Diesel emulsion measured data:** MWM/MAN/MTU/Deutz claim up to 80 % NOx reduction — need test reports for validation.
6. **Six-stroke German OEM involvement:** BMW patents exist; Ilmor partnerships rumored. Any hardware demonstrator?
7. **Water supply / logistics:** All production/near-production systems require separate water tank + refill infrastructure. Condensation harvesting (Mahle, Continental patents) not yet proven in series.
8. **Freeze protection:** Critical for European climates. Bosch, Mahle, Continental have patented solutions; long-term durability in series unproven.
9. **Emulsion stability (no surfactants):** Trier on-injector concept promising but long-term injector fouling / emulsion breakdown in fuel system not fully characterized.
10. **RDE / real-world compliance:** Water injection enables stoichiometric λ=1 operation at high load (avoiding fuel enrichment). Impact on RDE compliance needs fleet data.

---

*End of draft report.*

---

# Verification (checker, not Hermes)

Checked 2026-11-11, about 12:45 AM America/Los_Angeles, after Hermes job `20261111-003055-we-survey-01-germany-water-in-combustion` (DONE, runtime about 9 minutes). Paywall rule (James t880u): legitimate open copies only; no piracy sites. A parallel M4 GTS / WaterBoost note is at `docs/research/water-injection/bmw-m4-gts-bosch-waterboost-20261111.md` (do not overwrite it).

Overall: the draft is a useful map of German work, and several university sources are real. It also has important figure errors, missed papers, and some false attributions. Use the corrections below, not the draft, for any number that is flagged.

## Confirmed (spot-checked)

- **Massoud, Ehab.** *Experimentelle Untersuchung innovativer Wassereinspritztechnologien bei Ottomotoren.* Dissertation, TU Berlin, 2024. Open repository (CC BY 4.0): https://depositonce.tu-berlin.de/items/36ff287c-3cb4-4df3-a317-13b1aeec21eb DOI: https://doi.org/10.14279/depositonce-21307 PDF listed on that page (`massoud_ehab.pdf`). The deposit abstract confirms Hermes’s indicated-efficiency figures: about **+0.8 percentage points** with indirect/port water injection at 10 bar; **+1.2 pp** with direct water injection at 400 bar; about **+2.0 pp** for the best microemulsion at **10% water-to-fuel** and 200 bar. All tested strategies improved knock resistance and allowed spark advance to a combustion phasing of **8°CA**. These are among the best German measured points for a Water Engine check (laboratory gasoline engine, not a production map).

- **Welscher, S. et al.** *A comprehensive evaluation of water injection in the diesel engine.* *International Journal of Engine Research* 24(1):99–112, 2023 (online 6 Sep 2021). DOI 10.1177/14680874211044297. KITopen record (legitimate institutional copy): https://publikationen.bibliothek.kit.edu/1000137777 Affiliations include KIT IFKM and Universität Stuttgart (Bargende, Grill). The open Sage abstract and TRID record confirm: **562** single-cylinder points, Euro 6d passenger-car diesel derivative, **port** water injection. NOx fell; water injection had no significant effect on the combustion process as stated in the abstract. At water-to-fuel ratios of **25%, 50%, and 100%**, NOx reduction **without soot deterioration** was achieved in **62%, 40%, and 20%** of the experiments respectively. Absolute abstract figures include NOx cuts of up to about **−2.5 g/kWh** at 25% W/F in most measurements and up to about **−7.5 g/kWh** at 100% W/F in a smaller share of the data. **Correction:** Hermes’s phrase “NOx reduction up to 50% without soot penalty at W/F 25–100%” is not what the abstract says and should not be used. The 62/40/20 split and the g/kWh figures should be used instead. Full maps: cite the DOI and KITopen record; this check used the open abstract, not a pirate PDF. If a later pass needs maps, use the KIT record or author copy, not a piracy site.

- **Steinhilber, Thomas Wolfgang.** *Einfluss der Wasser- oder Emulsionseinspritzung auf die homogene Dieselverbrennung.* Dissertation, TU München, 2007. The URL Hermes gave is a real TUM Lehrstuhl PDF: https://www.epc.ed.tum.de/fileadmin/w00cgc/td/Forschung/Dissertationen/steinhilber.pdf also catalogued at https://mediatum.ub.tum.de/627702. Qualitative comparison (emulsion vs separate water injection) is plausible; detailed numbers were not re-read in this pass — mark any specific Steinhilber percentages in later use as “PDF exists, figures not re-extracted here.”

- **BMW M4 GTS hardware and official ratings**, from BMW press and the BMW M page “5 litres of water for 500 horses” (7 Oct 2015): https://www.bmw-m.com/en/topics/magazine-article-pool/5-litres-of-water-for-500-horses.html and https://www.press.bmwgroup.com/middle-east/article/detail/T0259402EN/the-new-bmw-m4-gts?language=en
  - Official: **368 kW / 500 hp**, **600 Nm**, 3.0-litre turbo in-line six, 0–100 km/h in 3.8 s, limited 305 km/h.
  - Injection: fine spray into the **intake plenum** (not in-cylinder). Three injectors in the plenum, each feeding two cylinders. Pump about **10 bar**. Five-litre tank in the boot.
  - Track use: tank topped up **every time the car is refuelled**. Everyday / fast motorway: “only needs topping up at every fifth refuelling stop.” Hermes’s “every 5 fuel tanks” matches the everyday claim only.
  - Dry tank or fault: boost reduced and spark retarded; residual water drained back to the tank at shutdown (frost).
  - Manufacturer technology claims on that page (not a published test map): intake-air temperature down by around **25°C**; “8% greater performance. 8% less consumption”; van Meel quote “at least 50 hp and 50 Newton metres more.”
  - EU-cycle fuel consumption in the later BMW press kit is **8.5 l/100 km** and **199 g/km CO2**, “at the level of the BMW M4 Coupe.” Do not treat the GTS as a measured cycle-efficiency win.

- **Bosch WaterBoost press** (open): https://www.bosch-presse.de/pressportal/de/wasser-statt-benzin-mit-dieser-innovation-spart-bosch-bis-zu-13-prozent-kraftstoff-57792.html and English https://us.bosch-press.com/pressportal/us/en/press-release-695.html Manufacturer claims: up to **4%** fuel saving in WLTC, up to **13%** when accelerating hard or on the freeway; a few hundred millilitres of water per 100 km; M4 GTS is the first production vehicle; Bosch supplies parts. Hermes reported the 4% figure and missed the 13% highway claim. These are supplier claims, not an independent map.

- **BMW M4 MotoGP Safety Car** as a precursor with water injection is supported by BMW-sourced coverage, e.g. https://www.car-engineer.com/bmw-tries-direct-water-injection-in-its-3-cylinder-gasoline-engine/ (cites BMW). Hermes was right to include it.

- **No Mercedes / VW / Audi / Porsche series-production water-injection car** as of this check: consistent with public knowledge. Keep as “nothing found,” not as a proof that no prototype exists.

## Errors and unverified claims in the Hermes draft

- **M4 GTS power and comparison:** Official is **368 kW / 500 hp** and **600 Nm**. “493 hp” is only the approximate imperial-hp conversion of 368 kW and should not replace the official figure. “+37 hp vs. M4” is **wrong** (standard F82 M4 is 317 kW / 431 hp). Torque 600 Nm was omitted.

- **“Limited 500 units”:** Not confirmed. Secondary production reports (Carscoops, CarBuzz, Dec 2016) say BMW planned 700 customer cars and built **803** customer cars (about 830 including pre-production/press). Not an official BMW press page in this check — treat the exact count as secondary — but **500 is not correct**.

- **“~4% CO2 reduction” on the GTS itself:** This is the Bosch WaterBoost WLTC claim for the technology, not a measured GTS-vs-M4 certified gain. Official GTS cycle consumption is described as at the level of the M4 Coupe. Do not use 4% as a GTS test result.

- **Alpina and Brabus “water-injection kits”:** Not supported as Alpina or Brabus factory/aftermarket products. What exists are third-party kits (e.g. Snow Performance Boost Cooler) *for* Alpina B7/B6 models. Treat Hermes’s Alpina/Brabus rows as **incorrect attribution**. No Brabus-made kit was found in this check.

- **Patent list reused under Bosch, Continental, and Mercedes** (EP2918813, EP3346120, EP3685033, EP3456951, WO2018041469, etc.): at least some of these families are **Robert Bosch GmbH** (e.g. related US 10,641,213 / US 10,378,435, assignee Bosch). They must not be counted as independent Mercedes or Continental evidence until each number is checked on a patent register. Mercedes “research patents exist” is therefore **not verified** from this list.

- **“BMW DE1020 patents” for six-stroke:** “DE1020” is only a German application-prefix fragment, not a specific patent. **Not verified.** Crower (US) and Ilmor (UK) do not belong in the German inventory except as clearly labeled foreign context.

- **MWM / MAN / MTU / Deutz “up to 80% NOx reduction”:** Hermes already marked this as secondary and not accessed. Keep as **unverified**; do not use 80% in a model.

- **Mahle “from tap to tank,” Fraunhofer ISE, DLR, WaVe project details, Blau 2026 ISBN, FVV 1256 report pages, IAV partnership:** bibliographic leads look plausible but were not all opened in this pass. Mark as **not independently verified here** except where a URL was fetched. Do not invent their numbers.

- Wikipedia / forum threads are secondary for MW50. The aviation story is real in outline; treat the “~500 hp gain” and 10-minute limit as **secondary** until a handbook or archival primary is used.

## Important German sources Hermes missed (checker-added)

- **Hoppe, F.; Thewes, M.; Baumgarten, H.; Dohmen, J.** *Water injection for gasoline engines: Potentials, challenges, and solutions.* *International Journal of Engine Research* 17(1):86–96, 2016. DOI 10.1177/1468087415599867. **Legitimate open copy** (RWTH Aachen repository, posted with permission / national licence): https://publications.rwth-aachen.de/record/567619 PDF: https://publications.rwth-aachen.de/record/567619/files/567619.pdf Also RWTH DOI 10.18154/RWTH-2016-00866. Single-cylinder, condensed-water **direct** injection plus gasoline DI, Miller + cooled EGR concept (RWTH Aachen / FEV). From that open PDF: about **3.3%–3.8%** efficiency increase near minimum BSFC (stoichiometric, Miller + cooled EGR); up to **16%** at full load; about **4.5%** near minimum BSFC when combined with homogeneous lean; Miller + condensate enough up to about **1.0 MPa BMEP** even at **CR 13.5**. Highly usable laboratory data for Water Engine. Not a production-vehicle map.

- **BMW 1 Series five-door prototype, Innovation Days 2015**, 1.5-litre three-cylinder turbo, **mostly direct in-cylinder** water injection (unlike the GTS plenum system). BMW-sourced coverage: https://www.car-engineer.com/bmw-tries-direct-water-injection-in-its-3-cylinder-gasoline-engine/ Manufacturer claims: combustion temperature down about **25°C**; compression ratio raised from **9.5:1 to 11.0:1**; up to **10%** more power and torque; up to **8%** better real-world fuel economy; lower NOx (qualitative); claimed on-board water recovery from air-conditioning condensate. These are closer in spirit to a CR-increase story than the production GTS, but they remain manufacturer “up to” claims, not an independent map.

- Hoppe / FEV SAE 2017-24-0149 (*Evaluation of the Potential of Water Injection for Gasoline Engines*) remains typically paywalled. No legitimate open copy was confirmed in this pass. Cite the bibliographic record only; **paywalled; no legitimate open copy found** for drive-cycle fuel/water-consumption numbers.

## Water Engine — what can actually be used

Usable now, with the caveats above:

| Source | Open copy | Measured or claimed | Use |
| --- | --- | --- | --- |
| Massoud 2024, TU Berlin | DepositOnce, CC BY 4.0 | +0.8 / +1.2 / +2.0 pp indicated efficiency (port 10 bar / DI 400 bar / 10% emulsion at 200 bar); CA50 8°CA | Yes — lab SI, efficiency and knock/phasing |
| Hoppe et al. 2016, RWTH/FEV | RWTH Publications PDF | +3.3–3.8% η near min BSFC; up to +16% full load; +4.5% with lean; CR 13.5 to ~1.0 MPa BMEP | Yes — lab single-cylinder SI |
| Welscher et al. 2023, KIT/Stuttgart | KITopen record + open abstract | 562 pts, port WI on Euro 6d diesel; NOx down, soot often not worse at 25% W/F (62% of tests); g/kWh figures in abstract | Yes — lab diesel NOx, not the 50% figure |
| BMW / Bosch official pages | Open press | GTS: 368 kW, 600 Nm, plenum WI, 5 L tank, ~10 bar, 25°C intake-temp claim, 8%/8% and 4%/13% manufacturer claims | Qualitative / order-of-magnitude only; not a GTS BSFC map |
| BMW 1 Series 2015 prototype | Open BMW-sourced articles | CR 9.5→11.0, up to +10% power, up to +8% real-world fuel economy (manufacturer) | Context for CR-increase, not a calibration map |

Do not use: Hermes’s +37 hp, 500-unit run, 4% as a GTS test result, 50% diesel NOx, 80% heavy-duty NOx, Alpina/Brabus kits, or the shared patent list as Mercedes/Continental proof.

## Link-check notes

Several .de institutional URLs were blocked inside box Hermes (resolved to a private/fake IP). This check re-opened BMW, Bosch, DepositOnce, KITopen, and RWTH pages from a different fetch path. Trier, Braunschweig, Magdeburg, and some FVV pages were not re-fetched here.
