import zmq

ec2_host = "ec2-13-58-201-148.us-east-2.compute.amazonaws.com"
port = 9002

if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, "")
    socket.bind("tcp://*:{0}".format(port))  # notice

    while True:
        data = socket.recv_json()
        print('second subscriber: ', data)
        print('\n')


"""
import socket
import threading
import time

INITIALIZE_CONNECTION_PORT = 50054
print_lock = threading.Lock()


def other_thread(input):
    print_lock.acquire()
    print("Spawn Secondary new thread: {}".format(input))
    print_lock.release()
    time.sleep(5)
    print_lock.acquire()
    print("Returning Secondary thread: {}".format(input))
    print_lock.release()
    return


def thread_function(connection, ip, port, tmp):
    with connection:
        connection.send(str(5034).encode("utf-8"))
    print_lock.acquire()
    print("Spawn new thread: {}".format(tmp))
    print_lock.release()
    threading.Thread(target=other_thread, args=(-tmp,)).start()
    time.sleep(2)
    print_lock.acquire()
    print("Returning thread: {}".format(tmp))
    print_lock.release()
    return


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as inc_sock:
    inc_sock.bind((socket.gethostbyname(socket.gethostname()), INITIALIZE_CONNECTION_PORT))
    inc_sock.listen(5)
    num = 0
    while True:
        incoming_connection, incoming_address = inc_sock.accept()
        threading.Thread(target=thread_function, args=(incoming_connection, incoming_address[0], incoming_address[1], num)).start()
        num += 1
"""

"""
import zmq

host = "ec2-13-58-201-148.us-east-2.compute.amazonaws.com"
port = "5001"

# Creates a socket instance
context = zmq.Context()
socket = context.socket(zmq.SUB)

# Binds the socket to a predefined port on localhost
socket.bind("tcp://*:{1}".format(host, port))

# Subscribes to the coffee maker and toaster topic
socket.subscribe("COFFEE MAKER")
socket.subscribe("TOASTER")

poller = zmq.Poller()
poller.register(socket, zmq.POLLIN)

while True:
    evts = dict(poller.poll(timeout=100))
    if socket in evts:
        topic = socket.recv_string()
        status = socket.recv_json()
        print(f"Topic: {topic} => {status}")
"""