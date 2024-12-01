import serial
import time

def test_arduino_serial():
    # Try to establish a serial connection to the Arduino
    try:
        ser = serial.Serial('/dev/serial0', 9600, timeout=2)  # Use the correct UART port
        time.sleep(2)  # Allow some time for the connection to initialize
        print("Serial connection established with Arduino.")
    except serial.SerialException as e:
        print(f"Error: Could not connect to Arduino. {e}")
        return

    try:
        while True:
            # Send the "R" command to request LDR values
            ser.write(b'R')
            print("Sent 'R' command to Arduino. Waiting for response...")

            # Read the response from Arduino
            data = ser.readline().decode('utf-8').strip()
            if not data:
                print("No data received from Arduino. Retrying...")
                continue

            # Display the raw data received from Arduino
            print(f"Raw data: {data}")

            # Parse the data into a list of integers
            try:
                ldr_values = [int(value) for value in data.split(',') if value.isdigit()]
                print(f"Parsed LDR values: {ldr_values}")
            except ValueError as parse_error:
                print(f"Error parsing LDR values: {parse_error}")

            # Add a small delay to avoid overwhelming the Arduino
            time.sleep(1)

    except KeyboardInterrupt:
        print("Test interrupted by user. Closing connection...")
    finally:
        ser.close()
        print("Serial connection closed.")

if __name__ == "__main__":
    test_arduino_serial()
