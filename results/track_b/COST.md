# Water Engine - Track B cost metric

Generated 2026-10-25 07:35 PDT by `python -m sims.cost.report` (also run by `python -m sims.track_b.report`). **NOT YET PEER-REVIEW VERIFIED** - Module 03 and M03-CRN are two in-repo engines from the same toolchain; independent engine review (2+ engine rule) still pending.

Rule (James, 2026-10-25 06:53 PDT): gains are judged on cost too. If adding water keeps power (horsepower) the same or better, the fuel it saves per unit work is a cost-per-mile (MPG) gain. Existing result files only - no new combustion runs.

## Method (how fuel use per unit work is defined)

* w = m_water/(m_water + m_fuel); water per kg fuel r = w/(1-w) (checked against the saved masses for every row).
* The charge is stoichiometric on the fuel; water is **added**, it does not replace fuel inside the
  stoichiometric mix. What water "displaces" is fuel **per unit of work**: efficiency is
  eta = W_ind / (m_fuel x LHV_fuel) (water has no heating value and is not in the denominator), so
  fuel energy, mass and volume per unit work all change by **eta_dry/eta - 1** vs the same fuel's dry baseline.
* Power = IMEP (Module 03 `IMEP_Pa`; M03-CRN IMEP derived as IMEP_M03 x eta_CRN/eta_M03 at the same fuel mass).
  Equal-or-better = IMEP change >= -0.01 % (the 3.3e-5 efficiency noise level is ~1e-4 relative).
* **Water price.** Headline/default = **0.10 USD/gal, James's chosen test-case water cost** (2026-10-25 07:32 PDT).
  Secondary comparison = **0 USD/gal** (free tap water; James 07:31 PDT: most people pay for water through the
  utility bill and have no extra cost to fill a tank of water). Retail distilled water (1.54 USD/gal) is only a
  footnote sensitivity. With free water the cost change equals the fuel-per-work change, so the cost optimum is the
  efficiency optimum wherever power holds.
* Cost per kWh of indicated work = (p_fuel + r x p_water) / (eta x LHV); cost per mile = that x
  0.4 kWh indicated work per mile (reference vehicle: 30 mpg gasoline car, 33.7 kWh/gal / 30 x ~0.35
  indicated efficiency). The % changes do not depend on the vehicle; they are the primary numbers.
* **Verdict COST GAIN** (at the headline 0.10 USD/gal) = power equal or better in every engine AND cost per mile lower by more than
  0.01 % in every engine (Track B: both engines; Track A grid: Module 03 only, labelled).
* Points per chain: **eff-opt** = the best-efficiency point the Track B rule accepted; **cost-opt** = the water
  fraction with the lowest cost per mile at 0.10 USD/gal among computed points with equal-or-better power in both
  engines (w = 0 means water never pays); **cost-opt $0** = the same at free water. A cost-opt one step past eff-opt
  is the first rejected step (gain positive but below the 3.3e-5 noise threshold) - equal within noise.

## Prices used (dated, cited; `sims/cost/prices_20261025.json`)

