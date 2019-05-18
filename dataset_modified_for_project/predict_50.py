import csv

r = csv.reader(open("transcoding_mesurment.csv","rb"))

c = csv.writer(open("predict_50.csv", "wb"))


count=0

for row in r:
        if(count<=1000):
                count+=1
                continue

        print row
        c.writerow(row)
        count+=1
        
        if count==1050:
                break

r.close()
c.close()
