FROM alpine:latest

# Install bash, wget, git
RUN apk add --no-cache bash wget git

# Set working directory
WORKDIR /app

# Copy the script
COPY start.sh /start.sh

# Make it executable
RUN chmod +x /start.sh

# Use bash instead of sh
CMD ["/bin/bash", "/start.sh"]
