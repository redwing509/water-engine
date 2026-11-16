# Tunisia — water in the combustion cycle (checked)

Status: DONE (checked). Hermes job 20261115-172439-we-survey-63-tunisia-water-in-combustion (key we-survey-63-tunisia, profile we-research, OVH gpt-oss-120b throttled, no fallback) ran 5:24–5:36 PM America/Los_Angeles 15 Nov 2026, rc 0, and produced a short draft built on **two** sources, neither of them Tunisian work. The checker confirmed both sources, corrected what Hermes said about them, and added Tunisian sources from its own search (French, Arabic and English) on 15 Nov 2026, about 8:22–8:35 PM America/Los_Angeles. Only publisher sites, conference proceedings, HAL, OpenAlex/Crossref/Semantic Scholar metadata and a Tunisian news site were used. No piracy sites were used.

Prompt language: French (with an Arabic citation-honesty block). Report language: English.

Water is not treated as a fuel in this note. Hydrogen/“HHO” made from water by electrolysis is excluded (it is not water injection).

## Verification (checker)

### Main finding

**No Tunisian production or near-production road vehicle with water injection, no Tunisian water-injection product and no Tunisian water-injection patent were found.** Tunisian water-in-combustion work found is **modelling only**: an ENIT (Tunis) measurement-and-simulation study of water injection in a marine diesel (Larbi & Bessrour 2010; paywalled, numbers NOT FOUND in an open copy), a University of Gafsa simulation of steam injection in an HCCI engine (2017, open), and University of Gabès (ENIG) thermodynamic studies of steam-injected gas-turbine combined cycles (2014–2017). No Tunisian engine bench test with water was found.

### Sources opened and usable figures

- **Fridhi Hadia, Soua Wadhah, Ammar Hidouri, Ahmed Omri (2017)**, “Investigation of combined effects of compression ratio and steam injection on performance, combustion and emissions characteristics of HCCI engine”, *Case Studies in Thermal Engineering* 10, 262–271, DOI 10.1016/j.csite.2017.07.005 (open access, CC BY-NC-ND 4.0). Affiliation: “Research Unit: Materials, Energy and Renewable energies, Faculty of Sciences of Gafsa, Tunisia”. Abstract read from the publisher abstract as carried by OpenAlex (the ScienceDirect page blocks the checker).
  - Quote (method): “Combined effects of compression ratios and steam injection on performance, combustion and emission characteristics of a HCCI engine are numerically investigated.” “Combustion is performed by using the Internal Combustion Engine (ICE) model.”
  - Quote (result): “Three values of steam injection ratio are tested. Results show that the performance of the HCCI engine is very low if the steam injection exceed 20%.”
  - Simulation only, validated against “published data available in the literature”; no Tunisian engine test.
- **Larbi N., Bessrour J. (2010)**, “Measurement and simulation of pollutant emissions from marine diesel combustion engine and their reduction by water injection”, *Advances in Engineering Software* 41(6), 898–906, DOI 10.1016/j.advengsoft.2010.01.004 (paywalled; OpenAlex: closed, no repository copy). Affiliations from the publisher metadata: Bessrour at “Ecole Nationale d’Ingénieurs de Tunis, BP 37, 1002 Tunis Belvédère, Tunisia”; Larbi at an address in Radès, Tunisia.
  - Only the title, authors, affiliations and venue were confirmed. The engine, the water rates and every result are **NOT FOUND** in an open copy, so no numbers are given. (A search-engine summary quoted a NOx figure for this paper; it could not be traced to an opened source and was not used.)
  - Same authors, open companion paper on ammonia injection (*Advances in Mechanical Engineering* 2009, DOI 10.1155/2009/459813, both authors at ENIT): “An analytical model based on detailed chemical kinetics employed to calculate the pollutant emissions of a marine diesel engine gave satisfactory results, in general, compared to experimentally measured results.” Context only (not water).
- **Kilani N., Khir T., Ben Brahim A. (2014)**, “A Thermal Analysis and Optimization of a Combined Cycle by Several Technologies”, *American Journal of Energy Research* 2(2), 35–41, open: https://pubs.sciepub.com/ajer/2/2/3/index.html . Authors at National School of Engineers of Gabès, University of Gabès.
  - Quote: “a calculation code established according to EES software. The first studied cycle is a simple combined cycle containing gas turbine cycle with a steam injection system … The overall efficiency of this cycle in inlet ambient conditions is about 46%. The second cycle is a combined one with steam injection system for which the steam injected is generated outside the HRSG using heat recovery system at the air compressor outlet. The performance of this cycle in the same initial conditions is higher of about 1%.”
  - The paper uses “Tunisian natural gas” as the fuel (“LHV=40546.25 KJ/Nm 3”). Thermodynamic calculation, not plant data.
  - Same group: Kilani, Khir, Ben Brahim, “Parameters influences on two combined cycle power plants”, IREC 2016, DOI 10.1109/irec.2016.7478860 (abstract): “a difference of 4% of overall efficiency is obtained between the cycles” and “The overall efficiency for the installation equipped with a system of air cooling steam generator can be more than 58% for the year except in the summer season.” Also *Int. J. Hydrogen Energy* 2017, DOI 10.1016/j.ijhydene.2017.01.233 (title/authors only; abstract not open).

