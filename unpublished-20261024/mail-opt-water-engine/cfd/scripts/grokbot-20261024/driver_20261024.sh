#!/bin/bash
# grokbot 2026-10-24 driver: A2 batch then M13 batch, each its own ai-job (water-engine) so Hermes can interleave.
S=/opt/water-engine/cfd/scripts/grokbot-20261024
run() { # $1 name  $2 ttl-min  $3 task  $4 batch script
  echo "$(date -u +%FT%TZ) submit $1"
  ai-job --owner grokbot --resource water-engine --task "$3" --ttl "$2" --wait -- \
    docker run --rm --pull=never --name we-grokbot-$1 --network none --cpus 8 --memory 24g --memory-swap 24g \
      --pids-limit 1024 --user 0:0 --mount type=bind,src=/opt/water-engine/cfd,dst=/opt/water-engine/cfd \
      --entrypoint /bin/bash opencfd/openfoam-default:2512 $S/$4
  echo "$(date -u +%FT%TZ) $1 finished rc=$?"
}
run a2  150 "grokbot A2-C2H5OH/-RD/EBLEND -mail (Tc clamp, ReitzDiwakar) 3 ms, 4 ranks" a2_batch.sh
run m13 780 "grokbot M13 US20+CARB60 coarse -mail (scotch 4r, maxCo .25 SOI+2ms, bounded k-eps, nOuter 3) to 23 ms" m13_batch.sh
echo "$(date -u +%FT%TZ) driver done"
