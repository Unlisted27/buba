#!/usr/bin/env python3
import pigpio, time

PIN     = 19      # your IR LED GPIO
CARRIER = 38000   # 38 kHz
DUR     = 1.0     # seconds

pi = pigpio.pi()
if not pi.connected:
    raise RuntimeError("Cannot connect to pigpio daemon")
pi.set_mode(PIN, pigpio.OUTPUT)

# 1) Constant ON (no carrier)
print(">>> Constant ON (no carrier) for 1 s")
pi.write(PIN, 1)
time.sleep(DUR)
pi.write(PIN, 0)
time.sleep(0.5)

# 2) 38 kHz carrier for 1 s
print(">>> 38 kHz carrier for 1 s")
# hardware_PWM(pin, frequency, dutycycle) — dutycycle: 0 to 1e6 (i.e. 0%–100%)
pi.hardware_PWM(PIN, CARRIER, 500_000)  # 50% duty
time.sleep(DUR)
pi.hardware_PWM(PIN, 0, 0)              # stop PWM
pi.stop()

print("Done")
