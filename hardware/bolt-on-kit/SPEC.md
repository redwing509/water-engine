# Water-injection kit for factory high-CR portable generators (1-10 kW) - SPEC v0.2 bench-spec (Grok Bot 2026-10-29)

For James (t282u + 2:15 PM update). Kit = printable intake spacer + mister/nozzle + reservoir/pump + ESP32 controller, fitted to a generator
engine ordered from the factory at a raised compression ratio (see `ENGINE-ORDER-SPEC.md`). Status: DESIGN, nothing built or measured.

## 1. Expected gains (honest)
- All gains are MODEL output (M03 cycle + M03-CRN; Track A klCR from one knock engine), NOT measured on any engine.
- At a fixed stock CR the fair-baseline model gain is about +1 to +2 pp efficiency (PRF91 hot ~+2.1 pp at W/F 0.43, R-WE-22 cap W/F <= 0.6).
- With the factory CR raised to the wet knock limit, the old PR 10 numbers (+7 to +8 pp) were vs an unfair dry baseline. Against the
  fair dry baseline (dry also gets fuel-evap cooling AND its own knock-limited CR) the PR 10 rows were -1 to -3 pp with power loss.
  The re-scan (box jobs 172-175) finds the real wet optimum CR per fuel; see `sims/pr10_fair_highcr/RESULT.md` when done.
- High CR cannot run dry at full load/advance: section 5 failsafe is mandatory.
- Warranty: a factory-modified engine + water injection is outside normal warranty; agree terms with the maker.
- Emissions: EPA Phase 3 / CARB SORE certification covers the engine as certified; a modified CR or added injection needs the maker's
  certification or an exemption (e.g. test/experimental use). Water lowers NOx; CO/HC may rise.
- Corrosion: water in the intake and condensate in the crankcase - see ENGINE-ORDER-SPEC section 7 and the post-run dry purge.

