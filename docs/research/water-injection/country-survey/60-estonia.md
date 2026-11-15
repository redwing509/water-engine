# Estonia — water in the combustion cycle (checked)

Status: DONE (checked). Hermes drafted (job 20261115-051345-we-survey-60-estonia-water-in-combustion, key we-survey-60-estonia-r2, profile we-research, rc 0, 5:13:47–5:18:37 AM America/Los_Angeles 15 Nov 2026, runtime about 5 minutes; the first attempt 20261115-022740 failed on a timeout after a rate limit). The prompt was in Estonian and already included the Simulators section, so no separate simulator follow-up job was run. The checker re-opened and searched sources on 15 Nov 2026, about 8:13–8:45 AM America/Los_Angeles, using university repositories (Estonian University of Life Sciences DSpace, TalTech library), conference proceedings, the journal *Oil Shale* (Estonian Academy Publishers) and the patent record only. No piracy sites were used. The Hermes draft is kept in the private archive only.

Prompt language: Estonian. Report language: English.

Water is not treated as a fuel in this note. Where ethanol is carried with the water, the gains are not credited to the water.

## Verification (checker)

**The Hermes draft said nothing at all was found for Estonia and cited no sources. That is mostly right for classic water injection, but it missed one real line of measured work.** No Estonian production or near-production vehicle with water injection, no Estonian water-injection or water-in-diesel emulsion engine paper, and no Estonian water-injection patent were found. However, the **Estonian University of Life Sciences (EMU, Eesti Maaülikool), Institute of Technology, Tartu** (Jüri Olt, Arne Küüt, Risto Ilves) ran bench tests in 2011–2014 on a D-120 tractor diesel fumigated with **"wet" ethanol of only 60 % strength, i.e. about 40 % water by volume**, through an auxiliary intake fuel system they patented (EE 05665 B1). That is water entering the cylinder together with ethanol. The measured NOx cut is large, but it comes with much higher specific fuel consumption and cannot be credited to water alone.

### What the draft said and what the check found

| Claim in the Hermes draft | Checked result |
| --- | --- |
| "Searches of TalTech, EMU, Tartu University … repositories returned no relevant items" | **Partly wrong.** EMU DSpace holds two open doctoral theses (Küüt 2013; Ilves 2014) and the group published open conference/journal papers (2011–2012) on diesel dual-fuel operation with 60–96 % hydrous ethanol. Nothing relevant was found at TalTech or the University of Tartu in this pass. |
| "No publications or patents from Estonia on water-diesel emulsions, water-methanol blends, or steam-injection cycles" | **Right for emulsions, steam and water-methanol; incomplete overall.** Patent EE 05665 B1 (Eesti Maaülikool, 2011 filing) covers the dual/auxiliary fuel-mixture feed used for the hydrous-ethanol tests. It is a fuel-feed patent, not a water-injection patent; it lapsed in 2014 for non-payment of fees. |
| "No Estonian‑manufactured road vehicle with water‑injection" | **Confirmed** (nothing found). |
| "No historical records (1926–present) … racing, aviation, marine, industrial" | **Confirmed for engines** in this pass. The only Estonian "water injection" hits are in **oil-shale power-plant boilers** (Narva), not engines — excluded. |
| "Nothing found" for simulators | **Confirmed.** The EMU work used SolidWorks (2010) flow simulation for an injector air-flow check and AVL IndiModul (measurement hardware). Neither is a combustion simulator for water injection; nothing was added to the candidate list. |
| Search method claims ("Estonian Patent Register", "Google Scholar", ".ee" domain searches) | **Unverifiable.** The job left no search log or citations. The claims are not relied on. |

### Sources opened and usable figures

