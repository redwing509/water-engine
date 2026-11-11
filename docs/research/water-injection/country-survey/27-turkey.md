# Turkey — water in the combustion cycle (checked)

Status: DONE (checked). Hermes draft plus a verification section.
Hermes job: `20261111-140245-we-survey-27-turkey-water-in-combustion` (started 2:02 PM, ended 2:06 PM America/Los_Angeles, 11 Nov 2026; runtime about 3 min; RESULT STATUS: DONE, rc 0).
Prompt language: Turkish. Report language: English.

The Hermes text starts below. For numbers, prefer the verification section at the end.

---

# Turkey — water in the combustion cycle (Hermes draft)
Country: Turkey
Prompt language: Turkish
Author: Hermes (box hjob)
Date: 2026-11-11

## 1. Executive summary

This survey covers documented work in Turkey (1926–2026) where water is introduced into a vehicle engine's combustion cycle: water injection (port, direct, compressor-after), water-methanol injection, water-fuel emulsions (including diesel-water), in-cylinder steam/water cycles, and six-stroke engines with water injection. Ordinary jacket cooling, windshield washer fluid, and AdBlue/DEF/urea (exhaust after-treatment) are excluded — mentioned here only to note the boundary.

**Key findings:**
- **No production or near-production road vehicles** from Turkish OEMs (Tofaş, Ford Otosan, Oyak Renault, Toyota Türkiye, Hyundai Assan) use water injection in the combustion cycle. Their R&D centers focus on conventional DI, turbocharging, EGR, and after-treatment.
- **Strong university research base** exists, especially at Gazi University (six-stroke water injection), Istanbul Technical University / Yıldız Technical University (water-diesel emulsion thermodynamics), and Sakarya University (direct water injection, steam injection, emulsified fuels).
- **Multiple experimental studies** demonstrate NOx reductions of 10–27%, thermal efficiency gains of 7–10% (six-stroke), but with BSFC penalties of 5–9% for emulsified fuels.
- **Patents**: Aygaz (additive injection system, priority TR 2013/15663), Tofaş (engine cooling system TR201310902A2 — not combustion water injection), ITU (rotary engine PCT/TR2018/050177).
- **Aviation/marine transfer**: ITU and Yıldız Technical University marine engineering departments have studied water injection and water-diesel emulsion for ship diesel engines (IMO NOx compliance).
- **Water-methanol injection**: No peer-reviewed Turkish university research found; only aftermarket kit suppliers (Bosporus Innovations, etc.) and forum discussions.
- **Negative areas**: No documented work from TÜBİTAK MAM on combustion water injection; no historical Anadol/BMC/TEMSA/Otokar water-injection records found; no racing/prototype programs documented.

---

## 2. Production or near-production road vehicles

**None found.** Searches of Tofaş, Ford Otosan, Oyak Renault, Toyota Türkiye, Hyundai Assan public disclosures, patent portfolios, and technical press reveal no water-in-combustion systems in production or pre-production vehicles. All four major Turkish OEMs operate R&D centers (Tofaş Bursa — Stellantis Europe's only non-Italian center; Ford Otosan Gölcük — one of Ford's three global centers) but their published work centers on conventional DI, Miller/Atkinson cycles, EGR, SCR, and electrification. No water injection patents assigned to these OEMs with combustion-cycle scope were located.

*Boundary note*: Tofaş holds TR201310902A2 / EP3047124A2 / WO2015038087A2 "Bir motor soğutma sistemi" (engine cooling system) — jacket/coolant-circuit only, not combustion water injection. Aygaz (LPG distributor, not an OEM) holds US9551305B2 (priority TR 2013/15663) for an additive safety/injection system for fluidic fuels (LPG/LNG/CNG), not water.

---

## 3. Research, prototypes, and supplier systems

### 3.1 Six-stroke engine with direct water injection — Gazi University (2012–2016)

| Item | Detail |
|------|--------|
| **Organization** | Gazi University, Faculty of Technology, Department of Automotive Engineering (Ankara) |
| **Years** | 2012–2016 (PhD thesis 2014; journal papers 2015–2016) |
| **Engine / vehicle** | Single-cylinder, four-stroke gasoline engine converted to six-stroke via new cam mechanism; LPG fuel |
| **What was done** | Water injected directly into cylinder during 5th stroke (exhaust heat recovery stroke). Three injection timings (BTDC, TDC, ATDC), four pressures (25, 50, 75, 100 bar), constant duration. Stoichiometric λ=1, 2250–3500 rpm, full load. |
| **Measured results** | Exhaust gas temp −7%; specific fuel consumption −9%; thermal efficiency +8.72%; power output +10%; CO −21.97%, HC −18.23% (≤3000 rpm); NO decreased (lower end-cycle temperature). Brake torque +12.27% average vs. four-stroke baseline. |
| **Source** | Arabaci E., İçingür Y., Solmaz H., Uyumaz A., Yılmaz E., "Experimental investigation of the effects of direct water injection parameters on engine performance in a six-stroke engine," *Energy Conversion and Management*, Vol. 98, pp. 89–97, 2015. DOI: 10.1016/j.enconman.2015.03.045. Project TEF-07/2012-05 (Gazi University Scientific Research Foundation). Thesis: "Dört zamanlı buji ateşlemeli bir motorun egzoz ısısı geri kazanımı ile altı zamanlı bir motora dönüştürülmesi…" (Gazi Univ., 2014, Turkish). Follow-up: Arabaci & İçingür, "Thermodynamic investigation of experimental performance parameters of a water injection with exhaust heat recovery six-stroke engine," *Journal of the Energy Institute*, 89(4), 569–577, 2016. DOI: 10.1016/j.joei.2015.06.006. |

