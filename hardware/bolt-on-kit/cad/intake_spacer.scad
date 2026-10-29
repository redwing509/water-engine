// Water-injection intake spacer, parametric (Grok Bot 2026-10-29). Sits between carb/throttle body and intake port
// (or between air filter and carb on engines with no room). Print in ASA or PA12-CF (see SPEC.md 2.2). Units mm.
/* [Bore / flange] */
bore_d        = 24;    // venturi-side bore, match carb outlet (GX200 ~19-21, 420cc ~24, EFI TB 28-32)
thickness     = 12;    // spacer thickness; >=10 for nozzle boss
flange_w      = 60;    // overall flange width
flange_h      = 36;
stud_spacing  = 46;    // centre-to-centre of the two carb studs
stud_d        = 6.5;   // M6 clearance
gasket_groove = true;  // 1.6 mm O-ring/gasket groove on both faces
/* [Nozzle] */
nozzle_type   = "mister";   // "mister" = 16/20 mm ultrasonic disc pocket upstream; "nozzle" = 1/8 NPT / M8 fine nozzle boss
nozzle_angle  = 30;    // deg from bore axis, pointing downstream
boss_d        = 14;
nozzle_thread_d = 8.0; // M8x1 tap drill 7.0 -> print 7.0, tap after; or heat-set brass insert
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
    translate([0, -bore_d/2, thickness/2]) rotate([90-nozzle_angle,0,0]) translate([0,0,-2]) cylinder(d=nozzle_thread_d-1, h=30);
    if (temp_rh_port_d > 0) translate([0, bore_d/2, thickness/2]) rotate([-90,0,0]) cylinder(d=temp_rh_port_d, h=30);
  }
}
module boss() {
  translate([0, -bore_d/2-2, thickness/2]) rotate([90-nozzle_angle,0,0]) difference() {
    cylinder(d=boss_d, h=12); translate([0,0,-1]) cylinder(d=nozzle_thread_d-1, h=14);
  }
}
union(){ body(); boss(); }
