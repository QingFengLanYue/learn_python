import re

file='files/dws_pms_transaction_stat_df.sql'


import re

with open(file,mode='r',encoding='utf-8') as f:
    table_names=set()
    lines=str(f.readlines())
    pattern = r"FROM\s+([\w.]+)|JOIN\s+([\w.]+)"
    matches = re.findall(pattern, lines, flags=re.IGNORECASE)
    # print(matches)
    for match in matches:
        new_tuple = [item for item in match if item != '']
        table_names.update(new_tuple)

    print(table_names)

# 示例用e1', 'table2'}