# Moldova — water in the combustion cycle (checked)

Status: DONE (checked). Hermes job 20261116-162126-we-survey-73-moldova-water-in-combustion (key we-survey-73-moldova, profile we-research, OVH gpt-oss-120b throttled, no fallback) finished rc 0 on 16 Nov 2026. The checker re-opened every source Hermes cited and corrected the draft.

Prompt language: Romanian (Hermes prompt). Report language: English.

Water is not treated as a fuel in this note. Hydrogen/"HHO" made from water by electrolysis is excluded.

## Verification (checker)

### Main finding

**Moldova has no production or near-production road vehicle with water injection, no Moldovan water-injection product or patent (none found), and no measured engine test of water injection or a water-fuel emulsion carried out in Moldova.** What exists is two Technical University of Moldova (UTM, Chișinău) master's theses on water-fuel emulsion, and one 2026 journal article published in a Moldovan journal. This is a negative result from the checker's searches, not proof that none exists.

**Hermes's headline was wrong on origin.** Hermes presented the 2026 water-in-diesel (WiDE) article as Moldovan research done on UTM facilities. The article's authors are all from India (Kakinada, Guntur, Hyderabad, Mylavaram) and the engine tests used a Kirloskar single-cylinder diesel; it only appears in a Moldovan journal (Problemele Energeticii Regionale, Institutul de Energetica, Chișinău) and is hosted in the UTM repository. It is real, measured data, but Indian work, not Moldovan.

### Sources opened

- **Madusudanprasad M., Abshalomu Y., Dinesh R., Harish B.B., Bala S.S.R.M., "Environmental impact mitigation in diesel engines using emulsified Water-in-Diesel fuel blended with Al₂O₃ nanoparticles", Problemele Energeticii Regionale 1 (69), 2026**, DOI https://doi.org/10.52254/1857-0070.2026.1-69.01; repository record https://repository.utm.md/handle/5014/35076; open PDF https://repository.utm.md/bitstream/handle/5014/35076/JPRE-2026-V69-N1-p1-9.pdf (opened, HTTP 200, 9 pages, full text read).
  - Quote: "Emulsified fuels were prepared as containing 5%, 10%, and 15% water by volume. Furthermore, 100 ppm of Al2O3 nanoparticles were uniformly dispersed in the blends".
  - Quote: "the best behavior was shown by WiDE10, which showed a 7.14% increase in brake thermal efficiency and reductions in HC by 50.00%, CO by 16.67%, NOX by 66.67%, and smoke by 46.88%."
  - Quote: "diesel shows a peak pressure of 62.74 bar at 366°CA, whereas WiDE blends produce smoother combustion with a lower heat release rate due to water-induced micro-explosions."
  - Method detail (full text): Span 80 / Tween 80 surfactants (1 % by volume mixture), ultrasonication, Kirloskar single-cylinder water-cooled direct-injection diesel on an eddy-current dynamometer, no load to full load. It is an emulsified fuel blend, not direct water injection. Authors' affiliations are all in India.
- **Borta S., master's thesis, "Influența utilizării emulsiei de combustibili asupra funcționării motorului cu ardere internă și ameliorarea situației ecologice", UTM, Chișinău, 2025** (supervisor Gorobeț V.), https://repository.utm.md/handle/5014/36446; open file https://repository.utm.md/bitstream/handle/5014/36446/Borta-Sergiu-FIMIT-STAITA-2025.pdf (opened, 8 pages: annotation, introduction, contents, bibliography; the full 74-page thesis is not in the open file).
  - Quote (annotation): "conducting theoretical research on the use of water-fuel emulsion based on the thermal calculation of the ICE".
  - Quote: "emulsia de combustibil injectată în camera de ardere a motorului a înregistrat o majorare a puterii efective (cu circa 17%) ... scăderea neesențială a consumului efectiv specific de combustibil cu 11 %" for the DC 4 102/130 compression-ignition engine. These are **results of a thermal calculation of the real cycle, not measurements**; the stated method is "metoda comparativă" on calculated values. (The annotation's "insignificant decrease ... by 11 %" wording is the thesis's own and is internally odd; treat as unverified.)
- **Cojocari D. (spelled Cojocaru on the title page), master's thesis, "Cercetări cu privire la utilizarea emulsiei de apă-combustibil la funcționarea motoarelor cu ardere interne ale autovehiculelor", UTM, 2023** (supervisor Beșleaga I., Dr., conf. univ.), https://repository.utm.md/handle/5014/22257; open file https://repository.utm.md/bitstream/handle/5014/22257/Cojocari-Doru-FIMIT-STAITA-2023.pdf (opened, 8 pages: contents, introduction, bibliography).
  - Quote: "La mijlocul secolului al XX-lea, motoarele de avioane americane și germane foloseau un sistem de injecție în amestecul de lucru de apă în combinație cu metanol pentru a crește puterea." The introduction only recounts history (aero engines, then race cars); no Moldovan measurement is visible in the open pages.
- **AGEPI patent database search** for UTM (https://db.agepi.md/inventions/Statsearch?name=UNIVERSITATEA+TEHNIC%C4%82+A+MOLDOVEI) via web search: top classes are measuring, biotech, hydraulics, gearing, wind etc.; no water-injection or emulsion-fuel patent appeared. Not an exhaustive patent search.

### Hermes errors corrected

- Hermes said the 2026 article was by "Moldovan researchers" and "carried out in Moldova (UTM facilities)". Wrong: Indian authors and Indian lab; only the journal and repository are Moldovan.
- Hermes called the 2026 article "peer-reviewed". Not stated in anything opened; dropped. It is a journal article.
- Hermes described the 2025 Borta thesis as investigating injection "aiming to assess ecological benefits" without saying the results are calculated, not measured. Added: thermal calculation (about +17 % effective power, -11 % specific fuel consumption, DC 4 102/130 engine).
- Hermes listed "Vitomir Efimow" as a Moldovan CFD consultant. No source for that was opened by the checker or quoted by Hermes; dropped and not used. Simulators: none verified.
- Hermes's Pass 1 marked sources 2 and 3 as "abstract only"; the checker also opened the open PDFs (annotation, introduction, bibliography). Hermes's claim that the three documents "cover the same thematic line" at UTM is true only for the two theses.
- Hermes's "Authors/Years" line "2023 (master's thesis), 2025 (master's thesis), 2026 (journal article)" is correct as to years.

## Production or near-production road vehicles
NOT FOUND for Moldova.

## Research, prototypes and supplier systems
UTM Faculty of Mechanical Engineering, Industrial and Transport (Transport department) master's theses, 2023 and 2025, on water-fuel emulsion (the 2025 one is a thermal calculation). No Moldovan test-bench measurement, prototype or supplier system found.

## Industrial / power-plant use
NOT FOUND.

## Water-fuel emulsions and other cycles
Moldovan: theses only (above). The 2026 WiDE article (India, published in a Moldovan journal) is the only measured emulsion data tied to Moldova, with the WiDE10 results quoted above (about 10 % water by volume, 100 ppm Al₂O₃).

## Marine and aviation
NOT FOUND (the 2023 thesis only mentions WWII-era aero-engine water-methanol injection as history).

## Simulators and modeling tools
Simulators found: none after check. Hermes reported NOT FOUND, and the only name it gave (a consultancy individual) is unverified and dropped. The Borta thesis uses a classical thermal calculation of the engine cycle; no software or download is named in the opened pages. A "Not added" note went into the candidate list, and nothing was installed.
