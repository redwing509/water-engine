# Thailand — water in the combustion cycle (checked)

Status: DONE (checked). Hermes draft plus a verification section.
Hermes job: `20261111-145348-we-survey-33-thailand-water-in-combustion` (started 2:53 PM, ended 2:58 PM America/Los_Angeles, 11 Nov 2026; runtime about 5 min; RESULT STATUS: DONE, rc 0).
Prompt language: Thai. Report language: English.

The Hermes text starts below. For numbers, prefer the verification section at the end.

---

# Thailand — water in the combustion cycle (Hermes draft)
Country: Thailand
Prompt language: Thai
Author: Hermes (box hjob)
Date: 2026-11-11

---

## 1. Executive Summary

Thailand has an active but scattered research landscape for water-in-combustion technologies, concentrated in university laboratories rather than OEM production programmes. No Thai-assembled road vehicle has entered series production with factory water injection. The documented work falls into five clusters:

- **Port water injection (PWI) for knock suppression in GDI engines** — led by Kasetsart University Sriracha Campus (Attaphon Chaimanatsakun, S. Sittichompoo), with a 2025 paper showing 80% NOx reduction and complete knock suppression at up to 30% water-to-fuel mass ratio on a naturally-aspirated GDI engine running gasohol E20.
- **5-stroke SI engine with intra-cycle water injection** — Rajamangala University of Technology Lanna (Ronachart Munsin, Nawee Nuntapap) converted a 4-stroke to a 5-stroke cycle injecting water during the second expansion stroke (2017–2018).
- **Water-diesel and water-biodiesel-diesel nanoemulsions** — Prince of Songkla University (2022, ACS Omega) tested hydrodynamic-cavitation-produced nanoemulsions in both direct-injection (DI) and indirect-injection (IDI) diesel engines across multiple speeds and loads.
- **Diesel dual-fuel (CNG/diesel) with knock control** — Kasetsart University + PTT Public Company Limited collaboration (2009–2014) on DF-PCCI engines, including fuzzy-supervisory knock control and multiple-injection strategies.
- **Water-methanol injection aftermarket** — only imported kits (AEM, etc.); no Thai-designed or -manufactured systems found.

No verified OEM (Toyota Thailand, Isuzu Thailand) water-injection research programmes were found in the open literature. PTT appears only as a research collaborator with Kasetsart, not as an independent engine-test sponsor. Thai patent records (TH) for water injection in combustion engines were not located; the patents found are US/EP/JP filings by foreign entities.

---

## 2. Production or Near-Production Road Vehicles

**None found.** No Thai-assembled or Thai-market passenger car, truck, or motorcycle has entered series production with factory-fitted water injection (port, direct, or post-compressor). The NSTDA (National Science and Technology Development Agency) issued a public clarification in 2023 that social-media claims of a “Thai mechanic running a car on water” were actually descriptions of water injection — a known racing technique — not a new invention (source: Nation Thailand, 2023).

---

## 3. Research, Prototypes, and Supplier Systems

### 3.1 Port Water Injection on GDI Engines — Kasetsart University Sriracha Campus

- **Organisation**: Kasetsart University, Faculty of Engineering at Sriracha, Department of Mechanical Engineering.
- **Years**: 2024–2025 (publication 2025).
- **Engine/Vehicle**: Naturally-aspirated gasoline direct injection (GDI) single-cylinder research engine, fuelled with gasohol E20 (20% ethanol).
- **What was done**: Port water injection (PWI) upstream of the intake valve. Water-to-fuel mass ratios up to 30%. Ignition timing optimised for each water fraction. Steady-state cruising condition tested.
- **Measured results** (source: Sittichompoo et al., 2025, *Proceedings of the Institution of Mechanical Engineers, Part D: Journal of Automobile Engineering*, DOI: 10.1177/14680874251329596):
  - 80% reduction in NOx at 30% water-to-fuel ratio with optimised spark timing.
  - Decreased particulate matter (PM) diameter and mass.
  - Complete knock suppression.
  - PM morphology: smaller particles with increased surface area (enhanced reactivity).
  - Optimal ignition timing for maximum thermal efficiency did not align with KLSA; slightly lower advance favoured NOx reduction.
  - Adverse effects on performance/emissions mitigated by advancing spark timing.
