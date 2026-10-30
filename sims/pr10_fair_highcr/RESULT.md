# PR 10 high-CR fair rerun: merged result (Grok Bot, 2026-10-29 21:10 PDT)

Status: EXECUTED, not validated. Model output only (M03 two-zone + M03-CRN, knock engines M03 integral, CRECK Livengood-Wu screen,
and full CRECK end-gas check on the limit-bracket rows). Nothing here is measured. Build one engine and bench test it before ordering.

Fair baseline: every wet case is compared with dry DEI (fuel-evaporation cooling) of the same fuel and regime, each at its OWN
knock-limited CR (klCR). Factory CR rule = klCR - 1 margin, lower of hot and normal duty. W/F = w/(1-w); W/F > 0.6 is flagged (R-WE-22).

## Flags (read first)
1. **The alcohol gains hold only under the full-evaporation assumption.** Both intake modes (humid_evap and liquid) assume the injected
   water fully evaporates before or during compression. Wall film, droplets reaching the cylinder, or incomplete evaporation are not modelled;
   if water does not fully evaporate, the charge-cooling and knock benefit (and so the higher CR) will be smaller.
2. **Humid and liquid water give identical results** for methanol, ethanol and E85, and for PRF91 in normal duty, wherever both were run
   (row-for-row identical up to CR 26). The only exception is PRF91 hot duty at w0.2/w0.3, where liquid is about 0.4-0.5 pp better and
   allows 0.5 CR more. Apparent humid-vs-liquid differences in RESULT-alcohols.md come only from the CR range: the extended scan
   (wet CR 28-32, dry CR 22-28) was run on the humid dirs only, and the liquid dirs' dry baseline stops at CR 20, which makes liquid gains
   look larger. Use the humid rows for alcohols.
3. **Alcohol knock limits sit at the scan edge.** Methanol never knocked in any knock engine up to CR 32 (wet) / 28 (dry). Ethanol wet
   at w >= 0.3 is knock-free up to CR 32. "klCR 32" is therefore the top of the scan, not a knock limit; the true model limit is higher, and
   the practical limit will be set by preignition, peak pressure and the dry-running failsafe, not by end-gas knock.
4. Second-model check: the full CRECK end-gas check ran on 69 bracket rows (4 humid dirs). It found knock only on rows that M03 already
   flags (ethanol dry CR 26-28, ethanol w0.15 CR 30-32) and none on methanol, so it did not lower any alcohol klCR. On the blends it lowered
   PRF91 hot dry klCR from 8.0 to 7.5. Liquid alcohol dirs were not end-gas checked (identical rows, flag 2).
5. Dry-running risk: ethanol dry klCR is 16 (hot) / 18 (normal). An engine built near the wet limit (> 20) is far beyond the dry knock
   limit, so the water-out failsafe (ENGINE-ORDER-SPEC section 6) is mandatory, not optional.

## Best wet case per fuel (bound i, power >= dry, W/F <= 0.6)
| fuel | regime | dry klCR | best wet case | wet klCR | d_eta pp M03/CRN | power % | cost/mile % M03/CRN |
|---|---|---|---|---|---|---|---|
| PRF91 | hot | 7.5 | humid w0.3 | 9.5 | +2.75 / +2.84 | +18.8 | -6.57 / -6.78 |
| PRF91 | hot | 7.5 | liquid w0.3 | 10.0 | +3.25 / +3.33 | +11.9 | -7.77 / -7.96 |
| PRF91 | normal | 10 | w0.3 (humid = liquid) | 14 | +3.56 / +3.55 | +9.5 | -7.80 / -7.76 |
| E85 | hot | 12 | w0.3 (humid = liquid) | 19 | +4.44 / +4.40 | +13.7 | -8.83 / -8.75 |
| E85 | normal | 13 | w0.3 (humid = liquid) | 22 EDGE | +3.67 / +3.63 | +4.1 | -7.19 / -7.09 |
| Methanol | hot | 28 EDGE | humid w0.15 | 32 EDGE | +2.03 / +2.18 | +2.4 | -3.87 / -4.16 |
| Methanol | normal | 28 EDGE | humid w0.15 | 32 EDGE | +1.55 / +1.70 | +2.0 | -2.96 / -3.25 |
| Ethanol | hot | 16 | humid w0.3 | 32 EDGE | +3.72 / +3.94 | +12.2 | -6.22 / -6.64 |
| Ethanol | normal | 18 | humid w0.3 | 32 EDGE | +1.88 / +2.15 | +1.0 | -2.36 / -2.92 |
For the alcohols, bound ii (the pessimistic bound) gives smaller gains and loses power for methanol; see the full tables. E85 normal w0.1 loses power.

## Recommended factory CR (klCR - 1, lower of hot/normal)
| fuel | model klCR (limiting regime) | model factory CR | note |
|---|---|---|---|
| PRF91 | 9.5 (hot, humid w0.3) | 8.5 | 9.0 if liquid injection is confirmed on the bench (liquid hot klCR 10) |
| E85 | 19 (hot, w0.3) | 18 | normal duty allows 22+ (scan edge) |
| Methanol | >= 32 (scan edge, both regimes) | >= 31 (not knock-limited in the model) | cap by preignition / p_max / failsafe, see spec |
| Ethanol | >= 32 at w0.3 (scan edge, both regimes) | >= 31 (not knock-limited at w0.3) | dry klCR only 16; cap by failsafe |

## Files
- RESULT-alcohols.md: full alcohol table (8 dirs, both bounds, humid + liquid) from summary_mail.py, with EDGE markers.
- RESULT-blends.json: PRF91 / E85 rows from summary_blends.py (klCR_M03 and klCR with CRECK end-gas).
- fullcheck.sh: the second-model run (BRACKET=1). Raw jsonl stays on the job hosts (mail: /opt/water-engine/pr10-fair-highcr-20261029/jobs,
  box: /workspace/self-jobs/pr10-blends).
