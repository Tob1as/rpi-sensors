import os
#import sys
import time
import board
import adafruit_dht
import mariadb

# Variables
DHT_DATA_PIN = int(os.environ.get('GPIO_PIN_DHT22', 4))
DHT_READ_TIMEOUT = float(os.environ.get('DHT22_SLEEPTIME', 2))
DHT_ID = int(os.environ.get('DHT22_ID', 1))
print("Set GPIO-Pin to %s and SleepTime to %s and ID to %s" % (DHT_DATA_PIN, DHT_READ_TIMEOUT, DHT_ID))
DB_HOST = str(os.environ.get('DB_HOST', 'localhost'))
DB_PORT = int(os.environ.get('DB_PORT', 3306))
DB_DATABASE = str(os.environ.get('DB_DATABASE', ''))
DB_USER = str(os.environ.get('DB_USER', ''))
DB_PASSWORD = str(os.environ.get('DB_PASSWORD', ''))
print("Database - set Host to \"%s\", Port to \"%s\", DB to \"%s\" and User to \"%s\"" % (DB_HOST, DB_PORT, DB_DATABASE, DB_USER))

def save_to_sql(temperature_f, temperature_c, humidity):
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
        print(f"Error connecting to MariaDB Platform: {e}")
        #sys.exit(1)
    
    # Get Cursor
    cur = conn.cursor()

    #insert information 
    try: 
        cur.execute("INSERT INTO measurements (sensor_id,temperature_f,temperature,humidity) VALUES (?,?,?,?)", (DHT_ID,temperature_f,temperature_c,humidity)) 
    except mariadb.Error as e: 
        print(f"Error: {e}")
    
    conn.commit() 
    print(f"Database - Last Inserted ID: {cur.lastrowid}")
    
    conn.close()

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)
#dhtDevice = adafruit_dht.DHT22(DHT_DATA_PIN) # not working in docker container

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
#dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

while True:
    try:
        # Get values and print
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        #print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))
        
        temperature_c = float(round(temperature_c,1))
        temperature_f = float(round(temperature_f,1))
        humidity = float(round(humidity,1))
        print("Temp: %s F / %s C    Humidity: %s%%" % (temperature_f, temperature_c, humidity))
        
        # Save the values to the Database
        if (DB_DATABASE !='' and DB_USER !='' and DB_PASSWORD !=''): 
            save_to_sql(temperature_f, temperature_c, humidity)
        #else: 
        #    print("Database - settings missing.")
 
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(DHT_READ_TIMEOUT)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
 
    time.sleep(DHT_READ_TIMEOUT)
