#!/usr/bin/env python3
import socket, bubasics
import RPi.GPIO as GPIO
GPIO.cleanup()
try:
    btn_select = bubasics.btn_select
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP
    bubasics.scrnprint("My ip: "+get_ip())
    btn_select.wait_for_press()
except Exception as e:
    print(e)
    bubasics.error_warn()
    exit()