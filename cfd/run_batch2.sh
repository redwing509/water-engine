#!/bin/bash
# Module 12 phase A batch (v2, per amendment water-engine-20261022-185000):
# wait for A0, run cases sequentially at 6 ranks, record peak RAM per case,
# and run the 1.5x grid check (A1-BLEND-fine) only if its RAM estimate fits.
cd "$(dirname "$0")"; R=runs; P=progress.txt
log(){ echo "$(date '+%F %T %Z') $*" >> $P; }
sample(){ # sample total sprayFoam RSS into $1/peak_rss_mb.txt until the case finishes
  local d=$1 pid=$2 pk=0 s
  [ -f $d/peak_rss_mb.txt ] && pk=$(cat $d/peak_rss_mb.txt)
  while :; do
    s=$(ps -o rss= -C sprayFoam | awk '{t+=$1} END{print int(t/1024)}')
    [ "$s" -gt "$pk" ] && pk=$s && echo $pk > $d/peak_rss_mb.txt
    [ -f $d/runtime.txt ] && break
    kill -0 $pid 2>/dev/null || break
    sleep 15
  done
}
a0=$(pgrep -f "run_case.sh A0" | head -1); [ -n "$a0" ] && sample $R/A0 $a0
while pgrep -f "run_case.sh A0" >/dev/null; do sleep 30; done
log "A0 finished: $(cat $R/A0/runtime.txt 2>/dev/null || echo NO-RUNTIME), peak RSS $(cat $R/A0/peak_rss_mb.txt 2>/dev/null) MB (sampling began ~14 min into the run)"
for c in A1-H2O A1-CH3OH A1-BLEND A2-H2O A2-CH3OH A2-BLEND A1-BLEND-fine; do
  if [ -f $R/$c/runtime.txt ]; then log "$c already done"; continue; fi
  if [ $c = A1-BLEND-fine ]; then
    base=$(cat $R/A1-BLEND/peak_rss_mb.txt 2>/dev/null || echo 0)
    est=$(( base * 343 / 100 ))   # cells 62*62*150 / 41*41*100 = 3.43x
    avail=$(( $(awk '/MemAvailable/{print $2}' /proc/meminfo) / 1024 ))
    limit=$(( avail - 1024 )); [ $limit -gt 4096 ] && limit=4096   # amendment budget ~4 GB
    echo "A1-BLEND peak ${base} MB x3.43 = est ${est} MB; free-now ${avail} MB; limit ${limit} MB" > $R/$c/ram_estimate.txt
    if [ $base -le 0 ] || [ $est -gt $limit ]; then
      echo "SKIPPED: needs mail" >> $R/$c/ram_estimate.txt; log "$c SKIPPED needs mail ($(head -1 $R/$c/ram_estimate.txt))"; continue
    fi
    log "$c fits ($(head -1 $R/$c/ram_estimate.txt))"
  fi
  log "$c start"
  ( cd $R && ../run_case.sh $c 6 ) & cp=$!
  sample $R/$c $cp; wait $cp && log "$c done $(cat $R/$c/runtime.txt), peak RSS $(cat $R/$c/peak_rss_mb.txt 2>/dev/null) MB" || log "$c FAILED (see $R/$c/log.sprayFoam)"
  python3 scripts/postprocess.py > /dev/null 2>>$P
done
python3 scripts/postprocess.py > results/postprocess_stdout.txt 2>>$P
log "BATCH COMPLETE"
