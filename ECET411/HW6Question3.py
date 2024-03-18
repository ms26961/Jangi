import RPi.GPIO as GPIO
import time

# Define GPIO pins
ROTARY_DT = 5  # DT pin of rotary encoder
ROTARY_CLK = 6  # CLK pin of rotary encoder
WATER_SENSOR_PIN = 13  # Pin for water sensor
LED_PIN = 18  # Pin for LED

# Initialize GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(ROTARY_DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ROTARY_CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(WATER_SENSOR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

# Initialize variables
pulses_count = 0
brightness = 0

# Function to handle rotary encoder events
def rotary_callback(channel):
    global pulses_count
    global brightness

    if GPIO.input(ROTARY_DT) == GPIO.input(ROTARY_CLK):
        pulses_count += 1
    else:
        pulses_count -= 1

    # Ensure pulses count doesn't go below 0
    pulses_count = max(0, pulses_count)
    brightness = min(100, pulses_count * 10)  # Adjust brightness based on pulses count

# Add event detection for rotary encoder
GPIO.add_event_detect(ROTARY_DT, GPIO.BOTH, callback=rotary_callback)

try:
    while True:
        # Check water sensor for wetness
        if GPIO.input(WATER_SENSOR_PIN):
            GPIO.output(LED_PIN, GPIO.LOW)  # Turn off LED if water detected
        else:
            # Set LED brightness based on pulses count
            if pulses_count <= 0:
                GPIO.output(LED_PIN, GPIO.LOW)  # Turn off LED if pulses count is 0 or less
            else:
                duty_cycle = brightness / 100.0
                GPIO.output(LED_PIN, GPIO.HIGH)
                time.sleep(duty_cycle)

except KeyboardInterrupt:
    GPIO.cleanup()
