import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)  # Ignore warning for now
stepPads = [19, 13, 6, 5]
GPIO.setmode(GPIO.BCM)

for i in range(0, 4):
    GPIO.setup(stepPads[i], GPIO.OUT)

def motorDrive(numberSteps, Frequency, Direction):
    speed = float(1 / Frequency)
    if Direction == 'R':
        for k in range(0, numberSteps):
            for x in range(3, -1, -1):
                for j in range(3, -1, -1):
                    if x == j:
                        GPIO.output(stepPads[j], True)
                        print("Step Number = ", k)
                    else:
                        GPIO.output(stepPads[j], False)
                        print("Reverse")
                time.sleep(speed)
    elif Direction == 'F':
        for k in range(0, numberSteps):
            for x in range(0, 4, 1):
                for j in range(0, 4, 1):
                    if x == j:
                        GPIO.output(stepPads[j], True)
                        print("Step Number = ", k)
                    else:
                        GPIO.output(stepPads[j], False)
                        print("Forward")
                time.sleep(speed)
    else:
        print("WRONG DIRECTION ENTERED!")

while True:
    numSteps = int(input("Enter Number of Steps: "))
    Freq = float(input("Enter Frequency: "))
    Dir = input("Enter Direction: ")
    motorDrive(numSteps, Freq, Dir)
