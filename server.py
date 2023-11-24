import socket
import threading

# a dictionary to store all client sockets
clients = dict()

def handle_client(c_socket):
    """handles a client's interaction with the server"""
    name = ""
    while True:
        try:
            # receive name from the client
            name = c_socket.recv(1024).decode("utf-8")
            if name in clients:
                c_socket.sendall("name_taken".encode("utf-8"))
            else:
                c_socket.sendall("name_valid".encode("utf-8"))
                break
        except ConnectionResetError:
            return

    # add the socket to the dictionary of all sockets
    clients[name] = c_socket
    users = "c" + " ".join(clients.keys())
    broadcast(users)

    while True:
        try:
            # receive data from the client
            data = c_socket.recv(1024).decode("utf-8")
        except ConnectionResetError:
            # handle client disconnection
            remove_client(name)
            break

        if data != "":
            match data[0]:
                # data is a text message
                case "t":
                    message = "t" + name + ": " + data[1:]
                    broadcast(message)
                # c means client has disconnected
                case "c":
                    remove_client(name)
                    break

def remove_client(name):
    clients.pop(name)
    users = "c" + " ".join(clients.keys())
    broadcast(users)

def broadcast(message):
    print(message)
    # duplicate the clients dictionary, so it can be changed while iterating over it
    c_sockets = dict(clients)
    # broadcast the message to all clients
    for name, sock in c_sockets.items():
        try:
            # send the message to the client
            sock.sendall(message.encode("utf-8"))
        except BrokenPipeError:
            # remove the socket from the dictionary if it can't be reached
            remove_client(name)

if __name__ == "__main__":
    # get a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to my port
    s.bind(("", 54321))
    s.listen(2)
    while True:
        # wait for an incoming connection
        c_socket, addr = s.accept()
        # create a thread for the new client
        c_thread = threading.Thread(target=handle_client, args=(c_socket,))
        c_thread.start()
