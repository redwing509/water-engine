# rig1: Track B H1 CH3OH/hot/humid_evap chain extension 200 -> 400 steps (noise rule 3.3e-5)

Finished 2026-10-25 12:21 PDT (box clock). Ran on rig1 (i5-4590, Idle, 2 cores, watchdog). Code pr8 @015e8ca, sims/track_b/run.py chain_noise, OUT=results/track_b/h1_hot.

```
[ext] CH3OH/hot/humid_evap best_w=0.235 steps=235 d_eta=+0.01618 stop=M03-CRN gain None not positive 3573s
```

Files: /workspace/pr8/results/track_b/h1_hot/ext_CH3OH_hot_humid_evap_400.json, /workspace/pr8/results/track_b/h1_hot/steps_CH3OH_hot_humid_evap__noise.jsonl (backup of the 200-step file in /workspace/pr8/results/track_b/h1_hot/bak-pre-rig1-202610251220). Hot regime only: the normal-regime CH3OH humid_evap chain already stopped below its cap. Cost metric ($0.10/gal headline, $0 secondary) still to be computed with sims/cost. Not yet peer-review verified; not committed.
