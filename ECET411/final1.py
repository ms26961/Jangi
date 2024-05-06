import tkinter as tk
import RPi.GPIO as GPIO
import time

# GPIO Pins for RGB LED
red_pin = 5
green_pin = 22
blue_pin = 27

# GPIO Pin for Buzzer
Buzzer_pin = 26

# GPIO to LCD mapping
LCD_RS = 21
LCD_E = 20
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

# Device constants
LCD_CHR = True  # Character mode
LCD_CMD = False  # Command mode
LCD_CHARS = 16  # Characters per line (16 max)
LCD_LINE_1 = 0x80  # LCD memory location for 1st line
LCD_LINE_2 = 0xC0  # LCD memory location 2nd line

# Function to initialize GPIO
def setup_gpio():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Buzzer_pin, GPIO.OUT)
        GPIO.setup(red_pin, GPIO.OUT)
        GPIO.setup(green_pin, GPIO.OUT)
        GPIO.setup(blue_pin, GPIO.OUT)

        # Setup LCD GPIO
        GPIO.setup(LCD_E, GPIO.OUT)
        GPIO.setup(LCD_RS, GPIO.OUT)
        GPIO.setup(LCD_D4, GPIO.OUT)
        GPIO.setup(LCD_D5, GPIO.OUT)
        GPIO.setup(LCD_D6, GPIO.OUT)
        GPIO.setup(LCD_D7, GPIO.OUT)
    except Exception as e:
        print("Error setting up GPIO:", e)

# Function to play sound
def play_sound(frequency):
    p = GPIO.PWM(Buzzer_pin, 100)
    p.start(50)
    p.ChangeFrequency(frequency)
    time.sleep(0.2)  # Adjust this to control the duration of the sound
    p.stop()

# Function to handle key presses
def key_pressed(note, frequency):
    output = "Key pressed: " + note
    print(output)
    lcd_text(output, LCD_LINE_1)
    lcd_text("Frequency: {:.2f}".format(frequency), LCD_LINE_2)
    play_sound(frequency)
    # Calculate color based on note
    color = calculate_color(note)
    # Set RGB LED color
    set_rgb_color(color)

# Define color mappings for notes
note_colors = {
    "C-": (255, 0, 0),    # Red
    "D": (255, 165, 0),   # Orange
    "E": (255, 255, 0),   # Yellow
    "F": (0, 255, 0),     # Green
    "G": (0, 0, 255),     # Blue
    "A": (128, 0, 128),   # Purple
    "B": (75, 0, 130),    # Indigo
    "C+": (255, 0, 0),    # Red (Second Octet)
    "D+": (255, 165, 0),  # Orange (Second Octet)
    "E+": (255, 255, 0),  # Yellow (Second Octet)
    "F+": (0, 255, 0),    # Green (Second Octet)
    "G+": (0, 0, 255),    # Blue (Second Octet)
    "A+": (128, 0, 128),  # Purple (Second Octet)
    "B+": (75, 0, 130),    # Indigo (Second Octet)
    "C++": (255, 0, 0)    # Red (Third Octet)
}

# Function to calculate color based on note
def calculate_color(note):
    # Return the color based on the note
    return note_colors.get(note, (255, 255, 255))  # Default to white if note is not found

# Function to set RGB LED color
def set_rgb_color(color):
    GPIO.output(red_pin, color[0])
    GPIO.output(green_pin, color[1])
    GPIO.output(blue_pin, color[2])

# Function to initialize LCD
def lcd_init():
    lcd_write(0x33, LCD_CMD) # Initialize
    lcd_write(0x32, LCD_CMD) # Set to 4-bit mode
    lcd_write(0x06, LCD_CMD) # Cursor move direction
    lcd_write(0x0C, LCD_CMD) # Turn cursor off
    lcd_write(0x28, LCD_CMD) # 2 line display
    lcd_write(0x01, LCD_CMD) # Clear display
    time.sleep(0.0005)     # Delay to allow commands to process

# Function to write to LCD
def lcd_write(bits, mode):
    GPIO.output(LCD_RS, mode) # RS

    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)

    # Toggle 'Enable' pin
    lcd_toggle_enable()

# Function to toggle Enable pin
def lcd_toggle_enable():
    time.sleep(0.0005)
    GPIO.output(LCD_E, True)
    time.sleep(0.0005)
    GPIO.output(LCD_E, False)
    time.sleep(0.0005)

# Function to write text to LCD
def lcd_text(message, line):
    # Send text to display
    message = message.ljust(LCD_CHARS, " ")

    lcd_write(line, LCD_CMD)

    for i in range(LCD_CHARS):
        lcd_write(ord(message[i]), LCD_CHR)

# CREATE THE WINDOW
root = tk.Tk()
root.title("Piano")

# Define notes and their frequencies for two octaves
notes = ["C-", "D", "E", "F", "G", "A", "B", "C", "D", "E", "F", "G", "A", "B", "C+"]
frequencies = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25, 555.28, 591.25, 610.85, 653.62, 701.62, 755.5, 784.87]

# Define White Keys
keys = []
for i, (note, freq) in enumerate(zip(notes, frequencies)):
    button = tk.Button(root, text=note, padx=20, pady=80, fg="black", bg="white",
                       command=lambda note=note, freq=freq: key_pressed(note, freq))
    button.grid(row=1, column=i * 2, columnspan=2)
    keys.append(button)

# Define Black Keys
black_keys = ["C#", "D#", "", "F#", "G#", "A#", "", "C#", "D#", "", "F#", "G#", "A#"]
for i, note in enumerate(black_keys):
    if note == "":
        continue  # Skip empty column
    button = tk.Button(root, text=note, padx=15, pady=40, fg="white", bg="black",
                       command=lambda note=note, freq=(frequencies[i] + 15): key_pressed(note, freq))
    # If the note is F# or G#, place it after the first black key, otherwise after A#
    if note in ("F#", "G#"):
        button.grid(row=0, column=2 * (i + 1), sticky="nsew")
    else:
        button.grid(row=0, column=2 * (i + 1) + 1, sticky="nsew")

# Setup GPIO
setup_gpio()

# Initialize LCD
lcd_init()

try:
    # Create an event loop
    root.mainloop()
finally:
    # Cleanup GPIO
    GPIO.cleanup()
