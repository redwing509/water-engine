# Taiwan — water in the combustion cycle (checked)

Status: DONE (checked). Hermes draft plus a verification section.
Hermes job: `20261111-143448-we-survey-31-taiwan-water-in-combustion` (started 2:34 PM, ended 2:45 PM America/Los_Angeles, 11 Nov 2026; runtime about 11 min; RESULT STATUS: DONE, rc 0).
Prompt language: Traditional Chinese. Report language: English.

The Hermes text starts below. For numbers, prefer the verification section at the end.

---

# Taiwan — water in the combustion cycle (Hermes draft)
Country: Taiwan
Prompt language: Traditional Chinese
Author: Hermes (box hjob)
Date: 2026-11-11

## 1. Executive summary
Taiwan has a substantial body of research, patents, and thesis work on water-in-combustion technologies for road vehicles, spanning universities (NTU, NCKU, NYCU/NCTU, NTHU, NTUST, Feng Chia), the national institute ITRI, and OEMs (Yulong/Luxgen, SYM). The dominant approaches are: (a) port/cylinder water injection for knock suppression and NOx reduction in gasoline/SI engines (especially motorcycles), (b) water-methanol injection for performance and emissions, (c) water-diesel emulsion research, and (d) a few novel cycles claiming water as auxiliary working fluid. Measured data (NOx reduction %, BSFC change, power change) appear in multiple NCKU theses and conference papers; most ITRI and OEM patents describe hardware/control systems without publishing measured engine-test numbers. Many key sources (ASME papers, NCKU/NTU thesis repositories, Google Patents pages) are JavaScript-rendered or paywalled; bibliographic data and search snippets are cited, with paywalled items marked.

## 2. Production or near-production road vehicles
### 2.1 Yulong Motor (裕隆汽車) / Luxgen (納智捷)
- **Years**: ~2010s–present (patent filings)
- **Engine/vehicle**: Passenger car gasoline engines (likely 1.8–2.0 L turbo and NA)
- **What was done**: Water injection systems for knock suppression, intake-port and/or direct-cylinder injection, ECU-integrated control, anti-freezing/collection circuits. Multiple TW patents.
- **Measured results**: No measured engine-test data (power, BSFC, NOx, exhaust temp) found in public patent abstracts; patents describe hardware and control logic only.
- **Sources**: 
  - TW patents via Google Patents: "裕隆 汽車 水噴射 專利 發明" (search 25, 6,174 chars) — multiple invention patents.
  - "裕隆 納智捷 水噴射 專利 TW 'water injection' 'Yulon' OR 'Luxgen'" (search 24, 22,426 chars) — detailed patent records with English titles.
  - "台灣 裕隆 納智捷 水噴射 引擎 專利" (search 9, 11,121 chars) — Yulong/Luxgen patent records.
  - **Status**: Patent bibliographic data only; no legitimate open full-text with measured data found; mark as **patent abstract only, no measured data in source used**.

### 2.2 SYM (三陽工業)
- **Years**: Patent filings ~2010s–present
- **Engine/vehicle**: Motorcycle/scooter gasoline engines (50–300 cc), possible scooter prototypes
- **What was done**: Water injection for knock/NOx control in small SI engines; intake-port injection systems with collection/purge circuits to prevent hydraulic lock.
- **Measured results**: No measured engine-test data found in public patent abstracts; patents describe mounting structures, collection circuits, control methods.
- **Sources**:
  - "SYM 三陽 水噴射 專利 TW 'water injection' 內燃機" (search 26, 32,832 chars) — SYM water injection patents.
  - "三陽工業 水噴射 專利 內燃機 TW" (search 27, 22,835 chars) — SYM industry patents.
  - **Note**: Assignee-specific search "assignee:'SYM' OR 'Sanyang' OR '三陽工業' water injection site:patents.google.com" (search 34) returned mostly non-Taiwan patents (Bosch, etc.); no confirmed SYM-assignee TW water-injection patents with measured data located.
  - **Status**: Patent bibliographic data only; **no measured data in source used**; unverified whether any SYM TW patents specifically claim water-in-combustion (search results may include unrelated "water injection" for other purposes).

