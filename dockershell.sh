#!/bin/bash

VERSION=latest

docker pull fredericklab/capcalc:${VERSION}
docker run -it fredericklab/capcalc:${VERSION} xyzzy
