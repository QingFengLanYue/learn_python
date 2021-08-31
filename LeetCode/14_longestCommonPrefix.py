# 最长公共前缀，python直接按照acsii值进行排序的
def longestCommonPrefix(st: list) -> str:
    if not st:
        return ""
    str0 = min(st)
    str1 = max(st)
    print(str0, str1)

    s = ''
    for i in range(len(str0)):
        if str0[i] != str1[i]:
            s = str0[:i]
            break
    return s


a = longestCommonPrefix(["flower", "fllow", "flight"])
print(a)
