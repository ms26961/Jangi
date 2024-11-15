import serial
import time

# Open the serial port where the Arduino is connected
ser = serial.Serial('/dev/ttyACM0', 9600)  # Replace ttyUSB0 with correct port
time.sleep(2)  # Wait for the connection to be established

while True:
    if ser.in_waiting > 0:
        # Read a line from the serial port
        ldr_data = ser.readline().decode('utf-8').strip()  # Read and decode the incoming data
        
        # Split the comma-separated values into a list
        ldr_values = ldr_data.split(',')
        
        # Convert the string values into integers
        try:
            ldr_values = [int(value) for value in ldr_values]
        except ValueError:
            print("Error: Non-integer value received in LDR data")
            continue

        # Ensure we received data for all 64 LDRs
        if len(ldr_values) != 64:
            print(f"Warning: Expected 64 values but received {len(ldr_values)}. Data: {ldr_values}")
            continue

        # Print the LDR values grouped by multiplexer (optional)
        for mux in range(4):
            start_index = mux * 16
            end_index = start_index + 16
            print(f"Multiplexer {mux + 1} Values: {ldr_values[start_index:end_index]}")

        # (Optional) Process the LDR data to generate encryption keys or other output
        # process_ldr_data(ldr_values)

    time.sleep(0.1)  # Add a small delay to avoid overwhelming the serial port
