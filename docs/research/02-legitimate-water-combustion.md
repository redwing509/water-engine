# 02 — Legitimate water use in combustion engines (WME-1 research note)

**Framing.** WME-1 burns methanol or ethanol. Water in its intake supplies no chemical energy: it is a fully oxidised combustion product with zero heating value, so all work must be paid for by the alcohol's LHV (methanol 20.09 MJ/kg, ethanol 26.95 MJ/kg [53]).
Water can legitimately suppress knock, cool the charge, add steam-expansion work recovered from waste heat, and cut NOx. The literature below quantifies each of these, and any claim of net energy *from* water (HHO "water fuel", water-powered cars) is treated as a claim to debunk.
Liquid-intake water fractions above 50 % by mass have precedent: injected water at water/fuel mass ratios up to 1.5 in 1940s SI aircraft cylinders [1], and 40 % ethanol-in-water in HCCI [10]. No source found shows an alcohol-fuelled SI engine operating there.

*Compiled 2026-10-21. Every number carries a numbered source. "Derived" marks arithmetic done here on sourced numbers. "Secondary" marks press, wiki or review sources. "Not found" means the value was searched for and not located in an accessible source.*

---

## 1. Water and water–methanol injection in SI engines

### 1.1 WWII anti-detonation injection (ADI)
- NACA Report 756 (1942) inducted water into a single-cylinder aircraft engine (202 in³, CR 7.0, 2000 rpm, 20° BTC spark, 250 °F inlet air). It found that "water injection allowed a fuel to be operated above its normal maximum permissible performance limits" [1].
- Water/fuel mass ratios of 0.2, 0.4 and 0.6 were run on AN-F-28 fuel. At fuel/air 0.067, W/F = 0.6 raised knock-limited IMEP from 180 to 305 psi (+69 %, derived) [1]. With 80-octane gasoline the ratio went up to 1.5, reaching 263.4 psi IMEP [1]. The report estimated that W/F = 0.6 let an engine needing 100-octane fuel run on 80-octane fuel [1]. The OCR of the scan is partly garbled, so its percentage tables should be checked against the original figures [1].
- NACA ARR E4H31 (1944; Wright C9GC cylinder, CR 7.0, 100-octane fuel) tested water, 30/70 and 70/30 methanol–water, methanol, and 80/20 ethanol–water at coolant/fuel ratios of 0–0.65. The summary gains were +60 % temperature-limited take-off power and +60 % knock-limited cruise power; the knock-limited rated-power figure is illegible in the OCR [2].
- Above ~250 psi IMEP at 2500 rpm, specific *liquid* consumption (fuel + coolant) with internal coolant was lower than specific fuel consumption without it [2]. The coolant let the engine run leaner at high power; it did not mean water supplied energy.
- Engines fitted with water or methanol–water injection included the BMW 801 (MW 50), Daimler-Benz DB 605, Junkers Jumo 213 and Pratt & Whitney R-2800 [3, secondary]. No source opened here confirmed the MW 50 mixing ratio.

### 1.2 Saab
- The 1978 Saab 99 Turbo S reportedly used water injection to gain 15–20 hp from its 2-litre engine, and the 1980 Saab 900 "Enduro" is also listed. The only source found tags both claims "citation needed" [3, secondary], so they are **uncertain**.

### 1.3 BMW M4 GTS (2015) and Bosch WaterBoost
- In the M4 GTS, BMW's S55 3.0-litre six makes 493 hp at 6,250 rpm (+16 % vs the M4) and 442–443 lb-ft at CR 10.2:1. Three injectors, each serving two cylinders, spray water into the intake plenum at about 145 psi from a 1.3-gallon tank [4].
- Turbo compression can heat intake air to 320 °F. The intercooler removes up to 160 °F and water injection a further 80 °F. The cooling raises the knock threshold, so boost and spark advance can be increased; if the water system fails, the ECU cuts boost and retards spark [4]. BMW publishes no degrees of advance and no mpg figures [4].
- A secondary source says boost rose from 1.19 to 1.49 bar relative to the N55, citing BMW M [3, secondary]. BMW says fuel efficiency in normal driving is "similar" to the M4's and that full-throttle consumption is lower [4]. A journal paper's "13 % better fuel efficiency" for the GTS [8] is not supported by BMW's own release, so it is treated as **uncertain**.
- Bosch WaterBoost was co-developed with BMW. Bosch claims up to 5 % more power, up to 4 % lower CO₂ and up to 13 % better fuel economy [3, 5]; these are manufacturer claims reported by secondary sources. Reported water use is ~5 L of demineralised water per ~3,000 km of normal driving [5], about 0.17 L/100 km (derived).
- FEV/RWTH (Hoppe et al. 2016) report gains from a condensed-water injection concept: 3.3–3.8 % efficiency near minimum BSFC (stoichiometric, Miller, cooled EGR), up to 16 % at full load, and 4.5 % with homogeneous lean combustion [6]. A 2017 follow-up used single-cylinder direct-water-injection maps and drive-cycle simulation to derive fuel-versus-water trade-off curves and tank sizes [7].

### 1.4 Water-to-fuel ratios used
| Study | Engine / fuel | Water/fuel ratio | Result |
|---|---|---|---|
| NACA 756 (1942) [1] | Aircraft cyl., CR 7, AN-F-28 / 80-oct. | 0.2–0.6; up to 1.5 (mass) | knock-limited IMEP 180→305 psi at 0.6 |
| NACA E4H31 (1944) [2] | Wright C9GC, 100-oct. | 0–0.65 (coolant/fuel, mass) | +60 % knock-limited cruise power |
| Lestz & Meyer (cited in [8]) | SI | 1–1.25 | NO −50 % at MBT |
| Wang et al. (cited in [8]) | SI | 1.0 (water/gasoline) | NOx reduced by >80 % |
| Zhuang et al. 2020 [8] | 1.5 L TGDI, CR 11.5 | 0–50 % (volume), optimum 30 % | see §1.5 |
| Li & Zheng 2020 [9] | GDI CFD, CR 9.5 | ≈0.10 (8.23 mg water / 82.31 mg fuel, derived) | knock index ~4 → 0.94 at −21 °CA |
| Cesur 2022 [71] | SI, M15 (15 % methanol) | 0.1, 0.2, 0.3 (mass, intake manifold) | NOx up to −12 %, HC up to −16 % |
| Conway (cited in [3]) | port WI, medium load | 0.4–0.5 | same effect as ≈10 % EGR |
| Mohamed et al. 2024 [30] | H₂ PFI, CR 11.3 | reported as % of H₂ mass (table garbled in source) | see §5 |

**Maximum reported:** water/fuel mass ratio 1.5 (NACA 1942, gasoline, SI) [1]. No modern SI study found went beyond W/F ≈ 1.25 [8].

