import socket
import threading

# a set of all client sockets
client_sockets = set()

def handle_client(c_socket):
    """handles a clients interaction with the server"""
    # receive name from client
    try:
        name = c_socket.recv(1024).decode("utf-8")
    except ConnectionResetError:
        return
    # add socket to list of all sockets
    client_sockets.add(c_socket)
    message = "User " + name + " connected"
    broadcast(message)
    while True:
        # receive data from client
        try:
            data = c_socket.recv(1024).decode("utf-8")
        except ConnectionResetError:
            message = "User " + name + " disconnected"
            broadcast(message)
            break
        match data[0]: 
            case "t":# concatenate name with data
                message = name + ": " + data[1:]
                broadcast(message)
            case "c":
                message = "User " + name + " disconnected"
                client_sockets.remove(c_socket)
                broadcast(message)

def broadcast(message):
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
    # get a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    # bind the socket to my port
    s.bind(("", 54321))
    s.listen(2)
    while True:
        # wait for incoming connection
        c_socket, addr = s.accept()
        # create thread for new client
        c_thread = threading.Thread(target=handle_client, args=(c_socket,))
        c_thread.start()
