import tkinter as tk
import RPi.GPIO as GPIO
import time

# GPIO Pins for RGB LED
red_pin = 5
green_pin = 22
blue_pin = 27

# GPIO Pin for Buzzer
Buzzer_pin = 26

# Function to initialize GPIO
def setup_gpio():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Buzzer_pin, GPIO.OUT)
        GPIO.setup(red_pin, GPIO.OUT)
        GPIO.setup(green_pin, GPIO.OUT)
        GPIO.setup(blue_pin, GPIO.OUT)
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
    print("Key pressed:", note)
    play_sound(frequency)
    # Calculate color based on frequency
    color = calculate_color(frequency)
    # Set RGB LED color
    set_rgb_color(color)

# Function to calculate color based on frequency
def calculate_color(frequency):
    # Normalize frequency to a value between 0 and 1
    normalized_freq = (frequency - min(frequencies)) / (max(frequencies) - min(frequencies))
    # Convert normalized frequency to a color value between 0 and 255
    color_value = int(normalized_freq * 255)
    # Return RGB color tuple (red, green, blue)
    return (255 - color_value, 0, color_value)  # Red component decreases, blue component increases

# Function to set RGB LED color
def set_rgb_color(color):
    GPIO.output(red_pin, color[0])
    GPIO.output(green_pin, color[1])
    GPIO.output(blue_pin, color[2])

# CREATE THE WINDOW
root = tk.Tk()
root.title("Piano")

# Define notes and their frequencies
notes = ["C-", "D", "E", "F", "G", "A", "B", "C+"]
frequencies = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]

# Define White Keys
keys = []
for i, (note, freq) in enumerate(zip(notes, frequencies)):
    button = tk.Button(root, text=note, padx=20, pady=80, fg="black", bg="white",
                       command=lambda note=note, freq=freq: key_pressed(note, freq))
    button.grid(row=1, column=i*2, columnspan=2)
    keys.append(button)

# Define Black Keys
black_keys = ["C#", "D#", "", "F#", "G#", "A#"]
for i, note in enumerate(black_keys):
    if note == "":
        continue  # Skip empty column
    button = tk.Button(root, text=note, padx=15, pady=40, fg="white", bg="black",
                       command=lambda note=note, freq=(frequencies[i]+15): key_pressed(note, freq))
    # If the note is F# or G#, place it after the first black key, otherwise after A#
    if note in ("F#", "G#"):
        button.grid(row=0, column=2*(i+1), sticky="nsew")
    else:
        button.grid(row=0, column=2*(i+1) + 1, sticky="nsew")

# Setup GPIO
setup_gpio()

try:
    # Create an event loop
    root.mainloop()
finally:
    # Cleanup GPIO
    GPIO.cleanup()
