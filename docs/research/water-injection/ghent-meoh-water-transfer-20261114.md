# Ghent methanol–water track → other Water Engine fuel mixes

**Question (James t1012u / t1013u, 14 Nov 2026, America/Los_Angeles):** can anything in the Ghent model help the project's *other* fuel mixtures reach **higher efficiency (BTE)**?

**This note:** originally research only (no improvement runs). The four follow-ups James later approved are reported in **Additional findings (Nov 14, 2026)** below and do not rewrite the earlier sections. No edits to Module 09 or Module 13. The live Ghent track (local branch `track/ghent-meoh-water-20261114`, not in this repository) was read, not written; another executor is editing it. NOx is secondary here.

**Status of all numbers below:** model-only estimates or already-executed (not validated) project results, plus verified literature. Nothing here is a claim that a bench will beat Ghent's measured 45.9% BTE, or that these deltas will appear on a real engine.

The original sections below are unchanged. Results of the four follow-ups James later approved are in **Additional findings (Nov 14, 2026)** at the end.

---

## Ghent mechanisms that actually raise efficiency

Source: Dierickx, Dejaegere, Peeters, Sileghem, Verhelst, *Fuel* 333 (2023) 126349, doi:10.1016/j.fuel.2022.126349 (Volvo Penta D7C-B TA, diesel-pilot + port methanol–water, 1500 rpm). Verified from the open accepted manuscript (doi:10.1016/j.fuel.2022.126349). VUB and UCLouvain figures used later in this note are also in [country-survey/21-belgium.md](country-survey/21-belgium.md). Track-local model: first-pass Ghent track result note, 14 Nov 2026 (local, not in this repository; PUSH=0).

Headline measured result: **45.9% BTE** at 12.3 bar, MeOH-50, MEF 38%. That is **+4.9 percentage points vs diesel-only (41.0%)** and **+3.3 pp vs the best pure-methanol point (42.6%)**. Water is a diluent / charge cooler, never a fuel.

What raised BTE (paper §5.4, confirmed in direction by the track):

1. **Earlier, more isochoric CA50.** The 50/50 blend shortened the useful heat-release window and moved CA50 earlier than diesel-only (~17° ATDC). This is the main efficiency mechanism.
2. **Methanol energy share (MEF) under a hard cap.** The optimum was 38%, not the maximum possible. Adding water *cut* the cap: max MEF at 12.3 bar fell from 75–76% (MeOH-100, knock) to **46% (MeOH-50, misfire)**. Water did **not** suppress knock in this diesel-pilot mode; it lengthened ignition delay and made the premixed spike worse, then flipped the limiter to misfire.
3. **Water fraction in the methanol** as charge cooler, not as a knock extender. MeOH-50 beat MeOH-64 and MeOH-100 on BTE at high load.

What the first-pass *model* added, quoted only vs its own 44.09% baseline (it under-predicts the headline point by **−1.81 pp**, so a modelled “win” of 1–2 pp is not a win over 45.9%):

| Candidate | Change | Model ΔBTE vs 44.09% | Note |
|---|---|---:|---|
| C3 | Stock CR 19, CA50 12.6°→10°, MEF 0.38→0.44 (still <46% misfire limit), same 50/50 blend | **+0.75 pp** | Most transferable: timing + energy share only |
| C2 | Same plus CR 19→21 | **+1.13 pp** | Hardware change; model NOx up (secondary) |
| C1 | Also an unphysical 274 K intake | +1.83 pp | Thrown out |

Calibration lesson (method, not a BTE mechanism): fit FMEP to the *dry / diesel-only* baseline, then judge wet deltas. A single Wiebe curve was too crude; a two-Wiebe (pilot + premixed) model is the approved next step on the Ghent track itself and should not be waited on for the estimates below.

**Track-only water cap:** `w_max = 0.3987` (MeOH-50 at MEF 0.48). Project-wide **`w ≤ 0.30` still applies to every other track and module.** The headline Ghent point is already `w = 0.3616`. It cannot be copied onto Track A/B, R34, QWE3, or Module 13 unless James raises the cap there too.

---

## Inventory of the other mixes

