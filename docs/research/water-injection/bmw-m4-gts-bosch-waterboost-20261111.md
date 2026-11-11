# BMW M4 GTS / Bosch WaterBoost water-injection data for Water Engine

**Date:** 11 November 2026, America/Los_Angeles (Pacific Time)  
**Scope:** Research only. No code changes, no git pushes, no PRs, no emails.  
**Question:** Is there verifiable, citable public data from the BMW M4 GTS (S55 + Bosch port water injection / WaterBoost) that Water Engine can use for validation or calibration?

## 1. How this was done

- Water Engine quantities were taken from the box copy at `the public redwing509/water-engine tree` (repo `redwing509/water-engine`, commit `1a9ee24`, 10 Nov 2026 Pacific Time), especially `SPEC.md`, `README.md`, and `results/R31_R32_RESULTS.md`. An earlier research note already exists in other worktrees at `docs/research/02-legitimate-water-combustion.md` (section 1.3). This note re-checks the primary sources and does not reuse unverified figures from that file.
- Sources were opened or HTTP-checked on 11 Nov 2026. Official BMW/Bosch pages were preferred. Peer-reviewed papers are listed with bibliographic records; their internal maps were **not** opened (paywalled or PDF not retrieved), so no figures were taken from them.
- No numbers were invented. Derived estimates are labeled as such and include the assumptions.

## 2. What Water Engine actually uses

The model is a 0-D closed-cycle spark-ignition engine (Wiebe heat release, Woschni heat transfer, Livengood–Wu knock). Default Module 03 geometry is naturally aspirated (`p_IVC = 1.0 bar` WOT). Headline R31/R32 results are **model arithmetic only, not experimentally validated**.

Quantities that matter for a validation or calibration check:

| Quantity | How the model uses it | Current headline (R31+R32 rescore, 10 Nov 2026) |
|---|---|---|
| Water fraction `w` / water-to-fuel ratio `WFR` | `WFR = m_water / m_fuel`; `w = WFR / (1 + WFR)` | Best cost cases at `w = 0.30` (`WFR = 0.429`) |
| Compression ratio | Knock relief is used mainly to raise CR | Best: dry CR 8 → wet CR 12 (PRF91, normal, 1500 rpm) |
| Spark / CA50 | Default CA50 = 8° aTDC; if knocking, retard in 2-CAD steps up to 30° aTDC | Not published as a free output in the headline table |
| Charge cooling / `T_IVC` | Fraction `f_evap_intake` (default 0.5) evaporates before IVC and lowers `T_IVC`; remainder evaporates during compression | Intake set-points: normal 320 K, hot 400 K |
| Efficiency / cost per mile | Gross indicated efficiency and a retail-fuel cost model (water at $0.10/gal) | Best modelled cost/mile **−9.728 %**, power **+10.16 %** |
| IMEP / power | Cycle work at equal or better power vs a like-for-like dry baseline | See above |
| Exhaust (EVO) temperature | Output per point | No public GTS map to compare |
| Relative NO | Extended Zeldovich in the burned zone, relative to dry at the same CR | No public GTS NOx data |
| Equivalence ratio `φ` | Defined on fuel and air only; Module 03 sweeps at `φ = 1` | Production turbo engines often enrich at full load; water can replace that enrichment |
| Geometry / fuel | Default test engine 86 × 86 mm; best R31/R32 point 86 × 107.5 mm; PRF91 / PRF87 / alcohols | S55 is 84.0 × 89.6 mm, 2979 cc, gasoline |

Important architectural mismatch: Water Engine’s headline gain is **knock-limited CR increase on a naturally aspirated 0-D cycle at high water fraction**. The production M4 GTS is a **turbocharged, plenum/port-injected** system that, on the evidence below, spent the knock margin on **boost and spark**, kept the same **10.2:1** compression ratio, and used a much lower duty-cycle water rate.

## 3. Verdict

**Useful as qualitative and order-of-magnitude context, not as a direct calibration set for the R31/R32 headline point.**

There is solid, citable manufacturer data on hardware, rated power/torque, certified fuel economy, tank size, injection pressure, and the stated mechanism (charge cooling, higher knock limit, more boost, earlier spark). There is **no public measured BSFC map, no official water-to-fuel ratio, no spark-advance degrees, no exhaust-temperature or NOx measurements, and no controlled wet-versus-dry test of the same GTS hardware**. Certified fuel economy for the GTS is the same as, or slightly worse than, the regular M4, because BMW used the system for power, not for a cycle-efficiency gain.

The closer OEM analogue to Water Engine’s CR-increase story is the **2015 BMW 1 Series / three-cylinder prototype** (Innovation Days), which BMW said raised compression from **9.5:1 to 11.0:1**. Those figures are still manufacturer “up to” claims, and that system injects most of the water **directly into the chamber**, not into the intake plenum like the GTS.

## 4. Best sources (short list)

### 4.1 BMW US press kit — primary, official (best single GTS source)

- **URL (original):** https://www.press.bmwgroup.com/usa/article/detail/T0237582EN_US  
- **URL (live redirect, 200 on 11 Nov 2026):** https://newsroom.bmwgroup.com/americas/the-new-2016-bmw-m4-gts-an-exclusive-high-performance-special-edition-m4-available-for-the-first-time-in-the-us  
- **Type:** Primary manufacturer press kit, 6 October 2015.  
- **Engine table (official US specs):** S55B30T0; bore **84 mm**, stroke **89.6 mm**, 2979 cc; compression ratio **10.2:1**; **493 hp** at 6250 rpm; **443 lb-ft** at 4000–5500 rpm; fuel tank **15.8 gal**; fuel AKI 91 minimum, AKI 93 recommended; water injection listed as part of M TwinPower Turbo.
- **Power/torque vs M4:** maximum power “an increase of **16 percent** over the BMW M4”; peak torque “increased by **10 percent** to 442 lb-ft”. US 0–60 mph 3.7 s; limited top speed 189.5 mph.
- **Fuel economy:** “similar levels to those found in the BMW M4 Coupe.” No separate efficiency-gain percentage for the GTS.
- **System:** first production road-car water injection; already used on the M4 MotoGP Safety Car. Three injectors in the intake-manifold plenum, each feeding two cylinders. Water tank **1.3 gallon** in the trunk, pump **approximately 145 psi**, quantity varied with load, speed, and temperature.
- **Thermal numbers in this US kit:** compressor can heat intake air to **as much as 320 °F**; intercooler can reduce that temperature **by as much as 160 °F**; water injection “reduce[s] the temperature of the intake air by an **additional 80 °F**.” Spark can be advanced closer to optimum; boost can be higher; exhaust temperatures are described as lower, with no degrees given.
- **Water use:** on the track the tank “might have to be topped up every time the vehicle is refueled”; on the highway, “every fifth refueling interval.”
- **Failsafe:** if the tank is empty or the system faults, “boost pressure and spark timing are adjusted” so the engine can still run safely. Lines drain back to the tank at shutdown (frost protection).
- **Trust:** high for ratings, geometry, CR, tank size, and pressure. The **80 °F water-cooling figure conflicts with the German BMW M text (~25 °C)**; see §6. The 16 % / 10 % figures are rated output vs the regular M4, not a controlled A/B with only water added.

