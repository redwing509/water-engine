#!/bin/bash
# Module 12 phase A batch: wait for A0, then cases sequentially, post-process after each.
cd "$(dirname "$0")"; R=runs; P=progress.txt
log(){ echo "$(date '+%F %T %Z') $*" >> $P; }
while pgrep -f "run_case.sh A0" >/dev/null; do sleep 60; done
log "A0 finished: $(cat $R/A0/runtime.txt 2>/dev/null || echo NO-RUNTIME)"
for c in A1-H2O A1-CH3OH A1-BLEND A2-H2O A2-CH3OH A2-BLEND A1-BLEND-fine; do
  if [ -f $R/$c/runtime.txt ]; then log "$c already done"; continue; fi
  log "$c start"
  ( cd $R && ../run_case.sh $c 6 ) && log "$c done $(cat $R/$c/runtime.txt)" || log "$c FAILED (see $R/$c/log.sprayFoam)"
  python3 scripts/postprocess.py > /dev/null 2>>$P
done
python3 scripts/postprocess.py > results/postprocess_stdout.txt 2>>$P
log "BATCH COMPLETE"