| key | price | basis | date | source |
|---|---|---|---|---|
| water_test_case | 0.1 USD/US gal | HEADLINE / default. James's chosen test-case water cost for the Water Engine cost metric (decision 2026-10-25 07:32 PDT; he first set water free at 07:31 PDT because most people pay for water through the utility bill and have no extra cost to fill a tank of water). A stated assumption chosen by the project owner, not a market quote. | 2026-10-25 | James (project owner) decision, chat 2026-10-25 07:32 PDT |
| water_free | 0.0 USD/US gal | Secondary comparison: free tap water (James 2026-10-25 07:31 PDT: water already paid through the utility bill, no extra cost to fill a tank). | 2026-10-25 | James (project owner) decision, chat 2026-10-25 07:31 PDT |
| gasoline_regular | 4.2892 USD/US gal | US retail national average, regular unleaded (in practice E10) | 2026-10-25 | [AAA Gas Prices, national average](https://gasprices.aaa.com/) |
| gasoline_premium | 5.1972 USD/US gal | US retail national average, premium | 2026-10-25 | [AAA Gas Prices, national average](https://gasprices.aaa.com/) |
| e85 | 3.3585 USD/US gal | US retail national average, E85 | 2026-10-25 | [AAA Gas Prices, national average](https://gasprices.aaa.com/) |
| diesel | 6.3474 USD/US gal | US retail national average, diesel (reference only; no diesel fuel is modelled) | 2026-10-25 | [AAA Gas Prices, national average](https://gasprices.aaa.com/) |
| methanol | 1450.0 USD/metric ton | Methanex North America Non-Discounted Reference Price (wholesale contract), valid 2026-10-01..2026-10-31, posted 2026-09-29 | 2026-10-01 | [Methanex posted prices](https://www.methanex.com/about-methanol/pricing/) |
| ethanol | 1.94 USD/US gal | USDA AMS National Weekly Ethanol Report, Iowa ethanol plant FOB truck average, week 2026-10-19..2026-10-23 (wholesale fuel ethanol; denaturant ignored) | 2026-10-23 | [USDA AMS Livestock, Poultry & Grain Market News report 3616](https://www.ams.usda.gov/mnreports/ams_3616.pdf) |
| cng | 3.1 USD/GGE | US national average retail CNG, Clean Cities Alternative Fuel Price Report July 2026 (latest quarterly issue; prices reported 2026-07-01..31). 1 GGE of CNG = 5.660 lb (NIST Handbook 44 Appendix D). Methane (CH4) is priced as CNG. | 2026-07-31 | [US DOE Alternative Fuels Data Center](https://afdc.energy.gov/fuels/prices) |
| water_distilled | 1.54 USD/US gal | FOOTNOTE SENSITIVITY ONLY (not a headline case). Retail distilled water, Great Value 1 gal jug (conservative: bulk deionised/tap water is far cheaper; the free-water bound is also reported) | 2026-10-25 | [Walmart.com product listing](https://www.walmart.com/ip/Great-Value-Distilled-Water-1-Gallon/17501951806) |

Fuel -> price: PRF87 = gasoline_regular, PRF91 = gasoline_regular, E10 = gasoline_regular, PRF97 = gasoline_premium, E85 = e85, CH3OH = methanol, C2H5OH = ethanol, CH4 = cng. PRF87/PRF91 surrogates of US regular and E10 are priced as AAA regular (US regular is E10); PRF97 (premium surrogate) as AAA premium; E85 as AAA E85. USD/kg: PRF87 1.641, PRF91 1.640, E10 1.617, PRF97 1.985, E85 1.146, CH3OH 1.450, C2H5OH 0.653, CH4 1.207, water (headline test case) 0.0265, free 0, retail distilled (footnote) 0.408.

## Headline per fuel (lowest cost per mile at equal-or-better power, any regime / mode)

**Headline water price = 0.10 USD/gal, James's chosen test-case water cost (2026-10-25 07:32 PDT).** Comparison: free water (0 USD/gal; James 07:31 PDT - water is paid through the utility bill, no extra cost to fill a tank). 'w = 0' = no amount of water lowers cost per mile at that price. Eff-opt w = the best-efficiency step the Track B rule accepted in the same chain. Break-even = the highest water price at which some equal-or-better-power step still lowers cost per mile (M03 / CRN at that step).

| fuel | **$0.10/gal: where, w** | **cost per mile %** (M03 / CRN) | power % (M03 / CRN) | verdict | eff-opt w in that chain | $0: where, w | cost per mile % at $0 (M03 / CRN) | power % (M03 / CRN) | break-even water USD/gal (M03 / CRN), where, w |
|---|---|---|---|---|---|---|---|---|---|
| PRF87 | normal / liquid, 0.100 | -1.239 / -1.220 | +3.352 / +3.332 | COST GAIN | 0.100 | normal / liquid, 0.100 | -1.416 / -1.397 | +3.352 / +3.332 | 0.91 / 0.90, normal / liquid, 0.002 |
| PRF91 | hot/H1 / liquid, 0.100 | -1.183 / -1.172 | +2.850 / +2.838 | COST GAIN | 0.100 | hot/H1 / liquid, 0.100 | -1.360 / -1.348 | +2.850 / +2.838 | 0.84 / 0.84, hot/H1 / liquid, 0.003 |
| PRF97 | normal / liquid, 0.100 | -0.869 / -0.851 | +2.935 / +2.915 | COST GAIN | 0.100 | normal / liquid, 0.100 | -1.016 / -0.997 | +2.935 / +2.915 | 0.81 / 0.79, normal / liquid, 0.001 |
| E10 | normal / liquid, 0.100 | -0.953 / -0.933 | +3.144 / +3.123 | COST GAIN | 0.100 | normal / liquid, 0.100 | -1.133 / -1.113 | +3.144 / +3.123 | 0.73 / 0.72, normal / liquid, 0.003 |
| E85 | normal / liquid, 0.100 | -1.501 / -1.467 | +4.678 / +4.642 | COST GAIN | 0.100 | normal / liquid, 0.100 | -1.753 / -1.719 | +4.678 / +4.642 | 0.80 / 0.79, normal / liquid, 0.003 |
| CH3OH | hot/H1 / humid_evap, 0.200 | -3.466 / -3.447 | +21.076 / +21.052 | COST GAIN | 0.200 | hot/H1 / humid_evap, 0.200 | -3.904 / -3.886 | +21.076 / +21.052 | 2.59 / 2.56, hot/H1 / liquid, 0.001 |
| C2H5OH | hot / humid_evap, 0.288 | -2.821 / -2.812 | +26.023 / +26.011 | COST GAIN | 0.288 | hot / humid_evap, 0.289 | -4.396 / -4.387 | +26.031 / +26.019 | 0.79 / 0.78, hot / liquid, 0.003 |
| CH4 | hot / humid_evap, 0.111 | -0.911 / -0.872 | +4.199 / +4.158 | COST GAIN | 0.110 | hot / humid_evap, 0.111 | -1.181 / -1.143 | +4.199 / +4.158 | 0.58 / 0.56, hot / liquid, 0.001 |

<sub>Footnote (sensitivity only): at retail distilled water (1.54 USD/gal, Walmart.com product listing, 2026-10-25) the best cost-per-mile changes are: PRF87 +0.00 % (w 0.000, normal / liquid); PRF91 +0.00 % (w 0.000, normal / liquid); PRF97 +0.00 % (w 0.000, normal / liquid); E10 +0.00 % (w 0.000, normal / liquid); E85 +0.00 % (w 0.000, normal / liquid); CH3OH -0.42 % (w 0.043, hot/H1 / humid_evap); C2H5OH +0.00 % (w 0.000, normal / liquid); CH4 +0.00 % (w 0.000, normal / liquid).</sub>

**Power drops (any computed eligible step with IMEP down by more than the noise in any engine):** E85 normal humid_ambient w 0.001 (-0.013 / -0.013 %); E85 hot humid_ambient w 0.001 (-0.014 / -0.013 %); CH3OH normal humid_ambient w 0.001 (-0.019 / -0.019 %); CH3OH hot/H1 humid_ambient w 0.001 (-0.017 / -0.017 %); C2H5OH normal humid_ambient w 0.001 (-0.016 / -0.016 %); C2H5OH hot humid_ambient w 0.001 (-0.014 / -0.013 %)


## Every chain (both engines side by side)

| fuel | regime | mode | point | w | d_eta pp (M03 / CRN) | power (IMEP) % (M03 / CRN) | fuel volume per unit work % (M03 / CRN) | **cost per mile % at $0.10/gal water** (M03 / CRN) | cost per mile % at $0 water (M03 / CRN) | verdict ($0.10) | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PRF87 | normal | liquid | eff-opt | 0.100 | +0.533 / +0.526 | +3.352 / +3.332 | -1.416 / -1.397 | -1.239 / -1.220 | -1.416 / -1.397 | COST GAIN | stopped |
| PRF87 | normal | liquid | cost-opt | 0.100 | +0.533 / +0.526 | +3.352 / +3.332 | -1.416 / -1.397 | -1.239 / -1.220 | -1.416 / -1.397 | COST GAIN |  |
| PRF87 | normal | liquid | cost-opt $0 | 0.100 | +0.533 / +0.526 | +3.352 / +3.332 | -1.416 / -1.397 | -1.239 / -1.220 | -1.416 / -1.397 | COST GAIN |  |
| PRF87 | normal | humid_evap | eff-opt | 0.100 | +0.468 / +0.466 | +5.167 / +5.160 | -1.247 / -1.239 | -1.070 / -1.062 | -1.247 / -1.239 | COST GAIN | stopped |
| PRF87 | normal | humid_evap | cost-opt | 0.100 | +0.468 / +0.466 | +5.167 / +5.160 | -1.247 / -1.239 | -1.070 / -1.062 | -1.247 / -1.239 | COST GAIN |  |
| PRF87 | normal | humid_evap | cost-opt $0 | 0.100 | +0.468 / +0.466 | +5.167 / +5.160 | -1.247 / -1.239 | -1.070 / -1.062 | -1.247 / -1.239 | COST GAIN |  |
| PRF87 | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| PRF87 | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| PRF87 | normal | humid_ambient | cost-opt $0 | 0.001 | +0.001 / +0.001 | -0.008 / -0.008 | -0.002 / -0.002 | +0.000 / -0.000 | -0.002 / -0.002 | no cost gain |  |
| PRF87 | hot (H1 low-CR) | liquid | eff-opt | 0.022 | +0.076 / +0.074 | +0.515 / +0.510 | -0.224 / -0.219 | -0.188 / -0.183 | -0.224 / -0.219 | COST GAIN | stopped |
| PRF87 | hot (H1 low-CR) | liquid | cost-opt | 0.023 | +0.079 / +0.078 | +0.538 / +0.533 | -0.233 / -0.228 | -0.196 / -0.191 | -0.233 / -0.228 | COST GAIN |  |
| PRF87 | hot (H1 low-CR) | liquid | cost-opt $0 | 0.023 | +0.079 / +0.078 | +0.538 / +0.533 | -0.233 / -0.228 | -0.196 / -0.191 | -0.233 / -0.228 | COST GAIN |  |
| PRF87 | hot (H1 low-CR) | humid_evap | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| PRF87 | hot (H1 low-CR) | humid_evap | cost-opt | 0.001 | +0.003 / +0.003 | +0.035 / +0.035 | -0.009 / -0.009 | -0.007 / -0.007 | -0.009 / -0.009 | no cost gain |  |
| PRF87 | hot (H1 low-CR) | humid_evap | cost-opt $0 | 0.001 | +0.003 / +0.003 | +0.035 / +0.035 | -0.009 / -0.009 | -0.007 / -0.007 | -0.009 / -0.009 | no cost gain |  |
| PRF87 | hot (H1 low-CR) | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| PRF87 | hot (H1 low-CR) | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| PRF87 | hot (H1 low-CR) | humid_ambient | cost-opt $0 | 0.001 | +0.000 / +0.000 | -0.009 / -0.009 | -0.001 / -0.001 | +0.001 / +0.000 | -0.001 / -0.001 | no cost gain |  |
| PRF91 | normal | liquid | eff-opt | 0.100 | +0.384 / +0.376 | +2.933 / +2.910 | -1.014 / -0.992 | -0.837 / -0.815 | -1.014 / -0.992 | COST GAIN | stopped |
| PRF91 | normal | liquid | cost-opt | 0.100 | +0.384 / +0.376 | +2.933 / +2.910 | -1.014 / -0.992 | -0.837 / -0.815 | -1.014 / -0.992 | COST GAIN |  |
| PRF91 | normal | liquid | cost-opt $0 | 0.100 | +0.384 / +0.376 | +2.933 / +2.910 | -1.014 / -0.992 | -0.837 / -0.815 | -1.014 / -0.992 | COST GAIN |  |
| PRF91 | normal | humid_evap | eff-opt | 0.100 | +0.371 / +0.369 | +4.882 / +4.877 | -0.978 / -0.973 | -0.801 / -0.795 | -0.978 / -0.973 | COST GAIN | stopped |
| PRF91 | normal | humid_evap | cost-opt | 0.100 | +0.371 / +0.369 | +4.882 / +4.877 | -0.978 / -0.973 | -0.801 / -0.795 | -0.978 / -0.973 | COST GAIN |  |
| PRF91 | normal | humid_evap | cost-opt $0 | 0.100 | +0.371 / +0.369 | +4.882 / +4.877 | -0.978 / -0.973 | -0.801 / -0.795 | -0.978 / -0.973 | COST GAIN |  |
| PRF91 | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| PRF91 | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| PRF91 | normal | humid_ambient | cost-opt $0 | 0.001 | +0.000 / +0.000 | -0.009 / -0.009 | -0.001 / -0.001 | +0.001 / +0.000 | -0.001 / -0.001 | no cost gain |  |
| PRF91 | hot (H1 low-CR) | liquid | eff-opt | 0.100 | +0.483 / +0.479 | +2.850 / +2.838 | -1.360 / -1.348 | -1.183 / -1.172 | -1.360 / -1.348 | COST GAIN | stopped |
| PRF91 | hot (H1 low-CR) | liquid | cost-opt | 0.100 | +0.483 / +0.479 | +2.850 / +2.838 | -1.360 / -1.348 | -1.183 / -1.172 | -1.360 / -1.348 | COST GAIN |  |
| PRF91 | hot (H1 low-CR) | liquid | cost-opt $0 | 0.100 | +0.483 / +0.479 | +2.850 / +2.838 | -1.360 / -1.348 | -1.183 / -1.172 | -1.360 / -1.348 | COST GAIN |  |
| PRF91 | hot (H1 low-CR) | humid_evap | eff-opt | 0.100 | +0.422 / +0.424 | +4.188 / +4.194 | -1.189 / -1.194 | -1.012 / -1.017 | -1.189 / -1.194 | COST GAIN | stopped |
| PRF91 | hot (H1 low-CR) | humid_evap | cost-opt | 0.100 | +0.422 / +0.424 | +4.188 / +4.194 | -1.189 / -1.194 | -1.012 / -1.017 | -1.189 / -1.194 | COST GAIN |  |
| PRF91 | hot (H1 low-CR) | humid_evap | cost-opt $0 | 0.100 | +0.422 / +0.424 | +4.188 / +4.194 | -1.189 / -1.194 | -1.012 / -1.017 | -1.189 / -1.194 | COST GAIN |  |
| PRF91 | hot (H1 low-CR) | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| PRF91 | hot (H1 low-CR) | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| PRF91 | hot (H1 low-CR) | humid_ambient | cost-opt $0 | 0.001 | +0.001 / +0.001 | -0.008 / -0.008 | -0.002 / -0.002 | +0.000 / -0.000 | -0.002 / -0.002 | no cost gain |  |
| PRF97 | normal | liquid | eff-opt | 0.100 | +0.396 / +0.388 | +2.935 / +2.915 | -1.016 / -0.997 | -0.869 / -0.851 | -1.016 / -0.997 | COST GAIN | stopped |
| PRF97 | normal | liquid | cost-opt | 0.100 | +0.396 / +0.388 | +2.935 / +2.915 | -1.016 / -0.997 | -0.869 / -0.851 | -1.016 / -0.997 | COST GAIN |  |
| PRF97 | normal | liquid | cost-opt $0 | 0.100 | +0.396 / +0.388 | +2.935 / +2.915 | -1.016 / -0.997 | -0.869 / -0.851 | -1.016 / -0.997 | COST GAIN |  |
| PRF97 | normal | humid_evap | eff-opt | 0.100 | +0.380 / +0.378 | +4.881 / +4.876 | -0.977 / -0.972 | -0.830 / -0.825 | -0.977 / -0.972 | COST GAIN | stopped |
| PRF97 | normal | humid_evap | cost-opt | 0.100 | +0.380 / +0.378 | +4.881 / +4.876 | -0.977 / -0.972 | -0.830 / -0.825 | -0.977 / -0.972 | COST GAIN |  |
| PRF97 | normal | humid_evap | cost-opt $0 | 0.100 | +0.380 / +0.378 | +4.881 / +4.876 | -0.977 / -0.972 | -0.830 / -0.825 | -0.977 / -0.972 | COST GAIN |  |
| PRF97 | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| PRF97 | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| PRF97 | normal | humid_ambient | cost-opt $0 | 0.001 | +0.000 / +0.000 | -0.009 / -0.009 | -0.001 / -0.001 | +0.000 / +0.000 | -0.001 / -0.001 | no cost gain |  |
| PRF97 | hot (H1 low-CR) | liquid | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| PRF97 | hot (H1 low-CR) | liquid | cost-opt | 0.001 | +0.003 / +0.003 | +0.020 / +0.020 | -0.007 / -0.007 | -0.006 / -0.006 | -0.007 / -0.007 | no cost gain |  |
| PRF97 | hot (H1 low-CR) | liquid | cost-opt $0 | 0.001 | +0.003 / +0.003 | +0.020 / +0.020 | -0.007 / -0.007 | -0.006 / -0.006 | -0.007 / -0.007 | no cost gain |  |
| PRF97 | hot (H1 low-CR) | humid_evap | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| PRF97 | hot (H1 low-CR) | humid_evap | cost-opt | 0.001 | +0.002 / +0.002 | +0.033 / +0.033 | -0.007 / -0.007 | -0.006 / -0.006 | -0.007 / -0.007 | no cost gain |  |
| PRF97 | hot (H1 low-CR) | humid_evap | cost-opt $0 | 0.001 | +0.002 / +0.002 | +0.033 / +0.033 | -0.007 / -0.007 | -0.006 / -0.006 | -0.007 / -0.007 | no cost gain |  |
| PRF97 | hot (H1 low-CR) | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| PRF97 | hot (H1 low-CR) | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| PRF97 | hot (H1 low-CR) | humid_ambient | cost-opt $0 | 0.001 | +0.000 / +0.000 | -0.009 / -0.009 | -0.001 / -0.001 | +0.001 / +0.000 | -0.001 / -0.001 | no cost gain |  |
| E10 | normal | liquid | eff-opt | 0.100 | +0.441 / +0.433 | +3.144 / +3.123 | -1.133 / -1.113 | -0.953 / -0.933 | -1.133 / -1.113 | COST GAIN | stopped |
| E10 | normal | liquid | cost-opt | 0.100 | +0.441 / +0.433 | +3.144 / +3.123 | -1.133 / -1.113 | -0.953 / -0.933 | -1.133 / -1.113 | COST GAIN |  |
| E10 | normal | liquid | cost-opt $0 | 0.100 | +0.441 / +0.433 | +3.144 / +3.123 | -1.133 / -1.113 | -0.953 / -0.933 | -1.133 / -1.113 | COST GAIN |  |
| E10 | normal | humid_evap | eff-opt | 0.100 | +0.416 / +0.413 | +5.161 / +5.154 | -1.069 / -1.063 | -0.889 / -0.883 | -1.069 / -1.063 | COST GAIN | stopped |
| E10 | normal | humid_evap | cost-opt | 0.100 | +0.416 / +0.413 | +5.161 / +5.154 | -1.069 / -1.063 | -0.889 / -0.883 | -1.069 / -1.063 | COST GAIN |  |
| E10 | normal | humid_evap | cost-opt $0 | 0.100 | +0.416 / +0.413 | +5.161 / +5.154 | -1.069 / -1.063 | -0.889 / -0.883 | -1.069 / -1.063 | COST GAIN |  |
| E10 | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| E10 | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| E10 | normal | humid_ambient | cost-opt $0 | 0.001 | +0.000 / +0.001 | -0.009 / -0.009 | -0.001 / -0.001 | +0.000 / +0.000 | -0.001 / -0.001 | no cost gain |  |
| E10 | hot (H1 low-CR) | liquid | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| E10 | hot (H1 low-CR) | liquid | cost-opt | 0.001 | +0.003 / +0.003 | +0.022 / +0.022 | -0.008 / -0.008 | -0.007 / -0.007 | -0.008 / -0.008 | no cost gain |  |
| E10 | hot (H1 low-CR) | liquid | cost-opt $0 | 0.001 | +0.003 / +0.003 | +0.022 / +0.022 | -0.008 / -0.008 | -0.007 / -0.007 | -0.008 / -0.008 | no cost gain |  |
| E10 | hot (H1 low-CR) | humid_evap | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| E10 | hot (H1 low-CR) | humid_evap | cost-opt | 0.001 | +0.003 / +0.003 | +0.035 / +0.035 | -0.008 / -0.008 | -0.006 / -0.006 | -0.008 / -0.008 | no cost gain |  |
| E10 | hot (H1 low-CR) | humid_evap | cost-opt $0 | 0.001 | +0.003 / +0.003 | +0.035 / +0.035 | -0.008 / -0.008 | -0.006 / -0.006 | -0.008 / -0.008 | no cost gain |  |
| E10 | hot (H1 low-CR) | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| E10 | hot (H1 low-CR) | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| E10 | hot (H1 low-CR) | humid_ambient | cost-opt $0 | 0.001 | +0.000 / +0.000 | -0.010 / -0.009 | -0.001 / -0.001 | +0.001 / +0.001 | -0.001 / -0.001 | no cost gain |  |
| E85 | normal | liquid | eff-opt | 0.100 | +0.723 / +0.710 | +4.678 / +4.642 | -1.753 / -1.719 | -1.501 / -1.467 | -1.753 / -1.719 | COST GAIN | stopped |
| E85 | normal | liquid | cost-opt | 0.100 | +0.723 / +0.710 | +4.678 / +4.642 | -1.753 / -1.719 | -1.501 / -1.467 | -1.753 / -1.719 | COST GAIN |  |
| E85 | normal | liquid | cost-opt $0 | 0.100 | +0.723 / +0.710 | +4.678 / +4.642 | -1.753 / -1.719 | -1.501 / -1.467 | -1.753 / -1.719 | COST GAIN |  |
| E85 | normal | humid_evap | eff-opt | 0.100 | +0.676 / +0.666 | +7.630 / +7.602 | -1.640 / -1.614 | -1.387 / -1.362 | -1.640 / -1.614 | COST GAIN | stopped |
| E85 | normal | humid_evap | cost-opt | 0.100 | +0.676 / +0.666 | +7.630 / +7.602 | -1.640 / -1.614 | -1.387 / -1.362 | -1.640 / -1.614 | COST GAIN |  |
| E85 | normal | humid_evap | cost-opt $0 | 0.100 | +0.676 / +0.666 | +7.630 / +7.602 | -1.640 / -1.614 | -1.387 / -1.362 | -1.640 / -1.614 | COST GAIN |  |
| E85 | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| E85 | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| E85 | normal | humid_ambient | cost-opt $0 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| E85 | hot | liquid | eff-opt | 0.096 | +0.410 / +0.400 | +3.183 / +3.157 | -1.073 / -1.048 | -0.830 / -0.805 | -1.073 / -1.048 | COST GAIN | stopped |
| E85 | hot | liquid | cost-opt | 0.097 | +0.413 / +0.403 | +3.217 / +3.190 | -1.081 / -1.056 | -0.836 / -0.810 | -1.081 / -1.056 | COST GAIN |  |
| E85 | hot | liquid | cost-opt $0 | 0.097 | +0.413 / +0.403 | +3.217 / +3.190 | -1.081 / -1.056 | -0.836 / -0.810 | -1.081 / -1.056 | COST GAIN |  |
| E85 | hot | humid_evap | eff-opt | 0.100 | +0.454 / +0.453 | +5.712 / +5.709 | -1.186 / -1.183 | -0.933 / -0.930 | -1.186 / -1.183 | COST GAIN | stopped |
| E85 | hot | humid_evap | cost-opt | 0.100 | +0.454 / +0.453 | +5.712 / +5.709 | -1.186 / -1.183 | -0.933 / -0.930 | -1.186 / -1.183 | COST GAIN |  |
| E85 | hot | humid_evap | cost-opt $0 | 0.100 | +0.454 / +0.453 | +5.712 / +5.709 | -1.186 / -1.183 | -0.933 / -0.930 | -1.186 / -1.183 | COST GAIN |  |
| E85 | hot | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| E85 | hot | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| E85 | hot | humid_ambient | cost-opt $0 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| CH3OH | normal | liquid | eff-opt | 0.132 | +1.065 / +1.050 | +8.445 / +8.407 | -2.452 / -2.417 | -2.181 / -2.146 | -2.452 / -2.417 | COST GAIN | stopped |
| CH3OH | normal | liquid | cost-opt | 0.132 | +1.065 / +1.050 | +8.445 / +8.407 | -2.452 / -2.417 | -2.181 / -2.146 | -2.452 / -2.417 | COST GAIN |  |
| CH3OH | normal | liquid | cost-opt $0 | 0.132 | +1.065 / +1.050 | +8.445 / +8.407 | -2.452 / -2.417 | -2.181 / -2.146 | -2.452 / -2.417 | COST GAIN |  |
| CH3OH | normal | humid_evap | eff-opt | 0.080 | +0.873 / +0.860 | +8.373 / +8.342 | -2.018 / -1.990 | -1.863 / -1.834 | -2.018 / -1.990 | COST GAIN | stopped |
| CH3OH | normal | humid_evap | cost-opt | 0.080 | +0.873 / +0.860 | +8.373 / +8.342 | -2.018 / -1.990 | -1.863 / -1.834 | -2.018 / -1.990 | COST GAIN |  |
| CH3OH | normal | humid_evap | cost-opt $0 | 0.080 | +0.873 / +0.860 | +8.373 / +8.342 | -2.018 / -1.990 | -1.863 / -1.834 | -2.018 / -1.990 | COST GAIN |  |
| CH3OH | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| CH3OH | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| CH3OH | normal | humid_ambient | cost-opt $0 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| CH3OH | hot (H1 low-CR) | liquid | eff-opt | 0.063 | +0.716 / +0.694 | +3.986 / +3.920 | -2.005 / -1.943 | -1.884 / -1.822 | -2.005 / -1.943 | COST GAIN | stopped |
| CH3OH | hot (H1 low-CR) | liquid | cost-opt | 0.064 | +0.720 / +0.697 | +4.029 / +3.964 | -2.014 / -1.952 | -1.891 / -1.830 | -2.014 / -1.952 | COST GAIN |  |
| CH3OH | hot (H1 low-CR) | liquid | cost-opt $0 | 0.064 | +0.720 / +0.697 | +4.029 / +3.964 | -2.014 / -1.952 | -1.891 / -1.830 | -2.014 / -1.952 | COST GAIN |  |
| CH3OH | hot (H1 low-CR) | humid_evap | eff-opt | 0.200 | +1.423 / +1.416 | +21.076 / +21.052 | -3.904 / -3.886 | -3.466 / -3.447 | -3.904 / -3.886 | COST GAIN | in progress (step 200) |
| CH3OH | hot (H1 low-CR) | humid_evap | cost-opt | 0.200 | +1.423 / +1.416 | +21.076 / +21.052 | -3.904 / -3.886 | -3.466 / -3.447 | -3.904 / -3.886 | COST GAIN |  |
| CH3OH | hot (H1 low-CR) | humid_evap | cost-opt $0 | 0.200 | +1.423 / +1.416 | +21.076 / +21.052 | -3.904 / -3.886 | -3.466 / -3.447 | -3.904 / -3.886 | COST GAIN |  |
| CH3OH | hot (H1 low-CR) | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| CH3OH | hot (H1 low-CR) | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| CH3OH | hot (H1 low-CR) | humid_ambient | cost-opt $0 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| C2H5OH | normal | liquid | eff-opt | 0.173 | +0.765 / +0.754 | +7.794 / +7.767 | -1.688 / -1.663 | -0.854 / -0.829 | -1.688 / -1.663 | COST GAIN | stopped |
| C2H5OH | normal | liquid | cost-opt | 0.173 | +0.765 / +0.754 | +7.794 / +7.767 | -1.688 / -1.663 | -0.854 / -0.829 | -1.688 / -1.663 | COST GAIN |  |
| C2H5OH | normal | liquid | cost-opt $0 | 0.173 | +0.765 / +0.754 | +7.794 / +7.767 | -1.688 / -1.663 | -0.854 / -0.829 | -1.688 / -1.663 | COST GAIN |  |
| C2H5OH | normal | humid_evap | eff-opt | 0.101 | +0.556 / +0.548 | +7.737 / +7.720 | -1.231 / -1.216 | -0.782 / -0.766 | -1.231 / -1.216 | COST GAIN | stopped |
| C2H5OH | normal | humid_evap | cost-opt | 0.102 | +0.559 / +0.551 | +7.744 / +7.726 | -1.238 / -1.222 | -0.783 / -0.767 | -1.238 / -1.222 | COST GAIN |  |
| C2H5OH | normal | humid_evap | cost-opt $0 | 0.102 | +0.559 / +0.551 | +7.744 / +7.726 | -1.238 / -1.222 | -0.783 / -0.767 | -1.238 / -1.222 | COST GAIN |  |
| C2H5OH | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| C2H5OH | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| C2H5OH | normal | humid_ambient | cost-opt $0 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| C2H5OH | hot | liquid | eff-opt | 0.096 | +0.857 / +0.837 | +4.493 / +4.441 | -2.152 / -2.103 | -1.730 / -1.681 | -2.152 / -2.103 | COST GAIN | stopped |
| C2H5OH | hot | liquid | cost-opt | 0.097 | +0.860 / +0.840 | +4.528 / +4.475 | -2.159 / -2.110 | -1.733 / -1.684 | -2.159 / -2.110 | COST GAIN |  |
| C2H5OH | hot | liquid | cost-opt $0 | 0.097 | +0.860 / +0.840 | +4.528 / +4.475 | -2.159 / -2.110 | -1.733 / -1.684 | -2.159 / -2.110 | COST GAIN |  |
| C2H5OH | hot | humid_evap | eff-opt | 0.288 | +1.789 / +1.785 | +26.023 / +26.011 | -4.389 / -4.380 | -2.821 / -2.812 | -4.389 / -4.380 | COST GAIN | stopped |
| C2H5OH | hot | humid_evap | cost-opt | 0.288 | +1.789 / +1.785 | +26.023 / +26.011 | -4.389 / -4.380 | -2.821 / -2.812 | -4.389 / -4.380 | COST GAIN |  |
| C2H5OH | hot | humid_evap | cost-opt $0 | 0.289 | +1.792 / +1.788 | +26.031 / +26.019 | -4.396 / -4.387 | -2.820 / -2.811 | -4.396 / -4.387 | COST GAIN |  |
| C2H5OH | hot | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| C2H5OH | hot | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| C2H5OH | hot | humid_ambient | cost-opt $0 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| CH4 | normal | liquid | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| CH4 | normal | liquid | cost-opt | 0.001 | +0.002 / +0.002 | +0.019 / +0.019 | -0.004 / -0.004 | -0.002 / -0.002 | -0.004 / -0.004 | no cost gain |  |
| CH4 | normal | liquid | cost-opt $0 | 0.001 | +0.002 / +0.002 | +0.019 / +0.019 | -0.004 / -0.004 | -0.002 / -0.002 | -0.004 / -0.004 | no cost gain |  |
| CH4 | normal | humid_evap | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| CH4 | normal | humid_evap | cost-opt | 0.001 | +0.002 / +0.002 | +0.035 / +0.035 | -0.005 / -0.005 | -0.003 / -0.003 | -0.005 / -0.005 | no cost gain |  |
| CH4 | normal | humid_evap | cost-opt $0 | 0.001 | +0.002 / +0.002 | +0.035 / +0.035 | -0.005 / -0.005 | -0.003 / -0.003 | -0.005 / -0.005 | no cost gain |  |
| CH4 | normal | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| CH4 | normal | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| CH4 | normal | humid_ambient | cost-opt $0 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| CH4 | hot | liquid | eff-opt | 0.085 | +0.369 / +0.356 | +1.990 / +1.956 | -0.889 / -0.857 | -0.687 / -0.655 | -0.889 / -0.857 | COST GAIN | stopped |
| CH4 | hot | liquid | cost-opt | 0.086 | +0.373 / +0.359 | +2.012 / +1.978 | -0.897 / -0.864 | -0.693 / -0.660 | -0.897 / -0.864 | COST GAIN |  |
| CH4 | hot | liquid | cost-opt $0 | 0.086 | +0.373 / +0.359 | +2.012 / +1.978 | -0.897 / -0.864 | -0.693 / -0.660 | -0.897 / -0.864 | COST GAIN |  |
| CH4 | hot | humid_evap | eff-opt | 0.110 | +0.489 / +0.474 | +4.159 / +4.119 | -1.174 / -1.135 | -0.906 / -0.867 | -1.174 / -1.135 | COST GAIN | stopped |
| CH4 | hot | humid_evap | cost-opt | 0.111 | +0.492 / +0.477 | +4.199 / +4.158 | -1.181 / -1.143 | -0.911 / -0.872 | -1.181 / -1.143 | COST GAIN |  |
| CH4 | hot | humid_evap | cost-opt $0 | 0.111 | +0.492 / +0.477 | +4.199 / +4.158 | -1.181 / -1.143 | -0.911 / -0.872 | -1.181 / -1.143 | COST GAIN |  |
| CH4 | hot | humid_ambient | eff-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain | stopped |
| CH4 | hot | humid_ambient | cost-opt | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | no cost gain |  |
| CH4 | hot | humid_ambient | cost-opt $0 | 0.001 | +0.000 / +0.000 | -0.007 / -0.007 | -0.001 / -0.001 | +0.001 / +0.001 | -0.001 / -0.001 | no cost gain |  |

## Caveats carried over (still apply to every cost number)

* **Running cost only.** Not included: the water system's hardware (pump, tank, injector, controls), freeze
  protection (antifreeze, or methanol in the water), the extra weight of the water carried, and the energy to heat
  or pressurise the water. These would reduce (and could erase) the cost gains shown here.
* **Water quality.** Tap water carries minerals that leave deposits in injectors and combustion chambers; real
  water-injection systems use distilled or deionised water. Treat the $0.10/gal headline and the $0/gal tap-water
  comparison as optimistic; the retail-distilled sensitivity is the conservative case.
* **Fixed burn duration model gap.** Module 03 holds the 10-90 % burn duration essentially fixed as water is
  added (flame-speed fits only reduce S_L; the burn-duration penalty of water dilution measured in engines is not
  reproduced). The B1 sign test (spark held at the dry setting) still gains, while published engine tests lose
  efficiency at fixed timing, so every efficiency - and therefore every fuel-saving and cost gain - here is an
  **upper bound**.
* **Knock is modelled only in Module 03.** M03-CRN has no knock model; it re-runs the Module 03 spark timing. The
  part of a gain that comes from knock relief therefore rests on one engine.
* **Lower bounds at w = 0.10 for the gasoline blends** (PRF87/91/97, E10, E85): those chains stop at the end of the
  flame-speed fit validity (w <= 0.10), not because the gain ran out, so their cost gains could be larger.
* No gas-exchange / friction model: power and efficiency are indicated (IMEP), not brake, so read the gains
  as indicated upper bounds. Brake power is not modelled; at equal speed and
  friction the brake-power change has the same sign and a larger % magnitude.
* Absolute $/mile is NOT comparable across fuels (road fuels at retail, alcohols at wholesale, CNG quarterly
  retail). Compare each fuel only with its own dry baseline (the % columns).

