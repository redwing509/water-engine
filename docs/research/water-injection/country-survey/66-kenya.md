# Kenya — water in the combustion cycle (checked)

Status: DONE (checked). Hermes job 20261116-021730-we-survey-66-kenya-water-in-combustion (key we-survey-66-kenya, profile we-research, OVH gpt-oss-120b throttled, no fallback) ran 2:17–2:35 AM America/Los_Angeles 16 Nov 2026, rc 0, and reported PARTIAL. It **did not write its draft file**; its result summary cited **one** source, a University of Nairobi MSc thesis on biodiesel, and claimed the abstract "explicitly mentions water‑emulsion fuel". The checker opened that thesis abstract and found **no mention of water or emulsion fuel** (claim rejected), then ran its own English searches on 16 Nov 2026, about 5:13–5:16 AM America/Los_Angeles. Only publisher open-access PDFs (SCIRP, CC BY 4.0), an institutional thesis record (icipe "The Hive") and a World Bank public document were used. No piracy sites were used.

Prompt language: English. Report language: English.

Water is not treated as a fuel in this note. Hydrogen/"HHO" made from water by electrolysis is excluded (it is not water injection).

## Verification (checker)

### Main finding

**No Kenyan production or near-production vehicle with water injection, no Kenyan water-injection product or patent, and no Kenyan engine bench test with water injection or a water emulsion were found.** The only Kenyan water-in-combustion study found is a **CFD simulation** of non-surfactant water-in-diesel emulsion at the Pan African University Institute for Basic Sciences, Technology and Innovation (PAUSTI, hosted at JKUAT, Nairobi), 2019: 5 % water gave the lowest NOx ("reduce NOx up to 35%"), while power fell and soot rose as water increased. A 2024 JKUAT / Technical University of Mombasa syngas-engine paper only *mentions* water or steam injection as a possible NOx measure; it did not test it. A 2004 KenGen environmental assessment for the Kipevu gas turbines proposes low-NOx burners, not water injection.

### Sources opened and usable figures

- **Confidence C., Ndiritu E. H., Gathitu B. (2019)**, "Effect of Emulsified Diesel Fuel on Performance and Emissions Characteristics", *Energy and Power Engineering* 11, 333–341, DOI 10.4236/epe.2019.119021 (open access, CC BY 4.0). Affiliation: "Department of Mechanical Engineering, Pan African University Institute for Basic Sciences, Technology and Innovation, Nairobi, Kenya". https://www.scirp.org/journal/paperinformation?paperid=95028 (PDF: https://www.scirp.org/pdf/EPE_2019091215282213.pdf)
  - Quote (abstract): "The present work carried out a simulation of non-surfactant emulsified diesel fuel where composition of water in emulsion varied from 0% to 20% … For this simulation, 5% of water in diesel without surfactant was able to reduce NO x up to 35%. It was shown that as the percentage of water increases, the power from that fuel combustion reduces."
  - Quote (method): "The geometrical model of combustion chamber is generated using ANSYS fluent R17.1 and the model is 2D." "This model is 87.5 mm of diameter and 10 mm of length." "The number of nodes is 681 and the number of elements is 594".
  - Quote (conclusions): "At 5% of water in emulsified diesel fuel, NOx was minimum; it reduced up to 35%." "Soot increase as water percentage increase in emulsified diesel fuel." "There is no significant change in carbon dioxide."
  - Simulation only (steady 2D CFD); no engine test.
- **Kariuki B., Njogu P., Kamau J., Kinyua R., Bachani S. (2024)**, "Comparative Study of Exhaust Emissions from Diesel and Syngas Powered 3.5 kW Compression Ignition Engine with and without Load", *Journal of Power and Energy Engineering* 12, 30–46, DOI 10.4236/jpee.2024.128003 (open access, CC BY 4.0). Affiliations: Institute of Energy and Environmental Technology, Jomo Kenyatta University of Agriculture & Technology, Nairobi; Department of Mechanical and Automotive Engineering, Technical University of Mombasa. https://www.scirp.org/pdf/jpee2024128_31771129.pdf
  - Quote: "Other strategies to reduce NOx emission include the use of catalyst reduction, steam injection, or water injection, after the injection of the pilot fuel."
  - Quote: "To reduce EGT and NOx, exhaust gas recirculation can be applied in combination with the injection of water into the engine chambers."
  - Context only: the engine was run on diesel and syngas; water injection was **not** tested.
