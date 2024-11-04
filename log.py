import serial
import csv
import time
from datetime import datetime

SERIAL_PORT = 'COM19' 
BAUD_RATE = 9600
DURATION = 1 * 60  # Run for one hour (60 minutes * 60 seconds)

# Open serial port
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  

# Open CSV file to save data
with open('Logs/data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["Timestamp", "Voltage (V)", "Current (A)", "Power (W)", "Energy (kWh)", "Frequency (Hz)", "Power Factor"])

    start_time = time.time()
    while time.time() - start_time < DURATION:
        line = ser.readline().decode('utf-8').strip()
        
        # Check for different data patterns
        if "Voltage:" in line:
            voltage = line.split(": ")[1].replace("V", "").strip()
        elif "Current:" in line:
            current = line.split(": ")[1].replace("A", "").strip()
        elif "Power:" in line:
            power = line.split(": ")[1].replace("W", "").strip()
        elif "Energy:" in line:
            energy = line.split(": ")[1].replace("kWh", "").strip()
        elif "Frequency:" in line:
            frequency = line.split(": ")[1].replace("Hz", "").strip()
        elif "PF:" in line:
            pf = line.split(": ")[1].strip()

            # Write data row only after reading all values in a cycle
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([timestamp, voltage, current, power, energy, frequency, pf])
            print(f"{timestamp} - Voltage: {voltage} V, Current: {current} A, Power: {power} W, Energy: {energy} kWh, Frequency: {frequency} Hz, PF: {pf}")
        
        # time.sleep(1)  # Collect data every 1 second

ser.close()