### 3.2 Water-diesel emulsion (WDE) — Istanbul Technical University / Yıldız Technical University (2020–2023)

| Item | Detail |
|------|--------|
| **Organization** | ITU (Marine Engineering) / Yıldız Technical University (Marine Engineering & Naval Architecture) — joint authorship |
| **Years** | 2020–2023 |
| **Engine / vehicle** | Single-cylinder diesel engine, full load, max torque & max power regions |
| **What was done** | Surfactant-stabilized water-diesel emulsions at 5% (W5), 10% (W10), 15% (W15) water by volume. Experimental tests + thermodynamic simulation (AVL Boost) + multi-criteria optimization (Fuzzy-AHP, CODAS). |
| **Measured results** | **Max torque region**: brake power −5.22% (W15), BSFC +7.42% (W15), NOx −16.84% (W15). **Max power region**: brake power −5.46%, BSFC +8.96%, NOx −10.8% (W10 optimum by Fuzzy-AHP/CODAS). Theoretical results agree with experiment. |
| **Source** | Okumuş F., Kaya C., Kökkülünk G., "NOx based comparative analysis of a CI engine fueled with water in diesel emulsion," *Energy Sources, Part A*, 45(3), 6710–6729, 2023. DOI: 10.1080/15567036.2020.1839147. Okumuş F., Kökkülünk G., Kaya C., Aydın Z., "THERMODYNAMIC ASSESSMENT OF WATER DIESEL EMULSIFIED FUEL USAGE IN A SINGLE CYLINDER DIESEL ENGINE," *Energy Sources, Part A*, 45(2), 3708–3721, 2023. DOI: 10.1080/15567036.2021.1900458. ITU research portal records confirm affiliation. |

### 3.3 Direct water injection (DWI) and steam injection — Sakarya University of Applied Sciences (2009–2020)

| Item | Detail |
|------|--------|
| **Organization** | Sakarya University / Sakarya University of Applied Sciences, Technology Faculty, Mechanical Engineering (Sakarya) |
| **Years** | 2009 (PhD) – 2020 (journal) |
| **Engine / vehicle** | Single-cylinder, water-cooled, direct-injection diesel engine (1 L naturally aspirated, bowl-in-piston) |
| **What was done** | **PhD (Ayhan 2009)**: Steam injection and liquid water injection (port, emulsified, direct) compared. **Journal 2016**: Steam (133°C) and liquid water (20°C) injected at intake manifold; emulsified fuels (2% surfactant). **Applied Energy 2020**: Electronically controlled direct water injection at compression stroke (dedicated injector on cylinder head). Water/fuel mass ratios 10–100% (W10–W100). Injection timing swept; optimum 270°CA BTDC (compression stroke). |
| **Measured results** | **2020 DWI**: Optimum water ratio 60% (W60) — engine power increased, SFC decreased. NOx reduced significantly (exact % not in abstract; paywalled). **2016**: Steam injection more effective than liquid water for NOx reduction at same water mass; emulsified fuel reduced NOx but increased BSFC. **PhD 2009**: Steam injection reduced NOx and soot; baseline data in thesis. |
| **Source** | Ayhan V., "New application to reduce NOx emissions of diesel engines: Electronically controlled direct water injection at compression stroke," *Applied Energy*, 260, 114328, 2020. DOI: 10.1016/j.apenergy.2019.114328. Project 2018-2-7-2 (Sakarya Univ. Applied Sciences BAP). Ayhan V., "Direkt enjeksiyonlu bir dizel motoruna buhar ve farklı yöntemlerle su gönderiminin performans ve NOx emisyonlarına etkilerinin incelenmesi," *SAÜ Fen Bil Der*, 20(3), 463–471, 2016. DOI: 10.16984/saufenbilder.91773. Ayhan V., PhD thesis "Bir dizel motoruna buhar enjeksiyonunun NOx ve is emisyonlarına etkisinin araştırılması," Sakarya University, 2009. Tunca S., Ayhan V., Çay Y., Çeşur İ., "Direkt Enjeksiyonlu Bir Dizel Motorunda Stabilize Emülsife Yakıt Kullanımının Etkilerinin İncelenmesi," *Academic Platform J. Eng. Sci.*, 5(3), 41–48, 2017. DOI: 10.21541/apjes.325971. |

### 3.4 Water addition into intake air (WAIA) — automotive diesel engine

