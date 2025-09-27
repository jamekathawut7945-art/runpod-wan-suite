#!usrbinenv bash
set -e
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb256
uvicorn appapp --host 0.0.0.0 --port 8000
