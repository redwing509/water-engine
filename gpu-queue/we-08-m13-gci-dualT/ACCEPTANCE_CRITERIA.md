# we-08 M13 GCI x dual-temperature — acceptance criteria (pre-registered 2026-10-24, before any run)

Case: M13 intake-port spray + wall film (reactingParcelFoam, OpenFOAM v2512), generator `cfd/port13` at the
commit given as `M13_REF` (must be a commit where the coarse case completed rc 0). Chemistry is off (no
combustion), but the port-wall temperature drives film evaporation, so James's dual-temperature rule is
applied to the port wall and intake charge:
- normal: port wall 363 K, intake 360 K;  hot: port wall 388 K, intake 400 K;  heated port: 420 K / 400 K
  (sims/dual_temp/regimes.py on wme1-hiT; MAHLE/VW SSP 222, SAE 960271, SAE 2010-01-0802, Heywood ch. 12).
Mesh levels: background dx 2.5 / 1.768 / 1.25 mm (r = sqrt 2), same snappy refinement levels.
Quantities at IVC (end of injection event): film %, evaporated %, airborne-drop % of injected liquid.

PASS (per regime) requires: all 3 levels complete rc 0; monotone convergence; 0.5 <= p <= 4;
GCI_fine <= 10 % for evaporated % and airborne %, and <= 20 % (or <= 1 percentage point absolute) for film %.
Regime comparison is reported side by side with an explicit "hotter port: better / worse / trade-off" line, and
counts only where the GCI band is smaller than the regime difference.
No parameter changes after seeing results. Executed != verified (second engine) != validated (experiment).
