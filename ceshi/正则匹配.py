import re
patter=re.compile('.*python.*')
result=patter.search('hello python,good python')
print(result.group())
print(re.match('python','python hello').group())
print(re.search('python','lpython hello').group())


# print(re.findall('python','lpython hello,a python'))
# print(re.sub('aa','b','saacbaaa',1))
# print(re.split('a','nnaya,ah'))
print(re.search(r'(y)th[n-z]{2,}(aa)','plythonaa').group(0,1,2))