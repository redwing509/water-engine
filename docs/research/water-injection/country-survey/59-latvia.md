# Latvia — water in the combustion cycle (checked)

Status: DONE (checked). Hermes drafted (job 20261114-232451-we-survey-59-latvia-water-in-combustion, key we-survey-59-latvia, profile we-research, rc 0, 11:24:52–11:25:42 PM America/Los_Angeles 14 Nov 2026, runtime about 50 seconds). The prompt was in Latvian and already included the Simulators section, so no separate simulator follow-up job was run. The checker re-opened and searched sources on 15 Nov 2026, about 2:25–2:45 AM America/Los_Angeles, using university repositories, conference proceedings, the patent record and the company's own pages only. No piracy sites were used. The Hermes draft is kept in the private archive only.

Prompt language: Latvian. Report language: English.

Water is not treated as a fuel in this note. Where ethanol or LPG/CNG is added with the water, the gains are not credited to the water.

## Verification (checker)

**The Hermes draft said nothing was found for Latvia, including no theses, no patents, no emulsion work and no simulators. That is wrong.** No Latvian production or near-production road vehicle with factory water injection was found, but Latvia has a real, continuous line of measured work at the **Latvia University of Life Sciences and Technologies (LBTU, formerly LLU), Alternative Fuels Research Laboratory, Jelgava**: water-bioethanol intake injection on rapeseed-oil diesel engines (2013–2014, with a Latvian patent), and intake steam injection on a tractor-class diesel (2023 model, 2024 bench test). A Latvian company, **ABLabs SIA (Jūrmala)**, holds granted patents and sells a retrofit that feeds water vapour together with LPG/CNG into common-rail diesel engines; its performance figures are company claims only.

### What the draft said and what the check found

| Claim in the Hermes draft | Checked result |
| --- | --- |
| "No theses, papers or patents from RTU, LBTU … on water in engines" | **Wrong.** LBTU/LLU has a doctoral thesis (Birkavs 2014), journal paper (Birkavs, Dukulis, Birzietis 2013), two *Engineering for Rural Development* papers (Amatnieks et al. 2023, 2024) and a granted Latvian patent (LV14648 B). Nothing relevant was found for RTU in this pass. |
| "No Latvian patents" | **Wrong.** LV14648 B (LV14648 A), Latvijas Lauksaimniecības universitāte, inventors Aivars Birkavs and Ilmārs Dukulis, filed 17 Jan 2013: water-ethanol solution injected into the diesel intake to cut NOx, usable at sub-zero temperatures. https://patents.google.com/patent/LV14648B/en |
| "No water-diesel emulsion / water-methanol / steam work" | **Wrong.** Water-ethanol intake injection (2013–2014) and intake steam injection (2023–2024) both have measured or modelled numbers. No Latvian water-in-diesel emulsion paper was found. |
| "ABLabs: marketing only, excluded" | **Partly right.** ABLabs SIA is real (Jūrmala), with granted patent US 11,808,236 B2 (inventor Alberto Bonomi, assignee ABLabs SIA, priority 14 Oct 2019) and EP 4045787 B1 for an ultrasonic water-vapour + gas system for common-rail diesels. The diesel-replacement figures are company or grant-press claims with no independent test report found, so no performance numbers are taken. It is a dual-fuel (LPG/CNG) product with water vapour, not a water-injection test result. |
| "No simulators" | **Wrong.** The LBTU group built its engine/NOx models in **ExtendSim** (2014 thesis; 2023 steam-injection model). Added as a candidate. |

### Sources opened and usable figures

