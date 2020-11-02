import zmq
import cv2  # maybe? probably not though
import socket

STARTING_PORT = 10000
AVAILABLE_PORTS = [*range(10000, 20000, 1)]
INITIALIZE_CONNECTION_PORT = 5000


def find_new_port():
    new_port = STARTING_PORT
    while True:
        if new_port in AVAILABLE_PORTS:
            AVAILABLE_PORTS.remove(new_port)
            break
        new_port += 1
    return new_port


def add_back_port(port):
    AVAILABLE_PORTS.append(port)
    AVAILABLE_PORTS.sort()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("ec2-13-58-201-148.us-east-2.compute.amazonaws.com", INITIALIZE_CONNECTION_PORT))



