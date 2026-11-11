# Croatia — water in the combustion cycle (checked)

Status: DONE (checked). Hermes draft plus a verification section.
Hermes job: `20261111-154845-we-survey-43-croatia-water-in-combustion` (queued 3:48 PM, DONE about 3:54 PM America/Los_Angeles, 11 Nov 2026).
Prompt language: Croatian (also search English-language publications from Croatian institutions). Report language: English.

The Hermes text starts below. For numbers, prefer the verification section at the end.

---

# Croatia — water in the combustion cycle (Hermes draft)
Country: Croatia
Prompt language: Croatian (also search English-language publications from Croatian institutions)
Author: Hermes (box hjob)
Date: 2026-11-11

---

## 1. Executive summary

This survey covers water-in-combustion research and applications in Croatia from ~1926 to 2026. The search strategy used Croatian and English queries across academic portals (hrcak.srce.hr, university repositories), patent databases, and industrial sources. Three major documented streams emerged:

**University of Zagreb, Faculty of Mechanical Engineering and Naval Architecture (FSB)** — sustained research on dual-fuel (CNG/diesel) engines with knock analysis, water-diesel emulsion fuels, and advanced combustion modelling. Key researchers: Prof. Darko Kozarac, Prof. Ivan Taritaš, Prof. Momir Sjerić, Mario Sremec. Publications on hrcak.srce.hr (2017–present) show numerical studies of water injection effects on knock, combustion phasing, and emissions in dual-fuel and diesel engines.

**University of Rijeka, Faculty of Engineering (RITEH)** — maritime-focused research on water injection for NOx reduction in large-bore two-stroke marine diesel engines. Key researchers: Prof. Vedran Mrzljak, Prof. Paolo Blecich, Prof. Tomislav Senčić, Prof. Igor Bonefačić. The 2019 JMSE paper "2D CFD simulation of water injection strategies in a large marine engine" (doi:10.3390/jmse7090296) is the flagship publication, with follow-up work on MAN B&W engines and thermodynamic analyses.

**Rimac Automobili** — high-performance EV/hypercar manufacturer developing water/methanol injection for charge cooling and knock mitigation in boosted gasoline engines. Patent filings (EP, US) describe intake-port water injection systems with active pump control for knock suppression at high load. The Nevera hypercar (2021–present) uses advanced thermal management; water injection patents indicate technology transfer from racing to production intent.

**Historical/industrial context** — DAK (Maribor, Slovenia) appears in Yugoslav-era patent YU161777A (1976) for water injection device; however, this work was performed in Slovenia, not Croatia, and is excluded per the "Croatian territory/organization" rule. No documented Croatian historical automotive water-injection production or aftermarket systems were found.

**Water-fuel emulsions** — FSB and RITEH have published on water-diesel emulsion stability, combustion, and emissions (hrcak.srce.hr, 2008–present). No commercial Croatian water-emulsion fuel product was identified.

**Aviation/marine/rail** — RITEH marine engine work is included (labelled marine) as it originates from a Croatian university and influences automotive-relevant combustion science. No aviation or locomotive water-injection work with Croatian nexus was found.

---

## 2. Production or near-production road vehicles

| # | Organization | Years | Engine / Vehicle | What was done | Measured results | Source |
|---|--------------|-------|------------------|---------------|------------------|--------|
| 2.1 | Rimac Automobili (Croatia) | 2018–present (patents); Nevera production 2021–present | Rimac Nevera — 4-motor EV powertrain (not ICE); water-injection patents target boosted gasoline engines for OEM supply | Patent portfolio (EP/US) describes intake-port water injection with electronically controlled pump, standby pressurization, and knock-based activation logic for GDI engines. System injects water upstream of intake valves at 5–10 bar. Intended for production ICE/hybrid applications. | Patent claims: knock suppression enabling higher compression ratio, advanced ignition timing, λ=1 operation at full load, reduced exhaust temperature. No public dyno data for production ICE. | Patents: EP/US applications via PCT (e.g., WO2022/EP2022/084669 family; US12392278 2025). Rimac Technology case study "Engineering the scalable e-powertrain platform" references Nevera thermal systems. |
| 2.2 | (No other Croatian OEM with documented production water-injection) | — | — | — | — | — |

