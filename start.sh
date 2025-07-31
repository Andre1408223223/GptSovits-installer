#!/bin/sh
if [ ! -e /app/api.py ]; then
    echo "Installing GPT-SoVITS..."

    echo "Cloning GPT-SoVITS into /app/gpt-temp..."
    git clone https://github.com/RVC-Boss/GPT-SoVITS.git /app/gpt-temp

    echo "Moving contents up one level..."
    mv /app/gpt-temp/* /app
    mv /app/gpt-temp/.* /app 2>/dev/null || true

    echo "Removing temporary folder..."
    rm -rf /app/gpt-temp

    # inatall dependesies

    echo "installed succsessfully"
else
    echo "GPT-SoVITS already installed"
fi

# Keep container running
tail -f /dev/null
