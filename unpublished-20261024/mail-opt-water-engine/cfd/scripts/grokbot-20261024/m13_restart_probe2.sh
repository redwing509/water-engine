#!/bin/bash
# Probe: does the 0.008 precursor restart with the -mail numerics + 4-rank scotch decomposition?
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
source /usr/lib/openfoam/openfoam2512/etc/bashrc >/dev/null 2>&1
for c in M13-US20-coarse-mail M13-CARB60-coarse-mail; do
  SRC=/opt/water-engine/cfd/runs/$c; D=/smoke/r-$c; rm -rf $D; mkdir -p $D
  cp -a $SRC/0 $SRC/0.008 $SRC/constant $SRC/system $SRC/chemkin $D/; cd $D
  sed -i 's/^endTime .*/endTime 0.00806;/; s/^maxCo .*/maxCo 0.25;/' system/controlDict
  for f in system/decomposeParDict system/wallFilmRegion/decomposeParDict; do sed -i "s/^method .*/method scotch;/" $f; done
  decomposePar -force > log.dp 2>&1; decomposePar -region wallFilmRegion -force > log.dpf 2>&1
  timeout 420 mpirun --allow-run-as-root --oversubscribe -np 4 reactingParcelFoam -parallel > log.run 2>&1; rc=$?
  echo "restart $c rc=$rc steps=$(grep -c '^Time =' log.run) last=$(grep '^Time =' log.run | tail -1) maxcont=$(grep 'continuity' log.run | awk '{print $9}' | sort -g | tail -1) parcels=$(grep 'Current number of parcels' log.run | tail -1)"
done
