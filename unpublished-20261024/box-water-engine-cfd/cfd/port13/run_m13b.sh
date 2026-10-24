#!/bin/bash
# Continuation of run_m13.sh (job water-engine-20261023-124600 step 4).
# 1) keep sampling the running M13-US20-coarse Allrun (pid $1) and post-process it;
# 2) run M13-CARB60-coarse restarted from the US20 gas-only precursor at t = 0.008 s
#    (identical mesh/BCs/precursor; only the cloud injector differs), saving 8 of 23 ms.
cd "$(dirname "$0")/.." || exit 1
. /usr/lib/openfoam/openfoam2512/etc/bashrc >/dev/null 2>&1 || true
log() { echo "$(date '+%F %T %Z') $*" >> port13/progress.txt; }
rss() { ps -eo rss,comm | awk '$2=="reactingParcelFo"||$2=="reactingParcelFoam"{t+=$1} END{print int(t/1024)}'; }
US=M13-US20-coarse; CB=M13-CARB60-coarse; P0=0.008
pid=$1; peak=$(cat runs/$US/peak_rss_mb.partial 2>/dev/null || echo 0)
while kill -0 $pid 2>/dev/null; do s=$(rss); [ "$s" -gt "$peak" ] && peak=$s; sleep 5; done
echo $peak > runs/$US/peak_rss_mb.txt
log "$US done peak RSS ${peak} MB ($(tail -1 runs/$US/log.Allrun))"
python3 port13/post_m13.py $US >> port13/progress.txt 2>&1 || log "$US post FAILED"
# ---- CARB60 from the precursor
for d in runs/$US/processor0/$P0 runs/$US/processor1/$P0; do [ -d $d ] || { log "$CB: precursor $d missing, ABORT"; exit 1; }; done
python3 port13/make_port_case.py $CB >/dev/null || { log "$CB make FAILED"; exit 1; }
cd runs/$CB || exit 1
rm -rf 0 constant/polyMesh constant/wallFilmRegion/polyMesh processor*
cp -a ../$US/0 . && cp -a ../$US/constant/polyMesh constant/ && cp -a ../$US/constant/wallFilmRegion/polyMesh constant/wallFilmRegion/
[ -d ../$US/constant/triSurface ] && cp -a ../$US/constant/triSurface constant/
for p in processor0 processor1; do
  mkdir -p $p && cp -a ../$US/$p/constant $p/ && cp -a ../$US/$p/$P0 $p/
  rm -rf $p/$P0/lagrangian $p/$P0/uniform/lagrangian $p/$P0/wallFilmRegion/lagrangian
done
cp ../$US/log.checkMesh log.checkMesh.fromUS20 2>/dev/null
echo "precursor 0-$P0 s copied from $US (identical mesh, BCs, gas-only phase); lagrangian state removed" > PRECURSOR_FROM_US20.txt
cd ../..
log "$CB start (restart from $US t=$P0)"
t0=$(date +%s)
( cd runs/$CB && . /usr/lib/openfoam/openfoam2512/etc/bashrc >/dev/null 2>&1;
  mpirun --oversubscribe -np 2 reactingParcelFoam -parallel > log.reactingParcelFoam 2>&1; rc=$?
  reconstructPar -latestTime > log.reconstructPar 2>&1
  reconstructPar -region wallFilmRegion -latestTime > log.reconstructParFilm 2>&1
  echo "reactingParcelFoam rc=$rc" > log.Allrun; exit $rc ) &
pid=$!; peak=0
while kill -0 $pid 2>/dev/null; do s=$(rss); [ "$s" -gt "$peak" ] && peak=$s; sleep 5; done
wait $pid; rc=$?
echo $peak > runs/$CB/peak_rss_mb.txt
log "$CB done rc=$rc runtime_s $(( $(date +%s)-t0 )) peak RSS ${peak} MB"
python3 port13/post_m13.py $CB >> port13/progress.txt 2>&1 || log "$CB post FAILED"
log "M13 BATCH COMPLETE"