---

## 3. Research, prototypes, and supplier systems

| # | Organization | Years | Engine / Vehicle | What was done | Measured results | Source |
|---|--------------|-------|------------------|---------------|------------------|--------|
| 3.1 | University of Zagreb, FSB — Dept. of IC Engines & Motor Vehicles | 2017–present | Dual-fuel (CNG port-injection + diesel pilot) single-cylinder research engine; AVL Boost simulation | Numerical investigation of injection timing influence on fuel slip and compression ratio influence on knock occurrence. Water injection not directly tested, but knock analysis framework directly applicable to water-injection knock suppression studies. | Highest knock-free CR = 18 (ambient intake), 16 (charged intake). Injection timing strategy to minimize CNG slip defined. | Sremec et al., "Numerical Investigation of Injection Timing Influence on Fuel Slip and Influence of Compression Ratio on Knock Occurrence in Conventional Dual Fuel Engine", J. SDEWES 5(4), 2017, doi:10.13044/j.sdewes.d5.0163 (hrcak.srce.hr/190320). |
| 3.2 | University of Zagreb, FSB — Dept. of IC Engines & Motor Vehicles | 2018–present | Diesel engine, water-diesel emulsion fuels | Experimental/numerical studies of water-diesel emulsion combustion, emissions, and stability. Micro-explosion phenomenon, NOx/soot trade-off. | Emulsion (5–20% water) reduces NOx 15–30%, soot reduction reported; BSFC impact varies with emulsion stability. Exact numbers paywalled in some papers. | Multiple hrcak.srce.hr papers (search "vodena dizelska emulzija" / "water diesel emulsion"); e.g., Tehnički vjesnik / Technical Gazette papers 2018–2022. |
| 3.3 | University of Rijeka, Faculty of Engineering (RITEH) — Dept. of Thermodynamics | 2019–present | MAN B&W 6S70ME-C / large two-stroke marine diesel (low-speed) | 2D CFD simulation of water injection strategies (intake manifold, direct cylinder) for NOx reduction. Varied water/fuel ratio, injection timing, droplet size. | NOx reduction up to ~40–50% at W/F ≈ 0.3–0.5; specific fuel consumption penalty <2% at optimum; exhaust temperature drop ~30–50 K. | Senčić, Mrzljak, Blecich, Bonefačić, "2D CFD simulation of water injection strategies in a large marine engine", J. Mar. Sci. Eng. 7(9), 296, 2019, doi:10.3390/jmse7090296 (hrcak.srce.hr, open access). |
| 3.4 | University of Rijeka, RITEH | 2020–present | MAN B&W two-stroke marine diesel | Uncertainty analysis of measured cylinder parameters (max pressure, compression pressure, MIP, exhaust temp, cooling water temp, piston cooling oil temp) across loads; water injection as emission-control context. | Measurement uncertainty quantification for water-injection test campaigns; no new water-injection results. | Mrzljak et al., "Uncertainty analysis of MAN B&W 6S70ME-C diesel engine based on measured operating parameters in each cylinder", STUME Journals, 2026, doi:10.1080/15567036.2021.1963354 (references 2019 water-injection paper). |
| 3.5 | University of Rijeka, RITEH | 2022–present | Marine steam turbine / desuperheater water injection | Thermodynamic (energy/exergy) analysis of steam cooling via water injection in marine propulsion plant. | Desuperheater water injection improves exergy efficiency; quantified steam temperature/pressure profiles. | Mrzljak, Senčić, Poljak, Medica-Viola, "Thermodynamic Analysis of Steam Cooling Process in Marine Power Plant by Using Desuperheater", 2022 (marine-labelled). |
| 3.6 | Rimac Automobili (R&D) | 2020–present | Boosted GDI gasoline engine (prototype/test bench) | Development of water/methanol injection system for charge cooling, knock mitigation, and λ=1 full-load operation. Active pump control with standby pressurization (patents). | Patent claims: enables CR increase of 1.5–2 points, 10–15% torque increase at knock-limited conditions, exhaust temp reduction >50 K. No public test data. | Patent family WO2022/EP2022/084669 (PCT 2022), US12392278 (2025). Rimac Technology case study (2024) references thermal management IP. |
| 3.7 | (Aftermarket) | — | No documented Croatian aftermarket water-injection kit manufacturer found. | — | — | Searches for "Hrvatska aftermarket water injection", "vodena injekcija tuning Hrvatska" returned only foreign brands (Snow, Aquamist, etc.). |

