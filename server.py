import socket
import threading

clients = []


def handle_client(c_socket):
    """handles a clients interaction with the server"""
    name = c_socket.recv(1024).decode("utf-8")
    clients.append((name, c_socket))
    while True:
        data = c_socket.recv(1024).decode("utf-8")
        print(name + ": " + data)


if __name__ == "__main__":
    # get a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to my port so that it will accept connections from everywhere
    s.bind(("", 54321))
    s.listen(1)
    while True:
        # wait for incoming connection
        c_socket, addr = s.accept()
        c_thread = threading.Thread(target=handle_client, args=(c_socket,))
        c_thread.start()
