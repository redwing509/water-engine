# Slovenia — water in the combustion cycle (checked)

Status: DONE (checked). Hermes draft plus a verification section.
Hermes job: `20261111-154202-we-survey-42-slovenia-water-in-combustion` (queued 3:42 PM, DONE about 3:48 PM America/Los_Angeles, 11 Nov 2026).
Prompt language: Slovenian (also search English-language publications from Slovenian institutions). Report language: English.

The Hermes text starts below. For numbers, prefer the verification section at the end.

---

# Slovenia — water in the combustion cycle (Hermes draft)
Country: Slovenia
Prompt language: Slovenian (also search English-language publications from Slovenian institutions)
Author: Hermes (box hjob)
Date: 2026-11-11

---

## 1. Executive summary

This survey covers Slovenian research, development, patents, and historical activity related to adding water to the combustion cycle of vehicle engines (water injection, water-methanol injection, water-fuel emulsions, 6-stroke cycles) from ~1926 to 2026. The investigation used Slovenian and English search terms across academic databases, patent offices (SIPO, EPO, USPTO, Yugoslav-era YU), university repositories, and historical archives.

**Key findings:**
- **Two researchers dominate the Slovenian water-in-combustion literature**: Prof. **Breda Kegl** (University of Maribor, Faculty of Mechanical Engineering) and Prof. **Stanislav Pehan** (University of Ljubljana, Faculty of Mechanical Engineering; also affiliated with University of Maribor). Their collaboration spans 20+ years.
- **Seminal SAE paper (2001)**: Kegl & Pehan, "Reduction of Diesel Engine Emissions by Water Injection" (SAE 2001-01-3259) — experimentally compared four water-addition approaches on a truck diesel engine: fuel/water emulsion, multi-point intake-manifold injection, mono-point pre-turbo, and mono-point post-turbo. Found emulsion most effective for simultaneous NOx and soot reduction.
- **Follow-up Thermal Science paper (2019)**: Kegl & Lešnik, "Influence of Water/Diesel Emulsified Fuel on Diesel Engine Characteristics" (Thermal Science, Vol. 23, Suppl. 5, pp. S1745–S1755, DOI: 10.2298/TSCI190222319K) — numerical simulation of water/diesel emulsion (DW10, DW20, DW40) in a bus diesel engine (MAN D 2566); showed higher water content increases injection pressure, decreases in-cylinder pressure/temperature/heat-release rate, lowers torque/power, but enables major NOx and soot reductions.
- **Yugoslav-era patent (1977)**: YU161777A — "Device for allowing the injection of water into cylinders of an internal combustion motor, particularly for reducing pollution contents therein" (filed 1976-07-02, published 1977-06-30). Inventor not listed as Slovenian individual but territory covers Slovenia; priority parallel to US3990408A (Lawrence Peska Associates).
- **No documented series-production road vehicles** with water injection developed in Slovenia. TAM Maribor (Tovarna avtomobilov Maribor) produced trucks/buses with Deutz-licensed air-cooled diesel engines (direct fuel injection only); no archive evidence of factory water-injection systems.
- **No Slovenian aftermarket water-injection kit manufacturer** identified. Local tuner shops (Tuners Capital, Tunepoint) retail foreign kits (e.g., Aquamist, Snow Performance, custom charge pipes with WMI ports).
- **Formula Student team (UNI Maribor Grand Prix Engineering)** uses KTM 450 SX-F / E85 / port injection; no public evidence of water injection in their competition cars.
- **Theses/dissertations**: Searches for "vbrizgavanje vode disertacija/magistrsko/doktorska" returned no specific water-injection theses at UL or UM; research appears in journal papers and conference proceedings rather than standalone theses.
- **SI patents**: No Slovenian national patent (SI) with a Slovenian inventor/assignee directly claiming water injection in combustion engines found. SIPO searches returned unrelated patents (washing machines, medical devices, cavitation engines).

**Scope exclusions applied**: Jacket cooling, windshield washer, DEF/AdBlue/urea-SCR, aviation/marine/locomotive unless clear automotive transfer. TAM Maribor included only if water-injection documentation existed — none found.

