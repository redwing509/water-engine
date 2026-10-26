# Track B fit edge: E10 hot humid_evap chain past w 0.30 (EXECUTED, 2 engines; NOT validated)

Claude review Oct 26 2026 item 3. **Hot regime only, by Claude's explicit ask** (the both-regimes rule is waived for this extension; the E10 normal chain is not extended). Knock label: knock engine 2: ranking validated, absolute klCR offset +2-2.5 CR vs M03 (gate FAILED); not used for this chain's stop rule.

## S_L fit (same method: Cantera FreeFlame CRECK TPRF_HT_ALC, phi 1, water vapour, hot IVC state, cubic)

- w 0..0.45, 10 points: RMS 0.019 cm/s (old w 0..0.30 fit RMS 0.013 cm/s).
- w 0.30 consistency: existing point 0.4924 m/s, fresh solve 0.4914 m/s; fit at 0.30 old 0.4924 vs new 0.4918 m/s.
- points (w, S_L m/s): 0.00: 0.5594, 0.05: 0.5511, 0.10: 0.5419, 0.15: 0.5317, 0.20: 0.5196, 0.25: 0.5069, 0.30: 0.4914, 0.35: 0.4752, 0.40: 0.4566, 0.45: 0.4351

## Chain (continuation from step 300, CR 9.0, T_intake 400 K, wall 520 K)

- consistency row w 0.300: eta M03 0.38356367536590746 (old fit 0.38357543539515954), CRN 0.38372109027431356 (old 0.3837314941882532)
- stop: w 0.302 (last accepted); reason: M03 gain 2.33e-05 <= noise threshold 3.3e-05
- d_eta vs DEI dry baseline (pp, M03 / CRN): +1.278 / +1.281  (was at w 0.300: +1.272 / +1.274)
- failed rows: none

## Cost metric vs the fair dry-evap (DEI w 0) baseline

| fuel | regime | mode | point | w | d_eta pp (M03 / CRN) | power (IMEP) % (M03 / CRN) | fuel volume per unit work % (M03 / CRN) | **cost per mile % at $0.10/gal water** (M03 / CRN) | cost per mile % at $0 water (M03 / CRN) | verdict ($0.10) | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E10 | hot | humid_evap | best-eff (last accepted) | 0.302 | +1.278 / +1.281 | +18.883 / +18.890 | -3.331 / -3.337 | -2.647 / -2.652 | -3.331 / -3.337 | COST GAIN |  |
| E10 | hot | humid_evap | cost-optimal w ($0.10, within w 0.30..stop) | 0.303 | +1.280 / +1.283 | +18.890 / +18.896 | -3.337 / -3.342 | -2.649 / -2.654 | -3.337 / -3.342 | COST GAIN |  |
| E10 | hot | humid_evap | cost-optimal w ($0 water, secondary) | 0.303 | +1.280 / +1.283 | +18.890 / +18.896 | -3.337 / -3.342 | -3.337 / -3.342 | -3.337 / -3.342 | COST GAIN |  |
| E10 | hot | humid_evap | previous stop w 0.300 (old fit) | 0.300 | +1.272 / +1.274 | +18.712 / +18.719 | -3.315 / -3.321 | -2.637 / -2.643 | -3.315 / -3.321 | COST GAIN |  |

Cost per kWh % at $0.10 (M03 / CRN), best-eff: -2.647 / -2.652; fuel energy per work % (M03 / CRN): -3.331 / -3.337; mpg % (M03 / CRN): +3.446 / +3.452.
Verdict ($0.10/gal): **COST GAIN**; at $0 water: COST GAIN.

Caveats: ignition correlation has no explicit w term (valid_w_range label widened to 0.45, assumption); S_L at the IVC state, not engine pressure; fit change at w 0.300: steps < 0.300 used the w 0..0.30 fit, steps >= 0.300 the w 0..0.45 fit (the w 0.300 consistency row above gives the size of the change).
