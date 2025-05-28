import time
import adafruit_dht
import board

# Constants
TEMPERATURE_THRESHOLD = 30  # °C

# Init DHT11 sensor (connected to GPIO4)
# dht_device = adafruit_dht.DHT11(board.D4)

# Decision logic
def check_for_fire(temperature, humidity):
	fire_detected = False
	reason = ""

	if temperature > TEMPERATURE_THRESHOLD:
		fire_detected = True
		reason = "High temperature"

	return fire_detected, reason

# Main loop
def run_dht11_sensor():
	dht_device = adafruit_dht.DHT11(board.D4)
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
						return "fire", temperature_c, humidity
					else:
						print("No fire detected.")

			except RuntimeError as err:
				print("Sensor read error:", err.args[0])

			time.sleep(2.0)

	except KeyboardInterrupt:
		print("Monitoring stopped.")

	finally:
		# dht_device.exit()
		try:
			if hasattr(dht_device, "pulse_in"):
				dht_device.exit()
		except Exception as e:
			print("Cleanup error:", e)        


