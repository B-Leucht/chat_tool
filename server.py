import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 54321))
s.listen(1)
conn, addr = s.accept()
while True:
    data = conn.recv(1024)
    print(data)