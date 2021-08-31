def romanToInt(s: str) -> int:
    n = 0
    m = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    for i in range(len(s)):
        if i < len(s) - 1 and m[s[i]] < m[s[i + 1]]:
            n -= m[s[i]]
        else:
            n += m[s[i]]
    return n


a = romanToInt('MMCMLXXXIV')
print(a)
