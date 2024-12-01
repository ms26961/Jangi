import serial
import time

try:
    # Open the serial port
    ser = serial.Serial('/dev/serial0', 9600, timeout=2)
    time.sleep(2)  # Allow time for the connection to initialize
    print("Serial connection established on /dev/serial0.")

    # Send the 'R' command to the Arduino
    ser.write(b'R')
    print("Sent 'R' command. Waiting for response...")

    # Read response from Arduino
    data = ser.readline().decode('utf-8').strip()
    if data:
        print(f"Received data from Arduino: {data}")
        # Convert the data into a list of integers
        try:
            ldr_values = [int(value) for value in data.split(',') if value.isdigit()]
            print(f"Parsed LDR values: {ldr_values}")
        except ValueError as e:
            print(f"Error parsing LDR values: {e}")
    else:
        print("No data received from Arduino.")

except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial connection closed.")
