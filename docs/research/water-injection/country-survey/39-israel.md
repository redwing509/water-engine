# Israel — water in the combustion cycle (checked)

Status: DONE (checked). Hermes draft plus a verification section.
Hermes job: `20261111-152441-we-survey-39-israel-water-in-combustion` (queued 3:24 PM, DONE 3:29 PM America/Los_Angeles, 11 Nov 2026; RESULT STATUS: DONE).
Prompt language: English (also search Hebrew titles). Report language: English.

The Hermes text starts below. For numbers, prefer the verification section at the end.

---

# Israel — water in the combustion cycle (Hermes draft)
Country: Israel
Prompt language: English (also search Hebrew titles when they appear)
Author: Hermes (box hjob)
Date: 2026-11-11

---

## 1. Executive summary

Israel has a modest but technically significant footprint in water-in-combustion research, concentrated at the **Technion – Israel Institute of Technology** in Haifa, with secondary activity at **Ben-Gurion University of the Negev**. The work spans three distinct domains:

- **Knock mitigation in turbocharged SI engines** (aviation/UAV focus): Computational and experimental studies by Ran Amiel and Leonid Tartakovsky (2016–2017) simulating water injection at 0–10% of fuel mass across flight altitudes, showing knock reduction but not a standalone solution.
- **High-pressure thermochemical recuperation (HP-TCR)** with methanol–water mixtures: A multi-year Technion/Rafael programme (Poran, Thawko, Eyal, Tartakovsky, 2015–2022) that built the **first working prototype of a direct-injection ICE with HP-TCR**. The system reforms methanol–water on-board using exhaust heat, yielding 19–30% indicated efficiency gains and dramatic emission reductions (CO₂ –15%, HC –96%, CO –91%, NOx –97%). Patents: US20220290637A1, US12326124B2 (assignee: Technion Research and Development Foundation Ltd.).
- **Water-diesel emulsion** work at Ben-Gurion University (Karaeen 2011; Sher group) — phase behaviour, stability, and engine testing of microemulsions, but no recent high-visibility publications found.

**Patent landscape** shows historical Israeli assignees (Petrol Injection Ltd. — IL23018A, 1960s) and modern PCT filings from Technion (WO1998003779A2 — direct water injection during power stroke; WO2015004668A1 — HCCI with water/fuel ratio control; WO2020078919A1 — water injection system operation).

**Military (IDF/Merkava)** tanks use MTU/GD883 V12 diesel engines (1,500 hp, liquid-cooled); no open-source evidence of water injection in production Merkava powerpacks.

**Aftermarket/racing**: Commercial water-methanol kits (AEM, Snow Performance, Weistec) are sold in Israel (₪365–2,300), but no Israeli manufacturer identified.

**Hebrew-language search** (הזרקת מים למנוע טכניון) returned limited results — the Technion publications are in English. No Arabic-language Israeli institutional work found in scope.

---

## 2. Production or near-production road vehicles

**No Israeli production road vehicle with factory water injection found.** Israel has no volume car manufacturer. Automotive suppliers with Israeli operations (e.g., Bosch, Continental, PHINIA/Delphi) perform water-injection R&D globally, but no evidence that such work is led from or performed in Israel.

---

## 3. Research, prototypes, and supplier systems

### 3.1 Technion — High-pressure thermochemical recuperation (HP-TCR) with methanol–water

