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
    
    t.append(float(row[0]))
    t.append(int(float(row[1])))
    t.append(int(float(row[2])))
    t.append(int(float(row[3])))
    t.append(int(float(row[4])))
    t.append(int(float(row[5])))
    t.append(int(float(row[6])))
    t.append(int(float(row[7])))
    t.append(int(float(row[8])))
    t.append(int(float(row[9])))
    t.append(int(float(row[10])))
    train.append(t);
    t=[]
    target.append([float(row[11])])
    count+=1
    if count==10:
        break

print train
print target    
f.close()
    
