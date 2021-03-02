import getopt
import sys

def help_info():
    '''
    帮助信息
    '''
    print('请输入参数：-t table_list -s sheet_list')


opts,args = getopt.getopt(sys.argv[1:],'-h-f:-t:-s:','a')
#print(opts)
opts,args = getopt.getopt(sys.argv[1:],'-h-f:-t:-s:')
#print(opts)
for opt_name,opt_value in opts:
    if opt_name in ('-h'):
        help_info()

    if opt_name in ('-t'):
        table_name=eval(opt_value)
        print(table_name)

    if opt_name in ('-s'):
        sheet_name=opt_value

        sheet_name=eval(sheet_name)
        print(sheet_name)

    if opt_name in ('-f'):
        file_path=opt_value

        print(file_path)


