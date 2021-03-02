#Z字形转换
def convert(s,n):
    l1=[[] for j in range(n)]
    key=0
    flag=1
    for m in range(len(s)):

        l1[key].append(s[m])
        key += flag
        if key == n-1 or key == 0:
            flag *= -1
    result=list()
    for a in l1:
        result.extend(a)
    print(result)

    print(''.join(result))

convert("leetcodeisfiring",3)