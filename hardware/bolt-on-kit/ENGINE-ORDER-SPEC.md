# Engine order spec sheet: factory high-CR generator engine for water injection (DRAFT, Grok Bot 2026-10-29)

Status: DRAFT for James. CR values are MODEL output (M03 + M03-CRN, with the CRECK Livengood-Wu screen and the full CRECK end-gas
check as second knock model), NOT measured. Source: `sims/pr10_fair_highcr/RESULT.md` (2026-10-29 21:10 PDT). Do not place an order on
these numbers alone; build one engine, bench test it (SPEC.md section 7), then order.

## 1. Base engine
- Single-cylinder, air-cooled, OHV, 4-stroke, 196-460 cc class (GX200 / 420cc-clone family), for 1-10 kW gensets; carb or EFI.
- Fixed-speed 3000/3600 rpm (50/60 Hz) or inverter 2000-4200 rpm.

## 2. Compression ratio (geometric)
Rule: factory CR = model knock-limited CR (klCR, best wet case, fair dry-DEI baseline at its own klCR) minus 1 margin, lower of hot and normal duty.
| fuel | model factory CR (klCR - 1) | recommended order CR | basis (RESULT.md) | dry-safe CR (no water, dry klCR - 1) |
|---|---|---|---|---|
| PRF91 / pump 91 | 8.5 (9.0 if liquid injection) | 8.5 +/- 0.2 | hot w0.3 humid klCR 9.5 (liquid 10.0), normal w0.3 klCR 14; d_eta +2.75 pp hot, cost/mile -6.6 % | 6.5 (hot dry klCR 7.5) |
| E85 | 18 | 18 +/- 0.2 | hot w0.3 klCR 19 (normal 22, scan edge); d_eta +4.44 pp, cost/mile -8.8 % | 11 (hot dry klCR 12) |
| Methanol (M100) | >= 31 (no knock found up to CR 32, scan edge) | James to decide; model does not limit it | hot w0.15 humid +2.03 pp, cost/mile -3.9 %; dry klCR >= 28 (scan edge) | >= 27 |
| Ethanol (E100) | >= 31 at w0.3 (scan edge) | James to decide; model does not limit it | hot w0.3 humid +3.72 pp, cost/mile -6.2 %; w0.15 klCR only 22 | 15 (hot dry klCR 16) |
Notes:
- The alcohol gains hold only under the full-evaporation assumption (injected water fully evaporates); humid and liquid water give identical
  results wherever both were run (RESULT.md flags 1-2). Only PRF91 hot duty differs (liquid about 0.5 pp better, +0.5 CR).
- For methanol and ethanol the model's knock limit sits at the top of the scan, so the order CR must be capped by things the model does not
  capture: hot-spot preignition in an air-cooled head, peak cylinder pressure (section 3), and the water-out event (section 6). Ethanol at
  CR > 16 is past its dry knock limit, so it must never run dry at full load.
- Specify CR by fuel, +/- 0.2 tolerance, measured by cc'ing the chamber.

## 3. Mechanical changes
- Piston: forged or hypereutectic, flat-top or small dome to reach CR; quench/squish band 0.8-1.0 mm; hard-anodised crown or thermal-barrier
  coat; top ring moved down >= 5 mm with a steel (not cast) top ring; ring end gaps per maker for high CR.
- Head: reduced chamber volume (machined deck or new casting); stainless intake + exhaust valves (21-4N exhaust), stellite or nitrided seats;
  M14 spark plug one heat range colder; no sharp edges in chamber (deburr, 0.5 mm radius) to limit preignition hot spots.
- Con-rod / crank / bearings: rated for ~1.4x peak cylinder pressure of stock (model p_max rises with CR); confirm with maker.
- Head gasket: MLS steel.
- Starting: decompression release (auto-decomp on cam) - mandatory, recoil starts at CR > 10 are otherwise hard and kick back.

## 4. Knock sensor and ignition
- Boss on the cylinder (M8 or M10, flat machined spot-face) for a broadband piezo knock sensor (Bosch 0261231xxx class).
- Digital/programmable ignition (CDI or EFI ECU) with: crank trigger, map-based timing, and two hardware inputs: KNOCK_RETARD (opto, 12 V) and
  LIMP/FUEL_LIMIT (opto, 12 V), and a kill input. These are driven by the water controller (firmware `PIN_RETARD_OUT`, `PIN_FUEL_LIMIT`, `PIN_KILL_REQ`).

### Ignition timing map (deg BTDC), PROVISIONAL - set on dyno with knock sensor; values are starting points, not model output
| load (MAP kPa) | 2400 rpm | 3000 | 3600 | 4200 |
|---|---|---|---|---|
| <= 45 (light, dry) | 22 | 24 | 26 | 27 |
| 60 | 20 | 22 | 24 | 25 |
| 75 | 17 | 19 | 21 | 22 |
| 90 | 14 | 16 | 18 | 19 |
| 100 (full, wet) | 12 | 14 | 16 | 17 |
- WET (water confirmed): table as above (water slows burn; advance is kept).
- DRY-PROTECT (KNOCK_RETARD asserted): table minus 8 deg (PRF91/E85) or minus 6 deg (alcohols), floor 4 deg BTDC.
- Per-event knock retard: 2 deg/event, max 10 deg, recover 0.5 deg/s.

## 5. Fuel system
- EFI preferred (closed-loop lambda, fuel-limit input). Carb: governor stop-solenoid or throttle limiter driven by FUEL_LIMIT (caps load to 60 %).
- Alcohol fuels: alcohol-rated pump, Viton/FKM seals, stainless or anodised fuel parts, larger jets/injectors (~1.5x E85, ~2.2x methanol).

## 6. Dry-running failsafe (high CR must never run dry at full advance and full load)
1. Boot and every non-injecting state: controller asserts KNOCK_RETARD + FUEL_LIMIT (fail-safe = asserted on controller power loss: use
   normally-closed opto/relay logic so a dead controller = retarded + limited).
2. Released only after 2 s of confirmed water flow (pump duty + optional flow switch) and no knock.
3. Low water / freeze / sensor fault -> water off, retard + limit stay asserted, operator lamp.
4. Knock at max water -> retard + limit; heavy knock (>0.95) persists -> kill request.
5. Watchdog reset (2 s) -> boots into step 1.
6. Mechanical backstop: CR chosen at klCR - 1, and dry-safe operation at 60 % load with -8 deg verified on the bench before release.

## 7. Materials for water exposure
- Intake runner / spacer: ASA or PA12-CF printed (SPEC.md 2.2), or aluminium 6061 hard-anodised for production.
- Valves stainless; valve guides bronze; exhaust stainless 304/321; muffler aluminised or stainless.
- Cylinder bore: cast-iron liner or Nikasil; no bare aluminium bore.
- Crankcase breather routed away from intake water nozzle; oil with corrosion inhibitor, change interval halved; drain-down/dry-run 60 s
  without water at shutdown to purge (with retard asserted).
- Demineralised/distilled water only (< 10 uS/cm); reservoir HDPE; tubing PU or PTFE; pump with EPDM or Viton diaphragm.
