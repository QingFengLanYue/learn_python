import  pandas as pd
import  numpy as np
def other(sta):
    list_type=[0,0,0,0,0,0]
    if sta=='AMEX TLS':
        list_type[0]=1
    elif sta=='Ensemble  Signature':
        list_type[1]=1
    elif sta=='The Luxury Circle':
        list_type[2]=1
    elif sta=='Travel Leaders Grou':
        list_type[3]=1
    elif sta=='Traveler Made':
        list_type[4]=1
    elif sta=='Virtuoso':
        list_type[5]=1
    return list_type


a={'id':[1,2,3,4,5,6],
   'name':['AMEX TLS','Ensemble  Signature','The Luxury Circle','Travel Leaders Grou','Traveler Made','Virtuoso']
   }
df=pd.DataFrame(a)

col1=df['id']
col2=df['name']
for is_type in df['name'].values:
    type1=other(is_type)
    print(type1)
    x = np.empty(shape=[0, 6],dtype=int)
    #x = np.append(x,type1, axis=0)

    # print(type1)
    # x = np.append(type1,axis=0)    # print(s)

x=np.empty(shape=[0,4],dtype=int)
print(x)
x=np.append(x,[[1,2,3,4]],axis=0)
x=np.append(x,[[5,6,7,8]],axis=0)
print(x)

#print(x)
#
#
# def towFind(s,key):
#     low=0
#     hight=len(s)-1
#     i=0
#     while low <= hight :
#         middle = (hight+low)//2
#         mid=s[middle]
#         i+=1
#         if mid==key :
#             print(mid,i)
#             break
#         if key > mid:
#             low=middle+1
#         else:
#             hight=middle-1
#
#
# s=[1,3,4,6,13,18,27,38,99]
# key=18
# towFind(s,key)
#
#
# def reser_num(num):
#     num=str(num)
#     l=len(num)
#     n=0
#     for i in range(l):
#         l0=pow(10,i)
#         l1=int(num[i])
#         n+=l0*l1
#     print(n)
# reser_num(1656823099999950)
#
#
# import re
# def myAtoi(str: str) -> int:
#     mathes = re.match('[ ]*([+-]?\d+)', str)
#     if not mathes:
#         print('0')
#     ans = int(mathes.group(1))
#     print(min(max(ans, -2 ** 31), 2 ** 31 - 1))
#
# myAtoi('     +9888888888888888887')
#

#
# def twoFind(nums,s):
#     l=len(nums)
#     low,height=0,l-1
#     i=0
#     while low <= height :
#         i+=1
#         middle=(low+height)//2
#         mid=nums[middle]
#         if mid==s:
#             print (middle,s)
#             print (i)
#             break
#         if mid < s:
#             low=middle+1
#         else:
#             height=middle-1
#
# nums=[1,3,4,6,13,18,27,38,99]
# s=18
# twoFind(nums,s)
#
# def Binery(l, key):
#     hight = len(l)-0
#     lower = 0
#     while lower <= hight:
#         middle = (lower + hight) // 2
#         mid = l[middle]
#         if mid == key:
#             print(mid)
#             break
#         elif mid < key:
#             lower = middle + 1
#
#         else:
#             hight = middle - 1
#
# if __name__=='__main__':
#     l = [1, 2, 5, 7, 12, 15, 26, 67, 99]
#     key = 27
#     Binery(l, key)

