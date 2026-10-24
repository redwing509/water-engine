#!/bin/bash
# we-08-m13-gci-dualT: 3-mesh GCI of the M13 intake-port spray/wall-film case in the dual-temperature regimes.
# CPU run (reactingParcelFoam is Lagrangian/film dominated). Env knobs:
#   M13_REF   REQUIRED: water-engine commit that contains a WORKING cfd/port13 (coarse case completed rc=0).
#   NPROC (default nproc)  MATRIX (default "A")  OUT (/out)  PUSH (1 if GH_TOKEN set)  GENERATE_ONLY (1 = mesh+fields only)
#   RESULTS_REPO (default redwing509/water-engine)
# MATRIX A (GCI): US20 x {coarse,med,fine} x {normal: wall 363 K/intake 360 K, hot: wall 388 K/intake 400 K}  = 6 runs
# MATRIX B (regime spread at med mesh): CARB60 x {normal, hot, heated 420/400} + US20 heated 420/400            = 4 runs
set -o pipefail
B=$(cd "$(dirname "$0")" && pwd)
. /usr/lib/openfoam/openfoam2512/etc/bashrc || true
NPROC=${NPROC:-$(nproc)}; OUT=${OUT:-/out}; MATRIX=${MATRIX:-A}
RESULTS_REPO=${RESULTS_REPO:-redwing509/water-engine}
RUN_ID=${RUN_ID:-we08-m13-$(date -u +%Y%m%dT%H%MZ)}; R="$OUT/$RUN_ID"; mkdir -p "$R"; LOG="$R/finish.log"
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1   # HF containers may run as root
log() { echo "$(date -u +%FT%TZ) $*" | tee -a "$LOG"; }
[ -n "${M13_REF:-}" ] || { log "M13_REF not set: this bundle is BLOCKED until a working M13 coarse case is committed (see README)"; exit 64; }
log "start run_id=$RUN_ID M13_REF=$M13_REF nproc=$NPROC matrix=$MATRIX"
{ nproc; free -g; lscpu | grep -E 'Model name|^CPU\(s\)'; nvidia-smi -L 2>/dev/null || echo "no GPU visible (not used by this CPU bundle)"; } > "$R/hardware.txt" 2>&1
git clone --quiet --filter=blob:none --no-checkout "https://github.com/$RESULTS_REPO.git" "$R/src" && \
  git -C "$R/src" checkout --quiet "$M13_REF" -- cfd/port13 || { log "cannot fetch cfd/port13 at $M13_REF"; exit 65; }
P13="$R/src/cfd/port13"; echo "$M13_REF" > "$R/m13_ref.txt"
mkdir -p "$R/src/cfd/runs"; ln -sfn "$R/src/cfd/runs" "$R/runs"   # post_m13.py expects cases in cfd/runs/
# name injector level Twall Tintake ranks(of 32-vCPU budget)
matrix() { case "$1" in
 A) cat <<M
US20-fine-normal   US20 fine   363 360 16
US20-fine-hot      US20 fine   388 400 16
US20-med-normal    US20 med    363 360 8
US20-med-hot       US20 med    388 400 8
US20-coarse-normal US20 coarse 363 360 4
US20-coarse-hot    US20 coarse 388 400 4
M
 ;;
 B) cat <<M
CARB60-med-normal CARB60 med 363 360 8
CARB60-med-hot    CARB60 med 388 400 8
CARB60-med-heated CARB60 med 420 400 8
US20-med-heated   US20   med 420 400 8
M
 ;; esac; }
run_case() { # name inj level Tw Tin np
  local n="M13G-$1" t0 rc; local d="$R/runs/$n"
  python3 "$B/gen_m13_case.py" "$P13" "$R/src/cfd/runs" "$n" "$2" "$3" "$4" "$5" "$6" > "$R/runs/$n.gen.json" 2> "$R/runs/$n.gen.err" || return 30
  cd "$d" || return 31
  t0=$(date +%s); NP=$6 MESHONLY=${GENERATE_ONLY:-0} ./Allrun > log.Allrun.out 2>&1; rc=$?
  echo "runtime_s $(( $(date +%s) - t0 )) rc $rc" > run.status
  grep -h "uniform $4" wallFilmRegion/0/Tf 0/wallFilmRegion/Tf 2>/dev/null | head -1 | grep -q . && echo "Twall_check ok $4" >> run.status || echo "Twall_check NOT VERIFIED (inspect Tf)" >> run.status
  python3 "$P13/post_m13.py" "$n" > post.json 2> post.err || true
  return $rc
}
free=$NPROC; declare -A PID NP
while read -r name inj lvl tw tin np; do
  [ -n "$name" ] || continue; [ "$np" -gt "$NPROC" ] && np=$NPROC
  while [ "$free" -lt "$np" ]; do
    wait -n 2>/dev/null
    for k in "${!PID[@]}"; do kill -0 "${PID[$k]}" 2>/dev/null || { wait "${PID[$k]}"; log "$k finished rc=$?"; free=$((free+NP[$k])); unset "PID[$k]"; }; done
  done
  log "launch $name ($inj $lvl Twall=$tw Tin=$tin np=$np)"; ( run_case "$name" "$inj" "$lvl" "$tw" "$tin" "$np" ) & PID[$name]=$!; NP[$name]=$np; free=$((free-np))
done < <(matrix "$MATRIX")
for k in "${!PID[@]}"; do wait "${PID[$k]}"; log "$k finished rc=$?"; done
python3 "$B/gci_m13.py" "$R" > "$R/gci.log" 2>&1 || log "gci_m13.py failed"
P="$R/push"; mkdir -p "$P"; cp "$LOG" "$R"/hardware.txt "$R"/m13_ref.txt "$R"/gci_summary.json "$P/" 2>/dev/null
for d in "$R"/runs/M13G-*/; do n=$(basename "$d"); mkdir -p "$P/$n"
  cp "$d"/case_meta.json "$d"/run.status "$d"/post.json "$d"/log.checkMesh* "$P/$n/" 2>/dev/null
  for l in "$d"/log.*; do [ -f "$l" ] && tail -n 300 "$l" > "$P/$n/$(basename "$l").tail"; done
  [ -d "$d/postProcessing" ] && tar czf "$P/$n/postProcessing.tgz" -C "$d" postProcessing
done
du -sh "$P" | tee -a "$LOG"
if [ "${PUSH:-$([ -n "${GH_TOKEN:-}" ] && echo 1 || echo 0)}" = 1 ]; then
  bash "$B/push_results.sh" "$RESULTS_REPO" "hf-results/$RUN_ID" "$P" "cfd/verification/hf/$RUN_ID" \
    "we-08 M13 GCI x dual-T results ($RUN_ID, M13_REF $M13_REF) from HF job - unreviewed, needs 2-engine peer review" 2>&1 | tee -a "$LOG"
else log "PUSH disabled; results stay in $P"; fi
log done
