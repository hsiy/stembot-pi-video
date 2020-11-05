import zmq
import socket
import threading
import argparse

OFFSET = 10000
STARTING_PORT = 10000
AVAILABLE_PORTS = 10000
AVAILABLE_PORTS = [*range(STARTING_PORT, STARTING_PORT + AVAILABLE_PORTS, 1)]
INITIALIZE_CONNECTION_PORT = 5050
connections = dict()
print_lock = threading.Lock()
dict_lock = threading.Lock()

option_parse = argparse.ArgumentParser(description="Set up of EC2 server")
option_parse.add_argument("--debug", type=bool, default=False, help="Shows debugging information", choices=[True, False])
option_parse.add_argument("--data", type=bool, default=True, help="blocks data temporarily for ec2", choices=[True, False])

args = vars(option_parse.parse_args())


def find_new_port():
    new_port = STARTING_PORT
    while True:
        if new_port in AVAILABLE_PORTS:
            AVAILABLE_PORTS.remove(new_port)
            break
        new_port += 1
    return new_port


def add_back_port(port):
    AVAILABLE_PORTS.append(port)
    AVAILABLE_PORTS.sort()


def thread_timer_freeup(args):
    print_lock.acquire()
    print("Releasing connection: ")
    print_lock.release()
    return


def thread_function(connection, ip, port):
    
    if args["debug"]:
        print_lock.acquire()
        print("IP: ", ip, "Port: ", port)
        print_lock.release()

    dict_lock.acquire()
    new_port = find_new_port()
    dict_lock.release()

    connection_name = ""
    while True:
        data = connection.recv(8)
        if len(data) <= 0:
            break
        connection_name += data.decode("utf-8")
    
    connection.sendall(str(new_port).encode("utf-8"))
    connection.shutdown(socket.SHUT_WR)
    connection.close()

    if args["debug"]:
        print_lock.acquire()
        print("The port: {0} will be used for the connection: {1}".format(new_port, connection_name))
        print_lock.release()

    dict_lock.acquire()
    connections[connection_name] = dict()
    connections[connection_name]["port"] = new_port
    connections[connection_name]["active"] = True
    dict_lock.release()

    # receive from pi
    context_pi = zmq.Context()
    pi_socket = context_pi.socket(zmq.PAIR)
    pi_socket.set_hwm(1)
    pi_socket.bind("tcp://*:%s" % connections[connection_name]["port"])

    # send to unity
    context_send = zmq.Context()
    socket_send = context_send.socket(zmq.PUB)
    socket_send.set_hwm(1)
    socket_send.bind("tcp://*:%s" % (connections[connection_name]["port"] + OFFSET))

    timer = None
    from time import sleep
    while connections[connection_name]["active"]:
        #timer = threading.Timer(10, thread_timer_freeup, args=[]).start()
        if args["debug"] and False:
            print_lock.acquire()
            print("Sent frame for: {0} number: {1}".format(connection_name, count_frame))
            print_lock.release()
            count_frame = (count_frame + 1) % 100
        
        if args["data"]:
            msg = pi_socket.recv()
            socket_send.send(msg)
        else:
            sleep(.1)
        #timer.cancel()
    return


#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as inc_sock:
try:
    if args["debug"]:
        print_lock.acquire()
        print("Starting EC2 Server.")
        print_lock.release()

    inc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    inc_sock.bind((socket.gethostbyname(socket.gethostname()), INITIALIZE_CONNECTION_PORT))
    inc_sock.listen(5)
    while True:
        connection, address = inc_sock.accept()
        threading.Thread(target=thread_function, args=(connection, address[0], address[1])).start()
finally:
    inc_sock.close()