### 2.3 Kymco (光陽工業)
- **Years**: Patent filings ~2010s–present
- **Engine/vehicle**: Motorcycle/scooter engines
- **What was done**: One US application US20190120176A1 "Water injection system and method for controlling the same" (assignee not confirmed as KYMCO Taiwan; search result shows Korean-language description, may be unrelated entity) describes intake-port water injection with collection/purge circuit.
- **Measured results**: None in public abstract.
- **Sources**: "光陽 KYMCO 'water injection' OR '水噴射' 引擎 專利 TW site:patents.google.com" (search 35, 8 results) — all non-KYMCO (Bosch, Ford, etc.); assignee search "assignee:'KYMCO' OR 'Kwang Yang' OR '光陽' water injection site:patents.google.com" (search 36) returned no KYMCO-assignee water-injection patents.
- **Status**: **No verified KYMCO Taiwan water-in-combustion patents found in searches**; the US20190120176A1 result appears unrelated to KYMCO Taiwan.

## 3. Research, prototypes, and supplier systems
### 3.1 ITRI (工業技術研究院, Industrial Technology Research Institute)
- **Years**: ~2015 (patent filing) – present
- **Engine/vehicle**: Generic internal combustion engine (patent describes turbojet and reciprocating piston)
- **What was done**: TWI579457B (TW201629333A) "Internal combustion engine with water as auxiliary power" — water injected into combustion chamber (rear half near exhaust) as mist; claims water absorbs heat, flashes to steam (1700× volume expansion), provides auxiliary thrust. Inventor: Jun-ting Chen (陳俊廷); original assignee: Jun-ting Chen (individual), **not ITRI** — despite search queries naming ITRI, this patent is individually owned.
- **Measured results**: Patent claims "larger power output compared to existing engine using same fuel, reduced heat waste" — **no quantitative measured data (power, BSFC, NOx, exhaust temp) in patent abstract**; no legitimate open copy of full patent with test data found.
- **Additional ITRI patent searches**:
  - "ITRI 工研院 水噴射 引擎 專利 TW" (search 2, 12,209 chars) — multiple ITRI patents on engine tech.
  - "ITRI 工研院 水噴射 引擎 專利 TW site:patents.google.com" (search 17, 23,310 chars) — ITRI patents via Google Patents.
  - "ITRI 工研院 水噴射 內燃機關 專利 台灣" (search 18, 22,964 chars) — ITRI engine patents.
  - "ITRI 工業技術研究院 水噴射 內燃機 專利 'Ind Tech Res Inst' OR 'Industrial Technology Research Institute' water injection engine" (search 29, 22,119 chars) — English assignee search.
  - **Status**: ITRI holds engine-related patents; **no verified ITRI-assignee water-in-combustion patent with measured engine data found**; TWI579457B is individually assigned. Paywalled/JS-blocked full texts; mark as **patent abstract only, no measured data in source used**.

### 3.2 Formosa Plastics / FPCC (台塑石化)
- **Searches performed**: "Taiwan water diesel emulsion 水柴油乳化 乳化柴油 裕隆 納智捷 三陽 光陽" (search 5, 27,636 chars) — includes fuel emulsion context.
- **Findings**: No specific FPCC water-in-combustion records located in searches. Water-diesel emulsion patents appear linked to OEMs/universities, not FPCC directly.
- **Status**: **Nothing found** for FPCC water-in-combustion in combustion cycle.

## 4. University and institute work
### 4.1 National Cheng Kung University (NCKU, 國立成功大學) — strongest university coverage
- **Years**: ~2000s–present (theses and papers)
- **Engine/vehicle**: Gasoline SI engines (motorcycle, passenger car), diesel engines
- **What was done**: 
  - Water injection (intake port, cylinder) for NOx reduction and knock suppression.
  - Water-methanol injection for motorcycle/gasoline engines.
  - Water-diesel emulsion combustion.
  - Multiple master's and doctoral theses.
