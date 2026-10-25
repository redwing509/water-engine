# Water Engine - Track A cost metric

Generated 2026-10-25 07:02 PDT by `python -m sims.cost.report`. **NOT YET PEER-REVIEW VERIFIED** - Module 03 and M03-CRN are two in-repo engines from the same toolchain; independent engine review (2+ engine rule) still pending.

Track A = water-majority work (w = 0.5-0.8). Source: `results/track_b/trackA_humid_grid.json` (Module 03 dual-regime rerun, 3 water modes, CR 12-24; **single engine - no M03-CRN values saved**, so every verdict is labelled 1 engine). Dry reference = best eligible dry point of the same fuel and regime (Track B continuous spark optimiser; hot CH3OH has none in CR 9-24, so the H1 low-CR hot baseline is used). Wet and dry points are at their own best CR (best-dry-engine vs best-wet-engine, as Track A has always been compared).

## Method (how fuel use per unit work is defined)

* w = m_water/(m_water + m_fuel); water per kg fuel r = w/(1-w) (checked against the saved masses for every row).
* The charge is stoichiometric on the fuel; water is **added**, it does not replace fuel inside the
  stoichiometric mix. What water "displaces" is fuel **per unit of work**: efficiency is
  eta = W_ind / (m_fuel x LHV_fuel) (water has no heating value and is not in the denominator), so
  fuel energy, mass and volume per unit work all change by **eta_dry/eta - 1** vs the same fuel's dry baseline.
* Power = IMEP (Module 03 `IMEP_Pa`; M03-CRN IMEP derived as IMEP_M03 x eta_CRN/eta_M03 at the same fuel mass).
  Equal-or-better = IMEP change >= -0.01 % (the 3.3e-5 efficiency noise level is ~1e-4 relative).
* Cost per kWh of indicated work = (p_fuel + r x p_water) / (eta x LHV); cost per mile = that x
  0.4 kWh indicated work per mile (reference vehicle: 30 mpg gasoline car, 33.7 kWh/gal / 30 x ~0.35
  indicated efficiency). The % changes do not depend on the vehicle; they are the primary numbers.
* **Verdict COST GAIN** = power equal or better in every engine AND cost per mile lower by more than
  0.01 % in every engine (Track B: both engines; Track A grid: Module 03 only, labelled).
* Two points per chain: **eff-opt** = the best-efficiency point the Track B rule accepted; **cost-opt** = the
  water fraction with the lowest cost per mile among points with equal-or-better power (w = 0 means water never pays).

## Prices used (dated, cited; `sims/cost/prices_20261025.json`)

