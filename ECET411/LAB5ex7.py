import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

BUTTON_PIN = 26
LED_PIN = 21

GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

pwm_led = GPIO.PWM(LED_PIN, 100)
pwm_led.start(0)

while True:
    button_state = GPIO.input(BUTTON_PIN)
    
    if button_state == 0:
        print("Button Pressed")
        for duty_cycle in [100, 75, 50, 25, 0]:
            pwm_led.ChangeDutyCycle(duty_cycle)
            print(f"Duty Cycle: {duty_cycle}%")
            sleep(1)
    
    elif button_state == 1:
        print("Button Released")
        GPIO.output(LED_PIN, False)
        print("LED OFF")
        sleep(1)