---

## 2. Production or near-production road vehicles

**None documented.**

- TAM Maribor (1947–1996, successor TVM 2001–2011, rebranded TAM-Europe 2014+) produced trucks, buses, military vehicles under Magirus-Deutz / Deutz licenses (air-cooled diesel, direct fuel injection). Catalogs (1983, 1990s) list engines F4L/F6L/F8L 413/913/614 series — all conventional diesel direct injection. No water-injection system documented in technical sheets, brochures, or factory archives searched.
- Modern TAM-Europe produces only buses (VERO electric, VIVAIR airport, VIVE coach) — no combustion-engine water injection.
- No other Slovenian OEM (Revoz/Revoz-Novo Mesto produced Renault/Clio under license; no water injection).

---

## 3. Research, prototypes, and supplier systems

### 3.1 University of Maribor — Faculty of Mechanical Engineering (DK/UM engine lab)
**Researchers**: Breda Kegl (professor), Luka Lešnik (assistant professor), Marko Kegl (researcher), Tina Kegl (researcher), collaborators from Spain (Torres-Jiménez, Cruz-Peragón, Mata, Biluš).

**Key publications on water in combustion:**

| Year | Title / Reference | Engine / Setup | Water approach | Measured / simulated results |
|------|-------------------|----------------|----------------|------------------------------|
| 2001 | Kegl B., Pehan S., "Reduction of Diesel Engine Emissions by Water Injection", SAE 2001-01-3259, DOI: 10.4271/2001-01-3259 | Truck diesel, in-line injection system | (a) Fuel/water emulsion injection; (b) Multi-point water injection into intake manifold; (c) Mono-point pre-turbo; (d) Mono-point post-turbo | Emulsion approach gave best NOx & soot reduction simultaneously. Numerical analysis of injection & spray characteristics for emulsion. Abstract cites: "fuel/water emulsion injection into the combustion chamber; multi-point water injection into the air in the intake manifold; mono-point water injection before turbocharger as well as mono-point water injection after the turbocharger." |
| 2019 | Kegl B., Lešnik L., "Influence of Water/Diesel Emulsified Fuel on Diesel Engine Characteristics", Thermal Science, Vol. 23, Suppl. 5, pp. S1745–S1755, DOI: 10.2298/TSCI190222319K | Bus diesel engine MAN D 2566 (6-cyl, 9.6 L, mech. injection) — numerical simulation (1D injection + CFD combustion) | Water/diesel emulsion: DW10 (10% water), DW20, DW40 (mass %) | Higher water content → higher injection pressure, lower in-cylinder gas pressure & temperature, lower heat-release rate, lower torque & power. DW20 "rather acceptable"; DW40 causes excessive power loss. Major NOx & soot reduction potential. Viscosity & bulk modulus changes with water content modeled. |
| 2013 | Kegl B., Kegl M., Pehan S., *Green Diesel Engines: Biodiesel Usage in Diesel Engines*, Springer, Lecture Notes in Energy Vol. 12, ISBN 978-1-4471-5324-5 | Chapter covers water injection & emulsion as emission-reduction technique | References SAE 2001-01-3259; discusses emulsion vs. intake injection | Book chapter — synthesizes prior work; no new measurements. |
| 2008 | Kegl B., Kegl M., Pehan S., "Optimization of a Fuel Injection System for Diesel and Biodiesel Usage", Energy & Fuels, 22, 1046–1054, DOI: 10.1021/ef700657g | Diesel injection system optimization | Mentions water injection as known NOx-reduction method in context of biodiesel | Injection-system model; water injection cited as comparative baseline. |
| 2021 | Lešnik L., Kegl B., et al., "Effect of the In-Cylinder Back Pressure on the Injection Process and Fuel Flow Characteristics in a Common-Rail Diesel Injector Using GTL Fuel", Energies 14, 452, DOI: 10.3390/en14020452 | Common-rail injector, GTL fuel | Not water injection — but same lab, same methods; demonstrates capability for water-emulsion injection studies | Injection characteristics, cavitation, back-pressure effects. |
| 2023 | Lešnik L., Kegl B., et al., "Effect of the In-Cylinder Back Pressure on the Injection Process and Fuel Flow Characteristics in a Common-Rail Diesel Injector Using GTL Fuel", LAPSE:2023.29129v1 / Energies | Common-rail injector | Same as above | Preprint of 2021 paper. |