| Item | Detail |
|------|--------|
| **Organization** | Affiliation not fully resolved in open sources; likely Turkish university (author names: Mustafa TUTİ, Zehra ŞAHİN, Orhan DURGUN) |
| **Years** | 2023 (conference) / 2024 (journal) |
| **Engine / vehicle** | Automotive diesel engine, 2000–4000 rpm, full load |
| **What was done** | Water added to intake air at 2, 4, 6, 8, 10% ratios. Cylinder pressure, temperature, heat release rate (HRR), combustion duration (CD), energy balance measured. Empirical correlation for CD developed via multi-curve fitting. |
| **Measured results** | Cylinder pressure generally increased at 2000, 2500, 3500 rpm; decreased at 3000, 4000 rpm. Max cylinder temp shifted farther from TDC. HRR generally decreased (except 3000 rpm). CD shortened at all speeds under full load (e.g., 2000 rpm: NDF 13.10°CA → 12.68°CA at 8.32% water). Effective power/chemical energy decreased at 2000 rpm, increased at high water ratios at 4000 rpm. |
| **Source** | TUTİ M., ŞAHİN Z., DURGUN O., "Experimental Investigation of the Effects of Water Addition into the Intake Air on Combustion Parameters, Energy Balance and Developing an Empirical Combustion Duration Relation in Automobile Diesel Engine," presented at 23rd Congress on Thermal Science and Technology, Gaziantep, 2023; journal version in DergiPark (M6_2023_015). Open access PDF available. |

### 3.5 Three-phase diesel emulsion (oil/water/oil) — Gazi University (2013)

| Item | Detail |
|------|--------|
| **Organization** | Gazi University, Faculty of Engineering & Architecture (Ankara) |
| **Years** | 2013 |
| **Engine / vehicle** | Diesel engine (details in paper) |
| **What was done** | Three-phase emulsion (diesel/water/diesel) with 1% monoethylene glycol as co-surfactant. Tested 10% water (E1) and 15% water (E2). |
| **Measured results** | E1: emissions partially reduced, performance significantly reduced. E2: CO −45.9%, NOx −26.9%, soot −18.8%; **torque −15.72%**. |
| **Source** | Yılmaz E., Solmaz H., Polat S., Altın M., "Üç-Fazlı Dizel Emülsiyon Yakıtlarının Motor Performansı Ve Egzoz Emisyonlarına Etkisi," *Gazi Üniversitesi Mühendislik Mimarlık Fakültesi Dergisi*, 28(1), 127–134, 2013. DOI (TR Dizin): 10.29130/dubited.575123 (open access PDF on DergiPark). |

---

## 4. University and institute work (additional)

### 4.1 Çukurova University — Water-biodiesel emulsion (2022)

- **Thesis**: Gökçeli E., "Performance and emission characteristics of a diesel engine operated with water-biodiesel emulsion fuels," MSc, Çukurova Univ., 2022. Advisor: Dr. Erdi Tosun.
- **Fuels**: D (diesel), DS5 (93% D + 5% water + 2% surfactant), DS10, B (biodiesel), BS5, BS10. Mechanical stirring 1500 rpm, 1 hr.
- **Results**: Emulsion fuels reduced torque, brake power, CO, and NOx. (Full thesis open access via RDL Thesis repository.)
- **Tag**: Biodiesel-water emulsion.

### 4.2 Yıldız Technical University — Steam injection for biodiesel NOx control (2012)

- **Thesis**: Çoşgun T., "A theoretical and experimental study on the effects of water steam injection on NOx emissions of direct injection diesel engine running with different biodiesel blends," MSc, Yıldız Technical Univ., 2012. Advisor: Prof. Adnan Parlak.
- **Method**: Single-cylinder DI diesel, methyl esters (10%, 20% blend), steam injection 10–30% at intake manifold. Single- and two-zone combustion modeling validated with experiment.
- **Tag**: Aviation/marine (Naval Architecture dept.), steam injection.

### 4.3 ITU — Marine diesel water injection for NOx (conference/journal)

- **Paper**: "A study on exhaust emissions reduction system for marine diesel engines" (ITU research portal). Water injection to charge air (humid air motor concept) on medium-speed diesel engine aboard general cargo ship. MARPOL compliance testing. NOx reduction ~70% without optimization; engine performance almost unaffected; CO/CO₂ unchanged.
- **Authors**: ITU Marine Engineering / Naval Architecture group.
- **Tag**: Marine.

### 4.4 Other university mentions (abstract only / not verified)

- **Mehmet Akif Ersoy University** (Burdur) — co-author on Gazi six-stroke paper (Arabaci et al. 2015 lists Emin Gülmez High Vocational School affiliation).
- **Boğaziçi, Uludağ/Bursa, TÜBİTAK MAM** — no open water-in-combustion publications found in search. TÜBİTAK MAM's Energy Technologies department focuses on hydrogen, fuel cells, turbine blades, and grid storage; no combustion water-injection projects listed on public project pages.

---

## 5. Historical / racing / aviation-marine transfer (labeled)

