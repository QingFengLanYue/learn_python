import re
def read_file(fname):
    with open(fname,encoding='utf-8') as f:
        lines = f.readlines()
        reult = ''.join(lines)
        create_sql=sql_deal(reult)
        comment_sql=comment_deal(reult)
        return create_sql,comment_sql
def sql_deal(line):
    # a = "`id` sqligint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',"
    sql = re.sub("`","",line)

    sql = re.sub(" bigint\(\d+\) ", " int8 ", sql)
    sql = re.sub(" int\(\d+\) ", " int4 ", sql)
    sql = re.sub(" tinyint\(\d+\) ", " int2 ", sql)
    sql = re.sub(" unsigned ", " ", sql)
    sql = re.sub(" COMMENT '.*'","", sql)

    sql = re.sub(" ON UPDATE CURRENT_TIMESTAMP"," ", sql)
    sql = re.sub(" DEFAULT CURRENT_TIMESTAMP", " ", sql)
    sql = re.sub(" datetime ", " timestamp ", sql)
    sql = re.sub(" id.*NOT NULL AUTO_INCREMENT*"," id bigserial NOT NULL", sql)


    table_name = re.search("CREATE TABLE (.*) \(", sql).group(1)
    table_name = re.sub("\.","_",table_name)
    table_name = "CONSTRAINT "+table_name+"_pkey PRIMARY KEY(id)"
    sql = re.sub("PRIMARY KEY .*", table_name+"\n);", sql, re.M, re.S)
    
    
    return sql


def comment_deal(line):
    #line = "`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',"
    comment = line
    table_name = re.search("CREATE TABLE `(.*)` \(", comment).group(1)
    comment_list = re.findall(".* COMMENT .*", comment)
    comment_sql="\n"*2
    for i in comment_list:
        pattern1 = '.*`(.*?)`.*COMMENT (.*?),'
        s = re.compile(pattern=pattern1).search(i).group(1, 2)
        comment_sql1='comment on column %s.%s is %s ;' % (table_name, s[0], s[1])
        comment_sql=comment_sql+comment_sql1+"\n"
    return comment_sql


fname="create_table.sql"
create_sql,comment_sql=read_file(fname)
print(create_sql,comment_sql)