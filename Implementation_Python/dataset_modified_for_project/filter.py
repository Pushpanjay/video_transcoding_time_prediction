import csv
path1='MYFILE.csv'
path2='dataset.csv'
outdata = []
input_file = open(path1,'rb')
output = open (path2,'wb')

reader=csv.reader(input_file, delimiter=',')
writer=csv.writer(output,delimiter=',')
for row in reader:
    #print("row: ", row)
    outdata.append([row[1], row[3], row[4], row[5], row[6], row[10], row[14], row[16], row[17], row[18], row[19], row[21]])
print(outdata)
writer.writerows(outdata)
