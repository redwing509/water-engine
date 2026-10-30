// Pump / valve mounting plate that clamps to a generator frame tube (Grok Bot 2026-10-29, bench-spec rev).
// The Snow SNO-40012 3-qt tank has its own mounting tabs, so this part only carries the SEAFLO 21-series pump,
// the U.S. Solid NC valve and the SNO-40060 metering solenoid. Units mm.
// PRINT SETTINGS: Polymaker PolyLite ASA (BOM P1), 0.4 mm nozzle, 0.2 mm layers, 4 perimeters, 40 % gyroid infill,
// 255 C / 105 C bed, enclosed. Print plate-flat. PETG acceptable if mounted away from the exhaust (>150 mm).
// Hardware: 2x M5 pinch bolts + nyloc per clamp; M5 heat-set inserts or through-bolts for pump feet (measure pump foot pattern).
tube_d   = 25.4;   // frame tube OD (1")
wall     = 5;
clamp_w  = 25;
plate_l  = 160; plate_w = 90; plate_t = 5;
pump_holes = [[30,20],[30,70],[95,20],[95,70]]; // SEAFLO 21-series foot pattern - MEASURE your pump and edit
valve_holes = [[125,30],[145,30]];              // valve / solenoid strap holes (zip-tie or P-clip)
hole_d = 5.5;
$fn = 64;
module clamp() difference() {
  union() { cylinder(d=tube_d+2*wall, h=clamp_w); translate([tube_d/2, -wall, 0]) cube([wall+6, 2*wall, clamp_w]); }
  translate([0,0,-1]) cylinder(d=tube_d, h=clamp_w+2);
  translate([0,-1,-1]) cube([tube_d+20, 2, clamp_w+2]);                      // pinch slot
  translate([tube_d/2+wall/2+3, 0, clamp_w/2]) rotate([90,0,0]) cylinder(d=hole_d, h=40, center=true);
}
difference() {
  union() {
    cube([plate_l, plate_w, plate_t]);
    for (x=[0, plate_l-clamp_w]) translate([x+clamp_w, -tube_d/2-wall, plate_t]) rotate([0,-90,0]) clamp();
  }
  for (h=concat(pump_holes, valve_holes)) translate([h[0], h[1], -1]) cylinder(d=hole_d, h=plate_t+2);
}
