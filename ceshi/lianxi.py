import pandas as pd
test_file="D:/test/test1/user.txt"
xlsx_file="D:/test/test1/cs.xlsx"
with open(test_file,mode='r') as f :
    s=f.readlines()
    line1,line2=[],[]
    for s1 in s:
        name=s1.split(':')[0]
        passwd=s1.split(':')[1].replace('\n','')
        line1.append(name)
        line2.append(passwd)
    print(line1,line2)

xlsx=pd.read_excel(xlsx_file)
xlsx['用户']=line1
xlsx['密码']=line2
xlsx.to_excel(xlsx_file,index=None,sheet_name='user')
