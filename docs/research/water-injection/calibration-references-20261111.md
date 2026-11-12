# Water Engine calibration references

James designated these measured datasets as calibration references for Water Engine checks (11 Nov 2026, America/Los_Angeles). They are not interchangeable: each is a different method. None is a production-vehicle fuel-economy certification. The Water Engine model result they are checked against is model-only: naturally aspirated PRF91, water mass fraction w = 0.30 (water-to-fuel ratio 0.43), dry compression ratio 8 to wet 12, modelled power +10.16%, modelled cost per mile -9.728%.

Official open PDFs are kept in the private research archive. They are not copied to the public GitHub repository.

---

## 1. German RWTH Aachen / FEV — gasoline direct water injection — HIGH-TRUST

Designated by James at 12:44 AM on 11 Nov 2026.

**Source:** Hoppe, Thewes, Baumgarten, Dohmen, *International Journal of Engine Research* 17(1):86–96, 2016. DOI [10.1177/1468087415599867](https://doi.org/10.1177/1468087415599867). Legitimate open copy: [RWTH Publications 567619](https://publications.rwth-aachen.de/record/567619). Supporting context: Voßhall 2022 RWTH dissertation quoting Thewes 2016 Audi TT-S data, [RWTH Publications 860604](https://publications.rwth-aachen.de/record/860604).

**Engine:** laboratory single-cylinder gasoline (spark-ignition), condensed-water direct injection plus gasoline direct injection, Miller cycle and cooled exhaust-gas recirculation. This is the closer architecture match for Water Engine's planned injection path.

**Verified figures (from the open Hoppe et al. PDF):**

- About **3.3–3.8%** efficiency gain near minimum brake specific fuel consumption, stoichiometric, with Miller and cooled exhaust-gas recirculation.
- About **4.5%** near minimum fuel consumption when combined with homogeneous lean operation.
- Up to **16%** at full load. Caveat: that high-load figure uses an extrapolated dry (no-water) baseline.
- Miller plus condensate was enough up to about **1.0 MPa** brake mean effective pressure even at compression ratio **13.5**.

**Use for:** checking Water Engine efficiency claims against a measured gasoline water-injection map at the same displacement as the dry baseline. The model's larger -9.7% cost-per-mile result depends on an unmeasured dry compression-ratio 8 to wet 12 jump, which this dataset does not itself demonstrate.

---

## 2. Turkey, Ayhan and Ece 2019 — diesel direct in-cylinder water injection — CALIBRATION REFERENCE

Designated by James at 5:52 PM on 11 Nov 2026, alongside the German RWTH data, after the 4:30 PM discussion of how to combine the paper's fuel and power figures.

**Source:** Ayhan, V.; Ece, Y. M. *Tek silindirli bir dizel motora direkt su enjeksiyonunun performans ve emisyonlara etkisinin incelenmesi.* *İleri Teknoloji Bilimleri Dergisi* 8(1), 2019. Sakarya University of Applied Sciences. Official open PDF: https://dergipark.org.tr/en/download/article-file/719644

**Engine:** single-cylinder water-cooled direct-injection **diesel**, compression ratio **17.5**, full load; baseline effective power about **10 kW** near 2200 rpm. Water is injected directly into the cylinder through a head-mounted injector at **10, 20, 30, and 40%** of fuel mass. This is **not** a same-architecture match for Water Engine (naturally aspirated gasoline). Use it as a measured diesel direct-injection check, not as a direct prediction.

**Verified figures at 40% water (official body and abstract; conclusions paragraph notes below):**

- Brake specific fuel consumption about **-8.5%** at **1600 rpm**. The conclusions paragraph says **-7.5%**; the body figure of **8.5%** at the stated point is the one used for calibration.
- Maximum **power +6%** at **1200 rpm**.
- **NOx -38%** at **1200 rpm**.
- Effective efficiency about **+9%** at **1600 rpm** (consistent with the 8.5% fuel-consumption figure at that speed).
- Smoke / turbidity about **-28%** at **1200 rpm**.
- Hydrocarbons **+50%** at **2200 rpm**. This is a real downside.

**Do not add 8.5% and 6% together.** Fuel consumption per unit of power already includes any power change at that operating point. The 6% is peak power at a different speed. The honest combined claim is about 8.5% less fuel for the same work at 1600 rpm, plus up to 6% more peak power at 1200 rpm.

**Use for:** a measured diesel direct-water-injection sanity check on the model's -9.7% cost-per-mile result. The magnitudes are similar; the metrics and the engine type are not the same, so this is a check, not a match. Do not use third-party thesis summaries that quote NOx **-61.2%** at **100%** water; that ratio is not in this official paper.

---

## 3. Egypt, Attia and Kulchitskiy 2014 — water-in-fuel emulsion — CALIBRATION REFERENCE

Designated by James at 5:53 PM on 11 Nov 2026 as the calibration reference for **water mixed into the fuel** (emulsion), as distinct from injected water. He also directed research on how to improve on this paper's efficiency number.

**Source:** Attia, Ali M. A. (Benha University, corresponding) and Kulchitskiy, A. R. (Vladimir State University), *Influence of the structure of water-in-fuel emulsion on diesel engine performance,* *Fuel* 116 (2014) 703–708. DOI [10.1016/j.fuel.2013.08.057](https://doi.org/10.1016/j.fuel.2013.08.057). Official open Benha University staff copy: https://beng.stafpu.bu.edu.eg/Mechanical%20Engineering/4109/publications/Ali%20Mahmoud%20Ali%20Atya_Fuel%20Vol%20116%20pp%20703-708%202014.pdf

**Engine and method:** turbocharged three-cylinder **diesel**. Water-in-fuel emulsion made by membrane emulsification at **0.2 µm** and **0.45 µm**. Engine tests at **17% water by volume** and **0.5% emulsifier**. A body label of 19.75% water is **not** taken as the engine-test mixture; the official abstract and the body engine-test sentence both state 17%. This is an emulsion, not port or direct water injection, and it is diesel, not gasoline.

**Verified figures (official abstract; conclusions confirm the efficiency figure):**

- **Finer droplets** (the 0.2 µm membrane path): effective engine efficiency up to **+20%** (conclusions: up to **1.2 times** the efficiency on straight diesel). Smoke down **more than 80%**. Unburned hydrocarbons down **more than 35%**.
- **Larger droplets** (the 0.45 µm membrane path): **NOx** down as much as **25%**. The paper states that large droplets affect NOx more, while smaller droplets affect hydrocarbons, smoke, and efficiency.

**Related Egyptian work, not this calibration target:** Nour et al. 2016 and Farag et al. 2017 are exhaust- or intake-manifold water injection with exhaust-gas recirculation, not emulsions. Settled Farag 2017 figure: about **5%** lower fuel use with exhaust-manifold water at 25% exhaust-gas recirculation, versus recirculation alone. Do not use Nour/Farag “85%” or “88%” NOx as a water-only map.

**Use for:** the measured water-in-fuel efficiency target to improve on. The +20% is the strongest verified efficiency number in the country survey so far. It is diesel emulsion with controlled droplet size, not Water Engine's injection architecture, so any improvement path has to say whether it keeps the emulsion method, changes droplet size or water fraction, or tries a different method.

---

## How they sit together

| Reference | Method | Closest Water Engine use | Headline measured gain | Main caveat |
| --- | --- | --- | --- | --- |
| Hoppe et al. 2016, RWTH / FEV | Gasoline, direct water + gasoline | Architecture match (SI laboratory) | 3.3–3.8% efficiency near peak efficiency; up to 16% at full load | 16% uses an extrapolated dry baseline; does not measure a compression-ratio 8→12 jump |
| Ayhan and Ece 2019, Sakarya | Diesel, direct in-cylinder water | Fuel-use magnitude check only | About 8.5% lower BSFC at 1600 rpm; +6% peak power at 1200 rpm | Diesel, compression ratio 17.5; do not add the two percentages; HC +50% at 2200 rpm |
| Attia and Kulchitskiy 2014, Benha | Diesel, water-in-fuel emulsion, 17% water by volume | Water-in-fuel efficiency target | Effective efficiency up to +20% with finer droplets | Diesel emulsion, not injection; droplet size changes which gain you get (efficiency vs NOx) |

Country-survey notes: [Germany](country-survey/01-germany.md), [Turkey](country-survey/27-turkey.md), [Egypt](country-survey/46-egypt.md). M4 GTS hardware notes, including the original RWTH trust-tier entry: [bmw-m4-gts-bosch-waterboost-20261111.md](bmw-m4-gts-bosch-waterboost-20261111.md).

---

### Addendum (11 Nov 2026, evening): Attia droplet sizes and efficiency-improvement study

- Measured droplet D50 (Attia Fig. 5, after one month): **0.53 µm** (0.2 µm membrane) and **5.5 µm** (0.45 µm membrane). The 0.2/0.45 µm values are membrane pore sizes, not droplet sizes.
- The +20% is a best-point maximum from Fig. 7. Some points read only about +10–13%. At 2000 rpm / 35 kW the coarse emulsion matched the fine one. The paper does not define η_e.
- New supporting gasoline reference (water-in-gasoline emulsion): Tornatore et al. 2021, *Appl. Sci.* 11:9453, DOI 10.3390/app11209453. Indicated fuel use (gasoline only) **−3.7% / −7.1%** at 10 / 20 vol% water, measured only after moving to stoichiometric and knock-limited spark advance.
- Full checked study and ranked improvement paths: [egypt-efficiency-improvement-20261111.md](egypt-efficiency-improvement-20261111.md).
