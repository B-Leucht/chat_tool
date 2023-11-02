import socket
import sys
# ask user for their name
name = input('Name: ')
# get a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect the socket to the server
s.connect(('localhost', 54321))
# send name to server
s.sendall((name).encode('utf-8'))
# iterate over stdin and send the encoded strings to server
for line in sys.stdin:
    s.sendall(line.encode('utf-8'))
print("End.")