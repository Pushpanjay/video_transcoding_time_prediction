# Routing python file will call server based on their availability
 
import random
import socket


#Task types 
class TaskType(object):

    #Constructor
    def __init__(self, period, release, execution, deadline, name):
        self.period    = period
        self.release   = release
        self.execution = execution
        self.deadline  = deadline
        self.name      = name.replace("\n", "")


class Server:


    def __init__(self,capacity,occ,port,name):
        self.capacity   = capacity
        self.port       = port
        self.name       = name.replace("\n", "")
        self.occupied   = occ
        self.available  = capacity-occ      # initially available is capacity as none of the slot has been used yet
        self.id         = int(random.random() * 10000)

    def avail(self):
        return self.available

    def port_num(self):
        return self.port

    def assign(self,time):
        if self.available >= time:       # weighted transcoding time is assigned to server
            self.occupied += time
            self.available -= time
            return True
        else:
            return False

    #Get name as Name + # + id ; Random id for every Server
    def get_unique_name(self):
        return str(self.name) + "#" + str(self.id)

        
def capacity_cmp(self, other):
    if self.available < other.available:
        return 1
    if self.available > other.available:
        return -1
    return 0



if __name__ == '__main__':
    
    host = 'localhost'  # '127.0.0.1' can also be used

    port1 = 9091    #For server1
    port2 = 9092    #For server2
    port3 = 9093    #For server3

    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #For server1
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #For server2
    sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #For server3
    
    #Connecting to socket
    #Connect takes tuple of host and port
    sock1.connect((host,port1))
    sock2.connect((host,port2))
    sock3.connect((host,port3))

    
    
    serverfile = open('server.txt')
    lines = serverfile.readlines()
    taskfile = open('test.txt')
    tlines = taskfile.readlines()

    server_s = []
    task_types = []


    
    for line in lines:
        line = line.split(' ')
        for i in range (0,3):
            line[i] = int(line[i])
        if len(line) == 4:
            name = line[3]
        elif len(line) == 3:
            name = 'Server'
        else:
            raise Exception('Invalid Server.txt file structure')
        if int(line[0])>0:
            server_s.append(Server(capacity=line[0], occ=line[1], port=line[2], name=name))

    for tline in tlines:
        tline = tline.split(' ')
        for i in range (0,4):
            tline[i] = int(tline[i])
        if len(tline) == 5:
            name = tline[4]
        elif len(tline) == 4:
            name = 'Task'
        else:
            raise Exception('Invalid tasks.txt file structure')
        if int(tline[0])>0:
            task_types.append(TaskType(period=tline[0], release=tline[1], execution=tline[2], deadline=tline[3], name=name))
        
      
    server_s = sorted(server_s, capacity_cmp)
    #print "Sorted"
    server_assign = server_s[0]

    

    for tline in task_types:
        for s in server_s:
            if s.available > server_assign.available:
                server_assign = s
            
                
        if(server_assign.assign(tline.execution)):
            print tline.name+" assigned to Server : "+server_assign.get_unique_name()


            msg = str(tline.period) +" "+ str(tline.release) +" "+ str(tline.execution) +" "+ str(tline.deadline) +" "+ tline.name
            msg += "\n"
            
            #port number of selected server
            port=server_assign.port_num()

            if(port == 9091):
                data = sock1.recv(1024)
                print data
                sock1.send('HI! I am client.'+msg)
            elif(port == 9092):
                data = sock2.recv(1024)
                print data
                sock2.send('HI! I am client.'+msg)
            else:
                data = sock3.recv(1024)
                print data
                sock3.send('HI! I am client.'+msg)



            '''
            #port = server_assign.port
            port=52046
            # Creating the socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #Connecting to socket
            sock.connect((host, port)) #connect takes tuple of host and port
            data = sock.recv(1024)
            print data
            msg = str(tline.period) +" "+ str(tline.release) +" "+ str(tline.execution) +" "+ str(tline.deadline) +" "+ tline.name
            msg += "\n"
            sock.send('HI! I am client.'+msg)
            sock.close()
            '''


            
        else:
            print "All the servers are busy please try after some time"

    sock1.close()
    sock2.close()
    sock3.close()
            
            