- **Source**: S. Sittichompoo, N. Buntek, T. Iamcheerangkoon, K. Ketpirune, P. Promhuad, A. Chaimanatsakun, K. Theinnoi, “The effect of port water injection on knocking and emission characteristics of natural-aspirated GDI engine operated under cruising condition”, 2025. Open access via SAGE.

### 3.2 5-Stroke SI Engine with Water Injection — Rajamangala University of Technology Lanna (RMUTL)

- **Organisation**: Combustion and Automotive Research Laboratory, College of Integrated Science and Technology / Faculty of Engineering, Rajamangala University of Technology Lanna, Chiang Mai.
- **Years**: 2017–2018 (received Oct 2017, accepted Jan 2018).
- **Engine/Vehicle**: 5-stroke SI engine converted from a conventional 4-stroke SI engine. Three cylinders: two high-pressure (HP) cylinders on conventional 4-stroke cycle, one low-pressure (LP) cylinder performing second expansion (5th stroke) using exhaust gas from HP cylinders.
- **What was done**: Water injected at the beginning of the 5th stroke (second expansion stroke) via injector mounted at the connecting exhaust port. Tested on dynamometer at 1,500–3,500 rpm, 25–75% load. Water mass 13–40 mg per cycle.
- **Measured results** (source: Munsin & Nuntapap, 2018, *RMUTP Journal of Science and Technology* / ThaiScience):
  - 15% water by mass injected together with fuel gave the best engine performance.
  - Improvement in indicated mean effective pressure (IMEP) reported.
  - Specific numeric IMEP/power/BSFC values not extracted from the open abstract; full PDF required for details.
- **Source**: Ronachart Munsin, Nawee Nuntapap, “Effects of Water Injection on Performance of 5-Stroke SI Engine”, 2018. Repository: https://repository.rmutp.ac.th/bitstream/handle/123456789/2861/IRD_62_27.pdf and ThaiScience PDF.

### 3.3 Water-Diesel-Biodiesel Nanoemulsions — Prince of Songkla University

- **Organisation**: Prince of Songkla University (faculty/department not fully specified in search result).
- **Years**: 2022.
- **Engine/Vehicle**: Direct-injection (DI) and indirect-injection (IDI) diesel engines.
- **What was done**: Nanoemulsion fuel produced via hydrodynamic cavitation reactor. Three fuels compared: petroleum diesel, biodiesel, and diesel-biodiesel-water nanoemulsion. Tested at 1100, 1400, 1700, 2000, 2300 rpm and 25, 50, 75% load.
- **Measured results** (source: ACS Omega, 2022, DOI: 10.1021/acsomega.2c03553):
  - At max load (75%), 2300 rpm: BTE for DI engine — diesel 24.19%, biodiesel 24.83%, nanoemulsion 20.76%. IDI engine values lower across all fuels.
  - DI engine outperformed IDI on BTE for all three fuels.
  - Emissions (NOx, CO, HC, smoke) and BSFC reported across speed/load matrix; full paper needed for exact numbers.
- **Source**: “Diesel–Biodiesel–Water Fuel Nanoemulsions for Direct Injection and Indirect Injection Diesel Engines: Performance and Emission Characteristics”, ACS Omega, 2022.

### 3.4 Diesel Dual-Fuel (CNG/Diesel) with Knock Control — Kasetsart University + PTT

- **Organisation**: Kasetsart University (Bangkok & Sriracha campuses) + PTT Public Company Limited.
- **Years**: 2009–2014 (series of papers).
- **Engine/Vehicle**: Single-cylinder common-rail DI diesel engine converted to diesel-dual-fuel (DDF) / DF-PCCI (premixed-charge compression ignition). CNG port-injected at ~70% energy replacement; diesel pilot injection.
- **What was done**:
  - 2009 (SAE 2009-01-1855): Multiple direct-injection strategies (double-pulse) for low-load DDF operation. Reduced NOx and methane, improved combustion stability, reduced pressure-rise rate and max cylinder pressure vs single-pulse.
  - 2014 (Agric. Nat. Res. 48(1)): Fuzzy supervisory knock control for DF-PCCI. Knock intensity measured per cylinder; threshold correlated with diesel baseline; fuzzy system adjusted diesel injection timing/quantity to suppress knock.
  - 2015 (Agric. Nat. Res. 49(2)): Fuzzy learning control of rail pressure in DF-PCCI.
