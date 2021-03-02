#encoding=utf-8
a=[6,1,2,5,4,3,9]
# j=0
# while j < len(a):
#     i=0
#     while i < len(a)-1:
#         if a[i]<a[i+1]:
#             a[i],a[i+1]=a[i+1],a[i]
#             #print(a)
#         i=i+1
#     j=j+1
#     #print(j)
# print(a)
#冒泡排序
def maopoSort(a):
    for j in range(len(a)):
        for i in range(len(a)-1):
            if a[i]<a[i+1]:
                a[i],a[i+1]=a[i+1],a[i]
    return a

#选择排序
def selectionSort(nums):
    for i in range(len(nums) - 1):  # 遍历 len(nums)-1 次
        maxIndex = i
        for j in range(i + 1, len(nums)):
            if nums[j] > nums[maxIndex]:  # 更新最大值索引
                maxIndex = j
        nums[i], nums[maxIndex] = nums[maxIndex], nums[i] # 把最大数交换到前面
    return nums

#插入排序

def charuSort(num):
    for i in range(len(num)-1):
        nu,index=num[i+1],i
        while nu > num[index] and index >= 0:
            num[index+1]=num[index]
            index-=1

        num[index+1] = nu
    return num



#s=selectionSort(a)
#s=maopoSort(a)
s=charuSort(a)
print(s)