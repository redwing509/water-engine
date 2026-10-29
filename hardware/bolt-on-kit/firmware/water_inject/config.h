// Water-injection controller config (Grok Bot 2026-10-29). ESP32 (Arduino core 3.x). All maps are MODEL-SEEDED, NOT MEASURED.
#pragma once
// ---- pins ----
#define PIN_IGN_PICKUP   34   // opto-isolated inductive pickup on the kill/ignition lead (1 pulse/rev single-cyl magneto)
#define PIN_KNOCK_ADC    35   // piezo knock sensor -> TPIC8101 or band-pass+envelope -> ADC (see SPEC 3.2)
#define PIN_MAP_ADC      32   // MPX4115/MPXH6115 MAP, 5V -> divider to 3.3V
#define PIN_LEVEL        27   // float switch, LOW = water low
#define PIN_SPI_SCK      18
#define PIN_SPI_MISO     19
#define PIN_CS_EGT       5    // MAX31855 K-type EGT
#define PIN_I2C_SDA      21   // SHT45 intake temp/RH
#define PIN_I2C_SCL      22
#define PIN_PUMP_PWM     25   // MOSFET low-side, diaphragm pump
#define PIN_MISTER_EN    26   // ultrasonic mister driver enable (or nozzle solenoid)
#define PIN_SOLENOID     33   // normally-closed shutoff solenoid (fail = closed)
#define PIN_RETARD_OUT   14   // to factory ECU/CDI "knock retard / limp" input (high-CR failsafe, SPEC 5)
#define PIN_FUEL_LIMIT   13   // to ECU fuel/load limit input or governor stop solenoid
#define PIN_KILL_REQ     12   // last-resort ignition kill request (relay, NO -> grounds kill lead)
#define PIN_FLOW_PULSE   4    // optional fuel flow meter (efficiency test mode)
#define PIN_TEST_BTN     0
// ---- fuel / limits ----
enum Fuel { PRF91 = 0, E85 = 1, METHANOL = 2, ETHANOL = 3 };
#define FUEL_SELECTED    PRF91
// W/F mass-ratio caps (R-WE-22: W/F <= 0.6 stability; gasoline/PRF 0.1-0.3 working range)
static const float WF_CAP[4]   = {0.30f, 0.45f, 0.60f, 0.55f};
static const float FUEL_DENS[4]= {0.745f, 0.781f, 0.792f, 0.789f}; // kg/L
#define RPM_MIN_WATER    2400  // no water below (cranking / idle-down)
#define RPM_MAX          4200
#define WARMUP_S         90    // engine run time before water allowed
#define EGT_MIN_C        450   // no water below (cold engine)
#define EGT_MAX_C        780   // overtemp -> derate
#define INTAKE_FREEZE_C  3.0f  // freeze lockout
#define MAP_MIN_KPA      45    // light load -> no water (hydrolock risk at low airflow)
#define KNOCK_THRESH     0.60f // normalised knock intensity
#define PUMP_ML_MIN_MAX  120.0f // pump calibration: ml/min at 100 % PWM (measure!)
#define HIGH_CR_ENGINE   1     // factory high-CR engine: dry operation needs retard + fuel limit (SPEC 5)
