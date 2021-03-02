import re

def myAtoi(str: str) -> int:
    '''
        正则匹配，以n个空格开头，匹配到正负数字
    '''
    mathes = re.match('[ ]*([+-]?\d+)', str)
    if not mathes:
        print('0')
    ans = int(mathes.group(1))
    print(min(max(ans, -2 ** 31), 2 ** 31 - 1))

myAtoi('     -9888887a')