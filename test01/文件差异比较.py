#encoding=utf-8
import pandas as pd
import numpy as np

class dealExceldiff:

        
    def deal_same(primary_key,df1,df2):
        c=df1.columns.values
        lo=df1[primary_key].values
        co=df1.shape[1]
        m=[]
        for i in lo:
            f1=df1.loc[df1[primary_key]==i].values.flatten()
            f2=df2.loc[df2[primary_key]==i].values.flatten()
            for j in range(co):
                if f1[j] != f2[j]:
                    print('修改了%s=%s行对应的%s列,%s->%s'%(primary_key,i,c[j],f1[j],f2[j]))
                    f1[j]=str(f1[j])+'->'+str(f2[j])
                else :
                    f1[j] = f1[j]
            m.append(f1)
        n=pd.DataFrame(m,columns=c)
        n['flag']=0
        return n
        #n.to_excel("D:/work2/test_diff.xlsx",sheet_name='diff',index=False)

    def deal_add(df):
        df=pd.DataFrame(df)
        print('新增了行：',df)
        df['flag']=1
        return df

    def deal_del(df):
        df = pd.DataFrame(df)
        print('删除了行：',df)
        df['flag'] = -1
        return df

    def add_del(primary_key,df1,df2):
        df_same1=df1.loc[df1[primary_key].isin(df2[primary_key])]
        df_same2=df2.loc[df2[primary_key].isin(df1[primary_key])]
        df_add=df2.loc[~df2[primary_key].isin(df1[primary_key])]
        df_del=df1.loc[~df1[primary_key].isin(df2[primary_key])]
        return df_same1, df_same2, df_add, df_del

    def deal_result(primary_key,file1,file2,file_write):
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)

        df_same1,df_same2,df_add,df_del=dealExceldiff.add_del(primary_key,df1,df2)

        deal_df1 = dealExceldiff.deal_same(primary_key,df_same1, df_same2)
        deal_df2 = dealExceldiff.deal_add(df_add)
        deal_df3 = dealExceldiff.deal_del(df_del)
        res=pd.concat([deal_df1,deal_df2,deal_df3],ignore_index=True)
        print(res)
        res.to_excel(file_write, sheet_name='diff', index=False)

# if __name__ == '__main__':
#     file1="D:/work2/test1.xlsx"
#     file2="D:/work2/test2.xlsx"
#     file_write="D:/work2/test_diff.xlsx"
#     dealExceldiff.deal_result(file1,file2,file_write)