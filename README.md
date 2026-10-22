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
