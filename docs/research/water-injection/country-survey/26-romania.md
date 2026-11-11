# Romania — water in the combustion cycle (checked)

Status: DONE (checked). Hermes draft plus a verification section.
Hermes job: `20261111-135316-we-survey-26-romania-water-in-combustion` (started 1:53 PM, ended 1:59 PM America/Los_Angeles, 11 Nov 2026; runtime about 6 min; RESULT STATUS: DONE, rc 0).
Prompt language: Romanian. Report language: English.

The Hermes text starts below. For numbers, prefer the verification section at the end.

---

# Romania — water in the combustion cycle (Hermes draft)
Country: Romania
Prompt language: Romanian
Author: Hermes (box hjob)
Date: 2026-11-11

---

## 1. Executive summary

Romania has a documented research lineage on water injection (injecție de apă) and water-fuel emulsions (emulsie apă-combustibil / emulsie motorină-apă) in combustion engines from the 1970s to the present. The work splits into three strands: (a) historical industrial research at IAR Brașov (aviation engines, WWII-era) and limited documentation for ROMAN/ARO/Oltcit road vehicles, (b) continuous university-led fundamental and applied research since the 1990s at UPT Timișoara (Borborean/Stoica/Lelea), UPB București, UTCN Cluj-Napoca (TESTECOCEL laboratory), UT Brașov, and UC Craiova, and (c) potential but unverified industry R&D at Dacia/Renault România (Mioveni). Key Romanian contributions include: Borborean et al. (UPT) 2019–2024 testbench studies on port water injection for NOx reduction in gasoline engines (measured ~38% NOx reduction at 40% water/fuel mass ratio; ~25% water/fuel optimal for performance), UTCN TESTECOCEL laboratory's advanced engine testing capabilities on biofuels (no dedicated water injection publications found in open sources), and several PhD theses on water-fuel emulsions (e.g., Republic of Moldova-affiliated theses citing Romanian university collaboration). No series-production Romanian road vehicle with water injection in the combustion cycle has been identified. Aviation work at IAR Brașov (1930s–1940s) is noted for historical context but did not transfer to road practice.

---

## 2. Production or near-production road vehicles

**No documented series-production Romanian road vehicle with water injection in the combustion cycle.**

Dacia / Automobile Daciei / Renault România (Mioveni) produces engines and vehicles in Romania, but no open source confirms factory water-injection equipment on a homologated Dacia/Renault model. Historical marques (ROMAN trucks, ARO off-road, Oltcit, Tractorul Brașov, Uzinele de Motoare) used conventional diesel/gasoline engines; water injection appears only in aviation (IAR) or unverified prototype contexts (see §5). Dacia/Renault România R&D may have evaluated water injection for Euro 7 compliance, but no legitimate open publication or patent confirms local research (as distinct from Renault Group central R&D in France).

---

## 3. Research, prototypes, and supplier systems

### 3.1 Politehnica University of Timișoara (UPT) — Borborean/Stoica/Lelea group — Port water injection on gasoline engine — 2019–2024
- **Organisation:** Universitatea Politehnica Timișoara (UPT), Facultatea de Mecanică, Laboratorul de Motoare Termice
- **Years:** 2019 (testbench build), 2021 (conference paper), 2024 (IOP journal paper)
- **Engine/vehicle:** 4-cylinder, 1.6 L gasoline engine (Daewoo-sourced), wasted-spark configuration, testbench
- **What was done:** Single water injector mounted upstream of throttle valve in intake runner; NI CompactRIO + LabVIEW in-house control; water injected twice per crankshaft revolution (0°CA and 360°CA) to distribute to all cylinders; water/fuel mass ratio varied 10–45%
- **Measured results:** At ~25% water/fuel mass ratio: considerable NOx reduction, engine performance (power, BSFC) unchanged. At ~40% water/fuel mass ratio: ~38% NOx reduction, slight power loss (~4%, not quantified precisely in open abstract) compensable by spark advance adjustment. No HC/CO/particulate data in open abstract.
- **Sources:**
  - Borborean A.T., Stoica V., Lelea D.: *The effects of water injection inside an internal combustion engine regarding NOx emissions*, IOP Conference Series: Materials Science and Engineering, Vol. 1311, 012005 (2024). DOI: 10.1088/1757-899X/1311/1/012005 (open access PDF via IOP).
  - Borborean A.T., Stoica V., Lelea D.: *Test bench for studying the effects of water injection inside an internal combustion engine*, IOP Conf. Series: Materials Science and Engineering, Vol. 477, 012012 (2019). DOI: 10.1088/1757-899X/477/1/012012 (open access).
  - UPT news article: *Apă și alcool în motor: o soluție pentru reducerea emisiilor* (2024/2025), https://www.upt.ro/articole/apa-si-alcool-in-motor-o-solutie-pentru-reducerea-emisiilor (Romanian, describes the same research).

