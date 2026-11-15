# Lithuania — water in the combustion cycle (checked)

Status: DONE (checked). Hermes drafted (job 20261114-215721-we-survey-58-lithuania-water-in-combusti, key we-survey-58-lithuania, profile we-research, rc 0, 9:57:23–10:05:23 PM America/Los_Angeles 14 Nov 2026, runtime about 8 min). The prompt was in Lithuanian and already included the Simulators section, so no separate simulator follow-up job was run. The checker re-opened the sources on 14 Nov 2026, about 11:17–11:25 PM America/Los_Angeles, using university repositories and publisher open-access pages only. No piracy sites were used. The Hermes draft is kept in the private archive only.

Prompt language: Lithuanian. Report language: English.

Water is not treated as a fuel in this note.

## Verification (checker)

**No Lithuanian production or near-production road vehicle**, OEM or aftermarket water-injection product, or Lithuanian water-injection patent was found. Lithuania's contribution is **university test-bench and chassis-dyno work** (KTU, VILNIUS TECH with the gas-conversion firm SG dujos Auto, and the Agriculture Academy now part of VMU), plus older Klaipėda marine-diesel papers. Unlike the Hermes draft, the open copies contain **measured data**.

### What was opened and what can be taken

| Claim in the Hermes draft | Checked result |
| --- | --- |
| Steponavičius 2015, KTU master thesis, "no measured data" | **Real; open full text has measured data.** Supervisor Rolandas Makaras. VW Golf with an indirect-injection diesel; water sprayed into the air intake upstream of the turbocharger at 300 and 600 mL per 100 km. **NOx −16…25% / −25…30%**, smoke opacity −28.5% / −52% at 3000 rpm, CO2 −4…14%. Measured route fuel use: **urban 7.86 → 6.80 / 6.77 L/100 km (−13.5% / −13.8%)**, extra-urban 5.16 → 4.69 / 4.70 L/100 km (about −9%); max power and acceleration essentially unchanged. One car, student test. https://epubl.ktu.edu/object/elaba:8661258/index.html |
| 2021 VGTU master thesis, "unknown author", water + hydrogen "improved energy performance" | **Real; author is Aidas Raudonius** (supervisor Saugirdas Pukalskas, defended 1 Jun 2021). Chassis dyno, VW Caddy EcoFuel 2.0 L CNG (CR 13.5:1, 80 kW), modified AEM water kit, natural aspiration and external boost, 3000/4000 rpm, CNG + 0–20 vol% H2. With water 0→139.3 g/min: **BSFC up to +13% (boosted up to +5%), power up to −2% (boosted up to −7%)**, **CO −12…20%, NOx up to −30% at maximum water** (NOx rose at the medium rate at 3000 rpm), HC +3…6%. The energy gains come from **hydrogen**, not water. Open PDF: https://talpykla.elaba.lt/elaba-fedora/objects/elaba:95814034/datastreams/MAIN/content |
| Kurkauskas 2012, "Dissertation", intake water vapour, NOx −26%, BSFC +12% mid / −5% high load, CO +8% | **Numbers confirmed from the record abstract** (13.0 g/min steam at mid-load). It is a graduate ETD record; "Dissertation" (doctoral) is not supported. Full text server returned HTTP 500. |
| "No marine, no emulsion research" | **Wrong.** Klaipėda marine-diesel papers exist (see below). |

### Added by the checker