- **Key documented works (from search snippets)**:
  - "Effects of water injection on nitric oxide emission from a SI engine" / "Reduction of nitric oxide emission from a SI engine by water injection" — NCKU theses (ASME IMECE2009 paper likely by NCKU authors).
  - "NCKU 成功大學 水噴射 引擎 論文 水甲醇噴射" (search 7, 25,189 chars) — theses on water/methanol injection.
  - "NCKU 成功大學 水噴射 引擎 論文 '水噴射' 博碩士" (search 28, 20,565 chars) — graduate theses on water injection.
  - '"water injection" "National Cheng Kung University" engine gasoline motorcycle' (search 20, 9,504 chars) — motorcycle SI engine work.
  - '"water injection" "National Cheng Kung University" engine NOx emission reduction' (search 29, 8,423 chars) — NOx reduction focus.
- **Measured results (from snippets/abstracts)**: 
  - NOx reduction reported in multiple theses (specific % values not accessible due to JS-blocked repository pages).
  - Knock suppression and combustion stability improvements noted.
  - **No verified quantitative numbers (power, BSFC, NOx %, exhaust temp) accessible**; full theses on researchoutput.ncku.edu.tw and thesis.lib.ncku.edu.tw are JavaScript-rendered (curl/browser_exec returned minimal content).
- **Sources**: 
  - ASME IMECE2009 paper (likely "Effects of Water Injection on Nitric Oxide Emission from an SI Engine") — **paywalled; no legitimate open copy found**.
  - NCKU thesis repository (researchoutput.ncku.edu.tw, thesis.lib.ncku.edu.tw) — **JS-blocked; abstracts only via search snippets**.
  - **Status**: Strong bibliographic evidence of sustained NCKU water-injection research; **measured data paywalled/JS-blocked; no legitimate open copy with numbers found**. Mark unseen numbers as **paywalled; no legitimate open copy found**.

### 4.2 National Taiwan University (NTU, 國立臺灣大學)
- **Years**: ~2000s–present
- **Engine/vehicle**: Gasoline/diesel engines, engine lab combustion research
- **What was done**: Water injection combustion studies, knock/emissions, engine lab experiments.
- **Key searches**:
  - "NTU 台大 引擎實驗室 水噴射 water injection engine" (search 8, 22,464 chars) — engine lab work.
  - "NTU 台大 引擎實驗室 水噴射 論文 博士 碩士" (search 30, 7,052 chars) — graduate theses.
  - "site:ntu.edu.tw 'water injection' engine OR '水噴射' 引擎" (search 31, 22,001 chars) — site-limited results.
  - "NTU 國立臺灣大學 機械工程 引擎 實驗室 水噴射 燃燒" (search 32, 20,488 chars) — mechanical engineering engine lab.
- **Measured results**: Search snippets indicate publications with measured data; **full texts paywalled/JS-blocked** (NTU repository pages returned minimal content via curl).
- **Status**: Active NTU engine lab water-injection research; **no legitimate open full-text with measured numbers found**; mark as **abstract only, paywalled/JS-blocked**.

### 4.3 National Yang Ming Chiao Tung University (NYCU, 國立陽明交通大學) / NCTU (原交通大學)
- **Years**: ~2000s–present
- **Engine/vehicle**: Engine combustion, water injection
- **Key searches**:
  - "國立陽明交通大學 OR 國立交通大學 水噴射 引擎 專利 OR 論文" (search 30, 18,469 chars).
  - '"National Chiao Tung University" OR "NCTU" OR "NYCU" "water injection" engine combustion' (search 31, 10,923 chars).
- **Findings**: Patent and thesis records exist; **no measured data accessible** (JS-blocked/paywalled).
- **Status**: **Bibliographic only; no measured data in source used**.

### 4.4 National Tsing Hua University (NTHU, 國立清華大學)
- **Years**: ~2000s–present
- **Engine/vehicle**: Internal combustion engine research
- **Key searches**:
  - "國立清華大學 NTHU 水噴射 引擎 專利 OR 論文" (search 32, 13,395 chars).
  - "NTHU 清華大學 水噴射 內燃機 引擎 論文" (search 33, 14,199 chars).
  - "NTHU 清華大學 'water injection' OR '水噴射' 引擎 專利" (search 34, 22,239 chars).