### 1.5 Knock-limited spark advance and compression-ratio gains
- Zhuang et al. (1.5 L turbo GDI, 1500 rpm, WOT, port water injection): as water/gasoline rose from 0 to 50 %, knock-limited spark moved from about 2.0–2.5 °CA ATDC to 3 °CA BTDC, roughly 5 °CA (derived; the paper's sign convention is unclear) [8]. With re-optimised spark, BTE rose from 29.25 to 30.5 % and BSFC fell from 280 to 268 g/kWh. At fixed spark, IMEP fell from 19.2 to 17.9–18.1 bar [8].
- Li & Zheng (CFD, 5500 rpm, φ = 1.1): water at ~10 % of fuel mass allowed spark advance from −11 to −21 °CA without knock. The knock index was 0.94 with 60 °C water versus ~4 without water, where KI > 2 means knock [9].
- Mohamed et al. (H₂, CR 11.3): water allowed up to 6° more spark advance in the water sweep, and λ = 1 operation without spark retard [30].
- Compression ratio: no controlled study opened here measured a knock-limited CR increase from water alone. The reported data points are indirect. Kim et al. (cited in [8]) ran a CR 13.5 naturally aspirated prototype that reached 45 % thermal efficiency with water injection. Lanzafame et al. (cited in [8]) report RON rising from 70 to 93 and MON from 64 to 90 with a combined CR increase and water injection. Crower's press claim of CR 13:1 in a six-stroke is unverified [26]. **Knock-limited CR gain: uncertain, not found as a primary measurement.**

## 2. Wet ethanol and wet methanol

### 2.1 HCCI on wet ethanol (Mack, Aceves & Dibble 2009 and related LLNL/UC Berkeley work)
- Mack, Aceves & Dibble (Energy 34:782–787, 2009) ran a 4-cylinder 1.9 L engine in HCCI on 100, 90, 80, 60 and 40 % ethanol-in-water, studying operating limits, intake temperatures, heat release and emissions [10]. **Maximum water demonstrated: 60 % (40 % ethanol-in-water).** The accessible abstract does not say whether the fractions are by volume or by mass, and it gives no intake temperatures, φ or efficiencies [10, 11]; these are **not found**.
- Earlier modelling predicted HCCI operation on fuel containing as little as 35 % ethanol-in-water [10, 11].
- Flowers, Aceves & Martinez-Frias (SAE 2007-01-1867, model): an HCCI engine with efficient exhaust heat recovery, running on 35–65 % (vol) ethanol-in-water, reached 38.7 % brake thermal efficiency and 1.6 ppm NOx [12]. At 35 % ethanol, water-separation energy falls to 3 % of the ethanol-plus-coproduct energy, versus 37 % for pure ethanol, which raises the net energy gain from 21 % to 55 % [12].
- Saxena et al. (Applied Energy 98:448, 2012): using only an exhaust heat exchanger and no electric air heater, a modified VW 4-cylinder HCCI engine ran on up to 20 % water. The best results needed high intake pressure, high φ and strongly delayed combustion timing [13].
- Note for WME-1: the high-water HCCI results depend on large intake preheat to vaporise the water and reach autoignition. That heat comes from the exhaust or from external heaters, not from the water [12, 13].

### 2.2 Brazilian hydrous ethanol
- ANP Technical Regulation 3/2011 (Resolution 7/2011) sets hydrous ethanol fuel (EHC) at 92.5–93.8 % ethanol by mass (95.1–96 °GL), water ≤ 4.9 % (basis not stated) and density 807.6–811.0 kg/m³ at 20 °C; anhydrous ethanol is limited to ≤ 0.4 % water [14, secondary]. Current ANP limits may differ from this 2011 text [14].
- The implied non-ethanol content, essentially water, is 6.2–7.5 % by mass (derived). Typical hydrous ethanol therefore carries only about 5–7 % water (derived), an order of magnitude below WME-1's target.

### 2.3 Spark-ignition engine work at 20–40 % water (none found at 50–60 %)
- Lanzanova et al. (DISI, CR 11.8, 1500 rpm, 3.1 bar IMEP) went up to 20 % v/v water (E80W20). With residual-gas trapping, maximum indicated-efficiency gains were 8.6 % (E100), 6.1 % (E90W10) and 4.9 % (E80W20). The lowest ISNOx, 0.23 g/kWh, came from E80W20 at 31 % residual gas. More water needed more spark advance and raised THC [15].
- Literature summarised in [15] reports SI operation with up to 30 % v/v water using a catalytic igniter (Cordon et al.; Olberding et al.), and pre-chamber SI with up to 40 % v/v water (Martins et al.; Lanzanova et al.) [15, secondary].
- Munsin et al. (Fuel 106:586, 2013) ran a small SI generator at 3600 rpm on hydrous ethanol with up to 40 % water. More water lowered overall efficiency and NOx and raised BSFC, HC, CO and aldehydes, and a catalytic converter was needed [16]. According to [15], NOx fell ~80 % going from 20 to 40 % v/v water [15, secondary].
- Wet methanol: Sileghem et al. (SAE 2013-01-1319, Ghent) ran a 4-cylinder SI engine on methanol with 2.5, 5 and 10 % v/v water. BTE was essentially unchanged and stayed above gasoline, while NOx fell substantially as water increased [17]. Iwate University (KAKEN 03650166, 1991–93) ran a small two-stroke SI engine on methanol with 0, 10 and 20 % v/v water at CR 7.1–8.4. With rich mixtures, maximum power with up to 20 % water matched neat methanol, and at the highest CR thermal efficiency rose slightly. The flammable range narrowed and ignition delay lengthened [18].
- **Gap:** no SI engine data were found at 50–60 % water in an alcohol fuel blend. The 60 % water point exists only in HCCI with heavy intake preheat [10].

## 3. Water-in-diesel emulsions (PuriNOx, Aquazole)

| Product / study | Water fraction | NOx | PM | Notes |
|---|---|---|---|---|
| Lubrizol PuriNOx, EPA draft technical report (2003) [19] | 20 % | −9.0 to −12.9 % (highway, FTP); −17.0 to −20.2 % (nonroad, 8-mode) | −51.1 to −58.2 % (highway); −16.8 to −23.3 % (nonroad) | secondary report of EPA draft |
| PuriNOx, CARB verification Jan 2001 (as reported) [19] | 20 % | −14 % | −63 % | secondary |
| PuriNOx + AZ Purifier, CARB Level 2, EO DE 04-007 (2004) [20] | not stated | −20 % | −50 % | off-road 1996–2002 engines at ports and rail yards |
| Lubrizol bus test, Volvo B10A Euro 2, London bus cycle [21] | 10 % / 20 % by mass | −9 % / −18 % | −20 % / −43 % | manufacturer data |
| Elf Aquazole (EU LIFE project, 1998) [22] | ~13 % aqueous phase (+2–3 % additives); commercial fuel 10 % water | −15 to −30 % | −10 to −50 % (black smoke −30 to −80 %) | EU news item |

- Efficiency: CORDIS reports energy consumption 1–4 % lower but also says fuel consumption rises because water has no calorific value, so the source contradicts itself [22]. Abu-Zaid (cited in [9]) reported +3.5 % BTE with a 20 % emulsion in a DI diesel [9, secondary]. Volumetric fuel-economy penalties for PuriNOx are plotted in [21] but are not legible in the accessible text, so they are **uncertain**.
- Mechanism (qualitative, consistent with all the sources above): water lowers peak flame temperature, which cuts NOx, and micro-explosions plus longer ignition delay improve mixing, which cuts PM. None of the sources claims energy from the water.

## 4. Six-stroke water-injection engines

- **Conklin & Szybist (ORNL; Energy 35:1658–1664, 2010)** describe a four-stroke Otto/Diesel cycle followed by a two-stroke steam cycle. The exhaust valve closes early to recompress part of the exhaust, water is injected at top centre, and the steam/exhaust mixture expands in a sixth-stroke power stroke [23, 24]. With an ideal thermodynamic model and conventional SI geometry, the net steam-stroke MEP is **0.75–2.5 bar**, versus combustion MEP of up to ~10 bar for naturally aspirated gasoline engines [23, 24]. Valve closing is limited by 1 bar or by the dew point at exhaust-valve opening [23].
- The accessible abstract and OSTI record give **no percentage efficiency gain and no water mass per cycle**, so both are **not found** [23, 24]. The MEP ratios 0.75/10 to 2.5/10 imply idealised extra work of 7.5–25 % of combustion work at unchanged fuel (derived). That is an upper bound from an ideal model, not a figure the authors state. A 2024 review attributes a "40 %" combustion-efficiency increase jointly to [23] and another paper without separating them [29, secondary], so that figure is treated as **uncertain**.
- The related patent US 8,291,872 B2 specifies water at about 100 °C at the injector, venting 20–70 % of combustion products in a partial exhaust event ending at 560–660 °CA, and injection around 700–730 °CA (TDC = 720°). It gives no efficiency figure and no water quantity beyond "a small amount" [25].
- **Crower (2006):** Bruce Crower converted a single-cylinder diesel to inject water after the exhaust stroke. Press reports (AutoWeek, 27 Feb 2006, via [26]) claimed ~40 % better fuel efficiency, no need for a radiator, and CR 13:1 without knock. No test data were published, and the patent application was later abandoned [26, 27, secondary]. **Unverified claim.**
- **Bajulaz (Geneva, 1989):** this is not a water-injection engine. Each cylinder has a separate combustion chamber and an air-preheating chamber above it. The claimed fuel-consumption reduction of at least 40 % [27, secondary] is unverified; see SAE 860534 (Yuen et al., "The Bajulaz Cycle") and US 4,809,511 [27, 28].
- Experimental and CFD six-stroke data (via review [29], secondary): Yang et al. (2023) raised IMEP from 5.89 to 6.21 bar (+5.4 %, derived) by injecting 97.81 mg of steam at 20 bar. Arabaci et al. (2015) found HC −18.23 % and CO −21.97 % at 3000 rpm [29]. Arabaci et al. (cited in [9]) report specific fuel consumption −9 %, exhaust temperature −7 %, thermal efficiency +8.72 % and power +10 % [9, secondary].
- Energy accounting: the steam stroke converts exhaust and coolant heat that the alcohol has already released. It cannot exceed that heat, and the same waste heat must also supply the water's latent heat.

## 5. Hydrogen engines with water injection; flame speeds and limits with steam

### 5.1 Hydrogen engines
- Mohamed et al. (IJER 2024; PFI H₂, CR 11.3, 10 bar IMEP, 2000 rpm, λ = 1.8): 5 kg/h of port water cut NOx 79 % (≈2000 → 400 ppm), with ITE ~1 % lower because of partial burns [30]. At λ = 1, water raised ITE from 30 to 32 % and cut NOx by 74 % on average. Maximum load extended to 24 bar IMEP (+10 % torque), and peak ITE rose from 41 % to 42.5 % [30]. Water/H₂ ratios in the source table are partly garbled [30].
- Younkins, Wooldridge & Boyer (SAE 2013-01-0227): direct in-cylinder water injection into a PFI hydrogen engine cut NOx 95 % with an 8 % fuel-consumption penalty, or 85 % with no penalty [31].

### 5.2 Laminar flame speeds and flammability with steam dilution
- **H₂–air–steam:** steam raises the H₂ lean flammability limit by ~0.34 vol % H₂ per 10 vol % H₂O, up to 50 % steam, at 1 and 7 bar. Each +100 K of initial temperature lowers the limit by ~0.45 vol %, up to 7 bar [32]. Lean H₂–air (φ = 0.26) burns at ~17 cm/s at 1 bar and ~8 cm/s at 5 bar [32]. For a lean mixture labelled f = 0.39 at T₀ = 393 K, equilibrium burned-gas temperature drops from 1476 to 1352 to 1234 K for 0, 10 and 20 % steam, and the expansion ratio from 3.49 to 3.22 to 2.96 [32].
- Santner, Dryer & Ju (Proc. Combust. Inst. 34, 2013), via the FFCM-1 target set: for H₂/O₂/He with 5 % H₂O at 393 K and 2 atm, S_L = 110.4 ± 11 cm/s; with 15 % H₂O at 393 K and 1 atm, S_L = 93.9 ± 9.4 cm/s [44, 45]. Undiluted H₂/air at 298 K and 1 atm gives 211.1 ± 11.3 cm/s (φ = 1.0) and 213.2 ± 11.4 cm/s (φ = 3.0) [42, 43].
- Steam inerting concentration for H₂–air–steam: **not found** in the sources opened. Near-limit detonation data exist: for example, 17.26 % H₂ / 30 % H₂O at 650 K detonated in a 273 mm tube (Ciccarelli et al., NUREG/CR-6213). Steam is a weaker mitigant than CO₂ [33].
- **CH₄–steam:** Mazas et al. (Combust. Flame 158:2428, 2011) measured flames at steam mole fractions of 0–0.50, 373 K, 1 atm, φ = 0.5–1.5 and O₂ enrichment of 0.21–1.0. Flame speed falls quasi-linearly with steam. In methane–air, steam also has a non-negligible chemical effect through its high third-body efficiency, which weakens with O₂ enrichment [34]. Absolute values appear only in the paper's figures and are **not extracted**. Baseline CH₄/air at 298 K and 1 atm: 15.6 ± 1.8 cm/s (φ = 0.7), 36 ± 1.7 cm/s (φ = 1.0) and 24.7 ± 1.7 cm/s (φ = 1.3); at 300 K, 10 atm, φ = 1: 13.8 ± 2.0 cm/s [38–41].
- **Methanol–water–air:** Zhu et al. (Energies 13:6504, 2020) used spherical flames at 380 and 450 K, 1–4 bar and φ = 0.7–1.4, with water at 0, 20 and 40 % of the fuel's vapour mole fraction. At φ = 1, 450 K and 1 bar, S_L falls 31.1 % with 20 % water and 47.9 % with 40 % water, roughly linearly. Going from 380 to 450 K raises S_L 51.5 %, going from 1 to 2 bar lowers it 15.8 %, and the peak is at φ ≈ 1.1–1.2 (1–2 bar) [35]. Absolute values appear only in figures (uncertainty up to 5.7 cm/s) [35].
- **Ethanol–water–air:** Yang, Fang & Leach (Energy & Fuels 39:20966, 2025) tested 380/450 K, 2/4 bar and 0/20/40 vol % water. At 4 bar and 450 K the peak S_L falls from 60 to 40 cm/s with 40 % water (−33 %, derived) [36]. FFCM-2 and Olm (2016) match the data for φ < 1.1 without water but under-predict wet-ethanol flames at φ > 1.1. San Diego (2016) was among the mechanisms compared [36].
- Neat-alcohol flame-speed datasets suitable for validation, with values in the full papers' figures and tables (not extracted here): Veloo et al. 2010 (methanol, ethanol, n-butanol; counterflow; 1 atm; elevated T) [48]; Vancoillie et al. 2012 (methanol; heat flux; 298–358 K; φ 0.7–1.5; ±1 cm/s) [46]; Raida et al. 2021 (methanol and ethanol; heat flux; 318–338 K; 1–5 bar; φ 0.8–1.3; ±1–1.5 cm/s) [47].
- Ignition-delay datasets: methanol in an RCM at 7–30 bar, 850–1100 K, φ 0.25–2.0 [49]; methanol in a shock tube (Noorani et al. 2010) at 2–12 bar, φ 0.5–2 [52]; ethanol in an RCM at 10–50 bar, 825–985 K, φ 0.3–1.0 [50]; ethanol at φ = 1 in a high-pressure shock tube near 80 bar and 775–1300 K, and in an RCM down to 705 K [51]. Numeric delay values could not be extracted from the accessible text, and **no wet-alcohol ignition-delay data were found**.
- Flammability limits in air at 20 °C and 1 atm (secondary): H₂ 4–75 %, CH₄ 4.4–16.4 %, methanol 6.7–36 % and ethanol 3.3–19 % by volume [55]. The corresponding limits for methanol and ethanol with steam dilution were **not found**.

## 6. HHO / onboard electrolysis

- Physics: electrolysis must supply at least the energy later released when H₂ and O₂ recombine to water. On board, that electricity comes from the engine through an alternator, battery and electrolyser, each with losses. A closed loop therefore cannot produce net energy; at most HHO can act as a combustion promoter, and only if its benefit exceeds the electrical cost.
- Polverino, D'Aniello, Arsie & Pianese (Energy Conversion and Management, preprint 2018) put the ideal electrolysis energy at 2.19 kWh per m³ of HHO (diatomic, NTP). They estimate an average gross demand at the electrodes of 5.28 kWh/m³, an electrolyser efficiency of ~64 %, and an overall auxiliary-chain efficiency of 54.4 % [56]. Re-analysing published tests with the electrical cost charged back to the shaft, they found net losses in several cases (for example Wang et al., 0–70 L/min, with fuel use up to +17.7 %). They conclude that savings are not realistic for larger engines at higher flow [56]. Their "monoatomic" lower bound assumes atomic H and O, which an electrolyser does not stably produce, so the diatomic bound is the relevant one (assessment here).
- Cameron (USQ undergraduate dissertation, 2012; not peer-reviewed) tested a diesel generator with on-board electrolysers. They needed 3.1 Wh per litre of HHO at DC (4.06 Wh/L from the 240 V supply), against a theoretical 2.163 Wh/L. HHO *increased* diesel consumption in every test, by up to 5.2 % at 55 % load with 6 L/min. Breaking even would need 73–84 % net HHO production efficiency; the system achieved 11.4–16.0 % [57].
- Some peer-reviewed papers claim gains while leaving out the electrolysis energy. Premkartikkumar et al. (Thermal Science 18:259, 2014) report BTE rising from 24.32 to 27.01 % at 3.3 L/min, but neither BTE nor BSEC includes the electrolysis energy [58]. Yilmaz et al. (14 % average diesel reduction) and Bari & Esmaeil (14–15 % fuel-energy reduction) are criticised in [57] for flow-meter problems and for omitting system efficiency [57, secondary].
- **Verdict for WME-1:** no peer-reviewed source found shows a net energy gain from on-board electrolysis once the electrical input is counted. HHO is excluded from the WME-1 energy path.

## 7. Aluminium–water energy carriers (MIT, Hart group)

- Reactions: 2Al + 6H₂O → 2Al(OH)₃ + 3H₂ gives gibbsite, stable up to 280 °C. Boehmite is the stable product at 280–480 °C and alumina above 480 °C [61].
- Enthalpy: ~280 kJ per mol H₂ at ~50–100 °C (−279 kJ/mol H₂ at 100 °C; −337 kJ/mol H₂ at 700 °C) [61]. Godart, Fischman & Hart give ΔH_rxn = 430 kJ/mol Al at 100 °C. The fuel's embodied enthalpy of 859 kJ/mol Al splits roughly half into heat and half into the H₂ [59]. Godart's thesis gives 15.8 MJ/kg of heat from aluminium oxidation [60].
- Hydrogen yield: 11 wt % H₂ on aluminium alone, i.e. 9 kg Al per kg H₂ at 100 % yield (≈0.11 kg H₂/kg Al, derived), or 3.7 wt % counting the water and hydroxide [61]. Godart et al. report 5–11 wt %, depending on whether the water is carried on board [59].
- Activation: eutectic Ga–In (80/20 wt %) applied at 120 °C at 2.5–5 wt % of fuel mass gives >95 % reaction completion. The group built 3 kW and 10 kW fuel-cell systems; the prototype's total system efficiency was 20 % [59]. The thesis reports >99 % eGaIn recovery using NaCl solutions and theoretical H₂ yield fractions above 0.97 from scrap cans; reactivity dropped with less than 10× stoichiometric water [60]. Fuel energy density is 23.3 kWh/L [59], and H₂-only energy density up to 36.3 MJ/L [60].
- Energy accounting: the energy sits in the reduced aluminium, put there by smelting (15.552 kWh/kg Al, North American average, 2005). Hydrogen made with Hall–Héroult aluminium has an overall efficiency of ~24 % on an H₂ LHV of 120 MJ/kg and costs ~$20/kg H₂ at 2010 metal prices [61]. Water is the oxidant, not the fuel.
- Relevance to WME-1: an Al–water reactor could supply H₂ and steam as an auxiliary. However, it runs on a separate fuel (aluminium) with its own supply chain, which breaks the rule that the alcohol supplies all chemical energy.

## 8. Cantera-compatible ethanol and methanol mechanisms

- **San Diego (UCSD) mechanism, release 2016-12-14 (project baseline).** The page is https://web.eng.ucsd.edu/mae/groups/combustion/mechanism.html [62]. Files: `sdmech/sandiego20161214/sandiego20161214_mechCK.txt` (CHEMKIN), `sandiego20161214_mechFM.txt` (FlameMaster), `sandiego20160815_therm.txt`, `sandiego20160815_trans.txt` and `20161214_log.txt` [62, 63]. No Cantera YAML or CTI file is offered, so convert with Cantera's `ck2yaml` [69].
- **Reproducibility warning:** the file served at the 2016-12-14 URL is not the December 2016 text. On 2026-10-21 the server reported `Last-Modified: Fri, 28 Feb 2025` for the CHEMKIN file, and the change log records later edits [64]:
  - April 2017: H₂O third-body efficiency in H+CH₃(+M)⇌CH₄(+M) raised from 6.00 to 16.00 to match counterflow methane extinction with water addition.
  - March 2018: H+CH₃(+M) rate taken from Troe & Ushakov, and the CH₄ chaperon efficiency set to 4.0.
  - November 2018: C₂H₂+HO₂ and CHCHO+O₂ reactions added.
  - August 2022: C₃H₅ thermo corrected.
  - August 2024: O₃ decomposition added.
  - February 2025: O₃ prefactor revised.
- The current file lists 59 species, including CH₃OH, C₂H₅OH, CHCHO and O₃ [63]. Millán-Merino et al. describe the 2016-12-14 release as 54 species and 257 steps in their abstract, or 47 and 235 in their table [65].
- WME-1 should pin the files by checksum. SHA-256 of the files downloaded on 2026-10-21 (computed here):
  - `mechCK`: `728aa95e372aa71c59528850ac35511bf4c5f457954b9803c6ef823996163c73`
  - `therm`: `ba9518b7007d007353ca6ac927f881b05d6b302bbb56bc32c9e1ee80d3333d92`
  - `trans`: `dc8134f2c62cd54c7999d2428ac1de22743e2e331caef2da8286763bedd5ce94`
- Conversion check done here with Cantera 3.2.0: `ck2yaml --input=… --thermo=… --transport=… --output=…` passed and loads as 59 species and 271 reactions. NASA-polynomial discontinuity warnings at T_mid = 1000 K appear for C2H4OOH, C3H6OOH, CH2CH2OH, CH3CH2O, CH3CHOH, OC2H3OOH and OC3H5OOH; three of these are ethanol-derived radicals.
- The April 2017 H₂O third-body change bears directly on steam-diluted WME-1 flames. Predictions should be tested for sensitivity to the H₂O collision efficiencies.
- **University of Galway (C3):** the index is https://universityofgalway.ie/combustionchemistrycentre/mechanismdownloads/, and files sit under https://universityofgalway.ie/media/researchcentres/combustionchemistrycentre/files/mechanismdownloads/ [66]:
  - Methanol 2016 (Burke et al., Combust. Flame 165:125–136): `alcohols/Methanol_2016_mech.inp` plus therm and tran files.
  - Ethanol 2014 (Mittal et al., Combust. Flame 161:1164–1171): `alcohols/56.55_c3_chem.inp`. The RCM paper behind it covers 10–50 bar, 825–985 K and φ = 0.3–1.0 [50].
  - Ethanol/DME 2018: `alcohols/Mech_v2.8.MECH`.
  - AramcoMech 3.0: `aramcomech30/AramcoMech3.0.MECH`.
  - NUIGMech1.1.
- **LLNL ethanol (Marinov 1999, Int. J. Chem. Kinet. 31:183–220), archived:** https://combustion.llnl.gov/sites/combustion/files/2020-10/ethanol_mech.txt, https://combustion.llnl.gov/sites/combustion/files/ethanol_v1b_therm.txt and https://combustion.llnl.gov/sites/combustion/files/ethanol_trandat.txt [67].
- **CRECK (Politecnico di Milano), release 2003 (March 2020):** for example CRECK_2003_C1_C3_HT (114 species, 1999 reactions) and alcohol-containing TPRF variants. They are in CHEMKIN format, with download buttons at https://www.creckmodeling.polimi.it/?p=655. That page does not name methanol explicitly [68].
- **FFCM-1 (Stanford):** covers H₂/CO/CH₄ only, with no alcohols. It publishes per-target experimental values with uncertainties, which the validation table below uses [37–45].
- Conversion syntax per the Cantera tutorial is `ck2yaml --input=chem.inp --thermo=therm.dat --transport=tran.dat`, with `--permissive` available for recoverable parsing errors [69]. Cantera ships only illustrative input files such as `gri30.yaml` and `h2o2.yaml`, and says GRI-Mech 3.0 "should otherwise be used with caution" [70].

## 9. What this means for WME-1 (evidence and gaps)
- Supported by data:
  - Knock suppression, with spark-advance gains of ≈5–10 °CA in the two studies above [8, 9].
  - Charge cooling: a further −80 °F after the intercooler on the M4 GTS [4].
  - Large NOx cuts, from −50 % to −95 % across [8, 30, 31].
  - 3–16 % efficiency gains from water injection in modern gasoline studies [6].
  - A steam-stroke MEP of 0.75–2.5 bar in an ideal model [23].
- Weak or missing:
  - SI operation with more than 40 % water in an alcohol.
  - A measured knock-limited CR gain from water alone.
  - Conklin & Szybist's efficiency figure and water mass per cycle.
  - Absolute methanol flame speeds with steam (only relative values were found).
  - Steam-inerting limits for H₂, CH₄, methanol and ethanol.
  - Ignition delays of wet alcohols.
- Every efficiency gain above either reduces a loss (knock margin, heat rejection, pumping or charge temperature) or recovers alcohol heat that would otherwise be rejected. None is energy from water.

## Validation targets

| Quantity | Value | Conditions | Source |
|---|---|---|---|
| Laminar flame speed S_L, CH₄/air | 15.6 ± 1.8 cm/s | φ = 0.7, 298 K, 1 atm | [38] |
| S_L, CH₄/air | 36 ± 1.7 cm/s | φ = 1.0, 298 K, 1 atm | [39] |
| S_L, CH₄/air | 24.7 ± 1.7 cm/s | φ = 1.3, 298 K, 1 atm | [40] |
| S_L, CH₄/air | 13.8 ± 2.0 cm/s | φ = 1.0, 300 K, 10 atm | [41] |
| S_L, H₂/air | 211.1 ± 11.3 cm/s | φ = 1.0, 298 K, 1 atm | [42] |
| S_L, H₂/air | 213.2 ± 11.4 cm/s | φ = 3.0, 298 K, 1 atm | [43] |
| S_L, H₂/O₂/He/H₂O | 110.4 ± 11 cm/s | 0.11490 H₂ / 0.06759 O₂ / 0.05 H₂O / He, 393 K, 2 atm | [44] |
| S_L, H₂/O₂/He/H₂O | 93.9 ± 9.4 cm/s | 0.12567 H₂ / 0.07392 O₂ / 0.15 H₂O / He, 393 K, 1 atm | [45] |
| S_L, lean H₂/air | ≈17 cm/s (1 bar); ≈8 cm/s (5 bar) | φ = 0.26 | [32] |
| Relative S_L drop, methanol + water | −31.1 % (20 % water); −47.9 % (40 % water) | φ = 1, 450 K, 1 bar; water as vapour mole fraction of fuel | [35] |
| S_L temperature effect, methanol | +51.5 % | 380 → 450 K, φ = 1 | [35] |
| S_L pressure effect, methanol | −15.8 % (1→2 bar); −15.4 % (2→4 bar) | φ = 1 | [35] |
| Peak S_L, ethanol/air ± water | 60 cm/s (dry) → 40 cm/s (40 vol % water) | 450 K, 4 bar | [36] |
| Equilibrium burned-gas T, H₂–air–steam | 1476 / 1352 / 1234 K | T₀ = 393 K; 0 / 10 / 20 % steam; lean mixture labelled "f = 0.39" (H₂ % not stated) | [32] |
| Lean-limit shift of H₂ with steam | +0.34 vol % H₂ per 10 vol % H₂O | ≤ 50 % steam, 1–7 bar | [32] |
| Adiabatic flame T (secondary; cross-check with Cantera equilibrium) | MeOH 2222 K; EtOH 2238 K; H₂ 2483 K; CH₄ 2236 K | stoichiometric in air, 25 °C, 1 atm, constant pressure | [54] |
| LHV methanol | 20.094 MJ/kg (HHV 22.884) | GREET 1.8d.1 | [53] |
| LHV ethanol | 26.952 MJ/kg (HHV 29.847) | GREET 1.8d.1 | [53] |
| LHV hydrogen | 120.21 MJ/kg (HHV 142.18) | GREET 1.8d.1 | [53] |
| LHV natural gas (not pure CH₄) | 47.141 MJ/kg (HHV 52.225) | GREET 1.8d.1 | [53] |
| Ignition delay, methanol | dataset; numeric values not extracted | RCM, 7–30 bar, 850–1100 K, φ 0.25–2.0 | [49] |
| Ignition delay, ethanol | dataset; numeric values not extracted | RCM, 10–50 bar, 825–985 K, φ 0.3–1.0 | [50] |
| Knock-limited IMEP with water | 180 → 305 psi | W/F = 0.6 (mass), F/A 0.067, CR 7, 2000 rpm, 250 °F inlet, AN-F-28 | [1] |
| Knock-limited spark-advance gain | ≈5 °CA (derived); BTE 29.25 → 30.5 % | 1.5 L TGDI, 1500 rpm, WOT, water/gasoline 0 → 50 vol % | [8] |
| Spark advance enabled by water (CFD) | −11 → −21 °CA; knock index ~4 → 0.94 | GDI, CR 9.5, 5500 rpm, φ 1.1, water ≈ 10 % of fuel mass at 60 °C | [9] |
| Water-injection efficiency gain | 3.3–3.8 % near min BSFC; up to 16 % at full load | stoichiometric, Miller, cooled EGR, condensed-water injection | [6] |
| Six-stroke steam MEP | 0.75–2.5 bar (vs ≤ 10 bar combustion MEP) | ideal model, conventional SI geometry | [23] |
| Six-stroke IMEP gain | 5.89 → 6.21 bar | 97.81 mg steam injected at 20 bar | [29] |
| Wet-ethanol HCCI BTE (model) | 38.7 %; NOx 1.6 ppm | 35–65 vol % ethanol-in-water, exhaust heat recovery | [12] |
| Al + water reaction enthalpy | 430 kJ/mol Al; ~280 kJ/mol H₂ | 100 °C; 50–100 °C (gibbsite product) | [59], [61] |
| H₂ yield from Al | 11 wt % on Al (9 kg Al per kg H₂) | stoichiometric, 100 % yield | [61] |
| Charge-temperature drop from water | further −80 °F after intercooler | BMW M4 GTS, plenum injection | [4] |

## References

1. Rothrock, A. M., Eberle, A., Jones, A. W., "The Induction of Water to the Inlet Air as a Means of Internal Cooling in Aircraft-Engine Cylinders," NACA Report 756 (1942). https://ntrs.nasa.gov/api/citations/19930093187/downloads/19930093187.pdf
2. Wear, J. D., Held, L. F., Slough, J. W., "Some Effects of Internal Coolants on Knock-Limited and Temperature-Limited Power…," NACA ARR E4H31 (1944). https://ntrs.nasa.gov/api/citations/19930093209/downloads/19930093209.pdf
3. Wikipedia, "Water injection (engine)" (secondary). https://en.wikipedia.org/wiki/Water_injection_(engine)
4. BMW Group press release T0237582EN_US, BMW M4 GTS (manufacturer). https://www.press.bmwgroup.com/usa/article/detail/T0237582EN_US
5. New Atlas, "Bosch WaterBoost injection opens door to better power and economy" (secondary). https://newatlas.com/bosch-water-injection/45205
6. Hoppe, F., Thewes, M., Baumgarten, H., Dohmen, J., "Water injection for gasoline engines: Potentials, challenges, and solutions," Int. J. Engine Res. 17(1):86–96 (2016). https://journals.sagepub.com/doi/ref/10.1177/1468087415599867
7. Hoppe, F., Thewes, M., Seibel, J., Balazs, A., et al., "Evaluation of the Potential of Water Injection for Gasoline Engines," SAE Int. J. Engines 10(5) (2017), SAE 2017-24-0149. https://saemobilus.sae.org/content/2017-24-0149
8. Zhuang, Y., et al., "Investigation of water injection benefits on downsized boosted direct injection spark ignition engine," Fuel 264:116765 (2020). https://opus.cloud1.lib.uts.edu.au/bitstream/10453/146046/3/Investigation%20of%20water%20injection.pdf
9. Li, A., Zheng, Z., "Effect of Spark Ignition Timing and Water Injection Temperature on the Knock Combustion of a GDI Engine," Energies 13:4931 (2020). https://mdpi-res.com/d_attachment/energies/energies-13-04931/article_deploy/energies-13-04931.pdf
10. Mack, J. H., Aceves, S. M., Dibble, R. W., "Demonstrating direct use of wet ethanol in a homogeneous charge compression ignition (HCCI) engine," Energy 34(6):782–787 (2009). https://ideas.repec.org/a/eee/energy/v34y2009i6p782-787.html
11. Mack, J. H., Flowers, D. L., Aceves, S. M., Dibble, R. W., "Direct Use of Wet Ethanol in a HCCI Engine: Experimental and Numerical Results" (2007). https://escholarship.org/uc/item/6cd5b6vq
12. Flowers, D. L., Aceves, S. M., Martinez-Frias, J., "Improving Ethanol Life Cycle Energy Efficiency by Direct Utilization of Wet Ethanol in HCCI Engines," SAE 2007-01-1867. https://saemobilus.sae.org/content/2007-01-1867
13. Saxena, S., Schneider, S. H., Aceves, S., Dibble, R. W., "Wet ethanol in HCCI engines with exhaust heat recovery…," Applied Energy 98:448–457 (2012). https://eta-publications.lbl.gov/bibcite/export/bibtex/bibcite_reference/26150
14. NovaCana, "Controle de qualidade do etanol" (summary of ANP Resolution 7/2011; secondary). https://www.novacana.com/etanol/controle-qualidade
15. Lanzanova, T. D. M., et al., "The effects of residual gas trapping on part load performance and emissions of a spark ignition direct injection engine fuelled with wet ethanol" (Brunel repository). https://bura.brunel.ac.uk/bitstream/2438/18809/1/FullText.pdf
16. Munsin, R., Laoonual, Y., Jugjai, S., Imai, Y., "An experimental study on performance and emissions of a small SI engine generator set fuelled by hydrous ethanol with high water contents up to 40%," Fuel 106:586–592 (2013). https://kirim.kmutt.ac.th/converis/portal/detail/Publication/600633336?lang=en_GB
17. Sileghem, L., et al., "Performance and Emissions of a SI Engine using Methanol-Water Blends," SAE 2013-01-1319. https://saemobilus.sae.org/papers/performance-emissions-a-si-engine-using-methanol-water-blends-2013-01-1319
18. Fujita, N., et al., KAKEN project 03650166, "The Effect of Compression Ratio on Small Two Stroke Cycle SI Engine Fueled Methanol Containing Water" (1991–1993). https://kaken.nii.ac.jp/grant/KAKENHI-PROJECT-03650166/
19. DieselNet, "US EPA releases draft technical report on emission effects of Lubrizol's PuriNOx…" (2003; secondary). https://dieselnet.com/news/2003/01epa.php
20. California Air Resources Board, "Lubrizol PuriNOx and AZ Purimuffler/Purifier System," EO DE-04-007. https://ww2.arb.ca.gov/lubrizol-purinoxtm-and-az-purimufflertmpurifiertm-system
21. Langer, D. A., Bardasz, E. A. (Lubrizol), "Step Forward in Diesel Engine Emissions Reduction…," CONF-200008-77 (manufacturer). https://www.fischer-tropsch.org/DOE/DOE_reports/200008-77/CONF-200008-77.pdf
22. CORDIS (European Commission), "Adding water to diesel fuel to reduce pollution," 16 April 1998. https://cordis.europa.eu/article/id/10155-adding-water-to-diesel-fuel-to-reduce-pollution/fr
23. Conklin, J. C., Szybist, J. P., "A highly efficient six-stroke internal combustion engine cycle with water injection for in-cylinder exhaust heat recovery," Energy 35(4):1658–1664 (2010). https://ideas.repec.org/a/eee/energy/v35y2010i4p1658-1664.html
24. OSTI record 1035139 (Conklin & Szybist). https://www.osti.gov/biblio/1035139
25. Szybist, J. P., Conklin, J. C., US 8,291,872 B2, "Highly efficient 6-stroke engine cycle with water injection" (2012). https://patents.google.com/patent/US8291872
26. Paultan.org, "Bruce Crower's 6 stroke Crower cycle engine" (2006, citing AutoWeek 27 Feb 2006; secondary). https://paultan.org/2006/03/14/bruce-crowers-6-stroke-crower-cycle-engine
27. Wikipedia, "Six-stroke engine" (secondary). https://en.wikipedia.org/wiki/Six-stroke_engine
28. Bajulaz, R., US 4,809,511, "Internal combustion engine" (link only; not opened). https://patents.google.com/patent/US4809511
29. Mejía-Gallón, V., Gomez, S., Estrada Grisales, D., Fula, M. A., "6-Stroke water injection engine literature review…," Int. J. Environ. Sci. Technol. 21:6911–6924 (2024). https://link.springer.com/article/10.1007/s13762-023-05404-8
30. Mohamed, M., et al., "Exploring the benefits of hydrogen-water injection technology in internal combustion engines," Int. J. Engine Res. (2024), doi:10.1177/14680874241288624. https://bura.brunel.ac.uk/bitstream/2438/30036/1/FullText.pdf
31. Younkins, M., Wooldridge, M., Boyer, B., "Direct In-cylinder Injection of Water into a PI Hydrogen Engine," SAE 2013-01-0227. https://saemobilus.sae.org/papers/direct-cylinder-injection-water-a-pi-hydrogen-engine-2013-01-0227
32. Gelfand, B. E., et al., Appendix A, "Laminar and Turbulent Flame Propagation in Hydrogen–Air–Steam Mixtures" (state-of-the-art report appendix hosted by Caltech; the parent report is not named in the excerpt). https://www.shepherd.caltech.edu/SOAR/AppA.PDF
33. Gelfand, B. E., et al., Appendix B, "…Hydrogen-Air–Carbon Dioxide Mixtures and Detonability of Hydrogen-Containing Gaseous Mixtures." https://www.shepherd.caltech.edu/SOAR/AppB.PDF
34. Mazas, A. N., Fiorina, B., Lacoste, D. A., Schuller, T., "Effects of water vapor addition on the laminar burning velocity of oxygen-enriched methane flames," Combust. Flame 158(12):2428–2440 (2011) (EPA HERO record). https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/2676270
35. Zhu, Z., et al., "Laminar Flame Characteristics of Premixed Methanol–Water–Air Mixture," Energies 13(24):6504 (2020). https://www.mdpi.com/1996-1073/13/24/6504/htm
36. Yang, L., Fang, X., Leach, F., "Effects of Water Addition on Laminar Premixed Ethanol/Air Flame at Elevated Temperature and Pressure," Energy & Fuels 39(43):20966–20977 (2025). https://pmc.ncbi.nlm.nih.gov/articles/PMC12581129
37. Stanford/SRI FFCM-1, experimental targets index. https://web.stanford.edu/group/haiwanglab/FFCM1/pages/targets.html
38. FFCM-1 target fls_27a (CH₄/air, φ 0.7, 298 K, 1 atm). https://web.stanford.edu/group/haiwanglab/FFCM1/Targets/fls_27a.html
39. FFCM-1 target fls_27b (CH₄/air, φ 1.0, 298 K, 1 atm). https://web.stanford.edu/group/haiwanglab/FFCM1/Targets/fls_27b.html
40. FFCM-1 target fls_27c (CH₄/air, φ 1.3, 298 K, 1 atm). https://web.stanford.edu/group/haiwanglab/FFCM1/Targets/fls_27c.html
41. FFCM-1 target fls_30b (CH₄/air, φ 1.0, 300 K, 10 atm). https://web.stanford.edu/group/haiwanglab/FFCM1/Targets/fls_30b.html
42. FFCM-1 target fls_1a (H₂/air, φ 1.0, 298 K, 1 atm). https://web.stanford.edu/group/haiwanglab/FFCM1/Targets/fls_1a.html
43. FFCM-1 target fls_1b (H₂/air, φ 3.0, 298 K, 1 atm). https://web.stanford.edu/group/haiwanglab/FFCM1/Targets/fls_1b.html
44. FFCM-1 target fls_12a (H₂/O₂/He + 5 % H₂O, 393 K, 2 atm; Santner, Dryer, Ju 2013). https://web.stanford.edu/group/haiwanglab/FFCM1/Targets/fls_12a.html
45. FFCM-1 target fls_13a (H₂/O₂/He + 15 % H₂O, 393 K, 1 atm; Santner, Dryer, Ju 2013). https://web.stanford.edu/group/haiwanglab/FFCM1/Targets/fls_13a.html
46. Vancoillie, J., Christensen, M., Nilsson, E. J. K., Verhelst, S., Konnov, A. A., "Temperature Dependence of the Laminar Burning Velocity of Methanol Flames," Energy & Fuels 26(3):1557–1564 (2012). https://portal.research.lu.se/en/publications/temperature-dependence-of-the-laminar-burning-velocity-of-methano/
47. Raida, M. B., et al., "Laminar burning velocity measurements of ethanol+air and methanol+air flames at atmospheric and elevated pressures using a new Heat Flux setup," Combust. Flame 230:111435 (2021). https://research.tue.nl/en/publications/laminar-burning-velocity-measurements-of-ethanolair-and-methanola/
48. Veloo, P. S., Wang, Y. L., Egolfopoulos, F. N., Westbrook, C. K., "A comparative experimental and computational study of methanol, ethanol, and n-butanol flames," Combust. Flame 157:1989–2004 (2010). https://www.osti.gov/biblio/1065135
49. Kumar, K., Sung, C. J., "Autoignition of Methanol: Experiments and Computations," Int. J. Chem. Kinet. 43(4):175–184 (2011). https://combdiaglab.engr.uconn.edu/?p=289
50. "Autoignition of ethanol in a rapid compression machine," Combust. Flame 161(5):1164–1171 (2014) (University of Limerick record; listed by Galway as Mittal et al.). https://pure.ul.ie/en/publications/autoignition-of-ethanol-in-a-rapid-compression-machine/
51. "On the Chemical Kinetics of Ethanol Oxidation: Shock Tube, Rapid Compression Machine and Detailed Modeling Study," Z. Phys. Chem. (2012), doi:10.1524/zpch.2012.0185. https://www.degruyterbrill.com/document/doi/10.1524/zpch.2012.0185/html
52. CaltechMech, methanol ignition-delay report (plots of Noorani, Akih-Kumgeh, Bergthorson, Energy & Fuels 24:5834–5843, 2010). https://theforce.caltech.edu/CaltechMech/reports/report_tig_CH3OH.pdf
53. Argonne National Laboratory, GREET 1.8d.1, "Lower and Higher Heating Values of Gas, Liquid and Solid Fuels" (2010; copy hosted by UIUC NPRE 470). https://courses.grainger.illinois.edu/npre470/sp2018/web/Lower_and_Higher_Heating_Values_of_Gas_Liquid_and_Solid_Fuels.pdf
54. The Engineering ToolBox, "Adiabatic Flame Temperatures" (secondary). https://engineeringtoolbox.com/adiabatic-flame-temperature-d_996.html
55. The Engineering ToolBox, "Gases – Explosion and Flammability Concentration Limits" (secondary). https://engineeringtoolbox.com/explosive-concentration-limits-d_423.html
56. Polverino, P., D'Aniello, F., Arsie, I., Pianese, C., "Study of the energetic needs for the on-board production of Oxy-Hydrogen as fuel additive in internal combustion engines," Energy Convers. Manag. (preprint, 2018). https://www.iris.unisa.it/bitstream/11386/4720544/6/33%20Arsie%20Pre-print.pdf
57. Cameron, R., "Effects of On-board HHO and Water Injection in a Diesel Generator," undergraduate dissertation, University of Southern Queensland (2012; not peer-reviewed). https://sear.unisq.edu.au/23108/1/Cameron_2012.pdf
58. Premkartikkumar, S. R., Annamalai, K., Pradeepkumar, A. R., "Effectiveness of Oxygen Enriched Hydrogen-HHO Gas Addition on DI Diesel Engine…," Thermal Science 18(1):259–268 (2014). https://thermalscience.vinca.rs/pdfs/papers-2013/TSCI121014078P.pdf
59. Godart, P., Fischman, J., Hart, D., "Kilowatt-Scale Fuel Cell Systems Powered by Recycled Aluminum," J. Electrochem. Energy Convers. Storage 18(1):011003 (2021). https://dspace.mit.edu/bitstream/handle/1721.1/138803/jeecs_18_1_011003.pdf
60. Godart, P. T., "Mechanisms of Liquid-Metal-Activated Aluminum-Water Reactions and Their Application," PhD thesis, MIT (2021; advisor D. P. Hart). https://dspace.mit.edu/handle/1721.1/139978
61. Petrovic, J., Thomas, G., "Reaction of Aluminum with Water to Produce Hydrogen…," U.S. DOE (2010). https://www.energy.gov/sites/default/files/2014/03/f9/aluminum_water_hydrogen.pdf
62. UC San Diego, "Chemical-Kinetic Mechanisms for Combustion Applications" (San Diego Mechanism page). https://web.eng.ucsd.edu/mae/groups/combustion/mechanism.html
63. San Diego Mechanism 2016-12-14 files (fetched 2026-10-21): http://web.eng.ucsd.edu/mae/groups/combustion/sdmech/sandiego20161214/sandiego20161214_mechCK.txt ; http://web.eng.ucsd.edu/mae/groups/combustion/sdmech/sandiego20161214/sandiego20160815_therm.txt ; http://web.eng.ucsd.edu/mae/groups/combustion/sdmech/sandiego20161214/sandiego20160815_trans.txt
64. San Diego Mechanism change log. http://web.eng.ucsd.edu/mae/groups/combustion/sdmech/sandiego20161214/20161214_log.txt
65. Millán-Merino, A., Fernández-Tarrazo, E., Sánchez-Sanz, M., Williams, F. A., "A Multipurpose Reduced Mechanism for Ethanol Combustion" (arXiv 2202.07444). https://arxiv.org/pdf/2202.07444
66. University of Galway Combustion Chemistry Centre, mechanism downloads. https://universityofgalway.ie/combustionchemistrycentre/mechanismdownloads/
67. LLNL, archived ethanol mechanism (Marinov 1999). https://combustion.llnl.gov/archived-mechanisms/ethanol
68. CRECK Modeling Group, Politecnico di Milano, detailed kinetic mechanisms. https://www.creckmodeling.polimi.it/?p=655
69. Cantera, "Converting Chemkin Format Files" (ck2yaml tutorial). https://cantera.org/3.1/userguide/ck2yaml-tutorial.html
70. Cantera 3.2, "Example Input Files." https://cantera.org/3.2/examples/input/index.html
71. Cesur, I., "Investigation of the effects of water injection into an SI engine running on M15 methanol fuel…," Energy 261:125203 (2022). https://ideas.repec.org/a/eee/energy/v261y2022ipas036054422202093x.html
