import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)

while True:

        PIR_status = GPIO.input(PIR_PIN)
        if PIR_status == 1:
                print('Moved')
        sleep(.1)
