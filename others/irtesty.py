#!/usr/bin/env python3
import pigpio
import time

PIN     = 19      # your IR LED GPIO
CARRIER = 38000   # 38 kHz
DUR     = 1.0     # seconds

pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("Cannot connect to pigpio daemon")
pi.set_mode(PIN, pigpio.OUTPUT)

# 1) Constant on for 1 s
print(">>> Constant ON (no carrier) for 1 s")
pi.write(PIN, 1)
time.sleep(DUR)
pi.write(PIN, 0)
time.sleep(0.5)  # brief gap

# 2) Carrier at 38 kHz for 1 s
print(">>> 38 kHz carrier for 1 s")
# build a single wave of ~1 s of 38 kHz pulses
wf = []
cycles = int(CARRIER * DUR)
half_period = int(1e6 / CARRIER / 2)  # µs

for _ in range(cycles):
    wf.append(pigpio.pulse(1<<PIN, 0, half_period))
    wf.append(pigpio.pulse(0, 1<<PIN, half_period))

pi.wave_clear()
pi.wave_add_generic(wf)
wid = pi.wave_create()
if wid >= 0:
    pi.wave_send_once(wid)
    while pi.wave_tx_busy():
        time.sleep(0.01)
    pi.wave_delete(wid)
else:
    print("Failed to create 38 kHz wave")

pi.stop()
print("Done")