# How to beat Egypt's water-in-fuel efficiency figure (Attia and Kulchitskiy 2014): checked report

Requested by James, 11 Nov 2026: add Egypt as the Water Engine calibration reference for water mixed into the fuel, and start researching how to improve on its efficiency number. Written 11 Nov 2026 (America/Los_Angeles).

Method: done directly from official sources (no automated research draft was used). Same rule as the country survey: **a number is taken only if it was read in an official or legitimate open copy.** Figure readings are marked as such (read off the published plot, about ±0.01 absolute efficiency). Simulations, reviews and manufacturer-affiliated claims are flagged separately. No Sci-Hub or LibGen.

---

## 0. Bottom line

1. **The +20% is real in the paper, but it is a best-point figure from one unreplicated test series.** It is a figure maximum, not a map average. At several load points the gain is only about 10–13%. The paper does not define how "effective efficiency" was calculated, gives no repeat runs or error bars, and at the highest load tested at 2000 rpm the coarse emulsion matched the fine one. So the droplet-size claim does not explain the headline point.
2. **One open paper reports more than +20% thermal efficiency for a water-in-diesel emulsion:** Oliveira and Brójo 2024 (Portugal, *Energies*). It reports a mean of **+19.14%**, and its published curve reads about **+21% to +28%** at 1500–2500 rpm. **Low trust:** tiny 462 cc air-cooled single-cylinder engine at 2.4–2.8 kW, no droplet-size data, CO **+81%** and HC **+94%** at the same time, raw data only on request. Kyoto 2025 reads about **+19%** relative at 20 vol% water, but only at fixed injected volume and with about 20% less power. **No verified study beats +20% at equal power on a multi-cylinder engine.**
3. **Heavy-duty reality checks point the other way.** On a Caterpillar 3176, Lubrizol PuriNOx (20% water by mass) gave **−0.7%** brake specific energy consumption (SwRI/Lubrizol, SAE 2002-01-2891). The Texas DOT fleet test of 2 engines and 8 dump trucks found a fuel-efficiency **penalty of about 17%** (SAE 2004-01-0087). Large efficiency gains show up in small, low-efficiency research engines, not in modern heavy-duty ones.
4. **The droplet-size lever is disputed.** Attia found that finer droplets were better (D50 0.53 µm vs 5.5 µm). Kyoto 2025 (26.5–39.8 µm better than <3 µm) and Santoso 2024 (slower mixer and larger droplets, lower diesel-only fuel use) found larger droplets were better. The optimum is not settled.
5. **For Water Engine (naturally aspirated gasoline), Attia's mechanism mostly does not carry over.** Micro-explosion is a diesel-spray effect. In port-injected gasoline, the fuel evaporates before combustion. The only verified gasoline emulsion engine map found (Tornatore et al. 2021, turbocharged port-injected SI) gives **−3.7% / −7.1%** indicated fuel use at 10 / 20 vol% water. That gain came from knock relief that allowed stoichiometric operation and spark advance. Water injection gives the same knock benefit, and the RWTH data (3.3–4.5%; up to 16% at full load with an extrapolated baseline) remains the right Water Engine reference.

---

## 1. What produced Attia's +20%: verified from the official PDF

