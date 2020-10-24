import argparse
import time
import picamera
import numpy as np
import cv2
import socket
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
option_parse.add_argument("--port", type=int, default="5700", help="Set the IP address")
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

unity_socket = socket.socket()
#unity_socket.connect((option_parse.parse_args().ip, option_parse.parse_args().port))
#connection = unity_socket.makefile('wb')

camera = picamera.PiCamera()
camera.resolution = option_parse.parse_args().resolution
camera.framerate = option_parse.parse_args().framerate

stream = io.BytesIO()
count = 0
time.sleep(.2)
try:
    for frame in camera.capture_continuous(stream, format="jpeg", use_video_port=True):
        print(stream.getvalue())
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        count = count + 1
        if count == 5:
            break
finally:
    camera.close()
    stream.close()
    unity_socket.close()

"""
cap = cv2.VideoCapture(0)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here

    # Display the resulting frame
    nparr = frame
    img_byte = cv2.imencode(".jpg", nparr)[1].tostring()
    print(type(img_byte))
    print(img_byte)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


client_ip_address = "192.168.0.162"
options = {"hflip": True, "exposure_mode": "auto", "iso": 1500, "exposure_compensation": 15, "awb_mode": "horizon", "sensor_mode": 0}
stream = PiGear(resolution=(640, 480), framerate=60, logging=True, **options).start()
server = NetGear(address=client_ip_address, port='5454')

# loop over until KeyBoard Interrupted
while True:
    try:
        frame = stream.read()
        # add processing ai stuff here
        server.send(frame)
    except KeyboardInterrupt:
        break
stream.release()
server.close()
"""