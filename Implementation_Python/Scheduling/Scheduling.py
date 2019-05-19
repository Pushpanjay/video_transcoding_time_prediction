
# Efficient Scheduling of transcoding time of video

import string
import random
from prime import lcm



#A task instance
class TaskIns(object):

     #Constructor 
    def __init__(self, start, end, priority, name):
        self.start    = start
        self.end      = end
        self.usage    = 0
        self.priority = priority
        self.name     = name.replace("\n", "")
        self.id = int(random.random() * 10000)

    #Allow an instance to use the cpu (periodic)
    def use(self, usage):
        self.usage += usage
        if self.usage >= self.end - self.start:
            return True
        return False
    
    #Default representation
    '''
    def __repr__(self):
        return str(self.name) + "#" + str(self.id) + " - start: " + str(self.start) + " priority: " + str(self.priority) + budget_text   # return a printable representation of the object
        '''

    #Get name as Name#id ; id is generated randomly
    def get_unique_name(self):
        return str(self.name) + "#" + str(self.id)

    

#Task types 
class TaskType(object):

    #Constructor
    def __init__(self, period, release, execution, deadline, name):
        self.period    = period
        self.release   = release
        self.execution = execution
        self.deadline  = deadline
        self.name      = name

#Priority comparison
def priority_cmp(one, other):
    if one.priority < other.priority:
        return -1
    elif one.priority > other.priority:
        return 1
    return 0


#Deadline comparison
def tasktype_cmp(self, other):
    if self.deadline < other.deadline:
        return -1
    if self.deadline > other.deadline:
        return 1
    return 0



if __name__ == '__main__':
    #Variables
    html_color = { 'Task1':'red', 'Task2':'blue', 'Task3':'green', 'Task4':'aqua', 'Task5':'coral', 'Empty':'grey', 'Finish':'black'}
    #taskfile = open('tasks.txt')
    taskfile = open('test1.txt')
    lines = taskfile.readlines()
    task_types = []     # list of tasks object
    tasks = []          # list of tasks in queue for execution
    tot_period = []

    #Allocate task types
    for line in lines:
        line = line.split(' ')  
        for i in range (0,4):
            line[i] = int(line[i])
        if len(line) == 5:
            name = line[4]
        elif len(line) == 4:
            name = 'Task'
        else:
            raise Exception('Invalid tasks.txt file structure')
        if int(line[0])>0:
            task_types.append(TaskType(period=line[0], release=line[1], execution=line[2], deadline=line[3], name=name))
        
    #Calculate tot_period i.e. lcm of the periods of all the tasks
    for task_type in task_types:
        tot_period.append(task_type.period)
    tot_period = lcm(tot_period)         #contains the lcm of all the task's period

    #Sort tasks based on deadline in ascending order
    task_types = sorted(task_types, tasktype_cmp)  #tasktype_cmp is a custom function return 1 or -1 or 0 depending on the deadline of the other task with respect to 1st task


    #Create task instances 
    for i in xrange(0, tot_period):
        for task_type in task_types:        # task_types is a list of objects i.e.. array of Task and is sorted now accdng to deadline
            if  (i - task_type.release) % task_type.period == 0 and i >= task_type.release:    # when then period of a task start(i.e..when i-release_time is multiple of  period) then it will be perfectly divided by it's period and hence remainder 0 then if condition will be satisfied
                start = i
                end = start + task_type.execution   
                priority = start + task_type.deadline
                tasks.append(TaskIns(start=start, end=end, priority=priority, name=task_type.name))

    #Html output start
    html = "<!DOCTYPE html><html><head><title>Dynamic Scheduling of Transcoding time</title></head><body>"
    html += '<br /><br /><h1 style="font-weight: 900; text-align: center; color: rgb(0,0,0);">Jaypee Institute of Information Technology</h1>'
    html += '<h2 style="font-weight: 900; text-align: center; color: rgb(0,0,0);">Major Project</h2>'
    html += '<h2 style="font-weight: 900; text-align: center; color: rgb(0,0,0);">Dynamic Scheduling of Transcoding time for Optimal Performance</h1><br /><br />'
    
    #Check utilization
    utilization = 0
    for task_type in task_types:
        utilization += float(task_type.execution) / float(task_type.period)  # Formula for utilization : U= Summation(ei/pi)
    if utilization > 1:         # Utilization Bound : summation(Ui)<=1  Liu and Laylan's Condition
        print 'Utilization error!'
        html += '<br /><br />Utilization error!<br /><br />'

    #Simulate clock
    clock_step = 1      # just to get a reference of time for various parameters (execution time, peroid, deadline..etc..)
    for i in xrange(0, tot_period, clock_step):
        #Fetch possible tasks that can use cpu and sort by priority
        possible = []
        for t in tasks:         # possible list has tasks accdng to start time of various tasks 
            if t.start <= i:
                possible.append(t)      #tasks with start time less than i are appended in possible list for execution 
        possible = sorted(possible, priority_cmp)       # Sorted in terms of priority i.e in term of deadline in ascending order

        #Select task with highest priority
        if len(possible) > 0:       #if possible as any elements
            on_cpu = possible[0]     #on_cpu contains currently assigned task
            print on_cpu.get_unique_name() , " uses the processor. " ,      # get_unique_name is a function generates unique task name by combininf task name + # + random number
            #html += '<div style="align: "center"">'
            html += '<div style="float: left; text-align: center; width: 110px; height: 20px; background-color:' + html_color[on_cpu.name] + ';">' + on_cpu.get_unique_name() + '</div>'
            if on_cpu.use(clock_step):      # if the usage of task is complete..i.e it's execution time is over..then it is removed from the list
                tasks.remove(on_cpu)        # use function is used to compare the execution time and the time used by the task
                html += '<div style="float: left; text-align: center; width: 10px; height: 20px; background-color:' + html_color['Finish'] + ';"></div>'
                print "Finish!" ,
        else:
            print 'No task uses the processor. '
            html += '<div style="float: left; text-align: center; width: 110px; height: 20px; background-color:' + html_color['Empty'] + ';">Empty</div>'
        print "\n"
    #html += '</div>'
    #Print remaining periodic tasks
    html += "<br /><br />"
    for p in tasks:         # all the tasks which gets executed are removed from the tasks list bt those which are still left can't be executed further due to out of range from the tot_period(lcm of periods of all the task)
        print p.get_unique_name() + " is dropped due to overload!"
        html += "<p>" + p.get_unique_name() + " is dropped due to overload!</p>"

    #Html output end
    html += "</body></html>"
    output = open('output.html', 'w')
    output.write(html)
    output.close()