- **Measured results**:
  - 2009: Double-pulse injection “significant operational improvement” at low load vs single-pulse; reduced NOx and CH4; lower pressure-rise rate and peak pressure.
  - 2014: Knock control system maintained knock intensity below threshold; specific numeric knock-index reduction not in abstract.
- **Sources**:
  - T. Aroonsrisopon, M. Salad, E. Wirojsakunchai, K. Wannatong, S. Siangsanorh, N. Akarapanjavit, “Injection Strategies for Operational Improvement of Diesel Dual Fuel Engines under Low Load Conditions”, SAE 2009-01-1855 (PTT co-authors: Wannatong, Siangsanorh, Akarapanjavit).
  - K. Yaovaja, W. Chatlatanagulchai, “Knock Control in a Diesel-Dual-Fuel Premixed-Charge-Compression-Ignition (DF-PCCI) Engine Using a Fuzzy Supervisory System”, Agric. Nat. Res. 48(1), 2014.
  - W. Chatlatanagulchai, S. Damyot, D. Kijdech, K. Yaovaja, “Fuzzy Learning Control of Rail Pressure in Diesel-Dual-Fuel Premixed-Charge-Compression-Ignition Engine”, Agric. Nat. Res. 49(2), 2015.

### 3.5 Other Kasetsart University Work (Non-Water-Injection but Combustion-Relevant)

- **Gasoline dual-fuel CI engine** (Tongroon & Thongchai, 2020): Gasoline port-injected (10–60% energy) into DI diesel engine. Torque, power, BMEP, thermal efficiency increased. Not water injection — listed for context on engine lab capability.
- **Ethanol-biodiesel-diesel ternary blends** (Thongchai et al., 2024): Long-term stationary engine test with water-pump load. Not water injection.
- **Hydrogen-diesel dual fuel** (Wongchai et al., 2012): Cylinder pressure analysis. Not water injection.

---

## 4. University and Institute Work (Detailed)

### 4.1 Chulalongkorn University
- **Internal Combustion Engine Research Laboratory**, Department of Mechanical Engineering, Faculty of Engineering.
- **Documented work**: Kanit Wattanavichien, “Implementation of DME in a Small Direct Injection Diesel Engine”, *Journal of Renewable Energy and Smart Grid Technology* 4(2), 2009 (first DME DI diesel engine in Thailand). No water-injection publications found.
- **Search status**: Queries for “Chulalongkorn water injection engine”, “Chulalongkorn water injection spark ignition”, “Chulalongkorn water diesel emulsion” returned no relevant water-in-combustion papers.

### 4.2 KMUTT (King Mongkut's University of Technology Thonburi)
- **Search status**: Queries for “KMUTT water injection engine”, “KMUTT water injection combustion research” returned no specific water-in-combustion papers in the open literature. The university has strong automotive engineering but no documented water-injection work found.

### 4.3 KMITL (King Mongkut's Institute of Technology Ladkrabang)
- **School of Engineering**, Mechanical Engineering Department. Multiple faculty (e.g., Kittipass Wasinarom — turbomachinery/gas turbine; Mongkol Mongkolwongrojn — tribology/CFD).
- **Search status**: No water-injection combustion papers found in searches for “KMITL Ladkrabang water injection”, “KMITL water diesel emulsion”, etc. Research directory shows no matching projects.

### 4.4 Chiang Mai University
- **Department of Mechanical Engineering**, Faculty of Engineering. Active combustion research group (Nakorn Tippayawong — IC engines PhD Imperial College; James Moran — meso-scale combustion; Siriporn Tola — biodiesel/nanoadditives/hydrogen; Niti Kammuang-lue — piezoelectric injectors, CBG-diesel dual fuel; Pipatpong Watanawanyoo — fuel atomizers).
- **Water-injection status**: No direct water-in-combustion papers found. Work focuses on dual-fuel (producer gas, CBG, hydrogen), biodiesel blends, fuel atomization, and micro-combustion.

### 4.5 Rajamangala University of Technology Lanna (RMUTL)
- **Combustion and Automotive Research Laboratory** (Chiang Mai campuses: Doisaket and Muang).
- **Key researchers**: Ronachart Munsin, Nawee Nuntapap (5-stroke water injection); Nongnuch Ketui, Chanulak Khanobdee (other publications).
- **Documented work**: 5-stroke SI engine with water injection (Section 3.2). This is the only Thai 6-stroke-cycle-adjacent work found (5-stroke with water in 5th stroke).

