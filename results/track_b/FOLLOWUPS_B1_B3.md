# Track B follow-ups B1 and B3 (job water-engine-trackB-followups-20261025-0050), PARTIAL

Data: noise-rule chains as of 2026-10-25 ~01:05 PDT; the noise stage (PID 500749) is still running, so several
chains are mid-way. Both scripts rerun automatically when it ends (sign_test.json / lit_compare.json, final).
Labels: **executed; 2-engine (Module 03 + M03-CRN Woschni); B3 literature-compared. Not validated.**

## B1 [Track B] sign test, R-WE-09 (`sims/track_b/sign_test.py`, `sign_test_partial.json`)
Each positive optimum re-run at its best w with CA50 held at the dry setting (single evaluation, no spark search).

| fuel regime mode | w | total gain M03/CRN pp | fixed-spark gain M03/CRN pp | knock-relief share |
|---|---|---|---|---|
| C2H5OH hot liquid | 0.046 | +0.515/+0.507 | +0.106/+0.111 | 79 % |
| C2H5OH hot humid_evap | 0.054 | +0.597/+0.589 | +0.160/+0.166 | 73 % |
| C2H5OH normal liquid | 0.007 | +0.051/+0.050 | +0.022/+0.022 | 56 % |
| C2H5OH normal humid_evap | 0.008 | +0.063/+0.062 | +0.033/+0.032 | 48 % |
| CH3OH normal liquid | 0.048 | +0.608/+0.599 | +0.204/+0.201 | 67 % |
| CH3OH normal humid_evap | 0.057 | +0.730/+0.720 | +0.304/+0.301 | 58 % |
| CH4 hot liquid | 0.086 | +0.373/+0.359 | +0.154/+0.159 | 59 % |
| CH4 hot humid_evap | 0.111 | +0.492/+0.477 | +0.255/+0.260 | 48 % |
| E10 normal liquid | 0.100 | +0.441/+0.433 | +0.171/+0.179 | 61 % |
| E10 normal humid_evap | 0.100 | +0.416/+0.413 | +0.216/+0.224 | 48 % |
| E85 hot liquid | 0.097 | +0.413/+0.403 | +0.229/+0.244 | 45 % |
| E85 hot humid_evap | 0.100 | +0.454/+0.453 | +0.299/+0.313 | 34 % |
| E85 normal liquid | 0.087 | +0.635/+0.623 | +0.231/+0.228 | 64 % |
| E85 normal humid_evap | 0.100 | +0.676/+0.666 | +0.339/+0.335 | 50 % |
| PRF87 normal liquid | 0.081 | +0.432/+0.427 | +0.123/+0.129 | 72 % |
| PRF87 normal humid_evap | 0.100 | +0.468/+0.466 | +0.195/+0.203 | 58 % |
| PRF91 normal liquid | 0.076 | +0.298/+0.293 | +0.117/+0.125 | 61 % |
| PRF91 normal humid_evap | 0.098 | +0.363/+0.361 | +0.195/+0.206 | 46 % |
| PRF97 normal liquid | 0.059 | +0.239/+0.235 | +0.092/+0.099 | 61 % |
| PRF97 normal humid_evap | 0.074 | +0.279/+0.278 | +0.149/+0.157 | 46 % |

**Result:** the gain does NOT vanish with spark held at the dry setting. 34-79 % of it is knock relief / spark
advance; the rest (charge cooling, dilution, lower gamma loss, "I3") survives at fixed spark in both engines.
**This disagrees with WE-27**, where port water injection at the original spark LOWERED efficiency (slower early
burn, higher COV). Likely cause: Module 03 keeps the 10-90 % burn duration at ~25.0 CAD regardless of water
(only S_L changes, by <3 %), and neither engine has cycle-to-cycle variation, so water's burn-rate penalty is
missing. The fixed-spark share should be treated as an upper bound until a water-sensitive burn-duration model
(e.g. S_L/turbulent-flame scaling of the Wiebe duration) is added. Nobody should cite the +0.2-0.7 pp yet.

## B3 [Track B] stopping points vs literature, R-WE-08/09 (`sims/track_b/lit_compare.py`, `lit_compare_partial.{json,png}`)
Water/fuel by volume at every positive optimum: 3.8-8.7 % (liquid fuels; CH4 by mass 9.4-12.5 %). All are
BELOW the WE-27 optimum window (~30 % vol) and below WE-28's 10 % knock-free threshold, and our gains
(+0.24 to +0.73 pp absolute) are below WE-27's +1.5 %. Several chains are still climbing (E10, E85, PRF87 at the
w = 0.10 cap), so the gap to the 10-30 % window may close; the 200-step extension rule applies.
Total added in-cylinder water at the optima is 0.37-0.97 % of trapped mass. humid_ambient chains stop at
w <= 0.001 (saturation cap at T_intake), so they never reach equal total water and the WE-25/26 "curves collapse
at equal total water" test cannot be done from chain data; it needs matched-total-water probes (queued with B2).

## Still to do (queued, box fully loaded): B2 independent knock check (Douaud-Eyzat + WE-28), B4 CR re-optimisation,
A1 droplet sub-model vs Volkov & Strizhak (WE-32). Final B1/B3 rerun is armed for when the noise stage ends.
