#encoder
import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
CLK = 18
DT = 24
SW = 23
GPIO.setup(CLK, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN,pull_up_down=GPIO.PUD_UP)
clk_prev = 0
encode_count = 0
while True:
        clk_status = GPIO.input(CLK)
        dt_status = GPIO.input(DT)
        sw_status = GPIO.input(SW)
        if sw_status == 0:
                encode_count = 0
                print('encode_count = ', encode_count)

        if clk_status !=clk_prev:
                if clk_status == dt_status:
                        encode_count  = encode_count  + 1
                else:
                         encode_count  = encode_count - 1
                if clk_prev == 1:
                        clk_prev = 0
                else:
                        clk_prev  = 1
        print('Encoder pulses = ', encode_count)
