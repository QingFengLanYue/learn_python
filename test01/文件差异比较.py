# encoding=utf-8
import os

import pandas as pd


class DealLine:
    def __init__(self, df):
        self.df = df

    def deal_del(self):
        df = pd.DataFrame(self.df)
        print('删除了行：', df)
        df['flag'] = -1
        return df

    def deal_add(self):
        df1 = pd.DataFrame(self.df)
        print('新增了行：', df1)
        df1['flag'] = 1
        return df1


# class DealAddLine(DealDelLine):
#     def __init__(self, df):
#         super().__init__(df)
#
#     def deal_add(self):
#         df1 = pd.DataFrame(self.df)
#         print('新增了行：', df1)
#         df1['flag'] = 1
#         return df1


class DealColumn:
    """
    列的更新
    """

    def __init__(self, filename, df1, df2):
        self.filename = filename
        self.df1 = df1
        self.df2 = df2

    def deal_column(self):
        """
        返回新增的列和删除的列
        :return:
        """
        column_df1 = self.df1.columns.values
        column_df2 = self.df2.columns.values

        # 删除的行
        same_column = [i for i in column_df1 if i in column_df2]
        only_df1_column = [i for i in column_df1 if i not in column_df2]
        only_df2_column = [i for i in column_df2 if i not in column_df1]

        df1 = self.df1[same_column]
        df2 = self.df2[same_column]
        if only_df1_column:
            print('%s删除了 %s列' % (self.filename, only_df1_column))
        if only_df2_column:
            print('%s新增了 %s列' % (self.filename, only_df2_column))

        return df1, df2, only_df1_column, only_df2_column


class DealExcelDiff(DealLine):

    def __init__(self, primary_key, file1, file2, file_write):
        super().__init__(DealLine)
        self.primary_key = primary_key
        self.file1 = file1
        self.file2 = file2
        self.file_write = file_write
        self.filename = self.file_ana()

    def file_ana(self):
        file_path, filename = os.path.split(self.file1)
        return filename

    def deal_same(self, df1, df2):
        c = df1.columns.values
        lo = df1[self.primary_key].values
        co = df1.shape[1]
        m = []
        for i in lo:
            print(i)
            print(c)
            f1 = df1.loc[df1[self.primary_key] == i].values.flatten()
            f2 = df2.loc[df2[self.primary_key] == i].values.flatten()
            for j in range(co):
                print(j)
                if f1[j] != f2[j]:
                    print('修改了%s=%s行对应的%s列,%s->%s' % (self.primary_key, i, c[j], f1[j], f2[j]))
                    f1[j] = str(f1[j]) + '->' + str(f2[j])
                else:
                    f1[j] = f1[j]
            m.append(f1)
        n = pd.DataFrame(m, columns=c)
        n['flag'] = 0
        return n
        # n.to_excel("D:/work2/test_diff.xlsx",sheet_name='diff',index=False)

    def add_del(self, df1, df2):
        df_same1 = df1.loc[df1[self.primary_key].isin(df2[self.primary_key])]
        df_same2 = df2.loc[df2[self.primary_key].isin(df1[self.primary_key])]
        df_add = df2.loc[~df2[self.primary_key].isin(df1[self.primary_key])]
        df_del = df1.loc[~df1[self.primary_key].isin(df2[self.primary_key])]
        return df_same1, df_same2, df_add, df_del

    def deal_result(self):
        df1 = pd.read_excel(self.file1)
        df2 = pd.read_excel(self.file2)

        df1 = df1.fillna('001')
        df2 = df2.fillna('001')

        dc = DealColumn(self.filename, df1, df2)

        df1, df2, only_df1_column, only_df2_column = dc.deal_column()

        df_same1, df_same2, df_add, df_del = self.add_del(df1, df2)

        deal_df1 = self.deal_same(df_same1, df_same2)

        d1 = DealLine(df_add)
        d2 = DealLine(df_del)

        deal_df2 = d1.deal_add()
        deal_df3 = d2.deal_del()

        res = pd.concat([deal_df1, deal_df2, deal_df3], ignore_index=True)
        res[only_df1_column] = 'del_col'
        res[only_df2_column] = 'add_col'

        # 显示所有列
        pd.set_option('display.max_columns', None)
        # 显示所有行
        pd.set_option('display.max_rows', None)
        # 设置value的显示长度为100，默认为50
        pd.set_option('display.width', None)
        print('=' * 100)
        print(res)
        res.to_excel(self.file_write, sheet_name='diff', index=False)


if __name__ == '__main__':
    file1 = "D:/工作/room cube/新版room cube/Room Cube优先级较高的字段V1.2.xlsx"
    file2 = "D:/工作/room cube/新版room cube/Room Cube优先级较高的字段V1.3.xlsx"
    file_write = "D:/work2/test_diff.xlsx"
    primary_key = '需求字段'
    df1 = pd.read_excel(file1).fillna('001')
    df2 = pd.read_excel(file2).fillna('001')

    a = DealExcelDiff(primary_key, file1, file2, file_write)
    print(a.primary_key)

    a.deal_same(df1,df2)
