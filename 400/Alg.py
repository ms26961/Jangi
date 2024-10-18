import serial
import time

# Number of encryption keys to generate
NUM_KEYS = 32

# Open the serial port where the Arduino is connected
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Replace with your serial port
time.sleep(2)  # Wait for the connection to be established

# Function to convert sensor values to bits based on threshold
def ldr_to_bits(ldr_values, threshold=512):
    bits = []
    for value in ldr_values:
        if value > threshold:
            bits.append(1)
        else:
            bits.append(0)
    return bits

# Function to generate 32-bit encryption keys
def generate_encryption_keys(num_keys):
    encryption_keys = []
    bit_pool = []

    while len(encryption_keys) < num_keys:
        if ser.in_waiting > 0:
            # Read a line from the serial port
            ldr_data = ser.readline().decode('utf-8').strip()  # Read and decode the incoming data
            
            # Split the comma-separated values into a list
            ldr_values = ldr_data.split(',')
            
            # Convert the string values into integers
            ldr_values = [int(value) for value in ldr_values]
            
            # Convert LDR values to bits (0 or 1)
            bits = ldr_to_bits(ldr_values)
            
            # Append the bits to the bit pool
            bit_pool.extend(bits)

            # Check if we have enough bits to form a 32-bit key
            while len(bit_pool) >= 32:
                # Take the first 32 bits from the bit pool
                key_bits = bit_pool[:32]
                
                # Remove the used bits from the pool
                bit_pool = bit_pool[32:]
                
                # Convert the bits into an integer (encryption key)
                key = int(''.join(map(str, key_bits)), 2)
                
                # Append the key to the encryption keys list
                encryption_keys.append(key)
                print(f"Generated key {len(encryption_keys)}: {key}")

    return encryption_keys

# Generate 32 encryption keys
keys = generate_encryption_keys(NUM_KEYS)

# Print the final list of keys
print("Final 32 Encryption Keys:")
for i, key in enumerate(keys):
    print(f"Key {i+1}: {key}")
