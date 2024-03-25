import RPi.GPIO as GPIO
import time

# Pin Definitions
BUTTON_FORWARD_PIN = 17  # Pin for forward direction button (PB1)
BUTTON_REVERSE_PIN = 18  # Pin for reverse direction button (PB2)
BUTTON_STOP_PIN = 27     # Pin for stop button (PB3)
LED_FORWARD_PIN = 22     # Pin for LED1 (Forward Direction)
LED_REVERSE_PIN = 23     # Pin for LED2 (Reverse Direction)
LED_STOP_PIN = 24        # Pin for LED3 (Stop)
STEPPER_PINS = [5, 6, 13, 19]  # Pins for the stepper motor (GPIO pins connected to stepper driver)

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_FORWARD_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_REVERSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_STOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_FORWARD_PIN, GPIO.OUT)
GPIO.setup(LED_REVERSE_PIN, GPIO.OUT)
GPIO.setup(LED_STOP_PIN, GPIO.OUT)
for pin in STEPPER_PINS:
    GPIO.setup(pin, GPIO.OUT)

# Sequence for stepper motor rotation (can be adjusted based on stepper motor type)
STEPPER_SEQUENCE = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
]

# Function to rotate stepper motor in forward direction
def rotate_forward():
    for i in range(512):  # Adjust steps as needed
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(STEPPER_PINS[pin], STEPPER_SEQUENCE[halfstep][pin])
            time.sleep(0.001)

# Function to rotate stepper motor in reverse direction
def rotate_reverse():
    for i in range(512):  # Adjust steps as needed
        for halfstep in reversed(range(8)):
            for pin in range(4):
                GPIO.output(STEPPER_PINS[pin], STEPPER_SEQUENCE[halfstep][pin])
            time.sleep(0.001)

# Main function
def main():
    while True:
        forward_button_state = GPIO.input(BUTTON_FORWARD_PIN)
        reverse_button_state = GPIO.input(BUTTON_REVERSE_PIN)
        stop_button_state = GPIO.input(BUTTON_STOP_PIN)

        if forward_button_state == GPIO.LOW:
            rotate_forward()
            GPIO.output(LED_FORWARD_PIN, GPIO.HIGH)
            GPIO.output(LED_REVERSE_PIN, GPIO.LOW)
            GPIO.output(LED_STOP_PIN, GPIO.LOW)

        elif reverse_button_state == GPIO.LOW:
            rotate_reverse()
            GPIO.output(LED_FORWARD_PIN, GPIO.LOW)
            GPIO.output(LED_REVERSE_PIN, GPIO.HIGH)
            GPIO.output(LED_STOP_PIN, GPIO.LOW)

        elif stop_button_state == GPIO.LOW:
            GPIO.output(LED_FORWARD_PIN, GPIO.LOW)
            GPIO.output(LED_REVERSE_PIN, GPIO.LOW)
            GPIO.output(LED_STOP_PIN, GPIO.HIGH)

if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()
