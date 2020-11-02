import zmq
import cv2  # maybe? probably not though
import socket

STARTING_PORT = 10000
AVAILABLE_PORTS = [*range(10000, 19999, 1)]
new_port = STARTING_PORT
while True:
    if new_port in AVAILABLE_PORTS:
        AVAILABLE_PORTS.remove(new_port)
        break
    new_port += 1
print(new_port, AVAILABLE_PORTS)
