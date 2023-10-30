import socket
import sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 54321))

for line in sys.stdin:
    s.sendall(line.encode('utf-8'))
print("End.")