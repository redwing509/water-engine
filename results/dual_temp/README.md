# Dual-temperature combustion runs (normal vs high-performance), 2026-10-24

Standing rule from James (2026-10-24): every combustion simulation runs at **normal** and **high-performance (hot)** engine temperatures. Regimes and references are in `sims/dual_temp/regimes.py` and `docs/DUAL_TEMPERATURE_RULE.md` (PR #5).

| | normal | hot |
|---|---|---|
| coolant | 363.15 K (90 C) | 388.15 K (115 C) |
| chamber wall (Woschni wall T) | 450 K (SPEC section 6) | 520 K |
| intake charge sweep | 320, 360 K | 320, 360, 400 K |
| port wall (Module 11 film) | 363.15 K | 388.15 K, plus a heated port at 420 K |

Status: **executed** on the box (Cantera 3.2.0). The module code is unchanged; the wrappers only patch `wall_T_K` and the intake sweep. **Not verified** by a second engine, **not validated** against experiment.

## Module 03 engine cycle (`03_engine_cycle_{normal,hot}`, comparison in `03_compare/`)
- Normal reproduces the committed baseline to max |delta eta| 7.9e-12 over 864 points, so the wrapper is neutral. Hot passes the module's validation (energy closure 6.4e-4 against a tolerance of 0.02; ideal Otto passes).
- Same intake T, hotter walls only: gross indicated efficiency rises by a mean of **+0.22 to +0.30 points** for every fuel. Wall heat falls about 7-12 % and peak burned T rises about 5-6 K. Knock-limited points: no change, except CH3OH at 360 K (4 to 5).
- Hot 400 K intake compared with normal 360 K: mean **-0.29 to -0.41 points** (worst case -5.9). More points are knock-limited (CH3OH 4 to 16, C2H5OH 0 to 6), and peak T is up about 33-41 K. A hotter charge does not pay.
- Best points (gross eta):

| fuel | case | normal | hot |
|---|---|---|---|
| CH3OH | best overall | 45.58 % (CR 24, w 0.3, 320 K) | 45.97 % (same point) |
| CH3OH | best water-majority | 44.61 % (w 0.5, 360 K) | 45.21 % (w 0.5, 400 K) |
| CH3OH | best dry | 42.59 % (CR 20) | 42.30 % (CR 17; knock retard) |
| C2H5OH | best overall | 45.44 % (CR 24, w 0.4, 320 K) | 45.86 % |
| C2H5OH | best water-majority | 44.89 % | 45.35 % |
| C2H5OH | best dry | 44.54 % (CA50 14) | 44.50 % (CA50 16) |

- NO: `relative_NO` is normalised within each regime. Use `NO_mol_per_J_fuel` in `03_compare/normal_vs_hot.csv` to compare across regimes.

Conclusion (executed): hotter coolant and walls give about +0.4 points at the water-injected optima. Dry points gain nothing because they are knock-limited. A hot intake charge is a net loss.

## Module 04 six-stroke (`04_six_stroke_{normal,hot}`, full EVC x water sweep, adiabatic + Woschni)
- Both regimes pass validation. Water injection is **not beneficial in either regime** (best net extra work about -0.055 J).
- Hotter walls (520 K) cut the Woschni gas-spring loss by about 5 % (EVC 190: -21.1 J to -20.0 J). The verdict does not change.
- `04_six_stroke_normal_designpoints/`: design-point mode is adiabatic with zero water, so wall T has no effect there. It is kept only as a reproducibility check against the committed baseline (max diff 1e-7).

## Module 11 port wall-film (`port_film_wall_T/`)
Steady-state film-evaporation budget. A hotter port removes most wall-film misfire cases at nominal wetted length and film h, but the result is sensitive to those inputs. See its README.

## Not run here (handed to Claude via the ai-relay inbox)
- CFD hot variants for A2/M13.
- Module 13, which has no code yet.
- Module 08/02/10 hot rows.
- A second-engine check of these trends.
