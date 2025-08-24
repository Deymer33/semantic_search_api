FROM python:3.11-slim

ENV PIP_NO_CACHE_DIR=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential cmake libprotobuf-dev protobuf-compiler \
        cron mariadb-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requeriment.txt ./

RUN pip install --no-cache-dir -r requeriment.txt && \
    apt-get purge -y build-essential cmake libprotobuf-dev protobuf-compiler && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN mkdir -p /app/data

COPY crontab.txt /etc/cron.d/embeddings-cron
RUN chmod 0644 /etc/cron.d/embeddings-cron && crontab /etc/cron.d/embeddings-cron

COPY cronjob.sh /cronjob.sh
RUN chmod +x /cronjob.sh

EXPOSE 8000
CMD ["/cronjob.sh"]
