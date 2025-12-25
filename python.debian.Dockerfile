FROM python:3.14-slim

ARG VCS_REF
ARG BUILD_DATE

LABEL org.opencontainers.image.authors="Tobias Hargesheimer <docker@ison.ws>" \
	org.opencontainers.image.title="PI-Sensors" \
	org.opencontainers.image.description="Raspberry Pi GPIO Sensors (Debian (slim) with Python 3)" \
	org.opencontainers.image.licenses="Apache-2.0" \
	org.opencontainers.image.created="${BUILD_DATE}" \
	org.opencontainers.image.revision="${VCS_REF}" \
	org.opencontainers.image.url="https://hub.docker.com/r/tobi312/rpi-sensors/" \
	org.opencontainers.image.source="https://github.com/Tob1as/rpi-sensors"

SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

#COPY *.py /service/
COPY dht_sensor.py /service/

RUN \
    #set -ex; \
    #mkdir /service ; \
    apt-get update; \
    BUILD_PACKAGES='gcc libc6-dev libmariadb-dev pkg-config'; \
    apt-get install -y --no-install-recommends \
        $BUILD_PACKAGES \
        libgpiod3 \
        libmariadb3 \
    ; \
    rm -rf /var/lib/apt/lists/*; \
    pip3 install --no-cache-dir rpi.gpio==0.7.1; \
    #pip3 install --no-cache-dir sysv-ipc==1.1.0; \
    pip3 install --no-cache-dir adafruit-blinka==8.68.1 ; \
    pip3 install --no-cache-dir adafruit-circuitpython-dht==4.0.10; \
    MARIADB_CONFIG=/usr/bin/mariadb_config \
    pip3 install --no-cache-dir mariadb==1.1.14; \
    pip3 install --no-cache-dir paho-mqtt==2.1.0; \
    apt-get remove --purge -y $BUILD_PACKAGES; apt autoremove -y ; \
    chmod +x /service/*.py

WORKDIR /service

STOPSIGNAL SIGINT

CMD ["python3", "-u", "./dht_sensor.py"]