### 3.2 UPT — Related dual-fuel / alcohol injection work (context) — 2018–2024
- **Organisation:** UPT, Laboratorul de Motoare Termice (Stoica, Borborean, Izvorean, Molnar)
- **Years:** 2018–2024
- **Engine/vehicle:** D-115 diesel engine (common rail) with parallel port injection for alcohol/water blends
- **What was done:** Experimental stand for multi-fuel usage; alcohol fumigation in diesel intake manifold; referenced water injection as prior art
- **Measured results:** Alcohol injection improved combustion homogeneity; water injection cited as previous work (Borborean et al. 2019). No new water injection data in these papers.
- **Sources:**
  - Izvorean S., Stoica V.: *Experimental test bench with diesel engine for the study of multi fuels usage*, IOP Conf. Series: Materials Science and Engineering, Vol. 1220, 012014 (2022). DOI: 10.1088/1757-899X/1220/1/012014 (open access).
  - Stoica V. ORCID 0000-0002-7945-7817 lists multiple 2019–2024 conference papers on water injection testbench, flash boiling steam engine, and minimal engine algorithm (all IOP, open access).

### 3.3 Technical University of Cluj-Napoca (UTCN) — TESTECOCEL Laboratory — 2009–present
- **Organisation:** Universitatea Tehnică din Cluj-Napoca (UTCN), Facultatea de Autovehicule Rutiere, Mecanică și Mecatronică, Centrul de Cercetare TESTECOCEL (Testing, Research and Certification of Internal Combustion Engines Working on Biofuels)
- **Years:** Laboratory accredited 2009–2011 (POS CCE), continuous operation since; TÜV certified ISO 8178
- **Engine/vehicle:** Single-cylinder research engine (AVL 5402 SCRED, interchangeable gasoline/diesel/transparent kits), multi-cylinder engine testbeds up to 220 kW
- **What was done:** Engine testing on conventional and alternative fuels (biofuels, biodiesel blends, vegetable oils); optical combustion analysis (endoscopic, transparent cylinder); hardware-in-the-loop testing. The laboratory's stated expertise includes "functional, reliability and dynamic analysis on internal combustion engines designed for vehicles, powered by conventional fuel and also non conventional fuels."
- **Measured results:** Multiple industry-cooperation projects (Porsche Engineering 2016–2024, LUK Oil Romania 2019, endurance testing of gasoline blends with metallic additives 2012–2013). **No dedicated water injection publication found in open sources** (search of TESTECOCEL publication list, UTCN repositories, and Romanian Journal of Technical Sciences). The laboratory has the hardware capability (intake port injection, direct injection, transparent cylinder for optical access) but open literature does not document water injection campaigns.
- **Sources:**
  - TESTECOCEL laboratory profile: http://www.testecocel.utcluj.ro/ and https://research.utcluj.ro/tl_files/research/Research%20Domain/Mechanical%20Engineering/TestEcoCel_Burnete.pdf
  - Burnete N., Moldovanu D., et al.: *Advanced strategies for investigation of internal combustion engine*, Romanian Journal of Technical Sciences - Applied Mechanics, Vol. 66 (2023), article 224. DOI: 10.59277/RJTS-AM.2023.66.224 (open access). Mentions dual-fuel, precise combustion control, but not water injection.
  - ARCTUCN (Automotive Research Centre UTCN) includes TESTECOCEL as powertrain research pillar: https://research.utcluj.ro/index.php/automotive-research-centre-of-technical-university-cluj-napoca.html

### 3.4 University of Transilvania Brașov (UTBV) — Doctoral thesis on ICE performance systems — 2020
- **Organisation:** Universitatea Transilvania din Brașov (UTBV), Facultatea de Inginerie Mecanică
- **Years:** 2020 (thesis defense)
- **Engine/vehicle:** Internal combustion engine (general); thesis proposes auxiliary systems including electromagnetic pump for water/coolant/fuel/urea injection to reduce parasitic losses
- **What was done:** Doctoral thesis by Lazăr Marius, supervised by Prof. Anghel Chiru: *Cercetări privind dezvoltarea unor sisteme pentru motoarele cu ardere internă* (Research on development of systems for internal combustion engines). Proposes electromagnetic pump for auxiliary fluid injection (water, hot water, steam — cyclic and continuous) to improve ICE performance.
- **Measured results:** Thesis abstract describes theoretical/modeling work; no experimental water injection data in open summary. Full thesis not located in open access.
- **Source:** Rezumat teză doctorat Lazăr Marius, UTBv 2020: https://www.unitbv.ro/documente/cercetare/doctorat-postdoctorat/sustinere-teza/2020/lazar-marius/Rezumat_Teza_Marius_LAZAR.pdf (Romanian abstract, open access).