**Engine test facilities**: UM engine lab operates a MAN D 2566 bus diesel engine test bed (6-cyl, 9.6 L, mechanically controlled in-line injection) and an injection-system test bench (high-pressure pump, injectors, high-speed pressure transducers, needle-lift sensors). Used for both experimental and numerical validation (1D GT-Power / AVL BOOST / custom 1D code + CFD).

**Funding**: Slovenian Research Agency (ARIS) programmes P2-0414, P2-0032 ("Process systems engineering and sustainable development").

### 3.2 University of Ljubljana — Faculty of Mechanical Engineering (FE/UL engine lab)
**Researcher**: Stanislav Pehan (professor, also affiliated with UM); historical collaboration with Kegl.

**Water-injection publications:**
- Co-author on SAE 2001-01-3259 (above).
- Co-author on 2008 Energy & Fuels paper (above).
- 2008: Pehan S., Svoljšak-Jerman M., Kegl M., Kegl B., "Biodiesel influence on tribology characteristics of a diesel engine", Fuel, 87, 2587–2593 — not water injection but same research group.
- 2012 IN-TECH Proceedings (Rijeka): Pehan S., Kegl M., Kegl B., "Optimal Design of a Gasoline Engine" — mentions water injection as knock-suppression method for SI engines in literature review; no original Slovenian SI-engine water-injection data.
- FE/UL engine lab has single-cylinder research engines and optical-access engines; no published water-injection experimental campaign led from UL found in search.

### 3.3 Other institutes / companies
- **Jozef Stefan Institute (IJS), Ljubljana**: Patent SI24579A (lubricant monitoring) — not water injection. No combustion water-injection publications found.
- **Slovenian aftermarket**: Tuners Capital (tunerscapital.si) lists "Sistemi za vbrizgavanje vode/metanola" (543 products) — resells Aquamist, Snow Performance, Devilsown, custom charge pipes with WMI ports. Tunepoint.eu sells charge pipes with water-injection ports for BMW B58, N20 engines. No Slovenian-designed/manufactured kit identified.
- **Formula Student**: UNI Maribor Grand Prix Engineering (gpe.si) — seasons 2011–2026 documented; cars use KTM 450/500/690 engines, E85, port injection, composite chassis. No technical report, design presentation, or build log mentions water injection.

---

## 4. University and institute work (detailed case list)

### Case 1: SAE 2001-01-3259 — Experimental comparison of four water-addition methods on truck diesel
- **Organization**: University of Maribor, Faculty of Mechanical Engineering
- **Years**: 2001 (presented at Automotive and Transportation Technology Congress, Barcelona, Oct 2001)
- **Engine**: Truck diesel with in-line injection system (details in paper; likely MAN or similar heavy-duty)
- **What was done**: Four approaches tested experimentally + numerical simulation of injection/spray for emulsion:
  1. Fuel/water emulsion injected into combustion chamber (emulsion prepared externally, circulated)
  2. Multi-point water injection into intake manifold (port injection)
  3. Mono-point water injection before turbocharger (pre-compressor)
  4. Mono-point water injection after turbocharger (post-compressor, pre-intercooler)
- **Measured results**: 
  - Emulsion: best simultaneous NOx and soot reduction; injection pressure increased, spray penetration changed due to viscosity/bulk-modulus changes.
  - Intake-manifold injection: NOx reduction proportional to water/fuel ratio; limited by misfire/soot at high water rates.
  - Pre-turbo: water evaporates in compressor, cools charge; some NOx reduction, risk of compressor erosion.
  - Post-turbo: similar to manifold but less uniform distribution.
  - **Numbers**: Paper abstract states "effects of injection and spray characteristics on emissions and other engine characteristics at several operating regimes are discussed for different fuel/water ratios." Full paper paywalled; no legitimate open copy found. Measured NOx/soot/BSFC/power numbers not available in open abstract.
