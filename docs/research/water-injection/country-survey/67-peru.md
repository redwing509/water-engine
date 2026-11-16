# Peru — water in the combustion cycle (checked)

Status: DONE (checked). Hermes job 20261116-051840-we-survey-67-peru-water-in-combustion (key we-survey-67-peru, profile we-research, OVH gpt-oss-120b throttled, no fallback) ran 5:18–5:32 AM America/Los_Angeles 16 Nov 2026, rc 0, and wrote a two-source draft. The checker opened both sources on 16 Nov 2026, about 8:00–8:20 AM America/Los_Angeles, found serious errors in both, and ran its own Spanish searches. Only open sources were used: an institutional thesis repository (Universidad Nacional del Santa, CC BY 4.0 thesis PDF), Google Patents, and Enel Generación Piura's public annual and sustainability reports. No piracy sites were used.

Prompt language: Spanish. Report language: English (Spanish source titles kept).

Water is not treated as a fuel in this note. Claims that water "dissociates" into hydrogen and oxygen to add energy are not accepted. Hydrogen/"HHO" made from water by electrolysis is excluded (it is not water injection).

## Verification (checker)

### Main finding

**No Peruvian production or near-production road vehicle with water injection, no Peruvian water-injection product, and no Peruvian water-injection patent were found. No Peruvian engine bench test with water injection or a water emulsion was found either.** The Peruvian work found is two undergraduate theses about the Planta Éten cold-reserve power plant (Lambayeque), and both are calculation or design studies:
- Universidad Nacional del Santa (UNS, Nuevo Chimbote), 2023: a thermodynamic calculation of water injection (1–5 % of air mass flow) into the combustion chamber of the plant's GE 7FA.05 gas turbine. It predicts effective power rising from 215.64 MW to 239.4 MW (+9.92 %) and heat rate falling from 10259.10 to 9427.97 kJ/kWh (10.14 % better).
- Universidad Nacional Pedro Ruiz Gallo (UNPRG, Lambayeque), 2020: a design of a direct water-injection system for the plant's Wärtsilä W20V34DF diesel genset. The UNS thesis summarises it as giving 44.8 % → 54.8 % genset efficiency. That figure is a secondary report; the UNPRG repository timed out and the full text was NOT opened.

Real-world use was found in one industrial plant. Enel Generación Piura's Talara gas-turbine unit TG4 used demineralised-water injection for NOx control until about 2022. It was then converted to a "Dry Low NOx" EV burner, with inlet fogging added to recover power.

### Sources opened and usable figures

- **Cisneros Zavaleta, Jesus Eduardo (2023)**, *Efecto de la inyección de agua en la cámara de combustión de la turbina de gas en el rendimiento específico para la Central Termoeléctrica Planta Éten*. Bachelor's thesis (Ingeniero en Energía), Universidad Nacional del Santa, Facultad de Ingeniería; advisor Mariños Castillo, Gualberto Antenor; issued 2023-03-10; open access, CC BY 4.0. https://hdl.handle.net/20.500.14278/4285 (record: https://repositorio.uns.edu.pe/handle/20.500.14278/4285). Full text opened.
  - Quote (abstract): "La condición principal de inyección de agua al sistema es utilizar una cantidad de masa dentro de rango del 1% al 5% del flujo masico del aire." "Actualmente la Central Termoeléctrica obtiene un promedio de 215.64 MW de potencia efectiva y un Rendimiento Específico (HR) de 10259.10 kJ/kwh. Con la inyección de agua a la cámara de combustión puede llegar alcanzar una potencia efectiva de 239.4 MW y un Rendimiento Especifico (HR) de 9427.97 kJ/kwh." "un aumento de hasta el 9.92% en su Potencia Efectiva; … una mejora de hasta el 10.14 %".
  - Quote (abstract, method): "el diseño utilizado fue preexperimental de naturaleza descriptiva".
  - Quote (turbine table): "Fabricante General Electric … Modelo 7FA.05 … Combustible Diesel B5 … Potencia nominal 218.593 MW".
  - Quote (economics): "con la implementación de la inyección de agua, se logra un aumento en la potencia logrando mayor ingreso económico de hasta 64 687.56 USD/mes logrando una mejora económica del 11.01%."
  - Quote (recommendation): "Se hace la recomendación a la empresa Cobra-EMCE continuar con la investigación y realizar el estudio tecno-económico".
  - This is a calculation based on plant test data ("los datos se registraron en el ensayo basados en el procedimiento PR-17 del COES-SINAC"). Water was **not** injected into the turbine. NOx is discussed only from the literature; no NOx result was computed.
