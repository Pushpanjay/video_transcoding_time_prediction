# csv operation

import csv

f=open('dataset.csv')
csv_f=csv.reader(f)
count=0
t=[]
train=[]
target=[]
for row in csv_f:
    if count==0:
        count+=1
        continue
    
    #t.append(float(row[0]))
    t.append(float(row[1])/100)
    t.append(float(row[2])/100)
    t.append(float(row[3])/1000)
    t.append(float(row[4])/10)
    #t.append(int(float(row[5])))
    #t.append(int(float(row[6])))
    t.append(float(row[7])/1000)
    t.append(float(row[8])/10)
    t.append(float(row[9])/100)
    t.append(float(row[10])/100)
    train.append(t);
    t=[]
    target.append([float(row[11])/1000])
    count+=1
    if count==10:
        break

print train
print target    
f.close()
    
