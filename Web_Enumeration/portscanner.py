import socket
import threading
import sys
from queue import Queue

try:
    a1 = sys.argv[1]
    if a1.startswith('https://'):
        a1 = a1[8:]
    else:
        a1 = a1
except IndexError:
    # print(e)
    a1 = 'www.google.com'

target = a1
# target = '10.1.8.27'


def portscan(port):
    # print("port p pp p p pp p pp ")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        # print(port, "hello")
        return True
    except OSError:
        # print(port, "hello")
        return False


# noinspection PyShadowingNames
def fill_queue(port_list):
    # print("fill q")
    for port in port_list:
        q.put(port)
        # print(port)


def worker():
    while not q.empty():
        port = q.get()
        # print(port)
        if portscan(port):
            print("port", port, "is open")
            open_ports.append(port)


q = Queue()
open_ports = []
port_list = []


def fill_port_list(from1, to1):
    global port_list
    for i in range(from1, to1):
        port_list.append(i)


# fill_port_list(2, 81)
# fill_queue(port_list)
thread_list = []
# print(port_list)


def portscanner(thread1, a, b):
    global thread_list
    fill_port_list(a, b)
    fill_queue(port_list)
    print('\n\n Starting Port Scanning...\n\n ')
    print(f"thread={thread1}")
    print(f" target={target}")
    for i in range(1, thread1):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()
    thread_list = []
    print(f"open ports:{open_ports}")
    with open("result/port.txt", 'w') as f:
        f.write(f"open ports:{open_ports}")

    return 0


if __name__ == '__main__':
    portscanner(111, 3, 99)

