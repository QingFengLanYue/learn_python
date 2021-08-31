# 给定一个字符串 s，找到 s 中最长的回文子串。你可以假设 s 的最大长度为 1000。


def longestPalindrome(s):
    # dp[i][j] = true,if s[i] = s[j] ....
    # dp[0][len(s)-1]
    length = len(s)
    dp = [[0] * length for _ in range(length)]
    res = 0, 0  # 长度为1时
    for i in range(1, length):
        for j in range(length - i):
            if s[j] == s[j + i] and (j + 1 >= j + i - 1 or dp[j + 1][j + i - 1]):
                dp[j][j + i] = 1
                res = j, j + i
    left, right = res
    print(s[left: right + 1])


# longestPalindrome("cbababcbbd")


def longestPalindrome2(s):
    for i in range(len(s)):
        for l in range(i + 1):
            r = i - l
            temp = s[l:len(s) - r]
            if temp == temp[::-1]:
                print(temp)
    print('')


longestPalindrome2("cbababcbbd")
