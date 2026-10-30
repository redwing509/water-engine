# Wiring (bench-spec rev). Pin map is authoritative in `firmware/water_inject/config.h`.

```mermaid
flowchart LR
  BAT["12 V battery / genset DC"] --> ES["E-stop XB4BS8445 (E3)"] -->|NC contact| F1["Fuse 3 A (E2)"] --> BUCK["Pololu D24V22F5 5 V"]
  BAT --> F2["Fuse 10 A (E2)"] --> PR["Power Relay FeatherWing (C5)"] --> PUMP["SEAFLO 21 pump 80 psi (W1)"]
  BAT --> F3["Fuse 5 A (E2)"] --> MOS1["MOSFET 5648 #1 (C6)"] --> SOL["Snow SNO-40060 meter solenoid (W2)"]
  F3 --> MOS2["MOSFET 5648 #2 (C6)"] --> NCV["U.S. Solid NC master valve (W3)"]
  BUCK -->|5V| ESP["ESP32 DevKitC (C1)"]
  BUCK -->|5V| MAP["GM 1-bar MAP (S4)"]
  BUCK -->|5V| TPIC["TPIC8101EVM (S6)"]
  ESP -->|GPIO26| PR
  ESP -->|GPIO25 PWM 8 Hz| MOS1
  ESP -->|GPIO33| MOS2
  ESP -->|GPIO16| R1["Relay 4409 RETARD (NC)"] --> ECU1["ECU/CDI retard input"]
  ESP -->|GPIO17| R2["Relay 4409 FUEL_LIMIT (NC)"] --> ECU2["Fuel/load limit or governor stop"]
  ESP -->|GPIO13| R3["Relay 4409 KILL (NO)"] --> KILL["Ignition kill lead to GND"]
  ES -->|NO contact| KILL
  MAP -->|"Vout via 10k/20k divider"| A32["GPIO32"] --> ESP
  KS["Bosch knock sensor (S5)"] --> TPIC
  TPIC -->|"SPI SCK18 MISO19 MOSI23 CS15, INT/HOLD 14"| ESP
  TC["K-type EGT probe (S2)"] --> MAX["MAX31855 (S1)"] -->|"SPI CS5"| ESP
  SD["microSD (C3)"] -->|"SPI CS4"| ESP
  SHT["SHT45 (S3)"] -->|"I2C SDA21 SCL22"| ESP
  LVL["Optomax level (S7)"] -->|"GPIO27 pull-up, LOW=wet"| ESP
  IGN["Inductive pickup + opto"] -->|"GPIO34 + ext 10k pull-up"| ESP
```

Notes
- Grounds: one star point at the battery negative. The knock sensor shield goes to TPIC ground only, so do not ground it at the engine too.
- The solenoid and valve coils need flyback diodes. The Adafruit 5648 has one on board. Add a 1N5819 across the SNO-40060 at the coil if leads are longer than 1 m.
- Relay contacts: RETARD and FUEL_LIMIT use **COM-NC**. With the coil unpowered (controller off, reset or dead) the ECU input is asserted.
  KILL uses **COM-NO** and only grounds the kill lead when commanded. The latch is held in RTC no-init RAM, so it survives watchdog, panic and software resets; only a power cycle of the controller clears it.

**Hardwired E-stop (E3).** The NO contact grounds the ignition kill lead directly. The NC contact sits between the battery and the 3 A controller fuse (F1), so it carries only controller current (well inside the contact rating). Opening it removes 5 V from the ESP32, so the pump relay (C5) opens, both MOSFETs (C6) turn off (meter solenoid shut, NC master valve closes) and the RETARD/FUEL_LIMIT relays drop to their asserted NC state. All of this follows from loss of power alone, with no firmware involvement. The 10 A pump and 5 A valve branches are not switched by the button directly, because their gate/coil drive comes from the controller. It stays pressed until twisted to release.
- The GPIO34/35/39 inputs have no internal pull-ups. GPIO34 (ignition pickup, open-collector opto) ALWAYS needs an external 10k to 3V3, or it floats and gives false RPM. GPIO39 needs an external 10k to 3V3 when the flow meter is fitted; set FLOW_METER_FITTED 1 in config.h only then (with 0 the GPIO39 interrupt is not attached).
- TPIC8101EVM: power it from 5 V, check that the SPI logic level jumper is set to 3.3 V-compatible (or add a level shifter), and check its 8 MHz clock source against `TPIC_PRESCALER`.
- Connectors: Deutsch DT (E1) at the engine-side break: (1) MAP+knock, (2) pump+valves, (3) ECU outputs, (4) EGT+pickup.
