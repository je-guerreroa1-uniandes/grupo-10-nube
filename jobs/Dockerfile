# Otra opción:
FROM python:3.9.16-slim-buster

#RUN set -eux; \
#    apt-get update; \
#    apt-get install -y --no-install-recommends \
#    p7zip-full \
#    ; \
#    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

# To see Python output when running daemonized in Docker
# -u     : force the stdout and stderr streams to be unbuffered;
CMD [ "celery", "-A", "app", "worker", "-l", "info", "-Q", "files"]