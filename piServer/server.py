"""@package PyServer

This is the starting point for the pyserver to send
video feed back to the ec2 server.

More details.
"""

import argparse
import customcamera
import time
import zmq
import socket

"""Entry point for pyserver
Entry point for the pyserver. Will process arguments
and establish the connection with the ec2 server.
"""
option_parse = argparse.ArgumentParser(description="Set up of Raspberry Pi Camera streaming module")
option_parse.add_argument("--resolution", type=str, default=customcamera.CameraDefaults.CAMERA_RESOLUTION_DEFAULT, help="Set the resolution of the camera", choices=customcamera.get_valid_resolutions())
option_parse.add_argument("--framerate", type=int, default=customcamera.CameraDefaults.CAMERA_FRAME_RATE_DEFAULT, help="Set the frame rate", choices=customcamera.get_valid_frame_rate())
option_parse.add_argument("--hflip", type=bool, default=customcamera.CameraDefaults.CAMERA_H_FLIP_DEFAULT, help="Set the h-flip value", choices=customcamera.get_valid_hflip())
option_parse.add_argument("--vflip", type=bool, default=customcamera.CameraDefaults.CAMERA_V_FLIP_DEFAULT, help="Set the v-flip value", choices=customcamera.get_valid_vflip())
option_parse.add_argument("--rotation", type=int, default=customcamera.CameraDefaults.CAMERA_ROTATION_DEFAULT, help="Set the rotation value", choices=customcamera.get_valid_rotation())
option_parse.add_argument("--iso", type=int, default=customcamera.CameraDefaults.CAMERA_ISO_DEFAULT, help="Set the ISO value", choices=customcamera.get_valid_iso())
option_parse.add_argument("--brightness", type=int, default=customcamera.CameraDefaults.CAMERA_BRIGHTNESS_DEFAULT, help="Set the brightness value", choices=customcamera.get_valid_brightness())
option_parse.add_argument("--contrast", type=int, default=customcamera.CameraDefaults.CAMERA_CONTRAST_DEFAULT, help="Set the contrast value", choices=customcamera.get_valid_contrast())
option_parse.add_argument("--saturation", type=int, default=customcamera.CameraDefaults.CAMERA_SATURATION_DEFAULT, help="Set the saturation value", choices=customcamera.get_valid_saturation())
option_parse.add_argument("--stabilization", type=int, default=customcamera.CameraDefaults.CAMERA_STABILIZATION_DEFAULT, help="Set the stabilization value", choices=customcamera.get_valid_stabilization())
option_parse.add_argument("--debug", type=bool, default=customcamera.CameraDefaults.OTHER_DEBUG, help="Shows debugging information", choices=customcamera.get_valid_debug())

args = vars(option_parse.parse_args())
INITIALIZE_CONNECTION_PORT = 5050
DEBUG = args["debug"]
port_zmq = ""
pi_name = None

def get_PI_name():
    with open("pi_label.txt", "r") as f:
        pi_name = f.readline()
    if not pi_name:
        if DEBUG:
            print("Error defining the PI name.")
        raise
    return str(pi_name)

def set_up_connection(name):
    port = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_init:
        sock_init.connect(("ec2-13-58-201-148.us-east-2.compute.amazonaws.com", INITIALIZE_CONNECTION_PORT))
        sock_init.sendall(name.encode("utf-8"))
        sock_init.shutdown(socket.SHUT_WR)

        while True:
            msg = sock_init.recv(8)
            if len(msg) <= 0:
                break
            port += msg.decode("utf-8")

    if not port:
        if DEBUG:
            print("Error setting up port for connnection")
        raise
    return int(port)


try:
    pi_name = get_PI_name()
    zmq_port = set_up_connection(pi_name)
    if DEBUG:
        count_frame = 0
        print("ZMQ_PORT:", zmq_port, "PI_NAME", pi_name)
    """
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.set_hwm(1)     
    socket.connect("tcp://ec2-13-58-201-148.us-east-2.compute.amazonaws.com:%s" % zmq_port)

    camera = customcamera.CustomCamera(args)
    camera.start()
    time.sleep(.5)
    while camera.is_stopped():
        socket.send(camera.get_frame())

        # AI processing could go here in the future since the frame capture is on a separate thread
        
        if DEBUG:
            print("Sent: %s" % count_frame)
            count_frame = (count_frame + 1) % 100
    """
finally:
    camera.stop()
    socket.close()
    sock_init.close()
