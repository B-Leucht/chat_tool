import socket
import threading

# a set of all
client_sockets = set()
# get a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def handle_client(c_socket):
    """handles a clients interaction with the server"""
    # receive name from client
    try:
        name = c_socket.recv(1024).decode("utf-8")
    except ConnectionResetError:
        return
    # add socket to list of all sockets
    client_sockets.add(c_socket)
    while True:
        # receive data from client
        try:
            data = c_socket.recv(1024).decode("utf-8")
        except ConnectionResetError:
            print("User " + name + " disconnected")
            break
        if data != "": # make sure the message isn't an empty string
            # concatenate name with data
            message = name + ": " + data
            print(message)
            # duplicate the clients_sockets set, so it can be changed while iterating over it
            c_sockets = set(client_sockets)
            # broadcast message to all clients
            for sock in c_sockets:
                try:
                    # send message to client
                    sock.sendall(message.encode("utf-8"))
                except BrokenPipeError:
                    # remove socket from set if it can't be reached
                    client_sockets.remove(sock)


if __name__ == "__main__":
    # bind the socket to my port
    s.bind(("", 54321))
    s.listen(2)
    while True:
        # wait for incoming connection
        c_socket, addr = s.accept()
        # create thread for new client
        c_thread = threading.Thread(target=handle_client, args=(c_socket,))
        c_thread.start()
