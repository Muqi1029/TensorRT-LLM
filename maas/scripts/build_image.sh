#!/usr/bin/env bash

set -exuo pipefail

IMAGE="harbor.weizhipin.com/arsenal-ai/maas-tensorrt-llm-shortcut"

# TAG="v1.2.0rc2-protocol-log"
TAG="v1.3.0rc7-f1-truncate"

docker build --network=host -t $IMAGE:$TAG --platform=linux/amd64 -f maas/Dockerfile .
docker push $IMAGE:$TAG
