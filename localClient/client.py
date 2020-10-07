from vidgear.gears import NetGear
import cv2
options = {'flag': 0, 'copy': False, 'track': False}
client = NetGear(address='192.168.0.243', protocol='tcp',  pattern=1, receive_mode=True, logging=True,
                 **options)
while True:
    frame = client.recv()
    if frame is None:
        break
    cv2.imshow("Output Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cv2.destroyAllWindows()
client.close()
