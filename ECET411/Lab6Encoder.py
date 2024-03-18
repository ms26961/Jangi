import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

CLK_PIN = 18
DT_PIN = 24
SW_PIN = 23

GPIO.setup(CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

clk_prev_state = 0
encoder_count = 0

while True:
    clk_state = GPIO.input(CLK_PIN)
    dt_state = GPIO.input(DT_PIN)
    sw_state = GPIO.input(SW_PIN)
    
    if sw_state == 0:
        encoder_count = 0
        print('Resetting encoder count to 0')
        
    if clk_state != clk_prev_state:
        if clk_state == dt_state:
            encoder_count += 1
        else:
            encoder_count -= 1
        
        clk_prev_state = 1 if clk_prev_state == 0 else 0
                        
    print('Encoder pulses:', encoder_count)
    sleep(0.005)
