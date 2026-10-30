// Water-injection intake spacer, parametric (Grok Bot 2026-10-29). Sits between carb/throttle body and intake port
// (or between air filter and carb on engines with no room). Units mm. Carries the Snow SNO-N0050 nozzle (1/8-27 NPT).
// PRINT SETTINGS (bench-spec rev): Polymaker PolyLite ASA (BOM P1), 0.4 mm nozzle, 0.2 mm layers, 6 perimeters, 100 % infill,
// 255 C nozzle / 105 C bed, enclosure closed, fan <= 20 %, no supports needed if printed flange-face down.
// Post: tap nozzle boss 1/8-27 NPT by hand (pilot printed 8.7 mm = 11/32" tap drill), thread sealant rated for methanol (PTFE paste).
// Alternate material PA12-CF (drier, 0.6 mm hardened nozzle) for engines where the carb flange exceeds ~85 C.
/* [Bore / flange] */
bore_d        = 24;    // venturi-side bore, match carb outlet (GX200 ~19-21, 420cc ~24, EFI TB 28-32)
thickness     = 12;    // spacer thickness; >=10 for nozzle boss
flange_w      = 60;    // overall flange width
flange_h      = 36;
stud_spacing  = 46;    // centre-to-centre of the two carb studs
stud_d        = 6.5;   // M6 clearance
gasket_groove = true;  // 1.6 mm O-ring/gasket groove on both faces
/* [Nozzle] */
nozzle_type   = "nozzle";   // 1/8 NPT nozzle boss (Snow SNO-N0050). Ultrasonic mister option dropped for the bench kit.
nozzle_angle  = 30;    // deg the nozzle axis tilts DOWNSTREAM from the radial plane (spray goes inward and toward the port).
                       // Orientation: z = 0 face = carb/throttle side (upstream), z = thickness face = intake-port side (downstream).
boss_d        = 16;    // >= 2x wall around 1/8 NPT
nozzle_thread_d = 9.7; // pilot = nozzle_thread_d-1 = 8.7 mm -> tap 1/8-27 NPT
egt_port      = false; // spacer does not carry EGT (EGT goes in exhaust flange)
temp_rh_port_d = 0;    // 0 = none; else hole for SHT/BME probe upstream of nozzle
$fn = 72;
module body() {
  difference() {
    hull() for (s=[-1,1]) translate([s*(flange_w/2-flange_h/2),0,0]) cylinder(d=flange_h, h=thickness);
    translate([0,0,-1]) cylinder(d=bore_d, h=thickness+2);
    for (s=[-1,1]) translate([s*stud_spacing/2,0,-1]) cylinder(d=stud_d, h=thickness+2);
    if (gasket_groove) for (z=[-0.01, thickness-1.2]) translate([0,0,z])
      difference(){ cylinder(d=bore_d+7, h=1.21); cylinder(d=bore_d+4, h=1.21); }
    // nozzle passage into bore
    translate([0, -bore_d/2, thickness/2]) rotate([90+nozzle_angle,0,0])  /* CR-006: passage axis points outward and UPSTREAM, so the installed nozzle sprays inward and downstream (+z) */ translate([0,0,-2]) cylinder(d=nozzle_thread_d-1, h=30);
    if (temp_rh_port_d > 0) translate([0, bore_d/2, thickness/2]) rotate([-90,0,0]) cylinder(d=temp_rh_port_d, h=30);
  }
}
module boss() {
  translate([0, -bore_d/2-2, thickness/2]) rotate([90+nozzle_angle,0,0]) difference() {
    cylinder(d=boss_d, h=12); translate([0,0,-1]) cylinder(d=nozzle_thread_d-1, h=14);
  }
}
// boss is clipped flush with both flange faces so it can never stand proud of a gasket face
union(){ body(); intersection(){ boss(); translate([-100,-100,0]) cube([200,200,thickness]); } }
