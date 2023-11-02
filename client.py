import socket
import sys
name = input('Name: ')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 54321))
s.sendall(name+' ist mit dem Server verbunden').encode('utf-8'))
for line in sys.stdin:
    s.sendall(line.encode('utf-8'))
print("End.")