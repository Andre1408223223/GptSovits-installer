#!/usr/bin/env bash

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment in /app/venv..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

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

which python3

# Keep container running (replace with your actual entry command if needed)
tail -f /dev/null
