import RPi.GPIO as GPIO
import time

def sweep_servo():
    # Set up GPIO
    servo_pin = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin, GPIO.OUT)

    # Set PWM frequency to 50Hz for servos
    pwm = GPIO.PWM(servo_pin, 50)
    pwm.start(0)

    def set_angle(angle):
        duty = angle / 18 + 2.5
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.03)  # Adjust for smoothness/speed

    try:
        while True:
            print("Sweeping 0° to 180°")
            for angle in range(0, 181):
                set_angle(angle)

            time.sleep(0.5)

            print("Sweeping 180° back to 0°")
            for angle in range(180, -1, -1):
                set_angle(angle)

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Stopped by user")

    finally:
        pwm.stop()
        GPIO.cleanup()
        print("GPIO cleaned up.")
