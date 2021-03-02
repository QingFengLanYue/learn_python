import pandas as pd
import os
import datetime
import sys
import getopt
#处理excel
def excel_deal(file_path,sheet_name,write_file):
    df=pd.read_excel(file_path,sheet_name=sheet_name,dtype='str')
    with open(write_file, 'w', encoding='UTF-8') as f:
        for num in range(len(df)):
            str_arry=df.loc[num].fillna('')
            if num < len(df)-1:
                f.write('!#~'.join(str(st) for st in str_arry)+'\n')
            else :
                f.write('!#~'.join(str(st) for st in str_arry) )



#解析出需要生成的文件名称和路径,拼接sheet name作为新的文件名
def file_name(file_path,sheet_name):
    write_file=os.path.splitext(file_path)[0]+'_'+sheet_name+'.txt'
    write_file=write_file.replace(' ','_')
    return write_file

#获取昨天的日期
def getYesterday():
    yesterday = datetime.date.today() + datetime.timedelta(-1)
    return yesterday
# 输出

def args_check(sheet_name,table_name):
    if(len(sheet_name)!=len(table_name)):
        print("传入参数错误！，请检查参数")


def help_info():
    '''
    帮助信息
    '''
    print('请输入参数：-t table_list -s sheet_list')



def main(file_path,sheet_name,table_name):
    #sheet 名字要和表的顺序保持一致
    yesterday=getYesterday()
    for sheet in range(len(sheet_name)):
        write_file = file_name(file_path, sheet_name[sheet])
        print('生成 ' + write_file)
        excel_deal(file_path, sheet_name[sheet], write_file)
        # print('执行入库命令：load data local inpath \''+write_file+'\' overwrite into table '+table_name[sheet]+ ' partition(dt=\'2019\')')
        print("执行入库命令：load data local inpath %s overwrite into table %s partition ( dt = %s ) ;" % (
            write_file, table_name[sheet], yesterday))




# if __name__ == '__main__':
#
#     opts,args = getopt.getopt(sys.argv[1:],'-h-f:-t:-s:')
# #print(opts)
#     for opt_name,opt_value in opts:
#         if opt_name in ('-h'):
#             help_info()
#
#         if opt_name in ('-t'):
#             table_name=eval(opt_value)
#             print(table_name)
#
#         if opt_name in ('-s'):
#             sheet_name=opt_value
#
#             sheet_name=eval(sheet_name)
#             print(sheet_name)
#
#         if opt_name in ('-f'):
#             file_path=opt_value
#
#             print(file_path)
#
#     main(file_path,sheet_name,table_name)