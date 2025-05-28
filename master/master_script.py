import threading

import asyncio
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Azure')))

from dht11_temp_humid.dht11_final import run_dht11_sensor
from mq7_gas.mq_7_final import run_mq7_sensor
from motor.motor import sweep_servo
from Azure.drone_controller import DroneController

async def main():
	# Start servo in background
	# servo_thread = threading.Thread(target=sweep_servo, daemon=True)
	# servo_thread.start()

	# Initialise drone controller
	controller = DroneController()
	await controller.initialize()
	
	try:
		while True:
			print("Starting DHT11 monitoring...")
			status, temp, humid = run_dht11_sensor()

			if status == "fire":
				print("High Temperature Detected!")
				print("Switching to MQ7 gas monitoring...")
				gas_status, co = run_mq7_sensor()

				if gas_status == "unsafe":
					print("Air is unsafe!")
					print("Starting fire prediction through Azure CV... ")
					fire_confirmed = await controller.confirm_fire(co_level=co, temperature=temp, humidity=humid)

					print(f"Fire confirmation result: {fire_confirmed}")
				else:
					print("Air is safe. Returning to temperature monitoring.")				

	except KeyboardInterrupt:
		print("Program interrupted by user.")
	finally:
		await controller.shutdown()				
				

if __name__ == "__main__":
	asyncio.run(main())
	
