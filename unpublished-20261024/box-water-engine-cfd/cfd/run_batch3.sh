#!/bin/bash
# Module 12 ethanol batch (relay job water-engine-20261023-124600): A1/A2 x C2H5OH / EBLEND (60/40 wt% H2O/C2H5OH),
# same phase-A setup, run sequentially at 4 MPI ranks (decomposition (1 4 1) instead of (1 6 1): the job caps the box at
# 6 ranks in total and 2 are kept for the module 13 port case), peak RSS sampled as in run_batch2.sh.
cd "$(dirname "$0")"; R=runs; P=progress.txt
log(){ echo "$(date '+%F %T %Z') $*" >> $P; }
sample(){ local d=$1 pid=$2 pk=0 s
  while :; do
    s=$(ps -o rss= -C sprayFoam | awk '{t+=$1} END{print int(t/1024)}')
    [ "$s" -gt "$pk" ] && pk=$s && echo $pk > $d/peak_rss_mb.txt
    [ -f $d/runtime.txt ] && break; kill -0 $pid 2>/dev/null || break; sleep 15
  done; }
for c in ${CASES:-A1-C2H5OH A1-EBLEND A2-C2H5OH A2-EBLEND}; do
  if [ -f $R/$c/runtime.txt ]; then log "$c already done"; continue; fi
  log "$c start (4 ranks)"
  ( cd $R && ../run_case.sh $c 4 ) & cp=$!
  sample $R/$c $cp; wait $cp && log "$c done $(cat $R/$c/runtime.txt), peak RSS $(cat $R/$c/peak_rss_mb.txt 2>/dev/null) MB" || log "$c FAILED (see $R/$c/log.sprayFoam)"
  python3 scripts/postprocess.py > /dev/null 2>>$P
done
python3 scripts/postprocess.py > results/postprocess_stdout.txt 2>>$P
log "ETHANOL BATCH COMPLETE"
