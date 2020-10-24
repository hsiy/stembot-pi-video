import argparse
import time
import zmq
import picamera
import struct
import io

low = (640, 480)
high = (1080, 720)

class customActions(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(customActions, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if values == "low":
            values = low
        elif values == "high":
            values = high
        setattr(namespace, self.dest, values)       

option_parse = argparse.ArgumentParser(description="Set up of Raspberry Pi Camera streaming module")
option_parse.add_argument("--resolution", type=str, default=low, help="Set the resolution of the camera", choices=["high", "low"], action=customActions)
option_parse.add_argument("--ip", type=str, default="localhost", help="Set the IP address")
option_parse.add_argument("--port", type=int, default="5454", help="Set the IP address")
option_parse.add_argument("--framerate", type=int, default="30", help="Set the framerate")
option_parse.add_argument("--debug", type=bool, default=False, help="Shows debugging information", choices=[True, False])

DEBUG = option_parse.parse_args().debug

if DEBUG:
    print(option_parse.parse_args())
    print("Resolution: ", option_parse.parse_args().resolution)
    print("IP Address: ", option_parse.parse_args().ip)
    print("Port: ", option_parse.parse_args().port)
    print("Port: ", option_parse.parse_args().framerate)

(height, width) = option_parse.parse_args().resolution

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.set_hwm(1)
socket.bind("tcp://*:" + str(option_parse.parse_args().port))

camera = picamera.PiCamera()
camera.resolution = option_parse.parse_args().resolution
camera.framerate = option_parse.parse_args().framerate
# possibly remove preview?
camera.start_preview()
stream = io.BytesIO()

time.sleep(.1)

count_frame = 0
try:
    for frame in camera.capture_continuous(stream, format="jpeg", use_video_port=True):
        message = str(stream.getvalue())
        socket.send(stream.getvalue())
        if DEBUG:
            print("Sent!\n", framenum)
        framenum = (framenum + 1) % 100
        stream.seek(0)
finally:
    camera.close()
    stream.close()
    socket.close()
