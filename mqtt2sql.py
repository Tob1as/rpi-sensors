#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Raspberry Pi Sensors (DHT22 / AM2302) 

Subscribe MQTT, get Sensors measurement data and save to SQL Database!

https://github.com/Tob1as/rpi-sensors
"""

import sys
import os
import logging
import time
import mariadb
import json
import paho.mqtt.client as mqtt
import ssl

# Variables
LOGLEVEL = str(os.environ.get('LOGLEVEL', 'INFO').upper())
DB_HOST = str(os.environ.get('DB_HOST', 'localhost'))
DB_PORT = int(os.environ.get('DB_PORT', 3306))
DB_DATABASE = str(os.environ.get('DB_DATABASE', ''))
DB_USER = str(os.environ.get('DB_USER', ''))
DB_PASSWORD = str(os.environ.get('DB_PASSWORD', ''))
MQTT_HOST = str(os.environ.get('MQTT_HOST', 'vernemq'))
MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))
MQTT_SSL_ENABLED = bool(os.environ.get('MQTT_SSL_ENABLED', False))
MQTT_USER = str(os.environ.get('MQTT_USER', ''))
MQTT_PASSWORD = str(os.environ.get('MQTT_PASSWORD', ''))
MQTT_CLIENT_ID = str(os.environ.get('MQTT_CLIENTNAME', f'sensor-mqtt2sql'))
MQTT_TOPIC = str(os.environ.get('MQTT_TOPIC', 'sensors'))

# Logging
logging.root.handlers = []
logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8', stream=sys.stdout, level=LOGLEVEL)
logger = logging.getLogger(__name__) 

# current time
def currenttime():
    t = time.localtime()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
    return current_time

def save_to_sql(sensor_id, temperature_f, temperature_c, humidity, date_time):
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
        #cur.execute("INSERT INTO measurements (sensor_id,temperature_f,temperature,humidity) VALUES (?,?,?,?)", (sensor_id,temperature_f,temperature_c,humidity)) 
        cur.execute("INSERT INTO measurements (sensor_id,temperature_f,temperature,humidity,date_time) VALUES (?,?,?,?,?)", (sensor_id,temperature_f,temperature_c,humidity,date_time))
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
    #def on_message(client, userdata, message):
    #    logger.debug("Message Recieved: "+message.payload.decode())
    client = mqtt.Client(MQTT_CLIENT_ID)
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.on_connect = on_connect
    if MQTT_SSL_ENABLED == True:
        client.tls_set(ca_certs=None, cert_reqs=ssl.CERT_NONE) # for valid check: (ca_certs=/etc/ssl/certs/ca-certificates.crt, cert_reqs=ssl.CERT_REQUIRED)
        client.tls_insecure_set(True)                          # for valid check: False
    client.connect(MQTT_HOST, MQTT_PORT)
    return client

def on_message(client, userdata, message):
    msg = message.payload.decode()
    logger.debug("Received message '" + str(msg) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))
    msg_values = json.loads(msg)
    sensor_id = msg_values['sensor_id']
    temperature_f = msg_values['temperature_f']
    temperature_c = msg_values['temperature_c']
    humidity = msg_values['humidity']
    date_time = msg_values['date']
    logger.info("Data: SensorID=%s ; Temperature %sF / %s°C ; Humidity: %s%% ; Datetime='%s'" % (sensor_id, temperature_f, temperature_c, humidity, date_time))
    # Save the values to the Database
    if (DB_DATABASE !='' and DB_USER !='' and DB_PASSWORD !=''): 
        save_to_sql(sensor_id, temperature_f, temperature_c, humidity, date_time)
    else: 
        logger.debug("Data not save in Database!")

if __name__ == "__main__":
    logger.info("Sensor Service started!")
    logger.info("Database - set Host to \"%s\", Port to \"%s\", DB to \"%s\" and User to \"%s\"" % (DB_HOST, DB_PORT, DB_DATABASE, DB_USER))
    logger.info("MQTT - set Host to \"%s\", Port to \"%s\", Topic to \"%s\" and User to \"%s\" with Client-ID=%s and SSL=%s" % (MQTT_HOST, MQTT_PORT, MQTT_TOPIC, MQTT_USER, MQTT_CLIENT_ID, MQTT_SSL_ENABLED))
                                                                                    
    try:
        try:
            client = connect_mqtt()
            client.on_message = on_message
            client.subscribe(MQTT_TOPIC, qos=0)
            client.loop_forever()
        except Exception as error:
            logger.error('%s' % error)
    except KeyboardInterrupt:
        logger.info('KeyboardInterrupt')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
