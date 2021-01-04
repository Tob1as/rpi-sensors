## Development Info/Help

* GPIO: https://www.raspberrypi.org/documentation/usage/gpio/
* DHT22 (AM2302) - temperature- and humidity sensor:
    * Shop (de): https://www.rasppishop.de/Luftfeuchtigkeit-und-Temperatusensor-DHT22-AM2302
    * Shop (int.): https://www.adafruit.com/product/393
    * Info: https://learn.adafruit.com/dht
    * Python Libary: https://learn.adafruit.com/dht/dht-circuitpython-code + https://github.com/adafruit/Adafruit_CircuitPython_DHT
    * Go Libary: https://github.com/d2r2/go-dht + https://github.com/MichaelS11/go-dht (https://www.jeremymorgan.com/tutorials/go/get-temperature-raspberry-pi-go/)
* Docs/Examples:
    * https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup
    * https://tutorials-raspberrypi.de/raspberry-pi-luftfeuchtigkeit-temperatur-messen-dht11-dht22/
    * https://buyzero.de/blogs/news/tutorial-dht22-dht11-und-am2302-temperatursensor-feuchtigkeitsensor-am-raspberry-pi-anschliessen-und-ansteuern
    * https://www.laub-home.de/wiki/Raspberry_Pi_DHT22_Temperatur_Sensor#Adafruit_DHT_Python_Libraries
    * https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
    * https://stackoverflow.com/a/4907053 - Python env variable
* GPIO in Docker:  https://blog.alexellis.io/gpio-on-swarm/ (`--device /dev/gpiomem`). Only work as root in container?...
