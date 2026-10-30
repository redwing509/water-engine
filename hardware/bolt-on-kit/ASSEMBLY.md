# Assembly guide (bench-spec rev)
Tools: 1/8-27 NPT tap, 11/32" drill, Deutsch DT crimper, wire strippers, multimeter, 3D printer with an enclosure (for ASA).

1. **Print** `cad/intake_spacer.scad` and `cad/reservoir_bracket.scad` with the settings in each file's header (ASA, 0.2 mm layers;
   the spacer at 100 % infill with 6 walls). Set `bore_d`, `stud_spacing` and `thickness` for your carb first. Measure the pump foot pattern and edit `pump_holes`.
2. **Spacer:** tap the nozzle boss 1/8 NPT and fit the SNO-N0050 nozzle with methanol-rated PTFE paste. Fit longer carb studs (by spacer thickness) and gaskets on both faces.
   Check throttle/choke linkage and air-box clearance. Torque ≤ 6 N·m.
3. **Water side:** mount the Snow tank by its tabs. Run tank → filter (W6) → pump (W1) → NC master valve (W3) → meter solenoid (W2) → nozzle,
   with Snow 1/4" nylon tube (W7) and quick-connect fittings (W8). Mount the solenoid within 300 mm of the nozzle to keep the line volume small. Fit the Optomax sensor (S7) in the lower third of the tank.
4. **Sensors:** EGT probe 50 mm from the exhaust port (drill and tap 1/8 NPT in the header flange or a weld bung). Knock sensor on a flat machined boss
   on the cylinder or head, M8 at 20 N·m, no washer. Tee the MAP sensor into the spacer below the throttle, or into the intake runner. Mount the SHT45 in the air box upstream of the carb.
   Clamp the inductive pickup on the spark lead and wire it through the opto to GPIO34.
5. **Controller box:** build the electronics per `WIRING.md` (ESP32, buck, relays, MOSFETs, SD) and fuse each branch.
6. **ECU outputs:** find the factory module's retard / limp / governor input. If there is none, use FUEL_LIMIT on a governor stop solenoid and treat RETARD as not connected.
   That case is not safe at high CR, so do not run water-free at high CR without a working retard path (SPEC 5).
7. **Firmware:** set `FUEL_SELECTED`, then `arduino-cli compile --fqbn esp32:esp32:esp32 firmware/water_inject` and
   `arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 firmware/water_inject`.
8. Run BENCH-TEST.md part A (static checks) before the engine is started.