### 4.2 BMW M technical article (DE + EN) — primary, official

- **English:** https://www.bmw-m.com/en/topics/magazine-article-pool/5-litres-of-water-for-500-horses.html  
- **German (use this for units):** https://www.bmw-m.com/de/topics/magazine-article-pool/5-liter-wasser-fuer-500-pferde.html  
- **Type:** Official BMW M magazine article, 7 October 2015. Both pages were retrieved on 11 Nov 2026 (WebFetch). Curl from this host did not return a clean status, likely bot filtering; treat the pages as live.
- **Key numbers (German text):** compressor heat **up to 160 °C**; intercooler can cool the charge **to below 70 °C**; water spray in the plenum cools the combustion air **by about 25 °C** (“um etwa 25 °C”). Pump **about 10 bar**. Tank **five litres**. Three injectors, each supplying two cylinders. Injection quantity depends on load, speed, and temperature.
- **General technology claims (not GTS certified consumption):** heading “**8 % more performance. 8 % less consumption.**” Body text: if the turbo reaches rated power at peak rpm, power can rise by **about eight percent**. Ambient-temperature power loss above 20 °C can be offset by injecting more water. CEO Frank van Meel: “50 PS und 50 Newtonmeter mehr sollten schon drin sein” (at least 50 hp and 50 Nm more should be available) — a quote, not a test-sheet.
- **Water use:** on the track, refill whenever fuel is refueled; even in fast Autobahn driving, about **every fifth fuel stop**.
- **Failsafe:** boost and spark are pulled back; the engine continues at reduced power. German text adds that M was also looking at air-conditioning condensate (2–3 litres/hour on Alpine summer tests) for a self-replenishing system.
- **Trust:** high for hardware and the **25 °C** cooling figure. The 8 % / 8 % lines are general design claims, not a published GTS BSFC result. The article says water injection can allow a higher compression ratio if the engine is designed that way; it does **not** say the GTS CR was raised.

### 4.3 BMW Group Asia / EU-style press — primary, official

- **URL (original):** https://www.press.bmwgroup.com/asia/article/detail/T0259328EN/the-new-bmw-m4-gts?language=en  
- **Live redirect (200 on 11 Nov 2026):** newsroom.bmwgroup.com APAC mirror of the same release.  
- **Type:** Official press, same car, metric ratings.
- **Numbers:** **368 kW / 500 hp** at 6250 rpm; **600 Nm (442 lb-ft)** at 4000–5500 rpm; 0–100 km/h **3.8 s**; limited top speed **305 km/h**; combined fuel consumption **8.5 l/100 km**, CO2 **199 g/km**, “at the level of the BMW M4 Coupe.” DIN kerb weight 1,510 kg.
- **Trust:** high for official EU ratings. Same caveat: these are vehicle ratings, not a water-only experiment.

### 4.4 Bosch WaterBoost press releases — primary, official, but not GTS-specific

- **US:** https://us.bosch-press.com/pressportal/us/en/press-release-695.html (200)  
- **German:** https://www.bosch-presse.de/pressportal/de/wasser-statt-benzin-mit-dieser-innovation-spart-bosch-bis-zu-13-prozent-kraftstoff-57792.html (200)  
- **Type:** Supplier press, 30–31 August 2016. Bosch supplied water-injection parts for the M4 GTS. Bosch uses **port / intake-duct injection**, not direct in-cylinder injection.
- **Numbers actually in these releases:**
  - Fuel saving **up to 13 percent** when accelerating hard or driving on the freeway / Autobahn.
  - In the then-future cycle (**WLTC**), **up to 4 percent**.
  - Water use “only a few hundred millilitres” per 100 km; tank refilled **on average every 3,000 km**; distilled water.
  - Empty tank: engine still runs, but without the extra torque and lower consumption.
  - Aimed especially at **downsized three- and four-cylinder** midsize-car engines.
