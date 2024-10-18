import serial
import time
import random

# Open the serial port to read the data from the Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust based on your setup
time.sleep(2)  # Wait for the connection to stabilize

# Define the alphanumeric characters (62 characters: 26 lowercase, 26 uppercase, 10 digits)
alphanumeric_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def generate_encryption_key(ldr_values):
    key = ''
    
    # Scale the LDR values and convert to alphanumeric characters
    for value in ldr_values:
        # Normalize the LDR value to the range 0-61 to match the index of alphanumeric_chars
        normalized_value = value % 62
        # Append the corresponding character from alphanumeric_chars
        key += alphanumeric_chars[normalized_value]
    
    # Repeat the process until the key has 32 characters
    while len(key) < 32:
        # Randomly pick more values from the existing LDR data
        random_value = random.choice(ldr_values) % 62
        key += alphanumeric_chars[random_value]
    
    return key

# Main loop to receive data and generate encryption keys
while True:
    if ser.in_waiting > 0:
        # Read the comma-separated LDR values from Arduino
        ldr_data = ser.readline().decode('utf-8').strip()
        ldr_values = [int(value) for value in ldr_data.split(',')]
        
        # Generate a 32-character alphanumeric key
        encryption_key = generate_encryption_key(ldr_values)
        print(f"Generated Encryption Key: {encryption_key}")
        
        # Optional: Save or process the key as needed
        
    time.sleep(0.1)  # Small delay to avoid overwhelming the serial buffer
