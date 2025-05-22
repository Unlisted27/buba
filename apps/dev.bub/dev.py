#!/usr/bin/env python3
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(s.getsockname()[0])
s.close()
print("Hello World, Im dev")