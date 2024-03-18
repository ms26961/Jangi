import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
pwmPIN = 18
GPIO.setup(pwmPIN, GPIO.OUT)
pwm = GPIO.PWM(pwmPIN, 50) # GPIO 17 for PWM with 50Hz
pwm.start(0) # Initialization
while True:
  dutyCycle=float(input('Enter Duty Cycle: '))
  pwm.ChangeDutyCycle(dutyCycle)
  sleep(0.1)
