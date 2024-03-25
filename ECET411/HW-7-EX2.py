import RPi.GPIO as GPIO
import time

# Pin Definitions
BUTTON_PIN = 17  # Pin for the button (PB1)
BUZZER_PIN = 18  # Pin for the buzzer
SERVO_PIN = 14   # Pin for the servo motor

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Create PWM instance for servo
servo_pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz frequency

# Function to control servo
def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(SERVO_PIN, True)
    servo_pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(SERVO_PIN, False)
    servo_pwm.ChangeDutyCycle(0)

# Function to emit beeps
def emit_beeps(count):
    for _ in range(count):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(1)

# Main function
def main():
    prev_button_state = GPIO.input(BUTTON_PIN)
    button_press_count = 0

    while True:
        curr_button_state = GPIO.input(BUTTON_PIN)

        if curr_button_state != prev_button_state and curr_button_state == GPIO.LOW:
            button_press_count += 1
            if button_press_count == 1:
                set_angle(0)  # Move to 0 degree position
                emit_beeps(1)
            elif button_press_count == 2:
                set_angle(90)  # Move to 90 degree position
                emit_beeps(2)
            elif button_press_count == 3:
                set_angle(180)  # Move to 180 degree position
                emit_beeps(3)
            elif button_press_count == 4:
                button_press_count = 0  # Reset count

        prev_button_state = curr_button_state

if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()