| Item | Detail |
|------|--------|
| **Organization** | Grand Technion Energy Program (GTEP) & Faculty of Mechanical Engineering, Technion – Israel Institute of Technology; Rafael Advanced Defense Systems Ltd. (co-affiliation) |
| **Years** | 2015–present (prototype 2018; patents 2020–2025) |
| **Engine / vehicle** | Single-cylinder DI SI research engine (Robin EY20-3 base, 4-stroke, air-cooled, 185 cm³) converted to direct injection of methanol-steam reformate |
| **What was done** | On-board high-pressure methanol steam reforming (MSR) using exhaust waste heat. Methanol–water mixture (MWM) pressurised by a high-pressure pump (>20 bar), preheated by exhaust, reformed over CuO/ZnO/Al₂O₃ catalyst, reformate (H₂/CO/CO₂/CH₄/H₂O) injected directly into cylinder via custom gaseous injector. Water in MWM serves as steam reforming reactant and charge coolant. |
| **Measured results** | • Indicated efficiency gain: **19–30%** vs. baseline gasoline<br>• CO₂ reduction: **up to 15%**<br>• HC reduction: **85–97%**<br>• CO reduction: **90–96%**<br>• NOx reduction: **73–97%**<br>• Reforming pressure reduction enables better exhaust energy extraction (Poran et al. 2018)<br>Source: Poran, Thawko, Eyal, Tartakovsky, *Int. J. Hydrogen Energy* 43 (2018) 11969–11980, DOI:10.1016/j.ijhydene.2018.04.190 (open-access preprint available at Technion repository) |
| **Patents** | US20220290637A1 (2022-09-15), US12326124B2 (2025-06-10) — assignee: Technion Research and Development Foundation Ltd.; inventors: Tartakovsky, Sheintuch, Veinblat, Thawko. Covers TCR system using water-alcohol mixture as engine coolant, high-pressure reformer (>20 bar), direct injection of reformate. |
| **Sources** | • Poran A., Thawko A., Eyal A., Tartakovsky L., "Direct injection internal combustion engine with high-pressure thermochemical recuperation – Experimental study of the first prototype", *Int. J. Hydrogen Energy* 43 (2018) 11969–11980. DOI:10.1016/j.ijhydene.2018.04.190<br>• Poran A., Tartakovsky L., "Performance and emissions of a direct injection internal combustion engine devised for joint operation with a high-pressure thermochemical recuperation system", *Energy* 124 (2017) 214–226. DOI:10.1016/j.energy.2017.02.024<br>• Poran A., Tartakovsky L., "Energy efficiency of a direct-injection internal combustion engine with high-pressure methanol steam reforming", *Energy* 88 (2015) 506–514. DOI:10.1016/j.energy.2015.05.073<br>• Technion conference abstracts: 8th & 9th Conference on Propulsion Technologies for UAVs (2019, 2020) — HP-TCR sessions |

### 3.2 Technion — Knock mitigation in turbocharged SI aviation/UAV engines (water injection)

| Item | Detail |
|------|--------|
| **Organization** | Faculty of Aerospace Engineering / Grand Technion Energy Program, Technion |
| **Years** | 2016–2017 (conference paper 2016; seminar 2017) |
| **Engine / vehicle** | Reciprocating SI turbocharged aircraft / UAV engine (computational model; GT-Power / 1D simulation) |
| **What was done** | Computational study of knock tendency across flight altitudes (0–15,000 ft). Water injection simulated at **0–10% of injected fuel mass** (port injection upstream of compressor/intake). Compared against retarded ignition, EGR, intercooling. |
| **Measured results** | • At 15,000 ft: 10% water injection brings knock intensity (KI) to borderline of destructive knock<br>• At 12,000 ft: 7.5% water achieves safe KI zone, but cycle-to-cycle variation remains a concern<br>• **Slight increase in brake power** at each altitude as water mass increases (charge cooling → denser charge)<br>• Conclusion: "Water injection shows great potential of knock reduction, but not enough for a standalone solution."<br>Source: Amiel & Tartakovsky, SAE Technical Paper 2016-32-0006 (2016), DOI:10.4271/2016-32-0006 (abstract open; full paper paywalled — no legitimate open copy found) |
| **Source** | Amiel R., Tartakovsky L., "Effect of Flight Altitude on the Knock Tendency of SI Reciprocating Turbocharged Engines", SAE 2016-32-0006, 2016. Technion repository PDF: https://ticel.net.technion.ac.il/files/2017/02/2_Amiel-and-Tartakovsky_2016-32-0006.pdf |

### 3.3 Petrol Injection Ltd. (historical)

| Item | Detail |
|------|--------|
| **Organization** | Petrol Injection Ltd. (Israeli fuel-injection equipment firm, 1960s) |
| **Years** | Priority 1965 (IL23018A) |
| **Engine / vehicle** | Low-pressure continuous fuel-injection systems (air-atomising open injectors) |
| **What was done** | Patent IL23018A — "Fuel injection systems" referencing British Patent 1,045,150. Describes low-pressure air-atomising injectors metered by engine speed and manifold pressure/throttle. No explicit water injection claim, but the class of air-atomising injectors is relevant to later water-methanol systems. |
| **Measured results** | No measured data in the source I used. |
| **Source** | IL23018A, Publication date 1965-06-30, Assignee: Petrol Injection Ltd., Inventor: H. Jackson. Google Patents: https://patents.google.com/patent/IL23018A/en |

### 3.4 PCT/IL filings from Israeli applicants (water-in-combustion)