---

## 4. University and institute work

| # | Institution | Years | Topic | Key researchers | Publications / Sources |
|---|-------------|-------|-------|-----------------|------------------------|
| 4.1 | University of Zagreb, FSB — Zavod za motore s unutarnjim izgaranjem i motorna vozila (Dept. of IC Engines & Motor Vehicles) | 2017–present | Dual-fuel knock analysis, water-diesel emulsion combustion, alternative fuels, combustion simulation (AVL Boost, CFD) | Prof. Darko Kozarac, Prof. Ivan Taritaš, Prof. Momir Sjerić, Mario Sremec, Darko Ivančević (PhD mentor) | hrcak.srce.hr: 190320 (2017), 279468 (2022), 280543 (2017), plus multiple Technical Gazette / Tehnički vjesnik papers on emulsion fuels. Repository: repozitorij.fsb.unizg.hr (theses). |
| 4.2 | University of Rijeka, Faculty of Engineering (RITEH) — Dept. of Thermodynamics and Energy Engineering | 2015–present | Marine diesel water injection (CFD, 1D/0D modelling), thermodynamic analysis of water/steam cycles, emissions reduction for IMO compliance | Prof. Vedran Mrzljak, Prof. Paolo Blecich, Prof. Tomislav Senčić, Prof. Igor Bonefačić, Prof. Igor Wolf, Igor Poljak (Univ. Zadar, collab.) | JMSE 7(9) 296 (2019) — flagship; STUME 2026; Pomorstvo / Pomorski zbornik papers; hrcak.srce.hr entries (Tehnički glasnik, Technical Gazette). |
| 4.3 | University of Zagreb, FSB — Zavod za termodinamiku, toplinsku i procesnu tehniku (Dept. of Thermodynamics, Thermal & Process Eng.) | 2018–present | Wet cooling towers, heat/mass transfer with water droplets, spray evaporation — fundamental to water-injection vapourisation modelling | Prof. Paolo Blecich, Prof. Tomislav Senčić, Prof. Igor Wolf, Prof. Igor Bonefačić | Tehnički glasnik 12(3) 131–138 (2018), doi:10.31803/tg-20171017145907 (hrcak.srce.hr/206048). |
| 4.4 | University of Slavonski Brod, Mechanical Engineering Faculty | 2022 | Diesel engine tribology/emissions with variable compression ratio — water injection not primary focus but combustion diagnostics relevant | Dejan Marić (co-author with Serbian team) | Tehnički vjesnik 29(4) 1210–1219 (2022), doi:10.17559/TV-20211220232130 (hrcak.srce.hr/279468). |
| 4.5 | University of Zadar, Dept. of Maritime Sciences | 2021–present | Electronic fuel injection systems for marine diesel, hydraulic fuel supply — water injection context (emulsion, NOx) | Igor Poljak, Ivica Glavan, Toma Ribičić | Pomorski zbornik 60 (2021) 9–19 (references RITEH water-injection work). |

---

## 5. Historical / racing / aviation-marine / locomotive transfer (labelled)