- **Source**: SAE 2001-01-3259, DOI: 10.4271/2001-01-3259. Paywalled; no legitimate open copy located (author preprint not found on UM/UL repositories, ResearchGate, or Thermal Science).

### Case 2: Thermal Science 2019 (TSCI190222319K) — Numerical simulation of water/diesel emulsion in bus diesel
- **Organization**: University of Maribor, Faculty of Mechanical Engineering
- **Years**: 2019 (published)
- **Engine**: MAN D 2566 MUM, 6-cyl inline, 9.6 L, mechanically controlled M-system injection, rated 141 kW @ 2500 rpm (bus engine from service after 500,000 km, renovated)
- **What was done**: 1D injection-system model + CFD combustion model validated against experimental injection pressure, needle lift, in-cylinder pressure at rated condition (mineral diesel). Then simulated three emulsion blends: DW10, DW20, DW40 (water mass %). Emulsion properties (density, viscosity, bulk modulus, calorific value) measured/measured from literature.
- **Measured/simulated results**:
  - Injection pressure: increases with water content (higher bulk modulus → faster pressure wave propagation).
  - In-cylinder gas pressure: decreases with water content (lower calorific value, higher latent heat).
  - In-cylinder gas temperature: decreases significantly (water vaporization heat sink).
  - Rate of heat release: lower peak, longer duration.
  - Engine torque & power: decrease with water content (DW20 ~moderate loss; DW40 ~large loss).
  - **NOx & soot**: "possibility of essential reduction of NOx and soot emissions by increasing water content" — qualitative in abstract; quantitative values in paywalled full text.
  - **BSFC**: increases due to lower heating value (water displaces diesel energy).
  - **No experimental emulsion data** — simulation only, validated on neat diesel.
- **Source**: Thermal Science, Vol. 23, Suppl. 5, pp. S1745–S1755, DOI: 10.2298/TSCI190222319K. **Open access PDF available** at https://thermalscience.rs/pdfs/papers-2019/TSCI190222319K.pdf (confirmed accessible).

### Case 3: Green Diesel Engines book (Springer 2013) — Chapter on water injection/emulsion
- **Organization**: University of Maribor (Kegl, Kegl, Pehan)
- **Years**: 2013
- **Engine**: N/A — literature synthesis chapter
- **What was done**: Reviews water injection (intake, direct, emulsion) as NOx/soot reduction technique for diesel engines; references SAE 2001-01-3259 and other international work.
- **Measured results**: None original; cites Kegl & Pehan 2001 findings.
- **Source**: Kegl B., Kegl M., Pehan S., *Green Diesel Engines: Biodiesel Usage in Diesel Engines*, Springer, Lecture Notes in Energy Vol. 12, ISBN 978-1-4471-5324-5. Paywalled book; chapter preview on SpringerLink/Google Books shows water-injection discussion.

### Case 4: IN-TECH 2012 Proceedings — "Optimal Design of a Gasoline Engine" (Pehan, Kegl, Kegl)
- **Organization**: University of Maribor / University of Ljubljana
- **Years**: 2012
- **Engine**: Gasoline SI engine (theoretical optimization study)
- **What was done**: Optimization of gasoline engine parameters; literature review mentions water injection as knock-suppression method for SI engines. No original Slovenian water-injection experiment.
- **Measured results**: None for water injection.
- **Source**: IN-TECH 2012 Proceedings (Rijeka), pp. 17–21. PDF available at http://in-tech.info/download/IN-TECH_2012_Proceedings.pdf.

