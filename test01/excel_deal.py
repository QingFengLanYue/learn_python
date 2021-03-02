import  pandas as pd
import numpy as np
import xlrd
import openpyxl
# C:\Users\Administrator\Desktop\Agent手工数据需求说明V1.0.xlsx  IATA Mapping手工表 Account Category Mapping手工表

df_agent=pd.read_excel(r'C:\Users\Administrator\Desktop\Agent手工数据需求说明V1.0.xlsx',sheet_name='IATA Mapping手工表')
df_company=pd.read_excel(r'C:\Users\Administrator\Desktop\Agent手工数据需求说明V1.0.xlsx',sheet_name='Account Category Mapping手工表')
#print(df_agent)
#print(df_company)
# print(df_agent.duplicated())

#print(df_agent.columns)
# print(df_agent.index)
#print(df_agent[['IATA','Agency Grouping ']].values)

#df1=df_agent[['IATA','Agency Grouping ']].drop_duplicates()
#print(df1.values)
#df1.to_excel('C:/Users/Administrator/Desktop/cs.xlsx',columns=['IATA','Agency Grouping '],index=False)
df3=pd.read_excel(r'C:/Users/Administrator/Desktop/cs.xlsx',index=False)
#print(df3[['IATA'].replace('[- ]','',regex=True),['Agency Grouping ']])
iata=df3['IATA'].replace('[- ]','',regex=True)
agent=df3['Agency Grouping ']
# AMEX TLS  Ensemble  Signature  The Luxury Circle  Travel Leaders Group  Traveler Made   Virtuoso
def other(sta):
    list_type=[0,0,0,0,0,0]
    if sta=='AMEX TLS':
        list_type[0]=1
    elif sta=='Ensemble  Signature':
        list_type[1]=1
    elif sta=='The Luxury Circle':
        list_type[2]=1
    elif sta=='Travel Leaders Grou':
        list_type[3]=1
    elif sta=='Traveler Made':
        list_type[4]=1
    elif sta=='Virtuoso':
        list_type[5]=1




print(agent)