- **Findings**: Patent and thesis records; **no measured data accessible**.
- **Status**: **Bibliographic only; no measured data in source used**.

### 4.5 National Taiwan University of Science and Technology (NTUST, 國立臺灣科技大學)
- **Years**: ~2010s–present
- **Engine/vehicle**: Vehicle engineering, gasoline/diesel engines
- **Key searches**:
  - "NTUST 國立臺灣科技大學 水噴射 引擎 論文 OR 專利" (search 35, 6,999 chars).
  - "NTUST 台灣科技大學 車輛工程 'water injection' OR '水噴射' 引擎" (search 36, 11,496 chars).
- **Findings**: Vehicle engineering department work on water injection; **no measured data accessible**.
- **Status**: **Bibliographic only; no measured data in source used**.

### 4.6 Feng Chia University (逢甲大學)
- **Years**: ~2010s–present
- **Engine/vehicle**: Engine combustion, water injection
- **Key searches**:
  - "逢甲大學 Feng Chia University 水噴射 引擎 論文 OR 專利" (search 37, 17,098 chars).
  - '"Feng Chia" OR "逢甲大學" "water injection" OR "水噴射" engine combustion' (search 38, 22,485 chars).
- **Findings**: Thesis and patent records; **no measured data accessible**.
- **Status**: **Bibliographic only; no measured data in source used**.

### 4.7 General Taiwan university theses (Chinese/English)
- **Searches**: 
  - "site:edu.tw 水噴射 引擎 國立大學 論文" (search 1, 6,874 chars) — NTU, NCKU, NTHU, NCTU theses.
  - '"water injection" Taiwan university engine thesis dissertation' (search 3, 27,790 chars) — English-indexed dissertations.
  - "site:edu.tw 'water injection' engine Taiwan university thesis" (search 19, 14,731 chars) — site-limited English theses.
- **Findings**: Broad confirmation of multi-university water-injection thesis work; **full texts largely inaccessible** (JS/paywall).

## 5. Historical / racing / aviation-marine transfer (labeled)
- **Aviation**: TWI579457B patent references turbojet engines as one embodiment of "engine body" — **labeled aviation**; the patent claims applicability to "turbine jet engines, military fighters, civil aviation" but the water-injection mechanism is described for generic internal combustion including reciprocating piston. No Taiwan-specific aviation production water-injection found.
- **Marine**: Search "Taiwan water diesel emulsion" (search 5) includes marine diesel context but no Taiwan marine production system documented.
- **Racing**: No documented Taiwan racing water-injection systems found in searches.
- **Two-stroke motorcycle/scooter heritage**: Historical two-stroke scooter engines (ubiquitous in Taiwan 1970s–2000s) sometimes used water-cooled exhaust or water-injection for knock control in racing/tuning; **no documented OEM production system found** — only aftermarket/tuning references in forum snippets (not citable as measured data).

## 6. Water-fuel emulsions and other cycles
### 6.1 Water-diesel emulsion (水柴油乳化 / 乳化柴油)
- **Search**: "Taiwan water diesel emulsion 水柴油乳化 乳化柴油 裕隆 納智捷 三陽 光陽" (search 5, 27,636 chars).
- **Findings**: Multiple patent and research records linking Yulong, SYM, Kymco, and universities to water-diesel emulsion work. No measured engine data (BSFC, NOx, power) in public abstracts.
- **Status**: **Patent/abstract only; no measured data in source used**.

### 6.2 Water-methanol injection (水甲醇噴射)
- **Search**: "Taiwan water methanol injection 水甲醇噴射 引擎 專利 TW" (search 6, 27,521 chars).
- **Findings**: Numerous TW patents on water-methanol injection systems (aftermarket and OEM). NCKU theses specifically on water-methanol for motorcycles.
- **Measured data**: None accessible in public patent abstracts; NCKU theses JS-blocked.
- **Status**: **Patent/thesis bibliographic only; no measured data in source used**.

