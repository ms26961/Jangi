import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from time import sleep  # Import the sleep function from the time module

GPIO.setwarnings(False)  # Ignore warning for now
GPIO.setmode(GPIO.BCM)  # Use physical pin numbering

BUZZER_PIN = 21
GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)  # Set pin 21 to be an output pin and set initial value to low (off)

try:
    while True:  # Run forever
        GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Turn on
        print('BUZZER ON')
        sleep(1)  # Sleep for 1 second

        GPIO.output(BUZZER_PIN, GPIO.LOW)  # Turn off
        print('BUZZER OFF')
        sleep(1)  # Sleep for 1 second

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
