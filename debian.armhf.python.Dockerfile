FROM arm32v7/python:3-slim-buster

LABEL org.opencontainers.image.authors="Tobias Hargesheimer <docker@ison.ws>" \
	org.opencontainers.image.title="PI-Sensors" \
	org.opencontainers.image.description="Debian 10 Buster (slim) with Python 3 and Raspberry Pi GPIO Sensors" \
	org.opencontainers.image.licenses="Apache-2.0" \
	org.opencontainers.image.url="https://hub.docker.com/r/tobi312/rpi-sensors/" \
	org.opencontainers.image.source="https://github.com/Tob1as/rpi-sensors"

COPY dht_sensor.py /

RUN set -ex; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        #build-essential \
        #python3-dev \
        #python3-openssl \
        gcc libc6-dev \
        libgpiod2 \
        libmariadb-dev \
    ; \
    rm -rf /var/lib/apt/lists/*; \
    pip3 install --no-cache-dir rpi.gpio; \
    pip3 install --no-cache-dir adafruit-circuitpython-dht==3.5.5; \
    pip3 install --no-cache-dir mariadb; \
    chmod +x /dht_sensor.py

CMD ["python3", "-u", "./dht_sensor.py"]