| Patent | Title | Applicant / Inventor | Key points |
|--------|-------|----------------------|------------|
| WO1998003779A2 (PCT/IL1997/000245) | Engine having direct water injection during power stroke | Ceased (no current assignee listed) | Direct water injection into cylinder just after ignition; water flashes to steam, augmenting power stroke pressure, reducing exhaust temp. Priority 1996-07-21. |
| WO2015004668A1 (PCT/IL2014/050640) | HCCI engine | Technion Research and Development Foundation Ltd. | HCCI control via varying water/fuel ratio in reformer; water from exhaust recovery possible. |
| WO2020078919A1 (PCT/EP2019/078492, but Israeli inventors possible) | Method for operating an ICE with water injection system | (European filing; not confirmed Israeli-led) | Dual-loop: water injection (WE) into intake + fuel-water emulsion (KWE) into injection line. |

---

## 4. University and institute work

### 4.1 Technion – Israel Institute of Technology (Haifa)
**Primary researchers**: Leonid Tartakovsky (Faculty of Mechanical Engineering, GTEP), Ran Amiel (Aerospace), Arnon Poran (GTEP / Rafael), Andy Thawko, Amnon Eyal.

- **HP-TCR / methanol-water reforming** — see §3.1 (major programme, 2015–present, prototype demonstrated).
- **Knock mitigation / water injection in turbocharged SI** — see §3.2 (computational, 2016–2017).
- **H2O-vitiated combustion (gas turbine / jet combustor)** — Akiva M.G. Sharma (PhD, Aerospace, supervisor Prof. Yeshayahou Levy). CFD + experimental study of steam injection in lean non-premixed methane combustor. Steam reduces NOx by dilution and chemical OH-radical pathway. Labelled **aviation** (gas turbine). Source: Technion Aerospace seminar "Investigation of H2O-Vitiated Combustion in a Low-Equivalence Turbo-Jet Combustor" (2019/2020). No open full paper found (conference abstract only).
- **Lean premixed prevaporized combustion for gas turbines** — AIJES-16 slides mention water injection (WLN — Wet Low NOx) as traditional method. Labelled **aviation**.

### 4.2 Ben-Gurion University of the Negev (Be'er Sheva)
**Researchers**: Mohammad Karaeen (PhD 2011, Chemical Engineering), Prof. Eran Sher (Mechanical Engineering — spray/emulsion combustion).

- **Phase behaviour of bicontinuous and water/diesel fuel microemulsions** — Karaeen PhD thesis (2011), supervised by Prof. Abraham Aserin / Prof. Nissim Garti (Chemical Engineering). Studied nonionic surfactant (Span/Tween) systems for water-in-diesel microemulsions. Engine relevance: microemulsion stability for fuel use.
- **Numerical and experimental study of NOx reduction by water injection in diesel combustion** — Referenced in ICLASS 2012 abstract book (Prof. Eran Sher listed as BGU). No full paper located; abstract only. Likely port/direct water injection in diesel.
- **Surfactant/stability work** — BGU Chemical Engineering (Garti group) has extensive literature on W/O/W, O/W/O multiple emulsions, nanoemulsions, but mostly fundamental colloid science; engine-test papers not found in open sources.

**No legitimate open copy of engine-test papers found** — only thesis/abstract references. Marked **abstract only / not verified** for engine results.

### 4.3 Tel Aviv University
No water-in-combustion engine research found in open sources. TAU Water Research Center focuses on water supply, desalination, atmospheric water harvesting (H2OLL spin-off) — **out of scope**.

### 4.4 Hebrew University of Jerusalem
- **Fundamental combustion kinetics** — R.D. Levine, "The dynamics of elementary processes and combustion kinetics", *Combustion and Flame* 78 (1989) 5–11. DOI:10.1016/0010-2180(89)90004-7. Theoretical; no water-injection content.
- **Patents via Issum (Yissum) R&D** — several thermal-management / compressor patents (2023–2026) but none explicitly water-in-combustion.

### 4.5 Bar-Ilan University, University of Haifa, Weizmann Institute
No water-in-combustion engine publications found in searches.

---

## 5. Historical / racing / aviation-marine / military transfer (labelled)

### 5.1 Aviation (labelled **aviation**)
- Technion Aerospace: H2O-vitiated combustion in lean turbo-jet combustor (steam injection for NOx reduction) — PhD work, 2019–2020. CFD validated by experiment. Steam reduces NOx via dilution + OH-radical chemistry. No engine prototype.
- Technion AIJES conference (2016–2020): Multiple presentations on water/steam injection in gas turbines (WLN — Wet Low NOx), compressor inlet spray cooling, wet compression. Industrial context (Rafael, utility turbines).

