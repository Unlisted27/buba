#!/usr/bin/env python3

import os, pigpio, time#, bubasics

def test():
    pi = pigpio.pi()
    pi.set_mode(19, pigpio.OUTPUT)

    #bubasics.scrnprint("Blinking GPIO19...")
    for _ in range(5):
        pi.write(19, 1)
        time.sleep(0.5)
        pi.write(19, 0)
        time.sleep(0.5)

    pi.stop()
    #bubasics.btn_select.wait_for_press()

def send_in_chunks(data, chunk_size=50):
    pi = pigpio.pi()
    PIN     = 19
    CARRIER = 38000

    # Helper: build a pulse list from a slice of data
    def build_wf(data_slice):
        wf = []
        for idx, duration in data_slice:
            if duration < 10:
                continue
            if idx % 2 == 0:
                # mark: carrier burst
                cycles = int(CARRIER * duration / 1e6)
                on  = int(1e6 / CARRIER / 2)
                off = on
                for _ in range(cycles):
                    wf.append(pigpio.pulse(1<<PIN, 0, on))
                    wf.append(pigpio.pulse(0, 1<<PIN, off))
            else:
                # space: LED off
                wf.append(pigpio.pulse(0, 0, duration))
        return wf

    # Pair each duration with its index
    indexed = list(enumerate(data))
    # Split into chunks of chunk_size pairs
    for i in range(0, len(indexed), chunk_size):
        slice_ = indexed[i:i+chunk_size]
        wf    = build_wf(slice_)
        pi.wave_clear()
        pi.wave_add_generic(wf)
        wid = pi.wave_create()
        if wid >= 0:
            pi.wave_send_once(wid)
            while pi.wave_tx_busy():
                time.sleep(0.01)
            pi.wave_delete(wid)
        else:
            print("Chunk failed to create wave")
    pi.stop()


def listen():
    os.system("sudo systemctl start pigpiod") #Need to start pigpiod (pigpio deamon) for this to work
    time.sleep(0.5)  # Give it time to start

    PIN = 17  # GPIO where IR receiver OUT is connected
    listen_time = 5

    for _ in range(5):
        pi = pigpio.pi()
        if pi.connected:
            break
        time.sleep(0.2)
    else:
        #bubasics.error_warn()
        exit()

    pi.set_mode(PIN, pigpio.INPUT)

    # Store durations here
    raw_data = []
    last_tick = None

    def cbf(gpio, level, tick):
        nonlocal last_tick
        if last_tick is not None:
            delta = pigpio.tickDiff(last_tick, tick)  # Duration in microseconds
            raw_data.append(delta)
            print(delta, end=", ", flush=True)
        last_tick = tick

    # Start capturing
    cb = pi.callback(PIN, pigpio.EITHER_EDGE, cbf)

    try:
        print(f"Listening for IR signals for {listen_time} seconds...")
        #bubasics.scrnprint(f"Listening for IR signals for {listen_time} seconds...")
        time.sleep(listen_time)  #You can adjust the recording window
    finally:
        cb.cancel()
        pi.stop()
        print("\nCaptured pulse list:")
        print(raw_data)
        if len(raw_data) > 0:
            #bubasics.clear_screen()
            #bubasics.scrnprint(f"Captured {len(raw_data)} pulses!")
            print(f"Captured {len(raw_data)} pulses!")
            return raw_data
        else:
            print(f"Did not capture any pulses ):")
            #bubasics.scrnprint(f"Did not capture any pulses ):")
        

data = listen()
for i in range(100):
    send_in_chunks(data)
    print(i)
#test()
#bubasics.error_warn() #FOR TESTING
#bubasics.button_cleanup()
#bubasics.btn_select.wait_for_press()
#bubasics.button_cleanup()
exit()