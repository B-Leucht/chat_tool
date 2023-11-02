import socket
# get a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to my port so that it will accept connections from everywhere
s.bind(('', 54321))
s.listen(1)
# wait for incoming connection
conn, addr = s.accept()
# get the clients name and decode it
name = conn.recv(1024).decode('utf-8')

while True:
    data = conn.recv(1024)
    print(name+': '+data.decode('utf-8'))