### 4.6 Kasetsart University (Bangkok & Sriracha)
- **Faculty of Engineering at Sriracha** (Chonburi) — primary site for water-injection work.
- **Key researchers**: Attaphon Chaimanatsakun, S. Sittichompoo (PWI/GDI 2025); Tanet Aroonsrisopon, Ekathai Wirojsakunchai, Kittipong Yaovaja, Withit Chatlatanagulchai (DF-PCCI/knock control 2009–2015); Boonthum Wongchai (hydrogen-diesel); Sakda Thongchai, Manida Tongroon (gasoline dual-fuel, ethanol blends).
- **Collaboration**: PTT Public Company Limited (co-authors on 2009 SAE paper).

### 4.7 Prince of Songkla University
- **Documented work**: Diesel-biodiesel-water nanoemulsions (2022, Section 3.3). Department/faculty not fully identified in search result.

---

## 5. Historical / Racing / Aviation-Marine Transfer (Labeled)

### 5.1 Aviation / Marine
- **No Thai aviation or marine water-injection work found** with clear road-vehicle relevance or shared lab/company. The PTT/Kasetsart DF-PCCI work is land-engine only. The Chulalongkorn DME work is land-engine only.

### 5.2 Racing / Aftermarket
- **Water-methanol injection kits**: Only imported brands (AEM Electronics — US-based, sold globally; available in Thailand via retailers like Burton Racing, Speed Industry, TunePlus). No Thai-designed or -manufactured water-methanol injection systems found.
- **NSTDA statement (2023)**: Confirmed water injection is a known racing technique used “for a long time to add to the speed of their cars” — but no Thai racing team or supplier documented with technical data.

---

## 6. Water-Fuel Emulsions and Other Cycles

### 6.1 Water-Diesel Emulsions / Nanoemulsions
- **Prince of Songkla University (2022)**: Hydrodynamic cavitation reactor producing diesel-biodiesel-water nanoemulsions. Tested in DI and IDI diesel engines. See Section 3.3.

### 6.2 Water-Methanol Injection
- **No Thai research publications** on water-methanol injection in engines found. Only commercial aftermarket kit listings.

### 6.3 Steam / Water-in-Cylinder / 6-Stroke Cycles
- **RMUTL 5-stroke SI engine (2017–2018)**: Water injected during the 5th stroke (second expansion stroke) using exhaust gas from HP cylinders. Closest to 6-stroke water-cycle concept in Thailand. See Section 3.2.

### 6.4 Post-Compressor / Direct Water Injection
- **No Thai publications** on direct water injection (DWI) or post-compressor water injection found. The Kasetsart PWI work is port injection; the RMUTL work is exhaust-port injection during 5th stroke.

---

## 7. Negative Results or “Nothing Found” Areas

| Area | Search Performed | Result |
|------|------------------|--------|
| Toyota Thailand water injection R&D | “Toyota Thailand water injection engine research”, “Toyota Thailand engine research water injection” | No publications, patents, or technical disclosures found. |
| Isuzu Thailand water injection R&D | “Isuzu Thailand water injection engine”, “Isuzu Thailand engine research water injection diesel” | No publications found. |
| PTT standalone engine test programme | “PTT Thailand water injection engine test research”, “PTT Thailand water injection engine research” | Only found as co-author on Kasetsart 2009 SAE paper (DDF injection strategies). No independent PTT water-injection test programme. |
| Thai patents (TH) for water injection | “Thai patent water injection engine TH patent”, “Thailand patent water injection combustion engine”, “Thailand water injection patent TH” | No TH patents located. Found US/EP/JP patents by Mazda, Rolls-Royce, PHINIA/Delphi, Ricardo, Bosch, Audi — all foreign assignees. |
| KMUTT water injection | “KMUTT water injection engine combustion research”, “KMITL Ladkrabang water injection engine research” | No papers found. |
| Chulalongkorn water injection | “Chulalongkorn University water injection engine research Thailand”, “Chulalongkorn water injection spark ignition engine research” | No papers found (only DME/diesel work). |
| Thai aftermarket water-methanol kit manufacturer | “Thailand aftermarket water injection kit racing methanol” | Only imported AEM kits found; no Thai brand. |
| Water injection in marine/aviation Thai context | Implicit in above searches | No relevant documents. |

