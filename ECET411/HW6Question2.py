import RPi.GPIO as GPIO
import time

# Define GPIO pins
TRIG_PIN = 23
ECHO_PIN = 24
PIR_PIN = 17
LED_PIN = 18

# Initialize GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

# Function to measure distance using ultrasonic sensor
def measure_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return distance

try:
    while True:
        distance = measure_distance()
        # Adjust LED brightness based on distance
        brightness = max(0, min(100, (100 - distance)))
        duty_cycle = brightness / 100.0
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(duty_cycle / 10)  # 10 Hz frequency
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep((1 - duty_cycle) / 10)  # 10 Hz frequency

        # Check PIR sensor for motion
        if GPIO.input(PIR_PIN):
            GPIO.output(LED_PIN, GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()

