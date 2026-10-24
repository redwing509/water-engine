# CPU image (recommended) for we-08 M13 port-spray/wall-film GCI. Same OpenFOAM build as all WME-1 CFD so far.
FROM opencfd/openfoam-default:2512@sha256:33fb575aa9980d2bc42fd58c75ae698c489293ba30c991380fe3f899c622f319
USER root
RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates python3 python3-numpy \
 && rm -rf /var/lib/apt/lists/*
COPY . /bundle
RUN chmod +x /bundle/*.sh /bundle/*.py && mkdir -p /out
WORKDIR /bundle
ENTRYPOINT []
CMD ["bash", "/bundle/run.sh"]
