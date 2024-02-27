import RPi.GPIO as GPIO
from time import sleep

# Disable warnings (optional)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define button and LED pins
BUTTON_PIN = 23
LED_PIN = 24

# Setup button as input with pull-up resistor and LED as output
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

# Main loop
while True:
    button_state = GPIO.input(BUTTON_PIN)
    print(button_state)

    # Toggle LED based on button state
    GPIO.output(LED_PIN, not button_state)
    
    sleep(1)
