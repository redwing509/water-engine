#!/bin/bash
# Run module 13 cases sequentially at 2 MPI ranks; log peak RSS (sum over ranks).
cd "$(dirname "$0")/.." || exit 1
CASES=${CASES:-"M13-US20-coarse M13-CARB60-coarse"}
log() { echo "$(date '+%F %T %Z') $*" >> port13/progress.txt; }
for c in $CASES; do
  python3 port13/make_port_case.py $c >/dev/null || { log "$c make FAILED"; continue; }
  log "$c start"
  t0=$(date +%s)
  ( cd runs/$c && ./Allrun > allrun.nohup 2>&1 ) &
  pid=$!; peak=0
  while kill -0 $pid 2>/dev/null; do
    s=$(ps -eo rss,comm | awk '$2=="reactingParcelFo"||$2=="reactingParcelFoam"{t+=$1} END{print int(t/1024)}')
    [ "$s" -gt "$peak" ] && peak=$s
    sleep 5
  done
  wait $pid; rc=$?
  echo $peak > runs/$c/peak_rss_mb.txt
  log "$c done rc=$rc runtime_s $(( $(date +%s)-t0 )) peak RSS ${peak} MB ($(tail -1 runs/$c/log.Allrun))"
  python3 port13/post_m13.py $c >> port13/progress.txt 2>&1 || log "$c post FAILED"
done
log "M13 BATCH COMPLETE"
