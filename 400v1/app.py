from flask import Flask, render_template, request, send_file, jsonify
import serial
import time
import random
import pandas as pd
from fpdf import FPDF

app = Flask(__name__)

# Alphanumeric character set for encryption keys
alphanumeric_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# Serial port setup for Arduino
try:
    ser = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(2)  # Wait for the serial connection to initialize
except serial.SerialException:
    ser = None  # Handle the case where the Arduino is not connected

# Function to read LDR values from Arduino
def get_ldr_values():
    if ser and ser.in_waiting > 0:
        ldr_data = ser.readline().decode('utf-8').strip()
        ldr_values = [int(value) for value in ldr_data.split(',')]
        return ldr_values
    else:
        return [random.randint(0, 1023) for _ in range(16)]  # Dummy data if no input

# Function to generate a 32-character encryption key
def generate_encryption_key(ldr_values):
    key = ''
    for value in ldr_values:
        # Normalize LDR values to match alphanumeric character index
        normalized_value = value % 62
        key += alphanumeric_chars[normalized_value]
    
    while len(key) < 32:  # Ensure key is 32 characters
        random_value = random.choice(ldr_values) % 62
        key += alphanumeric_chars[random_value]
    return key

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for key generation
@app.route('/generate', methods=['POST'])
def generate_keys():
    try:
        # Get the number of keys from the form
        num_keys = int(request.form['num_keys'])
        keys = []

        # Generate the requested number of keys
        for _ in range(num_keys):
            ldr_values = get_ldr_values()
            key = generate_encryption_key(ldr_values)
            keys.append(key)

        # Render the key.html page with generated keys
        return render_template('key.html', num_keys=num_keys, keys=keys)
    except Exception as e:
        return f"Error generating keys: {e}", 500

# Route to perform LDR self-test and return JSON results
@app.route('/run_self_test', methods=['POST'])
def self_test():
    results = run_self_test()
    return jsonify(results)

# Function to perform self-test on LDR values
def run_self_test():
    ldr_values = get_ldr_values()
    results = []
    for i, value in enumerate(ldr_values):
        status = "Pass" if 100 <= value <= 1000 else "Fail"
        results.append({"Sensor ID": i + 1, "Value": value, "Status": status})
    return results

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