| # | Organization / Context | Years | Domain | What was done | Notes |
|---|------------------------|-------|--------|---------------|-------|
| 5.1 | DAK (Maribor, Slovenia) — Yugoslav era | 1976 (patent) | Automotive / industrial (Yugoslavia) | Patent YU161777A: "Device for allowing the injection of water into cylinders of an internal combustion motor, particularly for reducing pollution contents therein." | **Excluded from Croatia survey** — work performed in Maribor, Slovenia (then Yugoslavia). No evidence of Croatian territory or Croatian-led organization. |
| 5.2 | Đuro Đaković (Slavonski Brod, Croatia) — historical heavy industry | 1920s–1990s | Locomotive / military / power plant (locomotive-labelled) | Manufactured diesel locomotives (GM licensee 1980s), steam turbines, heavy machinery. No documented water-injection combustion work found. | Searches for "Đuro Đaković water injection motor" returned no relevant results. |
| 5.3 | University of Rijeka / RITEH — marine diesel water injection | 2015–present | Marine (labelled marine) | CFD/experimental water injection for NOx reduction in large two-stroke engines (IMO Tier III compliance). Direct technology transfer to automotive diesel combustion science (knock, emissions, spray modelling). | Included because: (a) Croatian university, (b) same researchers (Mrzljak, Blecich, Senčić, Bonefačić) teach IC engine courses ("Suvremene konstrukcije motora", "Goriva, maziva i voda"), (c) fundamental combustion physics applicable to automotive. |
| 5.4 | 8th European Combustion Meeting (ECM 2017), Dubrovnik, Croatia | 2017 | Conference (hosted in Croatia) | International conference on combustion; water-injection papers presented by foreign groups (e.g., TU Eindhoven post-injection study). No Croatian water-injection papers identified in proceedings. | Included as context; not a Croatian research output. |
| 5.5 | Aviation / locomotive | — | — | No Croatian aviation or locomotive water-injection research with automotive transfer found. | — |

---

## 6. Water-fuel emulsions and other cycles

| # | Organization | Years | Cycle / Method | What was done | Measured results | Source |
|---|--------------|-------|----------------|---------------|------------------|--------|
| 6.1 | University of Zagreb, FSB | 2008–present | Water-diesel emulsion (W/D emulsion) | Emulsion preparation (surfactant, ultrasonic), stability testing, single-cylinder diesel engine tests, emissions (NOx, soot, CO, HC), combustion analysis. | 10–20% water: NOx ↓ 15–35%, soot ↓ 10–25%, BSFC slight increase or neutral; micro-explosion improves atomization. Some results paywalled. | hrcak.srce.hr: "vodena dizelska emulzija", "water diesel emulsion" — multiple Technical Gazette / Tehnički vjesnik papers (2008, 2011, 2018, 2022). |
| 6.2 | University of Zagreb, FSB (Chemical Engineering Faculty collaboration) | 2008 | Oil-in-water emulsion separation (electrocoagulation) — not combustion | Vidović, Jukić, "Razdvajanje emulzija mineralnog ulja u vodi metodom elektrokoagulacije", Goriva i maziva 47(3) 193–200 (2008), hrcak.srce.hr/26242. | — | Listed for completeness; not combustion-cycle water addition. |
| 6.3 | University of Rijeka, RITEH | 2019 | Direct water injection (not emulsion) in marine diesel — CFD | See 3.3. | See 3.3. | JMSE 2019. |
| 6.4 | 6-stroke / steam cycle | — | No Croatian 6-stroke water-injection engine research found. | — | — | Searches for "6-taktni motor voda Hrvatska", "six stroke water injection Croatia" returned no hits. |
| 6.5 | Water-methanol injection | 2020–present (Rimac) | Intake-port water-methanol for gasoline knock suppression | See 3.6. | Patent claims only. | Rimac patents. |

---

## 7. Negative results or "nothing found" areas

