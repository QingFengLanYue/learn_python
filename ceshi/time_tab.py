# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# *********************************************
# **所属主题：theme
# **功能描述：desc
# **创建者：  jxq
# **创建日期: 19/9/19.
# *********************************************

import pandas as pd
import datetime
import math
import calendar
def month_simple(index):
    w = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    return w[index-1]

def month_simple_order(index):
    w = ['[01]Jan', '[02]Feb', '[03]Mar', '[04]Apr', '[05]May', '[06]Jun', '[07]Jul', '[08]Aug', '[09]Sept', '[10]Oct', '[11]Nov', '[12]Dec']
    return w[index-1]

def month(index):
    w = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return w[index-1]


def week_simple(index):
    w = [ 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat','Sun']
    return w[index]


def week_simple_order(index):
    w = [ '[1]Mon', '[2]Tue', '[3]Wed', '[4]Thu', '[5]Fri', '[6]Sat','[7]Sun']
    return w[index]

def week(index):
    w = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    return w[index]

def week_part(index):
    if index == 4 or index == 5:
        return 'Weekend'
    else:
        return 'Weekday'


def weekday_flag(index):
    if index == 4 or index == 5:
        return False
    else:
        return True

def weekend_flag(index):
    if index == 4 or index == 5:
        return True
    else:
        return False

def halfyear_flag(index):
    if int(index) <= 6:
        return 1
    else:
        return 2


'''
年分割周index 7-1 为一周
'''


def week_of_week_range(dayDate):
    day = dayDate.dayofyear
    if pd.Timestamp(str(dayDate.year) + "-01-01").dayofweek == 6:
        week_index = pd.Timestamp(str(dayDate.year) + "-01-01").dayofweek-6
    else:
        week_index = pd.Timestamp(str(dayDate.year) + "-01-01").dayofweek+1

    # print(dayDate,pd.Timestamp(str(dayDate.year) + "-01-01").dayofweek, "   ",week_index+day)
    # print(math.ceil((week_index+day)/7),day,week_index,pd.Timestamp(str(dayDate.year) + "-01-01").dayofweek)


    return math.ceil((week_index+day)/7)



'''
时间范围内 年分割周index
'''
def week_of_time_range_new(startDate, index):
    day = index.dayofyear
    year1 = datetime.datetime.strptime(startDate, "%Y-%m-%d").year
    year2 = datetime.datetime.strptime(str(index)[0:10], "%Y-%m-%d").year
    sub_value = year2 - year1
    # print(index,week_of_week_range(index, day),day)
    # print(week_of_week_range(index, day) + sub_value * 53)
    return week_of_week_range(index) + sub_value * 53

'''
时间范围内 年分割周index
'''
def week_of_time_range(startDate, index):
    year1 = datetime.datetime.strptime(startDate, "%Y-%m-%d").year
    year2 = datetime.datetime.strptime(str(index)[0:10], "%Y-%m-%d").year
    sub_value = year2 - year1
    return dt_week_by_year(index) + sub_value * 53




def dt_week_by_year_new(index):
    strftime1 = pd.to_datetime(index).strftime("%Y%m%d"),
    strftime2 = pd.to_datetime(index).strftime("%Y0113"),
    if  week_of_week_range(index) == 1 and strftime1 > strftime2:
        return 53
    elif week_of_week_range(pd.Timestamp(str(index.year) + "-01-01")) > 1:
        if week_of_week_range(index) > 51 and week_of_week_range(pd.Timestamp(str(index.year) + "-" + str(index.month) + "-7")) < 3:
            return 1
        else:
            return week_of_week_range(index) + 1
    else:
        return week_of_week_range(index)





def dt_week_by_year(index):
    strftime1 = pd.to_datetime(index).strftime("%Y%m%d"),
    strftime2 = pd.to_datetime(index).strftime("%Y0113"),
    if index.weekofyear == 1 and strftime1 > strftime2:
        return 53
    elif pd.Timestamp(str(index.year) + "-01-01").weekofyear > 1:
        if index.weekofyear > 51 and pd.Timestamp(str(index.year) + "-" + str(index.month) + "-7").weekofyear < 3:
            return 1
        else:
            return index.weekofyear + 1
    else:
        return index.weekofyear

'''
S/E/A/N
S 本周的开始
E 本周的结束
A 既是本周的开始又是本周的结束
N 以上都不是
'''
def week_period_flag(index):
    before_day = pd.Timestamp((pd.to_datetime(index) + datetime.timedelta(days=-1)))
    after_day = pd.Timestamp((pd.to_datetime(index) + datetime.timedelta(days=1)))

    before_dt_week_ext = dt_week_by_year_new(before_day)
    dt_week_ext = dt_week_by_year_new(index)
    after_dt_week_ext = dt_week_by_year_new(after_day)

    if dt_week_ext != before_dt_week_ext and dt_week_ext != after_dt_week_ext:
        return 'A'
    elif before_dt_week_ext != dt_week_ext and dt_week_ext == after_dt_week_ext:
        return 'S'
    elif before_dt_week_ext == dt_week_ext and dt_week_ext != after_dt_week_ext:
        return 'E'
    else:
        return 'N'


def month_day_num(index):
    strfyear = pd.to_datetime(index).strftime("%Y")
    strfmonth = pd.to_datetime(index).strftime("%m")
    monthRange = calendar.monthrange(int(strfyear), int(strfmonth))
    return monthRange[1]


def generateData(startDate='2019-1-01', endDate='2019-1-14'):
    d = {'dt': pd.date_range(start=startDate, end=endDate)}
    data = pd.DataFrame(d)

    data['dt_num'] = data['dt'].apply(lambda x: pd.to_datetime(x).strftime("%Y%m%d"))
    data['dt_year'] = data['dt'].apply(lambda x: x.year)
    data['dt_month'] = data['dt'].apply(lambda x: x.month)
    data['dt_day'] = data['dt'].apply(lambda x: x.day)
    data['dt_quarter'] = data['dt'].apply(lambda x: x.quarter)
    data['dt_week'] = data['dt'].apply(lambda x: x.weekofyear)


    # data['dt_week_new'] = data['dt'].apply(lambda x: week_of_week_range(x,x.day))


    data['dt_week_ext'] = data['dt'].apply(lambda x: week_of_week_range(x))
    # data['dt_week_ext'] = data['dt'].apply(lambda x: dt_week_by_year(x))

    data['week_period_flag_ext'] = data['dt'].apply(lambda x: week_period_flag(x))
    data['dt_week_day'] = data['dt'].apply(lambda x: x.dayofweek)
    data['week_part'] = data['dt_week_day'].apply(lambda x: week_part(x))
    data['week_eng'] = data['dt_week_day'].apply(lambda x: week(x))
    data['week_simple'] = data['dt_week_day'].apply(lambda x: week_simple(x))
    data['month_eng'] = data['dt_month'].apply(lambda x: month(x))
    data['month_simple'] = data['dt_month'].apply(lambda x: month_simple(x))
    data['weekday_flag'] = data['dt_week_day'].apply(lambda x: weekday_flag(x))
    data['weekend_flag'] = data['dt_week_day'].apply(lambda x: weekend_flag(x))
    data['halfyear_flag'] = data['dt_month'].apply(lambda x: halfyear_flag(x))
    data['week_of_time_range'] = data['dt'].apply(lambda x: week_of_time_range_new(startDate, x))
    data['month_day_num'] = data['dt'].apply(lambda x: month_day_num(x))

    data['week_simple_order'] =  data['dt_week_day'].apply(lambda x: week_simple_order(x))
    data['month_simple_order'] = data['dt_month'].apply(lambda x: month_simple_order(x))
    return data

def main():
    data = generateData(startDate='2012-01-01', endDate='2035-12-31')
    # data = generateData(startDate='2022-01-01', endDate='2022-01-31')
    cols = ['dt', 'dt_num', 'dt_year', 'dt_month', 'dt_day', 'dt_quarter', 'dt_week', 'dt_week_ext',
            'week_of_time_range',
            'week_period_flag_ext', 'week_part','week_eng', 'week_simple','month_eng','month_simple','weekend_flag', 'weekday_flag',
            'halfyear_flag','month_day_num','week_simple_order','month_simple_order']
    data[cols].to_csv('D:/work2/DIM_TIME.csv', sep='\t', index=False, header=True, index_label=False, encoding="utf_8_sig")


if __name__ == '__main__':
    main()


