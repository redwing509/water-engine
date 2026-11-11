# Water injection — public research notes

Literature research only. These notes collect **summaries, numbers, citations, and links** about adding water to the vehicle combustion cycle (water injection, water-methanol / ADI, water-fuel emulsions, and related cycles). They do **not** change Water Engine model code or results.

**Date:** 11 November 2026, America/Los_Angeles.  
**Repository path:** `docs/research/water-injection/`  
**Branch / PR:** `research/water-injection-20261111` (docs-only).

## How to read this folder

- Unverified, secondary, manufacturer-claim, or paywalled figures are marked in the notes. Prefer the verification sections over raw draft text.
- When a paper is paywalled, a **legitimate** alternate copy is used if one exists (author preprint, thesis, university repository, conference slides, or a later open paper that quotes the numbers). Piracy sites are not used. If no legitimate open copy is found, the bibliographic record is cited and unseen numbers are marked paywalled.
- **Copyrighted PDFs are not committed here.** Links and citations only.
- Country reports are added as each one is checked. A follow-up study on why production programmes were not continued will be added in `why-not-adopted/` when that job runs.

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








Corrections already found in the Germany draft (do not reuse the wrong figures): the GTS is not a 500-car run; “+37 hp vs M4” is wrong; Alpina/Brabus factory water-injection kits were not confirmed; a shared patent list was mis-attributed across firms; “up to 50% NOx” is not what Welscher’s abstract says.
