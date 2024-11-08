from flask import Flask, render_template, request, send_file
import serial
import time
import random
import pandas as pd
from fpdf import FPDF

# Flask App Setup
app = Flask(__name__)

# Alphanumeric character set for encryption keys
alphanumeric_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# Serial port setup for Arduino
# Update the port based on your system
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

# Generate a 32-character alphanumeric encryption key
def generate_encryption_key(ldr_values):
    key = ''.join(alphanumeric_chars[value % 62] for value in ldr_values)
    while len(key) < 32:
        key += alphanumeric_chars[random.choice(ldr_values) % 62]
    return key

# Function to run the self-test on LDR values
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

# Route for generating keys
@app.route('/generate', methods=['POST'])
def generate():
    num_keys = int(request.form['num_keys'])
    keys = [generate_encryption_key(get_ldr_values()) for _ in range(num_keys)]
    return render_template('keys.html', keys=keys, num_keys=num_keys)

# Route to perform LDR self-test and display results
@app.route('/self_test')
def self_test():
    results = run_self_test()
    return render_template('self_test.html', results=results)

# Route to download self-test results as CSV
@app.route('/download_self_test_csv')
def download_self_test_csv():
    results = run_self_test()
    df = pd.DataFrame(results)
    csv_file = 'self_test_results.csv'
    df.to_csv(csv_file, index=False)
    return send_file(csv_file, as_attachment=True)

# Route to download keys as CSV
@app.route('/download_csv')
def download_csv():
    num_keys = int(request.args.get('num_keys'))
    keys = [generate_encryption_key(get_ldr_values()) for _ in range(num_keys)]
    df = pd.DataFrame({'Keys': keys})
    csv_file = 'encryption_keys.csv'
    df.to_csv(csv_file, index=False)
    return send_file(csv_file, as_attachment=True)

# Route to download keys as PDF
@app.route('/download_pdf')
def download_pdf():
    num_keys = int(request.args.get('num_keys'))
    keys = [generate_encryption_key(get_ldr_values()) for _ in range(num_keys)]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for key in keys:
        pdf.cell(200, 10, txt=key, ln=True)
    pdf_file = 'encryption_keys.pdf'
    pdf.output(pdf_file)
    return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