| Label | Detail |
|-------|--------|
| **Aviation** | ITU / Yıldız Technical University marine engineering work on water-diesel emulsion is primarily for marine diesel (IMO Tier III). No Turkish aviation water-injection research found except TÜBİTAK MAM turbine blade materials (1350°C) — not combustion water injection. KAAN/F110 engine program uses conventional cooling. |
| **Marine** | ITU: "A study on exhaust emissions reduction system for marine diesel engines" — water injection to charge air on ship engine, ~70% NOx reduction. Yıldız Technical: Okumuş et al. water-diesel emulsion papers authored by Marine Engineering / Naval Architecture faculty. These explicitly target maritime NOx compliance. |
| **Racing / prototype** | No documented Turkish racing team or prototype program (e.g., Formula Student, rally, track) using water or water-methanol injection in peer-reviewed literature. Aftermarket kits (Snow Performance, Aquamist, local suppliers like Bosporus Innovations) are sold in Turkey but no academic validation from Turkish labs found. |
| **Historical OEMs** | Anadol, BMC, TEMSA, Otokar, Mercedes-Benz Türk — no archival patents, technical reports, or theses found referencing water injection in combustion cycle. |

---

## 6. Water-fuel emulsions and other cycles

Covered in Sections 3.2, 3.3, 3.5, 4.1. Summary:

| Cycle / Method | Institutions | Water % | Key Result |
|----------------|--------------|---------|------------|
| Water-diesel emulsion (2-phase, surfactant) | ITU/Yıldız Tech | 5–15% | NOx −10 to −17%; BSFC +7–9%; power −5% |
| Water-diesel emulsion (3-phase, oil/water/oil) | Gazi Univ. | 10–15% | NOx −27% (E2); torque −15.7% |
| Direct water injection (compression stroke) | Sakarya Univ. | 10–100% | Optimum 60% water: power ↑, SFC ↓, NOx ↓ |
| Steam injection (intake manifold) | Sakarya Univ., Yıldız Tech | 10–30% | NOx ↓, soot ↓; steam > liquid water for NOx |
| Water addition to intake air (WAIA) | Unresolved Turkish univ. | 2–10% | CD shortened; power ↓ at low rpm, ↑ at high rpm |
| Six-stroke with water injection (exhaust heat recovery) | Gazi Univ. | Variable (pressure 25–100 bar) | Thermal eff. +8.7%; SFC −9%; NOx ↓ |

---

## 7. Negative results or "nothing found" areas

| Area | Search performed | Outcome |
|------|------------------|---------|
| **OEM production water injection** | Tofaş, Ford Otosan, Oyak Renault, Toyota Türkiye, Hyundai Assan patent portfolios (TR/EP/US), technical press, R&D disclosures | None. Only conventional DI, EGR, SCR, electrification. |
| **Water-methanol injection (academic)** | "su metanol enjeksiyonu" + university names, TR Dizin, Google Scholar, DergiPark | Only aftermarket kit vendors (Bosporus Innovations, autopartia.com) and forum threads. No peer-reviewed Turkish university paper. |
| **TÜBİTAK MAM combustion water injection** | MAM website (enerji, projeler, malzeme), project lists, publications | No projects on water-in-combustion. Focus: hydrogen, fuel cells, turbine materials, grid storage, ceramic membranes. |
| **Historical Anadol/BMC/TEMSA/Otokar/Mercedes-Benz Türk** | Patent search (TR, EP), thesis repositories, TR Dizin, academic archives | No records of water injection in combustion cycle. |
| **Racing / Formula Student / prototype teams** | Search: "su enjeksiyonu" + "yarış", "formula student", "prototi̇p", "takım" + Turkish univ. names | No documented systems in open literature. |
| **Six-stroke beyond Gazi** | Search: "altı zamanlı" + "su enjeksiyonu", "six-stroke" + Turkey | Only Gazi group (Arabaci et al.) and citing papers (Korea, Bitlis Eren Univ. theoretical review). |

---

## 8. Source list (only real citations; legitimate open copies preferred)

