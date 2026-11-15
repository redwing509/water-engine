# Luxembourg — water in the combustion cycle (checked)

Status: DONE (checked). Hermes drafted (job 20261114-213335-we-survey-57-luxembourg-water-in-combust, key we-survey-57-luxembourg, profile we-research, rc 0, 9:34:42–9:40:52 PM America/Los_Angeles 14 Nov 2026, runtime 6.2 min). The prompt was in French and already included the Simulators section, so no separate simulator follow-up job was run. The checker re-opened the key sources on 14 Nov 2026, about 9:51–9:55 PM America/Los_Angeles. No piracy sites were used. The Hermes draft is kept in the private archive only.

Prompt language: French (Luxembourg is multilingual FR/DE/LB). Report language: English.

Water is not treated as a fuel in this note. Water electrolysis / hydrogen production is out of scope.

## Verification (checker)

**No Luxembourg production or near-production road vehicle** with water injection, water-methanol injection or water-fuel emulsion was found, and **no published Luxembourg measured engine data** (power, BSFC, knock, NOx) for water in the combustion cycle was found. Luxembourg's real contribution is **patents** from the Delphi / BorgWarner / Phinia fuel-injection centre (Bascharage, now Phinia Delphi Luxembourg SARL, Belvaux) and from DMA Tech S.à r.l., plus University of Luxembourg injector-cavitation work that uses water only as a test fluid.

### What was opened and what can be taken

| Claim in the Hermes draft | Checked result |
| --- | --- |
| LU501822B1 "Hydrogen-fueled four-stroke internal combustion engine" | **Confirmed; most relevant item.** DMA Tech S.à r.l. (LU), inventor Jacques Bouvy; filed 8 Apr 2022, granted 9 Oct 2023. Hydrogen DI spark/glow-plug engine with a **separate direct in-cylinder water injector**: main water quantity at **110–90° BTDC** (95–99.5 wt% of the water), a small early water shot at 180–110° BTDC (0.5–5 wt%), an early hydrogen shot at 180–100° BTDC (5–50 wt% of the hydrogen) and main hydrogen from 20° BTDC to 20° ATDC. Claimed effects: lower NOx, less knock, richer lambda than usual for H2 engines. **Patent only; no measured engine data.** Family includes PCT/EP2023/053310, US 18/836,621, CN, JP, CA, ES, PL, MA, RS. https://patents.google.com/patent/LU501822B1/en |
| GB2615733A "Method of operating a water injection system", BorgWarner Luxembourg Automotive Systems SA, 2021 | **Confirmed.** Inventor Gavin Dober; filed 16 Dec 2021; published 23 Aug 2023; granted as GB2615733B 29 Jan 2025. Water-pump standby / pre-pressurization control so a port water-injection system is ready when demand arrives. No measured data. https://patents.google.com/patent/GB2615733A/en |
| US12392278B2, assigned to Phinia Delphi Luxembourg SARL, Belvaux | **Confirmed.** Same family (PCT/EP2022/084669), inventor Gavin Dober (LU), granted 19 Aug 2025. The description targets turbocharged GDi high-performance engines: water injected into the intake port/manifold to replace full-load fuel enrichment, improve knock resistance and allow higher compression ratio / specific power. No test numbers. https://patents.google.com/patent/US12392278B2/en |
| DIRECT2 (University of Luxembourg + Phinia), "2023–2026", water-ethanol tests, "neutron imaging revealed…" | **Real; scope and dates corrected.** Project page: start 1 Dec 2023, 24 months, FNR BRIDGES, PIs Prof. Stephan Leyer and Dr Gavin Dober (Phinia); FNR results list the industry partner as BorgWarner Luxembourg Automotive Systems SA and €191,700 committed. CFD in **ANSYS Fluent** of pressure waves, cavitation, degassing and thermal effects in high-pressure injectors/pumps. The FEDIL écho article (16 Dec 2025, not 2023) says water was a **stand-in fluid** in Venturi/orifice rigs and water–ethanol blends were run in injector models; neutron imaging is **planned**, not done. **This is fuel-injector cavitation research, not water in the combustion cycle.** No numbers. |
| HEWASP (University of Luxembourg) | Real (Nov 2022, 36 months, Bradford Space). **Water boiling in space hot-gas propulsion** — out of scope. |
| LIST hydrogen work (HEPHOTO, CLEANH2, 3D-Oxides) | Water splitting / hydrogen production — **out of scope** (not water in the combustion cycle). Dropped. |
| FNR "low pressure liquid injection atomization" and "high load low NOx in RDE" project pages | **Both URLs return 404**; the RDE project could not be found by search. Dropped. |

