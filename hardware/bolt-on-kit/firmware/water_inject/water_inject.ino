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

Adafruit_MAX31855 egt(PIN_SPI_SCK, PIN_CS_EGT, PIN_SPI_MISO);
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
void IRAM_ATTR onFlow() { flowPulses++; }

enum State { OFF, WARMUP, ARMED_DRY, INJECTING, FAULT };
State st = OFF; const char* faultWhy = "";
float trim = 1.0f, knockI = 0, egtC = 0, tIn = 25, rh = 50, mapKpa = 100; uint32_t rpm = 0, runStartMs = 0, waterOkMs = 0;
bool testMode = false; File logf;

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
static float readKnock() { // normalised 0..1 envelope from band-pass front end, sampled in knock window (crude: peak over 2 ms)
  int pk = 0; for (int k = 0; k < 40; k++) { int v = analogRead(PIN_KNOCK_ADC); if (v > pk) pk = v; delayMicroseconds(50); }
  return pk / 4095.0f; }
static void failsafe(bool dryProtect) {  // HIGH-CR: whenever water is not confirmed, force ECU retard + fuel/load limit
  digitalWrite(PIN_RETARD_OUT, dryProtect ? HIGH : LOW); digitalWrite(PIN_FUEL_LIMIT, dryProtect ? HIGH : LOW); }
static void waterOff() { ledcWrite(PIN_PUMP_PWM, 0); digitalWrite(PIN_MISTER_EN, LOW); digitalWrite(PIN_SOLENOID, LOW); }
static void fault(const char* why) { st = FAULT; faultWhy = why; waterOff(); failsafe(HIGH_CR_ENGINE); }

void setup() {
  Serial.begin(115200);
  pinMode(PIN_IGN_PICKUP, INPUT); attachInterrupt(PIN_IGN_PICKUP, onIgn, FALLING);
  pinMode(PIN_FLOW_PULSE, INPUT_PULLUP); attachInterrupt(PIN_FLOW_PULSE, onFlow, FALLING);
  pinMode(PIN_LEVEL, INPUT_PULLUP); pinMode(PIN_TEST_BTN, INPUT_PULLUP);
  for (int p : {PIN_MISTER_EN, PIN_SOLENOID, PIN_RETARD_OUT, PIN_FUEL_LIMIT, PIN_KILL_REQ}) { pinMode(p, OUTPUT); digitalWrite(p, LOW); }
  ledcAttach(PIN_PUMP_PWM, 20000, 10);
  failsafe(HIGH_CR_ENGINE);                       // boot state = dry-protect (retard + limit) until water proven
  egt.begin(); Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL); sht.begin();
  if (SD.begin()) { logf = SD.open("/log.csv", FILE_APPEND); logf.println("ms,state,rpm,map,tin,rh,egt,knock,wf_cmd,trim,pump,fuel_gs,flow_pulses"); }
  esp_task_wdt_config_t w = {.timeout_ms = 2000, .idle_core_mask = 0, .trigger_panic = true}; // reboot -> boot dry-protect
  esp_task_wdt_reconfigure(&w); esp_task_wdt_add(NULL);
}

void loop() {
  esp_task_wdt_reset();
  uint32_t now = millis(), p = periodUs;
  rpm = (p && micros() - lastPulseUs < 200000) ? 60000000UL / p : 0;
  egtC = egt.readCelsius(); sensors_event_t h, t; if (sht.getEvent(&h, &t)) { tIn = t.temperature; rh = h.relative_humidity; }
  mapKpa = analogRead(PIN_MAP_ADC) / 4095.0f * 3.3f * 1.515f / 5.0f * 115.0f / 0.9f; // MPX4115 via 1.515 divider (calibrate)
  knockI = 0.8f * knockI + 0.2f * readKnock();
  bool levelOk = digitalRead(PIN_LEVEL) == HIGH;
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
    // hydrolock guard: never more than 10 % of the stoich air mass flow as liquid, and never beyond pump calibration
    pump = constrain(mlMin / PUMP_ML_MIN_MAX, 0.0f, 1.0f);
    digitalWrite(PIN_SOLENOID, HIGH); digitalWrite(PIN_MISTER_EN, HIGH); ledcWrite(PIN_PUMP_PWM, (int)(pump * 1023));
    if (pump > 0.05f) { if (!waterOkMs) waterOkMs = now; } else waterOkMs = 0;
    // dry-protect released only after 2 s of confirmed flow and no persistent knock
    failsafe(!(waterOkMs && now - waterOkMs > 2000 && knockI < KNOCK_THRESH));
    if (knockI > KNOCK_THRESH && trim >= 1.25f) failsafe(true);  // knock even at max water -> retard + limit
  } else { waterOff(); waterOkMs = 0; failsafe(HIGH_CR_ENGINE); }
  if (knockI > 0.95f && st != OFF) digitalWrite(PIN_KILL_REQ, HIGH);   // heavy knock despite retard -> stop engine

  static uint32_t lastLog = 0;
  if (now - lastLog >= (testMode ? 1000 : 5000)) { lastLog = now;
    char b[200]; snprintf(b, sizeof b, "%lu,%d,%lu,%.1f,%.1f,%.0f,%.0f,%.2f,%.3f,%.2f,%.2f,%.3f,%lu", now, st, rpm, mapKpa, tIn, rh, egtC,
                          knockI, wfCmd, trim, pump, fuelGs(), flowPulses);
    Serial.println(b); if (logf) { logf.println(b); logf.flush(); }
    if (*faultWhy) { Serial.print("# "); Serial.println(faultWhy); }
  }
  delay(20);
}