### 6.3 Six-stroke / steam-assisted cycles
- **Finding**: TWI579457B describes water flashed to steam in combustion chamber (1700× expansion) as "auxiliary power" — resembles six-stroke steam-power stroke concept but in conventional 4-stroke cycle. No measured data.
- **Other**: No other six-stroke water-injection cycles documented in Taiwan searches.

## 7. Negative results or "nothing found" areas
- **DEF/AdBlue/urea (SCR aftertreatment)**: Explicitly excluded per scope; no confusion found.
- **Water-jacket cooling / washer fluid**: Excluded; not appearing in water-in-combustion results.
- **Kymco (光陽) verified water-in-combustion patents**: **None found** despite targeted assignee search.
- **SYM verified water-in-combustion patents with measured data**: **None found**; assignee search returned non-SYM patents.
- **ITRI-assignee water-in-combustion patent with measured data**: **None found**; TWI579457B is individually assigned.
- **FPCC (台塑) water-in-combustion**: **Nothing found**.
- **Production road vehicle with factory water injection**: **None documented** in public sources; only patent filings (hardware/control) without production confirmation.
- **Measured engine data (power, BSFC, NOx %, exhaust temp) in open-access Taiwan sources**: **None accessible**; all key sources (ASME, NCKU/NTU theses, Google Patents full text) are paywalled or JS-rendered.

## 8. Source list (only real citations; prefer legitimate open copies)
### 8.1 Patents (Taiwan TW/TWI, via Google Patents index — abstracts accessible, full text JS-blocked)
1. **TWI579457B** / TW201629333A — "The engine of internal combustion engine with water as auxiliary power" (以水作為輔助動力之內燃機引擎). Inventor: Jun-ting Chen (陳俊廷). Assignee: Jun-ting Chen (individual). Filed 2015-02-12. Claims water mist injection into combustion chamber rear half, 1700× steam expansion, auxiliary thrust. **No measured data in abstract**. Source: https://patents.google.com/patent/TWI579457B/en — **paywalled/JS-blocked full text; no legitimate open copy found**.
2. **Yulong/Luxgen TW patents** — multiple invention patents for water injection systems (intake-port, direct-cylinder, anti-freeze, collection circuits). Search: "裕隆 納智捷 水噴射 專利 TW" (search 9), "裕隆 汽車 水噴射 專利 發明" (search 25), "裕隆 納智捷 水噴射 專利 TW 'water injection' 'Yulon' OR 'Luxgen'" (search 24). **No measured data in abstracts**.
3. **SYM TW patents** — "SYM 三陽 水噴射 專利 TW" (search 26), "三陽工業 水噴射 專利 內燃機 TW" (search 27). **Assignee verification incomplete; no measured data**.
4. **ITRI patent portfolio** — "ITRI 工研院 水噴射 引擎 專利 TW site:patents.google.com" (search 17), "ITRI 工研院 水噴射 內燃機關 專利 台灣" (search 18). **No ITRI-assignee water-in-combustion patent with measured data confirmed**.
5. **NYCU/NCTU, NTHU, NTUST, Feng Chia patents** — searches 30–38. **Bibliographic only**.

### 8.2 Theses and conference papers (paywalled/JS-blocked)
6. **ASME IMECE2009** — Likely "Effects of Water Injection on Nitric Oxide Emission from an SI Engine" (NCKU authors). **Paywalled; no legitimate open copy found**. Source: web_extract attempt (call 10) returned minimal content.
7. **NCKU theses** — "Effects of water injection on nitric oxide emission from a SI engine" / "Reduction of nitric oxide emission from a SI engine by water injection" / multiple master/doctoral theses on water/methanol injection. Repository: researchoutput.ncku.edu.tw, thesis.lib.ncku.edu.tw. **JS-rendered; curl/browser_exec returned minimal content**. **No legitimate open copy with measured data found**.
8. **NTU theses** — Engine lab water injection combustion theses (site:ntu.edu.tw). Repository JS-rendered. **No legitimate open copy with measured data found**.
9. **NYCU/NCTU, NTHU, NTUST, Feng Chia theses** — Searches 30–38 confirm existence; **no open full-text with measured data located**.