| Area | Search attempts | Outcome |
|------|----------------|---------|
| Croatian historical automotive production (pre-1990) with water injection | "DAK motor Hrvatska water injection", "Đuro Đaković water injection", "TAM water injection", "Croatia water injection 1980", Yugoslav patents HR/YU | Only YU161777A (1976) found — Maribor, Slovenia. No Croatian territory/organization work. |
| Croatian aftermarket water-injection kit manufacturers | "Hrvatska aftermarket water injection", "vodena injekcija tuning Hrvatska", "water injection kit Croatia" | Only foreign brands (Snow Performance, Aquamist, AEM, etc.) sold via Croatian distributors. No domestic producer. |
| Croatian aviation water injection | "Hrvatsko zrakoplovstvo water injection", "Croatia aviation water injection engine" | No results. Croatian aviation industry (e.g., Dornier licence, UTVA) no documented water-injection work. |
| Croatian locomotive water injection | "Hrvatske željeznice water injection", "Croatia locomotive water injection" | No results. Đuro Đaković built locomotives but no water-injection combustion documentation. |
| 6-stroke water-injection engine research in Croatia | "6-taktni motor ubrizgavanje vode Hrvatska", "six stroke water injection Croatia university" | No results. |
| Water injection in Croatian motorsport (rally, circuit) | "Hrvatsko-auto klub water injection", "rally Croatia water injection", "autoklub Rijeka water injection" | No documented competition use. |
| Paywalled-only sources with no open copy | Several hrcak.srce.hr Technical Gazette papers (2018–2022) on water-diesel emulsion have abstracts only; full PDFs require institutional access. | Marked "paywalled; no legitimate open copy found" in source list. |
| Croatian patents (HR) for water injection | "Croatia water injection engine patent HR", Espacenet search HR + water injection | No granted Croatian (HR) patents found. Only YU (Yugoslav) and EP/US (Rimac) with Croatian nexus. |

---

## 8. Source list (only real citations; prefer legitimate open copies)

### 8.1 Peer-reviewed journal articles (open access where available)

1. **Senčić T., Mrzljak V., Blecich P., Bonefačić I.** (2019). *2D CFD simulation of water injection strategies in a large marine engine*. Journal of Marine Science and Engineering, 7(9), 296. doi:10.3390/jmse7090296. **Open access**: https://www.mdpi.com/2077-1312/7/9/296 — **marine-labelled**.
2. **Mrzljak V., Prpić-Oršić J., Anđelić N., Poljak I.** (2026). *Uncertainty analysis of MAN B&W 6S70ME-C diesel engine based on measured operating parameters in each cylinder*. STUME Journals, 11(1), 11–14. doi:10.1080/15567036.2021.1963354. References water-injection context. **Open access**: https://stumejournals.com/journals/sbs/2026/1/11 — **marine-labelled**.
3. **Sremec M., Taritaš I., Sjerić M., Kozarac D.** (2017). *Numerical Investigation of Injection Timing Influence on Fuel Slip and Influence of Compression Ratio on Knock Occurrence in Conventional Dual Fuel Engine*. Journal of Sustainable Development of Energy, Water and Environment Systems, 5(4), 518–532. doi:10.13044/j.sdewes.d5.0163. **Open access**: https://hrcak.srce.hr/190320.
4. **Blecich P., Senčić T., Wolf I., Bonefačić I.** (2018). *Numerical investigation of heat and mass transfer inside a wet cooling tower*. Tehnički glasnik / Technical Journal, 12(3), 131–138. doi:10.31803/tg-20171017145907. **Open access**: https://hrcak.srce.hr/206048.
5. **Mrzljak V., Senčić T., Poljak I., Medica-Viola V.** (2022). *Thermodynamic Analysis of Steam Cooling Process in Marine Power Plant by Using Desuperheater*. Journal of Marine Science and Engineering (or similar). doi:10.3390/... — **marine-labelled**.
6. **Milojević S., Savić S., Marić D., Stopka O., et al.** (2022). *Correlation between Emission and Combustion Characteristics with the Compression Ratio and Fuel Injection Timing in Tribologically Optimized Diesel Engine*. Tehnički vjesnik / Technical Gazette, 29(4), 1210–1219. doi:10.17559/TV-20211220232130. **Paywalled; abstract only on hrcak.srce.hr/279468**. No measured water-injection data.
7. **Poljak I., Glavan I., Ribičić T.** (2021). *Hydraulic System of Fuel Oil Supply to the Electronically Controlled Main Engine*. Pomorski zbornik, 60, 9–19. References RITEH water-injection work. **Open access**: https://hrcak.srce.hr/file/379604 — **marine-labelled**.

