from vidgear.gears import NetGear
import cv2

client_ip_address = "192.168.0.162"
options = {'flag': 0, 'copy': False, 'track': False}
client = NetGear(address=client_ip_address, port='5454', receive_mode=True)
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
