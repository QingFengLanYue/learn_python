import pandas as pd
file = 'data/Category Mapping.xlsx'
h = pd.read_excel(file,sheet_name='Sheet1')
h = h.fillna(method='pad')
print(h)



def parse_header(df, skiprows, nrows):
    # 提取表头df，其中skiprows表示表格前的空行，nrows表示表头的行数，重新建立index
    head_df = df.loc[skiprows: skiprows+nrows-1]
    head_df = head_df.reset_index(drop=True)
    # 处理合并单元格，填充NaN
    head_df = head_df.fillna(method='ffill', axis=0)
    head_df = head_df.fillna(method='ffill', axis=1)
    # 建立表头
    head_df.loc[nrows] = ''
    head_df.loc[nrows] = head_df.apply(process_header, args=(nrows,))
    df = df.loc[skiprows+nrows:]
    df = df.reset_index(drop=True)
    df.columns = list(head_df.loc[nrows])

    return df

def process_header(x, index_range):
    header = x.loc[0]
    for i in range(index_range-1):
        if x.loc[i] != x.loc[i+1]:
            header = header + '_' + x.loc[i+1]
    return header


h=parse_header(h,1,0)
print(h)
