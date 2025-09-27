FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# System deps
RUN apt-get update && apt-get install -y \
    python3 python3-pip git ffmpeg libglib2.0-0 libsm6 libxrender1 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Python deps first (cache-friendly)
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Code
WORKDIR /workspace
COPY wan_backend.py app.py start.sh ./
RUN chmod +x start.sh

# Model path (จะ cache ไว้ใน volume/ติด image ก็ได้)
ENV MODEL_ID="Wan-AI/Wan2.1-T2V-1.3B" \
    MODEL_SOURCE="modelscope" \
    TORCH_CUDA_ARCH_LIST="8.6" \
    HF_HOME="/workspace/hf" \
    MS_HOME="/workspace/ms" \
    TRANSFORMERS_CACHE="/workspace/hf" \
    TOKENIZERS_PARALLELISM=false

EXPOSE 8000
CMD ["./start.sh"]
