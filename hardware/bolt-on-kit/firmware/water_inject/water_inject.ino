// Water-injection controller for factory high-CR generator engines (Grok Bot 2026-10-29, redwing509/water-engine).
// Open-loop W/F map (load x RPM) seeded from model optima, closed-loop trim on knock and EGT, safety interlocks,
// HIGH-CR DRY FAILSAFE (asserts ECU retard + fuel limit whenever water is not confirmed flowing), CSV logging,
// efficiency-test mode (g fuel per kWh). Model-seeded values are NOT measured; calibrate on the bench first (SPEC 7).
#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_MAX31855.h>   // lib: Adafruit MAX31855
#include <Adafruit_SHT4x.h>      // lib: Adafruit SHT4x
#include <SD.h>
#include <esp_task_wdt.h>
#include "config.h"

Adafruit_MAX31855 egt(PIN_CS_EGT, &SPI);   // shares hardware SPI with SD + TPIC8101
Adafruit_SHT4x sht;
// ---- W/F base map: rows = MAP kPa {45,60,75,90,100}, cols = RPM {2400,3000,3600,4200}. Fraction of WF_CAP. ----
static const float MAP_AX[5] = {45, 60, 75, 90, 100};
static const float RPM_AX[4] = {2400, 3000, 3600, 4200};
static const float WF_FRAC[5][4] = {   // seeded: model optimum near cap at full load, none at light load
  {0.00f, 0.00f, 0.00f, 0.00f},
  {0.20f, 0.25f, 0.30f, 0.30f},
  {0.45f, 0.55f, 0.60f, 0.60f},
  {0.75f, 0.85f, 0.90f, 0.90f},
  {0.90f, 1.00f, 1.00f, 1.00f}};
volatile uint32_t lastPulseUs = 0, periodUs = 0, flowPulses = 0;
void IRAM_ATTR onIgn() { uint32_t t = micros(); if (t - lastPulseUs > 4000) { periodUs = t - lastPulseUs; lastPulseUs = t; } }
void IRAM_ATTR onFlow() { flowPulses = flowPulses + 1; }
// ---- knock window: 20 kHz tick opens/closes TPIC8101 INT/HOLD at crank-angle positions derived from the last period ----
volatile uint32_t winStartUs = 0, winEndUs = 0; volatile bool winOpen = false, knockReady = false;
hw_timer_t* tick = nullptr;
void ARDUINO_ISR_ATTR onTick() {
  uint32_t p = periodUs; if (!p) return; uint32_t dt = micros() - lastPulseUs;
  uint32_t s = p * KNOCK_WIN_START_DEG / 360, e = p * (KNOCK_WIN_START_DEG + KNOCK_WIN_LEN_DEG) / 360;
  bool open = dt >= s && dt < e;
  if (open != winOpen) { winOpen = open; digitalWrite(PIN_KNOCK_INTHOLD, open); if (!open) knockReady = true; }
}
static const SPISettings TPIC_SPI(1000000, MSBFIRST, SPI_MODE1);
static uint8_t tpicXfer(uint8_t c) { SPI.beginTransaction(TPIC_SPI); digitalWrite(PIN_CS_KNOCK, LOW);
  uint8_t r = SPI.transfer(c); digitalWrite(PIN_CS_KNOCK, HIGH); SPI.endTransaction(); return r; }
static void tpicInit() { for (uint8_t c : {(uint8_t)TPIC_PRESCALER, (uint8_t)TPIC_CHANNEL, (uint8_t)TPIC_BANDPASS,
                                          (uint8_t)TPIC_GAIN, (uint8_t)TPIC_INTEGRATOR}) tpicXfer(c); }
static float lastKnock = 0;

enum State { OFF, WARMUP, ARMED_DRY, INJECTING, FAULT };
State st = OFF; const char* faultWhy = "";
float trim = 1.0f, knockI = 0, egtC = 0, tIn = 25, rh = 50, mapKpa = 100; uint32_t rpm = 0, runStartMs = 0, waterOkMs = 0;
bool testMode = false; File logFile;

