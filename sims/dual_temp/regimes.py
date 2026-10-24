"""Dual-temperature regimes for every WME-1 combustion simulation (James's standing rule, 2026-10-24).

NORMAL  = typical production engine, warmed up.
HOT     = high-performance / hot-running engine (hotter coolant, walls, ports and intake charge).

Sources (see docs/DUAL_TEMPERATURE_RULE.md for the full table):
  coolant 85-95 C full load, 95-110 C part load with mapped cooling; pressurised systems boil at 115-130 C
    -- MAHLE "Vehicle cooling" compact knowledge (VW SSP 222);  SAE 960271 (part-load coolant 110 C, 1-3 % fuel saving)
  chamber gas-side wall 450 K -- SPEC section 6 (Woschni wall temperature); 520 K hot = +70 K for 115 C coolant and a
    hotter-running head (still inside the usual 400-600 K gas-side range, Heywood ICE Fundamentals ch. 12)
  intake charge 320/360 K normal (Module 03 sweep); 400 K hot (un-intercooled boost / heated intake; Module 09 sweeps 320-420 K)
  intake-port wall ~ coolant temperature: 363 K normal, 388 K hot; 420 K = heated port / hot-spot variant
"""
NORMAL = dict(name="normal", coolant_K=363.15, chamber_wall_K=450.0, T_intake_K=(320.0, 360.0),
              port_wall_K=363.15)
HOT = dict(name="hot", coolant_K=388.15, chamber_wall_K=520.0, T_intake_K=(320.0, 360.0, 400.0),
           port_wall_K=388.15, heated_port_wall_K=420.0)
REGIMES = {"normal": NORMAL, "hot": HOT}