- **Birkavs, Dukulis, Birzietis (2013)**, "Rapšu eļļas degvielas patēriņa un izmešu emisijas pētījumi, iesmidzinot ūdens–bioetanola maisījumu motora ieplūdes sistēmā" (The rapeseed oil fuel consumption and exhaust emissions research injecting a water–bioethanol blend in the engine intake system), *Proceedings of the Latvia University of Agriculture* 29(1), 33–40, https://doi.org/10.2478/plua-2013-0004 ; lab open copy https://www.iitf.lbtu.lv/adzl/publikacijas/2013-03_Birkavs&Co.pdf — **Opel 16 DA 1.6 L four-cylinder diesel on rapeseed oil**, bench test, 50% water–bioethanol blend (WE50) into the intake. Abstract: **NOx −32%**, fuel consumption **−16…21%**. Body: at 1500 rpm the best WE50 share was 0.35% of intake air mass (fuel −0.11 L/h, −9%); at 2500 rpm the best share was 0.63% (**NOx −32%**, CO2 −3%, fuel −0.33 L/h, −16%); NOx fell up to 58% at the highest shares, but CO and particles rose 4–17 times, so the 1.86% share was stopped. The authors explain the fuel saving by the 50% bioethanol acting as fuel, so it is **not** a water effect.
- **Birkavs (2014)**, doctoral thesis (Dr.sc.ing.), "Rapša eļļas degvielas izmešu sastāva normalizācija dīzeļmotoros" (Rapeseed oil fuel emission normalization in diesel engines), LLU, supervisor Gints Birzietis, https://doi.org/10.22616/lludissert/2014.001 ; open PDF https://lbtufb.lbtu.lv/disertacijas/mechanical-engineering/Aivars_Birkavs_promoc_darbs_2014_LLU_TF.pdf — Main conclusions: **plain water injection into the cylinder intake caused unstable engine operation and cannot be used in winter**; ExtendSim model predicted NOx −24% with water and −52% with WE50 on a Ford YTR diesel (power +3.5% with WE50); measured on the Ford YTR bench with WE50: **NOx −63%**, HC to near zero, **CO +51%, particles about 6×**; **Land Rover Freelander on a chassis dyno: NOx −35%**, CO2 within 2%; IM-240 and Jelgava city-drive simulation: rapeseed-oil use −8…9%; road tests: power and torque +7…10% (with ethanol in the blend). Method patented as LV14648 B.
- **Amatnieks, Šmigins, Birkavs (2023)**, "Thermodynamic and NOx emission analysis of diesel engine with intake manifold steam injection", *Engineering for Rural Development* 22, 145–151, https://doi.org/10.22616/ERDev.2023.22.TF028 (open PDF) — **model only** (ExtendSim), Kohler KDI 1903M at 2600 rpm, 10–50 mg steam per cycle into the intake: at 50 mg, combustion temperature **−36 K**, **NOx −62 ppm**, power **+4.3%** (modelled).
- **Amatnieks, Birkavs (2024)**, "Effect of steam injection on performance and emissions of agricultural diesel engine", *Engineering for Rural Development* 23, https://doi.org/10.22616/ERDev.2024.23.TF026 (open PDF) — **bench test**: Kohler KDI 1903M three-cylinder diesel (CR 17, 31 kW at 2600 rpm) on a SIERRA CP Engineering test bench, AVL SESAM FTIR, home-made glow-plug steam generator at a constant **15 g/min** into the intake. **NOx −7.5% at idle, −5.7% at 2000 rpm no load, −4.1% (10 kW, 1500 rpm), −4.8% (20 kW, 2000 rpm)**; CO +3.0…5.6%; CO2 change small (+1.1% / +5.1% under load per conclusions); power and torque changes negligible. Authors say steam flow should be increased in further work.
- Context only (no water-injection data): **Amatnieks, Birkavs, Šmigins (2023)**, hydroxy (HHO) gas review, *Research for Rural Development* 29, https://doi.org/10.22616/RRD.29.2023.038 — literature review, no Latvian measurements; HHO is electrolysis gas, not water in the cycle.
- **ABLabs SIA / ArtuPower (Jūrmala)** — US 11808236 B2 (https://patents.google.com/patent/US11808236B2/en ; granted 7 Nov 2023), EP 4045787 B1, Eurasian patent 044741 (company patents page https://www.artupower.eu/technology/patents-2/). Retrofit feeding LPG/CNG plus water vapour (from an ultrasonic transducer) into common-rail diesels up to 18 L; Norway Grants/LIAA project NP-2022/6 (EUR 92,680 support). Company/press claims of 54–80% diesel replacement and up to 80% emission cuts are **not verified** and not taken.

### Usable figures (summary)

- Diesel intake steam, 15 g/min, small tractor-class diesel (LBTU 2024, bench): **NOx −4…7.5%**, CO +3…5.6%, power unchanged. Model (2023): −36 K, power +4.3% at 50 mg/cycle.
- Water–bioethanol (50/50) intake injection on rapeseed-oil diesels (LLU 2013–2014): **NOx −32…63%** (bench), **−35%** (Land Rover Freelander, chassis dyno); CO and particles rose sharply at higher shares; fuel savings came with the ethanol, not the water. Plain water alone caused unstable running and freezing problems.

## Corrections to Hermes (summary)

1. "Nothing found" was wrong: two journal/conference papers with measurements, one modelling paper, one doctoral thesis and one Latvian patent exist (all LBTU/LLU, open copies).
2. "No Latvian patents" was wrong: LV14648 B (LLU, Birkavs and Dukulis, 2013).
3. "No steam / water-alcohol work" was wrong (2013–2014 WE50; 2023–2024 steam).
4. ABLabs was not "marketing only": it holds granted US/EP/Eurasian patents. Its performance claims are still unverified and are not taken.
5. Simulators: "nothing found" was wrong; ExtendSim was used for the Latvian engine/NOx models.
6. The run took about 50 seconds while the draft claimed "extensive searches" of patent, university and library databases; that claim is not credible.

## Simulators and modeling tools

- **ExtendSim (ExtendSim Suite / Pro)** — general-purpose discrete-event and continuous simulation environment, now sold under ANDRITZ (per the official site). **Commercial** (licence pricing / quote on the official site). Official URL: https://extendsim.com/ . Latvian citation: Birkavs 2014 LLU doctoral thesis (NOx prediction with water and water-ethanol injection, Ford YTR) and Amatnieks, Šmigins, Birkavs 2023 (*ERDev* 22, TF028; intake steam-injection thermodynamic/NOx model of a KDI 1903M). The LBTU engine models themselves are not public. Not Latvian-developed; generic tool, not an engine-specific code.

**Not added:** AVL SESAM FTIR (exhaust analyser, not a simulator); SIERRA CP Engineering test bench (hardware); G-Tech Pro / G-Tech Pass SS (road-test accelerometer software). No Latvian-developed water-injection or engine-cycle simulator was found. Candidates only; nothing was installed, and installing anything still needs a separate OK.

## Limits

University bench, chassis-dyno and model work on small diesels and rapeseed-oil fuel; not production data. Several measured gains come with ethanol in the injected blend. No Riga Technical University or Latvian Maritime Academy water-in-combustion work was found in this pass, and no Latvian water-in-diesel emulsion paper was found; these are search-limited statements. ABLabs figures are company claims.
