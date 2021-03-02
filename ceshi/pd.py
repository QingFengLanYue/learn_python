import pandas as pd
df=pd.read_excel('C:/Users/Administrator/Desktop/pms 1014.xlsx',sheet_name='Hotel Info',dtype='str' )
# print(df)
#print(df.fillna(method='ffill'))
#print(df.drop(['HOTEL_PMS'], axis = 1))
print(df.drop([1,2,4],inplace=True))