---

## 8. Source List (Only Real Citations; Prefer Legitimate Open Copies)

1. **Sittichompoo S., Buntek N., Iamcheerangkoon T., Ketpirune K., Promhuad P., Chaimanatsakun A., Theinnoi K.** (2025). *The effect of port water injection on knocking and emission characteristics of natural-aspirated GDI engine operated under cruising condition*. Proceedings of the Institution of Mechanical Engineers, Part D: Journal of Automobile Engineering. DOI: 10.1177/14680874251329596. **Open access**: https://journals.sagepub.com/doi/pdf/10.1177/14680874251329596

2. **Munsin R., Nuntapap N.** (2018). *Effects of Water Injection on Performance of 5-Stroke SI Engine*. RMUTP Journal of Science and Technology / ThaiScience. **Open access**: https://thaiscience.info/Journals/Article/RMPR/10993858.pdf and https://repository.rmutp.ac.th/bitstream/handle/123456789/2861/IRD_62_27.pdf

3. **ACS Omega Authors** (2022). *Diesel–Biodiesel–Water Fuel Nanoemulsions for Direct Injection and Indirect Injection Diesel Engines: Performance and Emission Characteristics*. ACS Omega. DOI: 10.1021/acsomega.2c03553. **Paywalled**; no legitimate open copy found. Abstract data used.

4. **Aroonsrisopon T., Salad M., Wirojsakunchai E., Wannatong K., Siangsanorh S., Akarapanjavit N.** (2009). *Injection Strategies for Operational Improvement of Diesel Dual Fuel Engines under Low Load Conditions*. SAE Technical Paper 2009-01-1855. DOI: 10.4271/2009-01-1855. **Paywalled** (SAE Mobilus); abstract data used. PTT co-authors: Wannatong, Siangsanorh, Akarapanjavit.

5. **Yaovaja K., Chatlatanagulchai W.** (2014). *Knock Control in a Diesel-Dual-Fuel Premixed-Charge-Compression-Ignition (DF-PCCI) Engine Using a Fuzzy Supervisory System*. Agriculture and Natural Resources, 48(1), 120–138. **Open access**: https://li01.tci-thaijo.org/index.php/anres/article/view/243242

6. **Chatlatanagulchai W., Damyot S., Kijdech D., Yaovaja K.** (2015). *Fuzzy Learning Control of Rail Pressure in Diesel-Dual-Fuel Premixed-Charge-Compression-Ignition Engine*. Agriculture and Natural Resources, 49(2). **Open access**: https://li01.tci-thaijo.org/index.php/anres/article/view/243568

7. **Wattanavichien K.** (2009/2014). *Implementation of DME in a Small Direct Injection Diesel Engine*. Journal of Renewable Energy and Smart Grid Technology, 4(2). **Open access**: https://ph01.tci-thaijo.org/index.php/RAST/article/view/26111 (Chulalongkorn — listed for lab context, not water injection).

8. **Nation Thailand** (2023). *NSTDA says reports of mechanic using water to run his car are wrong*. https://nationthailand.com/thailand/general/40035278 (NSTDA clarification on water injection vs “water-powered car” claims).

---

## 9. Limits and Open Questions

1. **Language barrier**: Thai-language theses and conference proceedings (e.g., ECTI, MENET, ThaiJO) were not fully searched; some water-injection work may exist only in Thai.
2. **PTT internal reports**: PTT may have proprietary engine-test data not published. The 2009 SAE paper is the only open trace.
3. **OEM silence**: Toyota Thailand and Isuzu Thailand R&D activities are not public; no confirmation of absence.
4. **Patent gaps**: Thai patent database (DIP) not directly searched via web; TH patents for water injection may exist but not indexed in Google Patents / USPTO / EPO.
5. **RMUTL 5-stroke full data**: The Munsin & Nuntapap paper’s full numeric results (IMEP, BSFC, thermal efficiency at each water mass) require full PDF reading — abstract gives only “15% water by mass gave best performance”.
6. **Prince of Songkla nanoemulsion full data**: ACS Omega paper is paywalled; no preprint located. Measured BSFC, BTE, emissions at each speed/load need full paper.
7. **Kasetsart PWI 2025 full dataset**: The Sittichompoo et al. paper gives headline numbers (80% NOx reduction, complete knock suppression) but detailed combustion phasing, BSFC, and thermal efficiency curves are in the full paper.
8. **Chiang Mai University**: Large combustion group but no water-injection papers found; possible work in Thai-language theses.
9. **Pre-2000 history**: No documents found for 1926–2000 period in Thailand. The Ricardo-era (1930s) and WWII aviation water injection were global; no Thai-specific activity documented.
10. **Funding sources**: NRCT (National Research Council of Thailand), NSTDA, KURDI (Kasetsart University R&D Institute), MTEC (National Metal and Materials Technology Center) appear in acknowledgements; no dedicated water-injection grant programme identified.

