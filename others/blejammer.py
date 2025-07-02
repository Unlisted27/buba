import os
import time

# Random BLE advertising with hciconfig and hcitool
def advertise_loop():
    while True:
        os.system("sudo hciconfig hci0 noleadv")
        os.system("sudo hcitool -i hci0 cmd 0x08 0x0008 1E 02 01 1A 1B FF 4C 00 02 15 " +
                  "AA BB CC DD EE FF 00 00 00 00 00 00 00 00 C5 00 01")  # fake beacon data
        os.system("sudo hciconfig hci0 leadv 3")
        time.sleep(1)

try:
    advertise_loop()
except KeyboardInterrupt:
    print("Stopped.")
