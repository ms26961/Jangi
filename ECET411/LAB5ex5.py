import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
LED = 21
GPIO.setup(LED, GPIO.OUT)
while True:
    numBlinks = int(input('Enter Number of Blinks: '))
    delayOn = float(input('Enter DelayOn: '))
    delayOff = float(input('Enter DelayOff: '))
    for i in range(0, numBlinks, 1):
        GPIO.output(LED, GPIO.HIGH)
        print('LED ON')
        sleep(delayOn)
        GPIO.output(LED, GPIO.LOW)
        print('LED OFF')
        sleep(delayOff)