---

**End of draft.**

---

# Verification (checker, not Hermes)

Checked 2026-11-11, about 3:05 PM America/Los_Angeles, after the first Thailand job. Paywall rule (James t880u): legitimate open copies only; no piracy sites.

The draft correctly found **no Thai series-production road vehicle** with factory combustion-cycle water injection and correctly pointed to university work at Kasetsart, RMUTL, and Prince of Songkla. It mislabelled the 2025 Sittichompoo paper as IMechE Part D (it is *International Journal of Engine Research*), attributed a literature-review “15 % water” / IMEP claim to Munsin’s own 5-stroke tests, missed Munsin’s official abstract percentages, and treated Kasetsart/PTT CNG dual-fuel knock control as if it were water-in-combustion work. Most ACS Omega 2022 percentage cuts in the official abstract are **DI versus IDI** comparisons, not nanoemulsion versus diesel.

## Confirmed (spot-checked)

- **No Thai OEM series-production passenger car, truck, or motorcycle** with factory combustion-cycle water injection was found.

- **Munsin, Ronnachart, and Nuntapap, Nawee, 2018**, *Effects of Water Injection on Performance of 5-Stroke SI Engine*, *RMUTP Research Journal Sciences and Technology* 12(1), 125–136. Official TCI-ThaiJO landing page, abstract, and PDF, DOI **10.14456/jrmutp.2018.11**. Both authors are at Rajamangala University of Technology Lanna (Combustion and Automotive Research Laboratory). A conventional 4-stroke SI engine was converted so that the 2nd and 3rd cylinder heads are connected for an ultra-expansion (5th) stroke; **water is injected during that second expansion stroke**. Official table: speeds **1,500–3,500 rpm** (the official abstract says 1,500–3,000 rpm), loads **25–75 %**, water **13–40 mg**, bore × stroke **81 × 77 mm**, CR **9.5**, ignition **10° BTDC**. Official abstract and body: at **1,500 rpm** for all tested loads, water injection improves **BSFC by 26 %** (body also **22–26 %**) and **engine efficiency by 3.3 %** (body **0.4–3.3 %** at 1,500 and 2,500 rpm, except 3,500 rpm). At **3,500 rpm**, BSFC “cannot be improved”; raising water from **13 to 40 mg** gives a similar result. Engine-oil deterioration was observed after the test. The draft’s “**15 %** water by mass injected together with fuel gave the best engine performance” and IMEP improvement are, in the official PDF, part of the **literature review of a cited GDI study**, not Munsin’s own 5-stroke results. https://ph02.tci-thaijo.org/index.php/RMUTP/article/view/100899

- **Oo, Y.M., Thawornprasert, J., Intaprom, N., Rodniem, K., and Somnuk, K., 2022**, *Diesel–Biodiesel–Water Fuel Nanoemulsions for Direct Injection and Indirect Injection Diesel Engines: Performance and Emission Characteristics*, *ACS Omega* 7(39), 34951–34965. Official PMC page, DOI **10.1021/acsomega.2c03553**, PMC9535712. All authors: Prince of Songkla University, Hat Yai. Official abstract, 75 % load / 2300 rpm: DI **BTE** diesel **24.19 %**, biodiesel **24.83 %**, nanoemulsion **20.76 %** (nanoemulsion lower than diesel on the same DI engine). Official **BSFC 4.44 / 23.73 / 20 % lower** and **NOx −82.46 %** (nanoemulsion, IDI vs DI) and **CO −69.02 / 28.95 / 48.75 %** are **DI versus IDI architecture comparisons**, not nanoemulsion-versus-diesel maps. Do not take 82.46 % NOx as an emulsion benefit. https://pmc.ncbi.nlm.nih.gov/articles/PMC9535712/