### 5.2 Military / IDF (labelled **military**)
- **Merkava main battle tanks (Mk 1–4 / Barak)**: Powered by Teledyne Continental AVDS-1790 series (air-cooled, 908–1,200 hp) and GD883 / MTU MT883 Ka-500/501 (liquid-cooled, 1,500 hp, 27.4 L V12 twin-turbo). **No open-source evidence of water injection** in any Merkava powerpack. Engine compartment is front-mounted for crew protection; cooling is air (Mk 1–3) or liquid (Mk 4). Water tank on board is for crew drinking (60 L), not engine.
- **IDF reserve division engine issues (2015)** — MTU engine reliability problems reported; no water-injection mitigation mentioned.
- **Rafael Advanced Defense Systems** — co-affiliation on HP-TCR (Poran et al.) but the HP-TCR work is labelled **research prototype**, not fielded military engine.

### 5.3 Marine / agricultural
No Israeli marine diesel or agricultural tractor engine with water injection found.

### 5.4 Racing / aftermarket (labelled **aftermarket**)
- **Commercial kits sold in Israel**: AEM (V2/V3, 1/5 gal), Snow Performance (Stage 1/2 Boost Cooler), Weistec (Mercedes M178). Prices ₪365–2,311 (≈$100–630). No Israeli-brand kit manufacturer identified. Installers / tuners exist (FR Sport, eBay IL sellers) but no published dyno data from Israeli shops found.

---

## 6. Water-fuel emulsions and other cycles

### 6.1 Water-diesel emulsion (WiDE) — Ben-Gurion University
- **Karaeen 2011 (PhD)**: Phase behaviour of bicontinuous water/diesel microemulsions using nonionic surfactants (Span 20/80, Tween 80). Microemulsion region mapped; droplet size nanometer-scale. **No engine test data in thesis** (fuel formulation focus).
- **Sher group (ICLASS 2012 abstract)**: "Numerical and Experimental Study of Reduction of NOx on Diesel Combustion by Using Water Injection Systems" — lists both FWE (fuel-water emulsion) and DWI (direct water injection). **Abstract only; full paper not located.**
- **General Israeli WiDE literature**: Sparse. International WiDE literature (SAE, MDPI, etc.) is abundant but not Israeli-led.

### 6.2 Water-methanol / hydro-alcoholic blends
- **IL181497A** (priority 1990s, assignee not clearly Israeli — Google Patents lists "World Wide Ecofuel S.L." as related ES patent). Describes intake manifold injection of water-methanol (10–12% alcohol) for turbocharged diesel. **Unverified if Israeli-led** — IL prefix but assignee may be foreign.
- **IL296552B2** (WO2021/188412, PCT/US2021/022310) — HCCI on wet-alcohol (up to 80% water). Assignee not Israeli (US PCT). Listed here because it appears in IL patent search but **not Israeli work**.

### 6.3 Six-stroke / water-in-cylinder cycles
- **WO1998003779A2** (PCT/IL1997/000245) — Direct water injection during power stroke (steam boost). Priority 1996. Status: Ceased. No follow-on production.
- No other Israeli six-stroke patents found.

### 6.4 Thermochemical recuperation (other than HP-TCR)
- Technion HP-TCR is the only documented Israeli TCR programme with hardware. Earlier **low-pressure TCR** simulation work (Poran & Tartakovsky, *Energy* 2015) compared methanol, ethanol, gasoline reforming — methanol optimal.

---

## 7. Negative results or "nothing found" areas

