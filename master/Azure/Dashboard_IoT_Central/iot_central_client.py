import asyncio
import logging
import json
import random
from datetime import datetime

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
from Dashboard_IoT_Central import pnp_helper

logging.basicConfig(level=logging.ERROR)

# Device provisioning details 
DEVICE_ID = "RPiDroneFireLocator1"
DEVICE_ID_SCOPE = "0ne00EFDE3F"
DEVICE_KEY = "g8mBE/+JcTMIVxUPv3PIUdepVYu0GAOdr4kAO1/NRj0="
MODEL_ID = "dtmi:iotcentraldrone:IoTDrone_69o;1"

class IoTCentralClient:
    def __init__(self):
        self.device_client = None
        self.is_connected = False

    async def connect(self):
        """Connect to IoT Central"""
        try:
            provisioning_host = "global.azure-devices-provisioning.net"
            registration_result = await self._provision_device(
                provisioning_host, DEVICE_ID_SCOPE, DEVICE_ID, DEVICE_KEY, MODEL_ID
            )

            if registration_result.status != "assigned":
                raise RuntimeError("Could not provision device.")

            print("Device provisioned to hub:", registration_result.registration_state.assigned_hub)

            self.device_client = IoTHubDeviceClient.create_from_symmetric_key(
                symmetric_key=DEVICE_KEY,
                hostname=registration_result.registration_state.assigned_hub,
                device_id=registration_result.registration_state.device_id,
                product_info=MODEL_ID,
            )

            await self.device_client.connect()
            self.is_connected = True
            print("Connected to IoT Central successfully")
        except Exception as e:
            print(f"Error connecting to IoT Central: {str(e)}")
            raise

    async def _provision_device(self, provisioning_host, id_scope, registration_id, symmetric_key, model_id):
        """Provision the device to IoT Central"""
        provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
            provisioning_host=provisioning_host,
            registration_id=registration_id,
            id_scope=id_scope,
            symmetric_key=symmetric_key,
        )

        provisioning_device_client.provisioning_payload = {"modelId": model_id}
        return await provisioning_device_client.register()

    async def send_telemetry(self, telemetry_msg, component_name=None):
        """Send telemetry data to IoT Central"""
        if not self.is_connected:
            raise RuntimeError("Not connected to IoT Central")

        msg = pnp_helper.create_telemetry(telemetry_msg, component_name)
        await self.device_client.send_message(msg)
        print("Sent telemetry:", msg)

    async def send_location_telemetry(self, lat, lon, alt):
        """Send location telemetry to IoT Central"""
        telemetry_msg = {
            "deviceLocation": {
                "lat": lat,
                "lon": lon,
                "alt": alt
            }
        }
        await self.send_telemetry(telemetry_msg)

    async def shutdown(self):
        """Shutdown the IoT Central client"""
        if self.device_client:
            await self.device_client.shutdown()
            self.is_connected = False
            print("IoT Central client shutdown")

# Example usage:
"""
async def main():
    iot_client = IoTCentralClient()
    try:
        await iot_client.connect()
        
        # Send some test telemetry
        lat = round(random.uniform(51.4, 51.7), 6)
        lon = round(random.uniform(-0.2, 0.1), 6)
        alt = round(random.uniform(0, 100), 2)
        
        await iot_client.send_location_telemetry(lat, lon, alt)
        
    finally:
        await iot_client.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
"""