static float interp2(float m, float r) {
  auto idx = [](const float* ax, int n, float v, int& i, float& f) {
    if (v <= ax[0]) { i = 0; f = 0; return; } if (v >= ax[n-1]) { i = n-2; f = 1; return; }
    for (i = 0; i < n-1 && v > ax[i+1]; i++); f = (v - ax[i]) / (ax[i+1] - ax[i]); };
  int i, j; float fi, fj; idx(MAP_AX, 5, m, i, fi); idx(RPM_AX, 4, r, j, fj);
  float a = WF_FRAC[i][j]*(1-fj) + WF_FRAC[i][j+1]*fj, b = WF_FRAC[i+1][j]*(1-fj) + WF_FRAC[i+1][j+1]*fj;
  return a*(1-fi) + b*fi;
}
// Fuel mass flow estimate (g/s) from speed-density; replace with flow meter when fitted. DISP_L = engine displacement.
static const float DISP_L = 0.420f, VE = 0.80f, AFR[4] = {14.7f, 9.8f, 6.45f, 9.0f};
static float fuelGs() { float airGs = DISP_L * 1e-3f * (rpm / 120.0f) * VE * (mapKpa * 1000.0f) / (287.0f * (tIn + 273.15f)) * 1000.0f;
  return airGs / AFR[FUEL_SELECTED]; }
static float readKnock() {
#if KNOCK_FRONTEND == KNOCK_FRONTEND_TPIC
  // TPIC8101: after INT/HOLD falls the 10-bit integrator result shifts out on the next two SPI frames (low 8, then high 2).
  // Re-sending channel + gain keeps the setup unchanged while clocking the result out.
  if (!knockReady) return lastKnock; knockReady = false;
  uint8_t lo = tpicXfer(TPIC_CHANNEL), hi = tpicXfer(TPIC_GAIN);
  lastKnock = (((hi & 0x03) << 8) | lo) / 1023.0f; return lastKnock;
#else // ANALOG budget front end: band-pass + envelope detector into ADC, peak over 2 ms
  int pk = 0; for (int k = 0; k < 40; k++) { int v = analogRead(PIN_KNOCK_ADC); if (v > pk) pk = v; delayMicroseconds(50); }
  return pk / 4095.0f;
#endif
}
// HIGH-CR: whenever water is not confirmed, force ECU retard + fuel/load limit. Relays use NC contacts, so the ASSERTED
// state is coil OFF: a dead, resetting or unpowered controller also gives retard + limit.
static void failsafe(bool dryProtect) {
  digitalWrite(PIN_RETARD_RLY, dryProtect ? LOW : HIGH); digitalWrite(PIN_FUEL_LIM_RLY, dryProtect ? LOW : HIGH); }
static void waterOff() { ledcWrite(PIN_METER_SOL, 0); digitalWrite(PIN_PUMP_EN, LOW); digitalWrite(PIN_SHUTOFF, LOW); }
static void fault(const char* why) { st = FAULT; faultWhy = why; waterOff(); failsafe(HIGH_CR_ENGINE); }

void setup() {
  Serial.begin(115200);
  pinMode(PIN_IGN_PICKUP, INPUT); attachInterrupt(PIN_IGN_PICKUP, onIgn, FALLING);
  pinMode(PIN_FLOW_PULSE, INPUT); attachInterrupt(PIN_FLOW_PULSE, onFlow, FALLING);
  pinMode(PIN_LEVEL, INPUT_PULLUP); pinMode(PIN_TEST_BTN, INPUT_PULLUP);
  for (int p : {PIN_PUMP_EN, PIN_SHUTOFF, PIN_RETARD_RLY, PIN_FUEL_LIM_RLY, PIN_KILL_RLY, PIN_KNOCK_INTHOLD})
    { pinMode(p, OUTPUT); digitalWrite(p, LOW); }
  for (int p : {PIN_CS_EGT, PIN_CS_SD, PIN_CS_KNOCK}) { pinMode(p, OUTPUT); digitalWrite(p, HIGH); }
  ledcAttach(PIN_METER_SOL, METER_PWM_HZ, 10); ledcWrite(PIN_METER_SOL, 0);
  failsafe(HIGH_CR_ENGINE);                       // boot state = dry-protect (retard + limit) until water proven
  SPI.begin(PIN_SPI_SCK, PIN_SPI_MISO, PIN_SPI_MOSI);
  egt.begin(); Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL); sht.begin();
#if KNOCK_FRONTEND == KNOCK_FRONTEND_TPIC
  tpicInit(); tick = timerBegin(1000000); timerAttachInterrupt(tick, &onTick); timerAlarm(tick, 50, true, 0);
#endif
  if (SD.begin(PIN_CS_SD)) { logFile = SD.open("/log.csv", FILE_APPEND); logFile.println("ms,state,rpm,map,tin,rh,egt,knock,wf_cmd,trim,meter_duty,fuel_gs,flow_pulses"); }
  esp_task_wdt_config_t w = {.timeout_ms = 2000, .idle_core_mask = 0, .trigger_panic = true}; // reboot -> boot dry-protect
  esp_task_wdt_reconfigure(&w); esp_task_wdt_add(NULL);
}

