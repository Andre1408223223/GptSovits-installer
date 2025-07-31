FROM python:3.10-slim

WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*

# Clone the GPT-SoVITS repo
RUN git clone https://github.com/RVC-Boss/GPT-SoVITS.git

# Set working directory to the cloned repo
WORKDIR /app/GPT-SoVITS

# Run the api.py file
CMD ["python", "api.py"]