- **Larrea Santa Cruz, Luis Felipe (2020)**, *Diseño de un sistema de inyección mixta agua-combustible para un motor Diesel y mejorar la eficiencia del grupo electrógeno de la Central Térmica de Reserva Fría Eten*. Thesis, Universidad Nacional Pedro Ruiz Gallo; repository date 2020-01-09. https://repositorio.unprg.edu.pe/handle/20.500.12893/8063 — **not opened** (curl timed out, WebFetch 504). Record title, author, date and abstract seen in a search-index copy only.
  - Quote (abstract, search index): "Este sistema permite inyectar agua desmineralizada dentro de la cámara de combustión justo instantes antes que se produzca la máxima compresión".
  - Secondary figures, quoted from the UNS thesis above (its antecedentes, which cite it as "Larrea, S. & Luis, F. (2019)" and the university as "Pedro Luis Gallo"): "una eficiencia en el grupo electrógeno (Watsila W20V34DF) de 44.8% y con el sistema de inyección de agua (por gota) se obtenga una eficiencia de 54.8%". These numbers have not been confirmed from the UNPRG full text.
- **Enel Generación Piura S.A., Memoria 2021** (Talara, Piura). https://www.enelamericas.com/content/dam/enel-americas/investor/enel-generaci%C3%B3n-piura/piura/inversores/pdf/reportes/reportesanuales/2021/Memoria%202021%20EG%20Piura.pdf
  - Quote: "a fines del año 2019 iniciamos el proyecto de cambio de nuestra cámara de combustión en la Unidad TG4, que utiliza un sistema de inyección de agua para la reducción de emisiones, para ser cambiado por una tecnología “Dry Low NOx” (DLN)." "Actualmente, la Unidad TG4 usa agua desmineralizada para el control de emisiones, consumo que se reducirá a cero una vez que se instale el nuevo combustor." "se instalará en el sistema de admisión de aire a la turbina, un sistema de neblina (Fogging System) que permitirá recuperar potencia activa".
- **Enel Perú, Informe de Sostenibilidad 2022**. https://pluz.pe/content/dam/enel-americas/investor/enel-generaci%C3%B3n-piura/piura/inversores/pdf/reportes/informes-de-sostenibilidad/INFORME%20DE%20SOSTENIBILIDAD%20ENEL%20PERU%202022.pdf
  - Quote: "El reemplazo de la cámara de combustión por el nuevo diseño “EV Burner” ha reducido en 95% la emisión de gases NOx (óxidos de nitrógeno) … sin requerir inyección de agua para la reducción de emisiones. Con este proyecto, se ha logrado un ahorro anual de 400 mil m3 de agua."

### Hermes errors corrected

- Hermes merged the two theses into one and got its details wrong:
  - It credited the UNS gas-turbine thesis to "Larrea, S. & Luis, F. (2019)", "Universidad Nacional San Agustín" and the Mechanical Engineering programme. In fact the author is Cisneros Zavaleta (2023), the university is the **Universidad Nacional del Santa**, and the degree is Ingeniería en Energía.
  - It described a "gas‑turbine‑driven diesel generator (W20V34DF)". The UNS thesis is about the GE 7FA.05 gas turbine. The W20V34DF is the Wärtsilä genset in the separate UNPRG thesis.
  - It said "Experiments performed in the university’s Mechanical Engineering laboratory". The UNS thesis is a calculation ("preexperimental … descriptiva"); no laboratory test was done.
  - It said the full PDF was "not reachable". The UNS PDF is open access and was downloaded.
