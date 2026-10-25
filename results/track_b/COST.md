# Water Engine - Track B cost metric

Generated 2026-10-25 07:02 PDT by `python -m sims.cost.report` (also run by `python -m sims.track_b.report`). **NOT YET PEER-REVIEW VERIFIED** - Module 03 and M03-CRN are two in-repo engines from the same toolchain; independent engine review (2+ engine rule) still pending.

Rule (James, 2026-10-25 06:53 PDT): gains are judged on cost too. If adding water keeps power (horsepower) the same or better, the fuel it saves per unit work is a cost-per-mile (MPG) gain. Existing result files only - no new combustion runs.

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

## Headline per fuel (lowest cost per mile at equal-or-better power, any regime / mode)

Water priced at retail distilled (1.54 USD/gal). 'w = 0' = no water amount lowers cost at that price. Break-even = the highest water price at which some equal-or-better-power step still lowers cost per mile (M03 / CRN at that step).

| fuel | best cost per mile: where, w | **cost per mile %** (M03 / CRN) | power % (M03 / CRN) | verdict | biggest fuel saving (eff-opt): where, w | fuel per unit work % (M03 / CRN) | cost per mile % there (M03 / CRN) | same, water free % (M03 / CRN) | power % there (M03 / CRN) | break-even water price USD/gal (M03 / CRN), where, w |
|---|---|---|---|---|---|---|---|---|---|---|
| PRF87 | normal / liquid, 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | normal / liquid, 0.100 | -1.416 / -1.397 | +1.304 / +1.323 | -1.416 / -1.397 | +3.352 / +3.332 | 0.91 / 0.90, normal / liquid, 0.002 |
| PRF91 | normal / liquid, 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | normal / liquid, 0.100 | -1.014 / -0.992 | +1.719 / +1.741 | -1.014 / -0.992 | +2.933 / +2.910 | 0.84 / 0.84, hot/H1 / liquid, 0.003 |
| PRF97 | normal / liquid, 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | normal / liquid, 0.100 | -1.016 / -0.997 | +1.242 / +1.261 | -1.016 / -0.997 | +2.935 / +2.915 | 0.81 / 0.79, normal / liquid, 0.001 |
| E10 | normal / liquid, 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | normal / liquid, 0.100 | -1.133 / -1.113 | +1.635 / +1.656 | -1.133 / -1.113 | +3.144 / +3.123 | 0.73 / 0.72, normal / liquid, 0.003 |
| E85 | normal / liquid, 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | normal / liquid, 0.100 | -1.753 / -1.719 | +2.130 / +2.166 | -1.753 / -1.719 | +4.678 / +4.642 | 0.80 / 0.79, normal / liquid, 0.003 |
| CH3OH | hot/H1 / humid_evap, 0.043 | -0.420 / -0.388 | +4.293 / +4.259 | COST GAIN | normal / liquid, 0.132 | -2.452 / -2.417 | +1.718 / +1.754 | -2.452 / -2.417 | +8.445 / +8.407 | 2.59 / 2.56, hot/H1 / liquid, 0.001 |
| C2H5OH | normal / liquid, 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | hot / humid_evap, 0.288 | -4.389 / -4.380 | +19.758 / +19.769 | -4.389 / -4.380 | +26.023 / +26.011 | 0.79 / 0.78, hot / liquid, 0.003 |
| CH4 | normal / liquid, 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | hot / humid_evap, 0.110 | -1.174 / -1.135 | +2.949 / +2.989 | -1.174 / -1.135 | +4.159 / +4.119 | 0.58 / 0.56, hot / liquid, 0.001 |

## Every chain (both engines side by side)

