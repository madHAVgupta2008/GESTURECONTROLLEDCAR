import serial
ser = serial.Serial('COM5', 9600)
if ser.is_open:
    print("Serial connection established")
else:
    print("Failed to connect to serial port")