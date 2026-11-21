#!/usr/bin/env bash
# Run from any working directory; all paths remain repository-relative.
set -uo pipefail

mode=--full
if (( $# > 1 )); then
    printf 'Usage: bash run_all.sh [--quick|--full]\n' >&2
    exit 2
fi
if (( $# == 1 )); then
    case "$1" in
        --quick|--full) mode=$1 ;;
        *) printf 'Usage: bash run_all.sh [--quick|--full]\n' >&2; exit 2 ;;
    esac
fi

cd -- "$(dirname -- "${BASH_SOURCE[0]}")" || exit 1
mkdir -p results || exit 1
if [[ ! -s results/RUNLOG.md ]]; then
    printf '| Module | Exit code | Runtime [s] |\n| --- | ---: | ---: |\n' > results/RUNLOG.md || exit 1
fi

any_failed=0
while IFS= read -r -d '' module_path; do
    module_name=${module_path##*/}
    module_started=$SECONDS
    if nice -n 19 python -m "sims.${module_name}.run" "$mode" --workers 8 --out "results/${module_name}"; then
        module_exit=0
    else
        module_exit=$?
        any_failed=1
    fi
    module_runtime=$((SECONDS - module_started))
    printf '| %s | %s | %s |\n' "$module_name" "$module_exit" "$module_runtime" >> results/RUNLOG.md || exit 1
done < <(find sims -mindepth 1 -maxdepth 1 -type d -name '[0-9][0-9]_*' -print0 | sort -zV)

exit "$any_failed"
