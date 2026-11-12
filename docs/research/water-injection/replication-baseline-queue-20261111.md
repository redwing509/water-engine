# Replication and baseline queue (11 Nov 2026)

James (t898u, 6:12 PM PST) asked for a queue of tests worth replicating from the Egypt efficiency study, and for new baselines to work from. Numbers below are from the checked report `egypt-efficiency-improvement-20261111.md` and from the already-published R31+R32 rescore. This is a work queue, not new measured data.

Two tracks stay separate: **Water Engine** (naturally aspirated gasoline) and a **diesel-emulsion side project**. Attia's bursting-droplet mechanism does not carry over to port-injected gasoline, so "beat +20%" is not the Water Engine target.

---

## Baselines to work from

These are the starting points later runs are compared to. They are formalized here so a later result cannot quietly change the yardstick.

### B-WE-01 — Water Engine modelled cost per mile (already computed)

- **What it is:** the current gasoline Water Engine computational baseline, from the complete R31+R32 rescore on `main`.
- **Case:** PRF91, normal climate, 86 × 107.5 mm, 1500 rpm, `humid_evap` and `liquid` tied. Dry compression ratio 8 → wet 12, water mass fraction `w = 0.30` (water-to-fuel ratio 0.43, about 25–30% water by volume if it were an emulsion). Power +10.16%.
- **Baseline figure:** **−9.728% cost per mile** versus its own dry case at equal-or-better power. Model-only. Not a measured engine map.
- **Use:** every later Water Engine model change is compared to this case (same fuel, geometry, rpm, and intake mode) before it is called an improvement.
- **Status:** formalized. Source: `results/R31_R32_RESULTS.md` in [redwing509/water-engine](https://github.com/redwing509/water-engine).

### B-WE-02 — RWTH Aachen / FEV gasoline water injection (HIGH-TRUST)

- **What it is:** the measured spark-ignition direct water-injection reference James designated on 11 Nov 2026. Architecture match for Water Engine.
- **Source:** Hoppe, Thewes, Baumgarten, Dohmen, *International Journal of Engine Research* 17(1):86–96, 2016. DOI [10.1177/1468087415599867](https://doi.org/10.1177/1468087415599867). Open copy: [RWTH Publications 567619](https://publications.rwth-aachen.de/record/567619).
- **Use:** gasoline injection calibration. Do not swap its numbers with diesel emulsion or diesel direct-water-injection figures.
- **Status:** already a calibration reference. See `calibration-references-20261111.md`.

### B-WE-03 — Tornatore 2021 gasoline emulsion (new supporting baseline)

- **What it is:** the only verified gasoline water-in-fuel engine map in the Egypt study. Turbocharged port-injected SI.
- **Source:** Tornatore et al., *Applied Sciences* 11:9453, 2021. DOI [10.3390/app11209453](https://doi.org/10.3390/app11209453). Open MDPI PDF.
- **Targets to replicate computationally, then treat as a check:** indicated specific fuel consumption **−3.7% at 10 vol% water** and **−7.1% at 20 vol% water**, gained only from knock-limited spark advance and leaving enrichment. At the same spark timing the emulsion was worse. NO rose at stoichiometric. The tested batch used 0.2% Span 80, even though the abstract says "without addition of surfactants."
- **Use:** supporting gasoline-emulsion check next to RWTH. This is the right measured yardstick if Water Engine tries an emulsion at all. A fixed-ratio tank blend is a poor fit; an inline variable-ratio mixer used only at high load is the path that matches this paper.
- **Status:** queued as a computational replication (Q-WE-01). Not yet run.

### B-DE-01 — Attia 2014 dry-diesel equal-power baseline (new diesel-emulsion yardstick)

- **What it is:** the dry-diesel starting point for any attempt to reproduce or beat Attia's +20%.
- **Engine (from the official Benha PDF):** 3.1 L turbocharged three-cylinder diesel, compression ratio 15, stock injection timing, test bed SAK-H-670. Speeds and loads: 1500 rpm at 15–30 kW and 2000 rpm at 3–35 kW. Highest tested load is only about 6.7 bar BMEP; rated power was not tested.
- **Dry-diesel figure in the paper:** about **225–235 g/kWh** (read from the same efficiency plot; the paper never defines "effective efficiency" or gives heating values). The fine-emulsion peak of about 0.43, if it means power over diesel energy, is about 197 g/kWh — unusually low for this engine, and a reason to replicate before treating +20% as a target to beat.
- **Wet comparison rules (must all be used together):** 17% water by volume, 0.5% Span 80 / Tween 60, measured D50 **0.53 µm** (0.2 µm membrane) vs **5.5 µm** (0.45 µm membrane). Equal brake power. Fuel use counted on a diesel-only basis **and** on an energy basis with stated lower heating values. Three or more repeats. Full load included. Do not use the 19.75% body label. Do not treat +20% as a map average: several points are only about +10–13%, and at 2000 rpm / 35 kW the coarse emulsion matched the fine one.
- **Use:** diesel-emulsion side project only. Module 13 (the Hermes emulsion / micro-explosion work) should hook this case first.
- **Status:** formalized as a protocol and computational case. Waiting on Module 13. No new engine test is scheduled.

### B-DE-02 — Ayhan and Ece 2019 diesel direct water injection (magnitude check)

- Already a calibration reference: body BSFC about −8.5% at 1600 rpm / 40% water; do not add the +6% peak-power figure (different rpm). Official PDF: https://dergipark.org.tr/en/download/article-file/719644.
- **Status:** already designated. Not a replication of Attia (this is injection, not emulsion).

---

## Test queue

Priority is what is most useful to run, computationally first, once the matching model exists. Nothing here is an authorization to buy engine time.

### Water Engine (gasoline) — primary

| ID | Test | Why | Baseline it works from | Wait on | Status |
|---|---|---|---|---|---|
| Q-WE-01 | Computational replication of Tornatore 2021: 10% and 20% vol water, once at fixed spark and once with knock-limited spark advance | Only verified SI emulsion map; tells us whether the cycle model can see the real mechanism (knock relief, not micro-explosion) | B-WE-03 targets; compare also to B-WE-01 | Module 03 hook or a thin wrapper; emulsion mixer not required | Queued |
| Q-WE-02 | Water Engine inline variable-ratio water at the knock limit only, CR 8 (dry) and CR 12 (wet), water 0 to 0.30 mass fraction | This is the model's actual operating idea. No paper measures NA gasoline at CR 8→12 or at ~25–30 vol% water | B-WE-01 | Existing Module 03 is enough to start; Module 13 not required | Queued |
| Q-WE-03 | Same as Q-WE-02 but as port or direct **water injection** (not a fuel emulsion), checked against RWTH | Injection is the architecture match; emulsion at part load hurts burn rate | B-WE-02, B-WE-01 | Existing Module 03 | Queued |

### Diesel emulsion — side project ("beat +20%")

| ID | Test | Why | Baseline it works from | Wait on | Status |
|---|---|---|---|---|---|
| Q-DE-01 | Equal-power Attia replication, computational first: 17% water, D50 0.53 vs 5.5 µm, CR 15, stock timing, 1500 and 2000 rpm, Attia's load points plus a full-load point, diesel-only and energy-basis fuel use, stated LHVs | Until this exists, no "improvement" can be compared to +20%. The +20% may shrink | B-DE-01 | Module 13 emulsion / micro-explosion code | Queued, first diesel case for Module 13 |
| Q-DE-02 | 17% emulsion at CR 17 and 18, and a modest injection-timing advance, same equal-power rules as Q-DE-01 | Main untested upside in the literature (Vellaiyan +12% at CR 18 vs +3.7% at CR 15 is from a review, not the paywalled primary). NOx will rise | B-DE-01, then Q-DE-01 | Module 13 plus a diesel cycle hook | Queued after Q-DE-01 |
| Q-DE-03 | Droplet-size sweep at fixed 17% water, about 0.5 to 40 µm | Attia found finer better; Kyoto 2025 and Santoso 2024 found larger better. The optimum is not settled | B-DE-01, Q-DE-01 | Module 13 | Queued after Q-DE-01 |
| Q-DE-04 | Surfactant-free inline mixing, same 17% case, with a documented separation time | Practical fleet path (Santoso; Tornatore's micro-channel). Mix must be made on the vehicle (1.5 minutes to a few hours) | B-DE-01 | Module 13, later hardware notes | Queued, lower urgency |

### Not queued

- **Oliveira and Brójo 2024** as a target to beat. It reports a mean +19.14% and a curve that reads about +21% to +28%, but it is low trust (462 cc air-cooled single-cylinder at 2.4–2.8 kW, no droplet data, CO +81%, HC +94%). It stays a caution, not a baseline.
- **Nanoparticle additives** (aluminium oxide, cerium oxide). Abstract-level +8–11%, nanoparticle exhaust. Not recommended.
- **Heavy-duty fleet maps as something to "beat":** PuriNOx on a Caterpillar 3176 was −0.7% energy use (SAE 2002-01-2891, maker-affiliated, abstract only); Texas DOT was about a 17% fuel-efficiency penalty (SAE 2004-01-0087, abstract only). Those are reality checks that large Attia-like gains do not show up on modern heavy-duty engines, not baselines to improve on.

---

## Order of work

1. Keep B-WE-01 as the Water Engine yardstick. Run Q-WE-02 and Q-WE-03 on the existing cycle model when a slot is free — these do not wait on Hermes.
2. After Module 13 exists and passes review, run Q-DE-01 (Attia equal-power) and Q-WE-01 (Tornatore) as the first two uses of that code.
3. Only then Q-DE-02 (compression and timing) and Q-DE-03 (droplet-size sweep).
4. Q-DE-04 is practical-engineering follow-up, not a first model run.

Every reported "gain" has to state whether power was held equal, whether fuel mass includes water, which heating values were used, and whether it is model-only. Water is never a fuel.

## Relation to the Hermes Module 13 job

Module 13 is the emulsion and micro-explosion code now assigned to Hermes (four turns, then full pipeline review, Codex if review fails). When that code is complete, it will be pushed to GitHub with a document on what it can be used for: Q-DE-01 through Q-DE-03 first, Q-WE-01 as a gasoline check, and a clear statement of what it cannot do (it cannot by itself produce an engine efficiency figure, and it is not a claim that +20% has been reproduced or beaten).
