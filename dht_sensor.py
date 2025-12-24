#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Raspberry Pi Sensors (DHT22 / AM2302) 

https://github.com/Tob1as/rpi-sensors
"""

import os
import sys
import logging
import time
import board
import adafruit_dht
#from pulseio import PulseIn
import mariadb
import json
import paho.mqtt.client as mqtt
import ssl

# Variables
LOGLEVEL = str(os.environ.get('LOGLEVEL', 'INFO').upper())
DHT_DATA_PIN = int(os.environ.get('GPIO_PIN_DHT22', 4))
DHT_READ_TIMEOUT = float(os.environ.get('DHT22_SLEEPTIME', 15))
DHT_ID = int(os.environ.get('DHT22_ID', 1))
DB_HOST = str(os.environ.get('DB_HOST', 'localhost'))
DB_PORT = int(os.environ.get('DB_PORT', 3306))
DB_DATABASE = str(os.environ.get('DB_DATABASE', ''))
DB_USER = str(os.environ.get('DB_USER', ''))
DB_PASSWORD = str(os.environ.get('DB_PASSWORD', ''))
MQTT_HOST = str(os.environ.get('MQTT_HOST', ''))
MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))
#MQTT_SSL_ENABLED = bool(os.environ.get('MQTT_SSL_ENABLED', False))
MQTT_SSL_ENABLED = bool(eval(str(os.environ.get('MQTT_SSL_ENABLED', 'False')).title()))    # convert to boolean, because env are only str!
MQTT_USER = str(os.environ.get('MQTT_USER', ''))
MQTT_PASSWORD = str(os.environ.get('MQTT_PASSWORD', ''))
MQTT_CLIENT_ID = str(os.environ.get('MQTT_CLIENTNAME', f'sensor-{DHT_ID}'))
MQTT_TOPIC = str(os.environ.get('MQTT_TOPIC', 'sensors'))

# GPIO <https://www.raspberrypi.org/documentation/usage/gpio/>
# dictionary idea <https://github.com/adafruit/Adafruit_CircuitPython_DHT/issues/57>
boardspins = {'D0': board.D0, 
'D1': board.D1, 'D2': board.D2, 'D3': board.D3, 'D4': board.D4, 'D5': board.D5, 
'D6': board.D6, 'D7': board.D7, 'D8': board.D8, 'D9': board.D9, 'D10': board.D10, 
'D11': board.D11, 'D12': board.D12, 'D13': board.D13, 'D14': board.D14, 'D15': board.D15, 
'D16': board.D16, 'D17': board.D17, 'D18': board.D18, 'D19': board.D19, 'D20': board.D20, 
'D21': board.D21, 'D22': board.D22, 'D23': board.D23, 'D24': board.D24, 'D25': board.D25, 
'D26': board.D26, 'D27': board.D27}

# Logging
logging.root.handlers = []
logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8', stream=sys.stdout, level=LOGLEVEL)
logger = logging.getLogger(__name__)

# current time
def currenttime():
    t = time.localtime()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
    return current_time

def save_to_sql(measurement_time, temperature_f, temperature_c, humidity):
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_DATABASE,
            user=DB_USER,
            password=DB_PASSWORD
        )
    except mariadb.Error as e:
        logger.error(f"Error connecting to MariaDB Platform: {e}")
        #sys.exit(1)
    
    # Get Cursor
    cur = conn.cursor()

    #insert information 
    try: 
        cur.execute("INSERT INTO measurements (sensor_id,temperature_f,temperature,humidity) VALUES (?,?,?,?)", (DHT_ID,temperature_f,temperature_c,humidity))
        #cur.execute("INSERT INTO measurements (sensor_id,temperature_f,temperature,humidity,date_time) VALUES (?,?,?,?,?)", (DHT_ID,temperature_f,temperature_c,humidity,measurement_time))  
    except mariadb.Error as e: 
        logger.error(f"Error: {e}")
    
    conn.commit() 
    logger.debug(f"Database - Last Inserted ID: {cur.lastrowid}")
    
    conn.close()

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.debug("Connected to MQTT Broker!")
        else:
            logger.debug("Connect to MQTT Broker failed! result code: %d", rc)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, MQTT_CLIENT_ID)
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.on_connect = on_connect
    #client.on_message = on_message
    if MQTT_SSL_ENABLED == True:
        client.tls_set(ca_certs=None, cert_reqs=ssl.CERT_NONE) # for valid check: (ca_certs=/etc/ssl/certs/ca-certificates.crt, cert_reqs=ssl.CERT_REQUIRED)
        client.tls_insecure_set(True)                          # for valid check: False
    client.connect(MQTT_HOST, MQTT_PORT)
    return client

def get_JSON(measurement_time,temperature_f,temperature_c,humidity):
    jsonstring={
        'date': measurement_time,
        'sensor_id': DHT_ID,
        'temperature_f': temperature_f,
        'temperature_c': temperature_c,
        'humidity': humidity
    }
    jsondata = json.dumps(jsonstring)
    logger.debug("JSON:\n %s" % jsondata)
    return jsondata

def pub_to_mqtt(json_data):
    logger.debug("Will send Data to MQTT with Content from Date %s" % (json.loads(json_data)['date']))
    try:
        client = connect_mqtt()
        client.loop_start()
        client.publish(MQTT_TOPIC, payload='%s' % json_data , qos=0, retain=False)
        time.sleep(1)
        client.loop_stop()
        time.sleep(1)
        client.disconnect()
    except Exception as error:
        logger.error('%s' % error)


if __name__ == "__main__":
    logger.info("Sensor Service started!")
    logger.info("Set GPIO-Pin to D%s, SleepTime to %.0fs and ID to %s" % (DHT_DATA_PIN, DHT_READ_TIMEOUT, DHT_ID))
    logger.info("Database - set Host to \"%s\", Port to \"%s\", DB to \"%s\" and User to \"%s\"" % (DB_HOST, DB_PORT, DB_DATABASE, DB_USER))
    logger.info("MQTT - set Host to \"%s\", Port to \"%s\", Topic to \"%s\" and User to \"%s\" with Client-ID=%s and SSL=%s" % (MQTT_HOST, MQTT_PORT, MQTT_TOPIC, MQTT_USER, MQTT_CLIENT_ID, MQTT_SSL_ENABLED))

    pin = boardspins['D' + str(DHT_DATA_PIN)]

    # Initial the dht device, with data pin connected to:
    #dhtDevice = adafruit_dht.DHT22(board.D4)
    dhtDevice = adafruit_dht.DHT22(pin)

    # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
    # This may be necessary on a Linux single board computer like the Raspberry Pi,
    # but it will not work in CircuitPython.
    #dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    #dhtDevice = adafruit_dht.DHT22(pin, use_pulseio=False)

    try:
        while True:
            try:
                # Get values and print
                temperature_c = dhtDevice.temperature
                temperature_f = temperature_c * (9 / 5) + 32
                humidity = dhtDevice.humidity
                #logger.debug("Temp: {:.1f}F / {:.1f}°C ; Humidity: {}% ".format(temperature_f, temperature_c, humidity))

                temperature_c = float(round(temperature_c,1))
                temperature_f = float(round(temperature_f,1))
                humidity = float(round(humidity,1))
                logger.info("Measured Values: Temperature: %sF / %s°C ; Humidity: %s%%" % (temperature_f, temperature_c, humidity))

                measurement_time = currenttime()

                # Save the values to the Database
                if (DB_DATABASE !='' and DB_USER !='' and DB_PASSWORD !=''): 
                    save_to_sql(measurement_time, temperature_f, temperature_c, humidity)
                else: 
                    logger.debug("Data not save in Database!")

                # publish the values to MQTT
                if (MQTT_HOST !='' and MQTT_USER !='' and MQTT_PASSWORD !=''): 
                    json_data = get_JSON(measurement_time, temperature_f, temperature_c, humidity)
                    pub_to_mqtt(json_data)
                else: 
                    logger.debug("Data not publish to MQTT!")

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                logger.error(error.args[0])
                time.sleep(DHT_READ_TIMEOUT)
                continue
            except Exception as error:
                dhtDevice.exit()
                raise error

            time.sleep(DHT_READ_TIMEOUT)

    except KeyboardInterrupt:
        logger.debug('Keyboard interrupt')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
