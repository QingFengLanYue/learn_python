import pandas as pd
names=['酒店','日期','rep间夜','cube间夜','rep收入','cube收入','间夜差异','收入差异']
df=pd.read_excel(r'D:/work2/diff_room_cube.xlsx',names=names,index_col=False)
#print(df.shape)
# print(df['rep间夜'])
# print(df['cube间夜'])

df1=df['rep间夜']!=df['cube间夜']
df2=df['rep收入']!=df['cube收入']

df3=df[df1]
#df3=df3.loc[df3['酒店'].isin(['ESL'])]
print(df3)
df3=df3.fillna(0)



df4=df3[(df3['rep收入']!=df3['cube收入']) & (df3['rep收入'] !=0 )& (df3['cube收入'] !=0)]

print(df4)


df5=df4['酒店'].drop_duplicates()
df5=df5.reset_index(drop=True)
print(df5)