- Hermes called the patent "Peruvian" and said it was "filed and granted by … INDECOPI". **Rejected.** WO2009003494A1 is application PCT/DO2007/000001 by José Orlando ALIX / ENERGY SAVING DEPOT C POR A (Dominican Republic). AR053656 (Fioramonti) is cited inside it only as Argentine prior art (priority AR2005P105282). Neither document names Peru or INDECOPI. Its "10%-18%" fuel saving is a second-hand claim ("Según informaciones obtenidas se afirma"), and it rests on water "disociada en sus dos componentes oxígeno e hidrógeno", which is not accepted here. Dropped.
- Hermes said "the same diesel engine model (W20V34DF) is also used in heavy-duty trucks and mining equipment". No source given. Dropped.
- Hermes's simulator table (AVL CRUISE M "inferred", OpenFOAM "general knowledge", MATLAB/Simulink at an "INDECOPI-affiliated research centre") had no quoted source. Dropped: the UNS thesis names no engine-cycle software.

### Excluded

- WO2009003494A1 / AR053656 (Dominican Republic / Argentina; not Peruvian; claims rest on water dissociation).
- UNS thesis by Gonzales Vergaray (2024), *Operación de la Central de Reserva Fría de ETEN y su Impacto en la Seguridad Energética del SEIN* (hdl 20.500.14278/4760): it describes plant operation only, not water in combustion. It does list "01 tanque de almacenamiento de agua desmineralizada (500 m3)" (context only).
- Ortega Cárcamo, "Evaluación del efecto de inyección de agua en el desempeño de un motor ciclo diésel en operación dual con GLP" (doi 10.71700/dspace-memorias/209): its Peruvian origin was not verified, so it was not used.
- UNSAAC Cusco 2013 HHO gasoline-engine thesis: excluded as electrolysis/HHO.
- Foreign water-injection and emulsion theses (Ecuador ESPE/ESPOL, Colombia UTP, Spain) returned by the searches.

## Production or near-production road vehicles

None found for Peru.

## Research, prototypes and supplier systems

- UNS (Nuevo Chimbote), 2023: calculated water injection into the GE 7FA.05 gas turbine at Planta Éten (1–5 % of air mass flow; +9.92 % power, HR 10.14 % better, +11.01 % revenue).
- UNPRG (Lambayeque), 2020: design study of direct demineralised-water injection for the Wärtsilä W20V34DF genset at Reserva Fría Eten (efficiency 44.8 % → 54.8 %, from a secondary source only).
- No Peruvian prototype, bench test or supplier was found.

## Industrial / power-plant use

- Enel Generación Piura, Talara, unit TG4: water injection for NOx control, replaced around 2022 by a Dry Low NOx EV burner (NOx −95 %, 400 000 m³/year of water saved) plus inlet fogging to recover power.

## Water-fuel emulsions and other cycles

NOT FOUND for Peru: no water-in-diesel or water-in-fuel-oil emulsion engine work, and no water-methanol, steam-injection or six-stroke work.

## Mining, marine and aviation

NOT FOUND: no Peruvian mining-diesel, marine or aviation water-injection work.

## Simulators and modeling tools

Simulators found: none after check. The UNS 2023 thesis uses hand thermodynamic calculations plus a "simulador termodinámico Steam Table" for water properties; no named engine or turbine simulator was used. Hermes's three tools (AVL CRUISE M, OpenFOAM, MATLAB/Simulink) were not tied to any Peruvian source and were dropped. Nothing was installed.