| Mix / track | What it is | Current efficiency picture (executed, not validated) | Where |
|---|---|---|---|
| Track B alcohols | SI CH3OH / C2H5OH, dry then water in 0.1-pp steps, spark re-optimised | CH3OH normal: **+1.45 / +1.43 pp** vs dry at w=0.227; C2H5OH normal: **+0.99 / +0.98 pp** at w=0.237; CH3OH hot humid: **+1.94 / +1.93 pp** at w=0.325 (already above the 0.30 cap) | project Track A/B status tables (selfdir-1410; not in this repository) |
| Track B gasoline / E-blends | PRF87/91/97, E10, E85; same water chains + later geometry/speed grids | Early cost-optimal w often ~0.10. Geometry headline: PRF87 hot, 1000 rpm, 105×131, w=0.30, CR 5→7: **+4.41 / +4.49 pp** vs a weak knock-limited dry CR. PRF97 normal 1000 rpm: cost/mile −7.94%. E85 normal at high rpm: water often does not pay | project Track B status tables; later geometry/speed shards (not in this repository) |
| Track B / A methane | CH4 SI + water | Dry already strong (η=0.4397 at CR 24, CA50 at MBT). Water cost gains exist (e.g. hot humid w=0.111); efficiency room is small | project Track A/B status tables (not in this repository) |
| Track A water-majority | SI, w>0.5, high CR, CH3OH / C2H5OH (and CH4) | CH3OH hot humid w=0.55, CR 26: **+9.42 / +9.36 pp** vs a low dry CR (baseline historically disputed). Conflicts with the current project-wide w≤0.30 rule | project Track A/B status tables (not in this repository) |
| R34 | Geometry/speed study, w=0.05–0.28, fuels CH3OH, C2H5OH, E85, E10, PRF87, PRF91 | This shard only (3881 pts): alcohol peaks ~52% indicated at CR 32; E10/E85/PRF gains vs w=0.05 of **+1.7 to +2.9 pp**. Not a global best table | a later geometry/speed shard (not in this repository) |
| QWE3 | Fine w grid on PRF91, w=0.02–0.30 | This shard (1202 pts): best **43.67%** at w=0.26, CR 11.75, CA50 4.1°; only **+0.31 pp** vs w=0.02 at the same CR. At fixed CR, extra water past ~0.26 is not buying much efficiency | a later fine-*w* shard (not in this repository) |
| Module 13 emulsion | Water-in-diesel spray + micro-explosion; Attia 2014 target (17% water by volume, up to **+20% relative** effective efficiency, finer droplets) | SPEC written; cycle coupling not a finished efficiency result. Must not rewrite Module 09 | the project's Module 13 emulsion work (not in this repository) |
| Module 04 six-stroke | Late water as steam working fluid, not a port blend | Separate mechanism; no Ghent-style CA50/MEF lever | Module 04 in the project model tree (not reproduced here) |
| Hydrogen + water | H2 is in the Module 03 fuel registry; there is **no completed H2+water efficiency track** | Literature only (below) | the Module 03 fuel registry and the literature surveys in this folder |
| VUB micro-turbine | Humid-air / steam-injected Turbec T100 | Electrical efficiency up to **+4.2 pp**, power +30%+, fuel +11% (abstracts). Not a piston mix | Belgium org survey item 5 |
| Idaho 2011 (WE-72) | Informational diesel-water comparison | Not a design track | an informational baseline note (not in this repository) |

Module 03 fuel registry includes H2, CH4, CH3OH, C2H5OH (plus Track B surrogates). Diesel is not in the Module 03 registry; the Ghent track stayed track-local for that reason.

---

## Per-mix: which Ghent mechanisms could raise BTE, and by roughly how much

Estimates are **incremental** BTE on top of the mix's current modelled best, at **w≤0.30**, model-only, with the Ghent model's −1.81 pp baseline error as a caution. Confidence: high / medium / low.

### 1. Track B gasoline surrogates, E10 (and knock-limited E85 / hot points)

**Best transfer.** These are spark-ignition and often knock-limited, so the Ghent *efficiency* idea (get CA50 earlier and more isochoric) works, but the path is the opposite of the diesel-pilot finding: in SI gasoline, water **does** suppress knock and that is how you earn the earlier CA50 and, if hardware allows, a bit more CR.

