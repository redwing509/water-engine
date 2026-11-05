#!/bin/bash
# Job #8 fine-mesh GCI levels on mail (Grok Bot, 2026-10-24, James t75u). Runs under ONE ai-job cpu-heavy lock.
# Slots (12 ranks total, docker --cpus caps, nice 19; leaves 4 cores for Claude's M13 water-engine work + services):
#   slot A: A2-BLEND-r225 (6 ranks)                     -- critical path
#   slot B: A1-BLEND-r225 (3 ranks), then A1-BLEND-r100-mail (3 ranks, same-machine base level)
#   slot C: A2-BLEND-r150 (3 ranks), then A2-BLEND-r100-mail (3 ranks, same-machine base level)
B=/opt/water-engine/cfd/gci-20261024; R=$B/runs; IMG=opencfd/openfoam-default:2512
FL=$B/finish.log
run(){ # case ranks
  local c=$1 n=$2 mem=$3
  echo "$(date -u +%FT%TZ) START $c ranks=$n mem=$mem" >> $FL
  docker run --rm --name gci-$c --network none --cap-drop ALL --security-opt no-new-privileges:true \
    --pids-limit 512 --cpus $n --memory $mem --memory-swap $mem -v $B:$B $IMG \
    nice -n 19 bash $B/gci_case.sh $R/$c $n > $R/$c.docker.log 2>&1
  local rc=$?; echo "$(date -u +%FT%TZ) END $c rc=$rc $(cat $R/$c/runtime.txt 2>/dev/null)" >> $FL; return $rc
}
echo "$(date -u +%FT%TZ) driver start pid=$$" >> $FL
( run A2-BLEND-r225 6 22g ) & pA=$!
( run A1-BLEND-r225 3 20g; run A1-BLEND-r100-mail 3 6g ) & pB=$!
( run A2-BLEND-r150 3 8g; run A2-BLEND-r100-mail 3 6g ) & pC=$!
wait $pA; rA=$?; wait $pB; rB=$?; wait $pC; rC=$?
echo "$(date -u +%FT%TZ) ALL DONE slotA=$rA slotB=$rB slotC=$rC" >> $FL
[ $rA -eq 0 ] && [ $rB -eq 0 ] && [ $rC -eq 0 ]
