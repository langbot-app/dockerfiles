FROM nikolaik/python-nodejs:python3.12-nodejs22-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    wget \
    ca-certificates \
    openssh-client \
    jq \
    unzip \
    fontconfig \
    fonts-noto-cjk \
    && fc-cache -f \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/sandbox-requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/sandbox-requirements.txt \
    && rm /tmp/sandbox-requirements.txt

# Use Matplotlib's installation-wide defaults rather than a root-only config
# or a shared writable MPLCONFIGDIR. User/script overrides still take priority.
COPY matplotlibrc /tmp/sandbox-matplotlibrc
RUN install -m 644 /tmp/sandbox-matplotlibrc \
        "$(python -c 'import matplotlib; print(matplotlib.get_data_path())')/matplotlibrc" \
    && rm /tmp/sandbox-matplotlibrc

# Exercise real rendering on every architecture before an image can be pushed.
COPY tests/smoke_test.py /tmp/sandbox-smoke-test.py
RUN python /tmp/sandbox-smoke-test.py \
    && rm /tmp/sandbox-smoke-test.py \
    && rm -rf /root/.cache/matplotlib

WORKDIR /workspace
