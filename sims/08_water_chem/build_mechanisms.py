"""Build FH2O mechanism variants for module 08 (text-based, format-preserving).

Usage: python -m sims.08_water_chem.build_mechanisms

Three textual edits per file (preserving all unrelated formatting/thermo
precision bit-for-bit):

1. Duplicate the H2O species data block as FH2O (verbatim copy of composition,
   thermo, transport), inserted directly after the H2O block.
2. In every per-phase ``species: […, H2O, …]`` list, insert ``FH2O`` after
   ``H2O``.
3. In every reaction ``efficiencies`` mapping, replace the ``H2O:`` key with
   ``FH2O:`` — variant "a" keeps H2O's value, variant "b" uses 1.0.

FH2O never appears on the reactant or product side of any reaction, so its net
production rate is zero by construction.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "mechanisms" / "08_water_chem"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "sandiego": REPO_ROOT / "mechanisms" / "sandiego.yaml",
    "gri30": REPO_ROOT / "mechanisms" / "gri30.yaml",
}

WATER = "H2O"
FICTITIOUS = "FH2O"


# --- regex helpers ----------------------------------------------------
# Species block: from the line starting with "- name: H2O" up to (but not
# including) the next top-level "- name:" or "reactions:" key.
_SPECIES_RE = re.compile(
    r"(^[ \t]*- name: H2O\n"        # start: block header
    r"((?:.*\n)*?)"                  # body (greedy-lazy, non-capturing copy)
    r")(?=^- name: |^reactions:)",   # stop: next species or reactions section
    re.MULTILINE,
)

# Phase species list: the value part after "species:" on a list line or
# the start of a flow list.
_PHASE_SPECIES_RE = re.compile(
    r"(^[ \t]*species:\s)(\[[^\]]*\])",
    re.MULTILINE,
)

# Reaction efficiency entry: "H2O: <number>" inside an efficiencies mapping.
# Cantera YAML writes these with the species name as key.
_EFF_H2O_RE = re.compile(r"H2O:\s+([0-9.eE+-]+)")


def _species_block(text: str) -> tuple[str, str] | None:
    """Return (header_line, body) for the H2O species block, or None."""
    m = _SPECIES_RE.search(text)
    if not m:
        return None
    return m.group(0), m.group(2)


def _insert_fh2o_species(text: str) -> str:
    """Duplicate the H2O species block as FH2O, inserted just after it."""
    m = _SPECIES_RE.search(text)
    if not m:
        raise ValueError("H2O species block not found in source mechanism")
    block = m.group(0)            # full "- name: H2O ...<body>..."
    body = m.group(2)            # body text (thermo, transport, ...)
    fh2o_block = block.replace("name: H2O", f"name: {FICTITIOUS}", 1)
    # Insert FH2O right after the H2O block.
    return text[:m.end()] + "\n" + fh2o_block + text[m.end():]


def _add_to_phase_species(text: str, source_name: str) -> str:
    """Insert FH2O into every phase ``species: […]`` list, after H2O.

    For gri30, also add ``explicit-third-body-duplicates: mark-duplicate``
    to the gas phase entry — gri30 lists explicit H2O third-body reactions
    alongside generic M reactions; once H2O's efficiency is replaced by
    FH2O, Cantera treats the pair as undeclared duplicates and requires
    this flag.
    """
    def repl(match: re.Match) -> str:
        prefix = match.group(1)
        lst = match.group(2)
        if FICTITIOUS in lst:
            return match.group(0)
        new_lst = lst.replace(WATER, f"{WATER}, {FICTITIOUS}", 1)
        return prefix + new_lst

    text = _PHASE_SPECIES_RE.sub(repl, text)
    if source_name == "gri30":
        if "explicit-third-body-duplicates" not in text:
            text = re.sub(r"(kinetics: gas\n)",
                          r"\1  explicit-third-body-duplicates: mark-duplicate\n",
                          text, count=1)
    return text


def _replace_efficiencies(text: str, variant: str) -> tuple[str, int]:
    """Replace H2O entries in reaction efficiencies with FH2O.

    Variant 'a' preserves the H2O value; variant 'b' sets it to 1.0.
    Returns (new_text, count).
    """
    n = 0

    def repl_eff_h2o(match: re.Match) -> str:
        nonlocal n
        val = match.group(1)
        out = (1.0 if variant == "b" else float(val))
        n += 1
        return f"{FICTITIOUS}: {out}"

    return _EFF_H2O_RE.sub(repl_eff_h2o, text), n


def transform(source: Path, variant: str, source_name: str | None = None) -> tuple[str, int]:
    """Return (transformed_text, efficiency_count) for the given variant."""
    if source_name is None:
        source_name = source.stem
    text = source.read_text(encoding="utf-8")
    text = _insert_fh2o_species(text)
    text = _add_to_phase_species(text, source_name)
    text, n = _replace_efficiencies(text, variant)
    return text, n


def build(source_name: str, source_path: Path, variant: str) -> tuple[Path, int]:
    text, n = transform(source_path, variant, source_name)
    out = OUT / f"{source_name}_fh2o{variant}.yaml"
    out.write_text(text, encoding="utf-8")
    return out, n


def main() -> None:
    import cantera as ct
    for source_name, source_path in SOURCES.items():
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        for variant in ("a", "b"):
            out, n = build(source_name, source_path, variant)
            gas = ct.Solution(str(out))
            names = gas.species_names
            assert FICTITIOUS in names, out
            for rx in gas.reactions():
                eq = rx.equation or ""
                assert FICTITIOUS not in eq, f"{out}: FH2O in reaction: {eq}"
            i_h2o = names.index(WATER)
            i_fh2o = names.index(FICTITIOUS)
            assert gas.molecular_weights[i_fh2o] == gas.molecular_weights[i_h2o]
            print(f"{out.name}: {len(names)} species, "
                  f"{len(gas.reactions())} reactions, {n} efficiencies transferred")


if __name__ == "__main__":
    main()
