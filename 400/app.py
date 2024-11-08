#Import necessary libraries to communicate with devices
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

# Serial port to communicate with Arduino
# Replace '/dev/ttyUSB0' with the correct port on your system (can also be /dev/ttyACM0)
ser = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)  # Wait for the serial connection to initialize

# Generate a 32-character alphanumeric encryption key from LDR data
def generate_encryption_key(ldr_values):
    key = ''
    
    # Normalize the LDR values and convert to alphanumeric characters
    for value in ldr_values:
        normalized_value = value % 62  # Normalize to the range of 0-61 (corresponding to alphanumeric_chars)
        key += alphanumeric_chars[normalized_value]
    
    # Ensure the key is 32 characters long by adding more characters
    while len(key) < 32:
        random_value = random.choice(ldr_values) % 62  # Use remaining values to fill the key
        key += alphanumeric_chars[random_value]
    
    return key

# Function to read LDR values from Arduino via Serial
def get_ldr_values():
    # Read the serial input and split the comma-separated values
    if ser.in_waiting > 0:
        ldr_data = ser.readline().decode('utf-8').strip()  # Read and decode the incoming data
        ldr_values = [int(value) for value in ldr_data.split(',')]  # Convert string values to integers
        return ldr_values
    else:
        return [random.randint(0, 1023) for _ in range(16)]  # Return random values if no data is available

# Generate multiple encryption keys
def generate_multiple_keys(num_keys):
    keys = []
    for _ in range(num_keys):
        ldr_values = get_ldr_values()  # Get actual LDR values from Arduino
        key = generate_encryption_key(ldr_values)
        keys.append(key)
    return keys

# Flask route for the main index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to generate and display keys
@app.route('/generate', methods=['POST'])
def generate():
    num_keys = int(request.form['num_keys'])  # Get the number of keys from user input
    keys = generate_multiple_keys(num_keys)   # Generate the requested number of keys
    return render_template('keys.html', keys=keys, num_keys=num_keys)

# Route to download the keys as CSV
@app.route('/download_csv')
def download_csv():
    num_keys = int(request.args.get('num_keys'))  # Get the number of keys from the query parameters
    keys = generate_multiple_keys(num_keys)       # Generate the requested number of keys
    
    # Create a pandas DataFrame to hold the keys and save it as CSV
    df = pd.DataFrame({'Keys': keys})
    csv_file = 'encryption_keys.csv'
    df.to_csv(csv_file, index=False)  # Save the DataFrame as a CSV file
    
    return send_file(csv_file, as_attachment=True)  # Return the file as a downloadable attachment

# Route to download the keys as PDF
@app.route('/download_pdf')
def download_pdf():
    num_keys = int(request.args.get('num_keys'))  # Get the number of keys from the query parameters
    keys = generate_multiple_keys(num_keys)       # Generate the requested number of keys
    
    # Create a PDF file to hold the keys
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for key in keys:
        pdf.cell(200, 10, txt=key, ln=True)  # Add each key to a new line in the PDF
    
    pdf_file = 'encryption_keys.pdf'
    pdf.output(pdf_file)  # Save the PDF file
    
    return send_file(pdf_file, as_attachment=True)  # Return the PDF file as a downloadable attachment

# Main block to run the Flask web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the app on port 5000, accessible from any IP