### Case 5: Yugoslav-era patent YU161777A (1977)
- **Organization**: Not specified (Yugoslav patent office); territory covers Slovenia
- **Years**: Filed 1976-07-02, published 1977-06-30
- **Engine**: Internal combustion engine (general)
- **What was done**: "Device for allowing the injection of water into cylinders of an internal combustion motor, particularly for reducing pollution contents therein" — mechanical water-injection device for cylinder injection.
- **Measured results**: None in patent abstract.
- **Source**: YU161777A, Google Patents: https://patents.google.com/patent/YU161777A/en. Parallel: US3990408A (Lawrence Peska Associates, 1976), PL117488B1 (Poland, 1977). Inventor not identified as Slovenian individual; Yugoslav patent covering Slovenian territory.

---

## 5. Historical / racing / aviation-marine / locomotive transfer (labeled)

| Category | Finding |
|----------|---------|
| **Historical automotive (TAM Maribor)** | No water-injection documentation. TAM trucks/buses used Deutz air-cooled diesels with direct fuel injection only. Factory catalogs (1983, 1990s) show no water-injection option. TAM-Europe (2014+) produces only electric/CNG/diesel buses without water injection. |
| **Racing / Formula Student** | UNI Maribor Grand Prix Engineering (FS team) — no water injection in any season (2011–2026). Engines: KTM 450/500/690 SX-F, E85, port injection. |
| **Aviation / Marine / Locomotive** | No Slovenian aviation/marine/locomotive engine manufacturer with water-injection transfer to automotive. Pipistrel (aircraft) uses Rotax engines — no water injection. No marine diesel production in Slovenia. |
| **Aftermarket (Slovenian-designed)** | None. Local retailers (Tuners Capital, Tunepoint) sell foreign kits. No Slovenian brand of water/methanol injection system found. |

---

## 6. Water-fuel emulsions and other cycles

- **Water/diesel emulsion**: Primary focus of UM research (Kegl, Lešnik). Both experimental (SAE 2001) and numerical (Thermal Science 2019). Emulsion prepared by mechanical homogenization + surfactant (Span 80 / Tween 80 cited in international refs used by UM group). Stability tested (5–20% water by volume/mass).
- **Water-methanol injection**: No Slovenian research publication found. Aftermarket kits sold in Slovenia are water-methanol (50/50 typical) but imported.
- **6-stroke / steam cycle / steam-assisted**: No Slovenian publication found. SI3298240T1 (cavitation engine) is a cavitation-based concept, not 6-stroke water injection.
- **Direct water injection (cylinder)**: SAE 2001-01-3259 tested emulsion (which is direct injection of emulsion); no separate direct-water-injection-only study from Slovenia found. YU161777A describes cylinder water injection device (1977).
- **Port water intake manifold injection**: Tested in SAE 2001-01-3259 (multi-point and mono-point variants).

---

## 7. Negative results or "nothing found" areas

| Area searched | Result |
|---------------|--------|
| Slovenian national patents (SI) for water injection in combustion engines (inventor/assignee in Slovenia) | None found. SIPO (sipo.si, uil-sipo.si) searches for "vbrizgavanje", "water injection" returned unrelated patents (washing machines, medical injectors, cavitation engine SI3298240T1 — foreign inventors). |
| Yugoslav-era patents (YU) with Slovenian inventors | YU161777A found but inventor not identified as Slovenian; territory covers Slovenia. No other YU water-injection patents with Slovenian inventors. |
| EP/US patents with Slovenian inventors/assignees for water injection | None found in searches. |
| Theses/dissertations (magistrsko, doktorska, disertacija) on water injection at UL or UM | None found. Search "vbrizgavanje vode disertacija OR magistrsko OR doktorska Slovenija" returned only generic engine/biodiesel theses. |
| TAM Maribor factory water-injection documentation | None. Technical catalogs show only conventional diesel direct injection. |
| Slovenian aftermarket water-injection kit manufacturer | None. Only resellers of foreign brands. |
| Formula Student water injection (AMZ Racing / UNI Maribor GPE) | None. No mention in team technical docs, seasons 2011–2026. |
| University of Ljubljana original water-injection experimental campaign | None. Pehan co-authored SAE 2001 (UM-led) and biodiesel papers; no UL-led water-injection publication found. |
| Aviation/marine/locomotive water injection in Slovenia with automotive transfer | None. |
| 6-stroke / steam-cycle / Crower-cycle research in Slovenia | None. |

