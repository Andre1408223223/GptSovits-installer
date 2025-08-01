FROM continuumio/miniconda3

WORKDIR /app

# Create the environment 'gpt' during build time
RUN conda create -y -n gpt python=3.10 && conda clean -afy

# Install essential build tools
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    make \
    g++ \
    && apt-get clean

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/bin/bash", "/start.sh"]