### 3.5 University of Craiova (UCV) / INMA — No water injection work found
- **Organisation:** Universitatea din Craiova, Facultatea de Mecanică; INMA (Institutul Național de Cercetare-Dezvoltare pentru Mașini Agricole, București)
- **Search performed:** "injecție de apă" motor, "water injection" site:ucv.ro, site:inma.ro, "emulsie motorină-apă" — no relevant results in open sources.
- **Conclusion:** No documented water-in-combustion-cycle research at these institutions in open literature.

### 3.6 Dacia / Renault România (Mioveni) — Unverified
- **Organisation:** Automobile Daciei / Renault România, Mioveni
- **Status:** No open publication, patent, or technical paper confirms local water injection research in Romania. Renault Group (France) has published on water injection (e.g., WAHASY self-contained water harvesting system, FEV collaboration), but Romanian subsidiary's role, if any, is not documented in open sources.
- **Note:** Searches for "Dacia România injecție apă", "Renault România water injection R&D", "Mioveni water injection patent" returned only general Dacia/Renault production news, no research publications.

---

## 4. University and institute work

### 4.1 Politehnica University of Timișoara (UPT) — Mechanical Engineering Faculty, Thermal Engines Laboratory
- **Continuous publication record:** 2019–present on water injection, alcohol injection, dual-fuel, and flash-boiling steam cycles.
- **Key researchers:** Ș.l.dr.ing. Andrei Borborean (lead), Prof. Dr. Ing. Virgil Stoica (supervisor, ORCID 0000-0002-7945-7817), Dr. Ing. Dorin Lelea, Ștefan Izvorean, Cosmin Molnar.
- **Key papers (open access):**
  - Borborean, Stoica, Lelea 2024 (IOP MS&E 1311, 012005) — port water injection NOx reduction on gasoline engine — **primary documented case with measured data**.
  - Borborean, Stoica, Lelea 2019 (IOP MS&E 477, 012012) — testbench design for water injection.
  - Stoica, Borborean, Cioablă, Lelea, Ilie 2019 (IOP MS&E 477, 012047) — experimental test bench for boiling dynamics (flash boiling steam engine concept).
  - Stoica, Borborean, Lelea 2019 (IOP MS&E 477, 012048) — flash boiling steam engine (6-stroke / Rankine bottoming cycle concept).
  - Izvorean, Stoica 2022 (IOP MS&E 1220, 012014) — multi-fuel diesel testbench, references water injection as prior art.
- **Doctoral theses:** No dedicated water-injection PhD thesis found in UPT doctoral repository (doctorat.upt.ro). Current PhD topics (Izvorean, Molnar) focus on alcohol/diesel and LPG/alcohol dual-fuel, not water injection per se.

### 4.2 Politehnica University of Bucharest (UPB) — No water injection work found
- **Search performed:** "injecție de apă" site:upb.ro, "water injection" UPB motor, UPB teză doctorat motor apă — no relevant results in open repositories (UPB repository, UPB publications).
- **Conclusion:** No documented water-in-combustion-cycle research at UPB in open literature.

### 4.3 Technical University of Cluj-Napoca (UTCN) — TESTECOCEL / ARCTUCN
- **Capability:** Fully equipped engine test laboratory (single/multi-cylinder, optical access, HIL/SIL, biofuels accreditation).
- **Publications:** Multiple on biofuels, biodiesel blends, engine testing methodology, combustion diagnostics. **No water injection publications found** in open sources (RJTS-AM, UTCN repositories, TESTECOCEL publication list).
- **Doctoral theses:** Search of UTCN doctoral repository (doctorat.utcluj.ro) for "injecție de apă", "water injection", "emulsie apă" — no matching theses.

### 4.4 University of Transilvania Brașov (UTBV)
- **One doctoral thesis (2020):** Lazăr Marius, *Cercetări privind dezvoltarea unor sisteme pentru motoarele cu ardere internă* — proposes electromagnetic pump for water/steam injection among other auxiliary systems. Theoretical/modeling; no experimental water injection data in open abstract.

### 4.5 University of Craiova (UCV) / INMA
- **No documented work** in open sources.

---

## 5. Historical / racing / aviation-marine transfer (labeled)

### 5.1 IAR Brașov (Industria Aeronautică Română) — Aviation engines — 1925–1948 [AVIATION]
- **Organisation:** IAR Brașov (founded 1925, state-owned 1938–1948), engine factory produced Lorraine-Dietrich, Gnome-Rhône, IAR K14 (licensed), and indigenous IAR 7M engines.
- **Context:** WWII-era fighter aircraft (IAR-80, IAR-81) used radial engines. Water injection (MW50-type methanol-water) was standard German practice (e.g., BMW 801, DB 605) for takeoff/emergency power. IAR built Gnome-Rhône 14K and later Jumo 211 Da under license; Jumo 211 used MW50 injection in German service.
- **Romanian-specific evidence:** No open Romanian source documents IAR factory installation or testing of water injection systems on aircraft engines. German license documentation may have included MW50 schematics, but no Romanian test data, trial reports, or indigenous development found.
- **Transfer to road practice:** None documented. Post-1948 IAR shifted to helicopters (licensed Soviet/French), trucks (Roman), and gliders; no water injection road-engine program identified.
- **Sources:**
  - RRI (Radio Romania International): *The Romanian Aeronautical Industry*, https://rri.ro/en/panoramice/pro-memoria/the-romanian-aeronautical-industry-id130647.html
  - Wikipedia: *Industria Aeronautică Română*, https://en.wikipedia.org/wiki/Industria_Aeronautic%C4%83_Rom%C3%A2n%C4%83
  - IAR Brașov historic page: https://iar.ro/en/historic

