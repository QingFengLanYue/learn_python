
#最长公共前缀，python直接按照acsii值进行排序的
def longestCommonPrefix(strs: list) -> str:
    if not strs: return ""
    str0 = min(strs)
    str1 = max(strs)
    for i in range(len(str0)):
        if str0[i] != str1[i]:
            s = str0[:i]
            break
    print(s)


longestCommonPrefix(["flower","falow","flight"])