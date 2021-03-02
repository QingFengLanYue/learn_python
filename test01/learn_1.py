def Binry(l,key):
    low,hight,mid=0,len(l)-1,0
    i=0
    while low <= hight:
        i+=1
        mid=(low+hight)//2
        s=l[mid]
        if s==key:
            print(s,i)
            break
        if s < key :
            low=mid+1
        else :
            hight=mid-1

l=[1,3,5,7,8,12,19,20]
key=3

Binry(l,key)
