# Mechanism provenance

## San Diego mechanism (`sandiego.yaml`)

- Source: "Chemical-Kinetic Mechanisms for Combustion Applications", San Diego Mechanism web page, Mechanical and Aerospace Engineering (Combustion Research), University of California at San Diego. Page: https://web.eng.ucsd.edu/mae/groups/combustion/mechanism.html
- Release used: **2016-12-14** (latest release listed on the page at download time).
- Downloaded (UTC): 2026-10-22T01:26:20Z
- Caution (from research doc 02): the release directory's files have been edited since the original release. The server reports the mechanism file last modified 2025-02-28, and the release log describes a 2017 correction to third-body (collision) efficiencies, including water's. Those efficiencies matter for steam-diluted flames. The SHA-256 values below pin the exact bytes this project used.

| Original file | URL | SHA-256 |
|---|---|---|
| `sandiego20161214_mechCK.txt` | https://web.eng.ucsd.edu/mae/groups/combustion/sdmech/sandiego20161214/sandiego20161214_mechCK.txt | `728aa95e372aa71c59528850ac35511bf4c5f457954b9803c6ef823996163c73` |
| `sandiego20160815_therm.txt` | https://web.eng.ucsd.edu/mae/groups/combustion/sdmech/sandiego20161214/sandiego20160815_therm.txt | `ba9518b7007d007353ca6ac927f881b05d6b302bbb56bc32c9e1ee80d3333d92` |
| `sandiego20160815_trans.txt` | https://web.eng.ucsd.edu/mae/groups/combustion/sdmech/sandiego20161214/sandiego20160815_trans.txt | `dc8134f2c62cd54c7999d2428ac1de22743e2e331caef2da8286763bedd5ce94` |
| `20161214_log.txt` (release notes) | https://web.eng.ucsd.edu/mae/groups/combustion/sdmech/sandiego20161214/20161214_log.txt | `c15a1deda4a1c6938ba9a34ab3f05975bba883299ed69b4a66fd22cf4b3a1672` |

### Conversion

```
python -m cantera.ck2yaml --input=sandiego20161214_mechCK.txt \
  --thermo=sandiego20160815_therm.txt --transport=sandiego20160815_trans.txt \
  --output=sandiego.yaml
```

- Converter: Cantera 3.2.0 (`cantera.ck2yaml`), Python 3.12.3.
- Result: 59 species, 271 reactions; contains `CH3OH` and `C2H5OH`. `sandiego.yaml` SHA-256: `859b088d3e973c9803267fa0e6a05d7a82b5a473a994e43b3b4e158783191e20`.
- Converter warnings (uncertain, recorded rather than hidden): Cantera's `NasaPoly2::validate` reports small discontinuities at `Tmid = 1000 K` in cp/R and h/RT for some intermediate species, among them `C2H4OOH`, `OC2H3OOH`, `CH2CH2OH`, `CH3CHOH`, `CH3CH2O`, `C3H6OOH` and `OC3H5OOH`. The largest seen is about 0.5 in cp/R (about 2 %) and about 0.08 in h/RT. These are as published in the original thermo file; they have not been modified.

## GRI-Mech 3.0 (`gri30.yaml`)

Ships with Cantera. Its embedded metadata identifies GRI-Mech 3.0 (Smith et al., 1999). Used for H2 and CH4, and as the fallback for CH3OH if `sandiego.yaml` is unavailable (SPEC §2). Each `summary.json` records the mechanism used for each fuel.
