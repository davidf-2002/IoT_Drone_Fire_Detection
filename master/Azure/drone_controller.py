import asyncio
import logging
import random
import sys
import os
from dronekit import connect
import time
from datetime import datetime
from Fire_Identification_Azure_CV.drone_fire_detection import FireDetection
from Dashboard_IoT_Central.iot_central_client import IoTCentralClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DroneController:
	def __init__(self):
		# Initialize fire detection and IoT client
		self.fire_detection = FireDetection()
		self.iot_client = IoTCentralClient()
		self.is_running = False
		
		# Initialize vehicle connection at the start
		self.vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=57600)  # Or use 'udp:127.0.0.1:14550'
		logger.info("Drone connection established.")

	async def initialize(self):
		"""Initialize all components"""
		try:
			# Initialize camera
			self.fire_detection.initialize_camera()
			
			# Initialize IoT Central
			await self.iot_client.connect()
			
			logger.info("All components initialized successfully")
		except Exception as e:
			logger.error(f"Failed to initialize components: {str(e)}")
			raise

	def get_gps_location(self):
		"""Get the current GPS location from the drone using mavlink with a timeout"""
		try:
			logger.info("Getting drone location... ")
			timeout = time.time() + 10  # Set timeout to 10 seconds
			# Wait until we have a valid location or timeout
			while time.time() < timeout:
				if self.vehicle.location.global_frame.lat:  # Check if location is valid
					lat = self.vehicle.location.global_frame.lat
					lon = self.vehicle.location.global_frame.lon
					alt = self.vehicle.location.global_frame.alt
					logger.debug(f"GPS Location: Latitude={lat}, Longitude={lon}, Altitude={alt}")
					return {
						"latitude": lat,
						"longitude": lon,
						"altitude": alt
					}
				time.sleep(0.5)  # Wait before checking again
			
			# If timeout is reached without valid location, return None values
			logger.error("Timeout reached while waiting for GPS location.")
			return {"latitude": None, "longitude": None, "altitude": None}

		except Exception as e:
			logger.error(f"Error getting GPS location: {str(e)}")
			return {"latitude": None, "longitude": None, "altitude": None}

	async def confirm_fire(self, co_level, temperature, humidity):
		"""Checks for fire and sends telemetry to IoT Central"""
		try:
			# Get current location
			location_data = self.get_gps_location()
			
			# Check for fire
			fire_detection_data = self.fire_detection.process_capture()
			
			if fire_detection_data['detected']:
				logger.info(f"Fire confirmed by visual detection! Confidence: {fire_detection_data['confidence']*100:.2f}%")
				
				# Send telemetry to IoT Central
				await self.iot_client.send_telemetry({
					"deviceLocation": {
						"lat": location_data['latitude'],
						"lon": location_data['longitude'],
						"alt": location_data['altitude']
					},
					"fireConfidence": fire_detection_data['confidence'],
					"fireDetected": fire_detection_data['detected'],
					"coLevel": co_level,
					"temperature": temperature,
					"humidity": humidity,
					"detectionTimestamp": datetime.utcnow().isoformat()
				})
				return True
			else:
				logger.info("No fire detected visually")
				return False
		except Exception as e:
			logger.error(f"Error confirming fire: {str(e)}")
			return False

	async def shutdown(self):
		"""Clean up all resources"""
		try:
			self.fire_detection.shutdown()
			await self.iot_client.shutdown()
			
			# Close the vehicle connection when done
			self.vehicle.close()
			
			logger.info("All components shut down successfully")
		except Exception as e:
			logger.error(f"Error during shutdown: {str(e)}")


# Example usage:

async def main():
	controller = DroneController()
	try:
		await controller.initialize()
		
		# Example sensor data
		co_level = round(random.uniform(50, 200), 1) # ppm
		temperature = round(random.uniform(40, 100), 1)  # Celsius
		humidity = round(random.uniform(0, 40), 1) # %
		
		# Process sensor data
		fire_detected = await controller.confirm_fire(co_level, temperature, humidity)
		print(f"Fire detected: {fire_detected}")
		
	finally:
		await controller.shutdown()

if __name__ == "__main__":
	asyncio.run(main())
