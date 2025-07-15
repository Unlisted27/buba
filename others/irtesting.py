import pigpio
import time

IR_GPIO = 19      # GPIO pin connected to IR LED
CARRIER_FREQ = 38000  # 38 kHz
DUTY_CYCLE = 0.5  # 50%

# Start pigpio
pi = pigpio.pi()
if not pi.connected:
    print("Could not connect to pigpio daemon.")
    exit()

# Set hardware PWM
pi.hardware_PWM(IR_GPIO, CARRIER_FREQ, int(DUTY_CYCLE * 1e6))  # duty cycle in range 0–1e6

print("Transmitting 38kHz IR signal... Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")
    pi.hardware_PWM(IR_GPIO, 0, 0)  # Stop PWM
    pi.stop()
