import zmq
import time
from datetime import datetime

ec2_host = "ec2-13-58-201-148.us-east-2.compute.amazonaws.com"
port = 9002


def create_pub_socket():
    context = zmq.Context()
    sock = context.socket(zmq.PUB)
    sock.connect("tcp://{0}:{1}".format(ec2_host, port))  # notice
    return sock


def publish(pub_socket):
    message = {
        'data': 'hi my name is benyamin',
        'time': datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    }
    pub_socket.send_json(message, 0)
    return message


if __name__ == '__main__':
    socket = create_pub_socket()

    while True:
        print('\n')
        print('publisher: ', publish(socket))
        time.sleep(1)


"""
import socket

INITIALIZE_CONNECTION_PORT = 50054
ec2_host = "ec2-13-58-201-148.us-east-2.compute.amazonaws.com"


def set_up():
    port = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_init:
        sock_init.connect((ec2_host, INITIALIZE_CONNECTION_PORT))

        while True:
            msg_port = sock_init.recv(16)
            if len(msg_port) <= 0:
                break
            port += msg_port.decode("utf-8")

    if not port:
        raise ConnectionError("Error setting up port for connection")
    return int(port)


print(set_up())
print(set_up())
print(set_up())
print(set_up())
#print(set_up())
#print(set_up())
#print(set_up())
#print(set_up())
#print(set_up())
#print(set_up())
#print(set_up())
#print(set_up())
#print(set_up())
#print(set_up())
#print(set_up())
#print(set_up())
"""

"""
import time
import zmq
from threading import Thread

host = "ec2-13-58-201-148.us-east-2.compute.amazonaws.com"
port = "5001"

ctx = zmq.Context()

def update_smart_mirror(appliance):
    socket = ctx.socket(zmq.PUB)
    socket.connect("tcp://{0}:{1}".format(host, port))
    time.sleep(5)

    status = {"status": True}
    # Sends multipart message to subscriber
    socket.send_string(appliance, flags=zmq.SNDMORE)
    socket.send_json(status)

coffee_maker = Thread(target=update_smart_mirror, args=("COFFEE MAKER",))
toaster = Thread(target=update_smart_mirror, args=("TOASTER",))

coffee_maker.start()
toaster.start()

# waits for both to send messages before exiting
coffee_maker.join()
toaster.join()
"""