1. **Arabaci E., İçingür Y., Solmaz H., Uyumaz A., Yılmaz E.** (2015). *Experimental investigation of the effects of direct water injection parameters on engine performance in a six-stroke engine.* Energy Conversion and Management, 98, 89–97. DOI: 10.1016/j.enconman.2015.03.045. [Open access via ScienceDirect (paywalled); author preprint on Gazi AVESİS: https://avesis.gazi.edu.tr/yayin/d9027181-f2cd-427d-afcd-52edf469a827]

2. **Arabaci E., İçingür Y.** (2016). *Thermodynamic investigation of experimental performance parameters of a water injection with exhaust heat recovery six-stroke engine.* Journal of the Energy Institute, 89(4), 569–577. DOI: 10.1016/j.joei.2015.06.006.

3. **Thesis (Turkish)**: *Dört zamanlı buji ateşlemeli bir motorun egzoz ısısı geri kazanımı ile altı zamanlı bir motora dönüştürülmesi ve motor performans ve emisyon karakteristiklerinin incelenmesi.* Gazi University, 2014. [Tezara: https://tezara.org/theses/371607]

4. **Okumuş F., Kaya C., Kökkülünk G.** (2023). *NOx based comparative analysis of a CI engine fueled with water in diesel emulsion.* Energy Sources, Part A, 45(3), 6710–6729. DOI: 10.1080/15567036.2020.1839147. [ITU research portal: https://research.itu.edu.tr/en/publications/nosubxsub-based-comparative-analysis-of-a-ci-engine-fueled-with-w]

5. **Okumuş F., Kökkülünk G., Kaya C., Aydın Z.** (2023). *THERMODYNAMIC ASSESSMENT OF WATER DIESEL EMULSIFIED FUEL USAGE IN A SINGLE CYLINDER DIESEL ENGINE.* Energy Sources, Part A, 45(2), 3708–3721. DOI: 10.1080/15567036.2021.1900458. [ITU research portal: https://research.itu.edu.tr/en/publications/thermodynamic-assessment-of-water-diesel-emulsified-fuel-usage-in]

6. **Ayhan V.** (2020). *New application to reduce NOx emissions of diesel engines: Electronically controlled direct water injection at compression stroke.* Applied Energy, 260, 114328. DOI: 10.1016/j.apenergy.2019.114328. [Project 2018-2-7-2 acknowledged; paywalled, no legitimate open copy found — mark numbers as paywalled.]

7. **Ayhan V.** (2016). *Direkt enjeksiyonlu bir dizel motoruna buhar ve farklı yöntemlerle su gönderiminin performans ve NOx emisyonlarına etkilerinin incelenmesi.* SAÜ Fen Bil Der, 20(3), 463–471. DOI: 10.16984/saufenbilder.91773. [Open access on DergiPark: https://dergipark.org.tr/en/download/article-cite-file/270005/type/6]

8. **Ayhan V.** (2009). *Bir dizel motoruna buhar enjeksiyonunun NOx ve is emisyonlarına etkisinin araştırılması.* PhD thesis, Sakarya University. [Referenced in later papers; full thesis not located open.]

9. **Tunca S., Ayhan V., Çay Y., Çeşur İ.** (2017). *Direkt Enjeksiyonlu Bir Dizel Motorunda Stabilize Emülsife Yakıt Kullanımının Etkilerinin İncelenmesi.* Academic Platform J. Eng. Sci., 5(3), 41–48. DOI: 10.21541/apjes.325971. [Open access: https://dergipark.org.tr/en/download/article-file/347830]

10. **Yılmaz E., Solmaz H., Polat S., Altın M.** (2013). *Üç-Fazlı Dizel Emülsiyon Yakıtlarının Motor Performansı Ve Egzoz Emisyonlarına Etkisi.* Gazi Üniv. Müh. Mim. Fak. Derg., 28(1), 127–134. [Open access: https://dergipark.org.tr/tr/pub/gazimmfd/article/89066]

11. **TUTİ M., ŞAHİN Z., DURGUN O.** (2023/2024). *Experimental Investigation of the Effects of Water Addition into the Intake Air on Combustion Parameters, Energy Balance and Developing an Empirical Combustion Duration Relation in Automobile Diesel Engine.* 23rd Congress on Thermal Science and Technology, Gaziantep; DergiPark M6_2023_015. [Open access: https://dergipark.org.tr/en/download/article-file/3540100]

12. **Gökçeli E.** (2022). *Performance and emission characteristics of a diesel engine operated with water-biodiesel emulsion fuels.* MSc thesis, Çukurova University. [Open access: https://thesis.rawdatalibrary.net/en/thesis/bir-dizel-motorda-kullanlan-su-biyodizel-emulsiyon-yaktlarnn-performans]

13. **Çoşgun T.** (2012). *A theoretical and experimental study on the effects of water steam injection on NOx emissions of direct injection diesel engine running with different biodiesel blends.* MSc thesis, Yıldız Technical University. [Open access: https://thesis.rawdatalibrary.net/en/thesis/farkl-metil-ester-yaktlarla-calsan-bir-dizel-motorunda-su-buhar]

14. **ITU Marine Engineering** (n.d.). *A study on exhaust emissions reduction system for marine diesel engines.* ITU Research Portal. [https://research.itu.edu.tr/en/publications/a-study-on-exhaust-emissions-reduction-system-for-marine-diesel-e] (Abstract only; full paper paywalled.)

15. **Patent**: US9551305B2 — *Additive safety and injection system.* Assignee: Aygaz Anonim Şirketi (Istanbul). Priority: TR 2013/15663 (2013-12-31). PCT/TR2014/000419. [USPTO: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9551305] — Not water injection; LPG/LNG additive system.

16. **Patent**: TR201310902A2 / EP3047124A2 / WO2015038087A2 — *Bir motor soğutma sistemi / Système de refroidissement de moteur.* Applicant: Tofaş Türk Otomobil Fabrikası A.Ş. Priority: 2013-09-16. [Google Patents: https://patents.google.com/patent/TR201310902A2/fr] — Jacket cooling, not combustion water injection.

17. **Patent**: US20200018229A1 — *Internal combustion engine with a rotating piston…* Assignees: Istanbul Teknik Üniversitesi, Mitos Mikrodalga. Priority: TR 2017/05836, TR 2018/05337. PCT/TR2018/050177. [USPTO] — Rotary engine concept; no water injection claims.

---

## 9. Limits and open questions

1. **Paywalled primary data**: Several key papers (Ayhan 2020 Applied Energy; ITU marine water injection; Okumuş 2020/2023 full texts) are behind Elsevier/Taylor & Francis paywalls. No legitimate author preprints or university repository copies were found for the exact measured NOx/% numbers. These are marked "paywalled; no legitimate open copy found" in the source list.

2. **OEM internal R&D**: Turkish OEMs (Tofaş, Ford Otosan, Oyak Renault) operate large R&D centers but publish little in open literature. Water injection may be evaluated internally but not patented or published in Turkey. No evidence found in TR/EP/US patent databases under their names.

3. **Water-methanol gap**: The complete absence of peer-reviewed Turkish academic work on water-methanol injection is notable given global motorsport and aftermarket prevalence. Either the work is unpublished, done in non-academic tuning shops, or Turkish researchers have focused on pure water / emulsion routes.

4. **Six-stroke follow-on**: Gazi's experimental six-stroke (2015) has been cited in Korean (Hanyang Univ., 2023) and Turkish (Bitlis Eren Univ., 2018 theoretical) follow-ons, but no further Turkish experimental six-stroke work found post-2016.

5. **Marine vs. road classification**: ITU/Yıldız water-diesel emulsion papers are authored by marine engineering faculty and explicitly target IMO NOx compliance. They are included here because the engine technology (single-cylinder DI diesel) is directly transferable to road applications, and the thermodynamic analysis is engine-fundamental, not ship-specific. Tagged "marine" per instructions.

6. **TÜBİTAK MAM**: Public project listings show no combustion water-injection activity. Private industry contracts (endüstriyel hizmetler) are not publicly detailed. Possible unreported work exists but cannot be cited.

7. **Language/Indexing bias**: Search relied on Turkish and English keywords in Google Scholar, TR Dizin, DergiPark, university repositories, USPTO/EPO patent databases. Papers published in Turkish-only conference proceedings not indexed in these sources may have been missed.

---
---

# Verification (checker, not Hermes)

Checked 2026-11-11, about 2:15 PM America/Los_Angeles, after the first Turkey job. Paywall rule (James t880u): legitimate open copies only; no piracy sites.

The draft correctly found **no Turkish series-production road vehicle** with factory combustion-cycle water injection, correctly pointed to Gazi (six-stroke and emulsions), Sakarya/Ayhan (steam, intake water, direct water, emulsions), and the Okumuş/Kaya/Kökkülünk emulsion papers, and correctly left the 2020 Applied Energy direct-injection paper without invented percentages. It used the **swapped abstract** of the 2013 Gazi emulsion paper (CO and NOx reversed relative to the body), attached a **wrong DOI** to that paper, missed the official open 2019 Ayhan and Ece direct-water-injection journal paper, and took a **12.27 % torque** figure that is not in the official six-stroke abstract. An official ITU marine “~70 % NOx” claim was not opened and is not taken.

## Confirmed (spot-checked)

- **No Turkish OEM series-production passenger car, van, bus, or truck** with factory combustion-cycle water injection was found. Tofaş cooling-system patents, if real, are jacket cooling and out of scope.

- **Yılmaz, Solmaz, Polat, and Altın, 2013, Gazi Üniv. Müh. Mim. Fak. Der. 28(1) 127–134 (official open PDF).** *Üç-Fazlı Dizel Emülsiyon Yakıtlarının Motor Performansı Ve Egzoz Emisyonlarına Etkisi.* Gazi University, Faculty of Technology, Automotive Engineering (Polat: Hitit University). Single-cylinder four-stroke DI diesel on a Cussons P8160 stand (table: 19.6 Nm at 2200 rpm). Three-phase oil/water/oil emulsions with 1 % monoethylene glycol; E1 = 10 % water, E2 = 15 % water. **The official abstract swaps CO and NOx for E2** (it says CO −45.9 %, NOx −26.9 %, soot −18.8 %, torque −15.72 %). The **body results**, which the conclusion paragraph follows, are: E1 average **torque −23.3 %**, **SFC +45 %**, **CO −5.7 %**, **NOx −10.9 %**, **smoke −12.7 %**; E2 average **torque −15.72 %**, **SFC +32.6 %**, **CO −26.9 %**, **NOx −45.9 %**, **smoke −18.8 %**. Diesel minimum SFC 352.15 g/kWh and maximum measured torque 21.42 Nm at 2250 rpm. Use the body figures, not the abstract swap. Official DOI is **10.17341/gummfd.53296**, not the Düzce-journal DOI given in the draft. https://dergipark.org.tr/tr/download/article-file/76266

- **Ayhan, 2016, SAÜ Fen Bil Der. 20(3) 463–471 (official open PDF).** *Direkt enjeksiyonlu bir dizel motoruna buhar ve farklı yöntemlerle su gönderiminin performans ve NOx emisyonlarına etkilerinin incelenmesi.* Single-cylinder water-cooled DI diesel, full load. Water as E10/E15/E20 emulsions (2 % surfactant), intake liquid injection S10/S15/S20 at 20 °C, and intake steam B10/B15/B20 at 133 °C from exhaust heat, 10/15/20 % of fuel mass, 3 bar. Official abstract gives no percentages. Body: emulsion E20, max torque/power **−2.5 %** at 2400 rpm; intake liquid water, max **+2.3 %** at 1800 rpm; steam, max **+2.5 %** at 1800 rpm. NOx max reductions: **E20 −27 %** at 2400 rpm, **S20 −55 %** at 2400 rpm, **B20 −33 %** at 2200 rpm; the largest NOx cut was liquid intake injection, which also caused **intake-valve and manifold corrosion**. Steam is judged the better overall method. Official DOI on the PDF is **10.16984/saufenbilder.71773** (the draft’s 91773 is a typo). https://dergipark.org.tr/en/download/article-file/236502

- **Ayhan and Ece, 2019, İleri Teknoloji Bilimleri Dergisi 8(1) (official open PDF).** *Tek silindirli bir dizel motora direkt su enjeksiyonunun performans ve emisyonlara etkisinin incelenmesi.* Sakarya University of Applied Sciences. Missed by the draft as an open map (the draft relied on a later, typically paywalled Applied Energy paper). Single-cylinder water-cooled DI diesel, compression ratio **17.5**, full load; baseline effective power about **10 kW** near 2200 rpm. Direct water through a cylinder-head injector at **10, 20, 30, and 40 %** of fuel mass. Official abstract and body: at **40 %** water and **1200 rpm**, **NOx −38 %**; maximum **power +6 %** (body: at 1200 rpm / 40 % water); body also **BSFC about −8.5 %** at 1600 rpm / 40 % water, and **effective efficiency +9 %** at 1600 rpm / 40 % water; smoke/turbidity about **−28 %** at 1200 rpm / 40 % water; **HC +50 %** at 2200 rpm / 40 % water. The conclusions paragraph says BSFC −7.5 %; prefer the body/abstract **8.5 %** at the stated point. Do **not** use third-party thesis summaries that quote **NOx −61.2 %** at **100 %** water — that ratio is not in this official paper. https://dergipark.org.tr/en/download/article-file/719644

- **Okumuş, Kaya, and Kökkülünk, Energy Sources, Part A 45(3) 6710–6729, 2023 (official ITU research-portal abstract).** *NOx based comparative analysis of a CI engine fueled with water in diesel emulsion.* DOI 10.1080/15567036.2020.1839147. The opened ITU page lists the authors under **Yıldız Technical University, Department of Marine Engineering** (the paper is indexed on the ITU portal). Official abstract: 5/10/15 % water-in-diesel emulsions at rated torque and power. At maximum torque: brake power down up to **5.22 %**, BSFC up to **+7.42 %**, NOx down as much as **16.84 %**. At maximum power: brake power down up to **5.46 %**, BSFC up to **+8.96 %**, highest NOx cut **10.8 %**. 10 % emulsion chosen as optimum by Fuzzy-AHP/CODAS; AVL Boost compared with experiment. Full Taylor & Francis PDF not opened. https://research.itu.edu.tr/en/publications/nosubxsub-based-comparative-analysis-of-a-ci-engine-fueled-with-w/

- **Arabaci, İçingür, Solmaz, Uyumaz, and Yılmaz, Energy Conversion and Management 98 (2015) 89–97 (official Gazi AVESIS abstract).** *Experimental investigation of the effects of direct water injection parameters on engine performance in a six-stroke engine.* DOI 10.1016/j.enconman.2015.03.045. Single-cylinder four-stroke gasoline engine converted to six-stroke; LPG; λ=1; 2250–3500 rpm; full load; water DI at BTDC/TDC/ATDC and 25/50/75/100 bar. Official abstract: exhaust-gas temperature about **−7 %**, SFC about **−9 %**, fuel consumption **+2 %**, power **+10 %**, thermal efficiency about **+8.72 %**, CO **−21.97 %** and HC **−18.23 %** up to 3000 rpm; NO decreased (no percentage). The draft’s **brake torque +12.27 %** is **not** in this abstract and was **not taken**. The Elsevier PDF was not opened. https://avesis.gazi.edu.tr/yayin/d9027181-f2cd-427d-afcd-52edf469a827/experimental-investigation-of-the-effects-of-direct-water-injection-parameters-on-engine-performance-in-a-six-stroke-engine

- **Ayhan, Applied Energy 260 (2020) 114328.** Bibliographic record of electronically controlled direct water injection is accepted; the PDF is typically paywalled and was **not opened**. No W60 percentages were taken from secondary description.

- **Galata, Serkan, 2017, Yıldız Technical University master’s thesis (official dspace abstract; missed by the draft).** *İçten yanmalı motorlarda su enjeksiyonunun motor performansı ve egzoz emisyonları üzerine olan etkisinin deneysel araştırılması.* Direct water at 90 bar into a single-cylinder engine converted from diesel to SI, water mass fractions 3, 19, 52, 67, and 75 %. Official abstract has **no NOx or BSFC percentages**. https://hdl.handle.net/20.500.14981/13673

## Errors and unverified claims in the Hermes draft

- **Gazi 2013 E2 “CO −45.9 %, NOx −26.9 %”** follows the official abstract, which is **swapped** relative to the body (body: NOx −45.9 %, CO −26.9 % for E2).

- **Wrong DOI** 10.29130/dubited.575123 attached to the 2013 Gazi paper (that DOI is a Düzce journal identifier). Correct: 10.17341/gummfd.53296.

- **Ayhan 2016 DOI typo** 91773 instead of **71773**, and the draft gave only qualitative 2016 results although the open PDF has usable NOx and power percentages, including intake-water **NOx −55 %**.

- **Missed Ayhan and Ece 2019** official open direct-water-injection map (NOx −38 % at 40 % water / 1200 rpm; power +6 %). Do not substitute unopened thesis figures of −61.2 % at 100 % water.

- **Six-stroke “brake torque +12.27 %”** not in the official AVESIS abstract.

- **ITU/Yıldız affiliation** for Okumuş et al. overstated as a joint ITU laboratory map; the opened portal record lists Yıldız Marine Engineering.

- **ITU marine “NOx reduction ~70 %”** (section 4.3) was not opened as a named official paper; **not taken**.

- **Tuti, Şahin, and Durgun** combustion-duration numbers, **Çukurova 2022** thesis results, and **Çoşgun 2012** steam/biodiesel results were not opened in this pass; bibliographic only.

- **Patent numbers** (Aygaz, Tofaş, ITU rotary PCT) were not independently opened here; do not treat them as verified water-injection maps.

## Water Engine — what can actually be used

| Source | Open copy | What is usable |
| --- | --- | --- |
| Yılmaz et al. 2013, Gazi journal (official PDF) | Yes | Single-cylinder DI diesel, 10/15 % three-phase emulsions. Use **body** averages: E2 **NOx −45.9 %**, **CO −26.9 %**, **smoke −18.8 %**, **torque −15.72 %**, **SFC +32.6 %**. Do not use the abstract’s swapped CO/NOx. |
| Ayhan 2016, SAÜ Fen Bil (official PDF) | Yes | Full-load single-cylinder DI diesel. NOx: emulsion E20 **−27 %** (2400 rpm), intake water S20 **−55 %** (2400 rpm), steam B20 **−33 %** (2200 rpm). Power: E20 **−2.5 %**, S20 **+2.3 %**, B20 **+2.5 %**. Intake liquid water corroded the manifold/valve. |
| Ayhan and Ece 2019 (official PDF) | Yes | Direct in-cylinder WI, 10–40 % of fuel. At 40 % water / 1200 rpm: **NOx −38 %**; max **power +6 %**; body **BSFC about −8.5 %** at 1600 rpm / 40 % water; **HC +50 %** at 2200 rpm. |
| Okumuş, Kaya, Kökkülünk 2023 (official ITU abstract) | Abstract | Yıldız Marine Engineering emulsion tests: at max torque, power down to **−5.22 %**, BSFC up to **+7.42 %**, **NOx −16.84 %**; at max power, **NOx −10.8 %**. |
| Arabaci et al. 2015 (official Gazi AVESIS abstract) | Abstract | Six-stroke LPG conversion, water DI. EGT about **−7 %**, SFC about **−9 %**, fuel consumption **+2 %**, power **+10 %**, thermal efficiency about **+8.72 %**, CO **−21.97 %**, HC **−18.23 %** to 3000 rpm. No NO %; no 12.27 % torque. |
| Ayhan 2020, Applied Energy 114328 | Record only | Real DWI paper; PDF not opened; no W60 percentages taken. |
| Galata 2017 Yıldız thesis | Official abstract | Direct 90-bar water in a converted SI bench; no percentages in the abstract. |

Do not use: Gazi 2013 abstract CO/NOx swap; six-stroke torque +12.27 %; unopened thesis “61.2 % NOx at 100 % water”; ITU marine ~70 % NOx; unopened Applied Energy, Tuti, or Çukurova numbers; jacket-cooling patents as combustion-cycle WI.

## Link-check notes

Opened: official DergiPark PDFs of Yılmaz et al. 2013, Ayhan 2016, and Ayhan and Ece 2019; official ITU research-portal abstract for Okumuş et al. 2023; official Gazi AVESIS abstract for Arabaci et al. 2015; official Yıldız dspace abstract for Galata 2017. Elsevier and Taylor & Francis full PDFs were not opened. No piracy sites were used. Those PDFs were saved only to the private archive, not to the public GitHub repository.