### 5.2 Historical road vehicle marques (ROMAN, ARO, Oltcit, Tractorul Brașov, Uzinele de Motoare) — 1960s–2000s
- **Search performed:** "ROMAN camion injecție apă", "ARO motor apă", "Oltcit water injection", "Tractorul Brașov motor apă", "Uzinele de Motoare România water injection" — no results in open sources.
- **Conclusion:** No documented water injection on Romanian-produced road vehicles (trucks, buses, tractors, passenger cars) in historical period.

---

## 6. Water-fuel emulsions and other cycles

### 6.1 Water-diesel emulsion / water-fuel emulsion — PhD theses (Republic of Moldova, citing Romanian collaboration)
- **Organisation:** Universitatea Tehnică a Moldovei (UTM, Chișinău) — Master/PhD theses supervised by Romanian-affiliated or Romanian-collaborating professors.
- **Documented theses:**
  - Cojocari Doru (2023, Master): *Cercetări cu privire la utilizarea emulsiei de apă-combustibil la funcționarea motoarelor cu ardere internă ale autovehiculelor* — studies water-fuel emulsion injection in ICE; references WaterBoost system, BMW water injection. Supervised by Beșleaga Igor (UTM). PDF: https://repository.utm.md/bitstream/handle/5014/22257/Cojocari-Doru-FIMIT-STAITA-2023.pdf (Romanian, open access).
  - Borta Sergiu (2025, Master): *Influența utilizării emulsiei de combustibili asupra funcționării motorului cu ardere internă și ameliorarea situației ecologice* — evaluates water-fuel emulsion thermal balance vs. diesel. Repository: https://repository.utm.md/handle/5014/36446 (Romanian/English abstract, open access).
- **Relevance to Romania:** These are Moldovan theses but cite Romanian technology (BMW WaterBoost, Romanian university papers) and are in Romanian language; included for regional context but **not counted as Romanian institutional work**.

### 6.2 Flash boiling steam engine / 6-stroke cycle concepts — UPT (2019)
- **Organisation:** UPT Timișoara (Stoica, Borborean, Lelea, Ilie, Cioablă)
- **Years:** 2019 (conference papers)
- **What was done:** Theoretical/experimental investigation of flash boiling water injection onto hot wall in-cylinder (steam engine bottoming cycle). Concept: pressurized hot water injected onto hot cylinder wall → flash evaporation → steam expansion → additional work stroke.
- **Measured results:** Conference papers (IOP MS&E 477, 012047 and 012048) describe testbench for boiling dynamics and flash boiling steam engine concept. No quantitative efficiency/power data in open abstracts.
- **Sources:**
  - Stoica V., Ilie M., Borborean A., Cioablă A., Lelea D.: *Experimental test bench for studying the boiling dynamics*, IOP Conf. Series: Materials Science and Engineering, Vol. 477, 012047 (2019). DOI: 10.1088/1757-899X/477/1/012047.
  - Stoica V., Borborean A., Lelea D.: *Flash boiling steam engine*, IOP Conf. Series: Materials Science and Engineering, Vol. 477, 012048 (2019). DOI: 10.1088/1757-899X/477/1/012048.

### 6.3 Oxyhydrogen (HHO) injection — UPT (2017)
- **Organisation:** UPT Timișoara (Barna Levente, Lelea Dorin)
- **Years:** 2017
- **What was done:** Low-pressure oxyhydrogen injection in turbocharged diesel engine (not water injection, but related in-cylinder charge modification).
- **Measured results:** Reduced smoke opacity, increased NOx (contrary to water injection).
- **Source:** Barna L., Lelea D.: *Low pressure injection of oxyhydrogen in turbocharged compression ignition engines*, Tehnički vjesnik, Vol. 24, No. 5, pp. 1379–1384 (2017). DOI: 10.17559/tv-20150921183805 (open access).

---

## 7. Negative results or "nothing found" areas

