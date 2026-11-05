# CFD provenance — A1-BLEND-fine grid check (wme1)

## Image
- Registry: Docker Hub
- Repository: opencfd/openfoam-default
- Tag: 2512
- Digest: sha256:33fb575aa9980d2bc42fd58c75ae698c489293ba30c991380fe3f899c622f319
- Pulled: 2026-10-23 (mail)
- Installed apps: sprayFoam, blockMesh, decomposePar at
  /usr/lib/openfoam/openfoam2512/platforms/linux64GccDPInt32Opt/bin/

## Case
- Source: Grok Bot box, job water-engine-20261023-043000, 2026-10-23 PDT
- Bundle: wme1-cfd.bundle (branch wme1-cfd, HEAD 0034c5db6d0795be31514e78fb5bf28506d2854a)
- Case tarball: A1-BLEND-fine.tar.gz, sha256 f9dc33756ab849592a89fe3a52f6e3d725e933b0aacd0343b5c08fd0a5ffe4a2
- Case: runs/A1-BLEND-fine — A1 cond, BLEND liquid (60% H2O / 40% CH3OH), 1.5x refinement,
  p=100 kPa, T=360 K, dP=500 kPa, d=0.25 mm, dur=5 ms
- Grid: 62 x 62 x 150 = 576,600 cells (base 41 x 41 x 100 = 168,100; ratio 3.43)
- RAM est: ~5.3 GB peak over 6 ranks; allocated 12 GB

## Execution
- Launcher: run_case.sh (blockMesh, decomposePar simple n(1 6 1), mpirun --oversubscribe -np 6 sprayFoam -parallel)
- Container: docker run --rm --network none --cap-drop ALL --security-opt no-new-privileges:true --pids-limit 512 --cpus 12 --memory 12g -v /opt/water-engine/cfd:/opt/water-engine/cfd
- Scheduler: ai-job --owner hermes --resource cpu-heavy --ttl 720
- Runtime: 3037 s wall, rc 0, finished 2026-10-23T14:41:50Z
- Outputs: runs/A1-BLEND-fine/0 (final field), postProcessing/distribution1/{0.0005..0.006}/{Ux,Uy,Uz}.xy
- Status: COMPLETE, rc 0

## Fixes applied to run_case.sh on mail
- chmod -R 777 /opt/water-engine/cfd (container runs root, bind-mount had restrictive ownership)
- mpirun --allow-run-as-root (OpenFOAM v2512 refuses mpirun as root without it)