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


Corrections already found in the Germany draft (do not reuse the wrong figures): the GTS is not a 500-car run; “+37 hp vs M4” is wrong; Alpina/Brabus factory water-injection kits were not confirmed; a shared patent list was mis-attributed across firms; “up to 50% NOx” is not what Welscher’s abstract says.
