# csv operation

import csv

f=open('dataset.csv')
csv_f=csv.reader(f)
count=0
train=[]
target=[]
for row in csv_f:
    if count==0:
        count+=1
        continue
    train.append(row[0:13])
    target.append(row[13])
    count+=1
    if count==10:
        break

print train
#print target
    
f.close()
    