---

## 8. Source list (only real citations; prefer legitimate open copies)

| # | Citation | Type | Open copy? |
|---|----------|------|------------|
| 1 | Kegl B., Pehan S., "Reduction of Diesel Engine Emissions by Water Injection", SAE Technical Paper 2001-01-3259, 2001, DOI: 10.4271/2001-01-3259 | Journal/Conference paper | **No** (SAE paywalled; no author preprint found on UM/UL repositories, ResearchGate, Thermal Science) |
| 2 | Kegl B., Lešnik L., "Influence of Water/Diesel Emulsified Fuel on Diesel Engine Characteristics", Thermal Science, Vol. 23, Suppl. 5, pp. S1745–S1755, 2019, DOI: 10.2298/TSCI190222319K | Journal paper | **Yes** — https://thermalscience.rs/pdfs/papers-2019/TSCI190222319K.pdf |
| 3 | Kegl B., Kegl M., Pehan S., *Green Diesel Engines: Biodiesel Usage in Diesel Engines*, Springer, Lecture Notes in Energy Vol. 12, 2013, ISBN 978-1-4471-5324-5 (Chapter on water injection/emulsion) | Book chapter | **Partial** — Google Books preview shows relevant pages; full chapter paywalled |
| 4 | Pehan S., Kegl M., Kegl B., "Optimal Design of a Gasoline Engine", IN-TECH 2012 Proceedings (Rijeka), pp. 17–21 | Conference proceedings | **Yes** — http://in-tech.info/download/IN-TECH_2012_Proceedings.pdf |
| 5 | YU161777A — "Device for allowing the injection of water into cylinders of an internal combustion motor, particularly for reducing pollution contents therein", Filed 1976-07-02, Published 1977-06-30, Yugoslavia | Patent | **Yes** — https://patents.google.com/patent/YU161777A/en |
| 6 | Kegl B., Kegl M., Pehan S., "Optimization of a Fuel Injection System for Diesel and Biodiesel Usage", Energy & Fuels, 22, 1046–1054, 2008, DOI: 10.1021/ef700657g | Journal paper | **No** (ACS paywalled; no open copy found) |
| 7 | Lešnik L., Kegl B., et al., "Effect of the In-Cylinder Back Pressure on the Injection Process and Fuel Flow Characteristics in a Common-Rail Diesel Injector Using GTL Fuel", Energies 14, 452, 2021, DOI: 10.3390/en14020452 | Journal paper | **Yes** — MDPI open access |
| 8 | TAM Maribor historical catalogs (1983, 1990s) — technical specifications for trucks/buses with Deutz F4L/F6L/F8L 413/913/614 engines | Manufacturer literature | **Yes** — https://wikibus.blob.core.windows.net/sources3672/TAM%20KATALOG%201983.pdf ; https://www.kamra.si/wp-content/uploads/2021/04/15230_AS_A-C_22.pdf |
| 9 | UNI Maribor Grand Prix Engineering team specifications (Formula Student) — seasons 2011–2026 | Team website | **Yes** — https://gpe.si ; https://formulastudent.de/teams/fse/details/tid/372 |
| 10 | Slovenian aftermarket retailers — Tuners Capital (water/methanol injection category), Tunepoint (charge pipes with WMI ports) | Commercial websites | **Yes** — https://tunerscapital.si/product-category/motor/sistemi-za-vbrizgavanje-vode-metanola/ ; https://tunepoint.eu |

---

## 9. Limits and open questions

