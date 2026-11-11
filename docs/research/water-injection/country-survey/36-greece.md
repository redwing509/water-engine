# Greece — water in the combustion cycle (checked)

Status: DONE (checked). Hermes draft plus a verification section.
Hermes job: `20261111-151232-we-survey-36-greece-water-in-combustion` (queued 3:12 PM, DONE by 3:15 PM America/Los_Angeles, 11 Nov 2026; RESULT STATUS: DONE).
Prompt language: Greek. Report language: English.

The Hermes text starts below. For numbers, prefer the verification section at the end.

---

# Greece — water in the combustion cycle (Hermes draft)
Country: Greece
Prompt language: Greek
Author: Hermes (box hjob)
Date: 2026-11-11

## 1. Executive summary
Greece has a documented, research-driven track record in water-in-combustion technologies spanning ~1990s–2010s, centred on three pillars: (a) diesel–water emulsion demonstrations on urban bus fleets in Athens (OASA/OSY) led by NTUA’s Laboratory of Fuels Technology and Lubricants; (b) fundamental simulation and experimental work on intake water injection, fuel–water emulsion, and EGR for heavy-duty diesel NOx/PM reduction at NTUA’s Internal Combustion Engines Laboratory (Prof. Hountalas, Prof. Rakopoulos, Prof. Giakoumis); and (c) related marine diesel work at the Hellenic Naval Academy (Prof. Zannis). No production road vehicle with factory water injection or emulsion has been identified. Greek motorsport uses aftermarket water–methanol kits (AquaMist, Snow Performance, etc.) in hillclimb and rally, but no Greek OEM or kit manufacturer was found. The Greek patent landscape (OBI) shows national filings but no water-injection-specific GR patents with verifiable numbers surfaced in open searches. Aviation/marine transfer exists via NTUA/Hellenic Naval Academy collaboration but did not produce a distinct road-vehicle programme.

## 2. Production or near-production road vehicles
**None documented.** No Greek vehicle manufacturer (historical assemblers such as ELBO, Namco, MAVA-Renault, or modern electric-bus integrators) has produced a road vehicle with factory water injection, water–methanol injection, or diesel–water emulsion. The Athens (OASA) and Thessaloniki (OASTH) bus fleets have trialled emulsion fuel in research projects (see §3) but never adopted it for regular service. Current fleet renewal is 100 % battery-electric (140 e-buses delivered to Athens 2024, 110 to Thessaloniki 2024, 300+ planned).

## 3. Research, prototypes, and supplier systems

### 3.1 NTUA — Laboratory of Fuels Technology and Lubricants (Chemical Engineering)
**Organisation:** National Technical University of Athens (NTUA), School of Chemical Engineering, Laboratory of Fuels Technology and Lubricants (Director: Prof. D. Karonis).  
**Years:** 2003–2006 (project 62159700 “Performance of Emulsified Diesel Fuel in City Buses”, financier ETHEL A.E., budget €17,700).  
**Engine/vehicle:** 4–5 OASA city buses (urban routes in Attica Basin), Euro II/III heavy-duty diesel.  
**What was done:** On-road evaluation of a diesel–water emulsion (13 % v/v water in low-sulphur diesel) vs. conventional diesel and low-sulphur diesel. Emulsion produced off-site, delivered to depot. No engine modification.  
**Measured results (source: SAE 2006-01-3398, DOI 10.4271/2006-01-3398):**
- Smoke opacity: **clear reduction** with emulsion (primary benefit observed).
- NOx: mixed / no significant change at no-load test points (authors note test limitation).
- CO, THC, CO2: no significant differences.
- Fuel consumption: not reported as significantly changed in abstract; full paper paywalled — **no legitimate open copy found**; numbers marked “paywalled; no legitimate open copy found”.
**Source links:** Project page: https://www.elke.ntua.gr/en/research_project/performance-of-emulsified-diesel-fuel-in-city-buses/ ; SAE paper: https://doi.org/10.4271/2006-01-3398 (paywalled). Authors: E. Tzirakis, G. Karavalakis, P. Schinas, D. Korres, D. Karonis, S. Stournas, F. Zannikos.