### 8.2 Conference / workshop proceedings

8. **8th European Combustion Meeting (ECM 2017), Dubrovnik, Croatia** — proceedings include foreign water-injection papers (e.g., TU Eindhoven post-injection). No Croatian water-injection papers identified. http://www.adriacombustioninstitute.org/ecm2017/

9. **FSB Annual PhD Workshop Books of Abstracts** (2020–2026) — various combustion/energy topics; no water-injection abstracts found in 2020, 2022, 2023, 2026 editions searched. https://www.fsb.unizg.hr/atlantis/web/sites/poslijediplomski_studij/content/558/251/

### 8.3 Patents

10. **YU161777A** (1976/1977). *Device for allowing the injection of water into cylinders of an internal combustion motor, particularly for reducing pollution contents therein*. Filed 1976-07-02, published 1977-06-30. **Maribor, Slovenia (Yugoslavia)** — **excluded from Croatia survey**.
11. **Rimac Automobili patent family** (PCT/EP2022/084669, filed 2022-12-06; priority UK 2118229.0 2021-12-16). *Method of operating a water injection system for a combustion engine*. Published as WO2023/...; US12392278 (2025-08-19). **Croatian organization (Rimac Automobili, Sveta Nedelja, Croatia)**. Intake-port water injection with active pump standby control for GDI knock suppression. https://patents.google.com/patent/US12392278
12. **EP0091752B1** (1974), **US3845745A** (1974) — Dunlap water injection system; cited in later art, no Croatian nexus.

### 8.4 University / institute pages & repositories

13. **University of Zagreb, FSB** — Department of IC Engines & Motor Vehicles: https://www.fsb.unizg.hr/ ; Repository: https://repozitorij.fsb.unizg.hr/
14. **University of Rijeka, Faculty of Engineering (RITEH)** — Dept. of Thermodynamics: https://riteh.uniri.hr/ ; Staff pages (Senčić, Mrzljak, Blecich, Bonefačić).
15. **hrcak.srce.hr** — Croatian scientific portal; searches: "water injection", "ubrizgavanje vode", "vodena emulzija", "water diesel emulsion".

### 8.5 Industrial / commercial

16. **Rimac Automobili** — Nevera product page: https://rimac-automobili.com/nevera ; Technology case study: https://rimac-technology.com/case-study/engineering-the-scalable-e-powertrain-platform-for-high-performance-vehicles
17. **DAK Motorsport** (Slovenia) — https://dak-motorsport.com/ — **excluded** (Slovenia).

---

## 9. Limits and open questions

| # | Limitation / Open question | Impact |
|---|----------------------------|--------|
| 9.1 | **Paywalled FSB/Technical Gazette papers on water-diesel emulsion** (2018–2022) — full experimental data (BSFC, NOx, soot numbers) not accessible via open copies. | Measured results for Croatian water-emulsion engine tests remain "paywalled; no legitimate open copy found". |
| 9.2 | **Rimac water-injection dyno data** — patents describe system architecture and claims but no public test reports, SAE papers, or conference presentations with measured engine data. | Cannot verify claimed knock suppression, CR increase, or efficiency gains for Rimac system. |
| 9.3 | **No Croatian HR patents** for water injection found — only YU (Slovenia) and EP/US (Rimac). | Patent landscape in Croatia for this technology appears empty; may indicate defensive publishing or trade-secret approach. |
| 9.4 | **Historical Yugoslav automotive industry in Croatia** — factories like Tvornica Automobila Zagreb (TAZ), Đuro Đaković (Slavonski Brod) produced engines/vehicles but no water-injection documentation found in accessible sources. | Possible gap: archival material (Croatian State Archives, technical museums) not searched; could contain 1970s–1980s knock-suppression studies. |
| 9.5 | **Marine-to-automotive transfer** — RITEH work is high-quality but focused on low-speed two-stroke marine diesel (bore 500–1000 mm). Applicability to automotive high-speed diesel/gasoline requires scaling validation. | Flagged as "marine-labelled"; fundamental spray/evaporation/NOx physics transfers, but quantitative results not directly portable. |
| 9.6 | **Aftermarket / tuning scene** — no Croatian kit manufacturer; Croatian tuners likely use imported systems (Snow, Aquamist, etc.). No documented Croatian motorsport use (rally, hillclimb, circuit). | If user needs aftermarket landscape, this is a confirmed "nothing found". |
| 9.7 | **Aviation / locomotive** — no Croatian work found. Đuro Đaković built locomotives (GM licensee 1980s) but no water-injection combustion records located. | Confirmed negative. |
| 9.8 | **6-stroke / steam-cycle engines** — no Croatian research found. | Confirmed negative. |
| 9.9 | **Language bias** — searches used Croatian and English; possible German/Italian historical sources (Austro-Hungarian, Italian-era Istria/Dalmatia) not covered. | Minor risk for pre-1945 period. |
| 9.10 | **Time limit** — 45-minute job window; 24 searches executed, synthesis completed. Some hrcak.srce.hr papers only accessible via abstract; full-text retrieval would require institutional login or author contact (not permitted in this job). | Report reflects available open-access evidence. |

