# STANDING RULE: dual-temperature combustion runs (from James, 2026-10-24 11:20 PDT)

Every combustion simulation, in Water Engine (WME-1) and in any other project, must be run in TWO temperature regimes. The point is to find out whether a hotter engine gives better results and efficiency.

1. **Normal**: a warmed-up production engine.
   - Coolant about 90 C (363 K).
   - Combustion-chamber gas-side wall 450 K (WME-1 SPEC section 6, Woschni wall temperature).
   - Intake-port wall about coolant temperature (363 K).
   - Intake charge 320 to 360 K.
2. **High-performance (hot)**: hotter coolant, walls, ports and intake charge.
   - Coolant about 115 C (388 K).
   - Chamber gas-side wall 520 K.
   - Port wall 388 K, plus a heated-port variant at 420 K.
   - Intake charge up to 400 K.
   - Engines that are not WME-1 should use their own equivalent "hot" set, stated and cited.

References for these numbers:
- MAHLE, *Vehicle cooling* (from VW SSP 222): with mapped cooling, coolant runs 85 to 95 C at full load and 95 to 110 C at part load; pressurised systems boil at 115 to 130 C.
- SAE 960271: part-load coolant at 110 C cuts fuel use by 1 to 3 % on FTP-75.
- SAE 2010-01-0802: engine thermal condition affects efficiency, ignition delay and NOx.
- Heywood, *Internal Combustion Engine Fundamentals*, ch. 12: typical gas-side wall temperatures.

The machine-readable regime set is `sims/dual_temp/regimes.py` on water-engine branch `wme1-hiT`.

Required in every combustion job and result:
- State and cite the exact temperatures used for each regime: coolant, chamber wall, port wall, intake charge.
- Report both regimes side by side, wherever the model computes them:
  - ignition / misfire margin (MIE versus spark energy);
  - burn rate (CA50, 10-90 %, S_L / S_eff);
  - peak pressure and peak temperature;
  - indicated thermal efficiency;
  - wall heat loss;
  - knock margin;
  - NOx (or relative NO).
- End with an explicit conclusion: is hotter better, worse, or a trade-off, and on which metrics?
- If a job specifies only one regime, add the other as a variant job; don't drop it.
- This applies to future jobs AND retroactively to existing combustion results that have only one regime. Queue the missing regime as a variant job.
- Keep executed, verified (a second engine agrees within tolerance) and validated (against experiment) separate. The usual git, 2+ engine merge, no-paid-compute and Sentinel rules still apply.
