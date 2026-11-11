# Water injection — public research notes

Literature research only. These notes collect **summaries, numbers, citations, and links** about adding water to the vehicle combustion cycle (water injection, water-methanol / ADI, water-fuel emulsions, and related cycles). They do **not** change Water Engine model code or results.

**Date:** 11 November 2026, America/Los_Angeles.  
**Repository path:** `docs/research/water-injection/`  
**Branch / PR:** first survey notes merged via [PR #22](https://github.com/redwing509/water-engine/pull/22). The why-not-adopted study is a later docs-only addition.

## How to read this folder

- Unverified, secondary, manufacturer-claim, or paywalled figures are marked in the notes. Prefer the verification sections over raw draft text.
- When a paper is paywalled, a **legitimate** alternate copy is used if one exists (author preprint, thesis, university repository, conference slides, or a later open paper that quotes the numbers). Piracy sites are not used. If no legitimate open copy is found, the bibliographic record is cited and unseen numbers are marked paywalled.
- **Copyrighted PDFs are not committed here.** Links and citations only.
- Country reports 01–24 have been checked (01–15 in the first pass; Brazil through Canada and Priority B Belgium–Denmark in a later 11 Nov 2026 pass). A follow-up study on why production programmes were not continued is in [`why-not-adopted/why-not-adopted.md`](why-not-adopted/why-not-adopted.md).

## Contents

| File | Status | What it is |
| --- | --- | --- |
| [bmw-m4-gts-bosch-waterboost-20261111.md](bmw-m4-gts-bosch-waterboost-20261111.md) | Checked 11 Nov 2026 | BMW M4 GTS / Bosch WaterBoost hardware, official ratings, and what is (and is not) usable for Water Engine calibration |
| [country-survey/COUNTRY_LIST.md](country-survey/COUNTRY_LIST.md) | Plan | Ordered country list for the worldwide historical survey |
| [country-survey/01-germany.md](country-survey/01-germany.md) | Checked 11 Nov 2026 | Germany: makers, universities, measured data, source checks, and corrections |
| [country-survey/02-usa.md](country-survey/02-usa.md) | Checked 11 Nov 2026 | United States: Jetfire, ADI (aviation), aftermarket, labs; source checks and rejected paper/patent IDs |
| [country-survey/03-japan.md](country-survey/03-japan.md) | Checked 11 Nov 2026 | Japan: SIP Tokyo Tech/Keio super-lean + in-cylinder WI, patents (not production cars), source checks and corrections |
| [country-survey/04-france.md](country-survey/04-france.md) | Checked 11 Nov 2026 | France: Aquazole emulsion fleets, Renault F1 racing WI, IFPEN/Renault/PSA SAE 2019 work; source checks and corrections |
| [country-survey/05-uk.md](country-survey/05-uk.md) | Checked 11 Nov 2026 | United Kingdom: Bath/Golzari WI on the ULTRABOOST engine, no production car; source checks and corrections |
| [country-survey/06-italy.md](country-survey/06-italy.md) | Checked 11 Nov 2026 | Italy: CNR and PoliTo/Marelli research, racing specials; intercooler spray excluded; source checks and corrections |
| [country-survey/07-sweden.md](country-survey/07-sweden.md) | Checked 11 Nov 2026 | Sweden: Saab Sport kit accessory, Chalmers/Volvo Cars PWI, missed KTH methanol work; source checks |
| [country-survey/08-russia.md](country-survey/08-russia.md) | Checked 11 Nov 2026 | Russia/USSR: patents and later diesel intake-WI research; no production car; unsourced NAMI figures rejected |
| [country-survey/09-china.md](country-survey/09-china.md) | Checked 11 Nov 2026 | China: no production WI car; Japanese figures and a US-origin CN filing rejected; missed Chongqing/CNHTC research noted |
| [country-survey/10-south-korea.md](country-survey/10-south-korea.md) | Checked 11 Nov 2026 | South Korea: KAIST/SNU–Hyundai lab work, no production car; IJAT 2024 open-access BSFC figures |
| [country-survey/11-czech-republic.md](country-survey/11-czech-republic.md) | Checked 11 Nov 2026 | Czech Republic: Hanon Hluk / BUT WAHASY harvester (open 2021 paper); no production car; source checks |
| [country-survey/12-austria.md](country-survey/12-austria.md) | Checked 11 Nov 2026 | Austria: AVL RACETECH hydrogen race engine with port WI, TU Wien thesis, TU Graz HD hydrogen work; no production car |
| [country-survey/13-netherlands.md](country-survey/13-netherlands.md) | Checked 11 Nov 2026 | Netherlands: no production WI car; TU/e 2019 TGDI work missed by the draft; Delft/NPS hydrogen items relabelled |
| [country-survey/14-switzerland.md](country-survey/14-switzerland.md) | Checked 11 Nov 2026 | Switzerland: no production road WI vehicle; Wärtsilä Winterthur marine DWI and ETH/FHNW emulsion research |
| [country-survey/15-india.md](country-survey/15-india.md) | Checked 11 Nov 2026 | India: no production WI vehicle; open Ashok Leyland/Amrita 2019 intake-WI paper; ARAI and six-stroke figures qualified |
| [country-survey/16-brazil.md](country-survey/16-brazil.md) | Checked 11 Nov 2026 | Brazil: no production WI vehicle; Unicamp/MWM 2009 emulsion and UFMG/Bosch research; several open sources the draft had marked paywalled |
| [country-survey/17-spain.md](country-survey/17-spain.md) | Checked 11 Nov 2026 | Spain: no production WI vehicle; Seville 2019 intake-WI (open abstract NOx 60–70 %); student work qualified; Austrian and news figures rejected |
| [country-survey/18-poland.md](country-survey/18-poland.md) | Checked 11 Nov 2026 | Poland: no production WI vehicle; Lublin 2024 hydrogen Wankel + WI (open abstract); Gulak news and Ursus C-45 WI claims rejected |
| [country-survey/19-australia.md](country-survey/19-australia.md) | Checked 11 Nov 2026 | Australia: no production WI vehicle; Deakin 2024 open model of intake WI on a hydrogen/diesel Cummins; missed Monash emulsion and Melbourne H2+WI work |
| [country-survey/20-canada.md](country-survey/20-canada.md) | Checked 11 Nov 2026 | Canada: no production WI vehicle; Rival Technologies patent tests (NOx up to −33.5 %); ORF SAE 790925 and Transport Canada ICEF2005-1235 records without opened percentages |
| [country-survey/21-belgium.md](country-survey/21-belgium.md) | Checked 11 Nov 2026 | Belgium: no production WI vehicle; missed UCLouvain 2019 water-DI HCCI thesis; VUB mHAT is industrial; German Aarburg emulsion numbers corrected |
| [country-survey/22-finland.md](country-survey/22-finland.md) | Checked 11 Nov 2026 | Finland: no production WI road vehicle; Wärtsilä marine DWI (official 50–60 % NOx); missed Åbo Akademi 2009 official abstract |
| [country-survey/23-norway.md](country-survey/23-norway.md) | Checked 11 Nov 2026 | Norway: no production WI road vehicle; company-hosted MARINTEK 2009 White Diesel summary (NOx −0.88 % per percent water); Danish EPA report removed from Norway totals |
| [country-survey/24-denmark.md](country-survey/24-denmark.md) | Checked 11 Nov 2026 | Denmark: no production WI road vehicle; official EPA 1380 Copenhagen 4T50ME-X WIF tests (NOx approaching −60 % at 50 % load); MAN DWI ratios and DTU SCR paper not taken as combustion-cycle maps |

## Usable measured / official figures (short)

See the individual notes for caveats, units, and links. Headline items as of the first publish:

- **BMW M4 GTS (production, 2016):** official **368 kW / 500 hp**, **600 Nm**, 3.0 L turbo in-line six, intake-plenum water injection, 5 L tank, ~10 bar pump. Certified fuel economy is described as at the level of the M4 Coupe — not a measured cycle-efficiency win. Manufacturer technology claims (8%/8%, 4% WLTC / 13% highway from Bosch) are not independent maps.
- **Hoppe, Thewes, Baumgarten, Dohmen (RWTH Aachen / FEV), 2016**, open RWTH copy: laboratory single-cylinder, about **3.3%–3.8%** efficiency gain near minimum BSFC (stoichiometric, Miller + cooled EGR), up to **16%** at full load, about **4.5%** with homogeneous lean. DOI 10.1177/1468087415599867; https://publications.rwth-aachen.de/record/567619
- **Massoud, TU Berlin dissertation, 2024**, open DepositOnce (CC BY 4.0): indicated efficiency about **+0.8 pp** (port, 10 bar), **+1.2 pp** (direct, 400 bar), **+2.0 pp** (best 10% microemulsion, 200 bar). https://doi.org/10.14279/depositonce-21307
- **Welscher et al., KIT / Stuttgart, 2023**: 562 port-WI points on a Euro 6d diesel single-cylinder. Use the abstract’s 62/40/20 soot-neutral shares and g/kWh NOx figures, **not** a “50% NOx” shorthand. DOI 10.1177/14680874211044297; KITopen 1000137777.

- **Oldsmobile Jetfire (1962–1963):** official **215 hp / 300 lb-ft**, **10.25:1** CR, water-methanol Turbo-Rocket Fluid, ~5 psi boost, 9,607 built. Use SAE **620221** (not 620001). Do not use a 10–15% economy claim. Failsafe when the fluid tank is dry.
- **Tokyo Tech / Keio (SIP, Nagasawa et al., 2020):** 0.5 L single-cylinder, super-lean burn plus in-cylinder water injection. Open write-ups: gross indicated thermal efficiency **48.7 % → 50.2 %** at CR 15, λ=1.9, W/F 39 %; **52.6 %** (abstract **52.63 %**) at CR 17, λ=1.9, W/F 50 %. Official Tokyo Tech press also gives **51.5 %** brake thermal efficiency. The 52.6 % figure is the combined system, not a water-only gain. DOI 10.1177/1468087420908164 (PDF paywalled; figures from official PR, JSAE Engine Review, and Keio abstract).
- **No Japanese production road car** with combustion-cycle water injection was confirmed. Honda holds port-WI patents; Subaru STI S209 uses intercooler water spray, which is out of scope.

- **Elf Aquazole (late 1990s, heavy-duty emulsion fuel, not a passenger-car injection system):** official CORDIS 1998 figures — NOx **15–30 %**, PM **10–50 %**, black smoke **30–80 %**, energy/CO₂ **1–4 %** down, volumetric fuel consumption up. https://cordis.europa.eu/article/id/10155-adding-water-to-diesel-fuel-to-reduce-pollution
- **IFPEN / Renault / PSA / Magneti Marelli, SAE 2019-01-1139 (open abstract):** downsized GDI single-cylinder, port and direct water injection; over-fuelling eliminated; **about 13 %** fuel-consumption reduction at the stated high-load condition. DOI 10.4271/2019-01-1139 (PDF paywalled).
- **No French production passenger car** with combustion-cycle water injection was confirmed. Renault F1 water injection (1983–1986) is racing only.

- **University of Bath / Golzari et al., 2019 (open abstract):** port water injection on a boosted downsized GDI using ULTRABOOST engine hardware — up to about **5 %** net indicated efficiency at medium load and **15 %** at high load; NOx down up to about **60 %**. DOI 10.1177/1468087419832791 (PDF paywalled). These figures are **not** from the 2010–2013 ULTRABOOST project paper (SAE 2014-01-1185), which has an open White Rose copy and does not study water injection.
- **No UK production road car** with combustion-cycle water injection was confirmed.

- **CNR Istituto Motori (Marchitto, Tornatore, Valentino et al., 2018, open abstract):** port water injection on a small turbocharged PFI SI engine reduced over-fuelling and particle number and improved efficiency without a load penalty. DOI 10.1061/(ASCE)EY.1943-7897.0000559. No percentage map extracted from a paywalled PDF.
- **Politecnico di Torino, SAE 2023-01-0181 (open abstract):** numerical cycle study after wet/dry map validation — potential **4–8 %** CO₂ reduction, water **< 1.1 L/100 km**, with high CR and Miller. DOI 10.4271/2023-01-0181 (PDF paywalled).
- **No Italian series-production passenger car** with combustion-cycle water injection was confirmed. Autodelta GTA SA and Ferrari F1 Emulsistem are competition/racing. Fiat Uno and Integrale “Sacca” systems are intercooler spray, out of scope.

- **Saab Sport kit (late 1970s–1980s accessory):** official kit for 99/900 Turbo, water injected upstream of the compressor; PistonHeads: boost about **10 → 17.4 psi**, claimed **145 → at least 160 bhp**. Not standard on every car. Do not use a 15–25 % fuel-economy claim.
- **Chalmers / Khatri (2019–2022), Volvo Cars 1.5 L 3-cyl turbo GDI, port WI:** open licentiate PDF plus SAE 2019-01-0034 / **2020-01-0798**. Experimental knock/enrichment work; **~0.5–1 %** cycle fuel-consumption figures are **mild-hybrid simulations**, not a measured map.
- **No modern Swedish series-production passenger car** with factory combustion-cycle water injection was found.

- **No Soviet or Russian series-production passenger car** with factory combustion-cycle water injection was found. Confirmed USSR/RU patents include SU 769051, SU 1677356, and **RU 2069274** (not SU). Do not use unsourced NAMI “11.6 K / 11.8 %” figures. Later Russian diesel intake-WI work exists (Dmitriev & Khlyupin 2008; *Energies* 2020 on a 12CHN15/18), without extracted maps in this pass.

- **No Chinese OEM series-production passenger car** with factory combustion-cycle water injection was found. Do not use Tokyo Tech 52.6 % / 60 % NOx figures here (they are Japanese). CN1164268A is an Entherm/US filing published in China in 1997, not a 2006 Chinese invention. Later Chinese academic work exists (Chongqing University / CNHTC, *Fuel* 2020, DOI 10.1016/j.fuel.2020.117376); no map was extracted from an opened open copy in this pass.

- **No Korean OEM series-production passenger car** with factory combustion-cycle water injection was found (Hyundai/Kia patents are not production evidence).
- **KAIST / Bae with Hyundai, IJER 2016 (open abstract):** 1.6 L NA prototype, CR 13.5, 5 MPa direct water injection; over-fuelling eliminated at 1,500–3,000 r/min full load; BSFC improved. No percentage in the abstract. DOI 10.1177/1468087415613221.
- **Seoul National University / Min with Hyundai, IJAT 2024 (open access):** 2.0 L NA PFI, 100 bar direct WI. WI-only BSFC down up to **4.95 %** / **6.1 %**; WI + EGR up to **9.14 % versus base** (not 9.3 %). DOI 10.1007/s12239-024-00058-y.

- **No Czech series-production passenger car** with factory combustion-cycle water injection was found.
- **Hanon Systems (Hluk) / Brno University of Technology with FEV and Hanon Germany, 2021 (open MDPI):** WAHASY exhaust-condensate harvester on FEV’s Audi TT-S water-injection demonstrator; vehicle-point **90 % harvest efficiency** (not thermal efficiency). DOI 10.3390/ijerph18105392. Do not use “40–50 % WFR = 10 % EGR” as a Czech measurement (Conway 2019).

- **No Austrian series-production passenger car** with factory combustion-cycle water injection was found.
- **AVL RACETECH (Graz) hydrogen ICE race prototype (official press release):** **410 hp** from a **2 L** hydrogen combustion engine on the testbed; port water injection is described for combustion/thermal control. Racing only; do not treat 410 hp as a water-only gain. https://www.avl.com/en/press/press-release/410-hp-2-liter-displacement-prototype-h2-ice-race-engine-avl-racetech-proves-itself-testbed

- **No Dutch series-production passenger car** with factory combustion-cycle water injection was found. A 2009 Dutch-inventor patent (US 2009/0188467 A1) is a concept only. Eindhoven University of Technology published 2019 work on intake water injection on a 1.5 L TGDI engine (open record; percentages not extracted here). Do not attribute water injection or a 17 % NOx figure to the NPS Driven MH2X 250G hydrogen conversion.

- **No Swiss series-production road vehicle** with factory combustion-cycle water injection was found. Wärtsilä NSD Schweiz (Winterthur) direct water injection is a **marine** large-bore diesel technology. FHNW/ETH 2017 medium-speed emulsion + EGR work is also marine; do not use the draft’s 20 % / ~70 % figures.

- **No Indian series-production road vehicle** with factory combustion-cycle water injection was found.
- **Ashok Leyland / Amrita, IOP 2019 (open PDF):** heavy-duty diesel, atomized intake-manifold water injection. At **2.8 mg/cylinder**: in-cylinder temperature about **90 °C** down, **NOx 8–10 %** down, **smoke about 20 %** up, power unchanged. DOI 10.1088/1757-899X/577/1/012186. Laboratory/conference result, not a production truck. Do not use a 176 km/L six-stroke news claim, or the draft’s ARAI 33/36/24/20 % emission cuts, without an opened open copy.

- **No Brazilian series-production road vehicle** with factory combustion-cycle water injection was found.
- **Sperl, Unicamp / MWM, 2009 (open dissertation record + Jornal da Unicamp):** 3.0 L Euro III heavy-duty diesel, **22 wt %** water emulsion B, unchanged calibration, NBR 15634 13-mode: **NOx down 22 %**, **PM down 42 %**, **SFC up 8 %** on average. Laboratory, not production. https://hdl.handle.net/20.500.12733/1611365
- **Dantas Neto et al., UFRN, BJCE 2011 (open SciELO PDF):** diesel-water microemulsions, 15 wt % surfactant; only **up to 6 % water** met Brazilian fuel specs; SFC above diesel; CO and NOx up, smoke down versus diesel. DOI 10.1590/S0104-66322011000300017.
- **da Rocha et al., UFMG / Bosch, Energy 2021 (open abstract):** single-cylinder SI, 1500 r/min, 5 and 8 bar IMEP; water-injection timing and pressure reduced ISFC by **3 %** and **3.5 %**. DOI 10.1016/j.energy.2020.119346 (PDF paywalled).
- **Bosch LTDA, SAE 2021-36-0082 (open official abstract):** flex-fuel vehicles, higher compression ratio enabled by water injection; energy use down **up to 7.3 %** (1.59 → 1.47 MJ/km, naturally aspirated PFI) and **up to 4.8 %** (1.85 → 1.76 MJ/km, turbo DI). DOI 10.4271/2021-36-0082. Not a same-compression-ratio water-only map. Do not use the UFMG *Energies* 2022 **45.3 %** indicated-efficiency figure as a measured result (1D prediction).

- **No Spanish series-production road vehicle** with factory combustion-cycle water injection was found.
- **Serrano et al., Universidad de Sevilla, Energy 2019 (open idus abstract):** intake-manifold water injection with a flow-blurring injector on a modern diesel; **NOx down around 60–70 %** at different loads and speeds. DOI 10.1016/j.energy.2018.11.136; https://hdl.handle.net/11441/163994 . Laboratory, not production. Do not use AVL Racetech 410 hp here (Austrian) or news-site 67 % / 68 % emulsion figures.

- **No Polish series-production road vehicle** with factory combustion-cycle water injection was found.
- **Biały, Politechnika Lubelska, 2024 thesis (open official abstract):** hydrogen-fuelled Wankel on a dynamometer with in-chamber water injection; water quantity and duration can suppress or eliminate knock. PDF is closed access; no BSFC/NOx percentages extracted. https://hdl.handle.net/20.500.14629/18642 . Do not use Jan Gulak news figures or treat the Ursus C-45 as a water-injection tractor.

- **No Australian series-production road vehicle** with factory combustion-cycle water injection was found.
- **Sharkey and Zare, Deakin, *Energies* 2024 (open MDPI):** AVL Boost model of a Cummins ISBe 220 with intake-manifold water injection (0–700 mg/cycle), validated on baseline diesel only. Simulated water-injection increments at 700 mg/cycle include about **0.5 %** power / thermal-efficiency change and up to about **16 % / 83 %** NO / NO2 cuts versus the same hydrogen fraction. The **94 % / 96 %** CO / CO2 cuts and **~8.8 %** power rise at 90 % hydrogen are hydrogen-substitution effects, not measured water-only gains. DOI 10.3390/en17235838.
- **Mortimer et al., University of Melbourne, *Fuel* 2023 (open official poster):** Caterpillar C15 hydrogen DI test with intake-manifold water; about **25 % more power** at efficient combustion phasing by suppressing autoignition. https://energy.unimelb.edu.au/__data/assets/pdf_file/0003/4922751/mortimerMEI23A_v2.pdf (journal PDF paywalled). Do not use HYDI / HHO / Yull Brown claims as water-injection data.


- **No Canadian series-production road vehicle** with factory combustion-cycle water injection was found.
- **Rival Technologies Inc. (Canada), US 7,216,607 B2 (open official patent text):** charge-air water injection. Test-section engines were a **1995 Caterpillar 3406E** and a **Cummins NTC-350** (the Dodge Ram 2500 is the preferred-embodiment vehicle, not the test article). NOx mass down **up to 33.5 %** at **0.39 L/min (WFR = 40 %)**; particulate mass down **2–8.4 %**; fuel consumption down **as much as 0.5 %** (Caterpillar) and **2.0 %** (Cummins) at about **20 %** water/fuel; power unchanged within **±0.1 %**. Patent/prototype, expired 2011, not production. https://patents.google.com/patent/US7216607B2
- **Lawson and Last, Ontario Research Foundation, SAE 790925 (1979, not 1989):** real HydroShear unstabilized emulsion paper (DOI 10.4271/790925). Official record exists; the PDF was not confirmed open in this pass, so draft percentages were not taken. **Radloff and Gautier, Transport Canada, ASME ICEF2005-1235** is also a real charge-air water-injection paper (DOI 10.1115/ICEF2005-1235); the official abstract was not opened, so the draft’s 10–35 % NOx figure was not taken. Aquazole is French (already in the France report). Do not use Stanley Meyer “water fuel cell” filings.


- **No Belgian series-production road vehicle** with factory combustion-cycle water injection was found.
- **Collette and Gatin, UCLouvain, 2019 master’s thesis (open official abstract):** water direct injection on an HCCI single-cylinder bench; equivalence ratio **0.2 → 0.5**, abstract “**215 % boost**” of power density (read cautiously as possibly 2.15×). Laboratory thesis, not a vehicle. https://thesis.dial.uclouvain.be/entities/masterthesis/ea96dd2d-0d34-415c-b6f7-3d78dca0af79
- **VUB micro Humid Air Turbine (official abstract):** Turbec T100 with a spray saturator, industrial CHP, not a vehicle engine. At fixed speed, power **>+30 %**, fuel **+11 %**, electrical efficiency **up to +4.2 percentage points**. https://researchportal.vub.be/en/publications/experimental-characterisation-of-a-micro-humid-air-turbine-assess/
- **LANUV-Fachbericht 77 (2017, open PDF):** German Exomission emulsion retrofit on an inland ship whose engine is an **ABC 6DZC**; E3 **NOx −18.4 % / −17.5 %**, **PM −21.3 % / −44.6 %** (stability caveats). Not ABC’s own programme and not “NOx about 30 %.” https://www.lanuv.nrw.de/fileadmin/lanuvpubl/3_fachberichte/Fachbericht77_MSAarburg.pdf


- **No Finnish series-production road vehicle** with factory combustion-cycle water injection was found.
- **Wärtsilä official encyclopedia, Direct Water Injection (marine):** combined fuel/water valve, water pressure **200–400 bar**, **50–60 % NOx** reduction with some fuel-consumption penalty. The official page opened here does not state a 0.4–0.7 water-to-fuel ratio or “up to 70 %” NOx. https://www.wartsila.com/encyclopedia/term/direct-water-injection-(dwi) . Two-stroke Winterthur DWI remains in the Switzerland report.
- **Sarvi, Kilpinen, and Zevenhoven, Åbo Akademi, Fuel Processing Technology 2009 (open official abstract):** large medium-speed diesel; NOx “can be more than halved” by DWI; common rail + DWI **maximum about 50 %** NOx reduction. Finnish university work, not an external paper. DOI 10.1016/j.fuproc.2008.09.003.


- **No Norwegian series-production road vehicle** with factory combustion-cycle water injection was found.
- **Eco Energy Holding company summary of commissioned MARINTEK tests (February 2009):** Lite White Diesel emulsions with **8–15 % water**. Average NOx reduction factor **0.88** (NOx down **0.88 % per percent water** in that range); average **CO −39 %**, **THC −12 %**, **smoke about −50 %**, **PM about −21 %**. Marine laboratory test, company-hosted summary; engine identity and SFC were not taken from that page. https://www.eco.as/tests/marintek/2009/ . Do not use the draft’s executive-summary “NOx up to 50 % / PM up to 89 %,” which were not in the opened summary. A Danish EPA 2011 emulsion report listed in the draft belongs under Denmark.


- **No Danish series-production road vehicle** with factory combustion-cycle water injection was found.
- **Andreasen and Nyggard, Danish EPA Environmental Project No. 1380 (2011, official open PDF):** water-in-fuel emulsion tests on the **B&W 4T50ME-X** two-stroke research engine in **Copenhagen**. NOx (g/kWh) **approaching −60 %** at **50 % load** at the highest water content applied (water content = water/fuel added). CO and filter smoke number fall; ISO 8178 particulate **mass rises**; HC is somewhat higher. Combined WIF+EGR (preliminary): NOx **down to 0.2 g/kWh** (above 90 %, sometimes above 98 %). Marine laboratory, not a road vehicle. https://www2.mst.dk/udgiv/publications/2011/08/978-87-92779-30-4.pdf . Do not pair the 60 % NOx figure with “50 % water” unless reading that from the figure; do not use draft MAN DWI 50–60 % / 0.45 / 0.55 ratios, or the DTU SAE 2020-01-2196 SCR water/urea paper, as combustion-cycle maps.

- **Why production programmes were not continued (checked follow-up):** added tank/pump/injectors and a refill of distilled water are documented official features (BMW M4 GTS, Bosch WaterBoost). The GTS was a **700-unit** limited run; BMW M’s Frank van Meel said the engine was meant for that car and that further use depended on the vehicle concept. Official EU/EPA figures show the GTS was not a cycle-economy win versus the M4 Coupe (combined **8.5 L/100 km** / EPA combined **19 mpg**). Jetfire field problems and a 1965 free de-turbo conversion are documented in secondary histories; Saab’s system was a **Sport kit**, not a 1970–73 “Turbo X” factory programme. Draft claims of a regulatory “no fuel-economy credit” rule (40 CFR 86.1807, UNECE R94, EU 2020/…) were **incorrect**. **No documented oil-company lobbying** was found.











Corrections already found in the Germany draft (do not reuse the wrong figures): the GTS is not a 500-car run; “+37 hp vs M4” is wrong; Alpina/Brabus factory water-injection kits were not confirmed; a shared patent list was mis-attributed across firms; “up to 50% NOx” is not what Welscher’s abstract says.
