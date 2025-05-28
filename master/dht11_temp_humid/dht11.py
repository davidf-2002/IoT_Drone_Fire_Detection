import time
import adafruit_dht
import board

dht_device = adafruit_dht.DHT11(board.D17)

while True:
    try:
        temperature_c = dht_device.temperature
        temperature_f = temperature_c * (9 / 5) + 32

        humidity = dht_device.humidity

        print("Temp:{:.1f} C / {:.1f} F    Humidity: {}%".format(temperature_c, temperature_f, humidity))
    except RuntimeError as err:
        print(err.args[0])

    time.sleep(2.0)

# Complete Project Details: https://RandomNerdTutorials.com/raspberry-pi-dht11-dht22-python/
# Based on Adafruit_CircuitPython_DHT Library Example

# ~ import time
# ~ import board
# ~ import adafruit_dht

# ~ # Sensor data pin is connected to GPIO 4
# ~ sensor = adafruit_dht.DHT22(board.D4)
# ~ # Uncomment for DHT11
# ~ #sensor = adafruit_dht.DHT11(board.D4)

# ~ while True:
    # ~ try:
        # ~ # Print the values to the serial port
        # ~ temperature_c = sensor.temperature
        # ~ temperature_f = temperature_c * (9 / 5) + 32
        # ~ humidity = sensor.humidity
        # ~ print("Temp={0:0.1f}ºC, Temp={1:0.1f}ºF, Humidity={2:0.1f}%".format(temperature_c, temperature_f, humidity))

    # ~ except RuntimeError as error:
        # ~ # Errors happen fairly often, DHT's are hard to read, just keep going
        # ~ print(error.args[0])
        # ~ time.sleep(2.0)
        # ~ continue
    # ~ except Exception as error:
        # ~ sensor.exit()
        # ~ raise error

    # ~ time.sleep(3.0)
