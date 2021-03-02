import re


with open('C:/Users/HP/Desktop/create.sql', 'r+', encoding='utf-8') as f:
    date = f.read()
    # print(date)
    regx1 = re.search(r'.*odc.*', date)
    regx2= re.findall('odc.*_inc',date)
    print(regx2)

m = re.match('foo', 'seafood') # no match 匹配失败
print(m)
m = re.search('foo', 'seafood') # use search() instead 改用 search()
print(m.group())