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
print("Set GPIO-Pin to D%s and SleepTime to %s and ID to %s" % (DHT_DATA_PIN, DHT_READ_TIMEOUT, DHT_ID))
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

# GPIO <https://www.raspberrypi.org/documentation/usage/gpio/>
# dictionary idea <https://github.com/adafruit/Adafruit_CircuitPython_DHT/issues/57>
boardspins = {'D0': board.D0, 
'D1': board.D1, 'D2': board.D2, 'D3': board.D3, 'D4': board.D4, 'D5': board.D5, 
'D6': board.D6, 'D7': board.D7, 'D8': board.D8, 'D9': board.D9, 'D10': board.D10, 
'D11': board.D11, 'D12': board.D12, 'D13': board.D13, 'D14': board.D14, 'D15': board.D15, 
'D16': board.D16, 'D17': board.D17, 'D18': board.D18, 'D19': board.D19, 'D20': board.D20, 
'D21': board.D21, 'D22': board.D22, 'D23': board.D23, 'D24': board.D24, 'D25': board.D25, 
'D26': board.D26, 'D27': board.D27}

pin = boardspins['D' + str(DHT_DATA_PIN)]

# Initial the dht device, with data pin connected to:
#dhtDevice = adafruit_dht.DHT22(board.D4)
dhtDevice = adafruit_dht.DHT22(pin)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
#dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
#dhtDevice = adafruit_dht.DHT22(pin, use_pulseio=False)

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
