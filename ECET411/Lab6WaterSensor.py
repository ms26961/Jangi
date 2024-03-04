 import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
PIR_PIN = 23
GPIO.setup(PIR_PIN, GPIO.IN,pull_up_down=GPIO.PUD_UP)

while True:

        PIR_status = GPIO.input(PIR_PIN)
        if PIR_status == 1:
                print('/////WET')
        else:
                print('//////////DRY')
        sleep(.1)
