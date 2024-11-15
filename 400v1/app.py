from flask import Flask, render_template, request, jsonify
import serial
import time
import random

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
        try:
            ldr_values = [int(value) for value in ldr_data.split(',')]
            if len(ldr_values) == 64:
                return ldr_values
        except ValueError:
            print("Error: Non-integer value received in LDR data")
    # Return dummy data if Arduino is not connected or data is invalid
    return [random.randint(0, 1023) for _ in range(64)]

# Function to generate a 32-character encryption key
def generate_encryption_key(ldr_values):
    key = ''
    for value in ldr_values:
        normalized_value = value % 62
        key += alphanumeric_chars[normalized_value]
    while len(key) < 32:  # Ensure key is 32 characters
        random_value = random.choice(ldr_values) % 62
        key += alphanumeric_chars[random_value]
    return key

# Self-test function to accumulate values over 10 seconds and return the highest value for each sensor
def run_self_test():
    start_time = time.time()  # Record the start time
    accumulated_values = [[] for _ in range(64)]  # Create a list of 64 empty lists to store values for each sensor

    while time.time() - start_time < 10:  # Run for 10 seconds
        ldr_values = get_ldr_values()
        for i in range(64):
            accumulated_values[i].append(ldr_values[i])

    # Calculate the highest value for each sensor
    results = []
    for i, values in enumerate(accumulated_values):
        if values:  # Ensure the list isn't empty
            max_value = max(values)  # Find the maximum value for the sensor
            status = "Pass" if 100 <= max_value <= 1000 else "Fail"  # Check if it passes the test criteria
            results.append({"Sensor ID": i + 1, "Max Value": max_value, "Status": status})
        else:
            results.append({"Sensor ID": i + 1, "Max Value": "No Data", "Status": "Fail"})

    return results

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
