FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && apt-get clean

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/bin/bash", "/start.sh"]
