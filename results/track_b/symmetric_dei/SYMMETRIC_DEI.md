# Track B symmetric DEI rebase (fuel evaporated by DEI at every step incl. w0)

Executed, numerically cross-checked (Module 03 + M03-CRN), not validated. Baseline = each chain's own w0 DEI dry row at the fuel/regime DEI rule CR. normal = wall 450 K, T_intake 320 K (~90 C coolant); hot = wall 520 K, T_intake 400 K. Cost: $0.10/gal water headline, $0 secondary.

| fuel | regime | mode | CR | stop w | gain vs DEI pp (M03/CRN) | power % (M03/CRN) | cost/mile % $0.10 (M03/CRN) | cost/mile % $0 (M03/CRN) | cost-min w | verdict | knock 2-engine |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PRF87 | normal | liquid | 9.0 | 0.150 | +0.633 / +0.622 | +5.000 / +4.967 | -1.367 / -1.336 | -1.647 / -1.616 | 0.151 | COST GAIN | pass |
| PRF87 | normal | humid_evap | 9.0 | 0.149 | +0.631 / +0.620 | +5.168 / +5.137 | -1.362 / -1.333 | -1.639 / -1.610 | 0.150 | COST GAIN | pass |
| PRF87 | hot | liquid | 7.0 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | 0.001 | no cost gain | pass |
| PRF87 | hot | humid_evap | 7.0 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | 0.001 | no cost gain | pass |
| PRF91 | normal | liquid | 10.0 | 0.187 | +0.904 / +0.888 | +5.880 / +5.834 | -1.920 / -1.877 | -2.282 / -2.240 | 0.188 | COST GAIN | pass |
| PRF91 | normal | humid_evap | 10.0 | 0.187 | +0.904 / +0.888 | +5.880 / +5.834 | -1.920 / -1.877 | -2.282 / -2.240 | 0.188 | COST GAIN | pass |
| PRF91 | hot | liquid | 8.0 | 0.125 | +0.470 / +0.465 | +3.381 / +3.365 | -1.068 / -1.052 | -1.295 / -1.279 | 0.126 | COST GAIN | pass |
| PRF91 | hot | humid_evap | 8.0 | 0.026 | +0.088 / +0.089 | +1.001 / +1.004 | -0.203 / -0.206 | -0.246 / -0.249 | 0.027 | COST GAIN | FAIL |
| PRF97 | normal | liquid | 11.0 | 0.185 | +0.865 / +0.850 | +5.752 / +5.710 | -1.839 / -1.801 | -2.135 / -2.097 | 0.186 | COST GAIN | pass |
| PRF97 | normal | humid_evap | 11.0 | 0.185 | +0.865 / +0.850 | +5.752 / +5.710 | -1.839 / -1.801 | -2.135 / -2.097 | 0.186 | COST GAIN | pass |
| PRF97 | hot | liquid | 9.0 | 0.182 | +0.732 / +0.726 | +5.262 / +5.243 | -1.650 / -1.633 | -1.941 / -1.924 | 0.183 | COST GAIN | pass |
| PRF97 | hot | humid_evap | 9.0 | 0.002 | +0.007 / +0.007 | +0.076 / +0.076 | -0.017 / -0.017 | -0.020 / -0.020 | 0.003 | COST GAIN | FAIL |
| E10 | normal | liquid | 11.0 | 0.174 | +0.859 / +0.842 | +4.905 / +4.860 | -1.777 / -1.734 | -2.114 / -2.072 | 0.175 | COST GAIN | pass |
| E10 | normal | humid_evap | 11.0 | 0.174 | +0.859 / +0.842 | +4.905 / +4.860 | -1.777 / -1.734 | -2.114 / -2.072 | 0.175 | COST GAIN | pass |
| E10 | hot | liquid | 9.0 | 0.190 | +0.812 / +0.803 | +5.886 / +5.861 | -1.766 / -1.743 | -2.142 / -2.118 | 0.191 | COST GAIN | pass |
| E10 | hot | humid_evap | 9.0 | 0.300 | +1.272 / +1.274 | +18.712 / +18.719 | -2.637 / -2.643 | -3.315 / -3.321 | 0.300 | COST GAIN | pass |
| E85 | normal | liquid | 13.5 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | 0.001 | no cost gain | pass |
| E85 | normal | humid_evap | 13.5 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | 0.000 | no cost gain | pass |
| E85 | hot | liquid | 12.5 | 0.186 | +1.221 / +1.196 | +9.223 / +9.157 | -2.355 / -2.297 | -2.868 / -2.810 | 0.187 | COST GAIN | pass |
| E85 | hot | humid_evap | 12.5 | 0.182 | +1.208 / +1.185 | +9.200 / +9.137 | -2.340 / -2.284 | -2.840 / -2.784 | 0.183 | COST GAIN | pass |
| CH3OH | normal | liquid | 22.0 | 0.030 | +0.135 / +0.131 | -0.000 / -0.008 | -0.243 / -0.234 | -0.299 / -0.291 | 0.030 | COST GAIN | pass |
| CH3OH | normal | humid_evap | 22.0 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | 0.000 | no cost gain | pass |
| CH3OH | hot | liquid | 21.0 | 0.062 | +0.354 / +0.345 | +0.130 / +0.111 | -0.646 / -0.627 | -0.766 / -0.747 | 0.063 | COST GAIN | pass |
| CH3OH | hot | humid_evap | 21.0 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | 0.000 | no cost gain | pass |
| C2H5OH | normal | liquid | 24.0 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | 0.000 | no cost gain | FAIL |
| C2H5OH | normal | humid_evap | 24.0 | 0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | +0.000 / +0.000 | 0.000 | no cost gain | FAIL |
| C2H5OH | hot | liquid | 24.0 | 0.085 | +0.335 / +0.332 | +3.458 / +3.453 | -0.340 / -0.335 | -0.714 / -0.709 | 0.085 | COST GAIN | pass |
| C2H5OH | hot | humid_evap | 24.0 | 0.044 | +0.218 / +0.216 | +3.174 / +3.169 | -0.280 / -0.275 | -0.465 / -0.461 | 0.044 | COST GAIN | FAIL |

