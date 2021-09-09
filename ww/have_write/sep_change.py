import os
import sys
from optparse import OptionParser
import pandas as pd


def parse_args(arg):
    opt_parser = OptionParser()
    opt_parser.add_option('--old_file', action='store', type='string', dest='old_file')
    opt_parser.add_option('--chunksize', action='store', type='int', dest='chunksize', default=10000)
    opt_parser.add_option('--from_sep', action='store', type='string', dest='from_sep', default=',')
    opt_parser.add_option('--to_sep', action='store', type='string', dest='to_sep')
    opt_parser.add_option('--header', action='store_true', dest='header', default=False, help='if need header')
    option, args = opt_parser.parse_args(arg)
    return option


def write_col(old_file, new_file, from_sep, to_sep):
    col = pd.read_csv(old_file, sep=from_sep, nrows=0, encoding='utf-8', engine='python')
    col = [col for col in col.columns]
    col = to_sep.join(col)
    with open(new_file, 'w', encoding='utf-8') as w:
        w.writelines(col + '\n')


def write_data(old_file, new_file, from_sep, to_sep, chunksize):
    try:
        df = pd.read_csv(old_file, sep=from_sep, dtype=str, chunksize=chunksize, encoding='utf-8', engine='python')
        for rs in df:
            rs.fillna('', inplace=True)
            rs2 = rs.apply(lambda x: to_sep.join(x), axis=1)
            # print(rs2.shape)
            # 替换分隔符后写入文件
            # rs2.to_csv(new_file, index=False, mode='a', header=False, quoting=csv.QUOTE_NONE,
            #            escapechar=' ')
            # rs2.to_excel(new_file,index=False,)
            # print(rs2)
            l = rs2.tolist()

            h = '\n'.join(l)
            h = h + '\n'
            # print(h)
            with open(new_file, 'a', encoding='utf-8') as w:
                w.writelines(h)
            # count = len(open(new_file, 'r', encoding='utf-8').readlines())
            # print(count)
    except Exception as t:
        print(t)


def truncate_file(file_name):
    with open(file_name, 'r+') as f:
        f.truncate()


if __name__ == '__main__':

    print('********************* args ******************************')
    argv = parse_args(sys.argv[1:])
    assert argv.old_file, 'Please check old_file'
    assert argv.to_sep, 'Please check to_sep'

    print(argv)

    old_file = argv.old_file
    filepath, tempfilename = os.path.split(old_file)
    filename, extension = os.path.splitext(tempfilename)
    new_file = os.path.join(filepath, filename + '_new' + extension)
    chunksize = argv.chunksize
    from_sep = argv.from_sep
    to_sep = argv.to_sep
    header = argv.header

    try:
        if header:
            print('%s 开始写入列名' % new_file)
            write_col(old_file, new_file, from_sep, to_sep)
        elif os.path.exists(new_file):
            print("文件已经存在，开始清理文件")
            truncate_file(new_file)
        print('%s 开始写入数据' % new_file)
        write_data(old_file, new_file, from_sep, to_sep, chunksize)
        print('%s 转换成功\n生成新文件%s' % (old_file, new_file))
    except Exception as e:
        print("发生错误")
