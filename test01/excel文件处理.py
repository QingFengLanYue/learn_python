from test01.文件差异比较 import dealExceldiff
import pandas as pd
# file1 = "D:/work2/test1.xlsx"
# file2 = "D:/work2/test2.xlsx"
# file_write = "D:/work2/test_diff.xlsx"
#
# # if __name__ == '__main__':
# #     dealExceldiff.deal_result(file1, file2, file_write)

file3 = "D:/work2/test.xlsx"
df=pd.read_excel(file3,sheet_name='a',index_col=0)
print(df)

writer = pd.ExcelWriter(file3)

df1 = pd.DataFrame([[1,2],['a','b'],[3,4]],columns=['id','name'])
df2 = pd.DataFrame(['b'])

df1.to_excel(writer, sheet_name='a')
df2.to_excel(writer, sheet_name='b')
writer.save()