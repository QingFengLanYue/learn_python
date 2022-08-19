import time
from typing import List
from tqdm import tqdm
from itertools import chain
from zipfile import ZipFile
from rarfile import RarFile

start = time.time()

# chr(97) -> 'a' 这个变量保存了密码包含的字符集
# dictionaries = [chr(i) for i in
#                 chain(range(97, 123),    # a - z
#                       range(65, 91),    # A - Z
#                       range(48, 58))]    # 0 - 9
#
# dictionaries.extend(['.com', 'www.'])    # 添加自定义的字符集

dictionaries = list('123456970jJIAXQiasxq')
file_name = 'C:/Users/xiqiang.jia/Desktop/杂项/pojie.rar'


def all_passwd(dictionaries: List[str], maxlen: int):
    # 返回由 dictionaries 中字符组成的所有长度为 maxlen 的字符串

    def helper(temp: list, start: int, n: int):
        # 辅助函数，是个生成器
        if start == n:  # 达到递归出口
            yield ''.join(temp)
            return
        for t in dictionaries:
            temp[start] = t  # 在每个位置
            yield from helper(temp, start + 1, n)

    yield from helper([0] * maxlen, 0, maxlen)


if file_name.endswith('.zip'):
    fp = ZipFile(file_name, 'r')
elif file_name.endswith('.rar'):
    fp = RarFile(file_name, 'r')


def extract(fp, pwd: str) -> bool:
    try:
        # print(pwd)
        fp.extractall(path='.', pwd=pwd.encode('utf-8'))
        now = time.time()
        print(f"Password is: {pwd}")
        return True
    except Exception:
        return False
    # 用 bool 类型的返回值告诉主程序是否破解成功 (意思就是返回 True 了以后就停止)


lengths = [3]  # 密码长度
total = sum(len(dictionaries) ** k for k in lengths)  # 密码总数

for pwd in tqdm(chain.from_iterable(all_passwd(dictionaries, maxlen) for maxlen in lengths), total=total):
    if extract(fp, pwd):  # 记得extract函数返回的是bool类型的哦
        break