## 2. Mechanical
### 2.1 Layout
air filter -> carb/throttle body -> **spacer with nozzle or mister pocket** (`cad/intake_spacer.scad`) -> intake port.
Reservoir (1-2 L HDPE) + 12 V diaphragm pump + NC solenoid on the frame (`cad/reservoir_bracket.scad`), PU 4 mm tubing, 40 um inline filter. (Bench kit: Snow 3-qt tank, SEAFLO 80 psi pump, Snow 0.5 GPH nozzle and pulsed solenoid; see BOM.csv.)
Delivery options: (a) fine nozzle 0.15-0.3 mm (fogging nozzle, 3-7 bar) pointed downstream at 30 deg - preferred for 3-10 kW;
(b) ultrasonic mister disc (16-20 mm, 1.7 MHz or 110 kHz) in an upstream pocket, aerosol fed into the bore - preferred for 1-3 kW (low flow,
matches the model's "humid_evap" case). Liquid nozzle = model "liquid" case.
### 2.2 Printable materials
| part | material | why |
|---|---|---|
| intake spacer | ASA (Tg ~100 C) min; PA12-CF or PA6-CF (HDT 150+ C) preferred | carb flange 60-90 C, fuel + alcohol splash. PETG (Tg 80 C) NOT for spacer. Alcohols swell some nylons - use PA12, check |
| reservoir bracket, controller box | PETG or ASA | cool side, UV (ASA) |
| nozzle boss threads | brass heat-set insert M8x1 | printed threads leak |
Print 100 % infill around bore and studs, 4+ walls; seal faces with gasket material; torque studs <= 6 N m; replace after heat cycling review.
### 2.3 Parametric dimensions (OpenSCAD customiser)
`bore_d` (19-32 mm), `thickness` (10-15), `stud_spacing`, `stud_d`, `nozzle_angle`, `nozzle_thread_d`, `temp_rh_port_d`. Spacer moves carb out by `thickness`: check linkage/air-box clearance; longer studs.
### 2.4 Water flow sizing
water g/min = W/F x fuel g/min. 5 kW at ~300 g/kWh = 25 g/min fuel -> 2.5-7.5 g/min water at W/F 0.1-0.3 (gasoline); methanol (~2.2x fuel mass) at W/F 0.3 -> ~16 g/min. Bench kit: constant-pressure pump + pulsed solenoid, 0.5 GPH nozzle ~23 ml/min at 100 % duty (BENCH-TEST A3).

## 3. Electronics
- ESP32-WROOM-32E devkit; 12 V from genset DC or a 12 V battery; buck to 5 V/3.3 V; TVS + reverse protection on 12 V input.
- Sensors: RPM from ignition lead pickup (inductive clamp -> opto, 1 pulse/rev); EGT K-type in exhaust flange 50 mm from port via MAX31855;
  intake temp/RH SHT45 upstream of nozzle; MAP GM 1-bar (FAST 307029) teed into spacer (or TPS on EFI); piezo knock sensor on the cylinder boss via TPIC8101
  knock DSP (or band-pass 6-8 kHz + envelope to ADC, as coded); float level switch; optional fuel flow meter (efficiency test).
- Outputs: pump on/off (relay, constant ~80 psi); Snow metering solenoid 8 Hz PWM via MOSFET; NC master valve; three relay outputs to the factory ECU/CDI:
  KNOCK_RETARD, FUEL_LIMIT, KILL_REQ (fail-safe wiring: de-energised = asserted).
- MicroSD logging. Pin map in `firmware/water_inject/config.h`.

## 4. Firmware (`firmware/water_inject/water_inject.ino`, Arduino-ESP32 3.x)
- Base map W/F = WF_FRAC[MAP][RPM] x WF_CAP[fuel]; caps: PRF91 0.30, E85 0.45, ethanol 0.55, methanol 0.60 (R-WE-22 W/F <= 0.6).
  Seeded from model optima (water at full load, none at light load). Calibrate.
- Closed-loop trim 0.6-1.25: knock -> +5 %, EGT > 780 C -> +2 %, otherwise -0.2 %/cycle to find the minimum water that keeps knock-free.
- Water flow from speed-density fuel estimate (or flow meter). Logs CSV every 5 s (1 s in test mode).
- Efficiency-test mode (BOOT button): 1 Hz log incl. fuel-flow pulses; g/kWh = fuel mass / (load-bank kWh).
- Compiles with arduino-cli (esp32:esp32 3.3.12, FQBN esp32:esp32:esp32), 2026-10-29.

## 5. Safety interlocks and high-CR dry failsafe
No water: rpm 0 / cranking / < 2400 rpm (idle), < 90 s run or EGT < 450 C (warm-up), MAP < 45 kPa (light load, hydrolock risk), intake < 3 C (freeze),
low water. Fault-latch (until stop): EGT sensor fault, EGT > 840 C. Watchdog 2 s. Dry-protect (ECU retard + fuel limit) is asserted whenever
water is not confirmed for 2 s, and on any fault, boot or controller power loss. Heavy knock with retard asserted -> kill request (latched across watchdog/soft resets; power cycle clears). A hardwired E-stop (BOM E3) stops the engine and cuts kit power independently of the controller.
Hydrolock: pump flow capped by calibration and W/F cap; nozzle downstream of throttle only with MAP gate; drain the spacer low point.
Freeze: drain reservoir below 3 C storage, or 10 % methanol in water ONLY for methanol-fuelled engines. Water: demineralised/distilled only.

## 6. BOM
See **BOM.csv**: every part is off the shelf, and each link and price was checked on 2026-10-29. The kit costs **$867.97**, test equipment costs **$1,472.48** (preferred 5 kW load bank $1,320, out of stock until Jan 2027; Kill A Watt cross-check meter $29.99), and the main total is **$2,340.45**. Optional load alternatives are priced separately and excluded from the main total: (a) heaters $159.96, (b) DIY element box $147.18, (c) rental $330/day or $0 borrowed. See `LOAD-OPTIONS.md`.
The v0.1 estimate of ~$240 assumed generic parts. The verified kit is dearer mainly because of the TPIC8101EVM ($154.72) and the Snow water components.
Controller choice: CONTROLLER-CHOICE.md. Wiring: WIRING.md. Assembly: ASSEMBLY.md.

## 7. Test plan (dry vs wet, real generator, load bank). The full procedure is in BENCH-TEST.md
1. Same engine, same day, same fuel batch; resistive load bank at 25/50/75/100 % rated kW; log kW (true-power meter), fuel mass by scale
   (+/- 1 g) or Coriolis/flow meter, EGT, knock, intake T/RH, MAP.
2. Dry baseline: at the factory CR with dry-protect retard and its own best knock-free timing; 3 x 10 min per load point. This IS the fair dry baseline.
3. Wet: W/F steps 0.1/0.2/0.3 (gasoline) or to 0.6 (alcohols), full timing map, 3 x 10 min per point; ABAB order to cancel drift.
4. Metric: g/kWh (BSFC electrical) and efficiency = 3.6 MJ / (g/kWh x LHV); power at 100 % load must be >= dry.
5. Accept a gain only if > 2 sigma of repeat scatter (typically +/- 1-2 %). Oil sample and bore/valve inspection after 20 h for corrosion.
6. Dry-failsafe test: pull the water mid-run at 100 % load -> confirm retard+limit within 0.5 s, no knock, no damage.
