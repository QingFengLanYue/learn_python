import os
f=open('C:/Users/HP/Desktop/ceshi.txt','r')
#print(f.read())
#data1=f.readline()
#data2=f.readline()
#
count=0
for line in f:
    if count==3:
     line=''.join([line.strip(),'end 3'])
    print(line.strip())
count+=1