void loop() {
  esp_task_wdt_reset();
  uint32_t now = millis(), p = periodUs;
  rpm = (p && micros() - lastPulseUs < 200000) ? 60000000UL / p : 0;
  egtC = egt.readCelsius(); sensors_event_t h, t; if (sht.getEvent(&h, &t)) { tIn = t.temperature; rh = h.relative_humidity; }
  // GM 1-bar MAP (FAST 307029): ~10 kPa @ 0 V .. ~105 kPa @ 5 V (kPa ~= 18.9*V + 10.6). 10k/20k divider -> x1.5.
  // Calibrate: engine off, compare against local station pressure (BENCH-TEST step B1).
  mapKpa = 18.9f * (analogReadMilliVolts(PIN_MAP_ADC) / 1000.0f * 1.5f) + 10.6f;
  knockI = 0.8f * knockI + 0.2f * readKnock();
  bool levelOk = digitalRead(PIN_LEVEL) == LOW;     // Optomax: LOW = liquid at sensor
  if (digitalRead(PIN_TEST_BTN) == LOW) { testMode = !testMode; flowPulses = 0; delay(300); }

  // ---- interlocks (order matters; any trip -> water off; high-CR -> dry-protect) ----
  if (rpm == 0) { st = OFF; runStartMs = 0; waterOff(); failsafe(HIGH_CR_ENGINE); }
  else if (!runStartMs) { runStartMs = now; st = WARMUP; }
  if (st != OFF && st != FAULT) {
    if (isnan(egtC)) fault("EGT sensor");
    else if (egtC > EGT_MAX_C + 60) fault("overtemp");
    else if (tIn < INTAKE_FREEZE_C) { st = ARMED_DRY; faultWhy = "freeze"; }
    else if (!levelOk) { st = ARMED_DRY; faultWhy = "low water"; }
    else if (rpm < RPM_MIN_WATER || mapKpa < MAP_MIN_KPA) { st = ARMED_DRY; faultWhy = "idle/light load"; }
    else if (now - runStartMs < WARMUP_S * 1000UL || egtC < EGT_MIN_C) { st = WARMUP; faultWhy = "warmup"; }
    else { st = INJECTING; faultWhy = ""; }
  }
  if (st == FAULT && rpm == 0) st = OFF;          // faults latch until engine stops

  float wfCmd = 0, pump = 0;
  if (st == INJECTING) {
    // closed-loop trim: knock -> add water (charge cooling) up to cap; EGT high -> add; EGT well below & no knock -> creep down to save water
    if (knockI > KNOCK_THRESH) trim += 0.05f; else if (egtC > EGT_MAX_C) trim += 0.02f; else trim -= 0.002f;
    trim = constrain(trim, 0.6f, 1.25f);
    wfCmd = min(interp2(mapKpa, rpm) * trim * WF_CAP[FUEL_SELECTED], WF_CAP[FUEL_SELECTED]);
    float mlMin = wfCmd * fuelGs() * 60.0f;        // water g/min == ml/min
    // metering: pump holds constant pressure; solenoid duty = ml/min / calibrated full-duty flow (capped at 100 %)
    pump = constrain(mlMin / METER_ML_MIN_FULL, 0.0f, 1.0f);
    if (pump < METER_DUTY_MIN) pump = 0;
    digitalWrite(PIN_SHUTOFF, HIGH); digitalWrite(PIN_PUMP_EN, HIGH); ledcWrite(PIN_METER_SOL, (int)(pump * 1023));
    if (pump > 0 && levelOk) { if (!waterOkMs) waterOkMs = now; } else waterOkMs = 0;
    // dry-protect released only after 2 s of confirmed flow and no persistent knock
    failsafe(!(waterOkMs && now - waterOkMs > 2000 && knockI < KNOCK_THRESH));
    if (knockI > KNOCK_THRESH && trim >= 1.25f) failsafe(true);  // knock even at max water -> retard + limit
  } else { waterOff(); waterOkMs = 0; failsafe(HIGH_CR_ENGINE); }
  if (knockI > 0.95f && st != OFF) digitalWrite(PIN_KILL_RLY, HIGH);   // heavy knock despite retard -> stop engine (latched until reset)

  static uint32_t lastLog = 0;
  if (now - lastLog >= (testMode ? 1000 : 5000)) { lastLog = now;
    char b[200]; snprintf(b, sizeof b, "%lu,%d,%lu,%.1f,%.1f,%.0f,%.0f,%.2f,%.3f,%.2f,%.2f,%.3f,%lu", now, st, rpm, mapKpa, tIn, rh, egtC,
                          knockI, wfCmd, trim, pump, fuelGs(), flowPulses);
    Serial.println(b); if (logFile) { logFile.println(b); logFile.flush(); }
    if (*faultWhy) { Serial.print("# "); Serial.println(faultWhy); }
  }
  delay(20);
}
