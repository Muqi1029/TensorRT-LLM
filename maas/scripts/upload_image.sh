#!/usr/bin/env bash

set -euxo pipefail

IMAGE="maas-tensorrt-llm-shortcut:v1.3.0rc9-f1-truncate-b"

curl --location 'http://arsenal-maas-prod.kanzhun-inc.com/api/maas/build/image/import/common' \
  --header 'Content-Type: application/json' \
  --header 'Cookie: t_arsenal-web=xxxxxxxxxx' \
  --data "{
    \"name\": \"$IMAGE\",
    \"url\": \"harbor.weizhipin.com/arsenal-ai/$IMAGE\",
    \"describe\": \"$IMAGE\",
    \"imageType\": \"LLM_SHORTCUT_transformers\"
  }"
