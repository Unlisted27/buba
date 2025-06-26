import pigpio
import time

PIN = 17  # GPIO where IR receiver OUT is connected

pi = pigpio.pi()
if not pi.connected:
    exit()

pi.set_mode(PIN, pigpio.INPUT)

# Store durations here
raw_data = []
last_tick = None

def cbf(gpio, level, tick):
    global last_tick
    if last_tick is not None:
        delta = pigpio.tickDiff(last_tick, tick)  # Duration in microseconds
        raw_data.append(delta)
        print(delta, end=", ", flush=True)
    last_tick = tick

# Start capturing
cb = pi.callback(PIN, pigpio.EITHER_EDGE, cbf)

try:
    print("Press remote button...")
    time.sleep(5)  # You can adjust the recording window
finally:
    cb.cancel()
    pi.stop()
    print("\nCaptured pulse list:")
    print(raw_data)
