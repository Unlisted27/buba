#!/usr/bin/env python3
print("Made it!")
import socket, bubasics
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
    bubasics.clear_screen()
    bubasics.button_cleanup()
except Exception as e:
    print(e)
    bubasics.button_cleanup()
    bubasics.error_warn()
    exit()