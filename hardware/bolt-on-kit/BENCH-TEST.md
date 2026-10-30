# Bench-test procedure (bench-spec rev)
The compression ratios come from ENGINE-ORDER-SPEC.md: **PRF91 9.0, E85 12.5, methanol 14, ethanol 14**. They will change when the high-CR results come in.
Equipment: load bank (T3 or the partner lab's own), true-power kWh meter (T2), 0.1 g scale under the fuel tank (T1), the kit logger (SD CSV).
All settings in the firmware are model-seeded, not measured. Nothing below counts as a result until it has been run and logged.

## A. Static (engine off)
- A0 E-stop: before every run, with the engine idling, press the E-stop (E3). The engine must stop within 1 s and the pump and valve must de-energise. Twist to release; the engine must not restart on its own. Do not run without a working E-stop within the operator's reach.
- A1 Power-up: with the controller unpowered, confirm RETARD and FUEL_LIMIT are asserted (NC continuity) and KILL is open. After boot they stay asserted.
- A2 MAP: compare the logged MAP with the local station pressure, then adjust the offset in the `mapKpa` line to within ±1 kPa.
- A3 Flow calibration: run the pump into a beaker on the scale for 60 s at duty 100/50/25/10 %. Set `METER_ML_MIN_FULL` from 100 % and
  check that the response is linear (±10 %). Set `METER_DUTY_MIN` to the lowest repeatable duty. Expect about 23 ml/min at 100 % (0.5 GPH nozzle, 80 psi).
- A4 Spray pattern: aim the nozzle into a clear tube and confirm atomisation at 10 % and 100 % duty. There must be no dribble after shut-off. If there is, check the NC valve.
- A5 Leak: hold 80 psi for 10 min with the valve closed, with no drop on a gauge and nothing wet.
- A6 Knock chain: tap the block near the sensor with a 6 mm rod and confirm the logged `knock` rises. Set `TPIC_GAIN` so idle noise is 0.2-0.3.

## B. Running, dry baseline
- B1 Warm up 10 min. Confirm the state goes OFF→WARMUP→ARMED_DRY, then INJECTING once the load is above the gates.
- B2 Dry, at the factory timing with retard asserted: 25/50/75/100 % rated load, 3 × 10 min each. Log kW·h (T2), fuel g (T1), EGT, knock, T/RH and MAP.

## C. Running, wet
- C1 Enable water at the same load points. The W/F steps for PRF91 are 0.1, 0.2 and 0.3. For E85, methanol and ethanol, step in 0.15 increments up to the `WF_CAP`.
  Run the points in ABAB order (dry/wet alternating) to cancel drift, 3 × 10 min each.
- C2 Watch the `meter_duty` column. If it reads 1.00 at full load, the nozzle is too small, so fit the next size up (SNO-N0100).
- C3 Metric: BSFC = fuel g / kWh; efficiency = 3600 / (BSFC × LHV[kJ/g]). Accept a gain only if it exceeds 2σ of the repeat scatter.

## D. Fail-safe tests (100 % load, each 3 times)
- D1 Pull the tank feed (or let it run dry). The level sensor trips, and RETARD and FUEL_LIMIT must assert within 0.5 s, with no knock rise.
- D2 Unplug the controller's 12 V. The relays drop, so retard and limit are asserted, and the NC valve closes (no spray).
- D3 Disconnect the EGT thermocouple. The firmware must latch FAULT, turn the water off and assert dry-protect.
- D4 Induce knock (advance or fuel). The trim rises, and at max trim the retard asserts. Confirm KILL fires only at knock > 0.95. Then press the board EN (reset) button: KILL must stay asserted after the reboot and clear only after a power cycle.

## E. After the test
Change the oil and take a sample. Borescope the valves and bore for corrosion or wash-down after 20 h. Archive the SD logs with the run sheet.