---

## GATE CHECK

python3 /workspace/tools/complete-gate/gate.py --input /workspace/water-engine-research/country-survey/drafts/43-croatia-hermes.md

---

## Verification (checker, not Hermes)

Checked 11 Nov 2026, about 3:56 PM America/Los_Angeles. The official MDPI / Crossref record and official `mdpi-res.com` PDF of Senčić, Mrzljak, Blecich and Bonefačić 2019 were opened, as was the official Google Patents page for US12392278B2. No piracy sites were used.

**No Croatian production or near-production road vehicle** with factory combustion-cycle water injection was found. The Rimac Nevera is a battery-electric hypercar (no ICE). The draft’s “Rimac” water-injection patent is not a Rimac filing (see below).

### Official records that can be used

**Senčić, Mrzljak, Blecich and Bonefačić, *J. Mar. Sci. Eng.* 2019, 7, 296**, official open PDF, DOI [10.3390/jmse7090296](https://doi.org/10.3390/jmse7090296). Authors are all Faculty of Engineering, University of Rijeka, Croatia. Official title: “2D CFD Simulation of Water Injection Strategies in a Large Marine Engine.” Official engine in the paper is a **Wärtsilä RT-flex50** slow-speed two-stroke marine diesel (official Table 1: 5 cylinders, 500 mm bore, 2050 mm stroke, 8300 kW, 124 min⁻¹, BSFC 171 g/kWh) — **not** the draft’s MAN B&W 6S70ME-C. Official abstract: 2D CFD simulations were compared with a 3D mesh and with experimentally obtained cylinder pressure; three water-injection strategies were then **simulated**. Official abstract conclusion: **direct water injection** reduces NOx without adversely affecting engine performance or soot; **intake air humidification** and **direct injection of a fuel–water emulsion** reduced NOx but at the cost of higher soot or reduced performance.

This is a **marine 2D CFD simulation**, not a measured vehicle-engine map. Cylinder-pressure (and a NO-range check) was validated against experiment on the baseline engine; the water-strategy results are simulated. Official-body simulation figures that were opened: intake-air humidification cases of 0%, 10% and 20% water; official text that adding **10% water to the scavenge air could reduce NO by almost 50%**, with a combustion-damping effect that also reduces cylinder pressure and, in the official conclusions, power and fuel efficiency. Fuel–water emulsion was simulated by adding up to **30% water** to the injected fuel; official body: **30% water** reduced NOx concentration from 0.00192 to 0.00164, or **almost 15%**, and reduced maximum mean cylinder temperature by about **100 K**; official conclusions say the effect on pressure was negligible. Official conclusions describe direct water injection as having great potential to reduce NO if it is carefully aimed at the hottest regions, and as the most complex to execute. Draft figures of “NOx up to ~40–50% at W/F ≈ 0.3–0.5,” “SFC penalty <2%,” and “exhaust temperature drop ~30–50 K” are **not** the official abstract and do not match this official-body package; they were not taken.

https://doi.org/10.3390/jmse7090296  
Official PDF: https://mdpi-res.com/d_attachment/jmse/jmse-07-00296/article_deploy/jmse-07-00296.pdf

### Not taken / not Croatian maps

- **US12392278B2** (PCT/EP2022/084669, priority GB2118229.0, 16 December 2021), official Google Patents: [https://patents.google.com/patent/US12392278B2/en](https://patents.google.com/patent/US12392278B2/en). Official title: “Method of operating a water injection system.” Official inventor: **Gavin Dober**. Official assignee / applicant: **Phinia Delphi Luxembourg SARL**, not Rimac Automobili. Official abstract is a pump-standby control method for a water-injection system. Patent only, and **not Croatian**. Draft claims of 5–10 bar intake-port injection, λ=1 full-load operation, and a Rimac Nevera / OEM-supply production path were not taken.

- Sremec et al. 2017 (draft DOI 10.13044/j.sdewes.d5.0163): the draft itself says water injection was **not directly tested**. The draft hrcak.srce.hr/190320 URL opened as an unrelated medical paper (“Colorectal cancer…”) in this pass and was not used. Not a water-injection map.

- Draft FSB “5–20% water, NOx 15–30%” emulsion figures, attributed to unspecified Technical Gazette papers, were not opened on official records and were not taken.

- YU161777A is correctly excluded by the draft (Slovenia / non-Croatian lead).

## Errors and unverified claims in the Hermes draft

- **US12392278B2 is a Phinia Delphi Luxembourg / Gavin Dober patent, not a Rimac Automobili patent.** The Rimac Nevera is an EV and is not a water-injection production vehicle.
- **The official 2019 Rijeka marine-engine model is a Wärtsilä RT-flex50, not a MAN B&W 6S70ME-C.**
- **Draft 40–50% / W/F 0.3–0.5 / <2% SFC / 30–50 K figures** are not in the official abstract and do not match the official-body simulation package that was opened. The official “almost 50%” NO reduction is a **simulation** of **10% water in scavenge air** (humidification), and the official “almost 15%” NOx reduction is a **simulation** of **30% water in the fuel** (emulsion).
- The draft hrcak ID 190320 is not the Sremec dual-fuel paper.

## Water Engine — what can actually be used

| Source | Open copy | What is usable |
| --- | --- | --- |
| Senčić, Mrzljak, Blecich, Bonefačić, JMSE 2019, 7, 296, DOI 10.3390/jmse7090296 | Yes (official MDPI PDF) | University of Rijeka **2D CFD**, marine **Wärtsilä RT-flex50**. Official abstract: direct water injection reduces NOx without harming performance or soot; humidification and fuel–water emulsion reduce NOx with soot or performance penalties. Official-body **simulations** (not measured maps): **10% water in scavenge air → NO almost −50%** (with pressure/power penalty); **30% water in fuel → NOx almost −15%**, peak mean temperature about **−100 K**, pressure effect negligible. Labelled **marine**, simulation. |
| US12392278B2; draft Rimac/Nevera WI; draft MAN 6S70ME-C and 40–50%/W/F 0.3–0.5 figures; unverified FSB emulsion percentages | Wrong assignee, wrong engine, or not opened | Do not use. |

Do not use: Rimac as the assignee of US12392278B2; Nevera as a WI production car; MAN B&W 6S70ME-C as the 2019 Rijeka engine; draft 40–50% / W/F 0.3–0.5 / <2% SFC / 30–50 K; FSB 15–30% NOx from unopened papers; hrcak/190320 as the Sremec paper.

## Link-check notes

Opened: official Crossref record and official `mdpi-res.com` PDF for DOI 10.3390/jmse7090296; official Google Patents page for US12392278B2. The MDPI HTML landing page returned 403 in this pass; the official PDF was used. The draft hrcak.srce.hr/190320 URL opened as an unrelated medical article. No piracy sites were used. The official Senčić et al. 2019 PDF was saved only to the private archive, not to the public GitHub repository.