- **Olt, Mikita, Ilves, Küüt (2011)**, "Ethanol as an additive fuel for diesel engines", *Engineering for Rural Development* 10 (Jelgava, 2011), open PDF https://www.iitf.lbtu.lv/conference/proceedings2011/Papers/046_Olt.pdf — air-cooled **D-120** tractor diesel on a Dynas3 LI-250 dynamometer, diesel pilot injection plus ethanol of 60, 70, 80 or 96 % strength (rest distilled water) fed through an auxiliary carburettor into the intake. With **60 % ethanol, engine efficiency was about 10 % lower** than with 70–96 % ethanol; ethanol use cut efficiency by **up to 30 %** compared with diesel only. At 1300 rpm, operation became unstable above 3.2 kg/h of 60 % ethanol (diesel : ethanol 1 : 2.8).
- **Küüt, Ilves, Olt (2012)**, "Cost of ethanol when used in diesel engine", *Engineering for Rural Development* 11, open PDF https://www.iitf.lbtu.lv/conference/proceedings2012/Papers/064_Kuut_A.pdf — same D-120 rig, ethanol 60–90 %. Specific fuel consumption with ethanol fuels was **on average 36 % higher** than with diesel alone; cost model only.
- **Küüt (2013)**, PhD thesis, EMU, supervisor Jüri Olt, "Characteristics of bioethanol fuel obtained from lignocellulosic biomass in internal combustion reciprocating engines with spark- and compression-ignition", record https://dspace.emu.ee/items/15551ba0-282f-47fe-a986-b99c5fd4b5b8 (open PDF) — D-120 dual-fuel tests with **60 % lab ethanol diluted with water (DLGE)** and **58.9 % farm-made lignocellulose bioethanol (LGBE)**. Measured **NOx −27 % (DLGE) and −40 % (LGBE) at 1300 rpm; −52 % and −51 % at 1800 rpm** versus diesel; exhaust temperature 60–90 °C lower; **HC rose**; specific fuel consumption **+34.5…37.6 % at 1300 rpm and about +60 % at 1800 rpm**. Fuel-supply device patented as EE 05665 B1. The NOx drop reflects both ethanol and water cooling; it is **not** a water-only effect.
- **Ilves (2014)**, PhD thesis, EMU, supervisor Jüri Olt, "Fuel supply system of piston engine working on liquid biofuels", https://dspace.emu.ee/handle/10492/1887 (open PDF) — develops a compressed-air "pulveriser" fuel feed for non-standard biofuels including hydrous ethanol; water is used only as a spray-test fluid. With bioethanol fumigation in a diesel, HC rose, which the author links to water vapour from the wet ethanol. In an SI engine the pulveriser feed cut fuel use by about 6 % (petrol) and 3 % (bioethanol). No water-injection result.
- **Patent EE 05665 B1** (application P201100021, filed 17 Mar 2011 by Eesti Maaülikool; inventors Jüri Olt, Arne Küüt, Risto Ilves; granted/published 17 Jun 2013; lapsed 2014), "Piston engine blend formation method and blend feeding scheme", https://patents.google.com/patent/EE05665B1/en .
- Context: **Küüt, Ritslaid, Olt (2011)**, *Agronomy Research* 9 Spec. 1, 125–134, https://agronomy.emu.ee/vol09Spec1/p09s116.pdf (farmstead ethanol in an Otto engine) and **Küüt, Panova, Olt (2012)**, *Agronomy Research* 10 Spec. 1, 139–148, https://agronomy.emu.ee/vol10Spec1/p10s115.pdf (price model; tests used 60 % ethanol with distilled water). **Ilves, Sakalauskas, Olt**, "The impact of bioethanol fuel on agricultural tractor engine's exhaust gas", *Agricultural Engineering* (Lithuania), http://ageng.asu.lt/ae/article/view/17 — abstract only (journal site returned HTTP 500 on recheck); recommends 60 % ethanol as the minimum strength.

### Excluded or context only

- **Oil-shale boilers, Narva**: Kleesmaa, Latõšov, Karolin, *Oil Shale* 2011 (https://kirj.ee/public/oilshale_pdf/2011/issue_2/Oil-2011-2-321-336.pdf) and Karolin, Latõšov, Kleesmaa, *Oil Shale* 2017 (https://www.kirj.ee/public/oilshale_pdf/2017/issue_1/Oil_Shale-2017-1-70-81.pdf) — water injected after the superheater of pulverized oil-shale boilers to cut SO2 (2017 test: SO2 −17 %, steam output −25 t/h; judged ineffective by the authors). Boilers, not engines; excluded.
- **Estonian shale oil as diesel fuel**: Labeckas and Slavinskas, *Oil Shale* 23(3), 2006, 258–266, https://kirj.ee/public/oilshale/oil-2006-3-6.pdf — Lithuanian authors testing Estonian shale oil and the Estonian additive SO-2E in a D-243 diesel. No water in the cycle; context only.
- **Hydrogen/HHO and CNG dual-fuel work at EMU** (e.g. Ilves et al., *Transport* 2022, CNG with diesel pilot): not water in the cycle; excluded.
- **Soviet-era Tallinn Polytechnic marine-diesel work** (e.g. 1974 student theses on forced marine diesels, TalTech research portal): no water-injection content found; not used.

## Production or near-production road vehicles

None found for Estonia.

## Research, prototypes and supplier systems

- EMU (Tartu) D-120 tractor-diesel bench work on hydrous ethanol fumigation (about 40 % water in the ethanol fuel), 2011–2014, with the EE 05665 B1 auxiliary fuel-feed patent. Bench only; no field or vehicle fleet trial found.
- No Estonian supplier of water-injection or emulsion systems was found.

## Water-fuel emulsions and other cycles

No Estonian water-in-diesel emulsion, steam-injection, water-methanol or six-stroke engine work was found.

## Simulators and modeling tools

Simulators found: none after check. The EMU work used SolidWorks 2010 flow simulation only for an injector air-flow check, and AVL IndiModul 621 is in-cylinder pressure measurement hardware. Neither was added to the candidate list.

## Limits and open questions

- The Ilves *Agricultural Engineering* paper's emission numbers were not extracted (full text not reachable on recheck).
- Soviet-era Russian-language Tallinn Polytechnic reports on marine diesels were not searched in depth.
- Estonian Maritime Academy theses on marine NOx control (water emulsion or humid-air) were not found in open repositories.
