#!/bin/bash
set -e
set -i
set -x

docker build -t vidi-urls-plugin -f Dockerfile .
docker inspect vidi-urls-plugin

docker run \
    -e WORKSPACE=/srv/WORKSPACE \
    -v $WORKSPACE:/srv/WORKSPACE \
    vidi-urls-plugin sh /srv/WORKSPACE/build/build_rpm.sh
