# Module 06 carburetor sizing

Run `python -m sims.06_carburetor.run --full` and
`python -m pytest tests/test_carburetor.py`. Quick mode uses four rpm rows;
full mode uses seven, each with fifteen manifold-pressure ratios and two
options. The serial algebraic calculation accepts the common `--workers`
argument for `run_all.sh` compatibility. It reads Module 03 JSON files, never
Module 03 Python internals. Missing or unvalidated source results are errors.

The output is a **preliminary sizing model**, with metering validation,
thermal feasibility, and map limitations recorded separately. It is suitable
for concept CAD, not a claim of a calibrated or tested engine. The required
JSON, design-table CSV, operating-map CSV, phi/WFR PNG plots and summary are
written to `results/06_carburetor/`.

## Design basis and metering

The selected source is CH3OH, CR 24, water liquid mass fraction 0.6, intake
temperature setting 360 K and 2000 rpm WOT. Charge masses are scaled by
500 cc / 499.557 cc, then by rpm/120 for a four-stroke single cylinder.
Air demand elsewhere scales linearly with manifold pressure and rpm, holding
the source volumetric-efficiency and temperature effects fixed. This is a
demand envelope, not a new engine simulation or a butterfly-angle map.

Air enters the carburetor at 300 K; heating is downstream. An assumed 180 CAD
intake event per 720 CAD cycle gives a 0.25 flow duty, so venturi and main-jet
event flow is four times mean flow. This simple pulse assumption materially
affects jet dimensions. No booster venturi is assumed. The main venturi is
sized for Mach <= 0.30 at 4000 rpm WOT using the
[NASA compressible isentropic mass-flow relation](https://www.grc.nasa.gov/www/k-12/airplane/mflchk.html)
with Cd 0.95. Inlet and throttle diameters are respectively 1.45 and 1.30
times the throat, chosen as packaging assumptions. Bowl pressure is ambient.

Liquid jet flow includes float lift and a short-bore viscosity correction:

```
dp = signal - rho*g*float_drop
dp = mdot^2/(2*rho*Cd0^2*A^2) + 128*mu*L*mdot/(pi*rho*d^4)
Cd0 = 0.75; L = 1 mm; mdot = 0 when dp <= 0
```

The second term is the Poiseuille bore-loss limit, added to the orifice loss
as an engineering approximation. It is not a measured carburetor Cd(Re)
curve. Effective Cd and main-jet Reynolds numbers are reported. Nominal jet
diameters are rounded to 0.01 mm and re-evaluated before checking AFR. The
needle seat is sized for **mean** maximum demand plus 50% at a regulated
20 kPa supply differential, rounded up to preserve capacity. Bowls buffer
the intake pulses; bowl volume and float dynamics need a later design pass.

The liquid values at approximately 300 K are explicitly rounded estimates:

| Liquid | Density [kg/m3] | Viscosity [mPa s] | Surface tension [N/m] |
|---|---:|---:|---:|
| 40% methanol / 60% water by mass | 930 | 1.60 | 0.035 |
| Methanol | 785 | 0.55 | 0.022 |
| Water | 996.5 | 0.855 | 0.0717 |

The blend density/viscosity estimates are informed by the measured mixture
behavior in [Gonzalez et al. (2007), NIST ThermoML](https://trc.nist.gov/ThermoML/10.1016/j.jct.2007.05.004.html).
They are not represented as a digitized fit to that paper. Surface tensions
are screening assumptions. Properties and discharge coefficients need
measurement at actual bowl temperature before manufacture.

Option A has one premix bowl feeding conventional main and idle/progression
passages. “Single circuit” here means one liquid supply: the jets cannot
independently change WFR. Option B has separate fuel and water bowls,
separate main and idle jets, and a parallel water enrichment jet.

The water valve is fully closed above 25 kPa manifold vacuum, fully open
below 15 kPa and has a linear effective-area transition between them.
The steady-state map assumes the engine is running and warm. A separate
normally closed liquid shutoff must enforce those permissives: low vacuum
alone also occurs with the engine stopped. Base WFR is 0.5 and open-valve
WFR is 1.5. Reducing water at light load is not proof of knock-free operation
at CR 24; Module 03 supplies only the wet WOT design point used here.

For parallel water jets:

```
WFR_main = sum(Cd_w*A_w*opening) / (Cd_f*A_f)
           * sqrt(rho_w*dp_w / (rho_f*dp_f))
```

The effective Cds include the viscosity correction at the evaluated signal.
The specified equal-head formula follows when `dp_w = dp_f`. Equal physical
float drops do not produce equal pressure heads for unlike liquids. The
water float is therefore set to `h_f*rho_f/rho_w`. At idle, the water/fuel
idle passages are evaluated separately; a main-jet formula does not describe
the sum of two passages exposed to different pressure signals.

Idle jets are calibrated at 1000 rpm, manifold pressure 30% of WOT. Their
effective discharge-port exposure tapers linearly to zero at 700 Pa throat
signal. This is a named progression assumption, not a designed air-bleed or
transfer-slot geometry. The full map deliberately reports its mixture
deviations; only the requested design point has a 3% AFR acceptance target.

## Heat and evaporation

The 360 K source setting means **air plus methanol vapour before cold-water
mixing**, not a fully vaporized 360 K cylinder charge. Module 03 reports
T_IVC = 305.66 K and intake water evaporation fraction 0.12444. Two budgets
are therefore provided:

1. Main heat-balance test: vaporize both 300 K liquids and heat all fresh
   intake to 360 K. This is the full-vaporization duty and changes the original
   engine-cycle state; Module 03 would need rerunning for that configuration.
2. Module-03-compatible energy budget: vaporize methanol and heat it and air
   to 360 K, leaving incoming water at 300 K. Subsequent water evaporation is
   supplied by charge cooling as in Module 03. This is an energy comparison,
   not a prediction of selective methanol evaporation from Option A droplets.

Gas sensible enthalpy is integrated from NASA7 polynomials in the exact
mechanism identified by EVO. The narrow reader supports that checked-in
schema and rejects temperatures outside its ranges. It needs no kinetics
solver; input JSON and mechanism SHA256 hashes are recorded. Exhaust mass is
the **fresh charge per cycle**, excluding recirculating residual gas, and
composition is frozen at EVO. There is no combustion or water-energy credit
inside the heat exchanger.

The requested 0.6 effectiveness is applied as a heat-recovery screening
factor to exhaust sensible enthalpy between 877.09 K EVO and a 360 K minimum
outlet. This is a hot-side availability budget, not a solved exchanger with
UA, cold-side capacity rate and pinch. Using EVO directly is optimistic:
blowdown and pipe losses are unresolved. No exhaust condensation is credited.
Latent heats at 300 K are rounded to 2.437 MJ/kg for water and 1.169 MJ/kg for
methanol, consistent with [IAPWS water properties](https://iapws.org/relguide/IAPWS95-2018.pdf)
and [NIST methanol phase-change data](https://webbook.nist.gov/cgi/cbook.cgi?ID=C67561&Mask=4).
Premix heat of mixing is omitted. The results explicitly report a heat
balance failure when available recovery is insufficient; sizing-test success
does not turn that failure into a pass.

Atomization uses the Nukiyama–Tanasawa relation as reproduced in the
[EPA venturi study](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=91016WNN.TXT):

```
d32 [um] = 585/u [m/s] * sqrt(sigma [dyn/cm] / rho [g/cm3])
         + 597*(mu [poise]/sqrt(sigma*rho))^0.45 * (1000*Ql/Qa)^1.5
```

The EPA water example (~107 um at 80.6 m/s and Ql/Qa=0.00133) supplies a unit
conversion regression test. The design-point velocity is below the original
correlation's reported application range, so SMD is only a screening estimate.
Use at least factor-two SMD uncertainty. An isolated-drop, Nu=2,
[heat-limited d-squared law](https://ntrs.nasa.gov/citations/20040084641)
uses `K = 8*k/(rho_l*cp_g)*ln(1+cp_g*(Tgas-Tsurface)/L)` and `t = d32^2/K`.
The assumed surface temperature is 310 K and the heated plenum volume is
1 litre. Residence uses mean total-vapour volume flow at 360 K. Humidity,
preferential evaporation, wall films and convective enhancement are omitted;
the time comparison is not an evaporation guarantee.

## Output interpretation

`validation_passed` and `use_for_design` mean the requested metering checks
pass and the dimensions can feed Module 07 concept CAD. Their scope is
spelled out in `use_for_design_scope`. `heat_balance.passed` is the separate
thermal result; `operating_map.full_map_AFR_within_3pct` describes the whole
map. A runtime exit status of zero means sizing ran and its numerical tests
passed, even when the physical heat-balance conclusion is FAIL.

Plots normally use matplotlib. A Pillow PNG fallback is available in
restricted environments and is identified in the assumptions. All numerical
calculations use the Python standard library. The regression tests need
pytest. CadQuery is not needed for the sizing-to-CAD input-contract check.