### Hermes sources checked

- **Lalić B., Komar I., Kulenović Z., Antonić R. (2009)**, “Water-in-fuel emulsion as a primary method to remove NOx from diesel engine exhaust gas”, TMT 2009 conference, “Hammamet, Tunisia, 16-21 October 2009”, https://tmt.unze.ba/zbornik/TMT2009/115-TMT09-067.pdf . Confirmed: “approximately 20% NOx reduction in exhaust gas”. But the authors are at the “Faculty of Maritime Studies … Split, Croatia”, and the test was **not on a real engine**: “The efficiency of the Water - in - Fuel emulsification system was tested on engine room full mission simulator Kongsberg ERS-L11 MAN B&W-5L90MC–VLCC”. Tunisia is only the conference venue. Not credited to Tunisia.
- **Shah S. R., thesis** “Experimental and thermodynamical study of water injection at the intake of an automotive Diesel engine for in-cylinder emission reduction”, HAL tel-03139981 (HAL API record). École Centrale de Nantes / Laboratoire de mécanique des fluides (France), supervisors Xavier Tauzia and Alain Maiboom, **defended 21 Oct 2011** (Hermes said 2021). No Tunisian link. Hermes's BSFC +8 % and NOx −25…27.5 % quotes are **not** in the HAL record or TEI export it named, and the thesis PDF could not be downloaded (HAL bot check), so those numbers were dropped.

### Hermes errors corrected

- Hermes said the 2009 TMT emulsion work was “conducted on a B&W‑5L90MC marine engine”. The paper says it was tested on a Kongsberg engine-room **training simulator** in Split.
- Hermes dated the Nantes thesis 2021; HAL gives a defence date of 21 Oct 2011.
- Hermes's thesis quotes (BSFC +8 %, NOx −25 % / −27.5 %) could not be found in the source it cited; dropped.
- Hermes said “No Tunisian university or research institute thesis, report, or paper that experimentally or numerically investigates water injection”. That is wrong for numerical work: ENIT 2010 (marine diesel) and Gafsa 2017 (HCCI steam injection) exist. It is right that no Tunisian **bench test** was found.
- Hermes's “ENIT, ENIS, ENIM” suggestion has no source and was not used as a finding.

### Excluded

- **Hydrogen from water (HHO)**: Leaders.com.tn, 20 Jun 2017, a student from Sfax (ISET Djerba final-year project, with the Sfax technical-inspection centre of the ATTT) built a system “يعتمد بالأساس على غاز "الهيدروجين" المستخرج من المياه” (based mainly on hydrogen gas extracted from water), fitted to a car with an “OHC 1.2” four-cylinder engine: https://m.leaders.com.tn/article/1828 . Electrolysis gas, not water injection; the fuel-saving claim is a news claim, not taken.
- **Oxy-fuel GDI water-injection simulation (2021)**: a HAL record lists a co-author under a structure described as being at Université de la Manouba (Tunis), but the published version (*Energies* 14(17) 5287, DOI 10.3390/en14175287) lists Bedfordshire (UK), Tianjin (China), Lincoln (UK) and Lille (France) affiliations only. Not Tunisian work.
- Tunisian biodiesel and HHO-addition engine papers (Sfax, Gabès, Monastir) with no water addition.

## Production or near-production road vehicles

None found for Tunisia.

## Research, prototypes and supplier systems

- ENIT (Tunis) marine diesel water-injection measurement and simulation, 2010 — numbers NOT FOUND (paywalled).
- University of Gafsa HCCI steam-injection simulation, 2017 — performance “very low” above 20 % steam.
- No Tunisian supplier of water-injection or emulsion systems was found.

## Water-fuel emulsions and other cycles

- No Tunisian engine emulsion test was found. The 2009 emulsion paper presented in Hammamet is Croatian simulator work.
- Steam-injected gas-turbine combined cycles: University of Gabès (ENIG) thermodynamic studies, 2014–2017 (about 46 % overall efficiency for the simple steam-injected combined cycle; about +1 % with steam raised outside the HRSG).
- No aviation, water–methanol or production marine water-injection work from Tunisia was found.

## Simulators and modeling tools

Simulators found: none added after check. EES (Engineering Equation Solver, used by the Gabès group) is a commercial general-purpose equation solver, not a water-injection simulator. Kongsberg ERS-L11 (used in the 2009 Croatian paper) is a commercial engine-room training simulator and not Tunisian. The Gafsa 2017 abstract names only an “Internal Combustion Engine (ICE) model”; the software package is NOT FOUND in an opened source. The ENIT chemical-kinetics model has no public release. Hermes's “NOT FOUND” for simulators stands.

## Limits and open questions

- Larbi & Bessrour 2010 is paywalled with no open repository copy; its engine and results were not read.
- The Gafsa 2017 full text (open access) could not be fetched by the checker (publisher bot check); only the abstract was read.
- Tunisian engineering-school final-year projects (PFE) are mostly not online; unpublished bench work may exist.
- The Tunisian patent office (INNORPI) register was not searched directly; web and Google Patents searches found no Tunisian water-injection patent.