| key | price | basis | date | source |
|---|---|---|---|---|
| gasoline_regular | 4.2892 USD/US gal | US retail national average, regular unleaded (in practice E10) | 2026-10-25 | [AAA Gas Prices, national average](https://gasprices.aaa.com/) |
| gasoline_premium | 5.1972 USD/US gal | US retail national average, premium | 2026-10-25 | [AAA Gas Prices, national average](https://gasprices.aaa.com/) |
| e85 | 3.3585 USD/US gal | US retail national average, E85 | 2026-10-25 | [AAA Gas Prices, national average](https://gasprices.aaa.com/) |
| diesel | 6.3474 USD/US gal | US retail national average, diesel (reference only; no diesel fuel is modelled) | 2026-10-25 | [AAA Gas Prices, national average](https://gasprices.aaa.com/) |
| methanol | 1450.0 USD/metric ton | Methanex North America Non-Discounted Reference Price (wholesale contract), valid 2026-10-01..2026-10-31, posted 2026-09-29 | 2026-10-01 | [Methanex posted prices](https://www.methanex.com/about-methanol/pricing/) |
| ethanol | 1.94 USD/US gal | USDA AMS National Weekly Ethanol Report, Iowa ethanol plant FOB truck average, week 2026-10-19..2026-10-23 (wholesale fuel ethanol; denaturant ignored) | 2026-10-23 | [USDA AMS Livestock, Poultry & Grain Market News report 3616](https://www.ams.usda.gov/mnreports/ams_3616.pdf) |
| cng | 3.1 USD/GGE | US national average retail CNG, Clean Cities Alternative Fuel Price Report July 2026 (latest quarterly issue; prices reported 2026-07-01..31). 1 GGE of CNG = 5.660 lb (NIST Handbook 44 Appendix D). Methane (CH4) is priced as CNG. | 2026-07-31 | [US DOE Alternative Fuels Data Center](https://afdc.energy.gov/fuels/prices) |
| water_distilled | 1.54 USD/US gal | Retail distilled water, Great Value 1 gal jug (conservative: bulk deionised/tap water is far cheaper; the free-water bound is also reported) | 2026-10-25 | [Walmart.com product listing](https://www.walmart.com/ip/Great-Value-Distilled-Water-1-Gallon/17501951806) |

Fuel -> price: PRF87 = gasoline_regular, PRF91 = gasoline_regular, E10 = gasoline_regular, PRF97 = gasoline_premium, E85 = e85, CH3OH = methanol, C2H5OH = ethanol, CH4 = cng. PRF87/PRF91 surrogates of US regular and E10 are priced as AAA regular (US regular is E10); PRF97 (premium surrogate) as AAA premium; E85 as AAA E85. USD/kg: PRF87 1.641, PRF91 1.640, E10 1.617, PRF97 1.985, E85 1.146, CH3OH 1.450, C2H5OH 0.653, CH4 1.207, water 0.408.

## Track A grid (Module 03)

| fuel | regime | mode | point | CR / T_intake / w | d_eta pp (M03) | power % | fuel volume per unit work % | **cost per mile %** | cost/mile if water free % | verdict | dry reference |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CH3OH | normal | liquid | eff-opt | 24 / 360 / 0.50 | +2.458 | +4.73 | -5.48 | +21.08 | -5.48 | fuel saved, but water cost eats it (1 engine) | Track B dry sweep CR 9-24: CR 17, eta 0.4238 |
| CH3OH | normal | liquid | cost-opt | 17 / 320 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 17, eta 0.4238 |
| CH3OH | normal | humid_evap | eff-opt | 24 / 360 / 0.50 | +2.458 | +4.73 | -5.48 | +21.08 | -5.48 | fuel saved, but water cost eats it (1 engine) | Track B dry sweep CR 9-24: CR 17, eta 0.4238 |
| CH3OH | normal | humid_evap | cost-opt | 17 / 320 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 17, eta 0.4238 |
| CH3OH | normal | humid_ambient | eff-opt | 24 / 320 / 0.50 | +2.825 | -5.13 | -6.25 | +20.10 | -6.25 | power loss (1 engine) | Track B dry sweep CR 9-24: CR 17, eta 0.4238 |
| CH3OH | normal | humid_ambient | cost-opt | 17 / 320 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 17, eta 0.4238 |
| CH3OH | hot | liquid | eff-opt | 24 / 400 / 0.50 | +10.461 | +42.95 | -23.00 | -1.36 | -23.00 | COST GAIN (1 engine) | H1 low-CR CR 6-8: CR 8, eta 0.3502 |
| CH3OH | hot | liquid | cost-opt | 24 / 400 / 0.50 | +10.461 | +42.95 | -23.00 | -1.36 | -23.00 | COST GAIN (1 engine) | H1 low-CR CR 6-8: CR 8, eta 0.3502 |
| CH3OH | hot | humid_evap | eff-opt | 24 / 400 / 0.50 | +10.461 | +42.95 | -23.00 | -1.36 | -23.00 | COST GAIN (1 engine) | H1 low-CR CR 6-8: CR 8, eta 0.3502 |
| CH3OH | hot | humid_evap | cost-opt | 24 / 400 / 0.50 | +10.461 | +42.95 | -23.00 | -1.36 | -23.00 | COST GAIN (1 engine) | H1 low-CR CR 6-8: CR 8, eta 0.3502 |
| CH3OH | hot | humid_ambient | - | no eligible wet point | | | | | | | |
| C2H5OH | normal | liquid | eff-opt | 24 / 360 / 0.50 | +0.685 | +2.41 | -1.51 | +59.98 | -1.51 | fuel saved, but water cost eats it (1 engine) | Track B dry sweep CR 9-24: CR 24, eta 0.4458 |
| C2H5OH | normal | liquid | cost-opt | 24 / 320 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 24, eta 0.4458 |
| C2H5OH | normal | humid_evap | eff-opt | 24 / 360 / 0.50 | +0.685 | +2.41 | -1.51 | +59.98 | -1.51 | fuel saved, but water cost eats it (1 engine) | Track B dry sweep CR 9-24: CR 24, eta 0.4458 |
| C2H5OH | normal | humid_evap | cost-opt | 24 / 320 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 24, eta 0.4458 |
| C2H5OH | normal | humid_ambient | eff-opt | 24 / 320 / 0.50 | +0.259 | -9.14 | -0.58 | +61.50 | -0.58 | power loss (1 engine) | Track B dry sweep CR 9-24: CR 24, eta 0.4458 |
| C2H5OH | normal | humid_ambient | cost-opt | 24 / 320 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 24, eta 0.4458 |
| C2H5OH | hot | liquid | eff-opt | 24 / 400 / 0.50 | +6.703 | +35.07 | -14.68 | +38.60 | -14.68 | fuel saved, but water cost eats it (1 engine) | Track B dry sweep CR 9-24: CR 12, eta 0.3897 |
| C2H5OH | hot | liquid | cost-opt | 12 / 400 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 12, eta 0.3897 |
| C2H5OH | hot | humid_evap | eff-opt | 24 / 400 / 0.50 | +6.703 | +35.07 | -14.68 | +38.60 | -14.68 | fuel saved, but water cost eats it (1 engine) | Track B dry sweep CR 9-24: CR 12, eta 0.3897 |
| C2H5OH | hot | humid_evap | cost-opt | 12 / 400 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 12, eta 0.3897 |
| C2H5OH | hot | humid_ambient | eff-opt | 12 / 400 / 0.50 | +0.072 | -13.52 | -0.18 | +62.14 | -0.18 | power loss (1 engine) | Track B dry sweep CR 9-24: CR 12, eta 0.3897 |
| C2H5OH | hot | humid_ambient | cost-opt | 12 / 400 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 12, eta 0.3897 |
| CH4 | normal | liquid | eff-opt | 24 / 320 / 0.50 | +1.461 | +10.21 | -3.22 | +29.45 | -3.22 | fuel saved, but water cost eats it (1 engine) | Track B dry sweep CR 9-24: CR 24, eta 0.4397 |
| CH4 | normal | liquid | cost-opt | 24 / 320 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 24, eta 0.4397 |
| CH4 | normal | humid_evap | eff-opt | 24 / 320 / 0.50 | +1.461 | +10.21 | -3.22 | +29.45 | -3.22 | fuel saved, but water cost eats it (1 engine) | Track B dry sweep CR 9-24: CR 24, eta 0.4397 |
| CH4 | normal | humid_evap | cost-opt | 24 / 320 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 24, eta 0.4397 |
| CH4 | normal | humid_ambient | eff-opt | 24 / 320 / 0.70 | +0.119 | -9.44 | -0.27 | +78.27 | -0.27 | power loss (1 engine) | Track B dry sweep CR 9-24: CR 24, eta 0.4397 |
| CH4 | normal | humid_ambient | cost-opt | 24 / 320 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 24, eta 0.4397 |
| CH4 | hot | liquid | eff-opt | 24 / 400 / 0.60 | +3.888 | +30.58 | -8.63 | +37.63 | -8.63 | fuel saved, but water cost eats it (1 engine) | Track B dry sweep CR 9-24: CR 18, eta 0.4118 |
| CH4 | hot | liquid | cost-opt | 18 / 400 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 18, eta 0.4118 |
| CH4 | hot | humid_evap | eff-opt | 24 / 400 / 0.60 | +3.890 | +30.75 | -8.63 | +37.63 | -8.63 | fuel saved, but water cost eats it (1 engine) | Track B dry sweep CR 9-24: CR 18, eta 0.4118 |
| CH4 | hot | humid_evap | cost-opt | 18 / 400 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 18, eta 0.4118 |
| CH4 | hot | humid_ambient | eff-opt | 20 / 400 / 0.60 | -0.042 | -11.38 | +0.10 | +50.78 | +0.10 | power loss (1 engine) | Track B dry sweep CR 9-24: CR 18, eta 0.4118 |
| CH4 | hot | humid_ambient | cost-opt | 18 / 400 / 0.00 | +0.000 | +0.00 | +0.00 | +0.00 | +0.00 | no cost gain (1 engine) | Track B dry sweep CR 9-24: CR 18, eta 0.4118 |

## Caveats carried over (still apply to every cost number)

* **Fixed burn duration model gap.** Module 03 holds the 10-90 % burn duration essentially fixed as water is
  added (flame-speed fits only reduce S_L; the burn-duration penalty of water dilution measured in engines is not
  reproduced). The B1 sign test (spark held at the dry setting) still gains, while published engine tests lose
  efficiency at fixed timing, so every efficiency - and therefore every fuel-saving and cost gain - here is an
  **upper bound**.
* **Knock is modelled only in Module 03.** M03-CRN has no knock model; it re-runs the Module 03 spark timing. The
  part of a gain that comes from knock relief therefore rests on one engine.
* (Track B only) **Lower bounds at w = 0.10 for the gasoline blends** (PRF87/91/97, E10, E85): those chains stop at the end of the
  flame-speed fit validity (w <= 0.10), not because the gain ran out, so their cost gains could be larger.
* No gas-exchange / friction model: power is IMEP (indicated). Brake power is not modelled; at equal speed and
  friction the brake-power change has the same sign and a larger % magnitude.
* Absolute $/mile is NOT comparable across fuels (road fuels at retail, alcohols at wholesale, CNG quarterly
  retail). Compare each fuel only with its own dry baseline (the % columns).

