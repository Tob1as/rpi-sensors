FROM arm32v7/python:3-alpine3.12

LABEL org.opencontainers.image.authors="Tobias Hargesheimer <docker@ison.ws>" \
	org.opencontainers.image.title="PI-Sensors" \
	org.opencontainers.image.description="AlpineLinux with Python 3 and Raspberry Pi GPIO Sensors" \
	org.opencontainers.image.licenses="Apache-2.0" \
	org.opencontainers.image.url="https://hub.docker.com/r/tobi312/rpi-sensors/" \
	org.opencontainers.image.source="https://github.com/Tob1as/rpi-sensors" \
	docker.build="docker build -t dht:latest -f testing.armhf.python.Dockerfile ." \
	docker.run="docker run --rm --name dht --device=/dev/gpiomem -e GPIO_PIN_DHT22=4 -e DHT22_SLEEPTIME=15 -d dht:latest" \
	docker.logs="docker logs -f dht"	

SHELL ["/bin/sh", "-euxo", "pipefail", "-c"]

#COPY dht_sensor.py /

RUN \
	wget https://raw.githubusercontent.com/Tob1as/rpi-sensors/master/dht_sensor.py -O /dht_sensor.py ; \
    apk add --no-cache \
        gcc libc-dev \
        libgpiod \
        mariadb-connector-c-dev \
    ; \
    pip3 install --no-cache-dir rpi.gpio; \
    pip3 install --no-cache-dir mariadb; \
###################
## Install with PIP
	#pip3 install --no-cache-dir adafruit-circuitpython-dht; \
## Install from git
	\
	apk add --no-cache --virtual .build-deps git ; \
	git clone https://github.com/adafruit/Adafruit_CircuitPython_DHT.git /usr/src/Adafruit_CircuitPython_DHT ; \
    cd /usr/src/Adafruit_CircuitPython_DHT ; \
	# fix trig_wait https://github.com/adafruit/Adafruit_CircuitPython_DHT/issues/49#issuecomment-786310338
	sed -i 's|self._trig_wait // 1000000|self._trig_wait / 1000000|' adafruit_dht.py ; \
	pip3 install --no-cache-dir -r requirements.txt --no-compile -e . ; \
	rm -r .git ; \
	apk del --no-network --purge .build-deps ; \
	cd / ; \
	\
###################
	chmod +x /dht_sensor.py
	

CMD ["python3", "-u", "./dht_sensor.py"]
