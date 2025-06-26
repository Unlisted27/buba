#!/usr/bin/env python3
import pigpio
import time

PIN = 17 #GPIO pin where the IR OUT is connected

def cbf(gpio, level, tick):
    print(f"GPIO: {gpio}, Level: {level}, Tick: {tick}")

    
pi = pigpio.pi()
if not pi.connected:
    exit()

pi.set_mode(PIN, pigpio.INPUT)
cb = pi.callback(PIN, pigpio.EITHER_EDGE, cbf)

try:
    print("Listening for raw IR signal...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    cb.cancel()
    pi.stop()