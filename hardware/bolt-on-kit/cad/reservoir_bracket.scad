// Reservoir + pump bracket for a 1-2 L HDPE bottle on a generator frame tube (Grok Bot 2026-10-29). PETG ok (cool side, away from exhaust).
tube_d = 25.4; bottle_d = 90; pump_w = 40; pump_l = 60; wall = 4; width = 30; $fn = 64;
difference(){ union(){
  cylinder(d=tube_d+2*wall, h=width);                                  // frame clamp
  translate([tube_d/2, -wall, 0]) cube([40, 2*wall, width]);           // arm
  translate([tube_d/2+40+bottle_d/2, 0, 0]) cylinder(d=bottle_d+2*wall, h=width); // bottle ring
  translate([tube_d/2+10, wall, 0]) cube([pump_l, pump_w/2, wall]);    // pump shelf
 }
 translate([0,0,-1]) cylinder(d=tube_d, h=width+2);
 translate([-tube_d, -1, -1]) cube([tube_d, 2, width+2]);              // clamp slot (M5 pinch bolt)
 translate([-tube_d/2-wall, 0, width/2]) rotate([90,0,0]) cylinder(d=5.5, h=40, center=true);
 translate([tube_d/2+40+bottle_d/2, 0, -1]) cylinder(d=bottle_d, h=width+2);
}
