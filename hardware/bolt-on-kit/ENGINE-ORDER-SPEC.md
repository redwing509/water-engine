# Engine order spec sheet: factory high-CR generator engine for water injection (DRAFT, Grok Bot 2026-10-29)

Status: DRAFT for James. CR values are MODEL output (M03 + M03-CRN, one knock engine for the Track A scan), NOT measured.
Final CR numbers come from box jobs 172-175 (`sims/pr10_fair_highcr/`, RESULT.md). Do not place an order on these numbers alone;
build one engine, bench test it (SPEC.md section 7), then order.

## 1. Base engine
- Single-cylinder, air-cooled, OHV, 4-stroke, 196-460 cc class (GX200 / 420cc-clone family), for 1-10 kW gensets; carb or EFI.
- Fixed-speed 3000/3600 rpm (50/60 Hz) or inverter 2000-4200 rpm.

## 2. Compression ratio (geometric)
| fuel | provisional factory CR (with water, klCR - 1 margin) | basis | dry-safe CR (no water) |
|---|---|---|---|
| PRF91 / pump 91 | 9.0 +/- 0.2 (provisional) | Track B CR co-opt (box 145/149/155): hot-regime co-optimised wet CR 8.5 at w0.30, i.e. water buys little CR on gasoline in hot duty; normal-regime scan not yet run | 8.5 (stock) |
| E85 | 12.5 +/- 0.2 (provisional) | DEI baseline CR 12 hot | 12 |
| Methanol (M100) | 14 for hot/variable duty; up to 18 if jobs 172/174 confirm | Track A hot humid w0.15: CR 25 knock-free in M03 (box 156) but single-knock-engine and EXTRAPOLATED above 24 | ~12 |
| Ethanol (E100) | 14; up to 16 if jobs 173/175 confirm | PR 10 C2H5OH dry klCR 16 hot (CA50 rule) | ~13 |
Recommendation: specify CR by fuel, +/- 0.2 tolerance, measured by cc'ing the chamber; the high-CR numbers are capped
far below the model's 24-25 because (a) only one knock model ran on Track A, (b) an air-cooled engine sees hot-spot preignition
that the model does not capture, and (c) the engine must survive a water-out event (section 6).

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
