// Water-injection controller config (Grok Bot 2026-10-29, bench-spec rev). Board: Espressif ESP32-DevKitC (WROOM-32/32E),
// Arduino-ESP32 core 3.x, FQBN esp32:esp32:esp32. All maps are MODEL-SEEDED, NOT MEASURED - calibrate per BENCH-TEST.md.
#pragma once
// ---- pins (avoid strapping pins 2/12 for outputs that must be low at boot; see WIRING.md) ----
#define PIN_IGN_PICKUP   34   // in-only, NO internal pull-up: EXTERNAL 10k to 3V3 REQUIRED (open-collector opto). opto-isolated inductive pickup on spark lead, 1 pulse/rev (magneto, wasted spark)
#define PIN_KNOCK_ADC    35   // in-only. ANALOG knock front end (budget option, KNOCK_FRONTEND_ANALOG)
#define PIN_MAP_ADC      32   // GM 1-bar MAP (FAST 307029), 5V out -> 10k/20k divider -> 3.33 V max
#define PIN_LEVEL        27   // Optomax LLC200D3SH optical level: open-collector, LOW = liquid present (pull-up)
#define PIN_FLOW_PULSE   39   // in-only, optional fuel flow meter (needs EXTERNAL 10k pull-up to 3V3)
#define FLOW_METER_FITTED 0   // 1 only when the meter AND its pull-up are fitted; 0 = GPIO39 interrupt not attached
#define PIN_TEST_BTN     0    // BOOT button (IO0 strapping pin) toggles test logging. Read only after boot; NEVER wire anything that can pull IO0 low at power-up (see WIRING.md)
#define PIN_WATER_PSI    36   // CR-001: REQUIRED nozzle-line pressure transducer (S9, 0-100 psi, 0.5-4.5 V) -> 10k/20k divider. in-only ADC1_CH0
#define PIN_SPI_SCK      18
#define PIN_SPI_MISO     19
#define PIN_SPI_MOSI     23
#define PIN_CS_EGT       5    // MAX31855 (Adafruit 269)
#define PIN_CS_SD        4    // microSD breakout (Adafruit 254)
#define PIN_CS_KNOCK     15   // TPIC8101 /CS (TPIC8101EVM)
#define PIN_KNOCK_INTHOLD 14  // TPIC8101 INT/HOLD: HIGH = integrate (knock window)
#define PIN_I2C_SDA      21   // SHT45 intake temp/RH (Adafruit 5665)
#define PIN_I2C_SCL      22
#define PIN_METER_SOL    25   // MOSFET (Adafruit 5648) -> Snow SNO-40060 solenoid, low-frequency PWM = water metering
#define PIN_PUMP_EN      26   // Power Relay FeatherWing (10 A) -> SEAFLO pump (pump holds ~80 psi by its own switch)
#define PIN_SHUTOFF      33   // MOSFET -> U.S. Solid NC master valve. LOW/unpowered = CLOSED (fail closed)
#define PIN_RETARD_RLY   16   // relay coil. Contact used = NC: coil OFF => ECU retard input ASSERTED (fail-safe)
#define PIN_FUEL_LIM_RLY 17   // relay coil. Contact used = NC: coil OFF => fuel/load limit ASSERTED (fail-safe)
#define PIN_KILL_RLY     13   // relay coil. Contact used = NO: coil ON => grounds kill lead (latched until reset)
// ---- knock front end ----
#define KNOCK_FRONTEND_TPIC   1
#define KNOCK_FRONTEND_ANALOG 2
#define KNOCK_FRONTEND   KNOCK_FRONTEND_TPIC
// TPIC8101 setup bytes (datasheet SLIS110C tables). VERIFY codes for your oscillator / bore before first run.
#define TPIC_PRESCALER   0x46  // CR-003: cmd 010 D4..D0, D4..D1=0011 -> 8 MHz, D0=0 -> SDO active (TI SLIS110C prescaler table; 0x4C = 16 MHz)
#define TPIC_ADV_MODE    0x71  // command 6: enter advanced SPI mode (SDO then returns data instead of echo)
#define TPIC_ADV_ACK     0x8E  // advanced-mode response to 0x71 (inverted command), seen on the NEXT transfer
#define TPIC_CHANNEL     0xE0  // channel 1
#define TPIC_BANDPASS    0x2A  // band-pass index ~7.3 kHz (GX200-class 68 mm bore: f ~= 900/(pi*0.034)/... ~7-8 kHz)
#define TPIC_GAIN        0x8E  // gain index (adjust so normal-run knock value ~ 0.2-0.3 full scale)
#define TPIC_INTEGRATOR  0xC9  // integrator time-constant index
#define KNOCK_WIN_START_DEG 35 // window opens this many crank degrees after the pickup pulse (spark ~25 BTDC -> ~10 ATDC)
#define KNOCK_WIN_LEN_DEG   50 // window length, crank degrees
// ---- fuel / limits ----
enum Fuel { PRF91 = 0, E85 = 1, METHANOL = 2, ETHANOL = 3 };
#define FUEL_SELECTED    PRF91
// CR in use for now (ENGINE-ORDER-SPEC.md): PRF91 9.0, E85 12.5, methanol 14, ethanol 14. Updated later by high-CR results.
static const float ENGINE_CR[4] = {9.0f, 12.5f, 14.0f, 14.0f};
// W/F mass-ratio caps (R-WE-22: W/F <= 0.6 stability; gasoline/PRF 0.1-0.3 working range)
// CR-004: PRF91 cap 0.43 = W/F of the modeled w0.3 case (water mass fraction w=0.3 -> W/F = w/(1-w) = 0.43); still <= 0.6
static const float WF_CAP[4]   = {0.43f, 0.45f, 0.60f, 0.55f};
static const float FUEL_DENS[4]= {0.745f, 0.781f, 0.792f, 0.789f}; // kg/L
#define RPM_MIN_WATER    2400  // no water below (cranking / idle-down)
#define RPM_MAX          4200
#define WARMUP_S         90    // engine run time before water allowed
#define EGT_MIN_C        450   // no water below (cold engine)
#define EGT_MAX_C        780   // overtemp -> add water / derate
#define INTAKE_FREEZE_C  3.0f  // freeze lockout
#define MAP_MIN_KPA      45    // light load -> no water (hydrolock risk at low airflow)
#define KNOCK_THRESH     0.60f // normalised knock intensity
// ---- water metering (pulsed solenoid at constant pump pressure) ----
#define METER_PWM_HZ     8     // solenoid PWM frequency (Snow solenoids are fine at 5-10 Hz)
#define METER_ML_MIN_FULL 23.0f // ml/min at 100 % duty, SNO-N0050 0.5 GPH nozzle @ ~80 psi. MEASURE (BENCH-TEST step B3)
#define METER_DUTY_MIN   0.10f // below this the solenoid does not open repeatably -> treat as zero
// ---- water-delivery confirmation (CR-001). Dry-protect is only released when this sensor PROVES delivery. ----
#define WATER_PSI_FULL     100.0f // transducer span, psi at 4.5 V
#define WATER_PSI_ON_MIN   50.0f  // nozzle-line peak over 1 s must reach this while metering (pump ~80 psi). BENCH-CALIBRATE (B3)
#define WATER_PSI_OFF_MAX  25.0f  // and the 1 s minimum must fall below this (proves the nozzle is flowing, not blocked). BENCH-CALIBRATE
#define WATER_DUTY_NO_DECAY 0.90f // at >= this duty the off-time is too short to check decay; peak check only
#define HIGH_CR_ENGINE   1     // dry operation needs retard + fuel limit (SPEC 5)
