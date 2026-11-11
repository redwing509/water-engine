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

## Usable measured / official figures (short)

See the individual notes for caveats, units, and links. Headline items as of the first publish:

- **BMW M4 GTS (production, 2016):** official **368 kW / 500 hp**, **600 Nm**, 3.0 L turbo in-line six, intake-plenum water injection, 5 L tank, ~10 bar pump. Certified fuel economy is described as at the level of the M4 Coupe — not a measured cycle-efficiency win. Manufacturer technology claims (8%/8%, 4% WLTC / 13% highway from Bosch) are not independent maps.
- **Hoppe, Thewes, Baumgarten, Dohmen (RWTH Aachen / FEV), 2016**, open RWTH copy: laboratory single-cylinder, about **3.3%–3.8%** efficiency gain near minimum BSFC (stoichiometric, Miller + cooled EGR), up to **16%** at full load, about **4.5%** with homogeneous lean. DOI 10.1177/1468087415599867; https://publications.rwth-aachen.de/record/567619
- **Massoud, TU Berlin dissertation, 2024**, open DepositOnce (CC BY 4.0): indicated efficiency about **+0.8 pp** (port, 10 bar), **+1.2 pp** (direct, 400 bar), **+2.0 pp** (best 10% microemulsion, 200 bar). https://doi.org/10.14279/depositonce-21307
- **Welscher et al., KIT / Stuttgart, 2023**: 562 port-WI points on a Euro 6d diesel single-cylinder. Use the abstract’s 62/40/20 soot-neutral shares and g/kWh NOx figures, **not** a “50% NOx” shorthand. DOI 10.1177/14680874211044297; KITopen 1000137777.

Corrections already found in the Germany draft (do not reuse the wrong figures): the GTS is not a 500-car run; “+37 hp vs M4” is wrong; Alpina/Brabus factory water-injection kits were not confirmed; a shared patent list was mis-attributed across firms; “up to 50% NOx” is not what Welscher’s abstract says.
