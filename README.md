# Raspberry Pi Sensors (rpi-sensors)

## Description

This application measures temperature and humidity with a [DHT22/AM2302](https://learn.adafruit.com/dht) sensor connected to the Raspberry Pi.  
The sensor is read out with a Python script and the library [Adafruit_CircuitPython_DHT](https://github.com/adafruit/Adafruit_CircuitPython_DHT). The measurement data is displayed in the console and can optionally be save to a database (MariaDB) and displayed on a web server.

## Requirements

* Raspberry Pi
* Raspberry Pi OS (previously called Raspbian), Version: 10 buster / 11 bullseye
* Sensor: DHT22 (AM2302) (Buy: [int.](https://www.adafruit.com/product/393)/[de](https://www.rasppishop.de/Luftfeuchtigkeit-und-Temperatusensor-DHT22-AM2302))
* optional: Docker & docker-compose

## Installation / Usage

### Note: 
It use [physical PIN7 = GPIO4 (D4)](https://www.raspberrypi.com/documentation/computers/os.html#gpio-and-the-40-pin-header) by default. You can now[*](https://github.com/adafruit/Adafruit_CircuitPython_DHT/issues/57) change the GPIO Pin over a env-Variable (see below). 
The other two cable of `AM2302` are connect to 3V (or 5V) and Ground.

### First Step:    
```sh
# Clone Project 
git clone https://github.com/Tob1as/rpi-sensors.git
# change in folder
cd rpi-sensors/
```

### Secend Step:  
Use Docker (recommended) or manual installation.  

#### Docker

Requirements:
* installed [Docker](https://docs.docker.com/engine/install/debian/)
* installed [Docker-Compose](https://docs.docker.com/compose/install/#install-using-pip)
* Help? Use my install [Script](https://github.com/Tob1asDocker/Collection/raw/master/scripts/docker%2Bdocker-compose_install.sh) for that.
* Note: This was developed and tested on a Raspberry Pi 3. On 4 it run when you set `PRIVILEGED_MODE_ENABLE=true` in `.env`-File (see below).

Steps:  
1. copy env-File:
    ```sh
    cp example.env .env
    ```
2. change settings in `.env`-File, example Database Password or GPIO Pin. Then optional check config:
    ```sh
    docker-compose config
    ```
3. Run:
    ```sh
    docker-compose up -d
    ```
    or:
    ```sh
    docker-compose up -d mariadb dht22 web
    ```
4. [optional] Logs:
    ```sh
    docker-compose logs -f
    ```
5. [optional] Stop:
    ```sh
    docker-compose down -v
    ```

#### manual installation
  
1. Install requirements:
    ```sh
    sudo apt-get update
    sudo apt-get install -y build-essential python3-dev libgpiod2 libmariadb-dev
    sudo pip3 install adafruit-circuitpython-dht
    sudo pip3 install mariadb
    ```
2. Setup local or external MariaDB/MySQL.
3. Export Variable in `example.env`-File or change default value in `dht_sensor.py`.
4. Run:
    ```sh
    python3 ./dht_sensor.py
    ```
5. Optional: Copy html-Folder into Webserver with installed PHP-Modul and change database settings in php file.

### Troubleshooting

If your container (example: web) fails to start with Images that based on Alpine 3.13 on ARM devices like Raspberry with Raspbian Buster (32 bit) then see [here](https://github.com/Tob1asDocker/php#troubleshooting) or [here](https://github.com/Tob1asDocker/rpi-mariadb#troubleshooting) or [here](https://docs.linuxserver.io/faq#libseccomp) for a possible solution.

## This on

* [DockerHub](https://hub.docker.com/r/tobi312/rpi-sensors) for Container/Docker Image
* [GitHub](https://github.com/Tob1as/rpi-sensors) for Sourcecode and configuration
