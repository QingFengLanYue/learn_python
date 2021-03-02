class Solution:


    def threeSum(nums: list) -> list:
        nums=sorted(nums)
        list1=[]
        for i in range(len(nums)-2):
            if nums[i] > 0 :
                break
            # elif nums[i] == nums[i+1]:
            #     continue
            else:
                j,k=i+1,len(nums)-1
                while j < k :

                    s = nums[i] + nums[j] + nums[k]

                    if s==0:
                        print(nums[i],nums[j],nums[k])
                        j=j+1
                        k=len(nums)-1
                    elif s< 0  :
                        while nums[j] == nums[j + 1]:
                            j+=1
                        j+=1
                    else :
                        # while nums[k] == nums[k - 1]:
                        #     k-=1
                        k-=1







nums = [-1, 0, 1, 2, -2, -1, -4]
nu=Solution
nu.threeSum(nums)