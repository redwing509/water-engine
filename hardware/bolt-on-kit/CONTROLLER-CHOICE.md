# Controller choice (bench-spec rev, 2026-10-29)

| | ESP32 DevKitC (WROOM-32) | Speeduino (v0.4 board + Mega 2560) | Arduino Mega 2560 / Teensy 4.x |
|---|---|---|---|
| What it is | Dev board, 240 MHz dual core, Wi-Fi/BT | Complete open-source ECU (fuel + ignition) | Dev boards (8-bit 16 MHz / 600 MHz Cortex-M7) |
| Fit to job | Add-on controller beside the factory ignition | Replaces factory ignition/fuel, which is a much larger change for a bolt-on kit | Add-on controller |
| Knock | TPIC8101 over SPI, or the analog envelope on ADC | No knock conditioner on board (add-on only) | Same as ESP32 |
| ADC / PWM / timers | 12-bit ADC (non-linear, so it is calibrated), LEDC PWM down to <1 Hz, HW timers | 10-bit | Mega 10-bit; Teensy 10-12-bit |
| Logging / telemetry | SD + Wi-Fi (future live view) | TunerStudio serial | SD; no radio |
| Existing firmware | Already written for Arduino-ESP32 3.x, so the port is small | Full rewrite as a Speeduino fork | Port needed (LEDC, watchdog, timers) |
| Price (verified) | **$15.00** Adafruit 3269 | ~$100-200 board + Mega | Mega ~$48, Teensy 4.1 ~$32 |

**Choice: ESP32 DevKitC.** It is the cheapest option, the firmware is already on this platform, and it has the needed SPI, I2C, ADC and low-frequency
PWM. Speeduino would replace the engine's factory ignition, which defeats the point of a bolt-on kit, and it would still need an external
knock DSP. A Mega or Teensy has no feature advantage for this I/O count and would need a port.
Port/adaptation done in this revision (compiled with arduino-cli, FQBN `esp32:esp32:esp32`, core 3.3.12):
- Pulsed-solenoid water metering (8 Hz LEDC on the Snow SNO-40060) at constant pump pressure; pump on/off via relay; NC master valve.
- GM 1-bar MAP calibration (`analogReadMilliVolts`, 10k/20k divider).
- TPIC8101 SPI driver with a crank-angle knock window (20 kHz HW-timer tick drives INT/HOLD); analog path kept (`KNOCK_FRONTEND`).
- Shared hardware SPI for MAX31855 / SD / TPIC. Fixed a pre-existing SD CS clash with the EGT CS (both GPIO5) and a `logf` name clash that stopped the old sketch compiling.
- Relay outputs moved off strapping pins (GPIO12/14). RETARD/FUEL_LIMIT use NC contacts, so coil OFF = asserted.
