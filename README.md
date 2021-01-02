# Raspberry Pi Sensors (rpi-sensors)

* temperature- and humidity sensor: DHT22 (AM2302) 

## Requirements

* Raspberry Pi or comatible board with GPIO
* Raspberry Pi OS (previously called Raspbian) (Version: 10 Buster) - here it is successfully tested
* Sensor: DHT22 (AM2302) (Buy: [int.](https://www.adafruit.com/product/393)/[de](https://www.rasppishop.de/Luftfeuchtigkeit-und-Temperatusensor-DHT22-AM2302))

## Installation / Usage

First Step:    
```sh
# Clone Project 
git clone https://github.com/Tob1as/rpi-sensors.git
# change in folder
cd rpi-sensors/
```

Secend Step:  
Use Docker (recommended) or manual installation.  

Note: It use PIN7 = GPIO4 (D4), if you want to change it, it must be done manually in `dht_sensor.py`. Possible solutions for set over env variable in python? `adafruit_dht.DHT22(board.D4)`

### Docker

Requirements:
* installed [Docker](https://docs.docker.com/engine/install/debian/)
* installed [Docker-Compose](https://docs.docker.com/compose/install/#install-using-pip)
* Note: Use my install [Script](https://github.com/Tob1asDocker/Collection/raw/master/Docker_on_Raspbian_10_Buster.sh) for that.

Steps:  
1. copy env-File:
    ```sh
    cp example.env .env
    ```
2. change settings in `.env`-File, example Database Password. Then optional check config:
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

### manual installation
  
(not complete)  
  
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

## This on

* [DockerHub](https://hub.docker.com/r/tobi312/rpi-sensors) for Container/Docker Image
* [GitHub](https://github.com/Tob1as/rpi-sensors) for Sourcecode and configuration
