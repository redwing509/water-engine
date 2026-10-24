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

## AramcoMech 2.0 (`aramco20.yaml`) — X1 independent mechanism

- Source: Combustion Chemistry Centre, NUI Galway (University of Galway),
  "AramcoMech 2.0 (2018)" — Saudi Aramco Mechanism Release.
  Index page: https://universityofgalway.ie/combustionchemistrycentre/mechanismdownloads/
  (also http://c3.universityofgalway.ie/combustionchemistrycentre/mechanismdownloads/aramcomech20/)
- Files downloaded (UTC): 2026-10-24T17:40Z. The three files are the
  mechanism, thermochemistry and transport sub-files of the single
  AramcoMech 2.0 release (not separate versions).

| Original file | URL | SHA-256 |
|---|---|---|
| `AramcoMech2.0.MECH` | http://c3.universityofgalway.ie/media/researchcentres/combustionchemistrycentre/files/mechanismdownloads/aramcomech20/AramcoMech2.0.MECH | `300523af5b3f191a9d7fbb12585a203c284c516dc19f2f6927559e11d7c2eccd` |
| `AramcoMech2.0.therm` | http://c3.universityofgalway.ie/media/researchcentres/combustionchemistrycentre/files/mechanismdownloads/aramcomech20/AramcoMech2.0.therm | `c1fb70e6b4f45f1e8f4acd33f5b1ccdb671e0e28c3ba6d152045ab0ec9b7b6e1` |
| `AramcoMech2.0.tran` | http://c3.universityofgalway.ie/media/researchcentres/combustionchemistrycentre/files/mechanismdownloads/aramcomech20/AramcoMech2.0.tran | `47a127c74ba58e2e5f759e824c86267aded630f33018d3f02401f99e339cc59c` |

- Conversion (Cantera 3.2.0, `cantera.ck2yaml`, Python 3.11):

  ```
  python -m cantera.ck2yaml --permissive \
    --input=AramcoMech2.0.MECH --thermo=AramcoMech2.0.therm \
    --transport=AramcoMech2.0.tran --output=aramco20.yaml
  ```

  `--permissive` was required: the MECH file re-declares six species
  (`C5H10-2`, `C5H91-3`, `C5H91-4`, `C5H91-5`, `C5H92-4`, `C5H92-5`) that
  already appear earlier in the species list. With `--permissive` the
  duplicates are dropped and the conversion completes.
- Result: **493 species, 2716 reactions**. Contains `CH3OH` and `C2H5OH`
  (no separate vapour-phase species; liquid-alcohol latent heat is supplied
  by `sims/common/fuels.py`, not by the mechanism). `aramco20.yaml`
  SHA-256: `ff445870610f4bc1129f061e1823c0939dc5d44ce15996cb4ee85cd6ff72db33` (CRLF working copy on the PC/mail;
  the LF git checkout, enforced by `.gitattributes`, hashes to
  `26c09c2fe6ce31610477bd2b32979650e9159e4478748dea9e4ef832f913e121`; content identical apart from line endings).
- Cantera load check: `ct.Solution("mechanisms/aramco20.yaml")` loads
  successfully; `gas.species_index("CH3OH")` and `("C2H5OH")` resolve.
- Note: this is the X1 independent mechanism for the `xcheck/chem` branch.
  It is NOT the project baseline (San Diego 2016-12-14). All `xcheck/chem`
  results are compared against San Diego and literature targets, never
  blended with the baseline runs.

## GRI-Mech 3.0 (`gri30.yaml`)

Ships with Cantera. Its embedded metadata identifies GRI-Mech 3.0 (Smith et al., 1999). Used for H2 and CH4, and as the fallback for CH3OH if `sandiego.yaml` is unavailable (SPEC §2). Each `summary.json` records the mechanism used for each fuel.
