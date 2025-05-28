import RPi.GPIO as GPIO
import spidev
import time

# Pin definitions
DIGITAL_PIN = 26  # GPIO26 for digital CO detection
CO_DENSITY_THRESHOLD = -1  # Percentage (0–100%)

def read_mcp3008(channel):
    """Read from MCP3008 ADC (channel 0–7)"""
    if not 0 <= channel <= 7:
        raise ValueError("Invalid ADC Channel: must be between 0 and 7")

    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def run_mq7_sensor():
    global spi
    print("Initialising MQ-7 sensor...")

    # Setup SPI
    spi = spidev.SpiDev()
    spi.open(0, 0)  # SPI bus 0, device (CS) 0
    spi.max_speed_hz = 1350000

    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIGITAL_PIN, GPIO.IN)

    print("Please wait... warming up sensor.")
    time.sleep(20)

    try:
        while True:
            adc_value = read_mcp3008(0)
            voltage = (adc_value * 3.3) / 1023
            density = (adc_value / 1023.0) * 100  # Simplified CO %

            print(f"CO voltage = {voltage:.2f} V, CO density = {density:.2f} %")

            # Optional: You could use digital pin as an override or confirmation
            if density > CO_DENSITY_THRESHOLD:
                print("CO concentration above threshold!")
                return "unsafe", density
            else:
                print("CO concentration is safe.")
                return "safe", density

            time.sleep(2.0)

    except KeyboardInterrupt:
        print("MQ-7 monitoring interrupted.")

    # ~ finally:
        # ~ spi.close()
        # ~ GPIO.cleanup()
