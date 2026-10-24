#!/bin/bash
# Probe from t=0: which change (ranks/decomposition or numerics edits) breaks the M13 US20 start?
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
source /usr/lib/openfoam/openfoam2512/etc/bashrc >/dev/null 2>&1
SRC=/opt/water-engine/cfd/runs/M13-US20-coarse-mail
for v in orig2 orig4 mine2 mine4scotch orig4scotch; do
  D=/smoke/probe-$v; rm -rf $D; mkdir -p $D
  cp -a $SRC/0 $SRC/constant $SRC/system $SRC/chemkin $D/
  cd $D
  sed -i 's/^endTime .*/endTime 0.00004;/; s/^maxCo .*/maxCo 1.0;/' system/controlDict
  case $v in orig*) sed -i 's/nOuterCorrectors 3;/nOuterCorrectors 1;/' system/fvSolution
                    sed -i 's/bounded Gauss upwind/Gauss upwind/' system/fvSchemes ;; esac
  np=4; case $v in *2) np=2;; esac
  meth=simple; case $v in *scotch) meth=scotch;; esac
  for f in system/decomposeParDict system/wallFilmRegion/decomposeParDict; do
    [ -f $f ] && sed -i "s/^numberOfSubdomains .*/numberOfSubdomains $np;/; s/^method .*/method $meth;/; s/n (4 1 1)/n ($np 1 1)/" $f
  done
  decomposePar -force > log.dp 2>&1; decomposePar -region wallFilmRegion -force > log.dpf 2>&1
  timeout 300 mpirun --allow-run-as-root --oversubscribe -np $np reactingParcelFoam -parallel > log.run 2>&1; rc=$?
  echo "probe $v np=$np rc=$rc steps=$(grep -c '^Time =' log.run) last=$(grep '^Time =' log.run | tail -1) maxcont=$(grep 'continuity' log.run | awk '{print $9}' | sort -g | tail -1)"
done
