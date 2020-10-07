from vidgear.gears import PiGear
from vidgear.gears import NetGear
import cv2

options = {"hflip": True, "exposure_mode": "auto", "iso": 800, "exposure_compensation": 15, "awb_mode": "horizon",
           "sensor_mode": 0}
stream = PiGear(resolution=(640, 480), framerate=30, logging=True, **options).start()
options = {'flag': 0, 'copy': False, 'track': False}
server = NetGear(address='192.168.57.1', port='5454', protocol='tcp', pattern=0, logging=True, **options)

# loop over until KeyBoard Interrupted
while True:
    try:
        (grabbed, frame) = stream.read()
        if not grabbed:
            break
        server.send(frame)
    except KeyboardInterrupt:
        break
stream.release()
server.close()