Verified SI water-injection efficiency, not Ghent: Hoppe, Thewes, Baumgarten, Dohmen, *Int. J. Engine Res.* 17(1):86–96 (2016), doi:10.1177/1468087415599867 (James's high-trust calibration reference): **3.3–3.8% efficiency** near minimum BSFC (about **+1.2 to +1.5 pp** if the dry point is ~38–40%), **4.5%** with lean operation, and up to 16% at full load against an *extrapolated* dry baseline. Track B's own geometry result already shows **+4.4 pp** when water lifts a knock-limited dry CR 5 to CR 7 (PRF87 hot, 1000 rpm) — large because the dry baseline is weak, not because 4 pp is waiting on every map point. QWE3 at fixed CR 11.75 only added **+0.31 pp** from w=0.02 to 0.26, with CA50 already ~4°.

| Ghent mechanism | Transfers? | Why |
|---|---|---|
| Earlier CA50 / more isochoric burn | Yes, if CA50 is still knock-late | Same efficiency physics; water helps knock in SI (Hoppe; also Hefei/JAC *Fuel* 282 (2020) 118839: **+3.8%** ITE at 1500 rpm WOT from knock mitigation — Chinese bench, UTS co-author, not an Australian bench) |
| Water as knock extender | Yes in SI; **do not** import Ghent's diesel-pilot “water did not suppress knock” | Different combustion mode |
| MEF / energy-share cap | Weak analog (φ / enrichment), not methanol share | Keep mixture at the efficient CA50, don't over-dilute |
| CR co-sweep with water | Yes, already started in the geometry study; Track B originally froze CR at the dry optimum | Ghent C2 was +1.13 pp for CR 19→21, with a NOx rise |
| FMEP-fit to a dry baseline | Yes, method | Fit to Hoppe's dry point before quoting new deltas |
| w up to 0.40 / MeOH-50 | No | Project cap w≤0.30; Hoppe/Track B already live in that band |

**Rough incremental BTE:** **+0.5 to +1.5 pp** on groups that still have late, knock-limited CA50 or a CR that has not been co-optimised with w. **~0 to +0.3 pp** where CA50 is already ~4–8° at fixed CR (QWE3-like). Do not add another +4 pp on top of the already-reported PRF87 hot geometry best; that gain is mostly already the Ghent-style mechanism. Confidence: **medium** for the direction and the 0.5–1.5 pp band; **low** for any larger number.

### 2. Track B methanol and ethanol

**Partial transfer.** Track B already adds water and re-optimises spark at every step, and already has **+1.0 to +1.5 pp** (normal) and **+1.9 pp** (CH3OH hot, at w=0.325). Ghent's own SI work is the right literature, not the D7C diesel-pilot result: Sileghem, Casier, Coppens, Vancoillie, Verhelst, FISITA F2014-CET-014 (2014, open PDF): hydrous ethanol 5/10/20% v/v, BTE **unaffected or even improved**, still above gasoline; suggested optimum **5–10% v/v** water (no verified percentage for the BTE gain). Sileghem et al., SAE 2013-01-1319: methanol–water 2.5/5/10% v/v, BTE not significantly different across the methanol fuels and higher than gasoline; NOx down (percentages paywalled, not used).

| Ghent mechanism | Transfers? |
|---|---|
| Earlier CA50 | Only if some best rows are still against the 15° CA50 cap rather than true MBT. Track B already runs a golden-section spark search (CA50 0–16°). Residual room is small. |
| Water as charge cooler | Already in the chain. Modest water is enough (Sileghem 5–10% v/v is well under w=0.30). Raising w toward Ghent's 0.40 is more likely to hit misfire / flame-speed limits than to add BTE. |
| MEF cap / misfire gate | Useful as a *protection*: add a misfire / S_L / T_tdc gate so the chain does not walk past the efficient region. Protects the existing +1–1.5 pp more than it adds a new one. |
| “Water does not suppress knock” | Does **not** transfer to these SI alcohols. |
| CR 21-style bump | Possible in principle; alcohols already run high CR when dry. Extra CR+water is Track A territory and fights w≤0.30. |

**Rough incremental BTE:** **+0.3 to +0.8 pp** if any current bests are still late-CA50; **~0** if they are already at MBT. Confidence: **medium-low** (optimizer already in the loop). Do not expect another Ghent-like +3–5 pp on top of the existing Track B alcohol gains.

### 3. Track B / Track A methane (CH4)

**Weak transfer.** Dry methane is already at MBT at high CR. There is no liquid-fuel evaporative cooling of the fuel itself; port water still cools the charge, but Ghent's methanol–water blend physics do not copy over. Existing water steps show cost/power movement more than a large efficiency story.

**Rough incremental BTE:** **0 to +0.5 pp**, and the sign is not guaranteed if dilution lengthens the burn. Confidence: **low**.

### 4. Track A water-majority (w>0.5)

**Little incremental transfer, and a constraint conflict.** The large reported +6 to +9 pp figures are mostly “water allows a much higher CR than a knock-limited dry point,” already in the model, and they sit on w>0.5, which the current project-wide cap forbids on any new work. Ghent's misfire finding is a warning, not a license to add more water: at high water the D7C limiter flipped to misfire and the useful fuel share fell. Track A already gates flame speed (S_L ≥ 0.08 m/s). Ghent's w_max=0.40 must not be applied here.

**Rough incremental BTE from Ghent mechanisms:** **0 to +0.5 pp** (CA50 polish only). Confidence: **low**. No recommendation to raise Track A water using the Ghent track.

### 5. Hydrogen + water (no completed project track)

**Strong literature transfer for power; only a modest BTE case.** This would be a *new* model-only track, not a patch to an existing mix.

- University of Melbourne, Mortimer, Poursadegh, Brear et al., *Fuel* 335 (2023) 126652 (verified in [country-survey/19-australia.md](country-survey/19-australia.md); not a Belgian bench): intake-manifold water on a hydrogen DI SI cylinder, CA50 held at **5 ± 1° ATDC**, water used to suppress autoignition. Result: **close to 25% more power** at efficient combustion phasing. Programme ITE ~47% is *not* stated as a water-only efficiency delta. Water-to-hydrogen ratios and BTE/NOx deltas are paywalled and unused.
- UCLouvain, Collette & Gatin, 2019 thesis ([country-survey/21-belgium.md](country-survey/21-belgium.md)): H2 HCCI + direct water, φ **0.2→0.5**, **+215% IMEPn**. That is power density (and lower ringing), not a verified BTE gain; authors note non-negligible uncertainties.
- UIR co-author paper ([country-survey/54-morocco.md](country-survey/54-morocco.md), abstract only): water vs water-methanol injection on a hydrogen SI engine; **volumetric efficiency +4%** with water injection; brake power slightly down; NOx down (no verified %).

The Ghent-like efficiency lever is: use water as a charge cooler so you can **keep an early CA50** (or a richer mixture at the same knock/ringing limit). If CA50 is already ~5°, BTE barely moves and the prize is power, as in Melbourne.

**Rough BTE if a new track is opened:** **+0.5 to +2 pp** only if the dry H2 point is knock-limited and late; otherwise **~0 pp BTE**, with a large power-density gain. Confidence: **medium** for the power direction; **low-medium** for a BTE number (the efficiency deltas in *Fuel* 335 were not open).

### 6. Module 13 diesel emulsion (Attia)

**Limited, indirect transfer.** Ghent is port methanol–water plus a diesel *pilot*, not a water-in-diesel emulsion. Attia & Kulchitskiy, *Fuel* 116 (2014) 703–708, doi:10.1016/j.fuel.2013.08.057: 17% water by volume, finer droplets, effective efficiency up to **+20% relative** (some points only +10–13%). That target is already the emulsion calibration reference; Ghent does not raise it.

What does transfer: when the spray model is coupled to a cycle, **fit FMEP to a dry-diesel baseline and sweep CA50 / diesel SOI**, because water changes ignition delay and efficiency will follow CA50 (the Ghent lesson). A poorly phased emulsion can also *lose* efficiency (the Auckland IMECE2014-38746 6% emulsion, misattributed to Monash in an early draft, had BSFC **+6.6%** — not an Australian result, recorded only as a caution).

**Rough incremental BTE:** **+0.5 to +2 pp** versus an emulsion point with poor CA50, once a cycle hook exists; **do not** treat this as a path to Attia's +20%, and do not rewrite Module 09. 17% water by volume is about w≈0.19 by mass, inside the 0.30 cap. Confidence: **low**.

### 7. Six-stroke (Module 04) and VUB humid turbine

No useful piston-mix BTE transfer. Six-stroke water is a late-cycle working fluid, not a premixed CA50/MEF problem. VUB's up to +4.2 pp electrical efficiency is a humidified micro-turbine, not a fuel mixer in this project.

---

## Ranked model-only follow-ups (efficiency first)

Do not run these until James picks them. Do not modify other tracks or Module 09/13 in this research task. Keep w≤0.30, PUSH=0.

1. **Track B gasoline / E10 / PRF — joint CA50 + CR + w sweep at knock-limited points (w≤0.30).** Apply the Ghent efficiency mechanism where it pays: earlier CA50 and a small CR co-opt, using water as an SI knock suppressant (Hoppe, not the D7C diesel-pilot result). Expected incremental BTE: **+0.5 to +1.5 pp** on late-CA50 groups; ~0 where CA50 is already early (QWE3-like). Confidence: **medium**. Highest chance of a real efficiency gain among existing mixes.

2. **Track B methanol / ethanol — misfire-aware CA50 retune at the current best w (cap 0.30, not 0.40).** Recheck best rows that sit on the 15° CA50 cap; add a misfire / flame-speed gate so water is not pushed past the efficient region (Sileghem 2014: 5–10% v/v already enough). Expected: **+0.3 to +0.8 pp** if any points are late; else ~0. Confidence: **medium-low**.

3. **FMEP-fit (or a track-local wrapper; no Module 09/13 edits) to Hoppe 2016 and/or Sileghem 2014 dry baselines, then re-quote wet BTE.** Pure method transfer from the Ghent track. This may not raise true BTE; it may correct the claimed delta by on the order of **±1 pp** (the Ghent model itself was 1.81 pp low on the wet headline). Confidence: **high** that honesty improves; **unknown** signed correction.

4. **New model-only hydrogen + water SI track** (leave existing tracks untouched; H2 is already in the fuel registry). Calibrate conceptually to Melbourne (efficient CA50≈5°, power +~25%) and treat UCLouvain as a power-density / ringing check, not a BTE target. Expected BTE: **+0.5 to +2 pp** only if dry H2 is late and knock-limited; otherwise the gain is power, not efficiency. Confidence: **low-medium** for BTE. Needs James's yes to open a track.

5. **Module 13 cycle coupling with a dry-diesel FMEP fit and a CA50/SOI sweep** (isolated hook, Module 09 untouched). Expected: **+0.5 to +2 pp** vs a badly phased emulsion point; not a claim on Attia's +20%. Confidence: **low**. Waits on the emulsion model work already in flight.

C2-style CR-only hardware bumps are left out of this list unless James wants them, same as on the Ghent track.

---

## Constraint conflicts

- **w≤0.30** remains in force outside the Ghent track. The Ghent headline point (w=0.36) and w_max=0.40 cannot be reused on Track A/B, R34, QWE3, or Module 13. Track B CH3OH hot already reports a best at **w=0.325**.
- **Module 09 and Module 13 are not to be rewritten or crossed.** Emulsion follow-up must stay on the Module 13 hook.
- **PUSH=0.** No merge or push of this note or of any follow-up branch without James's yes.
- Water is never a fuel in any mix.
- The Ghent two-Wiebe upgrade is in progress on the Ghent track; these estimates used the published first-pass RESULT.md and should be revisited if that calibration moves a lot.

---

## What needs James

1. Whether to run follow-up **#1** (gasoline/PRF CA50+CR+w sweep) as the first efficiency experiment on the other mixes.
2. Whether to **open a new model-only H2+water track** (#4). That is the one new mix with a large *power* literature result; the BTE case is weaker.
3. Whether the Track B CH3OH hot best at **w=0.325** should be pulled back to 0.30.
4. Whether he wants the **FMEP-to-Hoppe/Sileghem** honesty pass (#3) before any new “we beat the old Track B number” claim.
5. No request here to raise the project-wide water cap. If he wants that, it is a separate decision.

Sources used (all pre-existing, checked files; no new invented citations): the first-pass Ghent track result note and Dierickx et al. *Fuel* 333 (2023) 126349; Sileghem, Casier, Coppens, Vancoillie, Verhelst, FISITA F2014-CET-014 (2014, open PDF https://biblio.ugent.be/publication/5694558/file/5694573.pdf) and Sileghem et al., SAE 2013-01-1319 (NOx percentages paywalled, not used); [country-survey/21-belgium.md](country-survey/21-belgium.md) (UCLouvain 2019, VUB mHAT); [country-survey/19-australia.md](country-survey/19-australia.md) (Mortimer *Fuel* 335 (2023) 126652); Hefei/JAC *Fuel* 282 (2020) 118839 (Chinese bench, UTS co-author, not an Australian result); [country-survey/54-morocco.md](country-survey/54-morocco.md) (UIR abstract); [calibration-references-20261111.md](calibration-references-20261111.md) (Hoppe 2016, Attia 2014); project Track A/B status tables and later point shards (summaries only, not in this repository); Module 13 SPEC.

---

## Additional findings (Nov 14, 2026)

James t1013s4951 (14 Nov 2026, America/Los_Angeles) approved four model-only follow-ups from the list above: (a) dry-baseline recalibration, (b) gasoline/E10/PRF CA50+CR+*w* sweep, (c) methanol/ethanol CA50 retune, and (d) a new hydrogen+water SI track. They were run the same day on separate local branches (PUSH=0). **None of the headline findings above is changed:** the Ghent measured 45.9% BTE, the first-pass Ghent model table, the stored Track B wet ITE deltas (including CH3OH hot at *w* = 0.325), and the ranked expectations stay as written. New work stayed at *w* ≤ 0.30. Water is a diluent / charge cooler, never a fuel. Module 09, Module 13, and the live Ghent track were not edited.

Status of all new numbers: **model-only, executed, not experimentally validated.**

### (a) Recalibrate FMEP / heat-loss to Hoppe 2016 and Sileghem 2014 dry baselines

Local branch `track/recal-hoppe-sileghem-20261114`. Track-local wrapper around Module 03; no Module 03/09/13 edits.

Published dry baselines (open PDFs, digitised):

- Hoppe, Thewes, Baumgarten, Dohmen, *Int. J. Engine Res.* 17(1):86–96 (2016), doi:10.1177/1468087415599867, official RWTH copy. Figure 8, *n* = 3000 1/min, IMEP = 1.46 MPa: **dry indicated efficiency 39.4% ± 0.3 pp**. The model used RON95 E5 as Track B E10; 16% EGR was lumped as `residual_fraction = 0.16`. Miller early-IVC was not modelled and is absorbed into the heat-loss constant.
- Sileghem, Casier, Coppens, Vancoillie, Verhelst, FISITA F2014-CET-014 (2014), open PDF https://biblio.ugent.be/publication/5694558/file/5694573.pdf. Figure 3, 80 Nm, 2500 rpm: **dry E100 BTE 31.1% ± 0.3 pp**, gasoline (Euro 95) **28.5% ± 0.3 pp**.

Fitted constants:

| Lever | Value | Dry match | Notes |
|---|---|---|---|
| Hoppe Woschni *C* (heat loss) | **5.97** (default 3.26) | Held CA50 = 8°: model ITE **39.48%** vs 39.4% (**+0.08 pp**) | Unconstrained spark-opt on this geometry is knock-limited at CA50 **22.4°**, ITE 38.24% (−1.16 pp vs the paper). The fit used the held-CA50 point, which matches the measured phasing. |
| Sileghem FMEP | **1.48 bar** | Spark-opt CA50 7.1°: model BTE **31.15%** vs 31.1% (**+0.05 pp**) | Closing parameter at 80 Nm / 2500 rpm. Used only as a BTE conversion, the same way the Ghent track fitted FMEP to the diesel-only point. |

Literature checks (not rewrites of stored Track B numbers):

- Hoppe wet at *w* = 0.30 and at the paper's 50% water/fuel (*w* = 0.333) could not be run with the stock E10 / PRF Metghalchi–Keck *S_L* fits (*w* ≤ 0.10). The gasoline sweep in (b) used the existing Track B Cantera *S_L*(*w* = 0…0.30) cubics instead.
- Sileghem gasoline (PRF91 stand-in, same FMEP): model BTE **31.4%** vs measured Euro 95 **28.5%** (**+2.9 pp**). The ethanol-fitted FMEP does **not** transfer to gasoline. Do not treat 1.48 bar as a gasoline friction map.
- Sileghem E90W10 analog (*w* ≈ 0.123): model BTE **31.77%**, **+0.62 pp** vs dry E100. The paper reports no significant difference (error bars ~±0.4 pp). Direction is the same (flat to slightly up); the model is a little more optimistic.

Re-quoted Track B wet ITE deltas (default Track B engine, 86 × 86 mm, 2000 rpm). Gasoline rows use Hoppe *C* = 5.97; alcohol rows keep default *C* = 3.26. The stored selfdir-1410 wet *w* values and published ITE deltas are left on record; this table is a signed correction only.

| Chain | Published ITE Δ | Recalibrated ITE Δ | Signed correction | Recalibrated BTE Δ |
|---|---:|---:|---:|---:|
| CH3OH normal liquid, *w* = 0.227, CR 17 | +1.453 pp | +1.453 pp | **0.00 pp** | +1.744 pp |
| C2H5OH normal liquid, *w* = 0.237, CR 24 | +0.994 pp | +0.994 pp | **0.00 pp** | +1.291 pp |
| CH3OH hot humid_evap, *w* = 0.325, CR 8 | +1.941 pp | +1.941 pp | **0.00 pp** | +2.931 pp |
| CH3OH hot humid_evap, *w* = 0.30, CR 8 | (not a stored best) | +1.852 pp | — | +2.842 pp |
| PRF87 normal liquid, *w* = 0.10, CR 9 | +0.533 pp | +0.348 pp | **−0.185 pp** | +0.430 pp |
| PRF91 normal liquid, *w* = 0.10, CR 9 | +0.384 pp | +0.205 pp | **−0.179 pp** | +0.287 pp |
| E10 normal liquid, *w* = 0.10, CR 10 | +0.441 pp | +0.237 pp | **−0.204 pp** | +0.324 pp |

**Headline signed correction:** fitting heat loss to Hoppe's dry indicated efficiency **cuts the gasoline/E10 wet ITE gains by about 0.18–0.20 percentage points**. Alcohol ITE gains are unchanged. A constant 1.48 bar FMEP makes the same alcohol steps look 0.3–1.0 pp larger on a brake basis than on an indicated basis; that BTE view should not be treated as independently validated, given the gasoline transfer miss.

The later geometry-study headline (PRF87 hot, 1000 rpm, 105 × 131, *w* = 0.30, CR 5→7, +4.4 pp) was not re-quoted here. CH3OH hot *w* = 0.325 still exceeds the project-wide cap of 0.30 and is **not changed**. At the same hardware, *w* = 0.30 gives +1.852 pp ITE vs dry, 0.09 pp less than at 0.325.

Confidence: **medium** for the Sileghem dry E100 FMEP match and for the Hoppe dry ITE match at the measured CA50; **medium-low** for transferring Hoppe *C* onto the default Track B geometry and speed; **low** for using the Sileghem FMEP on gasoline or as a general BTE converter.

### (b) Gasoline/E10/PRF joint CA50+CR+*w* sweep on the recalibrated model

Local branch `track/gas-ca50-cr-w-20261114`. Hoppe-fitted Woschni *C* = 5.97, default Track B engine, *w* ≤ 0.30. Grid: PRF87, PRF91, E10 × normal/hot × 6 CRs × CA50 4–16° × *w* = 0, 0.10, 0.20, 0.25, 0.30 (1,260 points). Physical gates: *T*_IVC ≥ 280 K, *p*_max ≤ 160 bar, no knock, *S_L* ≥ 0.08 m/s, energy closure < 2%. 290 points passed; all 970 rejects were knock.

**Best same-hardware candidate (no CR change):** PRF87 normal, CR 9 (the dry knock-limited CR), *w* = 0.30, CA50 10° (dry was stuck at 16°). ITE **35.94%** vs dry **34.91%**, **+1.03 pp**. The same pattern holds for PRF91 at CR 10 (**+1.00 pp**, CA50 16°→10°) and E10 at CR 11 (**+1.01 pp**, CA50 16°→12°). *T*_IVC 294–296 K, *p*_max 50–56 bar.

**Best in the grid (CR also raised):** PRF87 normal, *w* = 0.30, CR 12, CA50 16°. ITE **37.92%**, **+3.01 pp** vs the best dry point (CR 9, 34.91%). E10 normal at CR 14, *w* = 0.30, CA50 16° is **39.00%**, **+2.44 pp** vs its own best dry (CR 11, 36.56%). These are hardware changes. Peak pressures stay modest (60–64 bar).

PRF87 hot had no eligible dry point in this CR grid. Wet points at *w* = 0.30 do run (best 34.66% at CR 9, CA50 16°), but a dry-to-wet delta is not quoted there.

This is the Ghent efficiency mechanism on an SI engine: water as a charge cooler lets the burn be phased earlier. Unlike Ghent's diesel-pilot result, water *does* suppress knock here. Item (a) re-quoted the old *w* = 0.10 default-CR chains at only **+0.21 to +0.35 pp** ITE; this sweep is larger because more water is used, CA50 is actually advanced, and CR can be co-optimised. The +1.0 pp same-CR figure is the fair comparison against “timing and water only.” The +2.4 to +3.0 pp figures need a piston/head change. Hoppe's measured 3.3–3.8% *relative* near min BSFC is about +1.2 to +1.5 pp at a ~39% baseline, in the same band as the same-CR result. These gains already use *C* = 5.97, so they should not be stacked on top of the item (a) −0.18 pp correction.

Confidence: **medium** for the same-CR **+1.0 pp** and for the direction of the CA50 advance; **medium-low** for the +3 pp CR-up candidates (the model was already more knock-limited than Hoppe's Miller engine when spark was left free).

### (c) Methanol/ethanol misfire-aware CA50 retune

Local branch `track/alcohol-ca50-retune-20261114`. Default Woschni *C* = 3.26 (item (a) did not refit alcohol heat loss). Default Track B engine. CA50 4–16° in 1° steps at the current best *w*, plus a spark-optimised wet point and the dry baseline. Every grid point passed the physical gates. No misfire flags.

There is **no extra efficiency** beyond the existing Track B spark optimiser. The discrete CA50 grid is 0.00–0.004 pp *below* the spark-optimised wet point (grid resolution). The stored alcohol gains already include the earlier CA50.

| Case | Dry (knock-limited) | Spark-opt wet | Best grid CA50 | ITE vs dry | vs spark-opt |
|---|---|---|---|---:|---:|
| CH3OH normal liquid, *w* = 0.227, CR 17 | 42.38% at CA50 14.6° | 43.83% at CA50 9.6° (MBT) | 43.83% at 10° | **+1.45 pp** | −0.003 pp |
| C2H5OH normal liquid, *w* = 0.237, CR 24 | 44.58% at CA50 13.7° | 45.57% at CA50 11.6° (MBT) | 45.57% at 12° | **+0.99 pp** | −0.004 pp |
| CH3OH hot humid_evap, *w* = 0.325, CR 8 (existing) | 35.02% at CA50 13.5° | 36.96% at CA50 6.0° (MBT) | 36.96% at 6° | **+1.94 pp** | −0.000 pp |
| CH3OH hot humid_evap, *w* = 0.30, CR 8 (cap) | 35.02% at CA50 13.5° | 36.87% at CA50 5.9° (MBT) | 36.87% at 6° | **+1.85 pp** | −0.000 pp |

The stored CH3OH hot humid_evap best at ***w* = 0.325 is not changed.** At the same hardware, *w* = 0.30 is **0.09 pp** lower. No misfire appeared at either water level down to CA50 4°. This is consistent with Sileghem 2014 (BTE “unaffected or even improved” at 5–10% v/v water). The residual +0.3 to +0.8 pp suggested in the ranking above is **not supported** on these default-engine points.

Confidence: **high** that a tighter CA50 grid will not beat the existing spark optimiser on these four points; **medium** that these ITE deltas remain the right alcohol numbers after item (a), because heat loss was not refit for alcohols.

### (d) New model-only hydrogen+water SI track

Local branch `track/h2-water-20261114`. Calibrated conceptually to University of Melbourne, Mortimer, Poursadegh, Brear et al., *Fuel* 335 (2023) 126652, doi:10.1016/j.fuel.2022.126652, using the open ARENA / Melbourne Energy Institute conditions already recorded in [country-survey/19-australia.md](country-survey/19-australia.md): Caterpillar C15, one cylinder converted to hydrogen DI SI; CR 12 and 14; 0.4 bar boost; CA50 = 5 ± 1° ATDC; water in the intake airstream; **close to 25% more power** at efficient phasing. Programme ITE ~47% is *not* a water-only delta. Water-to-hydrogen ratios and BTE deltas in the *Fuel* paper are paywalled and were not used.

Geometry used: bore × stroke **137 × 171 mm** (published C15 15.2 L six-cylinder; not in the open ARENA excerpt). Speed **1500 rpm** assumed (genset-like; not stated in the open survey sources). *p*_IVC = 1.4 bar. Grid: CR 12/14 × φ 0.40/0.60/0.80/1.00 × *w* = 0…0.30 × CA50 4–12° (336 points). 230 passed; 93 knock rejects; a handful of state-inversion failures, all rejected. No FMEP was fitted (no open Melbourne dry BTE). All efficiencies below are **gross indicated**.

| Comparison | Dry | Wet (*w* ≤ 0.30) | Δ |
|---|---|---|---|
| Best ITE in the grid (lean, already early CA50) | 46.20% at CR 14, φ = 0.4, CA50 6°, IMEP 8.68 bar | 46.35% at CR 14, φ = 0.4, *w* = 0.30, CA50 6°, IMEP 8.82 bar | **+0.16 pp ITE** |
| Stoichiometric, allowing CR to rise | 39.94% at CR 12, φ = 1.0, CA50 10° (knock-limited) | 41.64% at CR 14, φ = 1.0, *w* = 0.30, CA50 8° | **+1.70 pp ITE** |

The 46.2–46.4% ITE sits next to the ARENA programme figure of ~47% indicated as a sanity check only (different operating points, and not a water-only result).

At Melbourne's CA50 = 5°, this is a **power** story: dry hydrogen knocks at CR 12 once φ exceeds 0.6, and at CR 14 once φ exceeds 0.4. With *w* = 0.30 the CR 12 cylinder can run **φ = 1.0** without knock. Richest knock-free dry (CR 12, φ = 0.6): ITE 43.12%, IMEP 11.51 bar. Richest knock-free wet (*w* = 0.30, CR 12, φ = 1.0): ITE 40.24%, IMEP 16.23 bar. Change: **−2.88 pp ITE**, **+41% IMEP**. Melbourne reported close to 25% more power at efficient phasing. The model has the same direction and a larger power gain. Indicated efficiency *falls* at that power-optimal point because the mixture is no longer lean. *T*_IVC on the wet points is 310–315 K. Peak pressure at the φ = 1, *w* = 0.30, CR 14 point is 113 bar, inside the 160 bar gate.

Confidence: **medium** for the direction (water extends the hydrogen knock limit and raises power at early CA50; also consistent with UCLouvain's H2 HCCI ringing control, which was a power-density result, not a BTE target); **low-medium** for the +41% IMEP magnitude and for the +0.16 / +1.70 pp ITE numbers (bore, stroke and speed are documented assumptions; the *Fuel* paper's water ratios were not used; this is 0-D premixed, not the bench's DI hydrogen jet); **high** that peak ITE does not move much once CA50 is already ~5–6° and the mixture stays lean.

### What these runs change about the earlier estimates

- The gasoline same-hardware gain landed in the predicted **+0.5 to +1.5 pp** band (**+1.0 pp** ITE; confidence **medium**). The +2.4 to +3.0 pp figures are CR-up hardware changes (confidence **medium-low**).
- The alcohol retune confirmed the existing **+1.45 / +0.99 / +1.94 pp** ITE figures and found **no extra** CA50 room (confidence **high** that a tighter grid will not help). The residual +0.3 to +0.8 pp in the ranking above is not supported on these default-engine points.
- The Hoppe dry fit **cuts** previously quoted gasoline/E10 wet ITE deltas by **0.18–0.20 pp**; alcohol ITE deltas are unchanged (**0.00 pp**). Existing stored Track B numbers are not rewritten.
- The new hydrogen track's lean peak is **+0.16 pp ITE**; the larger modelled number is **power (+41% IMEP at CA50 = 5°)**, with a stoich+CR alternative of **+1.70 pp ITE**. That matches the earlier “power first, modest BTE” reading of the Melbourne literature.

CH3OH hot *w* = 0.325 remains on record and is **not** pulled back. New work uses *w* ≤ 0.30; at the same hardware the cap point is 0.09 pp lower. No request here to raise the project-wide water cap, to rewrite Module 09/13, or to change the live Ghent track.