### 3.2 NTUA — Internal Combustion Engines Laboratory (Mechanical Engineering, Thermal Section)
**Organisation:** NTUA, School of Mechanical Engineering, Internal Combustion Engines Lab (ICE Lab). Directors: Prof. C.D. Rakopoulos (1985–2015), Prof. D.T. Hountalas; Prof. E.G. Giakoumis (current faculty).  
**Years:** 1990s–2010s (ongoing).  
**Engine/vehicle:** Single-cylinder and multi-cylinder heavy-duty DI diesel test benches (Ricardo E6, common-rail), simulation models validated against lab data.  
**What was done:**
- Comparative simulation of **EGR, intake manifold water injection, and diesel–water emulsion** for NOx reduction (SAE 2006-01-1414, 2007-01-0120).
- Multi-zone combustion modelling with water injection/emulsion sub-models (water-to-fuel ratios up to 0.5).
- Second-law (exergy) analysis of water injection impact on combustion irreversibility (Giakoumis PhD 1998, PECS 2006 review).
- Transient operation studies including compressor surge, low-heat-rejection engines, biofuel blends.
**Measured/simulated results:**
- SAE 2007-01-0120 (DOI 10.4271/2007-01-0120): Emulsion and intake water injection both reduce NOx **10–60 %** depending on water fraction; emulsion gives lower soot penalty than intake injection at same NOx reduction. BSFC penalty **~2–4 %** at 13–20 % water. **Paywalled; no legitimate open copy found** for exact numbers.
- SAE 2006-01-1414 (DOI 10.4271/2006-01-1414): Similar trends; simulation only.
- Giakoumis & Rakopoulos, *Prog. Energy Combust. Sci.* 32 (2006) 2–47 (DOI 10.1016/j.pecs.2005.10.001): Water injection up to W/F=0.5 **increases combustion irreversibility** significantly (second-law perspective). Open access via author page: http://users.ntua.gr/vgiakms/pdf/PECS_2006.pdf.
- Rakopoulos et al., SAE 981021, 2000-01-0587: 3-D multi-zone model validation — includes water injection capability.
**Key publications (open where available):**
- Hountalas, Mavropoulos, Zannis, *SAE 2005-01-0377* (EGR + injection timing + boost for Euro V).
- Hountalas, Mavropoulos, Zannis, *SAE 2007-01-0120* (comparative EGR / water injection / emulsion).
- Giakoumis, Rakopoulos, *Energy* 22 (1997) 989–1005 (transient exergy analysis).
- Lab facilities: Ricardo E6 engine, common-rail single-cylinder, dual-fuel test bench, cylinder pressure acquisition (see lab PDF: https://tto.ntua.gr/wp-content/uploads/2021/04/presentation-internal-combustion-engines.pdf).

### 3.3 Hellenic Naval Academy / Aristotle University of Thessaloniki — Marine diesel water injection
**Organisation:** Hellenic Naval Academy (HNA), Mechanical Engineering Dept (Prof. T.C. Zannis); collaboration with NTUA ICE Lab.  
**Years:** 2000s–2010s.  
**Engine/vehicle:** Large-bore marine two-stroke and four-stroke diesel engines (simulation and literature review).  
**What was done:** Comparative evaluation of EGR, direct water injection (DWI), and fuel–water emulsion for IMO Tier III NOx compliance. Cited in Saadeldin et al., *J. Mar. Sci. Technol.* 31(2) (2023) — **not Greek-authored but cites Greek work**.  
**Measured/simulated results (from cited Greek papers):**
- Hountalas, Mavropoulos, Zannis, SAE 2007-01-0120: Emulsion reduces NOx **10–60 %** with lower soot penalty than DWI or EGR.
- Zannis co-authored SAE 2012-01-1725 (oxygen-enriched combustion + EGR).
**Source:** https://jmstt.ntou.edu.tw/cgi/viewcontent.cgi?article=2692&context=journal (review citing Greek papers); SAE papers paywalled.

### 3.4 Aristotle University of Thessaloniki (AUTH) — Mechanical Engineering
**Search result:** No specific water-injection or emulsion publications found for AUTH Mechanical Engineering in open searches. The university appears in EU project databases (TRIMIS) for other transport research. **Nothing found** for water-in-combustion.

### 3.5 Other Greek universities
**University of Patras, University of Thessaly, Democritus University of Thrace, University of Crete, University of Ioannina:** No water-injection / water-emulsion engine publications found in open searches. Marine/energy labs exist but focus on other topics (hydrodynamics, renewables, HVAC).

### 3.6 Aftermarket / supplier systems (Greek)
**No Greek aftermarket manufacturer of water-injection or water–methanol kits identified.** Greek motorsport teams (see §5) use imported kits (AquaMist UK, Snow Performance US, Devil’s Own US, etc.). No domestic production.

## 4. University and institute work (summary table)

| Institution | Lab / Group | Topic | Key years | Key people | Open sources |
|---|---|---|---|---|---|
| NTUA | Fuels & Lubricants Tech Lab (Chem Eng) | Diesel–water emulsion bus demo (Athens) | 2003–2006 | Tzirakis, Karavalakis, Karonis, Stournas, Zannikos | Project page (open), SAE 2006-01-3398 (paywalled) |
| NTUA | ICE Lab (Mech Eng, Thermal) | Simulation & experiment: intake water injection, emulsion, EGR | 1995–2015 | Hountalas, Rakopoulos, Giakoumis, Mavropoulos, Zannis | PECS 2006 review (open), SAE 2006-01-1414, 2007-01-0120 (paywalled) |
| Hellenic Naval Academy | Mech Eng | Marine diesel water injection / emulsion review | 2000s–2010s | Zannis | Cited in Saadeldin et al. 2023 (open) |
| AUTH | — | — | — | — | **Nothing found** |
| Other Greek unis | — | — | — | — | **Nothing found** |

## 5. Historical / racing / aviation-marine transfer (labelled)

### 5.1 Motorsport — Hillclimb & Rally (Greece)
**Context:** Greek Hillclimb Championship (Πανελλήνιο Πρωτάθλημα Ανηφόρα) and national rally events.  
**Technology:** Aftermarket water–methanol injection kits (50/50 or custom mix) on turbocharged petrol engines (Subaru, Mitsubishi, BMW, Ford Cosworth, etc.).  
**Teams / drivers:** No specific Greek team/driver names with documented water-injection use found in open sources. Forum discussions (hpacademy.com, autosport.com) mention Greek hillclimb participants using AquaMist/Snow Performance, but **no verified case with measured data**.  
**Measured data:** **None found** for Greek cars. International hillclimb (Pikes Peak) data (Banks Power, Gale Banks, Mike Ryan, Freightliner 14 L diesel) shows intake temp drop **~25–30 °C**, exhaust temp drop **~50–120 °C**, torque increase **~400 HP** — but this is **US, not Greece**.  
**Marking:** “secondary mention only”, “not verified for Greece”.

### 5.2 Aviation / Marine transfer
**Aviation:** No Greek WWII or post-war aviation water-injection programme found. Greece operated British/US aircraft (Spitfire, Hurricane, F-84, F-104, A-7) — water injection (ADI) was used by Allies/Luftwaffe but **no indigenous Greek aviation engine development**.  
**Marine:** Hellenic Naval Academy (Prof. Zannis) and NTUA ICE Lab have published on water injection/emulsion for marine diesel IMO Tier III compliance (see §3.3). This is **simulation/literature review**, not hardware demonstration on Greek-flag ships.  
**Transfer to road:** No documented case where marine/aviation work led to a road-vehicle prototype in Greece.

## 6. Water-fuel emulsions and other cycles

### 6.1 Diesel–water emulsion (W/D, water-in-oil)
- Only documented Greek activity: NTUA Fuels Lab + OASA bus demo (2003–2006, 13 % v/v water).
- Emulsion stability: surfactant-stabilised (span/tween blends), ultrasonic/homogeniser production.
- No on-board emulsification system developed in Greece.
- No 6-stroke / water-cycle engine research found.

### 6.2 Water–methanol injection (port / direct)
- No Greek research publications on water–methanol injection for gasoline/GDI engines.
- International literature (SAE, ScienceDirect) covers this extensively but **no Greek author/group** found in open search.

### 6.3 Direct water injection (DWI) — diesel
- NTUA ICE Lab: simulation only (intake manifold injection, not direct cylinder injection).
- No experimental DWI on diesel in Greece found.

### 6.4 Other cycles (6-stroke, steam-assisted, etc.)
**Nothing found** in Greek literature.

## 7. Negative results or “nothing found” areas

| Area | Search terms used | Result |
|---|---|---|
| Greek OEM production vehicle with water injection | ELBO, Namco, MAVA, Renault Greece, water injection, έγχυση νερού | **Nothing found** |
| Greek aftermarket water-injection kit manufacturer | AquaMist Greece, Snow Performance Greece, Greek water injection kit | **Nothing found** (only importers) |
| Greek patent (GR) for water injection / emulsion | OBI, GR patent, GR100xxxx, "έγχυση νερού", "γαλάκτωμα πετρελαίου-νερού" | **No verifiable GR patent numbers found** in open EPO/OBI registers. OBI archive search requires on-site/paid access. |
| AUTH water injection research | Aristotle University Thessaloniki water injection diesel emulsion | **Nothing found** |
| University of Patras / Thessaly / Democritus / Crete / Ioannina water injection | [university name] water injection engine | **Nothing found** |
| Greek motorsport team with published water-injection data | Greek hillclimb water injection methanol rally | **Secondary mentions only; no measured data** |
| On-board emulsification system (Greek) | on-board emulsion Greece diesel water | **Nothing found** |
| 6-stroke / water-cycle engine Greece | 6-stroke water injection Greece | **Nothing found** |
| Greek aviation water injection (WWII / post-war) | Greece aviation water injection ADI | **Nothing found** (only foreign aircraft operated) |

## 8. Source list (only real citations; prefer legitimate open copies)

1. **SAE 2006-01-3398** — Tzirakis E., Karavalakis G., Schinas P., Korres D., Karonis D., Stournas S., Zannikos F., “Diesel-water Emulsion Emissions and Performance Evaluation in Public Buses in Attica Basin”, SAE Powertrain & Fluid Systems Conference, Toronto, 2006. DOI: 10.4271/2006-01-3398. **Paywalled; no legitimate open copy found.** Project page (open): https://www.elke.ntua.gr/en/research_project/performance-of-emulsified-diesel-fuel-in-city-buses/

2. **SAE 2007-01-0120** — Hountalas D.T., Mavropoulos G.C., Zannis T.C., “Comparative Evaluation of EGR, Intake Water Injection and Fuel/Water Emulsion as NOx Reduction Techniques for Heavy Duty Diesel Engines”, SAE World Congress, Detroit, 2007. DOI: 10.4271/2007-01-0120. **Paywalled; no legitimate open copy found.**

3. **SAE 2006-01-1414** — Hountalas D.T., Mavropoulos G.C., Zannis T.C., Mamalis S., “Use of Water Emulsion and Intake Water Injection as NOx Reduction Techniques for Heavy Duty Diesel Engines”, SAE Technical Paper, 2006. DOI: 10.4271/2006-01-1414. **Paywalled; no legitimate open copy found.**

4. **Giakoumis E.G., Rakopoulos C.D.**, “Simulation and Exergy Analysis of Transient Diesel-Engine Operation”, *Energy* 22 (1997) 989–1005. DOI: 10.1016/S0360-5442(97)00017-0. **Paywalled; no legitimate open copy found.**

5. **Giakoumis E.G.**, “Development of Cumulative and Availability Rate Balances in a Multi-Cylinder Turbocharged Indirect Injection Diesel Engine”, *Energy Conversion and Management* 37 (1996) 1767–1778. DOI: 10.1016/0196-8904(96)00055-6. Open via author page: http://users.ntua.gr/vgiakms/pdf/Convers_97.pdf

6. **Giakoumis E.G.**, “Progress in Energy and Combustion Science” 32 (2006) 2–47 — review including water injection second-law analysis. DOI: 10.1016/j.pecs.2005.10.001. **Open access:** http://users.ntua.gr/vgiakms/pdf/PECS_2006.pdf

7. **Rakopoulos C.D., Hountalas D.T.**, “Development and validation of a 3-D multi-zone combustion model for the prediction of DI diesel engines performance and pollutants emissions”, SAE 981021, 1998. **Paywalled.**

8. **Zannis T.C. (Hellenic Naval Academy)** — co-author on SAE 2007-01-0120, SAE 2012-01-1725. Cited in Saadeldin M.A. et al., “Effects of Direct Water Injection on the Nitrogen Oxide Emission Characteristics of Marine Diesel Engines”, *J. Mar. Sci. Technol.* 31(2) (2023). **Open:** https://jmstt.ntou.edu.tw/cgi/viewcontent.cgi?article=2692&context=journal

9. **NTUA ICE Lab facilities & activities** — lab presentation PDF (open): https://tto.ntua.gr/wp-content/uploads/2021/04/presentation-internal-combustion-engines.pdf

10. **NTUA Fuels & Lubricants Lab** — lab page (open): https://www.chemeng.ntua.gr/en/lab/fuels-and-lubricants-technology-lab/

11. **OBI (Hellenic Industrial Property Organisation)** — general info, no specific water-injection patents found in open search: https://obi.gr/en/inventions/legislation-jurisprudence/law-1733-87 ; EPO federated register: https://epo.org/en/searching-for-patents/legal/register/documentation/federated-register/gr

12. **Athens bus fleet decarbonisation (current, for context)** — OASA 140 e-buses 2024, NTUA support: https://smart-cities-marketplace.ec.europa.eu/news-and-events/news/2024/athens-welcomes-arrival-140-new-electric-buses ; https://www.civitas.eu/news/athens-welcomes-the-arrival-of-140-new-electric-buses

13. **Thessaloniki bus fleet** — OASTH 110 e-buses 2024: https://www.upperprojecteu.eu/news/may-bring-new-e-buses-in-thessaloniki/

14. **Greek Hillclimb Championship** — general context (no water-injection data): Wikipedia “Hillclimbing”, Greek motorsport forums.

15. **International water–methanol injection references (for context only, not Greek)** — MW Steel article (Finland) with measured data: https://mwsteel.eu/en/mws-blog/technical-articles/water-methanol-injection ; Banks Power Pikes Peak: https://motorsport.com/hillclimb/news/gale-banks-and-mike-ryan-will-be-breaking-bad-at-pikes-peak

## 9. Limits and open questions

- **Patent gap:** Greek national patents (GR) are not fully searchable via open EPO/OBI interfaces. A visit to OBI archive or paid EPO register search would be needed to confirm/deny GR water-injection patents.
- **Paywalled SAE papers:** The core NTUA ICE Lab experimental/simulation results (SAE 2006-01-1414, 2007-01-0120, 2005-01-0377) are paywalled. No author preprints found on NTUA open archive (https://openarchives.gr). Requesting copies from authors (Hountalas, Giakoumis, Zannis) would close the data gap.
- **Motorsport:** Greek hillclimb/rally teams’ build sheets and dyno logs are not public. Contacting the Greek Motorsport Federation (OMOE) or top teams (e.g., SX Racing, Kotsovos Racing) could yield unverified but valuable practical data.
- **Marine:** Hellenic Naval Academy may have unpublished test-bed data for marine DWI/emulsion. Prof. Zannis (tzannis@hna.gr) is the contact.
- **Language barrier:** Some Greek-language conference papers (HELMEC, THERMEC, “Μηχανικά” journal) may contain additional data not indexed in English searches. A Greek-language deep search (Google Scholar with Greek terms) could surface more.
- **Time scope:** Search covered ~1990–2026. Pre-1990 Greek industrial water-injection activity (if any) not captured.
- **Negative results are not proof of absence** — only of absence in open sources searched.

---

---

# Verification (checker, not Hermes)

Checked 2026-11-11, about 3:20 PM America/Los_Angeles, after the first Greece job. Paywall rule (James t880u): legitimate open copies only; no piracy sites.

The draft correctly found **no Greek series-production road vehicle** with factory combustion-cycle water injection and correctly pointed to NTUA work: an Athens public-bus diesel-water emulsion trial and ICE-lab simulations of intake water injection and fuel-water emulsion. It attached **10–60% NOx** and **~2–4% BSFC** figures to SAE 2007-01-0120 that are **not in the official SAE abstract**. Those two Hountalas papers are official simulation studies, not opened hardware maps. The official 2007 abstract’s 30% NOx figure is a **study-design upper limit**, not a measured reduction.

## Confirmed (spot-checked)

- **No Greek OEM series-production passenger car, truck, or motorcycle** with factory combustion-cycle water injection or emulsion fuel was found. The draft’s aftermarket hillclimb mentions are secondary and not a measured Greek map. Pikes Peak figures in the draft are US, not Greek.

- **Tzirakis, E., Karavalakis, G., Schinas, P., Korres, D., Karonis, D., Stournas, S., and Zannikos, F., 2006**, *Diesel-water Emulsion Emissions and Performance Evaluation in Public Buses in Attica Basin*, SAE 2006-01-3398, DOI **10.4271/2006-01-3398**, published 16 Oct 2006. Official SAE Mobilus abstract. Affiliation: Laboratory of Fuels Technology and Lubricants, National Technical University of Athens. Official abstract: **4 public buses** operated in Athens; fuels were a typical Greek-market automotive diesel, a low-sulfur diesel, and a diesel-water emulsion of **13% v/v water in low-sulfur diesel**, characterized to EN 590. Official abstract: CO, unburned hydrocarbons and CO2 “did not show any significant differences among the three fuels”; “effects on NOx emissions can be termed as mixed, bearing also in mind that they represent engine operation at **no load**”; “the beneficial effect of the emulsified diesel fuel could be readily observed in the case of **smoke opacity** emissions.” No fuel-consumption percentage is in the opened official abstract. The official NTUA Research Committee project page (ref. 62159700, “PERFORMANCE OF EMULSIFIED DIESEL FUEL IN CITY BUSES”, financier ETHEL A.E., scientific responsible Prof. Stamoulis Stournas) describes a project running 10 Jan–10 Oct 2003 with a budget of €17,700 and says “**FIVE** city buses of the Thermal Bus Company of Athens will be employed.” The official SAE abstract reports results from **4** buses. https://doi.org/10.4271/2006-01-3398 ; https://www.elke.ntua.gr/en/research_project/performance-of-emulsified-diesel-fuel-in-city-buses/

- **Hountalas, D.T., Mavropoulos, G.C., and Zannis, T.C., 2007**, *Comparative Evaluation of EGR, Intake Water Injection and Fuel/Water Emulsion as NOx Reduction Techniques for Heavy Duty Diesel Engines*, SAE 2007-01-0120, DOI **10.4271/2007-01-0120**. Official SAE Mobilus abstract. This is a **multi-zone simulation** (the model had previously been used for EGR; it was modified here for intake water injection and fuel/water emulsion) on a heavy-duty diesel engine at various operating conditions. Official abstract: the three techniques are evaluated by reducing NOx “by the **same percentage**” versus baseline and then comparing the relative variation of BSFC and soot. “The **upper limit for NOx reduction was kept at 30%** to avoid deterioration of engine power output when using fuel/water emulsions since the configuration of the injection system is maintained in the present analysis.” The official abstract does **not** state a 10–60% NOx range or a ~2–4% BSFC penalty at 13–20% water. Those draft figures were **not taken**. Zannis’s Hellenic Naval Academy affiliation on later papers does not turn this NTUA simulation into a measured marine map. https://doi.org/10.4271/2007-01-0120

- **Hountalas, D.T., Mavropoulos, G.C., Zannis, T.C., and Mamalis, S., 2006**, *Use of Water Emulsion and Intake Water Injection as NOx Reduction Techniques for Heavy Duty Diesel Engines*, SAE 2006-01-1414, DOI **10.4271/2006-01-1414**. Official SAE Mobilus abstract. Also a **multi-zone simulation** of water-fuel emulsion versus intake-manifold water injection, “various percentages of injected water.” Official abstract: “a significant reduction of NOx with both techniques”; “the reduction is higher when using water-fuel emulsion compared to water injection in the intake manifold for the **same water percentage**.” A BSFC penalty is discussed qualitatively; soot “in some cases” may fall. **No numerical NOx or BSFC percentages** are in the opened official abstract. https://doi.org/10.4271/2006-01-1414

- **Giakoumis / Rakopoulos PECS 2006** (DOI 10.1016/j.pecs.2005.10.001) and the claimed author PDF at users.ntua.gr were not opened in this pass (the PDF URL returned 500). The draft’s “W/F=0.5 increases combustion irreversibility” figure was **not taken**.

- **Saadeldin et al. 2023** *J. Mar. Sci. Technol.* is a review that cites Greek SAE papers; it is not itself a Greek measured map.

## Errors and unverified claims in the Hermes draft

- **SAE 2007-01-0120 “NOx 10–60%” and “BSFC ~2–4% at 13–20% water.”** Not in the official SAE abstract. Official wording is a simulation comparison at a **30% NOx-reduction upper limit** chosen so emulsion cases would not lose power with a fixed injection-system configuration. Do not treat 10–60% or 2–4% as opened maps, and do not treat 30% as a measured hardware result.

- **“4–5 buses.”** Official SAE abstract: **4** public buses. Official NTUA project page: **five** buses “will be employed” in the 2003 project plan.

- **Paywalled SAE papers described as if they contained opened percentages.** The official abstracts were available on SAE Mobilus and were opened in this pass; the 10–60% / 2–4% figures still do not appear there.

- **PECS 2006 W/F=0.5 irreversibility** not taken; official author PDF not opened.

## Water Engine — what can actually be used

| Source | Open copy | What is usable |
| --- | --- | --- |
| Tzirakis et al. 2006, official SAE 2006-01-3398 abstract (DOI 10.4271/2006-01-3398); NTUA project page ref. 62159700 | Yes (abstract + project page) | NTUA Fuels and Lubricants Lab, Athens public buses, **13% v/v** water in low-sulfur diesel versus market diesel and low-sulfur diesel. Official abstract (**4 buses**): CO, HC and CO2 no significant differences; NOx mixed, at **no load**; smoke opacity clearly reduced. No fuel-consumption % in the opened abstract. Project page planned five buses in 2003. |
| Hountalas, Mavropoulos and Zannis 2007, official SAE 2007-01-0120 abstract | Yes (abstract) | NTUA **multi-zone simulation** comparing EGR, intake water injection and fuel/water emulsion on a HD diesel. Official abstract: compared at the same NOx-reduction percentage; **upper limit kept at 30% NOx** as a study-design cap to avoid emulsion power loss with a fixed injection system. Not a hardware map. Draft 10–60% / 2–4% not taken. |
| Hountalas et al. 2006, official SAE 2006-01-1414 abstract | Yes (abstract) | NTUA **multi-zone simulation**. Official abstract: significant NOx reduction with both emulsion and intake-manifold water injection; **higher NOx reduction with emulsion than intake WI at the same water percentage**. No numerical percentages in the opened abstract. |
| PECS 2006 author PDF; unpublished marine tests | Not opened | Not taken. |

Do not use: draft 10–60% NOx or ~2–4% BSFC; 30% as a measured engine result; PECS W/F=0.5 without the opened PDF; Pikes Peak or other foreign motorsport figures as Greek data.

## Link-check notes

Opened: official SAE Mobilus abstracts for SAE 2006-01-3398, 2007-01-0120 and 2006-01-1414; official NTUA Research Committee project page for 62159700. The Giakoumis PECS 2006 author PDF URL returned 500 in this pass. No piracy sites were used.
