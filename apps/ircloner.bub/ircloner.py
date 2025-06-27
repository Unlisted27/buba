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


def send(data):
    #bubasics.clear_screen()
    print("Sending data...")
    #bubasics.scrnprint("Sending data...")
    pi = pigpio.pi()
    PIN = 19  # Must be a hardware PWM-capable GPIO (18 recommended)
    CARRIER = 38000  # 38 kHz
    marks_wid = {}
    spaces_wid = {}

    wave = []

    for i in range(len(data)):
        duration = data[i]
        if duration < 10:  # Skip junk durations
            continue
        if i % 2 == 0:
            # Mark (LED on with modulation)
            if duration not in marks_wid:
                wf = []
                cycles = int(CARRIER * duration / 1e6)
                on = int(1e6 / CARRIER / 2)
                off = on
                #bubasics.error_warn() #MADE IT HERE
                for _ in range(cycles):
                    wf.append(pigpio.pulse(1 << PIN, 0, on))
                    wf.append(pigpio.pulse(0, 1 << PIN, off))
                pi.wave_add_generic(wf)
                #bubasics.error_warn() #MADE IT HERE
                wid = pi.wave_create()
                if wid < 0:
                    bad_waves += 1
                    continue
                marks_wid[duration] = wid
                #bubasics.error_warn() #DIDNT MAKE IT
            wave.append(marks_wid[duration])
        else:
            # Space (LED off)
            #bubasics.error_warn() #DIDNT MAKE IT
            if duration not in spaces_wid:
                pi.wave_add_generic([pigpio.pulse(0, 0, duration)])
                wid = pi.wave_create()
                if wid < 0:
                    bad_waves += 1
                    continue
                spaces_wid[duration] = wid
        wave.append(spaces_wid[duration])
    #bubasics.error_warn() DIDNT MAKE IT
    pi.wave_chain(wave)
    #bubasics.error_warn()
    while pi.wave_tx_busy():
        time.sleep(0.01)

    for wid in marks_wid.values():
        pi.wave_delete(wid)
    for wid in spaces_wid.values():
        pi.wave_delete(wid)
    pi.wave_clear()
    pi.stop()
    print(f"Number of bad waves: {bad_waves}")
    #bubasics.scrnprint(f"Number of bad waves: {bad_waves}")
    #bubasics.btn_select.wait_for_press()

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
send(data)
#test()
#bubasics.error_warn() #FOR TESTING
#bubasics.button_cleanup()
#bubasics.btn_select.wait_for_press()
#bubasics.button_cleanup()
exit()