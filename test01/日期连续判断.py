import copy
import datetime
def lianxu_date(a):
    b=a.split()
    c=[]
    d=[]
    for i in range(len(b)-1):
        current_date=datetime.datetime.strptime(b[i], "%Y-%m-%d").date()
        yesterday_date=current_date-datetime.timedelta(days=1)
        list_date=datetime.datetime.strptime(b[i+1], "%Y-%m-%d").date()
        if yesterday_date != list_date :
            print(list_date, current_date,'需要补数')
            c.append(str(list_date))
            c.append(str(current_date))
            d.append(copy.deepcopy(c))
            c.clear()
    return d

def jiange_date(stat_date,end_date):
    stat_date=datetime.datetime.strptime(stat_date, "%Y-%m-%d").date()
    end_date=datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    date1=[]
    while stat_date < end_date - datetime.timedelta(days=1):
        stat_date = stat_date + datetime.timedelta(days=1)
        date1.append(str(stat_date))
    return date1

if __name__ == '__main__':
    a="""
       2020-01-10 2020-01-09 2019-11-30 2019-11-29 2019-11-05 2019-11-04 
       2019-11-03 2019-11-02 2019-11-01 2019-10-18 2019-10-17 2019-10-16 
       2019-10-02 2019-10-01 2019-09-15 2019-09-02 2019-08-21 2019-08-18
      """
    d=lianxu_date(a)
    m=[]
    for i in range(len(d)):
        date_range=d[i]
        start_date=date_range[0]
        end_date=date_range[1]
        m.extend(jiange_date(start_date,end_date))
    print(m)