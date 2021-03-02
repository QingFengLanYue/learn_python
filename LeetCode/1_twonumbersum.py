# 给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
# 你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。
#
#  
#
# 示例:
#
# 给定 nums = [2, 7, 11, 15], target = 9
#
# 因为 nums[0] + nums[1] = 2 + 7 = 9
# 所以返回 [0, 1]

nums = [2, 3, 6, 7, 11, 15]
target = 9

def numbersum1(nums,target):
    d={}

    for i,value in enumerate(nums):
        d[value]=i
    for j,key in enumerate(nums):
        k=d.get(target-key)
        if k is not None and k != j and k > j :
            print(j,k)

    #print(d.get(7))


numbersum1(nums,target)


def numbersum2(nums,target):
    for i in range(len(nums)):
        for j in range(i+1,len(nums)):
            if nums[i] + nums[j] == target:
                print(i,j)

numbersum2(nums,target)


def numbersum3(nums,target):
    for i in range(len(nums)):
        tmp=nums[i+1:]
        num=target-nums[i]
        if num in tmp:
            j = nums.index(num)
            print(i,j)


numbersum3(nums,target)