#!/usr/bin/env python3
import pigpio
import time
import os
os.system("sudo systemctl start pigpiod")

IR_GPIO = 19      # Your IR LED is connected to GPIO 19
CARRIER_FREQ = 38000  # 38 kHz

pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("Failed to connect to pigpiod.")

# Generate a carrier at 38kHz on GPIO 19
def carrier(gpio, duration=0.01, frequency=38000):
    """
    Send a modulated IR signal at 38kHz for `duration` seconds.
    """
    duty_cycle = 0.5  # 50%
    pi.hardware_PWM(gpio, frequency, int(duty_cycle * 1_000_000))  # duty in range 0–1M
    time.sleep(duration)
    pi.hardware_PWM(gpio, 0, 0)  # Turn off

# Send IR burst for 10 ms
carrier(IR_GPIO, 38000, 1)

os.system("sudo systemctl stop pigpiod")
pi.stop()
