#!/bin/bash
# Public launcher for the AH26/BH26 matched-dry cost rescore (Steamline).
# Does not run combustion, publish, or write git.
# Default (no --execute) only prints the plan.
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CONFIG=${WE_CONFIG:-$SCRIPT_DIR/stage_config.json}
ALLOW=${WE_ALLOW_KEYS:-$SCRIPT_DIR/allow-keys-AH26-BH26.json}
PY_SCRIPT=$SCRIPT_DIR/rescore_ah26_bh26.py

WE_PYTHON=${WE_PYTHON:-python3}
WE_PYTHONPATH=${WE_PYTHONPATH:-$SCRIPT_DIR/reference}
WE_JOBS=${WE_JOBS:-}
WE_RESULTS_ROOT=${WE_RESULTS_ROOT:-}

EXECUTE=0
RESUME=0
RESUME_DIR=
for arg in "$@"; do
  case "$arg" in
    --execute) EXECUTE=1 ;;
    --resume) RESUME=1 ;;
    --resume=*) RESUME=1; RESUME_DIR=${arg#--resume=} ;;
    -h|--help)
      echo "usage: $0 [--execute] [--resume[=DIR]]"
      echo "Set WE_JOBS to a directory of points_*.jsonl files."
      echo "Set WE_RESULTS_ROOT to an output directory."
      echo "without --execute: print the plan and exit 0"
      exit 0
      ;;
    *) echo "unknown argument: $arg" >&2; exit 2 ;;
  esac
done

cat <<PLAN
stage: rescore-AH26-BH26-matched-dry-cost
combustion_runs: 0
publish: no
git: no
workers: 1
python: $WE_PYTHON
pythonpath: $WE_PYTHONPATH
jobs: ${WE_JOBS:-"(set WE_JOBS)"}
results_root: ${WE_RESULTS_ROOT:-"(set WE_RESULTS_ROOT)"}
allow_keys: $ALLOW
This process only rescores existing result rows. Water is never a fuel.
Results are model arithmetic only, not experimental validation.
PLAN

if [[ $EXECUTE -ne 1 ]]; then
  echo "plan only (no --execute). Nothing was scored."
  exit 0
fi

if [[ -z "$WE_JOBS" || -z "$WE_RESULTS_ROOT" ]]; then
  echo "refusing: set WE_JOBS and WE_RESULTS_ROOT to explicit local paths before --execute" >&2
  exit 3
fi

if [[ ! -x $WE_PYTHON ]] && ! command -v "$WE_PYTHON" >/dev/null 2>&1; then
  echo "python not executable: $WE_PYTHON" >&2
  exit 2
fi
if [[ ! -f $CONFIG || ! -f $ALLOW || ! -f $PY_SCRIPT ]]; then
  echo "payload file missing beside the launcher" >&2
  exit 2
fi
for f in points_AH26.jsonl points_BH26.jsonl; do
  if [[ ! -f "$WE_JOBS/$f" ]]; then
    echo "missing input $WE_JOBS/$f" >&2
    exit 2
  fi
done
case "$WE_RESULTS_ROOT" in
  "$WE_JOBS"|"$WE_JOBS"/*)
    echo "refusing to write results inside the jobs directory" >&2
    exit 2
    ;;
esac

export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MPLBACKEND=Agg
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=$WE_PYTHONPATH${PYTHONPATH:+:$PYTHONPATH}

if [[ $RESUME -eq 1 ]]; then
  if [[ -z $RESUME_DIR ]]; then
    echo "resume requires --resume=DIR" >&2
    exit 2
  fi
  OUT=$RESUME_DIR
  EXTRA=(--resume)
else
  STAMP=$(date -u +%Y%m%dT%H%M%SZ)
  OUT=$WE_RESULTS_ROOT/rescore-AH26-BH26-$STAMP
  EXTRA=()
fi

mkdir -p "$(dirname -- "$OUT")"
EXPECT=()
if [[ $ALLOW == "$SCRIPT_DIR/allow-keys-AH26-BH26.json" ]]; then
  EXPECT=(--expect-full-grid)
else
  echo "allow-list override: full-grid shape check is off"
fi
echo "outdir: $OUT"
set +e
nice -n 19 "$WE_PYTHON" "$PY_SCRIPT" \
  --config "$CONFIG" \
  --jobs "$WE_JOBS" \
  --allow-keys "$ALLOW" \
  --outdir "$OUT" \
  --workers 1 \
  "${EXPECT[@]}" \
  "${EXTRA[@]}"
rc=$?
set -e
if [[ -d $OUT ]]; then
  printf '%s rc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$rc" >> "$OUT/EXIT.txt"
fi
echo "rc=$rc"
exit "$rc"
