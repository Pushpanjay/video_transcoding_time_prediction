import csv

r = csv.reader(open("transcoding_mesurment.csv","rb"))

c = csv.writer(open("MYFILE.csv", "wb"))


count=0

for row in r:

	print row
	c.writerow(row)
	count+=1
	
	if count==1000:
		break

r.close()
c.close()
