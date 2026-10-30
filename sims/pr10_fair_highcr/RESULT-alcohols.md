# PR 10 high-CR fair rerun (dry DEI at own klCR)

Summary for pr10-fair-highcr (Grok Bot 2026-10-29). klCR = highest CR before first M03 LW knock (integral >= 1);
best = max eta at CR <= klCR with a CRN row; wet vs the same fuel/regime dry DEI at ITS klCR. W/F = w/(1-w); flag > 0.6 (R-WE-22).
Knock engine 2 = full CRECK end-gas (knock_sym at the row CA50) on the limit-bracket rows (BRACKET=1, full.jsonl, added 2026-10-29 20:50 PDT);
klCR stops at the first M03, LW-CRECK or end-gas knock. "EDGE" = klCR is the top of the CR scan (no knock found; true limit is higher).
Liquid dirs were not end-gas checked (humid and liquid rows are identical wherever both ran). Factory CR = klCR - 1 margin. EXECUTED, not validated.

| fuel | regime | case | W/F | klCR | eta M03/CRN | d_eta pp M03/CRN | power % | cost/mile % M03/CRN | verdict |
|---|---|---|---|---|---|---|---|---|---|
| C2H5OH | hot | dry DEI | 0 | 16 | 0.4386/0.4383 | baseline | 0 | 0 | - |
| C2H5OH | hot | humid_evap-w0.15 i | 0.18 | 22 | 0.4611/0.4609 | +2.24 / +2.26 | +9.4 | -4.19 / -4.22 | COST GAIN |
| C2H5OH | hot | humid_evap-w0.15 ii | 0.18 | 22 | 0.4611/0.4609 | +2.24 / +2.26 | +9.4 | -4.19 / -4.22 | COST GAIN |
| C2H5OH | hot | humid_evap-w0.3 i | 0.43 | 32 EDGE | 0.4758/0.4776 | +3.72 / +3.94 | +12.2 | -6.22 / -6.64 | COST GAIN |
| C2H5OH | hot | humid_evap-w0.3 ii | 0.43 | 32 EDGE | 0.4644/0.4738 | +2.57 / +3.55 | +9.5 | -3.90 / -5.89 | COST GAIN |
| C2H5OH | hot | humid_evap-w0.375 i | 0.60 | 32 EDGE | 0.4725/0.4752 | +3.39 / +3.69 | +11.4 | -4.92 / -5.53 | COST GAIN |
| C2H5OH | hot | humid_evap-w0.375 ii | 0.60 | 32 EDGE | 0.4605/0.4757 | +2.19 / +3.74 | +9.1 | -2.44 / -5.62 | COST GAIN |
| C2H5OH | hot | humid_evap-w0.5 i | 1.00 | 32 EDGE | 0.4734/0.4728 | +3.48 / +3.45 | +11.6 | -3.59 / -3.54 | COST GAIN [W/F>0.6 R-WE-22] |
| C2H5OH | hot | humid_evap-w0.5 ii | 1.00 | 32 EDGE | 0.4520/0.4732 | +1.33 / +3.50 | +7.0 | +0.99 / -3.63 | fuel saved, but water cost eats it [W/F>0.6 R-WE-22] |
| C2H5OH | hot | dry DEI | 0 | 16 | 0.4386/0.4383 | baseline | 0 | 0 | - |
| C2H5OH | hot | liquid-w0.15 i | 0.18 | 22 | 0.4611/0.4609 | +2.24 / +2.26 | +9.4 | -4.19 / -4.22 | COST GAIN |
| C2H5OH | hot | liquid-w0.15 ii | 0.18 | 22 | 0.4611/0.4609 | +2.24 / +2.26 | +9.4 | -4.19 / -4.22 | COST GAIN |
| C2H5OH | hot | liquid-w0.3 i | 0.43 | 26 EDGE | 0.4677/0.4692 | +2.91 / +3.10 | +11.1 | -4.58 / -4.98 | COST GAIN |
| C2H5OH | hot | liquid-w0.3 ii | 0.43 | 26 EDGE | 0.4637/0.4727 | +2.51 / +3.45 | +10.1 | -3.76 / -5.68 | COST GAIN |
| C2H5OH | hot | liquid-w0.375 i | 0.60 | 26 EDGE | 0.4697/0.4718 | +3.11 / +3.35 | +11.6 | -4.35 / -4.85 | COST GAIN |
| C2H5OH | hot | liquid-w0.375 ii | 0.60 | 26 EDGE | 0.4603/0.4752 | +2.17 / +3.70 | +9.3 | -2.39 / -5.53 | COST GAIN |
| C2H5OH | hot | liquid-w0.5 i | 1.00 | 26 EDGE | 0.4702/0.4687 | +3.16 / +3.04 | +11.7 | -2.94 / -2.70 | COST GAIN [W/F>0.6 R-WE-22] |
| C2H5OH | hot | liquid-w0.5 ii | 1.00 | 26 EDGE | 0.4516/0.4723 | +1.29 / +3.40 | +7.2 | +1.07 / -3.43 | fuel saved, but water cost eats it [W/F>0.6 R-WE-22] |
| C2H5OH | normal | dry DEI | 0 | 18 | 0.4490/0.4486 | baseline | 0 | 0 | - |
| C2H5OH | normal | humid_evap-w0.15 i | 0.18 | 24 | 0.4600/0.4603 | +1.10 / +1.17 | +0.4 | -1.68 / -1.84 | COST GAIN |
| C2H5OH | normal | humid_evap-w0.15 ii | 0.18 | 32 EDGE | 0.4682/0.4716 | +1.92 / +2.29 | +1.3 | -3.41 / -4.18 | COST GAIN |
| C2H5OH | normal | humid_evap-w0.3 i | 0.43 | 32 EDGE | 0.4679/0.4701 | +1.88 / +2.15 | +1.0 | -2.36 / -2.92 | COST GAIN |
| C2H5OH | normal | humid_evap-w0.3 ii | 0.43 | 32 EDGE | 0.4632/0.4767 | +1.42 / +2.80 | +0.2 | -1.38 / -4.25 | COST GAIN |
| C2H5OH | normal | humid_evap-w0.375 i | 0.60 | 32 EDGE | 0.4692/0.4711 | +2.02 / +2.25 | +1.3 | -1.98 / -2.46 | COST GAIN |
| C2H5OH | normal | humid_evap-w0.375 ii | 0.60 | 32 EDGE | 0.4595/0.4775 | +1.05 / +2.89 | -0.6 | +0.09 / -3.76 | power loss |
| C2H5OH | normal | dry DEI | 0 | 18 | 0.4490/0.4486 | baseline | 0 | 0 | - |
| C2H5OH | normal | liquid-w0.15 i | 0.18 | 24 | 0.4600/0.4603 | +1.10 / +1.17 | +0.4 | -1.68 / -1.84 | COST GAIN |
| C2H5OH | normal | liquid-w0.15 ii | 0.18 | 26 EDGE | 0.4641/0.4672 | +1.50 / +1.86 | +0.9 | -2.55 / -3.29 | COST GAIN |
| C2H5OH | normal | liquid-w0.3 i | 0.43 | 26 EDGE | 0.4654/0.4672 | +1.64 / +1.86 | +1.2 | -1.84 / -2.31 | COST GAIN |
| C2H5OH | normal | liquid-w0.3 ii | 0.43 | 26 EDGE | 0.4592/0.4720 | +1.02 / +2.33 | -0.1 | -0.51 / -3.29 | power loss |
| C2H5OH | normal | liquid-w0.375 i | 0.60 | 26 EDGE | 0.4666/0.4678 | +1.75 / +1.91 | +1.5 | -1.42 / -1.75 | COST GAIN |
| C2H5OH | normal | liquid-w0.375 ii | 0.60 | 26 EDGE | 0.4556/0.4725 | +0.66 / +2.39 | -0.9 | +0.96 / -2.74 | power loss |
| CH3OH | hot | dry DEI | 0 | 28 EDGE | 0.4652/0.4653 | baseline | 0 | 0 | - |
| CH3OH | hot | humid_evap-w0.15 i | 0.18 | 32 EDGE | 0.4856/0.4871 | +2.03 / +2.18 | +2.4 | -3.87 / -4.16 | COST GAIN |
| CH3OH | hot | humid_evap-w0.15 ii | 0.18 | 32 EDGE | 0.4619/0.4691 | -0.34 / +0.39 | -1.1 | +1.05 / -0.50 | power loss |
| CH3OH | hot | humid_evap-w0.3 i | 0.43 | 32 EDGE | 0.4866/0.4890 | +2.13 / +2.37 | +2.7 | -3.63 / -4.11 | COST GAIN |
| CH3OH | hot | humid_evap-w0.3 ii | 0.43 | 32 EDGE | 0.4569/0.4736 | -0.83 / +0.83 | -2.2 | +2.62 / -0.99 | power loss |
| CH3OH | hot | humid_evap-w0.375 i | 0.60 | 32 EDGE | 0.4880/0.4879 | +2.28 / +2.26 | +3.0 | -3.63 / -3.60 | COST GAIN |
| CH3OH | hot | humid_evap-w0.375 ii | 0.60 | 32 EDGE | 0.4533/0.4714 | -1.20 / +0.62 | -2.9 | +3.77 / -0.23 | power loss |
| CH3OH | hot | humid_evap-w0.5 i | 1.00 | 32 EDGE | 0.4815/0.4802 | +1.62 / +1.49 | +1.6 | -1.61 / -1.34 | COST GAIN [W/F>0.6 R-WE-22] |
| CH3OH | hot | humid_evap-w0.5 ii | 1.00 | 32 EDGE | 0.4439/0.4589 | -2.13 / -0.64 | -4.9 | +6.71 / +3.24 | power loss [W/F>0.6 R-WE-22] |
| CH3OH | hot | humid_evap-w0.6 i | 1.50 | 32 EDGE | 0.4634/0.4660 | -0.19 / +0.08 | -2.2 | +3.15 / +2.57 | power loss [W/F>0.6 R-WE-22] |
| CH3OH | hot | humid_evap-w0.6 ii | 1.50 | 30 | 0.4289/0.4380 | -3.63 / -2.73 | -7.7 | +11.43 / +9.15 | power loss [W/F>0.6 R-WE-22] |
| CH3OH | hot | dry DEI | 0 | 20 EDGE | 0.4600/0.4601 | baseline | 0 | 0 | - |
| CH3OH | hot | liquid-w0.15 i | 0.18 | 26 EDGE | 0.4815/0.4829 | +2.14 / +2.28 | +2.6 | -4.14 / -4.41 | COST GAIN |
| CH3OH | hot | liquid-w0.15 ii | 0.18 | 26 EDGE | 0.4619/0.4691 | +0.18 / +0.91 | -0.8 | -0.08 / -1.62 | power loss |
| CH3OH | hot | liquid-w0.3 i | 0.43 | 26 EDGE | 0.4826/0.4843 | +2.26 / +2.43 | +2.9 | -3.94 / -4.27 | COST GAIN |
| CH3OH | hot | liquid-w0.3 ii | 0.43 | 26 EDGE | 0.4569/0.4736 | -0.31 / +1.35 | -1.9 | +1.47 / -2.10 | power loss |
| CH3OH | hot | liquid-w0.375 i | 0.60 | 26 EDGE | 0.4837/0.4826 | +2.37 / +2.25 | +3.1 | -3.86 / -3.62 | COST GAIN |
| CH3OH | hot | liquid-w0.375 ii | 0.60 | 26 EDGE | 0.4533/0.4714 | -0.68 / +1.14 | -2.7 | +2.61 / -1.34 | power loss |
| CH3OH | hot | liquid-w0.5 i | 1.00 | 26 EDGE | 0.4768/0.4736 | +1.67 / +1.35 | +1.6 | -1.75 / -1.08 | COST GAIN [W/F>0.6 R-WE-22] |
| CH3OH | hot | liquid-w0.5 ii | 1.00 | 26 EDGE | 0.4439/0.4589 | -1.61 / -0.12 | -4.7 | +5.52 / +2.09 | power loss [W/F>0.6 R-WE-22] |
| CH3OH | hot | liquid-w0.6 i | 1.50 | 26 EDGE | 0.4601/0.4583 | +0.01 / -0.18 | -1.9 | +2.71 / +3.14 | power loss [W/F>0.6 R-WE-22] |
| CH3OH | hot | liquid-w0.6 ii | 1.50 | 26 EDGE | 0.4289/0.4380 | -3.11 / -2.21 | -7.5 | +10.19 / +7.93 | power loss [W/F>0.6 R-WE-22] |
| CH3OH | normal | dry DEI | 0 | 28 EDGE | 0.4592/0.4592 | baseline | 0 | 0 | - |
| CH3OH | normal | humid_evap-w0.15 i | 0.18 | 32 EDGE | 0.4747/0.4762 | +1.55 / +1.70 | +2.0 | -2.96 / -3.25 | COST GAIN |
| CH3OH | normal | humid_evap-w0.15 ii | 0.18 | 32 EDGE | 0.4562/0.4636 | -0.30 / +0.44 | -1.1 | +0.98 / -0.63 | power loss |
| CH3OH | normal | humid_evap-w0.3 i | 0.43 | 32 EDGE | 0.4741/0.4762 | +1.49 / +1.70 | +1.7 | -2.38 / -2.82 | COST GAIN |
| CH3OH | normal | humid_evap-w0.3 ii | 0.43 | 32 EDGE | 0.4510/0.4678 | -0.82 / +0.86 | -2.2 | +2.62 / -1.08 | power loss |
| CH3OH | normal | humid_evap-w0.375 i | 0.60 | 32 EDGE | 0.4751/0.4745 | +1.59 / +1.53 | +1.9 | -2.29 / -2.17 | COST GAIN |
| CH3OH | normal | humid_evap-w0.375 ii | 0.60 | 32 EDGE | 0.4471/0.4654 | -1.21 / +0.62 | -3.1 | +3.83 / -0.26 | power loss |
| CH3OH | normal | dry DEI | 0 | 20 EDGE | 0.4542/0.4541 | baseline | 0 | 0 | - |
| CH3OH | normal | liquid-w0.15 i | 0.18 | 26 EDGE | 0.4704/0.4718 | +1.63 / +1.77 | +1.6 | -3.15 / -3.43 | COST GAIN |
| CH3OH | normal | liquid-w0.15 ii | 0.18 | 26 EDGE | 0.4562/0.4636 | +0.20 / +0.95 | -1.2 | -0.13 / -1.73 | power loss |
| CH3OH | normal | liquid-w0.3 i | 0.43 | 26 EDGE | 0.4708/0.4722 | +1.67 / +1.81 | +1.6 | -2.79 / -3.08 | COST GAIN |
| CH3OH | normal | liquid-w0.3 ii | 0.43 | 26 EDGE | 0.4510/0.4678 | -0.32 / +1.37 | -2.3 | +1.50 / -2.16 | power loss |
| CH3OH | normal | liquid-w0.375 i | 0.60 | 26 EDGE | 0.4715/0.4700 | +1.74 / +1.58 | +1.8 | -2.63 / -2.31 | COST GAIN |
| CH3OH | normal | liquid-w0.375 ii | 0.60 | 26 EDGE | 0.4471/0.4654 | -0.71 / +1.13 | -3.2 | +2.69 / -1.36 | power loss |

## Recommended factory CR (cost-best wet case with power >= dry and W/F <= 0.6, klCR - 1 margin; lower of hot/normal)
- C2H5OH: best humid_evap-w0.3 (hot) klCR 32 (scan edge, true limit higher) -> factory CR 31
- CH3OH: best liquid-w0.15 (hot) klCR 26 (scan edge, true limit higher) -> factory CR 25 **LIQUID-SCAN-ONLY value, NOT the order CR**: the liquid scan stops at CR 26; the extended humid scan is knock-free to CR 32 (see RESULT.md). Order CR = 32 per ENGINE-ORDER-SPEC.md (James 2026-10-29).
