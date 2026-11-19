# Steamline

Steamline is the Water Engine scoring and ranking code that rescores combustion-candidate result rows. It does not run a new combustion simulation. It reads existing result rows and applies the project's cost model (`reference/sims/cost/cost.py`).

The tested entry point is `rescore_ah26_bh26.py` (matched-dry cost-per-mile rescore, with `tests/test_rescore.py`). `rlib.py` and `rescore_combo_full.py` apply the same ranking rule to grouped campaign files.

## Honest limits

- Model-only: this is arithmetic on simulation rows, not experimental validation.
- Water is never a fuel. Water has no heating value in the cost model. All chemical energy comes from the fuel share (methanol, ethanol, or a gasoline surrogate).
- Factory compression-ratio recommendations stay withheld and are not published or updated by this code.
- A two-engine M03 / M03-CRN agreement inside the same toolchain is not independent experimental validation.

## Requirements

- Python 3.10 or newer
- The Python standard library only (no pip packages)

## How to run

From this directory, first print the plan (nothing is scored):

```
bash launch_rescore_ah26_bh26.sh
```

To rescore a directory of existing `points_AH26.jsonl` and `points_BH26.jsonl` rows:

```
export PYTHONPATH=reference
export WE_PYTHON=python3
export WE_JOBS=/path/to/points-directory
export WE_RESULTS_ROOT=/path/to/output-directory
bash launch_rescore_ah26_bh26.sh --execute
```

Or call the scorer directly:

```
PYTHONPATH=reference python3 rescore_ah26_bh26.py \
  --config stage_config.json \
  --jobs /path/to/points-directory \
  --allow-keys allow-keys-AH26-BH26.json \
  --outdir /path/to/output-directory
```

`rescore_combo_full.py` ranks grouped `points_R31*.jsonl` and `points_R32*.jsonl` files placed in this directory. Those large campaign files are not shipped here.

Self-check the reviewed cost module:

```
PYTHONPATH=reference python3 rescore_ah26_bh26.py --self-check --config stage_config.json
```

Tests (17 unit tests, including synthetic fixtures and the attached sample rows):

```
PYTHONPATH=reference python3 -m unittest discover -s tests -v
```

## License

MIT, same as the repository. Steamline itself has no third-party runtime dependencies. Public price sources used in `reference/sims/cost/prices_20261025.json` are documented in that file.
