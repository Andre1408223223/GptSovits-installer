FROM alpine:latest

# Install git and bash (bash optional, sh is fine)
RUN apk update && apk add --no-cache git

WORKDIR /app

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
