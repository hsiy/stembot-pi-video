from vidgear.gears import PiGear
from vidgear.gears import NetGear
import cv2

client_ip_address = "192.168.0.162"
options = {"hflip": True, "exposure_mode": "auto", "iso": 800, "exposure_compensation": 15, "awb_mode": "horizon", "sensor_mode": 0}
stream = PiGear(resolution=(640, 480), framerate=30, logging=True, **options).start()
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