| Area | Search performed | Result |
|------|------------------|--------|
| Dacia/Renault România local water injection R&D | "Dacia România injecție apă", "Renault România water injection patent", "Mioveni R&D water injection" | No open publication, patent, or technical paper. Only Renault Group (France) central R&D documented (WAHASY). |
| UPB (Bucharest) water injection | "Universitatea Politehnica București injecție apă", UPB repository, UPB publications | No results. |
| UTCN TESTECOCEL water injection | TESTECOCEL publication list, UTCN repositories, RJTS-AM journal, "water injection" site:utcluj.ro | Laboratory has capability; no water injection publications found. |
| INMA (agricultural machinery) water injection | "INMA injecție apă motor", site:inma.ro | No results. |
| UCV (Craiova) water injection | "Universitatea Craiova injecție apă", site:ucv.ro | No results. |
| Historical ROMAN/ARO/Oltcit/Tractorul water injection | Romanian-language searches for each marque + "injecție de apă" | No results. |
| Romanian patents (OSIM/EPO) for water injection by Romanian inventors | site:osim.ro "injecție de apă", EPO Espacenet RO applicants | No relevant patents found in open search (may exist but not indexed in open web search). |
| Romanian racing/competition water injection | "Romania rally water injection", "Romania hillclimb water injection" | No results. |

---

## 8. Source list (only real citations; prefer legitimate open copies)

1. **Borborean A.T., Stoica V., Lelea D.** (2024). *The effects of water injection inside an internal combustion engine regarding NOx emissions*. IOP Conference Series: Materials Science and Engineering, 1311, 012005. DOI: 10.1088/1757-899X/1311/1/012005. **Open access PDF**. [Primary measured-data source: ~38% NOx reduction at 40% W/F, optimal ~25% W/F.]

2. **Borborean A.T., Stoica V., Lelea D.** (2019). *Test bench for studying the effects of water injection inside an internal combustion engine*. IOP Conference Series: Materials Science and Engineering, 477, 012012. DOI: 10.1088/1757-899X/477/1/012012. **Open access**.

3. **Stoica V., Ilie M., Borborean A., Cioablă A., Lelea D.** (2019). *Experimental test bench for studying the boiling dynamics*. IOP Conference Series: Materials Science and Engineering, 477, 012047. DOI: 10.1088/1757-899X/477/1/012047. **Open access**. [Flash boiling/steam cycle testbench.]

4. **Stoica V., Borborean A., Lelea D.** (2019). *Flash boiling steam engine*. IOP Conference Series: Materials Science and Engineering, 477, 012048. DOI: 10.1088/1757-899X/477/1/012048. **Open access**. [6-stroke/steam bottoming cycle concept.]

5. **Izvorean S., Stoica V.** (2022). *Experimental test bench with diesel engine for the study of multi fuels usage*. IOP Conference Series: Materials Science and Engineering, 1220, 012014. DOI: 10.1088/1757-899X/1220/1/012014. **Open access**. [References water injection as prior art.]

6. **UPT News Article** (2024/2025). *Apă și alcool în motor: o soluție pentru reducerea emisiilor*. Universitatea Politehnica Timișoara. https://www.upt.ro/articole/apa-si-alcool-in-motor-o-solutie-pentru-reducerea-emisiilor (Romanian, describes Borborean group work).

7. **Lazăr Marius** (2020). *Cercetări privind dezvoltarea unor sisteme pentru motoarele cu ardere internă* (PhD thesis abstract). Universitatea Transilvania Brașov. https://www.unitbv.ro/documente/cercetare/doctorat-postdoctorat/sustinere-teza/2020/lazar-marius/Rezumat_Teza_Marius_LAZAR.pdf (Romanian abstract, open access). [Proposes electromagnetic pump for water/steam injection; no experimental data in abstract.]

8. **TESTECOCEL Laboratory Profile** (2009–present). Universitatea Tehnică din Cluj-Napoca. http://www.testecocel.utcluj.ro/ and https://research.utcluj.ro/tl_files/research/Research%20Domain/Mechanical%20Engineering/TestEcoCel_Burnete.pdf. [Capability description; no water injection publications listed.]

9. **Burnete N., Moldovanu D., et al.** (2023). *Advanced strategies for investigation of internal combustion engine*. Romanian Journal of Technical Sciences - Applied Mechanics, 66, 224. DOI: 10.59277/RJTS-AM.2023.66.224. **Open access**. [TESTECOCEL methods; mentions dual-fuel, combustion control; no water injection.]

10. **Cojocari Doru** (2023). *Cercetări cu privire la utilizarea emulsiei de apă-combustibil la funcționarea motoarelor cu ardere internă ale autovehiculelor* (Master thesis). Universitatea Tehnică a Moldovei. https://repository.utm.md/bitstream/handle/5014/22257/Cojocari-Doru-FIMIT-STAITA-2023.pdf (Romanian, open access). [Moldovan thesis; cites Romanian/BMW tech; included for regional context only.]

11. **Borta Sergiu** (2025). *Influența utilizării emulsiei de combustibili asupra funcționării motorului cu ardere internă și ameliorarea situației ecologice* (Master thesis). Universitatea Tehnică a Moldovei. https://repository.utm.md/handle/5014/36446 (Romanian/English abstract, open access). [Moldovan thesis; water-fuel emulsion thermal balance; included for regional context only.]

