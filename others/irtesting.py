import pigpio
import time

IR_GPIO = 19  # Output pin
CARRIER_FREQ = 38000  # 38kHz
CARRIER_DUTY = 0.5     # 50%

# Your captured data
raw_pulses = [
    9145, 4530, 610, 535, 586, 554, 610, 535, 585, 560, 610, 530,
    615, 530, 610, 535, 610, 535, 610, 1650, 610, 1655, 605, 1655,
    635, 1625, 610, 535, 610, 1650, 610, 1650, 610, 1655, 605, 1655,
    605, 1655, 610, 535, 605, 535, 605, 540, 610, 535, 605, 540,
    605, 540, 605, 535, 610, 535, 610, 1650, 610, 1655, 605, 1655,
    605, 1655, 610, 1650, 610, 1655, 605
]

pi = pigpio.pi()
if not pi.connected:
    print("Could not connect to pigpio daemon.")
    exit()

# Turn off any existing PWM
pi.hardware_PWM(IR_GPIO, 0, 0)

# Clear old waveforms
pi.wave_clear()

# Helper to generate 38kHz carrier for a given time (in microseconds)
def carrier_wave(gpio, duration_us):
    cycles = int(duration_us / (1_000_000 / CARRIER_FREQ))
    micros_per_cycle = 1_000_000 / CARRIER_FREQ
    on_micros = int(micros_per_cycle * CARRIER_DUTY)
    off_micros = int(micros_per_cycle - on_micros)

    pulses = []
    for _ in range(cycles):
        pulses.append(pigpio.pulse(1 << gpio, 0, on_micros))   # LED ON
        pulses.append(pigpio.pulse(0, 1 << gpio, off_micros))  # LED OFF
    return pulses

# Convert raw data to pigpio pulses
wf = []
on = True
for duration in raw_pulses:
    if on:
        wf += carrier_wave(IR_GPIO, duration)
    else:
        wf.append(pigpio.pulse(0, 0, duration))  # delay (IR off)
    on = not on

# Load and transmit
pi.wave_add_generic(wf)
wave_id = pi.wave_create()

if wave_id >= 0:
    pi.wave_send_once(wave_id)
    print("IR signal sent.")
    while pi.wave_tx_busy():
        time.sleep(0.01)
    pi.wave_delete(wave_id)

# Cleanup
pi.wave_clear()
pi.stop()
