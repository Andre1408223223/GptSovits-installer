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

    echo "Installed successfully"
else
    echo "GPT-SoVITS already installed"
fi


# Prevent container from exiting
tail -f /dev/null
