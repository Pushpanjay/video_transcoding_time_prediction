
import socket

TCP_IP = 'localhost'
TCP_PORT = 9002
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

filename='test.txt'
f = open(filename,'rb')

# 26th may...

while True:
    l=f.read(BUFFER_SIZE)
    while(l):
        s.send(l)
        l=f.read(BUFFER_SIZE)
    if not l:
        f.close()
        s.close()
        break


'''
with open('server1.txt', 'wb') as f:
    print 'file opened'
    while True:
        #print('receiving data...')
        data = s.recv(BUFFER_SIZE)
        print('data=%s', (data))
        if not data:
            f.close()
            print 'file close()'
            break
        # write data to a file
        f.write(data)
'''

#print('Successfully get the file')
#s.close()
print('connection closed')