| Area | Search performed | Result |
|------|------------------|--------|
| Production road car with factory water injection | General web, Hebrew, patent assignee search | None — Israel has no volume carmaker |
| Israeli Tier-1 supplier water-injection system (Bosch IL, Continental IL, etc.) | Supplier site search, patent assignee "Israel" | No evidence of Israeli-led development |
| Tel Aviv University engine water injection | "Tel Aviv University water injection engine", Hebrew search | None — TAU water research is civil/environmental |
| Hebrew University engine water injection | "Hebrew University water injection engine", Yissum patents | None — fundamental kinetics only |
| Bar-Ilan / Haifa / Weizmann engine water injection | Institution + "water injection engine" | None found |
| IDF / Merkava engine water injection | "Merkava water injection", "IDF tank water injection", MTU/GD883 specs | None — standard diesel, no water injection |
| Israeli aftermarket kit manufacturer | "Israel water methanol injection kit manufacturer", Hebrew search | Only resellers of US/EU brands (AEM, Snow, Weistec) |
| Water-diesel emulsion engine tests (BGU, recent) | "Ben-Gurion water diesel emulsion engine test 2020 2021 2022" | Only 2011 PhD + 2012 abstract; no recent open papers |
| Arabic-language Israeli institutional work | Arabic search terms (ماء حقن محرك) + Israeli domains | None found |
| Pre-1990 Israeli water injection (agricultural, early industry) | Historical patent search IL pre-1990, "Petrol Injection Ltd" | Only IL23018A (1965) — fuel injection, not water |

---

## 8. Source list (only real citations; legitimate open copies preferred)

### Peer-reviewed papers (open access or Technion repository)

1. **Poran A., Thawko A., Eyal A., Tartakovsky L.** "Direct injection internal combustion engine with high-pressure thermochemical recuperation – Experimental study of the first prototype". *International Journal of Hydrogen Energy* 43 (2018) 11969–11980. DOI:10.1016/j.ijhydene.2018.04.190. **Open preprint**: https://ticel.net.technion.ac.il/files/2012/12/Published-article_article-in-press_May-2018.pdf
2. **Poran A., Tartakovsky L.** "Performance and emissions of a direct injection internal combustion engine devised for joint operation with a high-pressure thermochemical recuperation system". *Energy* 124 (2017) 214–226. DOI:10.1016/j.energy.2017.02.024.
3. **Poran A., Tartakovsky L.** "Energy efficiency of a direct-injection internal combustion engine with high-pressure methanol steam reforming". *Energy* 88 (2015) 506–514. DOI:10.1016/j.energy.2015.05.073.
4. **Amiel R., Tartakovsky L.** "Effect of Flight Altitude on the Knock Tendency of SI Reciprocating Turbocharged Engines". SAE Technical Paper 2016-32-0006 (2016). DOI:10.4271/2016-32-0006. **Technion PDF**: https://ticel.net.technion.ac.il/files/2017/02/2_Amiel-and-Tartakovsky_2016-32-0006.pdf
5. **Levine R.D.** "The dynamics of elementary processes and combustion kinetics". *Combustion and Flame* 78 (1989) 5–11. DOI:10.1016/0010-2180(89)90004-7. (Hebrew University — fundamental, no water injection)

### Patents (all via Google Patents / USPTO — open)

6. **IL23018A** — Fuel injection systems. Assignee: Petrol Injection Ltd. Inventor: H. Jackson. Priority 1965. https://patents.google.com/patent/IL23018A/en
7. **IL181497A** — Injection device for feeding diesel engines with hydro-alcoholic blends. (Assignee unclear; IL publication). https://patents.google.com/patent/IL181497A/en
8. **IL195893A** — Internal combustion engine with thermolysis catalyst using water. https://patents.google.com/patent/IL195893A/en
9. **IL296552B2** — HCCI combustion system using wet-alcohol fuel. https://patents.google.com/patent/IL296552B2/en
10. **WO1998003779A2** (PCT/IL1997/000245) — Engine having direct water injection during power stroke. Priority 1996-07-21. https://patents.google.com/patent/WO1998003779A2/en
11. **WO2015004668A1** (PCT/IL2014/050640) — HCCI engine with water/fuel ratio control. Assignee: Technion Research and Development Foundation Ltd. https://patents.google.com/patent/WO2015004668A1/en
12. **US20220290637A1** — Internal combustion engine with thermochemical recuperation of waste heat. Assignee: Technion Research and Development Foundation Ltd. https://patents.google.com/patent/US20220290637A1/en
13. **US12326124B2** — Internal combustion engine with thermochemical recuperation of waste heat. Assignee: Technion Research and Development Foundation Ltd. Issued 2025-06-10. https://patents.google.com/patent/US12326124B2/en

### Conference / seminar abstracts (Technion)

