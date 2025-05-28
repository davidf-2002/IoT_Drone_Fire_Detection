# ~ import time
# ~ import adafruit_dht
# ~ import board

# ~ # Constants
# ~ TEMPERATURE_THRESHOLD = 45  # °C
# ~ CO_THRESHOLD = 500  # ppm (placeholder)

# ~ # Init DHT11 sensor (connected to GPIO17)
# ~ dht_device = adafruit_dht.DHT11(board.D4)

# ~ # Placeholder function for MQ-7 sensor reading
# ~ def get_co_level():
    # ~ # Replace with actual sensor reading logic
    # ~ # e.g., read from ADC like MCP3008
    # ~ return 50  # dummy value for now

# ~ # Decision fusion
# ~ def check_for_fire(temperature, humidity, co_level):
    # ~ fire_detected = False
    # ~ reason = ""

    # ~ if temperature > TEMPERATURE_THRESHOLD and co_level > CO_THRESHOLD:
        # ~ fire_detected = True
        # ~ reason = "High temperature and CO"
    # ~ elif temperature > TEMPERATURE_THRESHOLD:
        # ~ reason = "High temperature"
    # ~ elif co_level > CO_THRESHOLD:
        # ~ reason = "High CO level"

    # ~ return fire_detected, reason

# ~ # Main loop
# ~ try:
    # ~ while True:
        # ~ try:
            # ~ temperature_c = dht_device.temperature
            # ~ humidity = dht_device.humidity
            # ~ co_level = get_co_level()  # replace with real reading

            # ~ if temperature_c is not None and humidity is not None:
                # ~ print(f"Temp: {temperature_c:.1f}°C  Humidity: {humidity:.1f}%  CO Level: {co_level:.2f} ppm")

                # ~ fire_status, reason = check_for_fire(temperature_c, humidity, co_level)
                # ~ if fire_status:
                    # ~ print(f"Fire Detected! Reason: {reason}")
                # ~ else:
                    # ~ print("No fire detected.")

        # ~ except RuntimeError as err:
            # ~ print("Sensor read error:", err.args[0])

        # ~ time.sleep(2.0)

# ~ except KeyboardInterrupt:
    # ~ print("Monitoring stopped.")

import time
import adafruit_dht
import board

# Constants
TEMPERATURE_THRESHOLD = 55  # °C

# Init DHT11 sensor (connected to GPIO4)
dht_device = adafruit_dht.DHT11(board.D4)

# Decision logic
def check_for_fire(temperature, humidity):
    fire_detected = False
    reason = ""

    if temperature > TEMPERATURE_THRESHOLD:
        fire_detected = True
        reason = "High temperature"

    return fire_detected, reason

# Main loop
try:
    while True:
        try:
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity

            if temperature_c is not None and humidity is not None:
                print(f"Temp: {temperature_c:.1f}°C  Humidity: {humidity:.1f}%")

                fire_status, reason = check_for_fire(temperature_c, humidity)
                if fire_status:
                    print(f"Fire Detected! Reason: {reason}")
                else:
                    print("No fire detected.")

        except RuntimeError as err:
            print("Sensor read error:", err.args[0])

        time.sleep(2.0)

except KeyboardInterrupt:
    print("Monitoring stopped.")

finally:
    dht_device.exit()
