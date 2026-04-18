FROM nikolaik/python-nodejs:python3.12-nodejs22-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    wget \
    ca-certificates \
    openssh-client \
    jq \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