Source: Attia, A.M.A.; Kulchitskiy, A.R. *Fuel* 116 (2014) 703–708. DOI [10.1016/j.fuel.2013.08.057](https://doi.org/10.1016/j.fuel.2013.08.057). Official Benha staff PDF: https://beng.stafpu.bu.edu.eg/Mechanical%20Engineering/4109/publications/Ali%20Mahmoud%20Ali%20Atya_Fuel%20Vol%20116%20pp%20703-708%202014.pdf (read in full for this report).

**Engine and test (Section 2):**
- Turbocharged three-cylinder diesel, bore 105 mm, stroke 120 mm (≈3.12 L), **compression ratio 15**, on test bed SAK-H-670.
- Instruments: AVL-730 fuel-flow meter, RG-400 air-flow meter, AVL DiCom-4000 gas analyzer, AVL 415S smoke meter.
- No engine modifications except removing the fine fuel filter, so water droplets were not stripped out. Injection timing was **not** retuned.
- Test procedure: GOST R-41.96-2005 (stated as equivalent to UN ECE R96-01).
- Operating points (Table 1): **1500 rpm at 15–30 kW** and **2000 rpm at 3–35 kW**. Figure 7 shows 3 points at 1500 rpm (≈14.5 / 23 / 30.5 kW) and 4 at 2000 rpm (≈3.5 / 17 / 26 / 35 kW). The highest 2000 rpm point corresponds to about **6.7 bar BMEP**, so this is low-to-medium load for the engine, not rated power.

**Emulsion:**
- Ceramic tubular membranes: 6/10 mm inner/outer diameter, 22 cm long, 50% porosity, **0.2 µm or 0.45 µm pores**. Laminar flow, Reynolds number at most 800.
- Emulsifier: **0.5% by volume Span 80 (HLB 4.3, in the diesel) plus Tween 60 (HLB 14.9, in the water)**, mean HLB 9.2.
- Water content: **17% by volume**, as stated in the abstract and Section 2, and as "≈17%" in the Figure 5 caption. Table 1 lists "79.75% DF + 19.75% H2O + 0.5% emulsifier". That internal inconsistency stands; 17% is kept.
- **Measured droplet size (Figure 5, after one month):** 0.2 µm membrane → **D50 ≈ 0.53 µm**, δ ≈ 0.6. 0.45 µm membrane → **D50 ≈ 5.5 µm**, δ ≈ 0.9. The membrane pore size is not the droplet size: the "coarse" emulsion has droplets about 10 times larger than the fine one.
- Engine tests used emulsions **one month after preparation** (Figure 6 and 7 captions). An earlier Span 60/Tween 60 emulsion was stable for more than a month but was rejected for engine use because of condensed monolayers and a heating step.
- Viscosity rises with water content and with finer droplets (Figures 3 and 4).

**How "effective efficiency" is defined:** the paper plots η_e ("engine effective brake mechanical efficiency") but **gives no formula and no heating value** for the diesel or the emulsion. It is therefore not stated whether the water mass or the emulsifier was counted. If η_e is brake power divided by diesel energy input, which is the only meaningful version, η_e of 0.43 means about **197 g/kWh of diesel**. That would be exceptional for a compression-ratio-15, 3.1 L three-cylinder engine with a diesel baseline of 0.36–0.375 (about 225–235 g/kWh).

**Figure 7 readings (η_e, ±0.01):**

| Speed / power | Diesel | WFE-0.2 (D50 0.53 µm) | Gain | WFE-0.45 (D50 5.5 µm) |
|---|---|---|---|---|
| 2000 rpm, ≈3.5 kW | 0.105 | 0.135 | ≈+29% (3 points absolute) | ≈0.11 |
| 2000 rpm, ≈17 kW | 0.30 | 0.34 | ≈+13% | ≈0.29 |
| 2000 rpm, ≈26 kW | 0.335 | 0.37 | ≈+10% | ≈0.335 |
| 2000 rpm, ≈35 kW | 0.36 | ≈0.43 | ≈+19–21% | ≈0.435 (same as fine) |
| 1500 rpm, ≈14.5 kW | 0.315 | 0.39 | ≈+24% | ≈0.305 |
| 1500 rpm, ≈23 kW | 0.355 | 0.43 | ≈+21% | ≈0.385 |
| 1500 rpm, ≈30.5 kW | 0.375 | 0.42 | ≈+12% | ≈0.365 |

**Paper's own text (Results and Conclusions):**
- Finer droplets improve efficiency "at the entire range of working loads … up to 1.2 times" diesel. Coarser droplets help only at medium and high load.
- Smoke falls by more than 80% and HC by more than 35% with finer droplets.
- Coarser droplets give the larger NOx reduction, up to −25%. Finer droplets give **higher NOx than coarser ones**.
- The best emission effect is at more than 75% load.
- The paper says coarse droplets have a negligible effect on smoke at high speed.

**Limits and gaps in the paper:**
- One engine, 7 operating points, single runs, no uncertainty analysis, no in-cylinder pressure or heat-release data.
- No power-limit or full-load test.
- No storage or freeze test beyond one month at room temperature.
- The paper's own introduction says the WFE literature "did not show a high degree of reproducibility or consistency."

**Verdict on the +20% figure:** keep it as the reference target, labelled **"up to +20% (best points; 10–13% at several points), definition of η_e not stated, single unreplicated series."**

---

## 2. What later literature shows: verified measured results only

Basis: "diesel-only" means fuel use counted without the water mass. That is the correct basis for fuel cost.

| # | Study (official open source) | Engine | Water / droplets / emulsifier | Efficiency result | Other effects | Trust |
|---|---|---|---|---|---|---|
| A | **Attia & Kulchitskiy 2014**, *Fuel* 116 (Benha PDF above) | 3-cyl turbo diesel, CR 15 | 17 vol%; D50 0.53 vs 5.5 µm; 0.5% Span 80 / Tween 60 | η_e up to **1.2×** diesel (see table above) | Smoke >−80%, HC >−35% (fine); NOx up to −25% (coarse) | Medium: official, but single series and η_e undefined |
| B | **Oliveira & Brójo 2024**, *Energies* 17:1328, DOI [10.3390/en17061328](https://doi.org/10.3390/en17061328) | Hatz 1B40 single-cyl, 462 cc, air-cooled DI, CR 20.5, 7.3 kW rated; tested 1500–3000 rpm at ≈2.4–2.8 kW | 8% water; 91% Cocamide DEA + 9% Span 80 (hydrophilic blend tuned at 40 °C); low-energy stirring; **droplet size not reported** | Mean SFC **−7.57%** (emulsion mass), mean TE **+19.14%**. TE computed with emulsion LHV = 91.16% of diesel. Figure 16 reading: ≈+21% (1500), **≈+28% (2000)**, ≈+21% (2500), ≈+7% (3000 rpm). Equivalent diesel-only SFC ≈ −16% (derived) | NO −20.5%, smoke −75.2%, but **CO +81%, HC +94%** | **Low**: exceeds +20% only as reported; small engine; eddy-current brake ties load to speed; combustion-completeness data contradicts the efficiency claim |
| C | **Mukhtar et al. 2025** (Kyoto/Kindai), *J. Therm. Sci. Tech.* 20(1), DOI [10.1299/jtst.24-00385](https://doi.org/10.1299/jtst.24-00385) | Single-cyl air-cooled DI diesel, 2300 rpm, fixed governor and **fixed injected volume** (12.6 mm³/cycle) | 2–24 vol%; SMD <3 µm (stirring) vs 26.5 µm and 39.8 µm (Shirasu porous-glass membranes); 2 vol% surfactant, HLB 6 | Efficiency rises up to 14 vol% (<3 µm) and **20 vol% (26.5/39.8 µm)**, then falls. Figure 6 reading: diesel ≈31%, 39.8 µm at 20 vol% ≈37% (≈+19% relative). **<3 µm emulsions were below diesel** at most water contents | Power falls (≈2.85 → ≈2.3 kW); NOx and soot down; CO up | Medium: official; not an equal-power comparison |
| D | **Santoso et al. 2024**, *Automotive Experiences* 7(1):132–148, DOI [10.31603/ae.10907](https://doi.org/10.31603/ae.10907) (already in survey) | Small single-cyl diesel, 2000 rpm, 75% load (3.23 kW) | 15% water, **surfactant-free** inline mixer; mixer speed sets droplet size | BSFC **−13.3%** (694.98 → 602.52 g/kWh) at best point, **diesel-only basis** (paper §3.3.3 and Figure 8). On emulsion-mass basis BSFC **rose** 6.4–10.1% on average. Baseline ≈695 g/kWh (≈12% efficiency) | Power −1%, NOx −30%; emulsion begins separating after about **1.5 min** | Medium: official; very low-efficiency baseline inflates relative gains |
| E | **Tornatore et al. 2021** (CNR-STEMS / Nantes), *Appl. Sci.* 11:9453, DOI [10.3390/app11209453](https://doi.org/10.3390/app11209453) | **Gasoline**, turbo port-injected 2-cyl 875 cc, CR 10, 3000 rpm, IMEP 16 bar | 10 and 20 vol% water; micro-channel emulsifier (inline-capable), but the test batch was made offline with **0.2% Span 80** | Gasoline-only ISFC **−3.7% (10%) / −7.1% (20%)** vs the factory rich (λ 0.9) knock-limited point, **only** after moving to λ 1.0 and advancing spark to the new knock limit. At the same spark and λ, emulsion ISFC was **worse** (longer combustion) | HC slightly up; **NO up** at stoichiometric | Medium-high: official, careful method; indicated (not brake) |
| F | **Matheaus et al. 2002** (SwRI/Lubrizol/Sandia), SAE 2002-01-2891, [abstract](https://doi.org/10.4271/2002-01-2891) | Caterpillar 3176 heavy-duty, 8-mode | PuriNOx, 20% water by mass | Brake specific energy consumption **−0.7%** | NOx −19%, PM −16% | Manufacturer-affiliated; abstract only (paywalled; no open copy found) |
| G | **Matthews et al. 2004** (UT Austin/SwRI/TxDOT), SAE 2004-01-0087, [abstract](https://doi.org/10.4271/2004-01-0087) | 2 engines + 8 TxDOT dump trucks, mechanical and electronic | PuriNOx | Fuel-efficiency **penalty ≈17%** on average (the abstract does not state whether this is per volume of emulsion or per unit of energy) | NOx −16%, PM −20%; higher formaldehyde, acetaldehyde, acrolein and MEK | Real fleet; abstract only |

**Secondary or abstract-level, not taken as maps:**
- **Vellaiyan & Amirthagadeswaran** (*Energy Sources A* 37(18), 2015; paywalled). The official abstract says that at CR 15–16 the emulsion gave incomplete combustion and rough running, while CR 17–18 was comparable to diesel, with "significant improvements" in BSFC and BTE. The open 2025 *Carbon Research* review (Nnadozie et al., DOI [10.1007/s44246-025-00210-y](https://doi.org/10.1007/s44246-025-00210-y)) quotes average BTE gains of **+12% at CR 18 vs +3.7% at CR 15** for 10% water. Secondary figure; use as a direction only.
- **Same review, other quoted results (all secondary):** Abu-Zaid 2004 about +3.5% BTE at 20% water; Jhalani 2019 optimum 15% water (23.35% vs 21.86% BTE), with severe knock at 20%; Mondal & Mandal 2019, ultrasonic preparation +3% vs mechanical homogenizer −20% BTE at the same 10% water.
- **Nanoparticle-dosed emulsions (abstracts):** *Designs* 8(1):3 (2024), 2.5% water + 50 ppm 11 nm Al₂O₃: BTE **+7.94%** at maximum load, while water alone **reduced** BTE. UPM (Malaysia) B5 + 3% water + 90 ppm CeO₂: BTE **+11%** vs B5. Both are well below +20% and add engineered nanoparticles to the exhaust.
- **Gowrishankar et al. 2020**, SAE 2020-32-2312 (abstract): 3% water nanoemulsion gives about **+5%** BTE; emulsion beat port water fumigation on smoke.
- **Hassan et al. 2021** (PMC10358454, open): 2–10% water, BTE **down** as much as 13% and BSFC up as much as 32%. This paper notes that some studies claiming gains counted only the diesel mass in BSFC. That is legitimate for fuel cost, but it is not comparable to total-mass BSFC.
- **Peters & Stebar 1976** (GM), SAE 760547 (abstract): water-in-gasoline emulsions raised octane and cut NO, but HC rose, driveability fell, and the polyoxyethylene emulsifier gave poor stability and **rapid engine deposits**.

**Is there any paper that already beats +20%?** Only Oliveira & Brójo 2024 does, as reported (low trust; see row B). Nothing at equal power on a multi-cylinder or production-class engine was found.

---

## 3. Improvement levers, ranked by evidence (diesel emulsion path)

1. **Fix measurement first, then optimize.** Replicate Attia's 17% fine and coarse emulsions on one engine: equal brake power, stated LHVs, diesel-only BSFC and energy-specific consumption, 3 or more repeats, full load included. Without this, no claimed "improvement" can be compared to +20%. *(Evidence: Attia's undefined η_e; spread across rows A–G.)*
2. **Water fraction about 14–20 vol%, not more.** Kyoto found efficiency peaks at 14 vol% (fine) and 20 vol% (coarse) and falls beyond that. Jhalani's optimum was 15%, with knock at 20%. Attia used 17%, which is already in the window, so there is little upside here; this lever is mainly about not overshooting. *(Strong, consistent.)*
3. **Pair the emulsion with higher compression ratio or retuned injection timing.** Attia ran CR 15 with stock timing. Vellaiyan found CR 15–16 rough and CR 17–18 good, with a quoted +12% vs +3.7% (secondary). Emulsions lengthen ignition delay, so advancing injection is the obvious untested lever. *(Moderate; the main untested upside.)*
4. **Droplet-size sweep, not "smaller is better."** Attia found 0.53 µm better than 5.5 µm. Kyoto found 26.5–39.8 µm better than <3 µm, and Santoso found larger droplets better. A membrane sweep from about 0.5 to 40 µm at a fixed 17% is needed. Nanoemulsions (<0.2 µm) have **no verified map above about +5–8%**. *(Conflicting; important to test.)*
5. **Emulsifier choice and surfactant-free inline mixing.** Hydrophilic blends tuned to fuel temperature claim large gains but are low-trust (row B). Surfactant-free inline mixers (Santoso; Tornatore's micro-channel device) remove surfactant cost and the deposit risk Peters & Stebar saw, but the mix must be made at the engine because it separates in minutes to hours. *(Moderate; key for fleet practicality.)*
6. **Nano-additives (Al₂O₃, CeO₂):** +8–11% vs the base fuel in abstracts, with nanoparticle exhaust and EPA/fuel-registration issues. **Not recommended.**

**Trade-offs each path has to report** (from Attia and rows B–G):
- Finer droplets: efficiency, smoke and HC improve, but **NOx is higher** than with coarse droplets.
- More water: NOx and soot fall, but **CO and HC rise** (Kyoto, Oliveira, Santoso) and power falls at fixed injection volume (Kyoto).
- Advancing timing or raising compression ratio raises NOx (Tornatore: NO up at stoichiometric and advanced spark).
- Stability: Santoso begins separating in about 1.5 min; Tornatore lasts some hours; Attia's surfactant emulsion lasts about a month.
- Freezing and corrosion: **no opened paper measured cold storage, freeze or fuel-system corrosion.** Water freezes at 0 °C, so a Spokane fleet needs on-vehicle inline mixing from a heated or antifreeze-protected water tank (as DEF tanks already do), or a separate water-injection system. This is an engineering requirement, not a measured result.

---

## 4. What applies to Water Engine (naturally aspirated gasoline)

- **Different physics.** Attia's gain is attributed to micro-explosion and secondary atomization of diesel spray in hot compressed air. In a port-injected gasoline engine, the fuel is vaporized before ignition, so that mechanism mostly disappears. What remains is charge cooling and knock relief, and port or direct water injection already delivers those, with water metered by load.
- **Verified gasoline emulsion number:** Tornatore 2021, −3.7% / −7.1% indicated fuel use at 10 / 20 vol% water. The gain came only from knock-limited spark advance plus leaving enrichment. At fixed spark, emulsions were **worse**. NO rose at stoichiometric and HC rose slightly. This is the same mechanism and size as the RWTH water-injection references.
- **Fixed-ratio emulsion is a poor fit for naturally aspirated gasoline.** Water helps only near the knock limit and hurts burn rate at part load. A fixed blend in the tank would penalize most driving. If an emulsion is pursued, it should be **inline and variable-ratio** (Tornatore's micro-channel concept) and active only at high load.
- **Water Engine's modelled −9.7% cost per mile relies on compression ratio rising from 8 to 12.** No emulsion paper measures that on a naturally aspirated gasoline engine. The model's water mass fraction of 0.30 (water-to-fuel ratio 0.43, ≈25–30 vol% in an emulsion) is beyond every gasoline emulsion tested (≤20 vol%).
- **Recommendation:** keep Attia as the water-in-fuel reference for diesel and fleet-diesel work. For Water Engine itself, the calibration targets remain RWTH (gasoline direct water injection) and Tornatore 2021 (gasoline emulsion, new supporting reference). Treat "beat +20%" as a **diesel-emulsion side project**, starting with the replication in lever 1.

---

## 5. Ranked improvement paths (summary)

| Rank | Path | Applies to | Verified evidence | Expected realistic gain | Key risk |
|---|---|---|---|---|---|
| 1 | Replicate Attia with equal-power, energy-basis accounting | Diesel emulsion | Attia (gaps), Matheaus (−0.7%), Matthews (≈17% penalty) | Establishes whether +20% is real | It may shrink toward single digits |
| 2 | 17% emulsion + CR 17–18 and/or advanced injection timing | Diesel emulsion | Vellaiyan abstract and review (+12% vs +3.7%, secondary) | Only path with a plausible route above Attia | NOx up; untested combination with Attia's droplets |
| 3 | Droplet-size sweep from about 0.5 to 40 µm by membrane | Diesel emulsion | Attia vs Kyoto vs Santoso (conflict) | Finds the real optimum | Fine droplets raise NOx |
| 4 | Surfactant-free inline mixing | Diesel and gasoline fleets | Santoso; Tornatore | Removes surfactant cost, deposits and storage separation | Needs on-vehicle hardware |
| 5 | Inline variable-ratio water-in-gasoline at knock limit only | **Water Engine** | Tornatore (−3.7 / −7.1% ISFC) | ≈4–7% at knock-limited high load | No naturally aspirated or CR 12 data; NO and HC up |
| 6 | Hydrophilic surfactant blends | Diesel emulsion | Oliveira & Brójo (low trust) | Claimed about +19–28% | CO and HC up sharply; not replicated |
| 7 | Nanoparticle additives | Diesel emulsion | Abstract-level (+8–11%) | Small | Nanoparticle exhaust; regulation — **not recommended** |

---

## 6. Corrections and citation notes

- **Automated drafts:** none were used, so there are no draft errors to correct in this report.
- **Calibration note ([calibration-references-20261111.md](calibration-references-20261111.md)), Attia:** "0.2 µm and 0.45 µm" are **membrane pore sizes**. Measured droplet D50 values were **0.53 µm and 5.5 µm** (Figure 5). Added here; the calibration note should cite D50 values when describing droplet size.
- **Attia's +20% framing:** the figure is a best-point maximum. Several load points show about +10–13%, and at 2000 rpm/35 kW the coarse emulsion equalled the fine one. η_e is not defined in the paper.
- **Santoso 2024 (Indonesia survey note):** the −13.3% BSFC is on a **diesel-only basis**. On an emulsion-mass basis, BSFC was higher than diesel (+6.4% to +10.1% on average). The baseline BSFC was ≈695 g/kWh (≈12% efficiency), so relative gains are inflated by the low baseline. In this paper the better-performing emulsion was made at the slower mixer speed, which gives larger droplets.
- **Tornatore 2021:** the abstract says "without addition of surfactants," but the tested batch used 0.2% Span 80, made offline.

## 7. Sources opened for this report

Official open PDFs read (PDFs are not copied into this repository):
- Attia & Kulchitskiy 2014, *Fuel* 116:703–708, official Benha staff PDF (URL above).
- Oliveira & Brójo 2024, *Energies* 17:1328 (MDPI OA PDF).
- Tornatore et al. 2021, *Appl. Sci.* 11:9453 (MDPI OA PDF).
- Mukhtar et al. 2025, *J. Therm. Sci. Tech.* 20(1), 24-00385 (J-STAGE official PDF).
- Santoso et al. 2024, *Automotive Experiences* 7(1):132–148 (official OA PDF).

Official abstract or landing pages opened:
- SAE 2002-01-2891 (Matheaus et al.) and SAE 2004-01-0087 (Matthews et al.): doi.org pages.
- *Carbon Research* 2025 OA review (Nnadozie et al.), Springer page.
- PMC10358454 (Hassan et al. 2021).

Abstract-only via search (not separately opened, used only as listed in §2):
- Vellaiyan & Amirthagadeswaran 2015 (T&F abstract).
- *Designs* 8(1):3 (2024).
- UPM CeO₂ repository abstract.
- SAE 2020-32-2312.
- SAE 760547.
