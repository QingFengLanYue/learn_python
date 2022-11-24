"""
author:风起于青萍之末，浪成于微澜之间
project:learn_python
date:2022/11/24
"""
# coding=utf8

import datetime


def f_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d')


def sub_day(start_date, end_date):
    s = f_date(start_date)
    e = f_date(end_date)
    return (e - s).days


def per_money_day(money, days):
    return money / days


if __name__ == '__main__':
    stay_date = '2022-11-08'
    # stay_date = '2022-11-11'

    fmoney = 3860.17
    f_start = '2022-06-13'
    f_end = '2023-09-12'
    f_day = sub_day(f_start, f_end)
    f_m = per_money_day(fmoney, f_day)

    zmoney = 2650
    z_end = '2022-12-12'
    z_m = per_money_day(zmoney, 30)

    y_fmoeny = f_m * sub_day(stay_date, f_end)
    y_zmoney = z_m * sub_day(stay_date, z_end)

    print(f'退房时间为:{stay_date}\n剩余服务费应退:{y_fmoeny:.2f}\n剩余房租应退:{y_zmoney:.2f}')
    print(f'总的退费金额为:{y_fmoeny + y_zmoney + 2650:.2f}')