- **Pukalskas, Korsakas, Stankevičius, Kriaučiūnas, Mikaliūnas, *Energies* 17(9) 2132 (2024), open access**, https://doi.org/10.3390/en17092132 — VILNIUS TECH + SG dujos Auto. Same VW Caddy EcoFuel 2.0 L on a roller dyno, 35 kW traction load, 3000 rpm, CNG and CNG + 5/10/15 vol% H2, **port water injection 60 and 120 mL/min** (reconstructed AEM 30-3000 kit). Abstract: CO about −20%, NOx "4–5 times" lower, **fuel consumption +2.5…7% at 120 mL/min**. Conclusions: CO −25% average, **NOx −67…74%**; modelled after-burn in-cylinder temperature −99 K / −116 K; about 30 mL/min water would bring a 20% H2 blend back to pure-CNG NOx. (Abstract and conclusions state the NOx cut differently; both quoted.)
- **Pupinis, Nakčiūnas, Kurkauskas, Ambrulevičius, *Žemės ūkio inžinerija* 44(4), 59–70 (2012)**, https://hdl.handle.net/20.500.12259/85593 — diesel, 13.0 g/min steam into the intake at medium load: **NOx −14…26%**; CO, CO2, NO2 and **fuel consumption independent of steam amount** (differs from the thesis abstract's BSFC figures; not merged).
- **Stankevičius 2019, VGTU master thesis** (abstract only): CNG + H2 SI engine with water injection; NOx strongly reduced, effective indicators almost unchanged; model vs test within 7%. https://cris.vilniustech.lt/cris/entities/etd/3249eb32-c95b-4547-84b5-ba50970a115e
- Marine context (records/abstracts only, no numbers taken): **Senčila, Bernatonis, Erciutė 1994**, water–fuel emulsion in ship diesels (*Klaipėdos universiteto mokslo darbai, Serija D*, 108–112); **Senčila 2003**, water injection as a NOx method for ship diesels (*Jūra ir aplinka* 1(8), 93–101), https://hdl.handle.net/20.500.14911/213956

### Usable figures

- Diesel car, intake WI upstream of turbo (KTU 2015, one VW Golf IDI): NOx −25…30% at 600 mL/100 km; route fuel −13.8% urban, about −9% extra-urban (single-vehicle test, treat as indicative only).
- CNG/HCNG SI engine, port WI (VILNIUS TECH 2021/2024): NOx −30% (thesis) to −67…74% (2024 paper conclusions); fuel/BSFC **worse** by +2.5…7% (2024) or up to +13% (2021); power −2% (NA) to −7% (boosted).
- Diesel intake steam (2012): NOx −14…26% at 13.0 g/min; BSFC effect disputed between thesis and article.

## Corrections to Hermes (summary)

1. All three draft sources are real, but the draft said none had measured data; the open KTU and VILNIUS TECH theses do. Numbers were added from the open copies.
2. The 2021 thesis author was given as "unknown"; it is Aidas Raudonius (supervisor S. Pukalskas).
3. The draft implied water injection improved energy performance in the 2021 thesis; the thesis shows water **worsened** BSFC and power, and hydrogen gave the gains.
4. Kurkauskas 2012 was labelled a "Dissertation"; the record is a graduate ETD, doctoral status not supported.
5. "No marine / no emulsion research" was wrong: Klaipėda ship-diesel emulsion (1994) and water-injection (2003) papers exist.
6. Hermes missed the open-access *Energies* 2024 paper (VILNIUS TECH + SG dujos Auto), the 2012 *Žemės ūkio inžinerija* article and the 2019 VGTU thesis; the checker added them.
7. Simulators: Hermes said "nothing found"; AVL BOOST is used in the Lithuanian WI literature and was added (see below).

## Simulators and modeling tools

- **AVL BOOST** — AVL List GmbH (Graz, Austria). 1D/0D engine-cycle thermodynamics simulation; now migrated into **AVL CRUISE M**. **Commercial / proprietary** (license terms not published). Official page: https://www.avl.com/en/simulation-solutions/simulation-software/avl-cruise-m (the old AVL BOOST product URL returns 404; migration stated on AVL's webinar page). Lithuanian citation: Pukalskas et al., *Energies* 2024, 17, 2132 (in-cylinder temperature/pressure with 60/120 mL/min water; access via an AVL cooperation agreement with VILNIUS TECH). Not a Lithuanian-developed tool.

**Not added:** SolidWorks Flow Simulation (generic commercial CAD CFD, used in the KTU 2015 thesis for intake flow only); GT-SUITE (only in a literature-review mention of foreign work); DAS-01 (SG dujos Auto in-house data logging, not a simulator). No Lithuanian-developed water-injection or engine-cycle simulator was found. Candidates only; nothing was installed, and installing anything still needs a separate OK.

## Limits

Student theses and one journal paper on a single test car; not production data. The Kurkauskas 2012 full text could not be opened (server error). "Nothing found" for production vehicles, patents, racing and aviation is a search-limited statement. Water is not a fuel in any of these items.

Hermes: main draft produced (job 20261114-215721-we-survey-58-lithuania-water-in-combusti, rc 0). The checker corrected the draft where sources disagreed. No second 58 job was submitted.
