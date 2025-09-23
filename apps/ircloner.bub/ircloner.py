import serial, json
ser = serial.Serial('/dev/serial0', 1200, timeout=1)
ser.write(b'{"cmd":"start_scan"}\n')
line = ser.readline().decode().strip()
if line:
    print(line)
