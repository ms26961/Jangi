from flask import Flask, render_template, request, jsonify, send_file
import serial
import time
import pandas as pd
from fpdf import FPDF

app = Flask(__name__)

# Serial connection to Arduino via UART
try:
    ser = serial.Serial('/dev/serial0', 9600)  # Use /dev/serial0 for RX/TX pins
    time.sleep(2)
except serial.SerialException:
    ser = None
    print("Warning: Arduino not connected or serial port unavailable.")

# Function to request and read LDR values from Arduino
def get_ldr_values():
    if ser:
        try:
            # Send the "R" command to Arduino to request LDR data
            ser.write(b'R')
            print("Sent 'R' command to Arduino. Waiting for response...")

            # Read the data from Arduino
            data = ser.readline().decode('utf-8').strip()
            print(f"Raw data received from Arduino: '{data}'")  # Debugging log

            if not data:
                print("No data received from Arduino.")
                return []

            # Parse the received data
            ldr_values = [
                int(value) for value in data.split(',') 
                if value.strip().isdigit() and 1 <= int(value) <= 200
            ]
            
            if not ldr_values:
                print("No valid LDR values received (all were out of range or invalid).")
                return []

            print(f"Processed LDR values: {ldr_values}")
            return ldr_values
        except ValueError as e:
            print(f"ValueError while parsing LDR values: {e}")
            return []
        except Exception as e:
            print(f"Error reading from Arduino: {e}")
            return []
    else:
        print("Serial connection not established.")
        return []



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_self_test', methods=['POST'])
def run_self_test():
    ldr_values = get_ldr_values()
    if not ldr_values:
        return jsonify({"error": "No valid data received from sensors."}), 500

    # Group into 4 multiplexers with 16 sensors each
    grouped_results = [
        {"Multiplexer": f"Mux {mux + 1}", "Values": ldr_values[mux * 16:(mux + 1) * 16]}
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
        if not ldr_values:
            return "Error: No valid data received from sensors.", 500
        keys.append(''.join('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'[value % 62] for value in ldr_values[:32]))

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
