import socket
import sys
# ask user for their name
name = input('Name: ')
# get a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect the socket to the port and local host
s.connect(('localhost', 54321))
# send name to server
s.sendall((name+' ist mit dem Server verbunden').encode('utf-8'))
for line in sys.stdin:
    s.sendall(line.encode('utf-8'))
print("End.")