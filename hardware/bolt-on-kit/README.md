# hardware/bolt-on-kit - DRAFT, DO NOT MERGE
Water-injection kit + factory high-CR engine spec for 1-10 kW generators. Model-seeded, not built or measured.
- SPEC.md - kit spec, BOM, safety, test plan, caveats
- ENGINE-ORDER-SPEC.md - factory order sheet (CR per fuel, piston/head, knock sensor, timing map, materials, dry failsafe)
- cad/*.scad - OpenSCAD parametric spacer and reservoir bracket
- firmware/water_inject/ - ESP32 Arduino sketch + config.h
Part A model reruns: ../../sims/pr10_fair_highcr/ (result: RESULT.md, 2026-10-29; factory CR per fuel in ENGINE-ORDER-SPEC.md section 2).