| fuel | regime | mode | point | w | d_eta pp (M03 / CRN) | power (IMEP) % (M03 / CRN) | fuel volume per unit work % (M03 / CRN) | **cost per mile %** (M03 / CRN) | cost/mile if water free % (M03) | verdict | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PRF87 | normal | liquid | eff-opt | 0.100 | +0.533 / +0.526 | +3.352 / +3.332 | -1.416 / -1.397 | +1.304 / +1.323 | -1.416 | fuel saved, but water cost eats it | stopped |
| PRF87 | normal | liquid | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF87 | normal | humid_evap | eff-opt | 0.100 | +0.468 / +0.466 | +5.167 / +5.160 | -1.247 / -1.239 | +1.478 / +1.485 | -1.247 | fuel saved, but water cost eats it | stopped |
| PRF87 | normal | humid_evap | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF87 | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| PRF87 | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF87 | hot (H1 low-CR) | liquid | eff-opt | 0.022 | +0.076 / +0.074 | +0.515 / +0.510 | -0.224 / -0.219 | +0.333 / +0.338 | -0.224 | fuel saved, but water cost eats it | stopped |
| PRF87 | hot (H1 low-CR) | liquid | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF87 | hot (H1 low-CR) | humid_evap | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| PRF87 | hot (H1 low-CR) | humid_evap | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF87 | hot (H1 low-CR) | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| PRF87 | hot (H1 low-CR) | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF91 | normal | liquid | eff-opt | 0.100 | +0.384 / +0.376 | +2.933 / +2.910 | -1.014 / -0.992 | +1.719 / +1.741 | -1.014 | fuel saved, but water cost eats it | stopped |
| PRF91 | normal | liquid | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF91 | normal | humid_evap | eff-opt | 0.100 | +0.371 / +0.369 | +4.882 / +4.877 | -0.978 / -0.973 | +1.755 / +1.761 | -0.978 | fuel saved, but water cost eats it | stopped |
| PRF91 | normal | humid_evap | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF91 | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| PRF91 | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF91 | hot (H1 low-CR) | liquid | eff-opt | 0.064 | +0.308 / +0.306 | +1.776 / +1.769 | -0.873 / -0.866 | +0.811 / +0.818 | -0.873 | fuel saved, but water cost eats it | in progress (step 64) |
| PRF91 | hot (H1 low-CR) | liquid | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF91 | hot (H1 low-CR) | humid_evap | eff-opt | 0.078 | +0.325 / +0.327 | +3.176 / +3.181 | -0.919 / -0.923 | +1.164 / +1.160 | -0.919 | fuel saved, but water cost eats it | in progress (step 78) |
| PRF91 | hot (H1 low-CR) | humid_evap | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF91 | hot (H1 low-CR) | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| PRF91 | hot (H1 low-CR) | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF97 | normal | liquid | eff-opt | 0.100 | +0.396 / +0.388 | +2.935 / +2.915 | -1.016 / -0.997 | +1.242 / +1.261 | -1.016 | fuel saved, but water cost eats it | stopped |
| PRF97 | normal | liquid | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF97 | normal | humid_evap | eff-opt | 0.100 | +0.380 / +0.378 | +4.881 / +4.876 | -0.977 / -0.972 | +1.282 / +1.287 | -0.977 | fuel saved, but water cost eats it | stopped |
| PRF97 | normal | humid_evap | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF97 | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| PRF97 | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF97 | hot (H1 low-CR) | liquid | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| PRF97 | hot (H1 low-CR) | liquid | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF97 | hot (H1 low-CR) | humid_evap | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| PRF97 | hot (H1 low-CR) | humid_evap | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| PRF97 | hot (H1 low-CR) | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| PRF97 | hot (H1 low-CR) | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| E10 | normal | liquid | eff-opt | 0.100 | +0.441 / +0.433 | +3.144 / +3.123 | -1.133 / -1.113 | +1.635 / +1.656 | -1.133 | fuel saved, but water cost eats it | stopped |
| E10 | normal | liquid | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| E10 | normal | humid_evap | eff-opt | 0.100 | +0.416 / +0.413 | +5.161 / +5.154 | -1.069 / -1.063 | +1.701 / +1.708 | -1.069 | fuel saved, but water cost eats it | stopped |
| E10 | normal | humid_evap | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| E10 | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| E10 | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| E10 | hot (H1 low-CR) | liquid | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| E10 | hot (H1 low-CR) | liquid | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| E10 | hot (H1 low-CR) | humid_evap | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| E10 | hot (H1 low-CR) | humid_evap | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| E10 | hot (H1 low-CR) | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| E10 | hot (H1 low-CR) | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| E85 | normal | liquid | eff-opt | 0.100 | +0.723 / +0.710 | +4.678 / +4.642 | -1.753 / -1.719 | +2.130 / +2.166 | -1.753 | fuel saved, but water cost eats it | stopped |
| E85 | normal | liquid | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| E85 | normal | humid_evap | eff-opt | 0.100 | +0.676 / +0.666 | +7.630 / +7.602 | -1.640 / -1.614 | +2.249 / +2.275 | -1.640 | fuel saved, but water cost eats it | stopped |
| E85 | normal | humid_evap | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| E85 | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| E85 | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| E85 | hot | liquid | eff-opt | 0.096 | +0.410 / +0.400 | +3.183 / +3.157 | -1.073 / -1.048 | +2.665 / +2.691 | -1.073 | fuel saved, but water cost eats it | stopped |
| E85 | hot | liquid | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| E85 | hot | humid_evap | eff-opt | 0.100 | +0.454 / +0.453 | +5.712 / +5.709 | -1.186 / -1.183 | +2.720 / +2.723 | -1.186 | fuel saved, but water cost eats it | stopped |
| E85 | hot | humid_evap | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| E85 | hot | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| E85 | hot | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| CH3OH | normal | liquid | eff-opt | 0.132 | +1.065 / +1.050 | +8.445 / +8.407 | -2.452 / -2.417 | +1.718 / +1.754 | -2.452 | fuel saved, but water cost eats it | stopped |
| CH3OH | normal | liquid | cost-opt | 0.025 | +0.364 / +0.359 | +1.796 / +1.784 | -0.852 / -0.841 | -0.137 / -0.126 | -0.852 | COST GAIN |  |
| CH3OH | normal | humid_evap | eff-opt | 0.080 | +0.873 / +0.860 | +8.373 / +8.342 | -2.018 / -1.990 | +0.377 / +0.406 | -2.018 | fuel saved, but water cost eats it | stopped |
| CH3OH | normal | humid_evap | cost-opt | 0.032 | +0.463 / +0.458 | +3.551 / +3.538 | -1.081 / -1.068 | -0.162 / -0.149 | -1.081 | COST GAIN |  |
| CH3OH | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| CH3OH | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| CH3OH | hot (H1 low-CR) | liquid | eff-opt | 0.056 | +0.685 / +0.666 | +3.663 / +3.607 | -1.919 / -1.866 | -0.284 / -0.230 | -1.919 | COST GAIN | in progress (step 56) |
| CH3OH | hot (H1 low-CR) | liquid | cost-opt | 0.039 | +0.544 / +0.532 | +2.710 / +2.676 | -1.530 / -1.497 | -0.407 / -0.374 | -1.530 | COST GAIN |  |
| CH3OH | hot (H1 low-CR) | humid_evap | eff-opt | 0.067 | +0.784 / +0.763 | +6.495 / +6.432 | -2.191 / -2.133 | -0.217 / -0.157 | -2.191 | COST GAIN | in progress (step 67) |
| CH3OH | hot (H1 low-CR) | humid_evap | cost-opt | 0.043 | +0.592 / +0.580 | +4.293 / +4.259 | -1.662 / -1.630 | -0.420 / -0.388 | -1.662 | COST GAIN |  |
| CH3OH | hot (H1 low-CR) | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| CH3OH | hot (H1 low-CR) | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| C2H5OH | normal | liquid | eff-opt | 0.173 | +0.765 / +0.754 | +7.794 / +7.767 | -1.688 / -1.663 | +11.153 / +11.181 | -1.688 | fuel saved, but water cost eats it | stopped |
| C2H5OH | normal | liquid | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| C2H5OH | normal | humid_evap | eff-opt | 0.101 | +0.556 / +0.548 | +7.737 / +7.720 | -1.231 / -1.216 | +5.697 / +5.714 | -1.231 | fuel saved, but water cost eats it | stopped |
| C2H5OH | normal | humid_evap | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| C2H5OH | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| C2H5OH | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| C2H5OH | hot | liquid | eff-opt | 0.096 | +0.857 / +0.837 | +4.493 / +4.441 | -2.152 / -2.103 | +4.336 / +4.388 | -2.152 | fuel saved, but water cost eats it | stopped |
| C2H5OH | hot | liquid | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| C2H5OH | hot | humid_evap | eff-opt | 0.288 | +1.789 / +1.785 | +26.023 / +26.011 | -4.389 / -4.380 | +19.758 / +19.769 | -4.389 | fuel saved, but water cost eats it | stopped |
| C2H5OH | hot | humid_evap | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| C2H5OH | hot | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| C2H5OH | hot | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| CH4 | normal | liquid | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| CH4 | normal | liquid | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| CH4 | normal | humid_evap | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| CH4 | normal | humid_evap | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| CH4 | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| CH4 | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| CH4 | hot | liquid | eff-opt | 0.085 | +0.369 / +0.356 | +1.990 / +1.956 | -0.889 / -0.857 | +2.219 / +2.252 | -0.889 | fuel saved, but water cost eats it | stopped |
| CH4 | hot | liquid | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| CH4 | hot | humid_evap | eff-opt | 0.110 | +0.489 / +0.474 | +4.159 / +4.119 | -1.174 / -1.135 | +2.949 / +2.989 | -1.174 | fuel saved, but water cost eats it | stopped |
| CH4 | hot | humid_evap | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |
| CH4 | hot | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain | stopped |
| CH4 | hot | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 | no cost gain |  |

## Caveats carried over (still apply to every cost number)

* **Fixed burn duration model gap.** Module 03 holds the 10-90 % burn duration essentially fixed as water is
  added (flame-speed fits only reduce S_L; the burn-duration penalty of water dilution measured in engines is not
  reproduced). The B1 sign test (spark held at the dry setting) still gains, while published engine tests lose
  efficiency at fixed timing, so every efficiency - and therefore every fuel-saving and cost gain - here is an
  **upper bound**.
* **Knock is modelled only in Module 03.** M03-CRN has no knock model; it re-runs the Module 03 spark timing. The
  part of a gain that comes from knock relief therefore rests on one engine.
* **Lower bounds at w = 0.10 for the gasoline blends** (PRF87/91/97, E10, E85): those chains stop at the end of the
  flame-speed fit validity (w <= 0.10), not because the gain ran out, so their cost gains could be larger.
* No gas-exchange / friction model: power is IMEP (indicated). Brake power is not modelled; at equal speed and
  friction the brake-power change has the same sign and a larger % magnitude.
* Absolute $/mile is NOT comparable across fuels (road fuels at retail, alcohols at wholesale, CNG quarterly
  retail). Compare each fuel only with its own dry baseline (the % columns).

