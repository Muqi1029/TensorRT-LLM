#!/usr/bin/env bash

set -euxo pipefail

python scripts/build_wheel.py \
	--cuda_architectures "89-real" \
	--install \
	--extra-cmake-vars ENABLE_UCX=OFF \
    --skip_building_wheel
