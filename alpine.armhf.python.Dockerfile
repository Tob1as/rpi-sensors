FROM arm32v7/python:3-alpine3.12

LABEL org.opencontainers.image.authors="Tobias Hargesheimer <docker@ison.ws>" \
	org.opencontainers.image.title="PI-Sensors" \
	org.opencontainers.image.description="AlpineLinux with Python 3 and Raspberry Pi GPIO Sensors" \
	org.opencontainers.image.licenses="Apache-2.0" \
	org.opencontainers.image.url="https://hub.docker.com/r/tobi312/rpi-sensors/" \
	org.opencontainers.image.source="https://github.com/Tob1as/rpi-sensors"

SHELL ["/bin/sh", "-euxo", "pipefail", "-c"]

COPY dht_sensor.py /

RUN \
    apk add --no-cache --virtual .build-deps \
        gcc libc-dev \
        mariadb-connector-c-dev \
    ; \
    apk add --no-cache \
        libgpiod \
        mariadb-connector-c \
    ; \
    pip3 install --no-cache-dir rpi.gpio; \
    pip3 install --no-cache-dir mariadb; \
    pip3 install --no-cache-dir adafruit-circuitpython-dht==3.5.5; \
    apk del --no-network --purge .build-deps; \
    chmod +x /dht_sensor.py

CMD ["python3", "-u", "./dht_sensor.py"]
