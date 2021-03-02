import pandas as pd
import matplotlib.pyplot as plt
file='dream.csv'
col=['期数','date','red1','red2','red3','red4','red5','red6','blue']
#col=[0,1,2,3,4,5,6,7,8]
df=pd.read_csv(file,usecols=col)
df['year']=pd.to_datetime(df['date'].values).year
# print(df)
#
# red1=df['red1'].value_counts().sort_index()
# red2=df['red2'].value_counts().sort_index()
# red3=df['red3'].value_counts().sort_index()
# red4=df['red4'].value_counts().sort_index()
# red5=df['red5'].value_counts().sort_index()
# red6=df['red6'].value_counts().sort_index()
# blue=df['blue'].value_counts().sort_index()
#
# #print(print(pd.merge(red1,red2)))
# # print(red1)
# # col1=pd.DataFrame(red1)
# # col2=pd.DataFrame(red2)
#
# n1=pd.concat([red1,red2,red3,red4,red5,red6], axis=1)
# n2=n1.fillna(0)
# print(n2)
# n2["总和"] =n2.apply(lambda x:x.sum(),axis =1)
# n3=pd.DataFrame(n2['总和'].values,columns=['2003'])
# print(n3)
# # n3.plot(kind='bar')
# # n3.plot(kind='area')
# n3.plot(kind='box')
# # n3.plot(kind='kde')
# #plt.show()
def cc_plot():
    a=pd.to_datetime(df['date'].values).year.drop_duplicates()
    n4=pd.DataFrame()
    for i in a:
        df1=df.loc[df['year']==i]
        red1 = df1['red1'].value_counts().sort_index()
        red2 = df1['red2'].value_counts().sort_index()
        red3 = df1['red3'].value_counts().sort_index()
        red4 = df1['red4'].value_counts().sort_index()
        red5 = df1['red5'].value_counts().sort_index()
        red6 = df1['red6'].value_counts().sort_index()
        blue = df1['blue'].value_counts().sort_index()

        # print(print(pd.merge(red1,red2)))
        # print(red1)
        # col1=pd.DataFrame(red1)
        # col2=pd.DataFrame(red2)

        n1 = pd.concat([red1, red2, red3, red4, red5, red6], axis=1)
        n2 = n1.fillna(0)
        n2["总和"] = n2.apply(lambda x: x.sum(), axis=1)
        n3= pd.DataFrame(n2['总和'].values, columns=[i])
        #print(n3)
        n4=pd.concat([n4,n3],axis=1)
        #n4=n3.join(n4)

    n4.plot(kind='box')

    n4.plot(kind='bar')
    n4.plot(kind='area')
    n4.plot(kind='kde')

    plt.title('Cc Analys')
    plt.show()


def cc_sum():
    n1 = df.iloc[:, 2:9]
    n1["总和"] = n1.apply(lambda x: x.sum(), axis=1)
    return n1

def cc_jo(n1):
    joj=0
    joo=0
    for i in n1['总和'].values:
        if i%2==0:
            joo+=1
        else:
            joj+=1

    labels = '奇数', '偶数'
    sizes = joj , joo
    colors = 'lightgreen','gold'
    explode = 0.1,0.05
    plt.pie(sizes,explode=explode, labels=labels,colors=colors, autopct='%1.1f%%', shadow=True, startangle=50)
    plt.axis('equal')
    plt.title('奇偶数分布')
    plt.rcParams['font.sans-serif'] = ['SimHei']

    plt.show()

    #print(pd.cut(n1["总和"],5))


def cc_fb(n1):
    '''
       (40.855, 70.0] < (70.0, 99.0] < (99.0, 128.0] < (128.0, 157.0] <
    (157.0, 186.0]
    '''
    a1,a2,a3,a4,a5=0,0,0,0,0
    for i in n1['总和'].values:
        if i <= 70:
            a1 += 1
        elif i<= 99:
            a2 += 1
        elif i<= 128:
            a3 += 1
        elif i<= 157:
            a4 += 1
        elif i<= 186:
            a5 += 1

    labels = '40.855~70.0', '70.0~99.0','99.0~128.0','128.0~157.0','157.0~186.0'
    sizes = a1,a2,a3,a4,a5
    colors = 'lightgreen', 'gold','lightskyblue','lightcoral','blue'
    #explode = 0.1,0.05,0.15,0.1,0.12
    explode = 0.1,0.1, 0.1, 0.1, 0.1
    plt.pie(sizes, explode=explode,labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=50)
    plt.axis('equal')
    plt.title('总和区间分布图')
    plt.rcParams['font.sans-serif'] = ['SimHei']

    plt.show()

n1=cc_sum()
#cc_jo(n1)
#cc_fb(n1)

n1=n1['总和']
n1.plot(kind='area')

plt.title('Cc Analys')
plt.show()
plt.rcParams['font.sans-serif'] = ['SimHei']
print(n1)