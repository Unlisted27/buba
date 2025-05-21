#!/usr/bin/env python3
import sys,time,os, basics
from luma.core.interface.serial import spi
from luma.lcd.device import st7789
serial = spi(
    port=0,
    device=0,               # CE0 on GPIO8 (pin 24), marked as 0 cause spi 0 (chip select)
    gpio_DC=18,             # Data/Command (pin 12)
    gpio_RST=20,            # Reset (Pin 38)
    gpio_BACKLIGHT=12,      # Backlight (Pin 32)
    bus_speed_hz=40000000
)

# ---- create device ----
device = st7789(
    serial_interface=serial,
    width=320,
    height=240,
    #rotate=0,
    #offset_x=0,
    #offset_y=0,
)
def main():
    try:
        while True:
            try:
                curdir = [".."] + os.listdir()
                index, selected = basics.menu(device,curdir)
                selected_path = os.path.abspath(selected) #Ensuring its an absolute path
                #print(selected_path)
                if os.path.isdir(selected_path):
                    os.chdir(selected_path)
                elif basics.is_buba_exec(selected_path):
                    basics.run_buba_exec(selected_path)
                else:
                    print("Bad dir")
            except Exception as e:
                try:
                    print("ERROR: "+ str(type(e)))
                except Exception:
                    print("ERROR! Also, there was an error displaying the error type, GLHF (: )")
                basics.error_warn(device)
    except KeyboardInterrupt:
        sys.exit("Goodbye")

main()