FROM ubuntu:24.04

WORKDIR /app

# Install build tools + Python 3.13
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    build-essential \
    gcc \
    g++ \
    ninja-build \
    ca-certificates \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        python3.13 \
        python3.13-dev \
        python3.13-venv \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/python3.13 /usr/bin/python \
    && ln -sf /usr/bin/python3.13 /usr/bin/python3

# Create venv with Python 3.13
RUN python3.13 -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Unpack the pandas source tree
COPY pandas.tar.gz /app/
RUN mkdir -p /app/pandas \
    && tar -xzf pandas.tar.gz -C /app/pandas/ \
    && rm pandas.tar.gz
