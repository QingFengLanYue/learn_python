from optparse import OptionParser
import sys
'''optParser.parse_args() 剖析并返回一个字典和列表，
字典中的关键字是我们所有的add_option()函数中的dest参数值，
而对应的value值，是add_option()函数中的default的参数或者是
由用户传入optParser.parse_args()的参数
'''

optParser = OptionParser()  # 构造optionparser的对象
optParser.add_option('-f', '--file', action='store', type="string", dest='filename')
optParser.add_option("-v", "--vison", action="store_false", dest="verbose",
                     default='base', help="make lots of noise [default]")

args1 = ['-v', 'Hi!']
option, args = optParser.parse_args(args1)
print("option : ", option)
print("args : ", args)

fakeArgs = ['-f', 'file.txt', '-v', 'how are you', 'arg1', 'arg2']
op, ar = optParser.parse_args(fakeArgs)
print("op : ", op)
print("ar : ", ar)

fakeArgs1 = ['-f', 'file.txt', 'how are you', 'arg1', 'arg2']
op1, ar1 = optParser.parse_args(fakeArgs1)
print("op : ", op1)
print("ar : ", ar1)
print(op1.filename,op1.verbose,type(ar1),ar1[0])



if __name__ == '__main__':
    opt1 ,ar1 = optParser.parse_args(sys.argv[1:])
    print("----------------脚本传参----------------")
    print(opt1)
    print('filename is %s'%opt1.filename)
    print('vision is %s'  %opt1.verbose)
    print(ar1)
    print(sys.argv)