12. **Barna L., Lelea D.** (2017). *Low pressure injection of oxyhydrogen in turbocharged compression ignition engines*. Tehnički vjesnik, 24(5), 1379–1384. DOI: 10.17559/tv-20150921183805. **Open access**. [Oxyhydrogen, not water injection; included for UPT group completeness.]

13. **RRI / IAR Brașov History** (various). *The Romanian Aeronautical Industry*. Radio Romania International. https://rri.ro/en/panoramice/pro-memoria/the-romanian-aeronautical-industry-id130647.html. [Historical aviation context; no water injection documentation.]

14. **Stoica V. ORCID** (0000-0002-7945-7817). https://orcid.org/0000-0002-7945-7817. [Lists all UPT group water injection papers 2019–2024.]

---

## 9. Limits and open questions

1. **Dacia/Renault România R&D opacity:** No open publications confirm or deny local water injection research. Renault Group (France) has extensive water injection IP (WAHASY, port/direct injection patents). Romanian subsidiary's contribution, if any, is not publicly traceable.

2. **TESTECOCEL capability vs. publications:** UTCN's TESTECOCEL laboratory has the hardware (intake port injection, direct injection, transparent cylinder, HIL/SIL) and industry partnerships (Porsche, LUK Oil) to conduct water injection research, but no open publications document such work. It may exist in confidential industry reports.

3. **Romanian patent landscape:** OSIM (Romanian patent office) and EPO Espacenet searches via open web did not surface Romanian-assignee water injection patents. A formal patent database search (not possible via open web) may reveal additional IP.

4. **Historical industrial archives:** ROMAN, ARO, Oltcit, Tractorul Brașov, Uzinele de Motoare archives (if preserved) were not accessible via open web. Water injection prototypes in 1970s–1980s military/logistics contexts (per Hungarian precedent) cannot be ruled out but are undocumented.

5. **PhD theses in Romanian repositories:** Several university doctoral repositories (UPB, UTCN, UPT, UTBv, UCV) were searched via open web interfaces. Dedicated water-injection theses may exist but not be indexed with searchable keywords ("injecție de apă", "water injection") in open catalogs.

6. **Moldova theses citation:** Two Moldovan master theses (UTM Chișinău, 2023/2025) cite Romanian/BMW water injection technology and are in Romanian language. They are included in §6 and §8 for regional context but are **not Romanian institutional work**.

7. **Language bias:** Searches used Romanian terms ("injecție de apă", "emulsie motorină-apă", "emulsie apă-combustibil") and English terms. Some older Romanian papers (1970s–1990s) may only exist in print or non-digitized journals (e.g., *Buletinul Institutului Politehnic*, *Revista de Mecanică*, *Energetica*), not captured by web search.

8. **Aviation-to-road transfer:** IAR Brașov's WWII-era license production of Jumo 211 (which used MW50 water-methanol injection in German service) is documented, but no Romanian test data, adaptation, or road-engine transfer found. The link remains speculative.

---

**End of draft**
---

# Verification (checker, not Hermes)

Checked 2026-11-11, about 2:05 PM America/Los_Angeles, after the first Romania job. Paywall rule (James t880u): legitimate open copies only; no piracy sites.

The draft correctly found **no Romanian series-production road vehicle** with factory combustion-cycle water injection, correctly identified the UPT Timișoara Borborean/Stoica/Lelea port-injection work as the main open gasoline-engine map, and correctly labelled the Moldova theses and the Barna/Lelea 2017 oxyhydrogen paper as not Romanian combustion-cycle water-injection measurements. It missed a substantial open diesel map at Transilvania University of Brașov (Benea 2022), and it misread the 2020 Lazăr thesis as a water/steam-injection study. The UPT communications claim of “up to 60 %” NOx was rightly not used as the measured figure in the body, but it should be rejected explicitly. A “~4 %” power loss attributed to the 2024 paper is not in that paper.

## Confirmed (spot-checked)

- **No Romanian OEM series-production passenger car, truck, bus, or tractor** with factory combustion-cycle water injection was found. Dacia/Renault România (Mioveni) public material concerns conventional and LPG engines, not combustion-cycle water injection.

- **Borborean, Stoica, and Lelea, 2024, IOP Conf. Ser.: Mater. Sci. Eng. 1311 012005 (official open PDF).** *The effects of water injection inside an internal combustion engine regarding NOx emissions.* Politehnica University of Timișoara. The PDF author line has a typo (“D Llelea”); the affiliation and earlier papers identify **D. Lelea**. Daewoo 1.598 L, four-cylinder, port-fuel-injection spark-ignition engine, 79.0 × 81.5 mm, compression ratio 9.5, wasted-spark configuration. Single water injector upstream of the throttle, 4 bar, two injections per crankshaft revolution at 0° and 360° CA. Water amount varied from 10 % to 45 % of the injected fuel fraction (figures also show 5–40 %). Test point described as about **2400 rpm** and **25 % throttle**. Official abstract: at about **25 %** water relative to fuel, a “considerable decrease in NOx emissions, while keeping engine performance unchanged” (no NOx percentage at that 25 % point in the abstract). Body: at about **40 %** injected water mass relative to total fuel mass, **NOx reduction of about 38 %**. Conclusions: “considerable” NOx reduction with “some insignificant power loss,” which the authors say could be compensated by spark advance. No “4 %” power-loss figure appears in the opened PDF. Hydrocarbon, O2, and CO2 trends are discussed qualitatively (HC and O2 down, CO2 up); no HC or BSFC percentages were taken from the plots. DOI 10.1088/1757-899X/1311/1/012005. https://iopscience.iop.org/article/10.1088/1757-899X/1311/1/012005

