import socket

if __name__ == "__main__":
    # ask user for their name
    name = input("Name: ")
    # get a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect the socket to the server
    s.connect(("localhost", 54321))
    # send name to server
    s.sendall(name.encode("utf-8"))
    while True:
        line = input("You: ")
        s.sendall(line.encode("utf-8"))