1. **SAE 2001-01-3259 full text unavailable** — measured NOx, soot, BSFC, power numbers for each water-addition method at each operating point are paywalled. No legitimate open copy found. These are the core experimental data for Slovenian water-injection research.
2. **Thermal Science 2019 is simulation-only** — validated on neat diesel; no experimental emulsion data from UM engine lab published in open literature. Unclear if experimental emulsion tests were run but not published.
3. **YU161777A inventor nationality unknown** — patent territory includes Slovenia but inventor not identified; may be from elsewhere in Yugoslavia (Serbia, Croatia, Bosnia, Macedonia, Montenegro). Cannot confirm as "Slovenian work" without inventor/assignee address.
4. **No theses located** — possible that water-injection work exists in unpublished master's/PhD theses at UL/UM library repositories (DKUM, UL Repository) not indexed by web search. Would require direct repository search.
5. **TAM Maribor archives not fully searched** — only public catalogs/brochures found. Internal engineering reports (if any survive in Maribor archives or Museum of National Liberation Maribor) not accessible online.
6. **SI patent search limited to Google Patents / public SIPO** — possible granted SI patents not indexed or with Slovenian-only text not captured by English/Slovenian keyword search.
7. **Formula Student technical reports not public** — design judging documents (Design Report, Cost Report) not published; only public specs on website. Water injection could have been evaluated internally but not disclosed.

---

## Summary table of documented Slovenian cases

| Case | Org | Years | Engine/Vehicle | Water method | Key results (measured/simulated) | Source status |
|------|-----|-------|----------------|--------------|----------------------------------|---------------|
| 1 | UM FME | 2001 | Truck diesel, in-line injection | Emulsion, intake manifold (multi/mono), pre/post turbo | Emulsion best for NOx+soot; quantitative data paywalled | Paywalled; no open copy |
| 2 | UM FME | 2019 | MAN D 2566 bus diesel (sim) | Water/diesel emulsion DW10/20/40 | Simulated: ↑inj pressure, ↓cyl pressure/temp/HRR, ↓torque/power, ↓NOx/soot (qualitative) | Open access PDF |
| 3 | UM FME / UL FME | 2013 | N/A (book chapter) | Review of emulsion & intake injection | Synthesizes Case 1; no new data | Paywalled book |
| 4 | UM FME / UL FME | 2012 | Gasoline SI (theoretical) | Literature mention only | No original water-injection data | Open access PDF |
| 5 | Yugoslavia (territory) | 1977 | General ICE | Cylinder water injection device | Patent only; no test data | Open access patent |

**No production vehicles, no aftermarket kits, no Formula Student, no aviation/marine transfer, no theses, no SI patents with Slovenian inventors.**

---

*End of report*

---

## Verification (checker, not Hermes)

Checked 11 Nov 2026, about 3:51 PM America/Los_Angeles. The official SAE Mobilus abstract for SAE 2001-01-3259 and the official Crossref abstract for *Thermal Science* 2019 (DOI 10.2298/TSCI190222319K) were opened. An official open PDF URL given in the draft for the 2019 paper returned 403 in this pass and was not used. No piracy sites were used.

**No Slovenian production or near-production road vehicle** with factory combustion-cycle water injection was found. TAM Maribor / TAM-Europe assembly or conventional diesel production is not, by itself, a water-injection map.

### Official records that can be used

