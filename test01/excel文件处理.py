from test01.文件差异比较 import DealExcelDiff

if __name__ == '__main__':
    file1 = "D:/工作/room cube/新版room cube/Room Cube优先级较高的字段V1.2.xlsx"
    file2 = "D:/工作/room cube/新版room cube/Room Cube优先级较高的字段V1.3.xlsx"
    file_write = "D:/work2/test_diff.xlsx"
    primary_key = '需求字段'
    a = DealExcelDiff(primary_key, file1, file2, file_write)
    a.deal_result()

# file3 = "D:/work2/test.xlsx"
# df=pd.read_excel(file3,sheet_name='a',index_col=0)
# print(df)
#
# writer = pd.ExcelWriter(file3)
#
# df1 = pd.DataFrame([[1,2],['a','b'],[3,4]],columns=['id','name'])
# df2 = pd.DataFrame(['b'])
#
# df1.to_excel(writer, sheet_name='a')
# df2.to_excel(writer, sheet_name='b')
# writer.save()
