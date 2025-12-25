FROM python:3.14-alpine

ARG VCS_REF
ARG BUILD_DATE

LABEL org.opencontainers.image.authors="Tobias Hargesheimer <docker@ison.ws>" \
	org.opencontainers.image.title="PI-Sensors" \
	org.opencontainers.image.description="Raspberry Pi GPIO Sensors (AlpineLinux with Python 3)" \
	org.opencontainers.image.licenses="Apache-2.0" \
	org.opencontainers.image.created="${BUILD_DATE}" \
	org.opencontainers.image.revision="${VCS_REF}" \
	org.opencontainers.image.url="https://hub.docker.com/r/tobi312/rpi-sensors/" \
	org.opencontainers.image.source="https://github.com/Tob1as/rpi-sensors" \
	docker.build="docker build --pull -t local/dht:latest -f alpine.armhf.python_dht_git.Dockerfile ." \
	docker.run="docker run --rm --name dht --device=/dev/gpiomem -e GPIO_PIN_DHT22=4 -e DHT22_SLEEPTIME=15 -d local/dht:latest" \
	docker.logs="docker logs -f dht"	

SHELL ["/bin/sh", "-euxo", "pipefail", "-c"]

#COPY *.py /service/
COPY dht_sensor.py /service/

RUN \
    #mkdir /service ; \
    #wget https://raw.githubusercontent.com/Tob1as/rpi-sensors/master/dht_sensor.py -O /service/dht_sensor.py ; \
    apk add --no-cache --virtual .build-deps \
        gcc libc-dev \
        mariadb-connector-c-dev \
        git \
    ; \
    apk add --no-cache \
        libgpiod \
        mariadb-connector-c \
    ; \
    pip3 install --no-cache-dir rpi.gpio; \
    #pip3 install --no-cache-dir sysv-ipc; \
    pip3 install --no-cache-dir mariadb; \
    pip3 install --no-cache-dir paho-mqtt; \
###################
## Install with PIP
    #pip3 install --no-cache-dir adafruit-circuitpython-dht; \
## Install from git
    \
    git clone https://github.com/adafruit/Adafruit_CircuitPython_DHT.git /usr/src/Adafruit_CircuitPython_DHT ; \
    cd /usr/src/Adafruit_CircuitPython_DHT ; \
    pip3 install --no-cache-dir -r requirements.txt --no-compile -e . ; \
    rm -r .git ; \
    cd / ; \
    \
###################
    apk del --no-network --purge .build-deps ; \
    chmod +x /service/*.py

WORKDIR /service

STOPSIGNAL SIGINT

CMD ["python3", "-u", "./dht_sensor.py"]