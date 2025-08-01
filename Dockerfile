FROM python:3.10-slim

WORKDIR /app

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
