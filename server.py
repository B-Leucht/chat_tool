import socket
import threading

c_sockets = []
# get a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def handle_client(c_socket):
    """handles a clients interaction with the server"""
    # receive name from client
    name = c_socket.recv(1024).decode("utf-8")
    # add socket to list of all sockets
    c_sockets.append(c_socket)
    while True:
        #receive data from client
        data = c_socket.recv(1024).decode("utf-8")
        #concatenate name with data
        message = name + ": " + data
        print(message)
        #broadcast message to all clients
        for sock in c_sockets:
            sock.sendall(message.encode("utf-8"))


if __name__ == "__main__":
    # bind the socket to my port so that it will accept connections from everywhere
    s.bind(("", 54321))
    s.listen(1)
    while True:
        # wait for incoming connection
        c_socket, addr = s.accept()
        # create thread for new client 
        c_thread = threading.Thread(target=handle_client, args=(c_socket,))
        c_thread.start()
