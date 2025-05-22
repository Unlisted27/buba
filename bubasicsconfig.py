#This is all of the configuration that the basics.py module references.
from gpiozero import Button
from luma.core.interface.serial import spi
from luma.lcd.device import st7789

class buttons():
    # ---- Configure these settings if you adjust the GPIO for the buttons ----#
    # Numbers lead to GPIO pin numbers, NOT physical pin numbers
    # The bounce_time value is a delay between button presses to avoid mechanical interferance sending multiple pressed signals
    # Default GPIO values are: up:4 down:27 select:22
    btn_up_gpio = 4
    btn_down_gpio = 27
    btn_select_gpio = 22
    btn_up = Button(btn_up_gpio, bounce_time = 0.05)
    btn_down = Button(btn_down_gpio, bounce_time = 0.05)
    btn_select = Button(btn_select_gpio, bounce_time = 0.05)

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
    # Uncomment and adjust the following if you need to change the overall screen settings
    #rotate=0,
    #offset_x=0,
    #offset_y=0,
)