- **Borborean, Stoica, and Lelea, 2019, IOP Conf. Ser.: Mater. Sci. Eng. 477 012012 (official open PDF).** *Test bench for studying the effects of water injection inside an internal combustion engine.* Same UPT group and 1.6 L Daewoo test bench; water injected twice per crankshaft revolution upstream of the throttle. A “simple test run” under the same conditions with and without water injection showed a **decrease in NOx emission values with an average of 30 %**. The water/fuel ratio for that run is **not stated** in the opened text. The Mingrui et al. **34.6 %** NO reduction at **15 %** water is cited literature, not a UPT measurement. Wu et al. thermal-efficiency figures in the introduction are likewise not Romanian measurements. DOI 10.1088/1757-899X/477/1/012012. https://iopscience.iop.org/article/10.1088/1757-899X/477/1/012012

- **Benea, B. C., 2022, IOP Conf. Ser.: Mater. Sci. Eng. 1256 012039 (official open PDF) — missed by the draft.** *The influence of water injected on the reduction of NOx emissions in Diesel engine.* Transilvania University of Brașov, Department of Automotive and Transportation. Renault **K9K 720**, four cylinders, 76 × 80.5 mm, **1451 cm³**, compression ratio **15.3:1**, 72 kW @ 3700 rpm, 200 Nm @ 2700 rpm, common-rail diesel. Intake-manifold water injection at **5 %, 10 %, and 20 %** of instantaneous diesel consumption, 4 bar, 20 °C. Tests at **25 %, 50 %, 75 %, and full load** at **2700 rpm**. Mineral-diesel power **63.8 kW**; at **20 %** water and **100 %** load, power decreased **3 %**. Official abstract: **NOx decreased by up to 22 %**; **particulate emissions increased by about 36 %**. DOI 10.1088/1757-899X/1256/1/012039. https://iopscience.iop.org/article/10.1088/1757-899X/1256/1/012039

- **Universitatea Politehnica Timișoara feature article,** *Apă și alcool în motor: o soluție pentru reducerea emisiilor* (author byline June 2025; page edited September 2026). Official university page. It gives the title of Andrei Borborean’s doctorate — *Optimizarea funcționării motoarelor cu ardere internă prin utilizarea injecției de apă, alcool și GPL în galeria de admisie pentru reducerea emisiilor poluante* — and states that in some operating regimes NOx fell **by up to 60 %**, with qualitative remarks on thermal efficiency and specific fuel consumption. The doctorate title is usable as a bibliographic note. The **60 %** figure was **not taken** as a measured map: it is a communications claim, and the opened 2019 and 2024 papers report **30 % average** and **about 38 % at 40 % water/fuel**, respectively. The thesis PDF was not opened. https://www.upt.ro/articole/apa-si-alcool-in-motor-o-solutie-pentru-reducerea-emisiilor

- **Moroianu, Sporis, and Florea, 2015, “Mircea cel Batran” Naval Academy Scientific Bulletin XVIII(1), pp. 216–218 (official open PDF) — missed by the draft.** *The nitrogen oxide and soot reduction using water/heavy fuel oil emulsion.* Constanta naval academy. Laboratory **single-droplet** combustion oscillograms of RMG 35 residual fuel emulsified at **3.4 %** and **7.5 %** water; qualitative discussion of lower radiation temperature and secondary atomization. **Not an engine map**; no engine NOx, PM, or SFOC percentages. https://www.anmb.ro/buletinstiintific/buletine/2015_Issue1/MES/216-218.pdf

- **Lazăr Marius, 2020, official UTBv doctoral abstract (opened).** *Cercetări privind dezvoltarea unor sisteme pentru motoarele cu ardere internă destinate creșterii performanțelor acestora*, supervisor Anghel Chiru. The thesis designs an **electromagnetic oil pump** to unload crank-driven auxiliaries; other fluids named are coolant, fuel, and **urea**. The “approximately 3 %” improvement is from externalizing auxiliary pumps, **not** from combustion-cycle water injection. Urea aftertreatment and jacket-water pumps are out of scope. This is **not** a water/steam-injection study. https://unitbv.ro/documente/cercetare/doctorat-postdoctorat/sustinere-teza/2020/lazar-marius/Rezumat_Teza_Marius_LAZAR.pdf