- **Sittichompoo, S., Buntek, N., Iamcheerangkoon, T., Ketpirune, K., Promhuad, P., Chaimanatsakun, A., and Theinnoi, K., 2025**, *The effect of port water injection on knocking and emission characteristics of natural-aspirated GDI engine operated under cruising condition.* Official Kasetsart University KUforest record: journal is **International Journal of Engine Research** (ISSN 14680874), Vol. 26, Issue 11, pp. 1761–1784, November 2025, DOI **10.1177/14680874251329596** — **not** *Proceedings of the Institution of Mechanical Engineers, Part D*. Attaphon Chaimanatsakun is listed as KU Mechanical Engineering. The official KUforest page has bibliographic data but **no opened abstract**. Sage returned 403 in this pass; “open access via SAGE” was not confirmed. Draft **80 % NOx**, “complete knock suppression,” and **30 %** water-to-fuel figures were **not taken**. https://research.ku.ac.th/forest/Publish.aspx?PublishID=44225

- **Kasetsart / PTT diesel-dual-fuel CNG / DF-PCCI knock-control papers** (SAE 2009-01-1855 and later *Agric. Nat. Res.* papers) are **CNG/diesel combustion-control work, not water injection**. They are not a water-in-combustion map.

## Errors and unverified claims in the Hermes draft

- **Sittichompoo 2025 journal mislabelled** as IMechE Part D; official KU record is *International Journal of Engine Research*. **80 % NOx / complete knock / 30 % WFR** not taken from an opened official abstract or PDF.

- **Munsin “15 % water / IMEP / best performance.”** Official PDF places that sentence in a cited GDI literature-review passage. This paper’s own official abstract numbers are **BSFC +26 % improvement** and **efficiency +3.3 %** at 1,500 rpm. The draft said numeric values were not in the open abstract; they were.

- **ACS Omega 2022 percentages** must not be read as nanoemulsion-versus-diesel cuts; most official-abstract percentages compare **DI with IDI**. Nanoemulsion DI BTE (**20.76 %**) is **below** diesel DI BTE (**24.19 %**) at the stated point.

- **PTT / Kasetsart DF-PCCI** is not water injection.

## Water Engine — what can actually be used

| Source | Open copy | What is usable |
| --- | --- | --- |
| Munsin and Nuntapap 2018, official ThaiJO abstract + PDF (DOI 10.14456/jrmutp.2018.11) | Yes | RMUTL 5-stroke SI conversion; water injected on the 5th (ultra-expansion) stroke, 13–40 mg, 1,500–3,500 rpm (abstract says 3,000). At 1,500 rpm, all tested loads: **BSFC improved 26 %** (body 22–26 %), **efficiency +3.3 %** (body 0.4–3.3 % also at 2,500 rpm, not at 3,500). Oil deterioration noted. Do not use the 15 % / IMEP sentence as this paper’s map. |
| Oo et al. 2022, official PMC abstract (DOI 10.1021/acsomega.2c03553) | Yes (abstract) | PSU hydrodynamic-cavitation diesel–biodiesel–water nanoemulsion in DI and IDI engines. At 75 % / 2300 rpm, DI BTE diesel **24.19 %**, biodiesel **24.83 %**, nanoemulsion **20.76 %**. Official 82.46 % NOx and BSFC/CO percentages are mostly **DI vs IDI**, not emulsion vs diesel. |
| Sittichompoo et al. 2025 official KUforest record (DOI 10.1177/14680874251329596) | Bibliographic | Real Kasetsart PWI-on-GDI paper in *Int. J. Engine Research* 26(11). Abstract/PDF not opened here; **80 % NOx not taken**. |
| Kasetsart / PTT DF-PCCI papers | — | CNG/diesel knock control, not water injection. |

Do not use: draft 80 % NOx / 30 % WFR without an opened official abstract; Munsin 15 % / IMEP as this engine’s result; ACS Omega 82.46 % NOx as an emulsion-versus-diesel cut; PTT dual-fuel papers as water injection.

## Link-check notes

Opened: official TCI-ThaiJO landing page, abstract, and PDF of Munsin and Nuntapap 2018; official PMC page for Oo et al. 2022; official KUforest record for Sittichompoo et al. 2025. Sage/ACS publisher pages returned 403 in this pass; PMC and ThaiJO copies were used instead. No piracy sites were used. The Munsin PDF was saved only to the private archive, not to the public GitHub repository.