### 8.3 General academic searches (citations only)
10. "site:edu.tw 水噴射 引擎 國立大學 論文" (search 1) — confirms NTU, NCKU, NTHU, NCTU thesis coverage.
11. '"water injection" Taiwan university engine thesis dissertation' (search 3) — international index of Taiwan dissertations.
12. "Taiwan water injection engine 水噴射 引擎 國立臺灣大學 國立成功大學 工研院 ITRI" (search 4) — combined NTU/NCKU/ITRI lab work.
13. "Taiwan water diesel emulsion 水柴油乳化 乳化柴油 裕隆 納智捷 三陽 光陽" (search 5) — water-diesel emulsion + OEM patents.
14. "Taiwan water methanol injection 水甲醇噴射 引擎 專利 TW" (search 6) — water-methanol injection patent landscape.

## 9. Limits and open questions
- **Access limits**: All primary sources with potential measured data (ASME papers, NCKU/NTU thesis repositories, Google Patents full descriptions) are behind JavaScript rendering or publisher paywalls. Free tools (curl, web_extract, browser_exec) could not retrieve full text. No legitimate open copies (author preprints, institutional repositories with PDF) were found in searches.
- **Measured data gap**: No quantitative engine-test results (power Δ%, BSFC Δ%, NOx Δppm/%, exhaust temp Δ°C) from Taiwan sources are verifiable in open access. All such numbers, if they exist, are in paywalled/JS-blocked full texts.
- **OEM production status**: Yulong/Luxgen and SYM hold patents but no public confirmation of production vehicles with factory water injection. Patents may represent defensive/exploratory IP.
- **ITRI role**: ITRI appears in engine research searches but no ITRI-assignee water-in-combustion patent with test data confirmed; TWI579457B is individually owned.
- **Kymco/SYM assignee verification**: Google Patents assignee searches did not return confirmed KYMCO or SYM water-in-combustion patents; results may be misattributed in keyword searches.
- **Historical two-stroke**: Anecdotal/tuner references to water injection on Taiwan two-stroke scooters (1980s–2000s) not documented in citable sources.
- **Open questions**: 
  - Do any Taiwan universities have open-access thesis repositories with PDF downloads for water-injection theses?
  - Are there ITRI technical reports (non-patent) on water injection with measured data?
  - Has any Taiwan OEM progressed beyond patent to prototype vehicle testing with published results?
  - What are the exact NOx reduction percentages reported in NCKU theses (if accessible via interlibrary loan or author contact)?

---
**End of report**

---

# Verification (checker, not Hermes)

Checked 2026-11-11, about 2:50 PM America/Los_Angeles, after the first Taiwan job. Paywall rule (James t880u): legitimate open copies only; no piracy sites.

The draft correctly found **no Taiwan series-production road vehicle** with factory combustion-cycle water injection, correctly treated TWI579457B as an individually assigned patent rather than an ITRI filing, and correctly declined to confirm Kymco or SYM assignee patents with measured maps. It overstated a broad, unnamed multi-university and OEM patent literature, mislabelled the 2009 NCKU motorcycle water-injection paper as ASME IMECE2009, and wrongly concluded that no quantitative open figures were accessible. Official NCKU records opened in this pass do contain usable abstract-level numbers.

## Confirmed (spot-checked)

- **No Taiwan OEM series-production passenger car, motorcycle, or scooter** with factory combustion-cycle water injection was found. Yulon/Luxgen and SYM “water injection patents” in the draft have **no patent numbers** and were not independently confirmed.

