import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

SENSOR_PIN = 4
GPIO.setup(SENSOR_PIN, GPIO.IN)

while True:
    sensor_status = GPIO.input(SENSOR_PIN)
    
    if sensor_status == 1:
        print('Motion detected')
    
    sleep(0.1)
