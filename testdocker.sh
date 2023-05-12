#!/bin/bash

MYIPADDRESS=`ifconfig en0 | grep 'inet ' | awk '{print $2}'`

docker run \
    --rm \
    --ipc host \
    --mount type=bind,source=/Users/frederic/code/capcalc/capcalc/data/,destination=/data \
    -it \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -u capcalc fredericklab/capcalc:latest \
    capfromtcs \
        -i /data/manyfiles.txt \
        -o /data/output/manyfiles \
        --sampletime=0.72 \
        --varnorm \
        -m \
        -b 4800 \
        -S 1200 \
        --quality \
        -E default \
        --minout=2
