# Module 12 – OpenFOAM spray CFD, phase A

Non-reacting spray-chamber cases (water, methanol, 60/40 wt% water/methanol two-component cloud) to cross-check
the 0-D droplet model (module 09). Status labels: these are **executed** simulations; numerical verification is
limited to the A1-BLEND 1.5x grid check; nothing here is **experimentally validated**.

Host: native Debian 13 (trixie), OpenFOAM v2512 (ESI/OpenCFD apt package), Open MPI 5, 6 ranks. No Docker
(deviation from the job's docker plan, per James: run on Grok Bot's box). See PROVENANCE.md.

## Reproduce
```bash
curl -fsSL https://dl.openfoam.com/add-debian-repo.sh | sudo bash
sudo apt-get install -y openfoam2512 openfoam2512-tutorials python3-matplotlib
cd cfd
mkdir -p runs && cp -r /usr/lib/openfoam/openfoam2512/tutorials/lagrangian/sprayFoam/aachenBomb runs/A0
sed -i 's/numberOfSubdomains.*/numberOfSubdomains 6;/; s/(1 8 1)/(1 6 1)/' runs/A0/system/decomposeParDict
python3 scripts/make_cases.py          # writes runs/A1-*, runs/A2-*, runs/A1-BLEND-fine
(cd runs && ../run_case.sh A0 6)       # A0 smoke test (stock aachenBomb, n-heptane, reacting)
./run_batch.sh                         # remaining 7 cases sequentially + post-processing
python3 scripts/postprocess.py         # results/<case>.csv, .png, summary.json
```

## Cases (changes vs aachenBomb; see scripts/make_cases.py)
| | chamber | injection |
|---|---|---|
| A1 intake-like | 1.0 bar, 360 K air | liquid 300 K, ΔP 5 bar, d 0.25 mm, 5 ms |
| A2 compression-like | 20 bar, 700 K air | liquid 300 K, ΔP 100 bar, d 0.15 mm, 2 ms |

- Injected mass = Cd·A·sqrt(2·ρl·ΔP)·duration, Cd 0.9 (tutorial), top-hat rate profile.
- Gas: O2/N2 + H2O, CH3OH vapour; chemistry off, combustion none (non-reacting chamber). CH3OH NASA
  polynomials from GRI-Mech 3.0.
- Breakup: ReitzKHRT with the tutorial's (commented-out) default coefficients; the stock tutorial uses
  ReitzDiwakar, which A0 keeps. Evaporation liquidEvaporationBoil, wall interaction rebound, mesh 41x41x100
  (fine: 62x62x150) unchanged.
- Initial drop size: Rosin-Rammler as tutorial, scaled to orifice (λ = 0.79·d, max = d).
- writeInterval raised to 0.5 ms (output only) to save disk.

## Outputs
`results/<case>.csv` (penetration 95 % liquid mass, evaporated %, SMD, wall/escaped mass vs time, parsed from the
solver log), `results/<case>.png`, `results/summary.json` (end-of-injection values + grid check; each value is a row
of the named CSV). Evaporated % = 1 − (liquid in domain + escaped)/injected. Wall impact: rebound model, so wall
mass is not removed; penetration ≈ 100 mm means the spray reached the far wall.

## A0 status
A0 is **truncated at 4.0125 ms (smoke test)**, not run to its 10 ms endTime: stopped cleanly with `stopAt writeNow`
on 2026-10-23 01:06 PDT (job water-engine-20261023-001200) to save box time. Injection ends at 1.25 ms, so the
penetration history needed for the check is covered. Marker: `runs/A0/truncated.txt`; also the `status` field of
`results/summary.json` → `A0`.

## Known limitations (recorded per job water-engine-20261023-103500)
- **Wall interaction is `rebound`.** Parcels that reach a wall bounce back into the gas instead of forming a
  film. No wall film is modelled until module 13, so any wall-wetting and film evaporation (or the liquid
  loss to a film) is missing from these cases. Liquid that hits the far wall (penetration ≈ 100 mm) stays
  airborne, which biases late-time evaporated % compared with a filming wall. Module 09 removes bend-impinged
  liquid as wall film, so the two models treat walls differently.
- **Breakup models differ by case.** A0 keeps the stock aachenBomb `ReitzDiwakar` breakup (smoke test of the
  unmodified tutorial). A1/A2 use `ReitzKHRT` with the tutorial's commented-out default coefficients, because
  KH-RT is the more common choice for pressure-atomised sprays across the A1 (5 bar) to A2 (100 bar) ΔP range.
  A0 penetration is therefore not a like-for-like check of the A1/A2 breakup settings, and the KHRT
  coefficients are not calibrated to any measurement.
- These are model-to-model reference cases. Module 09's cross-check against them (nominal model A1 1.5–2.5×
  the CFD evaporated %, A2 +1 to +12 pp) is a known model difference, not a validation result. Module 09's
  `cfd_matched` variant is a sensitivity bound fitted to A1-/A2-BLEND only.
