#!/bin/bash
set -e

# Initialize conda
source /opt/conda/etc/profile.d/conda.sh

# Activate environment
conda activate gpt

# If GPT-SoVITS is not installed yet
if [ ! -e /app/api.py ]; then
    echo "Installing GPT-SoVITS..."

    echo "Cloning GPT-SoVITS into /app/gpt-temp..."
    git clone https://github.com/RVC-Boss/GPT-SoVITS.git /app/gpt-temp

    echo "Moving contents up one level..."
    mv /app/gpt-temp/* /app
    mv /app/gpt-temp/.git /app
    rm -rf /app/gpt-temp

    echo "Installing Python dependencies into venv..."
    pip install --upgrade pip
    pip install --no-cache-dir -r /app/extra-req.txt
    pip install --no-cache-dir -r /app/requirements.txt

    echo "Cloning pretrained models..."
    rm -rf /app/GPT_SoVITS/pretrained_models
    git clone https://huggingface.co/lj1995/GPT-SoVITS /app/GPT_SoVITS/pretrained_models

    echo "Installed GPT-SoVITS successfully"
else
    echo "GPT-SoVITS already installed, using existing environment"
fi

# Your commands here
tail -f /dev/null
