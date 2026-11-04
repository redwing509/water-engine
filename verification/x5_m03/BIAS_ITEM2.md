# Item 2: the +0.74 % X5 − module 03 efficiency gap: diagnosis, fix, pre-registered re-run

Grok Bot, 2026-10-24 (verification-queue-20261024 item 2). Probes: `bias/probe.py`, `bias/probe2.py`, `bias/probe3.py`.

## Diagnosis
- The gap is step-invariant (RESULTS_FIX.md: eff +0.725…+0.758 %), so it is a model or property difference, not discretisation.
- The IVC states agree exactly (T, p, n, every species mass). Wiebe and volume agree to the last digit.
- The gap persists with wall heat off (adiabatic eff +0.755 %). So it is in the thermodynamic state inversion, not Woschni.
- At fixed (U, V, x_b) the two `state()` functions agree at x_b = 0 and diverge with x_b. The cause is X5's energy reference:
  1. **Reference evaluated at the wrong temperature.** `h_ref = standard_enthalpies_RT · R · T_REF` was read after `P._set(WATER_T)`, i.e. h°(WATER_T)·T_REF/WATER_T instead of h°(T_REF). This scales every formation enthalpy by T_REF/WATER_T.
     - Over a full burn it changes the released energy by **9.79 J of 1458 J (0.67 % of Q_avail)**, CH3OH CR16 dry.
  2. **Enthalpy used as the internal-energy reference.** X5 computed U = Σ m (u(T) − h_ref) where the SPEC sensible energy is Σ m (u(T) − u_ref), as module 03 does. `self.u_ref` was aliased to `h_ref`.
     - Burning changes the mole number, so this adds Δn R T_ref = **2.89 J (0.20 %)**.
  - Together: **12.68 J = 0.87 % of Q_avail**, which matches the +0.74 % efficiency and +0.6 % T_EVO gaps. The same 0.86–0.87 % appears for C2H5OH and for the wet point.
- Conclusion: the gap is a **bug in X5**, not in module 03. Module 03 follows the SPEC sensible-energy definition.

## Fix (scripts_run/xcheck.py only)
`h_ref = h(T_REF)` and `u_ref = u(T_REF)` from the mixture object at T_REF. U, U_IVC and u_lat now use `u_ref`. The enthalpy uses (intake balance, h_lat, end gas) keep `h_ref`.
Disclosure: probe.py was run once on the fixed code before this file was written, as a smoke test: eff gap 0.0000 % at CH3OH/best_dry, 0.5°.

## Pre-registered re-run
`gci_study.py`, unchanged, output to `results_bias/`.
- Criteria A1–A5 from ACCEPTANCE_CRITERIA.md, unchanged.
- Additional item-2 criterion, stated now: |X5 − M03| / M03 ≤ **1e-4** (0.01 %) at the production step 0.5°, for eff, IMEP, T_EVO and pmax at all 6 points and in the Otto benchmark.
- Anything above that is reported as an unexplained residual.

## Consequences and open question (for Claude / James; nothing changed here)
- Every X5 number published before this fix (results/xcheck/cycle.md, 2026-10-24 02:00 PDT) is high by ~0.7 % in efficiency. X5–M03 agreement was never a test of the integrator anyway, since X5 is a line-for-line re-implementation of the same scheme.
- SPEC-level question, not a code bug: the model releases Q_avail = 0.98 · LHV (an enthalpy of combustion, liquid-fuel basis) into the *sensible internal energy*, with the fuel carried as vapour.
  - The thermodynamically consistent closed-system release would be ΔU_c = ΔH_c − Δn R T_ref, about 0.2 % less (plus the fuel vaporisation reference).
  - This is a model-definition choice, worth a SPEC note. It does not affect code verification.
