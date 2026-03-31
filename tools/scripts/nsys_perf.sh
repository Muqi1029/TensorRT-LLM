#!/usr/bin/env bash

set -xueo pipefail

# delay duration nsys
nsys profile --trace-fork-before-exec=true \
	--cuda-graph-trace=node \
	-o trtllm.out \
	--delay 10 \
	--duration 100 \
	trtllm-serve ${GR_QWEN_05B} \
	--backend tensorrt \
	--max_seq_len 1024 \
	--max_batch_size 128 \
	--max_beam_width 32

# session nsys
nsys launch --session=trtllm_perf \
    --trace-fork-before-exec=true \
    --cuda-graph-trace=node \
    trtllm-serve ${GR_F1_QWEN_05B} \
    --max_beam_width 96 \
    --max_batch_size 32 \
    --backend tensorrt \
    --max_seq_len 2048 \
    --port 10001

nsys start --session trtllm_perf -o trtllm_5con_32beam
nsys stop --session trtllm_perf