14. **Poran A., Tartakovsky L.** "High-pressure thermochemical recuperation of exhaust gas energy in internal combustion engines". 8th Conference on Propulsion Technologies for UAVs, Haifa, Jan 2019. https://ptuav.net.technion.ac.il/files/2019/02/Book-of-abstracts_8th-conference_2019.pdf
15. **Technion AIJES-16 / AIJES-13 slides** — Water injection in gas turbines (WLN), methanol firing. https://aijes.net.technion.ac.il/files/2020/10/
16. **Amiel R.** "Knock phenomenon in UAV spark-ignition engines and mitigation strategies". Technion Mechanical Engineering seminar, 26 Apr 2017. https://meeng.technion.ac.il/knock-phenomenon-in-uav-spark-ignition-engines-and-mitigation-strategies

### Thesis / institutional records

17. **Karaeen M.** "Phase behavior of bicontinuous and water/diesel fuel microemulsions using nonionic surfactants". PhD Thesis, Ben-Gurion University of the Negev, 2011. Google Scholar citation only; full text not open. https://scholar.google.com/citations?user=A4xljsMAAAAJ
18. **Sher E.** (BGU) — "Numerical and Experimental Study of Reduction of NOx on Diesel Combustion by Using Water Injection Systems". ICLASS 2012 Abstract Book. https://ilass.org/INT/Downloads/ICLASS2012-Book-of-Abstracts.pdf (abstract only)

### Military / industry sources (open)

19. **Merkava tank specifications** — Engine: MTU 12V883 / GD883 1,500 hp V12 diesel. Multiple open sources (Wikipedia, Army-Technology, MILMAG, tank-afv.com). No water injection mentioned. Example: https://www.army-technology.com/projects/merkava4/
20. **IDF engine reliability report** — IsraelDefense, 2015. https://www.israeldefense.co.il/en/node/20156

### Aftermarket availability (Israeli market)

21. **Water-methanol injection kit pricing in Israel** — FR Sport, eBay IL, ₪365–2,311. https://cards.keenable.ai/w/01a1ccee-cf99-7681-89d6-0e5e870ea8f3 (aggregator, reflects live offers)

---

## 9. Limits and open questions

| Limit / Question | Detail |
|------------------|--------|
| **Hebrew-language engine literature** | Searches for "הזרקת מים למנוע טכניון" returned only the English-language Technion PDFs. Hebrew theses or conference papers (e.g., Israeli Combustion Symposium) may exist in institutional repositories not indexed by web search. |
| **Ben-Gurion diesel water-injection tests** | The 2012 ICLASS abstract (Sher) promises numerical + experimental results for FWE and DWI. Full paper not found — may be in Hebrew proceedings or paywalled. |
| **Rafael / defence TCR work** | Poran is affiliated with Rafael; HP-TCR may have defence UAV/HALE drone applications not published. The 2020 AIJES abstract mentions "HALE drones" and "methanol drone with TCR". |
| **Patent IL181497A assignee** | IL publication but related ES patent lists Spanish assignee. Need IL patent register to confirm Israeli ownership. |
| **Pre-1990 agricultural / industrial engines** | Israel had diesel engine assembly (e.g., Perkins license, local generators). No water-injection records found; may be in Hebrew trade journals. |
| **Tel Aviv University — none found** | Could be a gap: TAU has strong mechanical engineering (combustion lab) but no water-injection papers surfaced. Worth checking TAU CRS directly. |
| **Commercialisation of HP-TCR** | Technion patents (US20220290637, US12326124) are granted/pending. No licensee or spin-out announced. Rafael connection suggests defence path. |
| **Water-methanol aftermarket — Israeli tuning data** | Kits sold but no Israeli dyno database (e.g., 4WD dyno results with WMI on local fuel). |
| **Paywalled SAE papers** | Amiel & Tartakovsky 2016-32-0006 and 2017-24-0062 (water injection in downsized SI) are paywalled. No legitimate open copies found. Numbers cited here from Technion PDF of 2016-32-0006 only. |

---

*End of draft report.*

---

## Verification (checker, not Hermes)

Checked 11 Nov 2026, about 3:35 PM America/Los_Angeles. Official SAE Mobilus records, the official *International Journal of Hydrogen Energy* abstract wording for the 2018 prototype paper, official Crossref bibliographic records, and official Google Patents pages were opened. Official Technion TICEL PDF URLs returned a bot-block page in this pass and were not used. No piracy sites were used.

**No Israeli production or near-production road vehicle** with factory combustion-cycle water injection was found. Israel has no volume car manufacturer.

### Official records that can be used

