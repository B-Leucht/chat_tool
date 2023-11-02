import socket
# get a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to my port so that it will accept connections from everywhere
s.bind(('', 54321))
s.listen(1)
#wait for incoming connection
conn, addr = s.accept()

while True:
    data = conn.recv(1024)
    print(data.decode('utf-8'))
