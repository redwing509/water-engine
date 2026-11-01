# Water Engine — an honest, simulation-backed investigation

> **Status: work in progress.** Simulations are being built and run; results land in `results/` as they finish.

## The short version

**No engine can run on water as its fuel.** Water (H₂O) is what hydrogen becomes *after* it burns — it is chemical "ash" with no energy left to release. Every "water-powered" engine ever demonstrated either:

1. had a **hidden energy source** (a battery, the alternator, a disguised fuel, or a reactive metal such as aluminium or calcium carbide),
2. used **on-board electrolysis (HHO / Brown's gas)**, which always costs more energy than it returns, or
3. was **misrepresented** — several inventors were convicted or found liable in court (see [`docs/research/01-water-engine-claims.md`](docs/research/01-water-engine-claims.md)).

## What this project builds instead

A design for a **Water-Majority Engine (WME-1)**: a spark-ignited engine whose **liquid intake is more than 50 % water by mass**, with a smaller share of fuel (methanol or ethanol) supplying *all* of the chemical energy. Water is not fuel here — it is a **working fluid and knock suppressant** that can:

- cool the charge and suppress knock, allowing a **higher compression ratio** (more efficiency),
- add **steam expansion work** recovered from exhaust heat (six-stroke cycle),
- cut **NOx** formation by lowering peak flame temperature.

The question the simulations answer: **how much water can an engine take, and still run well — and is it better or worse than running dry?**

## Current best screening results (as of 2026-11-01)

> **Screening results: executed, not validated.** These numbers come from 0-D simulation screening (Module 03 engine cycle + the independent M03-CRN Cantera reactor-network cross-check, M03 knock model only). They have **not** been validated against experiment or independently peer-reviewed, and several best points sit on the edge of the tested grid (marked `*`), so the true optimum may lie outside it. Do not treat them as engine performance claims.

Comparisons are against a dry baseline with the fuel evaporated in the intake air (DEI), spark timing optimised, with liquid water injection, and cost at dated retail fuel prices with water at $0.10/gal. "Hot" = high-performance regime (coolant 388 K, intake 400 K); "normal" = coolant 363 K, intake 320 K. `w` = water mass fraction of the liquid intake.

| Track | Fuel | Case | Bore x stroke | Water w | CR (dry -> wet) | Efficiency gain, pp (M03 / CRN) | Power | Cost per mile |
|---|---|---|---|---|---|---|---|---|
| B (best overall) | PRF87 (regular gasoline surrogate) | hot, 1000 rpm | 105 x 131 mm | 0.30* | 5 -> 7 | +4.41 / +4.49 | +14.1 % | **-12.35 %** |
| B | E10 | normal, 2000 rpm | 65 x 81 mm | 0.30* | 9 -> 16 | +4.99 / +5.05 | +10.2 % | **-11.05 %** |
| A | Methanol (CH3OH) | hot, 1000 rpm | 105 x 131 mm | 0.30* | 16 -> 32* (CR cap) | +4.29 / +4.39 | +5.5 % | **-8.29 %** |

Notes and caveats:

- The Track B gain is mostly knock relief: water lets a knock-limited engine run a higher compression ratio. The PRF87 dry baseline at this point is weak (knock-limited at CR 5), which inflates the relative gain.
- `*` marks a grid edge: w = 0.30 is the top of the water grid and CR 32 is the CR cap, so these are not interior optima.
- None of these cases is a "water-majority" engine (w > 0.5); at w >= 0.5 the screening so far shows power and cost losses versus the fair dry baseline.
- Source tables: geometry study `RESULT_BALL.md` (Track B) and `RESULT_AALL.md` (Track A), combined stages through 2026-11-01.

## Repository layout

| Path | What |
|---|---|
| `docs/research/` | Sourced research: prior water-engine claims (India and global) and the legitimate water-in-combustion literature |
| `SPEC.md` | The engineering spec every simulation module implements |
| `sims/` | Simulation modules (Cantera chemistry, 0-D engine cycle, six-stroke steam cycle, carburetor sizing, CAD) |
| `results/` | Outputs: CSV, plots, `summary.json` per module |
| `cad/` | Carburetor CAD (STEP/STL) generated from the sizing model |
| `tests/` | Validation tests against published combustion data |

## Simulators used

- **[Cantera](https://cantera.org)** — chemical equilibrium, laminar flame speed, ignition delay, reactor networks
- **[CoolProp](http://www.coolprop.org)** — water/steam properties for the six-stroke steam stroke
- A **0-D engine cycle model** (Wiebe heat release, Woschni heat transfer, Livengood–Wu knock integral) built on Cantera thermodynamics
- **[CadQuery](https://cadquery.readthedocs.io)** — parametric carburetor CAD
- **[OpenFOAM](https://openfoam.org)** — venturi CFD check (planned)

## License

MIT — see `LICENSE`.
