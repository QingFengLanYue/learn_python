# 给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度

def lengthOfLongestSubstring(s):
    # 哈希集合，记录每个字符是否出现过
    occ = set()
    n = len(s)
    # 右指针，初始值为 -1，相当于我们在字符串的左边界的左侧，还没有开始移动
    rk, ans = -1, 0
    for i in range(n):
        if i != 0:
            # 左指针向右移动一格，移除一个字符
            occ.remove(s[i - 1])
        while rk + 1 < n and s[rk + 1] not in occ:
            # 不断地移动右指针
            occ.add(s[rk + 1])
            rk += 1
        # 第 i 到 rk 个字符是一个极长的无重复字符子串
        ans = max(ans, rk - i + 1)
    print(ans)


# lengthOfLongestSubstring('asacadaasac')

def lengthOfLongestSubstring2(s):
    k = 0
    l1 = []
    for i in range(1, len(s)):
        s1 = s[i - 1:i]
        if s1 not in l1:
            l1.append(s1)
            i += 1

        else:
            num = l1.index(s1)
            l1 = l1[num + 1:]
            l1.append(s1)
            i += 1

        k = max(len(l1), k)
    print(k)


# lengthOfLongestSubstring2('abcarbcbb')


def lengthOfLongestSubstring3(s):
    k = 0
    l1 = []

    for i in range(len(s)):
        s1 = s[i]
        if s1 not in l1:
            l1.append(s1)

        else:
            num = l1.index(s1)
            l1 = l1[num + 1:]
            l1.append(s1)
        print(l1)
        k = max(len(l1), k)
    print(k)


# lengthOfLongestSubstring3("abcaarcabnbcbb")


def lengthOfLongestSubstring4(s):
    k = 0
    l1 = []

    for i in range(len(s)):
        s1 = s[i]
        if s1 in l1:
            num = l1.index(s1)
            l1 = l1[num + 1:]

        l1.append(s1)
        print(l1)
        k = max(len(l1), k)
    print(k)


lengthOfLongestSubstring4("abcaarcabnbcbb")
