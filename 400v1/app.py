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
ser = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)  # Wait for the serial connection to initialize

# Function to read LDR values from Arduino
def get_ldr_values():
    if ser.in_waiting > 0:
        ldr_data = ser.readline().decode('utf-8').strip()
        ldr_values = [int(value) for value in ldr_data.split(',')]
        return ldr_values
    else:
        return [random.randint(0, 1023) for _ in range(16)]  # Dummy data if no input

# Self-test function
def run_self_test():
    ldr_values = get_ldr_values()
    results = []
    for i, value in enumerate(ldr_values):
        status = "Pass" if 100 <= value <= 1000 else "Fail"
        results.append({"Sensor ID": i + 1, "Value": value, "Status": status})
    return results

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Route to perform LDR self-test and return JSON results
@app.route('/run_self_test', methods=['POST'])
def self_test():
    results = run_self_test()
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
