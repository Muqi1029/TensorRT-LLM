#!/usr/bin/env bash

set -exuo pipefail

IMAGE="harbor.weizhipin.com/arsenal-ai/maas-tensorrt-llm-shortcut"
# TAG="v1.2.0rc2-protocol-log"
TAG="1.3.0rc6-Ada"

docker build --network=host -t $IMAGE:$TAG --platform=linux/amd64 -f Dockerfile .
docker push $IMAGE:$TAG