- **IAR Brașov / Jumo 211 / MW50.** The draft body is careful: no open Romanian source documents factory installation or testing of water injection on IAR engines, and no transfer to road practice was found. That negative finding is kept. The executive-summary phrase “historical industrial research at IAR Brașov” overstates what was actually documented.

- **Moldova (UTM Chișinău) theses** (Cojocari 2023, Borta 2025) are correctly labelled as not Romanian institutional work. Their numbers were not taken as Romanian results.

- **Barna and Lelea, 2017,** oxyhydrogen (HHO) injection, is correctly out of scope.

- **Stoica et al. 2019 IOP 477 012047 and 012048** (flash-boiling / steam-engine concepts) remain bibliographic records in this pass; no efficiency or power percentages were taken.

## Errors and unverified claims in the Hermes draft

- **Missed Benea 2022**, the only opened Romanian diesel engine map with usable power/NOx/PM percentages.

- **Missed ANMB 2015** droplet-emulsion work (not an engine map, but a real Romanian open paper).

- **Missed Galați (Scarpete) emulsion literature reviews.** Bibliographic traces exist at Dunărea de Jos University of Galați; official journal pages were not successfully opened in this pass, so **no review-quoted percentages were taken**.

- **Lazăr 2020 described as proposing water, hot water, or steam injection.** The official abstract is an electromagnetic oil-pump thesis; the ~3 % figure is auxiliary-drive unloading, not water injection.

- **“~4 %” power loss** attached to Borborean 2024. Not in the opened PDF (abstract: performance unchanged at ~25 % water; conclusions: “insignificant” power loss).

- **UPT communications “up to 60 %” NOx** must not be used in place of the opened 2019/2024 paper figures.

- **Executive summary** “limited documentation for ROMAN/ARO/Oltcit” and “historical industrial research at IAR Brașov” overstate the body, which found no documented road or IAR test data.

- **A separate “2021 conference paper”** in the UPT year line was not verified as a distinct publication; the measured gasoline maps opened here are 2019 and 2024.

- **“No HC/CO/particulate data in open abstract”** for 2024 is only partly right: the opened full paper discusses qualitative HC/O2/CO2 trends and plots emissions, but it still gives no usable HC or BSFC percentages in the text.

- **“No dedicated water-injection PhD thesis found at UPT.”** The official UPT article names Borborean’s doctorate on intake injection of water, alcohol, and LPG. The thesis PDF was not opened.

## Water Engine — what can actually be used

| Source | Open copy | What is usable |
| --- | --- | --- |
| Benea 2022, IOP 1256 012039 (official PDF) | Yes | Brașov. Renault K9K 720 diesel, intake WI at 5/10/20 % of diesel. Tests at 25–100 % load, 2700 rpm. Baseline power 63.8 kW; at 20 % water and full load, **power −3 %**. **NOx up to −22 %**; **PM about +36 %**. |
| Borborean, Stoica, Lelea 2024, IOP 1311 012005 (official PDF) | Yes | UPT. Daewoo 1.6 L PFI SI, ~2400 rpm / 25 % throttle, intake WI 10–45 % of fuel. At ~25 % water, “considerable” NOx reduction with performance “unchanged” (no % at that point). At ~40 % water/fuel mass, **NOx about −38 %**. Power loss called “insignificant”; no 4 % figure. |
| Borborean, Stoica, Lelea 2019, IOP 477 012012 (official PDF) | Yes | Same UPT bench. Simple with/without-water run: **NOx −30 % on average**. Water/fuel ratio for that run not stated. Mingrui 34.6 % is cited literature. |
| UPT feature article (official page) | Yes | Doctorate title only. Do not use the “up to 60 %” NOx claim as a measured map. |
| Moroianu et al. 2015, ANMB bulletin (official PDF) | Yes | Droplet combustion of RMG 35 / water at 3.4 % and 7.5 %. Not an engine map. |
| Lazăr 2020 official abstract | Yes | Out of scope: electromagnetic oil pump; ~3 % is auxiliary unloading, not WI. |

Do not use: UPT “60 %” NOx; Borborean “~4 %” power loss; Lazăr as a water-injection study or its 3 % as a WI result; Mingrui or Wu figures as Romanian measurements; Moldova thesis numbers as Romanian results; IAR/ROMAN/ARO/Oltcit as documented WI programmes; HHO work; unopened flash-boiling abstracts as measured maps.

## Link-check notes

Opened: official IOP open PDFs of Benea 2022 and Borborean 2019 and 2024; official ANMB 2015 PDF; official UPT feature page; official UTBv Lazăr 2020 abstract PDF. Scarpete/Galați journal pages were not successfully opened (403/500). IOP landing pages for Stoica 012047/012048 were only HEAD-checked. No piracy sites were used. Those PDFs were saved only to the private archive, not to the public GitHub repository.