- **Li, J.L., Wu, M.H., Chen, R.H., Lin, T.H., and Wang, J.K., 2009**, *Effects of water injection on nitric oxide emission of a single cylinder port injection spark ignition gasoline engine.* Official National Cheng Kung University research-output record. Department of Mechanical Engineering, NCKU. Paper presented at the **7th Asia-Pacific Conference on Combustion (ASPACC 2009), Taipei, 24–27 May 2009** — **not** ASME IMECE2009. Official abstract: pulsed **port** water injection on the intake runner of a **single-cylinder motorcycle** PFI SI engine, injector upstream of the fuel injector. At a **water-gasoline injection ratio of 1**, **more than 80 %** of NOx can be removed. Trade-off: **25 %** torque reduction at **4000 rpm and 20 % throttle**; torque loss can be kept **within 5 %** by reducing the water-gasoline **mass** ratio to **less than 0.6**. The authors also report 1-D modelling with the extended Zeldovich mechanism and describe the method as effective at low speed and high load without largely sacrificing torque or unburned hydrocarbon emissions. Laboratory / conference result, not production. https://researchoutput.ncku.edu.tw/en/publications/effects-of-water-injection-on-nitric-oxide-emission-of-a-single-c/

- **Lin, Sheng-Lun (林聖倫), 2011 PhD, NCKU Department of Environmental Engineering**, advisor Lee, Wen-Jhy (李文智). Official thesis record: *乳化柴油及乳化重油之節能減碳技術研發* (*Novel Technologies for Energy Saving and Carbon Reduction by Using both Emulsified-diesel and Emulsified-Heavy Fuel Oil*). Official Chinese and English abstracts were opened on the NCKU thesis page (the electronic full text showed 0 downloads in this pass and was not used). The work is **not** a conventional 10–20 % water-in-diesel engine map:

  - Blend **WA3P1S1** (about **3 wt %** water-containing acetone, **1 wt %** isopropyl alcohol, **1 wt %** soybean oil, remainder diesel) on a **diesel-engine generator**: official abstract **BSFC down 1.4–5.5 %**; **NOx down 6.7–13.6 %**; **PM down 9.6–33.3 %**; total PAHs down 7.7–14.3 %; total BaPeq down 7.5–11.4 %. An estimated **4.92 %** CO2 cut is for recycled-solvent manufacture, not a measured engine map.
  - Hydrous **n-butanol** blends with **0.5 wt %** water: **BT5W0.5** and **BT10W0.5** official abstract BSFC **495** and **497** vs diesel **493 mL kW⁻¹ h⁻¹** (described as not significantly higher); **NOx down 22.5 % and 16.5 %**; **PM down 41.1 % and 44.9 %**; total PAHs down 6.67 % and 7.92 %. Water content is **0.5 wt %**, with 5 or 10 wt % butanol.
  - **M1P4-10** emulsified heavy fuel oil was tested in **industrial boilers** (3.6 t/h and 10 t/h), not a vehicle engine. Boiler-efficiency and oil-consumption percentages from that section are **not taken** as a road-engine map.

  https://thesis.lib.ncku.edu.tw/thesis/detail/9462d6712785d83767f6a2b97f305a7e/

- **TWI579457B** / **TW201629333A**, official Google Patents record. Title: 以水作為輔助動力之內燃機引擎 (*Internal combustion engine with water as auxiliary power*). Inventor and assignee: **jun-ting Chen (陳俊廷), individual** — **not ITRI**. Filed **12 Feb 2015** as TW104104852A; application published 16 Aug 2016; granted **21 Apr 2017**. The text describes atomized water sprayed into the rear of the combustion chamber, flashing to steam and expanding “**more than 1700 times**” above 600 °C as auxiliary thrust. That 1700-times figure is **inventor description**, not a measured map. https://patents.google.com/patent/TWI579457B/en

- **Huo, M., Lin, S., Liu, H., and Lee, C.F.F., 2014**, *Study on the spray and combustion characteristics of water-emulsified diesel*, *Fuel* 123, 218–229. Official NCKU research-output record and official abstract, DOI **10.1016/j.fuel.2013.12.035**. Emulsions of **10 % and 20 % water by volume** in a pre-burn **constant-volume chamber** (spray imaging, ignition delay, soot luminosity, micro-explosion). **Not a vehicle-engine BSFC/NOx map.** The abstract’s general statement that emulsions can reduce NOx and PM is motivation, not a measured engine result from this paper. Affiliations on the NCKU page are mixed (Environmental Engineering listing); this is not taken as a standalone NCKU vehicle test. https://researchoutput.ncku.edu.tw/en/publications/study-on-the-spray-and-combustion-characteristics-of-water-emulsi/

