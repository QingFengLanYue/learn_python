def minSubArrayLen(s: int, nums: list):
    l = len(nums)
    l1 = []
    m, k = 0, l
    for i in range(l):
        while sum(l1) > s:
            l1 = l1[1:]

        else:
            l1.append(nums[i])
            m = max(m, len(l1))
        k = min(m, k)
    print(k)


s = 7
nums = [2, 3, 1, 2, 4, 3]
minSubArrayLen(s, nums)


def minSubArrayLen1(s: int, nums) -> int:
    length = len(nums)
    i = 0
    j = 0
    min_len = float("inf")
    while j < length:
        if sum(nums[i:j + 1]) < s:
            j += 1
            continue
        if j - i < min_len:
            min_len = j - i + 1
        i += 1
    print(0 if len(nums) < min_len else min_len)


minSubArrayLen1(s, nums)


def maxsum(nums):
    max_pre = -float('inf')
    max_cur = -float('inf')
    for i in nums:
        max_cur = max(max_cur + i, i)
        max_pre = max(max_pre, max_cur)
    print(max_pre)


maxsum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
