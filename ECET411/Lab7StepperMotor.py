import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)  # Ignore warning for now
step_pads = [19, 13, 6, 5]
GPIO.setmode(GPIO.BCM)

for i in range(4):
    GPIO.setup(step_pads[i], GPIO.OUT)

def motor_drive(number_steps, frequency, direction):
    speed = 1 / frequency

    if direction == 'R':
        for k in range(number_steps):
            for x in range(3, -1, -1):
                for j in range(3, -1, -1):
                    if x == j:
                        GPIO.output(step_pads[j], True)
                        print("Step Number = ", k)
                    else:
                        GPIO.output(step_pads[j], False)
                print("Reverse")
                time.sleep(speed)

    elif direction == 'F':
        for k in range(number_steps):
            for x in range(4):
                for j in range(4):
                    if x == j:
                        GPIO.output(step_pads[j], True)
                        print("Step Number = ", k)
                    else:
                        GPIO.output(step_pads[j], False)
                print("Forward")
                time.sleep(speed)

    else:
        print("WRONG DIRECTION ENTERED!")

while True:
    num_steps = int(input("Enter Number of Steps: "))
    freq = float(input("Enter Frequency: "))
    direction = input("Enter Direction: ")
    motor_drive(num_steps, freq, direction)
