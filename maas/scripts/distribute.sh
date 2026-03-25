#!/usr/bin/env bash

set -euxo pipefail

python scripts/build_wheel.py \
	--cuda_architectures "89-real;80-real;120-real;90-real" \
	--install \
	--no-venv --extra-cmake-vars ENABLE_UCX=OFF --clean
