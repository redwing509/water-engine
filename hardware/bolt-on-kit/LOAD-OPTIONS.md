# Load options for the bench test

The engine has to drive a steady, known electrical load. A resistive load is used so that real power (W) equals what the generator delivers.

| Option | Status | BOM ids | Cost (2026-10-29) | Steps | Accuracy tradeoff |
|---|---|---|---|---|---|
| 5 kW Arcol/Ohmite load bank | **PREFERRED** | T3 | $1,320 (in main total; out of stock until 13 Jan 2027) | Fine switched steps, rated resistors, forced air | Most stable; resistance drift is small and the load is known before measuring |
| (a) Space-heater bank, 4 × Lasko 754200 | OPTIONAL | A1 | $159.96 | 0.9 / 1.5 kW per heater, ~0.9–6 kW | PTC ceramic elements lose ~10–15 % power as they warm, and the built-in thermostat can cycle the load off. Set the thermostat to max, fan on, give a 10 min soak, plug **one heater per dedicated 15/20 A circuit** (no strips or shared outlets), and reject any window where kW steps |
| (b) DIY water-barrel element box, 4 × Camco 1500 W in a 55 gal drum, one switch each | OPTIONAL | B1–B6 | $147.18 | 1.5 kW steps, 0–6 kW | The water holds the element temperature nearly constant, so power is steady once the water is warm (better than (a)). The water slowly heats (~26 K/h at 6 kW), so resistance and kW creep slightly; top up or swap the water to stay below ~80 °C. Coarse 1.5 kW steps. Shock/scald risk: GFCI/bonded box, elements always submerged |
| (c) Rent (AET 100 kW, 1 day + cables) or borrow the test partner's bank | OPTIONAL | R1–R3 | $330/day rented; $0 borrowed | 3.75 kW steps (AET) | A calibrated commercial bank is as good as T3, but 3.75 kW steps are coarse for a 5 kW genset: trim with (a) or (b). Delivery extra. Record the partner bank's make, step size and calibration date |

Optional rows are tagged `opt-a` / `opt-b` / `opt-c` in BOM.csv. They have their own totals and are **not** in `TOTAL_ALL`.

## Always measure the real load
Never trust the nameplate watts of any load. The Eastron SDM120M (T2) on the generator output logs kW and kWh for every run. For options (a) and (b), a P3 Kill A Watt (T4) cross-checks each heater/element step one at a time (it is rated 15 A / 1800 W) and must agree with T2 within 3 %. **Never** put T4 in series with the T3 or rented bank feed (up to ~45 A); there, T2 (45 A rated) is the meter, cross-checked against the bank's own panel reading.

## Holding a resistive load steady
1. **Steady-state first.** Switch in the load step, then wait until the T2 kW reading changes by less than 2 % over 5 min (at least 10 min for (a) and (b) from cold) and EGT is within ±10 °C. Only then start the measuring window.
2. **Log kW through the window.** Read T2 at least every 10 s (Modbus) or every 30 s by hand, and log V, A, kW and kWh. Reject the window and repeat it if any heater thermostat cycles, an element trips, or kW moves more than ±3 % from the window mean.
3. **Use delivered kWh, not set-point kW.** For each window, take E = kWh_end − kWh_start from T2 (cross-check with mean kW × hours). Fuel efficiency = E / fuel mass (T1, g), giving g/kWh. When two runs at the same set-point are compared, correct to a common load as g/kWh, and correct fuel mass to the window length. Never compare grams per run directly.
4. **Set points with coarse steps.** (a) and (b) cannot land exactly on 25/50/75/100 % of 5 kW. Use the closest combination (e.g. (b): 1.5 / 3.0 / 4.5 / 6.0 kW only if the genset is rated for it, otherwise 1.5 / 3.0 / 4.5 kW; (a): 0.9+0.9=1.8 kW, 1.5+0.9=2.4 kW, 1.5+1.5+0.9=3.9 kW, 1.5×3=4.5 kW as the top point; never exceed the genset rating, so 5.4 kW (1.5×3+0.9) is NOT allowed on a 5 kW set). Log and compare at the **measured** delivered kW and g/kWh, not the nominal % label, and use the same combination for the dry and wet runs.
5. **Record** the load option, step setting, water/ambient temperature (option b) and both meter readings in the run sheet.