### Added by the checker

- **US 2025/0215842 A1** "Injection device" (pending; filed 24 Mar 2023, published 3 Jul 2025). Applicant PHINIA DELPHI LUXEMBOURG SARL, Belvaux; inventor Nicholas More (North London, UK) — Luxembourg applicant, UK inventor. Injector that meters **water into gaseous fuel (hydrogen)** inside the injector and injects the water/H2 mixture into the combustion space, aimed at pre-ignition, detonation and NOx. No measured data. Opened on a third-party USPTO mirror (patents-review.com).

### Usable figures

- LU501822B1 timing windows (patent claims, not measurements): water 110–90° BTDC (95–99.5 wt% of total water), early water 180–110° BTDC (0.5–5 wt%), early hydrogen 180–100° BTDC (5–50 wt% of total hydrogen), main hydrogen 20° BTDC–20° ATDC.
- DIRECT2 funding: FNR €191,700 (BRIDGES 2022-1), 24 months from 1 Dec 2023.
- No Luxembourg measured water-injection engine numbers were found.

## Corrections to Hermes (summary)

1. DIRECT2 is fuel-injector cavitation research with water as a test fluid, not water in the combustion cycle. The FEDIL article is from 16 Dec 2025, not 2023; neutron imaging is planned, not done.
2. LIST hydrogen-production projects and HEWASP (space propulsion water boiling) are out of scope and were removed from findings.
3. Two FNR project URLs return 404; the "High Load Low NOx in RDE" project could not be found. Dropped.
4. The water-injection patents (LU501822B1, GB2615733A, US12392278B2) were listed only by title; the checker added the applicants, inventors, dates and the actual injection timing content.
5. "LuXDEM" is a research centre, not a tool, and its XDEM software is **not open source** (not publicly distributed; licences by arrangement). The draft URL (dpm.gforge.uni.lu) no longer resolves.
6. QuickSim is a Stuttgart (IVK/FKFS) tool; the claim that DIRECT2 used it is unsupported (DIRECT2 names ANSYS Fluent). Dropped as a Luxembourg find.
7. US 2025/0215842 A1 (Phinia Delphi Luxembourg water/hydrogen injector) was missed by Hermes and added.

## Simulators and modeling tools

- **XDEM** (eXtended Discrete Element Method) — LuXDEM Research Centre, University of Luxembourg (Prof. Bernhard Peters). C++ multi-physics framework for granular matter: particle motion, thermal conversion and combustion in packed beds, with coupling to OpenFOAM CFD. **Not publicly distributed** (neither source nor binaries); private copies/licences only to collaboration partners, commercial licences via Wikki GmbH. Official page: https://luxdem.uni.lu/software/index.html (confirmed from a search-index copy; direct fetch returned HTTP 500). Not a vehicle water-injection engine-cycle tool. The LuXDEM group's GDI-injector liquid-sheet breakup study (FNR-funded) used **OpenFOAM** VOF-LES (upstream open-source code, not a Luxembourg tool).
- **ANSYS Fluent** (commercial, ANSYS Inc., USA) is the CFD code named for DIRECT2 injector cavitation work. Not a Luxembourg tool; listed for context only.

**Not added:** QuickSim (German, link to Luxembourg unsupported); OpenFOAM itself (upstream). No Luxembourg-developed water-injection or engine-cycle simulator was found. Candidates only; nothing was installed, and installing anything still needs a separate OK.

## Limits

This is a small-country pass with a short Hermes run (6.2 min). Delphi/Phinia benches in Bascharage/Belvaux may hold unpublished water-injection results; none were public. Google Patents was used for abstracts/descriptions only. "Nothing found" for production vehicles, racing, aviation/marine transfer and emulsions is a search-limited statement. Water is not a fuel in any of these items.

Hermes: main draft produced (job 20261114-213335-we-survey-57-luxembourg-water-in-combust, rc 0). The checker corrected the draft where sources disagreed. No second 57 job was submitted.