- **GIBB (Eastern Africa) Ltd. for KenGen (February 2004)**, "Environmental Impact Assessment for the Conversion of Kipevu Open Cycle Gas Turbine to Combined Cycle Operation", Final Report, World Bank document E899 vol. 2. https://documents1.worldbank.org/curated/en/714501468753323174/txt/e8990vol-02.txt
  - Quote: "KenGen owns two gas turbines at its power station in the Kipevu area of Mombasa, Kenya. The gas turbines are operated in a simple, open combustion cycle."
  - Quote: "it has been proposed that low NOx burners be installed for the combined cycle plant."
  - The text has no mention of water injection, steam injection, fogging or evaporative inlet cooling (searched). NOx control proposed was low-NOx burners.

### Hermes source checked

- **Ndaya (Mogire) D. (2013)**, "Biodiesel Production From Candlenut And Calodendrum Capense Seeds: Process Design And Technological Assessment", MSc (Environmental Chemistry) thesis, University of Nairobi. Record: http://erepository.uonbi.ac.ke/handle/11295/55819; open record with full abstract: https://thehive.icipe.org/all-theses/42/
  - Hermes claim: the abstract "explicitly mentions water‑emulsion fuel". **Rejected.** The full abstract (opened) is about biodiesel from candlenut and calodendrum capense; the only "water" in it is "lipase enzyme cultured from Lake Bogoria water". Engine tests were biodiesel blends: "The engine performance tests of B5 and B20 for both candlenut and calodendrum capense were also investigated." Not water in combustion; excluded.
  - Hermes's three "PDF" downloads of the UoN bitstream were the repository's HTML loading page, not the thesis.

### Hermes errors corrected

- Draft file `66-kenya-hermes.md` was reported as written but does not exist (not on the runner either).
- "Abstract explicitly mentions water‑emulsion fuel" → false; the thesis is about biodiesel blends only.
- "No other Kenyan‑authored or Kenya‑based research was found on … water‑fuel emulsions" → missed the PAUSTI 2019 emulsion CFD paper (open access).

### Excluded

- UoN biodiesel thesis (no water in combustion).
- "Influence of Ethanol-Water Blends in Spark Ignition Engine Performance and Emissions Operated with Gasoline" (Int. J. Chem. Sci. 15(4), 2017): a search summary linked a co-author to Kenya, but the opened page lists only Hindustan University and Anna University, Chennai, India. Not Kenyan.
- JKUAT MSc thesis on syngas expansion in a gas turbine (Muinde): repository returned HTTP 500 / timed out; content NOT verified; not used.
- Foreign water-injection and emulsion papers returned by searches (Malaysia, India, Germany, Sudan) with no Kenyan author.

## Production or near-production road vehicles

None found for Kenya.

## Research, prototypes and supplier systems

- No Kenyan water-injection prototype, engine bench test or supplier was found.
- PAUSTI (Nairobi): 2019 CFD simulation of water-in-diesel emulsion (0–20 % water; NOx minimum at 5 %, "up to 35%" lower).

## Water-fuel emulsions and other cycles

- Water-in-diesel emulsion: PAUSTI 2019 simulation only (ANSYS Fluent R17.1, 2D).
- Gas turbines: KenGen Kipevu (Mombasa) simple-cycle gas turbines; 2004 EIA proposes low-NOx burners for the combined-cycle conversion. No Kenyan fogging, evaporative-cooling, water-injection or STIG study was found: NOT FOUND.
- No aviation, water–methanol or marine water-injection work from Kenya was found.

## Simulators and modeling tools

Simulators found: none added after check. ANSYS Fluent R17.1 (used in the PAUSTI 2019 emulsion simulation) is commercial. No Kenyan-origin open simulator was found. Nothing installed.

## Limits and open questions

- The University of Nairobi and JKUAT repositories were partly unreachable (HTML loading page; HTTP 500), so unpublished Kenyan theses or final-year engine projects may exist.
- The Kenyan patent registry (KIPI) was not searched directly; web searches found no Kenyan water-injection patent.
- KenGen gas-turbine plant operating practice (e.g., any inlet cooling) after 2004 was NOT FOUND in open sources.
