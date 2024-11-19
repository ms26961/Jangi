from flask import Flask, render_template, request, jsonify, send_file
import serial
import time
import random
import pandas as pd
from fpdf import FPDF

app = Flask(__name__)

# Serial connection to Arduino
try:
    ser = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(2)
except serial.SerialException:
    ser = None
    print("Warning: Arduino not connected or serial port unavailable.")

# Alphanumeric character set for encryption keys
alphanumeric_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# Function to request and read LDR values from Arduino
def get_ldr_values():
    if ser:
        try:
            ser.write(b'R')  # Send "R" command to Arduino to request LDR data
            data = ser.readline().decode('utf-8').strip()
            ldr_values = [int(value) for value in data.split(',') if 1 <= int(value) <= 200]
            return ldr_values
        except Exception as e:
            print(f"Error reading from Arduino: {e}")
            return None
    return None

# Function to generate a 32-character encryption key
def generate_encryption_key(ldr_values):
    filtered_values = [value for value in ldr_values if value > 0]  # Ignore invalid values
    return ''.join(alphanumeric_chars[value % 62] for value in filtered_values[:32])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/self_test')
def self_test_page():
    return render_template('self_test.html')

@app.route('/run_self_test', methods=['POST'])
def run_self_test():
    ldr_values = get_ldr_values() 
    valid_values = [value for value in ldr_values if value > 0]

    # Group into 4 multiplexers with 16 sensors each
    grouped_results = [
        {"Multiplexer": f"Mux {mux + 1}", "Values": valid_values[mux * 16:(mux + 1) * 16]}
        for mux in range(4)
    ]

    return jsonify(grouped_results)

@app.route('/generate', methods=['POST'])
def generate_keys():
    num_keys = int(request.form['num_keys'])
    output_option = request.form['output_option']  # Retrieve the user's selected output option

    keys = []
    for _ in range(num_keys):
        ldr_values = get_ldr_values()
        keys.append(generate_encryption_key(ldr_values))

    if output_option == 'display':
        return render_template('keys.html', keys=keys)
    elif output_option == 'csv':
        return download_keys(keys, format='csv')
    elif output_option == 'pdf':
        return download_keys(keys, format='pdf')
    else:
        return "Invalid output option selected.", 400

def download_keys(keys, format):
    if format == 'csv':
        df = pd.DataFrame({'Keys': keys})
        csv_file = 'encryption_keys.csv'
        df.to_csv(csv_file, index=False)
        return send_file(csv_file, as_attachment=True)
    elif format == 'pdf':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for key in keys:
            pdf.cell(200, 10, txt=key, ln=True)
        pdf_file = 'encryption_keys.pdf'
        pdf.output(pdf_file)
        return send_file(pdf_file, as_attachment=True)

@app.route('/download_self_test', methods=['POST'])
def download_self_test():
    ldr_values = get_ldr_values() 
    valid_values = [value for value in ldr_values if value > 0]

    # Group into 4 multiplexers
    grouped_results = [
        {"Multiplexer": f"Mux {mux + 1}", "Sensor ID": f"Sensor {i + 1}", "Value": valid_values[mux * 16 + i]}
        for mux in range(4) for i in range(16)
    ]

    format = request.form['download_format']
    if format == 'csv':
        df = pd.DataFrame(grouped_results)
        csv_file = 'self_test_results.csv'
        df.to_csv(csv_file, index=False)
        return send_file(csv_file, as_attachment=True)
    elif format == 'pdf':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for result in grouped_results:
            pdf.cell(200, 10, txt=f"{result['Multiplexer']} - {result['Sensor ID']}: {result['Value']}", ln=True)
        pdf_file = 'self_test_results.pdf'
        pdf.output(pdf_file)
        return send_file(pdf_file, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
