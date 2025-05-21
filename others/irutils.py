import pigpio
import time

RECV_GPIO = 17  # Adjust if using a different pin

pi = pigpio.pi()
if not pi.connected:
    print("Failed to connect to pigpiod.")
    exit()

# Store edges
edges = []

# Callback when IR edges change
def cbf(gpio, level, tick):
    global edges
    if level != pigpio.TIMEOUT:
        edges.append((level, tick))
    else:
        # No signal for 15ms, means IR message likely finished
        if len(edges) < 2:
            edges = []
            return

        print("\nIR signal received:")
        for i in range(1, len(edges)):
            duration = pigpio.tickDiff(edges[i - 1][1], edges[i][1])
            print(duration, end=", ")
        print("\n--- End ---\n")
        edges = []

# Set up pin
pi.set_mode(RECV_GPIO, pigpio.INPUT)
pi.set_pull_up_down(RECV_GPIO, pigpio.PUD_UP)

# Watchdog triggers after 15ms idle to detect end of message
pi.set_watchdog(RECV_GPIO, 15)

# Callback setup
cb = pi.callback(RECV_GPIO, pigpio.EITHER_EDGE, cbf)

try:
    print("Ready. Press buttons on your remote...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")

cb.cancel()
pi.set_watchdog(RECV_GPIO, 0)
pi.stop()