- **Not in the official releases opened here:** a “5 percent power” figure. That number appears in secondary reports (for example New Atlas, 1 Sep 2016, https://newatlas.com/bosch-water-injection/45205/ — 200) as something “Bosch says,” but it was not in the Bosch press text opened on this date. Do not treat 5 % as verified from the primary release.
- **Trust:** official for Bosch’s own “up to” claims. These are marketing maxima for a different engine class and duty cycle than the GTS, with no test conditions, engine displacement, or water-to-fuel ratio in the press release. **Do not use 13 % as a GTS or Water Engine calibration point.**

### 4.5 BMW Innovation Days 2015 — 1 Series / three-cylinder prototype (primary text, official URL broken)

- **Original official URL (now broken):** https://www.press.bmwgroup.com/global/article/detail/T0223224EN/bmw-group-innovation-days-2015-drive-technologies-of-the-future — on 11 Nov 2026 this redirected to the generic BMW Group newsroom homepage, not the 2015 article.
- **Working reprint of the BMW text:** https://www.automotiveworld.com/news/bmw-group-innovation-days-2015-drive-technologies-future/ (2 July 2015, 200). Closely matching technical reprint, citing BMW: https://www.car-engineer.com/bmw-tries-direct-water-injection-in-its-3-cylinder-gasoline-engine/ (200).
- **Type:** Official BMW Innovation Days 2015 material, preserved in contemporaneous reprints. Not the M4 GTS production system.
- **Stated numbers:**
  - Most of the water is injected **directly into the combustion chamber**, “rather than just into the intake manifold.” (The same official text also has a paragraph that still says the water is sprayed into the “intake manifold plenum chamber.” The wording is mixed; the distinctive claim is that this prototype is mostly direct in-cylinder injection.)
  - Combustion temperatures reduced by **around 25 °C**.
  - Real-world fuel economy improved by **up to 8 percent**, mainly by avoiding extra fuel for exhaust-temperature control at or near full throttle.
  - Compression ratio of the prototype three-cylinder raised from **9.5:1 to 11.0:1**.
  - Power and torque improved by **up to 10 percent** (earlier ignition and higher boost).
  - Intended to work on **RON 95**.
  - Lower emissions (Car Engineer’s BMW-based write-up says lower **NOx**; the Automotive World reprint says “lower emissions” without naming NOx).
  - MotoGP Safety Car (the GTS-related six-cylinder application) used a **five-litre** boot tank, refilled at every fuel stop in hard race use. The 1 Series concept was meant to be self-replenished from **air-conditioning condensate** in normal use.
- **Baseline engine mentioned for the standard M4 (not the GTS):** 317 kW / 431 hp and 550 Nm (405 lb-ft); combined consumption 8.8–8.3 l/100 km, CO2 204–194 g/km.
- **Trust:** high as a record of what BMW claimed in 2015. Still manufacturer “up to” figures, not a published map. This is the best public OEM evidence that water injection was actually used to **raise compression ratio**, which is the mechanism Water Engine models.

### 4.6 Independent / official cycle data, and weaker test evidence

**EPA fuel economy (official independent cycle test, not a water-injection experiment):**

- 2016 M4 GTS: https://www.fueleconomy.gov/feg/Find.do?action=sbs&id=37347 (200) — **16 city / 23 highway / 19 combined mpg**, premium gasoline, 15.8 gal tank, 300-mile range, 477 g/mi CO2, 3.0 L turbo I6, 7-speed AM-S7. (The fueleconomy.gov page also contains a leftover plug-in-hybrid template sentence about “the first 21 miles”; that is not GTS data and should be ignored.)
- 2016 M4 Coupe, automatic AM-S7: https://www.fueleconomy.gov/feg/Find.do?action=sbs&id=36732 (200, opened 11 Nov 2026) — **17 city / 24 highway / 19 combined mpg**, 459 g/mi CO2, same 15.8 gal tank. Combined mpg is the same 19; city, highway, and CO2 are slightly better on the regular Coupe (GTS is 477 g/mi). This does **not** show an efficiency gain for the GTS. Tires, aero, weight, and mapping all differ, so this is not a clean water-on vs water-off test.

**Motor Trend first drive (press, 13 Apr 2016):**  
https://www.motortrend.com/reviews/2016-bmw-m4-gts-first-drive-review (200)

- Repeats US ratings: 493 hp, 443 lb-ft; EPA 16/23/19.
- Journalist account of the system, attributed to the launch briefing: water sprayed **above approximately 5,000 rpm** through three “steel-tipped diesel injectors”; post-intercooler air cooled “by about 80 degrees to around 115–120 degrees”; boost increased by **4.3 psi**; if the water runs out, “your M4 GTS makes 444 hp” (the then Competition rating). Track: 5 litres / 1.3 gallons of water every fuel fill; street, if driven hard, every five to six tanks; if driven gently below 5,000 rpm, “you’ll never have to refill.” Distilled water only. Head of M engine development Jürgen Poggel said that if alcohol is detected the car goes into limp mode (the reporter flagged doubt about that last point).
- **Trust:** good color from a factory drive, but these operating details are not in the official kit opened here. The “80 degrees … to 115–120 degrees” mixes the US-kit 80 °F delta (see §6) with a final temperature that actually matches a **25 °C** drop from ~70 °C (45 °C ≈ 113 °F). The +4.3 psi boost and 5,000 rpm threshold are **unconfirmed by BMW’s published tables**. Do not use them as hard calibration points.

**One public dyno video (secondary, weak):**  
https://www.bmwblog.com/2016/06/16/video-bmw-m4-gts-posts-492-hp-crank-first-dyno-run/  
WebFetch retrieved the article on 11 Nov 2026; curl got 403.

- One Dynojet run reported as **492 hp “at the crank,”** compared by the writer with BMW’s **500 hp** (the EU PS figure; the official US rating is 493 hp SAE). The same article notes that Dynojet figures are often optimistic and that there was no back-to-back regular M4 on the same dyno.
- **Trust:** low for engineering use. One video, unclear correction method, wrong official-rating comparison, no water-flow, spark, boost, or BSFC data. At most, it does not contradict the rated power. It is not a validation point.

## 5. Related technical literature (not M4 GTS measurements)

These are real papers that study gasoline water injection and could later supply calibration data, but **this pass did not open the full texts**, so no internal numbers are quoted.

| Paper | Record | Why it matters | Status on 11 Nov 2026 |
|---|---|---|---|
| Hoppe, Thewes, Seibel, Balazs et al., “Evaluation of the Potential of Water Injection for Gasoline Engines,” *SAE Int. J. Engines* 10(5):2500–2512, 2017 | https://doi.org/10.4271/2017-24-0149 (resolves to SAE Mobilus, 200) | Direct water injection, CR and Miller variants, drive-cycle fuel vs water consumption trade-off, tank sizing | Abstract only. Full text paywalled. |
| Thewes, Baumgarten, Scharf, Birmes, Balazs, Lehrheuer, Hoppe, “Water Injection – High Power and High Efficiency Combined,” 25th Aachen Colloquium, 2016, pp. 345–380 | https://publications.rwth-aachen.de/record/674458 (200) | Often cited alongside Bosch WaterBoost claims | Bibliographic record only; no PDF retrieved. |
| Pauer, Frohnmaier, Walther, Schenk, Hettinger, Kampmann, “Optimierung von Ottomotoren durch Wassereinspritzung,” 37th Vienna Motor Symposium, 2016 | VDI/Wiley record: https://doi.org/10.51202/9783186799128-ii-18 | Bosch authors; likely the technical basis of the 4 % / 13 % press claims | Not opened. Do not back-fill press numbers from a paper that was not read. |
| Thewes, Hoppe, Baumgarten, Seibel, “Water Injection for Gasoline Combustion Systems,” *MTZ worldwide*, 2014/2015 | https://doi.org/10.1007/s38313-014-1012-0 | Early FEV/RWTH review | Paywalled; not opened. |
| Zhuang et al., “Investigation of water injection benefits on downsized boosted direct injection spark ignition engine,” *Fuel* 264:116765 (2020) | Open copy already cited in the Water Engine `02-legitimate-water-combustion.md` note | Measured KLSA, BTE, BSFC, IMEP vs water/gasoline ratio on a 1.5 L TGDI | Not re-opened in this pass; already in the project research file. This is **not** M4 GTS data. |

## 6. Hard measured data versus marketing, and one unit inconsistency

**Treat as hard, citable facts (ratings, hardware, official cycle results):**

- GTS official output: 368 kW / 500 PS (EU) or 493 hp (US SAE) at 6250 rpm; 600 Nm / 442–443 lb-ft at 4000–5500 rpm.
- Official geometry: 84.0 × 89.6 mm, 2979 cc, CR **10.2:1**, engine code S55B30T0, fuel tank 15.8 gal (≈ 59.8 L).
- Rated gain vs the regular M4: **+16 % power, +10 % torque** (US kit). Implied EU arithmetic from the Innovation Days baseline of 317 kW / 550 Nm: 368/317 = +16.1 %, 600/550 = +9.1 %.
- Certified consumption: EU **8.5 l/100 km, 199 g/km**, “at the level of the M4 Coupe.” EPA GTS **16/23/19**; 2016 M4 Coupe automatic listed at **17/24/19**.
- Hardware: 5 L / 1.3 gal distilled-water tank; three plenum injectors; pump ~10 bar / ~145 psi; quantity mapped by load, speed, and temperature; drain-back and frost protection; failsafe reduces boost and retards spark.
- Track refill ≈ every fuel fill; highway ≈ every fifth fill (official). Bosch general system: a few hundred ml/100 km, typically every ~3,000 km (not a GTS track figure).

**Treat as manufacturer “up to” or qualitative claims, not measured maps:**

- BMW M: “8 % more performance, 8 % less consumption”; “about eight percent” more power when the turbo is at peak rpm.
- Van Meel: “at least 50 hp and 50 Nm more.”
- “Substantial improvement in efficiency” and lower full-throttle consumption, while certified cycle consumption stays at the M4 level.
- Water injection “allows” a higher compression ratio — a design option, not evidence that the GTS CR changed.
- Bosch: up to 4 % in WLTC, up to 13 % in hard acceleration / freeway driving, on downsized 3/4-cylinder engines.
- Innovation Days prototype: up to 8 % real-world economy, up to 10 % power/torque, CR 9.5:1 → 11.0:1, ~25 °C combustion-temperature drop.

**25 °C versus 80 °F (do not average these):**

- German BMW M article: water cools the combustion air **by about 25 °C**. Intercooler cools the charge **to below 70 °C**. Compressor outlet **up to 160 °C**.
- US press kit: water cools intake air by an **additional 80 °F**. Intercooler reduces temperature **by as much as 160 °F**. Compressor outlet **as much as 320 °F**.
- 80 °F as a *difference* is 44 °C, not 25 °C. A common conversion mistake is to treat a 25 °C *difference* as an absolute temperature (25 × 1.8 + 32 = 77 ≈ 80). The 160 °F intercooler figure *does* match a drop from 160 °C to 70 °C (90 °C ≈ 162 °F), because that is a difference taken from two stated endpoints.
- Until BMW publishes a test-sheet, the safer engineering figure is the German **~25 °C** additional drop after the intercooler. Motor Trend’s final temperature of “115–120 degrees” (°F) is consistent with 70 °C − 25 °C = 45 °C ≈ 113 °F, not with an 80 °F drop from a sub-70 °C intercooler outlet.

**Do not use:**

- Bosch 13 % as a GTS result, or as Water Engine’s expected cost/mile gain.
- New Atlas’s “59 kW (80 hp)” GTS gain (arithmetic does not match 368 − 317 = 51 kW).
- The single 492 hp Dynojet video as a calibration point.
- Journalist-only figures (+4.3 psi, “above 5,000 rpm,” “3 % H2O” from a 1 Series drive story) without labeling them unverified.
- Any claim that GTS certified mpg improved because of water injection. Official cycle data do not show that.

## 7. Derived water-use estimates (not official WFRs)

Assumptions are stated so they can be rejected.

Gasoline density is taken as **0.74–0.75 kg/L**; water as **1.00 kg/L**. Official tanks: water **5.0 L**, fuel **15.8 gal = 59.8 L**.

**Track, if the two tanks empty together** (the official wording is that the water tank is topped up every time the car is refueled in hard track use):

- Volume ratio water:fuel ≈ 5.0 / 59.8 = **0.084** (about 1:12).
- Mass `WFR` ≈ 5.0 / (59.8 × 0.74 to 0.75) ≈ **0.111–0.113**.
- Mass fraction `w` ≈ **0.10**.

This is a **duty-cycle average** over a tank, including time when water is not being injected. Instantaneous full-load `WFR` would be higher, and is not published.

**Highway, official “every fifth refueling”:**

- Average volume ratio ≈ one-fifth of the track figure, ≈ **0.017**.
- Average mass `WFR` ≈ **0.022–0.023**, `w` ≈ **0.02**.

**Bosch midsize-car figure, 5 L per 3,000 km:**

- 5 / 3000 = **0.17 L/100 km**, which is consistent with “a few hundred millilitres” per 100 km. That is a Bosch general-use figure, not a GTS track figure, and it still is not an instantaneous `WFR`.

None of these is in the same range as Water Engine’s headline `w = 0.30` (`WFR = 0.43`).

## 8. Map onto Water Engine: what can and cannot be used

| Water Engine quantity | What the public GTS / BMW / Bosch data can do | Usable? |
|---|---|---|
| Charge cooling / evaporative ΔT | German official ~**25 °C** additional intake/combustion-air drop after the intercooler is a real order-of-magnitude check for the evaporative-cooling energy balance. It is a turbo, post-intercooler, plenum-injection result, not a 320/400 K naturally aspirated intake. Use as a directional check, not a fit target, and prefer 25 °C over the US-kit 80 °F. | **Limited use** |
| Knock mechanism | Official qualitative agreement: lower end-gas temperature, higher knock limit, earlier spark, (in a turbo) more boost. No Livengood–Wu data, no CA50, no spark degrees. | Qualitative only |
| Compression ratio | GTS official CR is **10.2:1**. BMW describes a higher CR as something water *can* enable if the engine is designed for it. No official statement was found that the GTS CR was raised versus the regular S55, which is widely specified at the same 10.2:1. **Do not use the GTS as validation of dry CR 8 → wet CR 12.** The 1 Series prototype (**9.5:1 → 11.0:1**) is the closer, still-unmapped, OEM analogue. | **Not usable for the headline CR jump**; prototype is a qualitative analogue only |
| Power / IMEP | Rated GTS vs M4 is +16 % power / +10 % torque, but the cars also differ in exhaust, cooling, mapping, tires, and aero, and the GTS can raise **boost**. Water Engine’s +10.16 % is a naturally aspirated, equal-geometry, CR-driven model result. BMW’s general “about 8 %” power if the turbo is already at the limit is a closer order-of-magnitude remark, still not a test-sheet. | Order-of-magnitude only; not a calibration point |
| Efficiency / BSFC / cost per mile | Official GTS cycle economy is **unchanged** (EU) or **no better** (EPA combined 19 vs 19, with slightly worse city/highway) than the M4 Coupe. BMW spent the knock margin on power. Bosch’s 4 % / 13 % are “up to” figures for other engines and were not independently reproduced here. **Cannot validate −9.728 % cost/mile.** | **Not usable** for the headline cost/mile result |
| `w` / `WFR` | Only duty-cycle averages can be derived (~0.11 track, ~0.02 highway). Instantaneous full-load ratio is unpublished. Headline model `w = 0.30` is far above those averages and above typical production port-injection practice. | **Not usable** to calibrate `w = 0.30` or water-majority (`w > 0.5`) |
| `φ = 1` | BMW and Bosch both say water can replace fuel used for component/exhaust cooling (over-fueling) at high load. That is a real efficiency path the 0-D model, which already assumes `φ = 1`, does not itself demonstrate. | Context for a limitation of the model, not a calibration number |
| EVO / exhaust temperature | Official: lower thermal load on pistons, exhaust valves, catalyst, and turbo; no degrees or maps. | **Not usable** quantitatively |
| NOx / relative NO | No GTS measurements. Innovation Days: lower emissions / (in one reprint) lower NOx, no figures. | **Not usable** |
| Geometry / rpm / boost | Official S55 is 84.0 × 89.6 mm, turbocharged, peak power at 6250 rpm. Water Engine default is 86 × 86 mm NA at 2000 rpm; best R31/R32 point is 86 × 107.5 mm at 1500 rpm. | Hardware context only |
| Failsafe / empty tank | Official: reduce boost, retard spark, reduced power. Motor Trend’s “444 hp” is a journalist paraphrase, not a measured derate curve. | Qualitative only |

**Bottom line for the project:** the M4 GTS proves that production port water injection can cool the charge, raise the knock limit, and support a substantial **power** increase on a turbo gasoline engine, with modest water use. It does **not** provide a measured wet-versus-dry data set that can confirm Water Engine’s modelled cost-per-mile gain, its high water fraction, or its large compression-ratio step. Anyone citing “BMW got 13 % better economy on the M4 GTS” would be misusing Bosch’s midsize-engine marketing figure.

## 9. Gaps (what would make this actually usable)

1. A **controlled engine-dyno map** of the S55 with water on vs water off: same hardware, spark, boost, λ, BSFC, IMEP, EGT, knock index, and water mass flow versus speed and load.
2. Official or measured **instantaneous water-to-fuel ratio** (and whether water is used only at high load / high rpm).
3. **Spark-advance / CA50** and boost pressure with and without water, in degrees and bar, not prose.
4. Confirmation, from a BMW technical paper or parts microfiche, whether GTS **compression ratio and turbo hardware** are identical to the regular M4 S55.
5. Open, numbered results from **Pauer 2016 (Vienna)** and **Thewes/Hoppe 2016–2017 (Aachen / SAE 2017-24-0149)** — the likely home of the 4 % / 13 % claims and of fuel-versus-water trade-off curves.
6. Independent laboratory NOx, CO, and HC data.
7. A working archival copy of the official Innovation Days 2015 press kit (the original BMW Group URL now lands on a generic newsroom page).

## 10. Link check (11 Nov 2026, Pacific Time)

| URL | Status |
|---|---|
| https://www.press.bmwgroup.com/usa/article/detail/T0237582EN_US | 200, redirects to newsroom.bmwgroup.com/americas/… (content confirmed) |
| https://www.press.bmwgroup.com/asia/article/detail/T0259328EN/the-new-bmw-m4-gts?language=en | 200, redirects to an APAC newsroom mirror (content confirmed) |
| https://www.bmw-m.com/en/topics/magazine-article-pool/5-litres-of-water-for-500-horses.html | Content retrieved by WebFetch; curl from this host did not return a clean status |
| https://www.bmw-m.com/de/topics/magazine-article-pool/5-liter-wasser-fuer-500-pferde.html | Same as English; German text used for the 25 °C figure |
| https://us.bosch-press.com/pressportal/us/en/press-release-695.html | 200 |
| https://www.bosch-presse.de/pressportal/de/wasser-statt-benzin-mit-dieser-innovation-spart-bosch-bis-zu-13-prozent-kraftstoff-57792.html | 200 |
| https://www.press.bmwgroup.com/global/article/detail/T0223224EN/bmw-group-innovation-days-2015-drive-technologies-of-the-future | 200 but **wrong page** (generic newsroom home). Official 2015 kit is not at this URL anymore |
| https://www.automotiveworld.com/news/bmw-group-innovation-days-2015-drive-technologies-future/ | 200 (reprint of the official 2015 text) |
| https://www.car-engineer.com/bmw-tries-direct-water-injection-in-its-3-cylinder-gasoline-engine/ | 200 |
| https://www.motortrend.com/reviews/2016-bmw-m4-gts-first-drive-review | 200 |
| https://www.fueleconomy.gov/feg/Find.do?action=sbs&id=37347 | 200 |
| https://www.fueleconomy.gov/feg/Find.do?action=sbs&id=36732 | 200 (2016 M4 Coupe AM-S7 comparison) |
| https://doi.org/10.4271/2017-24-0149 | 200 (abstract / paywall landing page) |
| https://publications.rwth-aachen.de/record/674458 | 200 (bibliographic record) |
| https://newatlas.com/bosch-water-injection/45205/ | 200 (secondary) |
| https://www.bmwblog.com/2016/06/16/video-bmw-m4-gts-posts-492-hp-crank-first-dyno-run/ | Content retrieved by WebFetch; curl 403 |
| https://www.bosch-waterboost.com or .de | Referenced in the 2016 Bosch release; not re-checked as a live technical source on this pass |

## 11. Note on the existing Water Engine research file

`docs/research/02-legitimate-water-combustion.md` (in older worktrees such as `an earlier local checkout (not published here)`) already has a short M4 GTS section. Several points in that file should be treated carefully if it is reused:

- It reports the US-kit **80 °F** cooling figure without the German **25 °C** conflict.
- It correctly flags a journalistic “13 % better fuel efficiency for the GTS” as uncertain; this pass confirms that 13 % is a **Bosch midsize-engine** claim, not a GTS rating.
- Boost “from 1.19 to 1.49 bar relative to the N55” is a secondary, mixed-baseline figure and was not found in the official GTS kit opened here.
- Official CR 10.2:1, 1.3 gal tank, and ~145 psi in that file match the US press kit.

## 12. Open copies of the paywalled papers (follow-up, 11 Nov 2026, Pacific Time)

James asked that paywalled sources always be chased through a legitimate second source. This section records what could, and could not, be opened legally. No Sci-Hub, LibGen, or other pirate sites were used. Local copies of the three official open files are in [`sources/`](sources/PROVENANCE.txt).

### 12.1 What was and was not opened

| Target paper | Legitimate full text? | What was used instead |
|---|---|---|
| Hoppe, Thewes, Seibel, Balazs, Scharf, SAE 2017-24-0149, *SAE Int. J. Engines* 10(5):2500–2512 | **No.** OpenAlex and Semantic Scholar both list it as closed. No author preprint, university PDF, or “all versions” copy was found. | Voßhall (2022) cites it as /30/ and /115/ but does not quote its drive-cycle figures in the passages opened here. |
| Thewes, Baumgarten, Scharf, Birmes, Balazs, Lehrheuer, Hoppe, “Water Injection – High Power and High Efficiency Combined,” 25th Aachen Colloquium, 2016, pp. 345–380 | **No full PDF.** RWTH record says the proceedings were issued on a USB stick. The official colloquium site still hosts later (2019) water-injection PDFs, but not this 2016 paper. | Key vehicle numbers are quoted, with citation, in Voßhall 2022, section 2.2 (see §12.3). |
| Pauer, Frohnmaier, Walther, Schenk, Hettinger, Kampmann, “Optimierung von Ottomotoren durch Wassereinspritzung,” 37th Vienna Motor Symposium, 2016, pp. II-18–II-33 (also cited as pp. 18–33) | **No full paper.** VDI e-library remains paywalled. | Official condensed symposium report (ÖVK / TU Wien) summarises the lecture without maps. Voßhall 2022 quotes the paper’s customer-survey water quantity (see §12.4). |
| Hoppe, Thewes, Baumgarten, Dohmen, “Water injection for gasoline engines: Potentials, challenges, and solutions,” *Int. J. Engine Research* 17(1):86–96, 2016, DOI 10.1177/1468087415599867 | **Yes — official Green OA.** Same authors and lab as the 2016 Aachen and 2017 SAE papers; this is the measured single-cylinder study behind a lot of the later “up to 16 %” language. | Full text opened. Live RWTH URL had a bot challenge from this host; the file was taken from the Internet Archive snapshot of the official RWTH PDF (see provenance). |
| Hoppe, “Einfluss der direkten Wassereinspritzung auf die ottomotorische Verbrennung,” RWTH Aachen dissertation, 2018 | **No PDF retrieved.** Catalogue: https://publications.rwth-aachen.de/record/731830 . A Wayback URL for `…/files/731830.pdf` existed but was HTML, not a PDF, so it was not treated as an open copy. | Voßhall 2022, who used the same single-cylinder setup, quotes two Hoppe-thesis operating points (see §12.5). |
| Thewes, Hoppe, Baumgarten, Seibel, “Wassereinspritzung für ottomotorische Brennverfahren,” *MTZ* 76(2):26–31, 2015 (English: “Water Injection for Gasoline / Petrol Combustion Systems,” *MTZ worldwide* / *Auto Tech Review*) | **No open full text found.** | Cited, not quoted with numbers, in Voßhall 2022 /05/ and /116/. |
| Böhm, Mährle, Bartelt, Rubbert (sometimes listed with Durst), “Funktionale Integration einer Wassereinspritzung in den Ottomotor,” *MTZ* 77(1):38–43, 2016; and Durst et al., MTZ-Fachtagung Ladungswechsel 2015 | **No open full text found.** | Not opened. These are the likely BMW-side MTZ articles; hardware numbers already rest on the official BMW press kit in §4. |
| Voßhall, “Untersuchung eines Ottomotors mit abgaskondensatgespeistem Wassereinspritzsystem,” RWTH Aachen dissertation, 2022, DOI 10.18154/RWTH-2022-11479 | **Yes — official OA.** | Used as a legitimate quotation source for Thewes 2016, Pauer 2016, and Hoppe 2018. Downloaded from the Internet Archive snapshot of the official RWTH PDF. |

### 12.2 Hoppe, Thewes, Baumgarten, Dohmen (2016), *Int. J. Engine Research* 17(1):86–96 — full text, official OA

**Citation:** F. Hoppe, M. Thewes, H. Baumgarten, J. Dohmen, “Water injection for gasoline engines: Potentials, challenges, and solutions,” *International Journal of Engine Research*, vol. 17, no. 1, pp. 86–96, 2016, doi:10.1177/1468087415599867. Received 12 May 2015, accepted 10 July 2015.

**Open links:** official RWTH deposit https://publications.rwth-aachen.de/record/567619/files/567619.pdf (bot-challenged from this host on 11 Nov 2026); Internet Archive snapshot used: https://web.archive.org/web/20240906145018id_/https://publications.rwth-aachen.de/record/567619/files/567619.pdf . Local copy: `sources/Hoppe_Thewes_2016_IJER_1468087415599867.pdf`.

**What this is:** single-cylinder, **direct** water injection (side injector) plus central gasoline DI, on a Miller-cycle, cooled-EGR research engine at **CR 13.5**. This is **not** the M4 GTS port/plenum system and not a turbo vehicle map. It is the best open, numbered, peer-reviewed measurement set from the same FEV / RWTH group that later wrote the 2016 Aachen and 2017 SAE papers.

**Engine (Table 2, p. 89):** 364 cm³, bore 75 mm, stroke 82.5 mm, CR 13.5, four valves, max fuel and water pressure 20 MPa, intake event 230° CA, IVC 240° CA ATDC (1 mm), fuel SOI 300° CA BTDC. Intake air 25 °C. Fuel via the central injector, water via the side injector.

**Theoretical charge cooling (pp. 87–88, Figure 2):** isooctane–air cycle with water injected for 30° CA at 180° CA ATDC? (text: premixed at 2180° CA ATDC — typographically “2 180°”, i.e. −180° / BDC), water/fuel ratio **52 %**. Heat-capacity effect alone ≈ **7 °C** cooler at spark; with evaporation, total mixture-temperature drop ≈ **34 °C**. The authors conclude the cooling is “almost entirely due to evaporation.” Water Δh_v = 2430 kJ/kg vs gasoline ≈ 397 kJ/kg and ethanol 952 kJ/kg (p. 87).

**Measured points (stoichiometric, no EGR, Figure 6, p. 90):** n = 2000 1/min, IMEP = 1.05 MPa. Optimum water SOI around intake-valve closing, **120° CA BTDC**. MFB 50 advanced by **nearly 5° CA**. Efficiency increase ≈ **3 %**. Exhaust-gas temperature reduced by **24 °C** at most. NOx down **up to 13 %** for early SOI and **5.6 %** at the 120° SOI; HC up **up to 11 %**. Target MFB 50 without knock restriction was 7–8° CA ATDC.

**Water pressure (Figure 7, p. 90):** same speed/load, SOI 120° CA BTDC, injected mass **5.3 mg** (1 ms at 10 MPa). 10–15 MPa already near-optimal for MFB 50; efficiency is **1.1 % worse** at 2.5 MPa than at 10 MPa. (This is a 100 bar DI system, not the GTS ~10 bar port pump.)

**With Miller + 16 % cooled EGR (Figure 8, pp. 90–91):** n = 3000 1/min, IMEP = 1.46 MPa. Still knock-limited at CR 13.5. MFB 50 improves linearly with water and reaches the optimum of about **8° CA ATDC at a water–fuel ratio of 50 %**. Best fuel consumption at that 50 % ratio: efficiency gain **3.3 %**. At 2000 1/min the same combination gave **3.8 %**. Exhaust temperature down ≈ **60 °C** at 50 % water/fuel. NOx “nearly constant” (MFB 50 advance offsets the cooling). Burn duration MFB 5–90 “nearly constant.”

**High load (Figure 10, p. 92):** n = 2000 1/min, IMEP = 2.26 MPa. **Stable dry operation was not possible.** The no-water baseline was obtained by **second-order polynomial extrapolation**. At water/fuel **60 %**, MFB 50 advanced by ≈ **15° CA**, exhaust temperature down **more than 100 °C**, efficiency gain **up to 16 %**, NOx down **more than 40 %**, burn duration increased. **This 16 % figure must not be used as a clean wet-versus-dry measurement**; it has the same kind of weak-dry-baseline problem already flagged in the Water Engine R31/R32 notes.

**Lean, λ = 1.4 (Figures 11–13, pp. 93–94):** n = 3000 1/min, IMEP = 1.46 MPa. SOI sweep at water/fuel ≈ **26 %** again favoured 120° CA BTDC. Quantity sweep: maximum efficiency gain **4.5 % at water/fuel 40 %**, exhaust temperature down **50 °C**.

**Authors’ own summary (abstract p. 86 and conclusion pp. 94–95):** 3.3–3.8 % in the region of minimum specific fuel consumption on a stoichiometric Miller + cooled-EGR concept; up to 16 % at full load; 4.5 % in the minimum-BSFC region if water is added to homogeneous lean combustion. Miller + condensate injection is said to be enough for optimal combustion up to about **1.0 MPa BMEP** even at CR 13.5; with VCR they argue part-load CR could go “significantly higher than 13.5.”

**Usable for Water Engine?**

- **Yes, with care, and this is the best open calibration set found in this pass.** Water/fuel 40–60 % is `WFR = 0.40–0.60`, i.e. `w = 0.29–0.38`, which sits on the same water fraction as the R31/R32 headline (`w = 0.30`). That is much more relevant than the GTS tank-average `w ≈ 0.10`.
- Charge-cooling (≈ 34 °C at 52 % WFR, calculated; 24–60 °C EGT drop, measured) is a quantitative check on the evaporative-cooling energy balance, in the same ballpark as BMW’s official ~25 °C intake-air drop, under different hardware.
- Spark / MFB 50 advances of ≈ 5° CA at 1.05 MPa and ≈ 15° CA at the unstable high-load point are usable as knock-model / CA50 order-of-magnitude checks, not as a fit target (different geometry, CR already 13.5, Miller + EGR, direct not port injection).
- Part-load efficiency gains of **3.3–3.8 %** (and 4.5 % lean) are **measured** and are smaller than Water Engine’s modelled **−9.728 % cost/mile**, which also includes a large CR step (8 → 12) from a knock-limited dry baseline. These FEV points already start at CR 13.5; water is used mainly to advance spark, not to raise CR in the test. That is a fair caution against treating the model headline as if it were already demonstrated at a fixed high CR.
- The **16 %** full-load number is **not** usable as a calibration point without the extrapolation caveat.
- NOx (−5.6 to −13 % in the no-EGR SOI sweep; > 40 % at the extrapolated high-load point; nearly flat in the EGR sweep) and EGT drops are usable as qualitative-to-semi-quantitative checks on the relative-NO and EVO-temperature outputs, with the usual mechanism and uncertainty caveats.
- **Not usable** as an M4 GTS validation, as a port-injection calibration, or as a turbo boost / enrichment-replacement vehicle cycle result.

### 12.3 Thewes et al., 25th Aachen Colloquium 2016 — no full PDF; numbers quoted by Voßhall (2022)

**Original:** M. Thewes, H. Baumgarten, J. Scharf, G. Birmes, A. Balazs, B. Lehrheuer, F. Hoppe, “Water Injection – High Power and High Efficiency Combined,” 25th Aachen Colloquium Automobile and Engine Technology, 2016, pp. 345–380. Also listed by Voßhall as /36/ (Thewes as sole named lecturer).

**Quotation source:** T. Voßhall, RWTH dissertation, 2022, section 2.2, PDF pp. 16–17 (printed pp. 3–4). Official OA copy as in §12.1. Voßhall is describing an FEV Europe Audi TT-S (FV) 2.0 l TFSI with a retrofit **port** water-injection system, and he cites Thewes 2016 [/36/] for the water/fuel map and the power/torque gain.

**Numbers Voßhall attributes to Thewes 2016:**

- Applied water-to-fuel mass-ratio map (his Abbildung 2-2, caption explicitly “/36/”): water injection begins at about **p_me ≈ 12 bar** with a maximum `ξ_H2O` = **5 %**, and rises with load to a maximum of **45 %**. The map is used when there is a knock intervention or turbine-inlet temperature **T3 > 930 °C**.
- With the system, power rises from **228 kW to 250 kW (Δ = +10 %)** and peak torque from **380 Nm to 450 Nm (Δ = +18 %)** (section 2.2, PDF p. 17, printed p. 4, citation /36/).

Voßhall also describes an ambient-temperature correction (his Abb. 2-3): at 0 °C the water quantity is cut by 75 % to a factor of 25 %, rising linearly to a factor of 50 % at 30 °C and holding there; the full map (`Φ = 1`) is released if T3 exceeds 930 °C or spark is retarded by at least 1.5° CA from the map. That correction paragraph is **not** explicitly tagged /36/, so it should be treated as Voßhall’s description of the demonstrator calibration, not as a verified Thewes 2016 figure.

**Usable for Water Engine?** Limited but valuable. This is a **port-injection, turbo, vehicle-level** data point, closer to the GTS architecture than the IJER single-cylinder DI work. Peak `WFR = 0.45` (`w ≈ 0.31`) again matches the model headline water fraction at high load, and the +10 % power is in the same range as Water Engine’s modelled +10.16 % and BMW’s general “about 8 %.” It is still a manufacturer/FEV demonstrator result quoted second-hand, not a full map of BSFC, spark, or NOx, and the torque gain includes whatever else was recalibrated on that TT-S.

### 12.4 Pauer et al., 37th Vienna Motor Symposium 2016 — no full paper; official summary + one quoted figure

**Original:** T. Pauer, M. Frohnmaier, J. Walther, P. Schenk, A. Hettinger, S. Kampmann, “Optimierung von Ottomotoren durch Wassereinspritzung / Optimization of Gasoline Engines by Water Injection,” 37th International Vienna Motor Symposium, 28–29 April 2016, proceedings pp. II-18–II-33, doi:10.51202/9783186799128-II-18. Bosch, Schwieberdingen.

**Official condensed report (opened):** https://wiener-motorensymposium.at/fileadmin/Documents/Tagungsberichte/37_2016.pdf (200, 3.67 MB). Local copy: `sources/Vienna_Motor_Symposium_2016_official_condensed_report.pdf`. German summary p. **17**; English summary p. **45**.

The official report confirms, in prose only, that Bosch: assessed several water-injection layouts for cost and series production; showed **measurements on a test engine** with the preferred layout; ran **vehicle simulations of water consumption in various driving cycles**; and presented a German/US customer survey on willingness to refill water. **No BSFC, WFR, spark, EGT, or NOx numbers appear in that summary.**

**Do not misread the three-column layout.** On English p. 45, the sentence “up to 31 % in CO2 savings” belongs to the adjacent Mahle monovalent natural-gas paper (Warth et al.), not to Pauer.

**Quoted Pauer figure, via Voßhall 2022, printed p. 6 / PDF ~p. 17, Abbildung 2-6, citation /52/ (same title and year as the Pauer paper):** a Fraunhofer IAO survey, presented in that 2016 paper, used a refill quantity of **0.16–0.26 l/100 km** of demineralised water and reported stated acceptance of **60 % (Germany)** and **56 % (USA)**. That quantity is consistent with Bosch’s 2016 press line of “a few hundred millilitres per 100 km,” and is a **design / survey assumption**, not a measured BSFC. Voßhall notes that his own FEV demonstrator used about **1 l/100 km** over 20,000 km, four to six times the survey quantity.

The official 2016 Bosch press 4 % WLTC / 13 % highway figures were still **not** found as numbered results in any open full text of the Pauer paper. They remain marketing “up to” claims until the full symposium paper or a later paper that actually quotes those test points is opened.

**Usable for Water Engine?** The 0.16–0.26 l/100 km figure is usable only as a **duty-cycle water-budget** check for a production-like port-injection system, not as a WFR or efficiency calibration. The 4 % / 13 % press claims are still not usable as calibration points.

### 12.5 Hoppe 2018 dissertation — no PDF; two operating points quoted by Voßhall

Voßhall 2022, chapter 5, Tabelle 5-1 and the following operating-point table (citation /85/), states that both of the following points were clearly knock-limited, or unreachable, at the chosen compression ratio without water injection, after Hoppe 2018:

- 2000 1/min, 14.5 bar IMEP, CA50 without water = **25° CA aTDC**
- 2000 1/min, 22.5 bar IMEP, **not reachable without water injection**

He then ran a water-mass sweep of `ξ_H2O = 15–120 %` at λ = 1, advancing spark to the knock limit, “cf. /85, 115/” (Hoppe 2018 and SAE 2017-24-0149). Those sweep **results** are Voßhall’s own measurements, not quoted Hoppe numbers, and are not extracted here as Hoppe/SAE calibration data.

**Usable for Water Engine?** Only the two dry knock-limit points above, and only as a second-hand quotation, until the dissertation PDF is obtained from RWTH.

### 12.6 Updated verdict for Water Engine calibration

The open Hoppe/Thewes 2016 IJER paper is the first **peer-reviewed, page-cited, measured** dataset that can actually be used to challenge or support the Water Engine model, with the caveats in §12.2. Together with Voßhall’s quotation of Thewes 2016, the picture is:

- High-load water fractions around `w ≈ 0.30` (`WFR ≈ 0.4–0.5`) are consistent with FEV’s measured and mapped practice, unlike the much lower GTS **tank-average** use.
- Charge cooling of order 25–35 °C and spark advances of order 5–15° CA are consistent in direction with the model’s knock-relief story.
- **Measured part-load efficiency gains at an already-high CR (13.5) are 3–4.5 %, not ~10 %.** The model’s larger cost/mile gain still depends on a CR increase from a knock-limited dry baseline, which the GTS did not do and which the IJER tests only discuss as a future VCR possibility. That is the main calibration tension, and it is now documented from an official open paper rather than from marketing.
- The 16 % full-load IJER figure, Bosch’s 13 %, and the GTS rated +16 % power must not be mixed together or treated as a single “water gives 13–16 %” constant.

**Still missing, and still worth chasing legally:** the full Pauer 2016 paper (the 4 % / 13 % test conditions), the 2016 Aachen proceedings PDF or slides, SAE 2017-24-0149 (drive-cycle fuel-vs-water trade-off and CR/Miller variants), Hoppe’s 2018 dissertation, and the BMW/Bosch MTZ articles. A later check of the live RWTH deposits in a browser (the official files are Green OA; only the bot challenge blocked this host) may yet yield the dissertation.


## Trust tier (James, Nov 11 2026 12:44 AM PST)
James designated the German RWTH Aachen / FEV measured data (Hoppe, Thewes, Baumgarten, Dohmen, IJER 17(1) 2016; Voßhall 2022 RWTH dissertation quoting Thewes 2016) as HIGH-TRUST reference data for Water Engine calibration checks. Caveat kept: IJER high-load 16% figure uses an extrapolated dry baseline.
