
#!usr/bin/python
from socket import *
 
host = 'localhost' # '127.0.0.1' can also be used
port = 52000
 
sock = socket()
#Connecting to socket
sock.connect((host, port)) #connect takes tuple of host and port
 
data = sock.recv(1024)
print data
sock.send('HI! I am client.')
 
sock.close()