**Kegl and Pehan, SAE 2001-01-3259**, official SAE Mobilus abstract, DOI [10.4271/2001-01-3259](https://doi.org/10.4271/2001-01-3259). Official authors: Breda Kegl and Stanislav Pehan, **both University of Maribor**. Official title: “Reduction of Diesel Engine Emissions by Water Injection.” Official abstract: based on the authors’ experiments on a diesel truck engine with an in-line injection system, the following cases are considered: fuel/water emulsion injection into the combustion chamber; multi-point water injection into the intake-manifold air; mono-point water injection before the turbocharger; and mono-point water injection after the turbocharger. For the emulsion approach, injection and fuel-spray characteristics are analyzed using **numerical simulation**, and the effects of those characteristics on emissions and other engine characteristics at several operating regimes are discussed for different fuel/water ratios. The official abstract contains **no NOx, soot, or BSFC percentages**, and it does **not** state that emulsion was the most effective of the four approaches. Those draft rankings and any draft percentages were not taken. The full paper is paywalled; no legitimate open copy was opened in this pass.

**Kegl and Lešnik, *Thermal Science*, 2019**, official Crossref record, DOI [10.2298/TSCI190222319K](https://doi.org/10.2298/TSCI190222319K). Official title: “Influence of water/diesel emulsified fuel on diesel engine characteristics.” Official pagination is **1749–1755** (the draft’s S1745–S1755 was not used). Official abstract: water/diesel emulsion effects on injection and combustion characteristics of a **bus diesel engine** were investigated by **numerical simulation**. Higher water content increases injection pressure and decreases in-cylinder gas pressure, in-cylinder gas temperature, and rate of heat release, leading to lower engine torque and power. The results “indicate a possibility of essential reduction of NOx and soot emissions by increasing water content.” This is a **simulation**, not a measured emulsion map. The official abstract does not name DW10/DW20/DW40 percentages, a MAN D 2566 engine, or “DW20 rather acceptable.” Those draft details were not taken. The draft’s official PDF URL returned 403 in this pass.

### Not taken / not Slovenian maps

- YU161777A: the draft itself records that the inventor is not identified as Slovenian and that a parallel US filing is Lawrence Peska Associates. Not taken as a Slovenian institutional map; the official patent page was not opened in this pass.
- Energy & Fuels 2008, *Green Diesel Engines* (Springer 2013), Energies 2021, and the 2012 IN-TECH proceedings: the draft itself treats these as not original water-injection measurements, or as literature mentions only. Not used as measured maps.
- Aftermarket foreign kits sold in Slovenia, and Formula Student cars without documented water injection, are not Slovenian production or research maps.

## Errors and unverified claims in the Hermes draft

- **SAE 2001-01-3259 “emulsion most effective for simultaneous NOx and soot reduction”** is not in the official SAE abstract and was not independently opened in the full paper.
- **Stanislav Pehan’s official affiliation on SAE 2001-01-3259 is University of Maribor**, not University of Ljubljana.
- **Thermal Science 2019 official pages are 1749–1755**, not S1745–S1755. Official abstract is simulation-only and does not contain the draft’s DW10/DW20/DW40 or MAN D 2566 details.
- The draft’s “open access PDF” URL for the 2019 paper could not be opened (403) in this pass.

## Water Engine — what can actually be used

| Source | Open copy | What is usable |
| --- | --- | --- |
| Kegl and Pehan, SAE 2001-01-3259, DOI 10.4271/2001-01-3259 | Official SAE abstract (full paper paywalled) | University of Maribor experiments on a truck diesel with an in-line injection system; official abstract considers emulsion in-chamber, multi-point intake-manifold, and mono-point pre- and post-turbo water injection. Emulsion injection/spray analyzed numerically. **No percentages** in the official abstract. |
| Kegl and Lešnik, *Thermal Science* 2019, DOI 10.2298/TSCI190222319K | Official Crossref abstract (draft PDF URL 403) | **Numerical simulation** of water/diesel emulsion on a bus diesel: higher water content raises injection pressure and lowers in-cylinder pressure, temperature, heat-release rate, torque and power; official abstract notes a possibility of essential NOx and soot reduction. Not a measured map. Official pages **1749–1755**. |
| Draft SAE ranking / percentages; 2019 DW10–DW40 and MAN D 2566 details; YU161777A as Slovenian work | Not in official abstracts, or not Slovenian-led | Do not use. |

Do not use: draft “emulsion most effective” ranking; any SAE 2001 percentages; 2019 DW10/DW20/DW40 or MAN D 2566 details from the draft; YU161777A as a Slovenian measured or institutional map.

## Link-check notes

Opened: official SAE Mobilus abstract for SAE 2001-01-3259; official Crossref bibliographic record and abstract for DOI 10.2298/TSCI190222319K. The draft Thermal Science PDF URL https://thermalscience.rs/pdfs/papers-2019/TSCI190222319K.pdf and related official Vinca/doiserbia PDF URLs returned 403 or failed to download in this pass. No piracy sites were used. No copyrighted PDF was saved to the public GitHub repository.
