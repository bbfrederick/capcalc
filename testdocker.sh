#!/bin/bash

MYIPADDRESS=`ifconfig en0 | grep 'inet ' | awk '{print $2}'`

docker run \
    --rm \
    --ipc host \
    --mount type=bind,source=/Users/frederic/code/capcalc/capcalc/data/examples,destination=/data \
    -it \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -u capcalc fredericklab/capcalc:latest \
    rapidtide \
        /data/src/sub-RAPIDTIDETEST.nii.gz \
        /data/dst/sub-RAPIDTIDETEST \
        --passes 3 \
        --nprocs 4 \
        --noglm
