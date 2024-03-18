import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pir_sensor_pin = 23
GPIO.setup(pir_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    pir_status = GPIO.input(pir_sensor_pin)
    if pir_status:
        print('-> Moist')
    else:
        print('-> Dry')
    sleep(0.1)