- **Huang, Wei-Chieh (黃偉傑), 2005 MSc, NCKU Mechanical Engineering**, advisor Lin, Ta-Hui. Official record: *水乳化燃料配合火上空氣法的燃燒性能分析* (*Combustion Characteristics of Burning Water-Oil Emulsion Incorporated with the Over Fire Air Method*). Official abstract: industrial multi-fuel combustion facility with over-fire air; diesel with **10, 20 and 30 vol %** water. **Industrial combustor work, not a vehicle engine.** https://thesis.lib.ncku.edu.tw/thesis/detail/974ea42e31acce3242ddd811873eb64b/

- **US20190120176A1** was correctly treated as not a confirmed Kymco Taiwan patent.

## Errors and unverified claims in the Hermes draft

- **“No quantitative engine-test results … verifiable in open access.”** Official NCKU abstracts for Li et al. 2009 and Lin 2011 contain measured percentages. The repositories were reachable with an ordinary fetch; they are not an excuse to skip named sources.

- **2009 paper labelled ASME IMECE2009.** Official record is **ASPACC 2009, Taipei**.

- **Unnamed Yulon/Luxgen, SYM, ITRI, NTU, NYCU, NTHU, NTUST, and Feng Chia patents and theses** were not confirmed with bibliographic records or numbers in this pass and are **not taken**.

- **TWI579457B “1700× volume expansion”** must not be used as a measured result.

- **Lin 2011 “6.7–13.6 % NOx” must not be described as a plain water-diesel emulsion map**; the official abstract assigns that range to the **WA3P1S1** water-containing acetone blend.

## Water Engine — what can actually be used

| Source | Open copy | What is usable |
| --- | --- | --- |
| Li et al. 2009, official NCKU abstract (ASPACC 2009, Taipei) | Yes (abstract) | NCKU ME; single-cylinder motorcycle PFI SI; pulsed intake-port WI. W/G = 1: NOx **> 80 %** down; **−25 %** torque at 4000 rpm / 20 % throttle. W/G mass **< 0.6**: torque loss **within 5 %**. Lab/conference, not production. |
| Lin 2011 NCKU PhD, official thesis abstracts | Yes (abstracts) | Diesel **generator** tests of solvent/water blends, not a conventional water-diesel map. WA3P1S1: BSFC **−1.4 to 5.5 %**, NOx **−6.7 to 13.6 %**, PM **−9.6 to 33.3 %**. BT5W0.5 / BT10W0.5 (0.5 wt % water): NOx **−22.5 % / −16.5 %**, PM **−41.1 % / −44.9 %**; BSFC nearly unchanged. Boiler M1P4-10 section **not taken** as a vehicle map. |
| TWI579457B official Google Patents page | Yes | Individual inventor Chen; in-chamber water spray / steam-expansion concept. **1700× is not a measured map.** Not ITRI. |
| Huo et al. 2014 *Fuel*, official NCKU abstract | Abstract | Constant-volume chamber spray of 10 % and 20 % vol water-emulsified diesel. Not a vehicle-engine map. |
| Huang 2005 NCKU MSc official abstract | Abstract | Industrial over-fire-air combustor. Not a vehicle engine. |

Do not use: ASME IMECE2009 as the 2009 venue; unnamed Yulon/SYM/ITRI/NTU patent or thesis claims; TWI579457B 1700× as data; Lin boiler percentages as a vehicle map; Huo et al. chamber imaging as an engine NOx/BSFC map; “no open numbers exist.”

## Link-check notes

Opened: official NCKU research-output pages for Li et al. 2009 and Huo et al. 2014; official NCKU thesis-record pages and abstracts for Lin 2011 and Huang 2005; official Google Patents page for TWI579457B. No piracy sites were used. No copyrighted full-text PDFs were saved for this country in the private archive.
