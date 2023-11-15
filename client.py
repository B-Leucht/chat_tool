import socket
import sys
import threading

# get a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def receive():
    """Handles incoming messages"""
    while True:
        data = s.recv(1024).decode("utf-8")
        print(data)


if __name__ == "__main__":
    # ask user for their name and make sure it's not an empty string
    name = ""
    while name == "":
        name = input("Name: ")
    # connect the socket to the server
    s.connect(("localhost", 54321))
    # send name to server
    s.sendall(name.encode("utf-8")[:1024])
    # create a thread, that receives incoming messages
    r_thread = threading.Thread(target=receive)
    r_thread.start()
    # get user input and send it to the server
    while True:
        line = input()
        if line != "":
            s.sendall(line.encode("utf-8"))
