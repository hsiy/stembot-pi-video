from vidgear.gears import NetGear
import socket
import cv2


def getDeviceIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("10.255.255.255", 1))
    IP = s.getsockname()[0]
    s.close()
    return IP


client_ip_address = getDeviceIP()
print("client_ip_address", client_ip_address)

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
