from gpiozero import AngularServo
from time import sleep

# Create an AngularServo object with the specified GPIO pin,
# minimum pulse width, and maximum pulse width
servo = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)

try:
    while True:
        # Set the servo angle to 90 degrees
        servo.angle = 90
        sleep(1)

        # Set the servo angle to 0 degrees
        servo.angle = 0
        sleep(1)

        # Set the servo angle to -90 degrees
        servo.angle = -90
        sleep(1)

finally:
    # Move to neutral position and release the pin
    servo.angle = 0
    servo.close()

