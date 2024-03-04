import RPi.GPIO as GPIO
import time

# Pin definitions
PB1_PIN = 17
PB2_PIN = 18
D1_PIN = 27

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PB1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PB2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(D1_PIN, GPIO.OUT)

# Initial duty cycle
duty_cycle = 1.0

# Function to toggle duty cycle
def toggle_duty_cycle():
    global duty_cycle
    duty_cycle -= 0.25
    if duty_cycle < 0.25:
        duty_cycle = 1.0

# Main loop
try:
    while True:
        if GPIO.input(PB1_PIN) == GPIO.LOW:
            toggle_duty_cycle()
            while GPIO.input(PB1_PIN) == GPIO.LOW:
                pass  # Wait for button release
            frequency = 100  # Frequency in Hz
            GPIO.output(D1_PIN, GPIO.HIGH)
            pwm = GPIO.PWM(D1_PIN, frequency)
            pwm.start(100 * duty_cycle)
            while GPIO.input(PB1_PIN) == GPIO.HIGH:
                if GPIO.input(PB2_PIN) == GPIO.LOW:
                    pwm.stop()
                    GPIO.output(D1_PIN, GPIO.LOW)
                    time.sleep(0.1)  # Debouncing delay
                    duty_cycle = 1.0  # Reset duty cycle
                    break
            pwm.stop()
            GPIO.output(D1_PIN, GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()
