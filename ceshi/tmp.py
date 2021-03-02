import numpy as np
import pandas as pd
f=pd.read_csv('C:/Users/HP/Desktop/cs.csv',sep=',')
ng=f.groupby('name')
def collect_set(group):
    return set(group.values)


f1=ng.agg(collect_set)
print(f1.ix[1])

