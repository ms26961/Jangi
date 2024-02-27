import RPi.GPIO as GPIO
from time import sleep

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the LED
LED_PIN = 21
GPIO.setup(LED_PIN, GPIO.OUT)

while True:
    num_blinks = int(input('Enter number of blinks: '))
    on_duration = float(input('Enter ON duration (seconds): '))
    off_duration = float(input('Enter OFF duration (seconds): '))
    
    for _ in range(num_blinks):
        GPIO.output(LED_PIN, GPIO.HIGH)
        print('LED ON')
        sleep(on_duration)
        
        GPIO.output(LED_PIN, GPIO.LOW)
        print('LED OFF')
        sleep(off_duration)
