import serial
import time

# Open the serial port where the Arduino is connected
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Replace ttyUSB0 with correct port
time.sleep(2)  # Wait for the connection to be established

while True:
    if ser.in_waiting > 0:
        # Read a line from the serial port
        ldr_data = ser.readline().decode('utf-8').strip()  # Read and decode the incoming data
        
        # Split the comma-separated values into a list
        ldr_values = ldr_data.split(',')
        
        # Convert the string values into integers
        ldr_values = [int(value) for value in ldr_values]
        
        # Print the LDR values (optional: replace with further processing)
        print(f"LDR Values: {ldr_values}")

        # (Optional) Process the LDR data to generate encryption keys or other output
        # process_ldr_data(ldr_values)

    time.sleep(0.1)  # Add a small delay to avoid overwhelming the serial port
