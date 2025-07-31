# !/usr/bin/env bash

# Only clone if not already installed
if [ ! -e /app/api.py ]; then
    echo "Installing GPT-SoVITS..."

    echo "Cloning GPT-SoVITS into /app/gpt-temp..."
    git clone https://github.com/RVC-Boss/GPT-SoVITS.git /app/gpt-temp

    echo "Moving contents up one level..."
    mv /app/gpt-temp/* /app
    mv /app/gpt-temp/.git /app
    rm -rf /app/gpt-temp

    echo "instailling cmake"
    apt install -y build-essential cmake
    echo "Installing Python dependencies from requirements.txt..."
    pip install --no-cache-dir -r /app/extra-req.txt
    pip install --no-cache-dir -r /app/requirements.txt

    echo "Installed successfully"
else
    echo "GPT-SoVITS already installed"
fi



# Prevent container from exiting
tail -f /dev/null