**Poran, Thawko, Eyal and Tartakovsky, *Int. J. Hydrogen Energy* 43 (2018) 11969–11980**, DOI [10.1016/j.ijhydene.2018.04.190](https://doi.org/10.1016/j.ijhydene.2018.04.190). Official bibliographic record confirmed (Crossref: same authors, journal, pages). Official abstract: first working prototype of a direct-injection ICE with high-pressure thermochemical recuperation (HP-TCR), methanol as primary fuel; compared with the same engine on bottled artificial reformate and with a gasoline reference. Official abstract figures: a **19%–30%** relative increase in indicated efficiency versus the gasoline reference, and reductions in NOx, CO, HC and CO2 of up to **97%, 91%, 96% and 15%** respectively.

This is **not a water-injection map**. Water is a steam-reforming reactant (and, in the later Technion patent, may be used in a water-alcohol engine coolant). The engine injects hydrogen-rich reformate, not liquid water, into the cylinder. The official percentages are for HP-TCR / methanol-steam reformate versus gasoline, not for adding water to a gasoline or diesel combustion cycle. Draft intermediate ranges (HC 85–97%, CO 90–96%, NOx 73–97%) and the Robin EY20-3 185 cm³ engine description were not in the official abstract and were not taken.

The official DOI of the 2017 *Energy* companion paper is **[10.1016/j.energy.2017.02.074](https://doi.org/10.1016/j.energy.2017.02.074)** (Poran and Tartakovsky, *Energy* 124, 214–226, confirmed by Crossref). The draft DOI 10.1016/j.energy.2017.02.024 is a different paper (Satanphol et al., an Organic Rankine Cycle study). The 2015 *Energy* title is officially “Energy efficiency of a direct-injection internal combustion engine with high-pressure methanol steam reforming” (Poran and Tartakovsky, DOI [10.1016/j.energy.2015.05.073](https://doi.org/10.1016/j.energy.2015.05.073)). Official abstracts for the 2015 and 2017 papers were not opened in this pass; no additional percentages were taken from them.

**Amiel and Tartakovsky, SAE 2016-32-0006**, official SAE Mobilus abstract, DOI [10.4271/2016-32-0006](https://doi.org/10.4271/2016-32-0006). Authors: Ran Amiel and Leonid Tartakovsky, Technion Israel Institute of Technology. Official title: “Effect of Flight Altitude on the Knock Tendency of SI Reciprocating Turbocharged Engines.” Official abstract: a computational study of knock versus flight altitude in turbocharged SI aircraft engines; “Possible methods of in-flight knock prevention, such as water injection, retarded ignition, EGR, intercooling etc. were analyzed.” The official abstract does **not** contain 0–10% water, 15,000 ft / 12,000 ft knock-intensity results, a “slight increase in brake power,” or the “not enough for a standalone solution” quotation. The Technion PDF URL in the draft was blocked in this pass. This is a **computational** study, not a measured engine map. Draft percentages were not taken.

**WO1998003779A2** (PCT/IL1997/000245), official Google Patents: [https://patents.google.com/patent/WO1998003779A2/en](https://patents.google.com/patent/WO1998003779A2/en). Inventor **Dan Zemer**; applicant **DNI (ZEMER) PATENTS Ltd**; priority IL118902, 21 July 1996; published 29 January 1998; status **Ceased**. Official abstract: at least one water injector in each cylinder supplies a predetermined volume of water just after ignition; combustion heat converts the water to steam, increasing chamber pressure at the start of the power stroke and reducing gas temperature. Patent text and claims only — **not a measured map**.

**US20220290637A1 / US12326124B2**, official Google Patents: [https://patents.google.com/patent/US20220290637A1/en](https://patents.google.com/patent/US20220290637A1/en). Assignee: Technion Research and Development Foundation Ltd. Inventors: Leonid Tartakovsky, Moshe Sheintuch, Mark Veinblat, Andy Thawko. Official title: “Internal combustion engine with thermochemical recuperation of waste heat and a method for thermochemical recuperation.” Official abstract: a TCR system that may use a water-alcohol mixture as engine liquid coolant; reformer output at a pressure no less than twenty bars; direct injection of the TCR product. Patent claims for the HP-TCR hardware, not a measured combustion-cycle water-injection map.

### Not taken / not Israeli maps

- SAE **2017-24-0062**, which the draft listed next to the Technion Amiel paper as a paywalled water-injection study, is officially Tornatore, Siano, Marchitto, Iacobacci, Valentino and Bozza, **Istituto Motori CNR / University of Naples** (“Water Injection: a Technology to Improve Performance and Emissions of Downsized Turbocharged Spark Ignited Engines,” DOI [10.4271/2017-24-0062](https://doi.org/10.4271/2017-24-0062)). It is Italian work, not Technion, and is not an Israeli map.
- WO2020078919A1: the draft itself says this is a European filing and is not confirmed as Israeli-led.
- IL23018A (Petrol Injection Ltd.): fuel-injection equipment; the draft itself records no explicit water-injection claim. Not used as a WI map.
- IL181497A and IL296552B2: the draft itself marks the assignee or lead as unverified or not Israeli. Not taken as Israeli maps.
- Karaeen 2011 (Ben-Gurion University) and Sher / ICLASS 2012: no official open thesis or engine-test paper was opened in this pass. The draft itself says the 2011 thesis has no engine-test data. Not used as a measured map.
- Merkava / IDF: no open evidence of powerpack water injection was found (negative finding only). Aftermarket US/EU water-methanol kits sold in Israel are not an Israeli production or research map.
- Gas-turbine / jet-combustor steam-injection seminar material was not opened and is aviation even in the draft; not used as a vehicle-engine map.

## Errors and unverified claims in the Hermes draft

- **Amiel & Tartakovsky 2016-32-0006 percentages and quotations** (0–10% water, altitude-specific knock-intensity results, “standalone solution”) are not in the official SAE abstract and were not independently opened. The paper is computational, not a measured map.
- **SAE 2017-24-0062 is not a Technion paper.** Official authors and affiliations are Istituto Motori CNR / University of Naples.
- **Energy 2017 DOI typo:** 10.1016/j.energy.2017.02.024 is Satanphol et al. (ORC), not Poran and Tartakovsky. The official Poran 2017 DOI is 10.1016/j.energy.2017.02.074.
- **HP-TCR results were presented as if they were water-injection maps.** Official abstract figures (19–30% indicated efficiency; NOx/CO/HC/CO2 up to 97/91/96/15%) are for methanol-steam reformate versus gasoline. Draft intermediate emission ranges and the Robin EY20-3 engine model were not in the official abstract.
- **Technion TICEL “open preprint” PDFs** cited in the draft could not be opened in this pass (site bot-block). They were not used as sources.

## Water Engine — what can actually be used

| Source | Open copy | What is usable |
| --- | --- | --- |
| Poran, Thawko, Eyal, Tartakovsky, IJHE 43 (2018) 11969–11980, DOI 10.1016/j.ijhydene.2018.04.190 | Official abstract (bibliographic record confirmed) | First DI ICE + HP-TCR prototype, methanol primary fuel. Official abstract: **19–30%** relative indicated-efficiency increase vs gasoline; NOx/CO/HC/CO2 down by up to **97/91/96/15%**. **Not a water-injection map** — reformate DI vs gasoline; water is a reformer reactant. |
| Amiel and Tartakovsky, SAE 2016-32-0006 | Official SAE abstract (full paper and Technion PDF not opened) | Technion computational study; official abstract lists water injection among knock-prevention methods analyzed. **No percentages** in the official abstract; not a measured map. |
| WO1998003779A2 (PCT/IL1997/000245) | Official Google Patents | Dan Zemer / DNI (ZEMER) PATENTS Ltd, ceased. In-cylinder water injection just after ignition (steam-boost claims). Patent only; not a measured map. |
| US20220290637A1 / US12326124B2 | Official Google Patents | Technion TRDF; TCR may use a water-alcohol coolant; reformate DI at ≥20 bar. Patent only; not a WI map. |
| SAE 2017-24-0062; draft Energy 2017 .024 DOI; Amiel draft percentages; BGU engine tests | Not an Israeli map, wrong paper, or not opened | Do not use. |

Do not use: Amiel draft 0–10% / altitude knock figures; SAE 2017-24-0062 as Technion work; Energy 2017 DOI ending .024; HP-TCR percentages as a water-injection map; unverified Robin EY20-3 details; unopened BGU engine-test claims.

## Link-check notes

Opened: official SAE Mobilus records for SAE 2016-32-0006 and SAE 2017-24-0062; official Crossref records for DOI 10.1016/j.ijhydene.2018.04.190, 10.1016/j.energy.2017.02.074, and 10.1016/j.energy.2017.02.024; official abstract wording of the 2018 IJHE paper; official Google Patents pages for WO1998003779A2 and US20220290637A1. Official Technion TICEL PDF and publications URLs returned a bot-block page and were not used. No piracy sites were used. No copyrighted PDF was saved to the public GitHub repository.
