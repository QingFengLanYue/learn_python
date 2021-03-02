def romanToInt( s: str) -> int:
    n=0
    a = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
    for i in range(len(s)):
        if i<len(s)-1 and a[s[i]]<a[s[i+1]] :
            n-=a[s[i]]
        else :
            n+=a[s[i]]
    print(n)

romanToInt('MMCMLXXXIV')