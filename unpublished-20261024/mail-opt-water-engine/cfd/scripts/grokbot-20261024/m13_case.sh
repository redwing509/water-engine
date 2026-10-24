#!/bin/bash
# usage: m13_case.sh <casedir>   4 ranks, 3 segments: seg0 gas-only precursor 0->0.008 (maxCo 1.0, as generator),
# seg1 SOI 0.008->0.010 (maxCo 0.25), seg2 0.010->0.023 (maxCo 0.5).
# 2026-10-24: the copied 0.008 precursor would not restart (p_rgh continuity error -16 on step 1 even with the
# original schemes/maxCo), so it is set aside as 0.008.unusable-precursor and the precursor is recomputed.
. /usr/lib/openfoam/openfoam2512/etc/bashrc >/dev/null 2>&1 || true
cd "$1" || exit 2; N=4; END0=${END0:-0.008}; END2=${END2:-0.023}; END1=${END1:-0.010}
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
st() { echo "$(date -u +%FT%TZ) $*" >> run.status; }
start=$(date +%s); st start
if [ ! -d processor0 ]; then
  [ -d 0.008 ] && [ ! -e 0.008.unusable-precursor ] && [ ! -e PRECURSOR_DONE ] && mv 0.008 0.008.unusable-precursor
  decomposePar -force > log.decomposePar 2>&1 || { st "decomposePar failed"; exit 3; }
  decomposePar -region wallFilmRegion -force > log.decomposeParFilm 2>&1 || { st "decomposePar film failed"; exit 4; }
fi
if [ ! -e PRECURSOR_DONE ]; then
  sed -i "s/^endTime .*/endTime         $END0;   \/\/ SEGMENT 0 (gas-only precursor)/; s/^maxCo .*/maxCo           1.0;   \/\/ SEGMENT 0/" system/controlDict
  mpirun --allow-run-as-root --oversubscribe -np $N reactingParcelFoam -parallel > log.reactingParcelFoam.seg0 2>&1; rc=$?
  st "seg0 rc=$rc last='$(grep '^Time = ' log.reactingParcelFoam.seg0 | tail -1)' nan_lines=$(grep -ciE '\bnan\b' log.reactingParcelFoam.seg0)"
  [ $rc -eq 0 ] || { echo "runtime_s $(( $(date +%s)-start ))" > runtime.txt; st "end rc=$rc"; exit $rc; }
  [ "$END0" = "0.008" ] && touch PRECURSOR_DONE
  [ "$END1" = "$END0" ] && { echo "runtime_s $(( $(date +%s)-start ))" > runtime.txt; st "end rc=0 (seg0 only)"; exit 0; }
fi
sed -i "s/^endTime .*/endTime         $END1;   \/\/ SEGMENT 1/; s/^maxCo .*/maxCo           0.25;   \/\/ SEGMENT 1/" system/controlDict
mpirun --allow-run-as-root --oversubscribe -np $N reactingParcelFoam -parallel > log.reactingParcelFoam.seg1 2>&1; rc=$?
st "seg1 rc=$rc last='$(grep '^Time = ' log.reactingParcelFoam.seg1 | tail -1)' nan_lines=$(grep -ciE '\bnan\b' log.reactingParcelFoam.seg1)"
if [ $rc -eq 0 ] && [ "$END2" != "$END1" ]; then
  sed -i "s/^endTime .*/endTime         $END2;   \/\/ SEGMENT 2/; s/^maxCo .*/maxCo           0.5;   \/\/ SEGMENT 2 (after SOI+2 ms)/" system/controlDict
  mpirun --allow-run-as-root --oversubscribe -np $N reactingParcelFoam -parallel > log.reactingParcelFoam.seg2 2>&1; rc=$?
  st "seg2 rc=$rc last='$(grep '^Time = ' log.reactingParcelFoam.seg2 | tail -1)' nan_lines=$(grep -ciE '\bnan\b' log.reactingParcelFoam.seg2)"
fi
echo "runtime_s $(( $(date +%s)-start ))" > runtime.txt
reconstructPar -latestTime > log.reconstructPar 2>&1
st "end rc=$rc"
exit $rc
