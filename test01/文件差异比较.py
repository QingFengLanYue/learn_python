#encoding=utf-8
import pandas as pd
import numpy as np

def deal_same(df1,df2):
    c=df1.columns.values
    lo=df1['id'].values
    co=df1.shape[1]
    m=[]
    for i in lo:
        f1=df1.loc[df1['id']==i].values.tolist()[0]
        f2=df2.loc[df2['id']==i].values.tolist()[0]
        for j in range(co):
            if f1[j] != f2[j]:
                print('修改了id=%s行对应的%s列,%s->%s'%(i,c[j],f1[j],f2[j]))
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

def add_del(df1,df2):
    df_same1=df1.loc[df1['id'].isin(df2['id'])]
    df_same2=df2.loc[df2['id'].isin(df1['id'])]
    df_add=df2.loc[~df2['id'].isin(df1['id'])]
    df_del=df1.loc[~df1['id'].isin(df2['id'])]
    return df_same1, df_same2, df_add, df_del

if __name__=='__main__':
    df1 = pd.read_excel(r"D:/work2/test1.xlsx")
    df2 = pd.read_excel(r"D:/work2/test2.xlsx")

    df_same1,df_same2,df_add,df_del=add_del(df1,df2)

    deal_df1 = deal_same(df_same1, df_same2)
    deal_df2 = deal_add(df_add)
    deal_df3 = deal_del(df_del)
    res=pd.concat([deal_df1,deal_df2,deal_df3],ignore_index=True)
    print(res)
    res.to_excel("D:/work2/test_diff.xlsx", sheet_name='diff', index=False)