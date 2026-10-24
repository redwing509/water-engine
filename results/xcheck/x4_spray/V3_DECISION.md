# V3: is Module 09's over-prediction a physics gap? (reply-verification-20261024-1430)

Decision: **UNRESOLVED BY CURRENT ENGINES. No Module 09 code change.** Spray evaporation stays **UNVERIFIED**.
Grok Bot, 2026-10-24 (PDT). Data: X4 (06abb30, this branch), Module 09 numerical verification (verify/m09-d2law-gci-20261024 bd1fbd0).

## Evidence
| | A1-H2O | A2-BLEND |
|---|---|---|
| M09 / CFD evaporated, EOI (3 CFD spray models) | 1.30-1.66 | 1.19-1.61 |
| M09 / CFD evaporated, end of run | 1.24-1.56 | 1.11-1.31 |
| CFD spread across its own spray models (end, max/min) | 2.98x | 1.47x |
| M09 reduction if vapour confined to spray cone | 1-3 % | 9-11 % |
| M09 reduction with half initial slip (relative-velocity decay) | 15-18 % | 3-5 % |

## Candidate gaps (job list), checked against the code and data
1. **Local spray-cone saturation.** M09 is 0-D well-mixed gas; CFD has a vapour-rich cone. Bound: -1 to -11 %. Real effect, but on its own it closes at most a fifth of the gap. Not "clearly physical and sufficient".
2. **Relative-velocity decay.** M09 already integrates Schiller-Naumann drag on the slip velocity, but in quiescent gas (no entrainment co-flow). Bound with half slip: -3 to -18 %. Cone + half-slip together still leave M09 high by about 1.15-1.3x for KHRT/RD.
3. **Droplet heating.** M09 already carries a transient droplet temperature (Abramzon-Sirignano, infinite conductivity); the OpenFOAM liquidEvaporation(Boil) models use the same uniform-temperature class. That is not a model-class gap relative to CFD. The ratio falling from EOI to end of run (e.g. A2 KHRT 1.54 -> 1.29) is consistent with a heat-up lag, but it is also consistent with spray-cone vapour build-up, so it cannot be attributed.

The M09-CFD gap (1.1-1.7x) is the same size as the CFD's own model spread (1.5-3x), and the CFD is coarse-mesh and not validated. No single physical gap is identified with enough confidence to change Module 09; tuning it toward one CFD variant would be calibration, not verification.

## Uncertainty band (record as UNVERIFIED)
Module 09 evaporated fraction is treated as an **upper estimate** with band **x0.60 to x1.0** of its value (EOI x0.60-0.84;
end of run x0.64-0.90; the band covers all 12 X4 comparisons at matched SMD). Numerical error (Module 09 V1-V3 PASS) is
negligible against this band. The band is model-vs-model; it is not experimental.
Downstream: Module 03's intake-evaporated fraction and the charge-cooling benefit it implies carry this band; module 03
results that depend on f_evap should be quoted with it.

## Next independent check (proposed, not run)
ECN (Engine Combustion Network) Spray A and Spray G experimental data: liquid length, vapour penetration and mixture
fraction under evaporating conditions. Run the same sprayFoam setup and Module 09 on the ECN conditions and fuels. That
validates the model class against experiment and narrows the CFD spread. A water/alcohol-specific check would need
published single-droplet or spray evaporation data for methanol-water blends (to be found by the nightly prior-art scan).
Also pending: LE-RD fine-mesh runs on mail (ai-job) to remove the coarse-mesh part of the CFD uncertainty.
