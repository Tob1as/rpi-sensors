FROM python:3.10-alpine

ARG VCS_REF
ARG BUILD_DATE

LABEL org.opencontainers.image.authors="Tobias Hargesheimer <docker@ison.ws>" \
	org.opencontainers.image.title="PI-Sensors" \
	org.opencontainers.image.description="Raspberry Pi GPIO Sensors (AlpineLinux with Python 3)" \
	org.opencontainers.image.licenses="Apache-2.0" \
	org.opencontainers.image.created="${BUILD_DATE}" \
	org.opencontainers.image.revision="${VCS_REF}" \
	org.opencontainers.image.url="https://hub.docker.com/r/tobi312/rpi-sensors/" \
	org.opencontainers.image.source="https://github.com/Tob1as/rpi-sensors"

SHELL ["/bin/sh", "-euxo", "pipefail", "-c"]

#COPY *.py /service/
COPY dht_sensor.py /service/

RUN \
    #mkdir /service ; \
    apk add --no-cache --virtual .build-deps \
        gcc libc-dev \
        mariadb-connector-c-dev \
    ; \
    apk add --no-cache \
        libgpiod \
        mariadb-connector-c \
    ; \
    pip3 install --no-cache-dir rpi.gpio; \
    #pip3 install --no-cache-dir sysv-ipc; \
    pip3 install --no-cache-dir adafruit-circuitpython-dht; \
    pip3 install --no-cache-dir mariadb==1.0.11; \
    pip3 install --no-cache-dir paho-mqtt; \
    apk del --no-network --purge .build-deps; \
    chmod +x /service/*.py

WORKDIR /service

CMD ["python3", "-u", "./dht_sensor.py"]
