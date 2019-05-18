#!/usr/bin/python
 
# Import all from module socket
from socket import *
 
# Defining server address and port
host = ''  #'localhost' or '127.0.0.1' or '' are all same
port = 52000 #Use port > 1024, below it all are reserved
 
#Creating socket object
sock = socket()
#Binding socket to a address. bind() takes tuple of host and port.
sock.bind((host, port))
#Listening at the address
sock.listen(5) #5 denotes the number of clients can queue
 
#Accepting incoming connections
conn, addr = sock.accept()
 
#Sending message to connected client
conn.send('Hi! I am server') #send only takes string
#Receiving from client
data = conn.recv(1024) # 1024 stands for bytes of data to be received
print data
 
#Closing connections
conn.close()
sock.close()
