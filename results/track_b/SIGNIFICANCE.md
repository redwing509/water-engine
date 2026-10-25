# Track B: cumulative significance and knock at the stopping point

Two tests; both require BOTH engines' gain > 2 sigma. Executed + 2-engine cross-checked only; not validated against experiment.

* **PRIMARY: gain-difference test** (Claude 20:15 PDT, recommended). 1-sigma = RSS(3.3e-5*sqrt(N), |M03 gain - CRN gain|, |CRN gain (Woschni) - CRN gain (Hohenberg)|). The heat-transfer term is the model-form error on the *gain*; the absolute Woschni/Hohenberg offset mostly cancels in a same-model wet-minus-dry difference.
* **SECONDARY: conservative absolute-band test** (a478dc5). Same, but the heat-transfer term is the absolute-efficiency band 0.4 pp (low) / 2.5 pp (high) from V1/C2.

| fuel | regime | water mode | best w | N | gain M03 (pp) | gain CRN W (pp) | gain CRN H (pp) | **2σ gain-diff (pp)** | **signif. (primary)** | 2σ band low/high (pp) | signif. low/high | CA50 / MBT CA50 | knock margin | spark limit |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CH4 | hot | humid_ambient | 0.000 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no | 0.800/5.000 | no/no | 14.6 / 11.1 | 0.0002 | knock |
| CH4 | normal | humid_ambient | 0.000 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no | 0.800/5.000 | no/no | 12.4 / 12.4 | 0.6020 | MBT |
| E10 | normal | humid_ambient | 0.000 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no | 0.800/5.000 | no/no | 12.8 / 7.3 | 0.0001 | knock |
| E85 | hot | humid_ambient | 0.000 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no | 0.800/5.000 | no/no | 11.2 / 7.3 | 0.0001 | knock |
| E85 | normal | humid_ambient | 0.000 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no | 0.800/5.000 | no/no | 14.8 / 8.5 | 0.0001 | knock |
| PRF87 | normal | humid_ambient | 0.000 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no | 0.800/5.000 | no/no | 14.7 / 6.9 | 0.0001 | knock |
| PRF91 | normal | humid_ambient | 0.000 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no | 0.800/5.000 | no/no | 11.8 / 6.9 | 0.0000 | knock |
| PRF97 | normal | humid_ambient | 0.000 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no | 0.800/5.000 | no/no | 12.3 / 7.3 | 0.0000 | knock |
| CH4 | normal | humid_evap | 0.000 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no | 0.800/5.000 | no/no | 12.4 / 12.4 | 0.6020 | MBT |
| CH4 | normal | liquid | 0.000 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no | 0.800/5.000 | no/no | 12.4 / 12.4 | 0.6020 | MBT |
| CH4 | hot | liquid | 0.085 | 85 | 0.3694 | 0.3564 | 0.6968 | 0.6840 | no | 0.803/5.000 | no/no | 12.1 / 11.1 | 0.0003 | knock |
| E85 | normal | humid_evap | 0.100 | 100 | 0.6757 | 0.6656 | 0.8048 | 0.2869 | yes | 0.803/5.000 | no/no | 12.7 / 8.4 | 0.0002 | knock |
| CH4 | hot | humid_evap | 0.110 | 110 | 0.4891 | 0.4736 | 0.8711 | 0.7985 | no | 0.804/5.001 | no/no | 11.6 / 11.0 | 0.0000 | knock |
| E10 | normal | humid_evap | 0.100 | 100 | 0.4158 | 0.4135 | 0.4915 | 0.1695 | yes | 0.803/5.000 | no/no | 11.0 / 7.3 | 0.0001 | knock |
| E85 | hot | humid_evap | 0.100 | 100 | 0.4536 | 0.4526 | 0.5560 | 0.2171 | yes | 0.803/5.000 | no/no | 9.0 / 7.3 | 0.0001 | knock |
| E85 | hot | liquid | 0.096 | 96 | 0.4098 | 0.4001 | 0.5783 | 0.3628 | yes | 0.803/5.000 | no/no | 7.9 / 7.3 | 0.0000 | knock |
| E10 | normal | liquid | 0.100 | 100 | 0.4409 | 0.4333 | 0.5669 | 0.2755 | yes | 0.803/5.000 | no/no | 10.2 / 7.3 | 0.0001 | knock |
| PRF87 | normal | humid_evap | 0.100 | 100 | 0.4684 | 0.4660 | 0.5245 | 0.1343 | yes | 0.803/5.000 | no/no | 12.9 / 6.8 | 0.0000 | knock |
| C2H5OH | hot | humid_ambient | 0.000 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no | 0.800/5.000 | no/no | 14.9 / 8.3 | 0.0001 | knock |
| C2H5OH | normal | humid_ambient | 0.000 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no | 0.800/5.000 | no/no | 13.7 / 11.9 | 0.0002 | knock |
| CH3OH | normal | humid_ambient | 0.000 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | no | 0.800/5.000 | no/no | 14.6 / 9.8 | 0.0006 | knock |
| PRF91 | normal | humid_evap | 0.100 | 100 | 0.3705 | 0.3687 | 0.4368 | 0.1515 | yes | 0.803/5.000 | no/no | 10.0 / 6.8 | 0.0001 | knock |
| E85 | normal | liquid | 0.100 | 100 | 0.7235 | 0.7097 | 0.9506 | 0.4870 | yes | 0.803/5.001 | no/no | 11.7 / 8.4 | 0.0000 | knock |
| PRF87 | normal | liquid | 0.100 | 100 | 0.5329 | 0.5261 | 0.6238 | 0.2066 | yes | 0.803/5.000 | no/no | 12.0 / 6.8 | 0.0001 | knock |
| PRF97 | normal | humid_evap | 0.100 | 100 | 0.3801 | 0.3785 | 0.4552 | 0.1671 | yes | 0.803/5.000 | no/no | 10.6 / 7.3 | 0.0001 | knock |
| PRF91 | normal | liquid | 0.100 | 100 | 0.3843 | 0.3761 | 0.4930 | 0.2436 | yes | 0.803/5.000 | no/no | 9.0 / 6.8 | 0.0001 | knock |
| PRF97 | normal | liquid | 0.100 | 100 | 0.3956 | 0.3884 | 0.5202 | 0.2721 | yes | 0.803/5.000 | no/no | 9.8 / 7.3 | 0.0001 | knock |
| CH3OH | normal | humid_evap | 0.080 | 80 | 0.8729 | 0.8603 | 1.4327 | 1.1466 | no | 0.803/5.000 | yes/no | 9.7 / 9.7 | 0.1703 | MBT |
| C2H5OH | hot | liquid | 0.096 | 96 | 0.8569 | 0.8369 | 1.2879 | 0.9051 | no | 0.804/5.001 | yes/no | 8.5 / 8.2 | 0.0000 | knock |
| C2H5OH | normal | humid_evap | 0.101 | 101 | 0.5558 | 0.5484 | 0.9288 | 0.7639 | no | 0.803/5.000 | no/no | 11.7 / 11.7 | 0.4289 | MBT |
| CH3OH | normal | liquid | 0.132 | 132 | 1.0652 | 1.0496 | 1.6529 | 1.2093 | no | 0.804/5.001 | yes/no | 9.6 / 9.6 | 0.6970 | MBT |
| C2H5OH | hot | humid_evap | 0.200 | 200 | 1.3490 | 1.3414 | 1.7756 | 0.8735 | yes | 0.806/5.001 | yes/no | 8.0 / 8.0 | 0.5902 | MBT |
| C2H5OH | normal | liquid | 0.173 | 173 | 0.7653 | 0.7536 | 1.1707 | 0.8391 | no | 0.805/5.001 | no/no | 11.6 / 11.6 | 0.7981 | MBT |

Heat-transfer gain-difference notes: M03-CRN Hohenberg re-run of dry + stop points; stopped at w=0: stop point = dry point, gain-difference 0 exactly
