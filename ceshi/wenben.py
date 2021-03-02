import os
import re
with open('C:/Users/HP/Desktop/文件记录/wenben.txt','r',encoding='utf-8') as f :
    lines=f.readlines()
    mat=r'.*foo.*'
    for line in lines:
        #a=re.findall(line,mat)
        pattern1 = re.compile(mat)
        res=pattern1.findall(line)
        s=[l for l in res if len(res)>0 ]
        print(s)


