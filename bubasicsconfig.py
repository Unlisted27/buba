#This is all of the configuration that the basics.py module references.

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