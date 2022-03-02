"""
author:cai
project:learn_python
date:2022/2/21
"""
# coding=utf8

import datetime
import os
from time import sleep
import pandas as pd
import requests
import jpype
from retrying import retry


def get_rsa_sign(url, apiSecret):
    """
    调用java jar包，对入参进行rsa签名
    :param sign_raw:待签名字符串
    :return:signature:签名后的加密字符串
    """
    # 启动JVM

    jvmPath = jpype.getDefaultJVMPath()
    # print(jvmPath)
    if not jpype.isJVMStarted():
        #     jpype.shutdownJVM()
        jpype.startJVM(jvmPath, '-ea', '-Djava.class.path=Base64Url.jar')
    # 指定main class
    JDClass = jpype.JClass('Base64Url')
    # 创建类实例对象
    jd = JDClass()
    # 引用jar包类中的方法 rsa_sign
    signature = jd.urlDecode(url, apiSecret)
    # 关闭JVM
    # jpype.shutdownJVM()
    return signature

@retry(stop_max_attempt_number=3)  # 最大重试3次，3次全部报错，才会报错
def data_get(s):
    if s:
        # print(s)
        r = requests.get(s,timeout=10)
        assert r.status_code == 200
        js = r.json().get('body')
        page = r.json().get('pageInfo')
        data = pd.DataFrame(js)
        return data, page
    else:
        print('获取数据获取失败')


def truncate_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, mode='w') as f:
            f.seek(0)
            f.truncate()


def channel_list():
    pageSize = 100
    pageNum = 0
    file_name = 'channel_list_'+tag+'.csv'
    url = 'https://localhost/list?'
    url1 = url+'&pageSize='+str(pageSize)+'&pageNum='+str(pageNum)+'&apiKey='+apiKey
    s = get_rsa_sign(url1, apiSecret)
    data, page = data_get(s)
    data.to_csv(file_name, index=False, encoding='utf_8_sig')
    while page and pageNum < page['pages']:
        pageNum += 1
        mode = 'a'
        url1 = url+'&pageSize='+str(pageSize)+'&pageNum='+str(pageNum)+'&apiKey='+apiKey
        s = get_rsa_sign(url1, apiSecret)
        data, page = data_get(s)
        data.to_csv(file_name, mode=mode, header=False, index=False, encoding='utf_8_sig')


def event_growth(beginDate,endDate):
    cl = read_channel()
    groupBy = 'day'
    file_name = 'event_growth_'+tag+'.csv'
    url = 'https://localhost/growth?'
    truncate_file(file_name)
    for channelCode in cl:
        print(channelCode,beginDate,endDate)
        url1 = url+'&apiKey='+apiKey+'&beginDate='+beginDate+'&endDate='+endDate+'&groupBy='+groupBy+'&platform=android'+'&channelCode='+channelCode
        s = get_rsa_sign(url1, apiSecret)
        data, page = data_get(s)
        if not data.empty:
            data['channelCode']=channelCode
            data.to_csv(file_name, index=False,header=False,mode='a',encoding='utf_8_sig')
        sleep(0.1)

def get_event_growth(begin_date,end_date,seq):
    date = date_between(begin_date,end_date,seq)
    for i in date:
        beginDate = i[0]
        endDate = i[1]
        event_growth(beginDate,endDate)



def event_live():
    beginDate = '2022-01-22'
    endDate = '2022-02-20'
    file_name = 'event_live_'+tag+beginDate+'~'+endDate+'.csv'
    url = 'https://localhost/live?'
    url = url+'&apiKey='+apiKey+'&beginDate='+beginDate+'&endDate='+endDate
    s = get_rsa_sign(url, apiSecret)
    data, page = data_get(s)
    data.to_csv(file_name, index=False, encoding='utf_8_sig')


def event_active():
    beginDate = '2022-01-22'
    endDate = '2022-02-20'
    groupBy = 'hour'
    file_name = 'event_active_'+tag+beginDate+'~'+endDate+'.csv'
    url = 'https://localhost/active?'
    url = url+'&apiKey='+apiKey+'&beginDate='+beginDate+'&endDate='+endDate+'&groupBy='+groupBy
    s = get_rsa_sign(url, apiSecret)
    data, page = data_get(s)
    data.to_csv(file_name, index=False, encoding='utf_8_sig')


def read_channel():
    df = pd.read_csv('channel_list_'+tag+'.csv')
    cl = df['channelCode'].values
    return cl


def data_get_one_rows(s):
    r = requests.get(s)
    js = r.json().get('body')
    # 将json中的key作为header, 也可以自定义header（列名）
    data = pd.DataFrame(js, index=[0])
    return data


def channel_detail():
    file_name = 'channel_detail_'+tag+'.csv'
    url = 'https://localhost/get?'
    cl = read_channel()
    flag = True
    mode = 'w'
    for channelCode in cl:
        print(channelCode)
        ur = url+'&apiKey='+apiKey+'&channelCode='+channelCode
        s = get_rsa_sign(ur, apiSecret)
        try:
            data = data_get_one_rows(s)
        except Exception as e:
            print(e)
            continue
        if not data.empty:
            data.to_csv(file_name, mode=mode, header=flag, index=False, encoding='utf_8_sig')
        flag = False
        mode = 'a'


def channel_child_list():
    file_name = 'child_list_'+tag+'.csv'
    url = 'https://localhost/child/list?'
    pageSize = 100
    cl = read_channel()
    flag = True
    mode = 'w'
    for parentChannelCode in cl:
        print(parentChannelCode)
        ur = url+'&apiKey='+apiKey+'&parentChannelCode='+parentChannelCode+'&pageSize='+str(pageSize)
        s = get_rsa_sign(ur, apiSecret)
        try:
            data = data_get_one_rows(s)
        except Exception as e:
            print(e)
            continue
        if not data.empty:
            data.to_csv(file_name, mode=mode, header=flag, index=False, encoding='utf_8_sig')
        flag = False
        mode = 'a'


def event_sum_live():
    """存量设备分布"""
    platform = 'ios'
    type = 'd30'
    sumBy = 'state'

    file_name = 'event_sum_live_'+tag+'_'+platform+'_'+type+'_'+sumBy+'.csv'
    url = 'https://localhost/sum/live?'
    url = url+'&apiKey='+apiKey+'&platform='+platform+'&type='+type+'&sumBy='+sumBy
    s = get_rsa_sign(url, apiSecret)
    data = data_get(s)
    data.to_csv(file_name, index=False, encoding='utf_8_sig')


def event_sum_growth():
    """新增设备分布"""
    platform = 'ios'
    sumBy = 'state'
    beginDate = '2022-01-22'
    endDate = '2022-02-20'
    file_name = 'event_sum_growth_'+tag+'_'+platform+'_'+beginDate+'~'+endDate+'_'+sumBy+'.csv'
    url = 'https://localhost/sum/growth?'
    url = url+'&apiKey='+apiKey+'&platform='+platform+'&beginDate='+beginDate+'&endDate='+endDate+'&sumBy='+sumBy
    s = get_rsa_sign(url, apiSecret)
    data = data_get(s)
    data.to_csv(file_name, index=False, encoding='utf_8_sig')


def channel_group():
    file_name = 'channel_group_list.csv'
    url = 'https://localhost/group/list?'
    url = url+'&apiKey='+apiKey
    s = get_rsa_sign(url, apiSecret)
    data = data_get(s)
    data.to_csv(file_name, index=False, encoding='utf_8_sig')


def event_growth_00():
    beginDate = '2022-01-22'
    endDate = '2022-02-20'
    groupBy = 'hour'
    file_name = 'event_growth_'+tag+beginDate+'~'+endDate+'.csv'
    url = 'https://localhost/growth?'
    url = url+'&apiKey='+apiKey+'&beginDate='+beginDate+'&endDate='+endDate+'&groupBy='+groupBy+'&platform=android'
    s = get_rsa_sign(url, apiSecret)
    data, page = data_get(s)
    data.to_csv(file_name, index=False, encoding='utf_8_sig')


def get_date(begin_date, end_date, seq):
    d = []
    while begin_date <= end_date:
        end_persiod = datetime.datetime.strptime(begin_date, '%Y-%m-%d')+datetime.timedelta(seq)
        d.append((begin_date, min(datetime.datetime.strftime(end_persiod, '%Y-%m-%d'), end_date)))
        begin_date = end_persiod+datetime.timedelta(1)
        begin_date = datetime.datetime.strftime(begin_date, '%Y-%m-%d')
    return d


def get_yesterday():
    yesterday = datetime.datetime.today()+datetime.timedelta(-1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    return yesterday


def date_between(begin_date=None, end_date=None, seq=None):
    yesterday = get_yesterday()
    if begin_date is None:
        begin_date = yesterday
        end_date = yesterday
        d = [(begin_date, end_date)]
    elif begin_date <= end_date:
        d = get_date(begin_date, end_date, seq)
    else:
        d = []
    return d



if __name__ == '__main__':
    apiSecret = 'ya'
    apiKey = '5'
    tag = 'internal'

    # channel_list()
    # event_growth()
    # event_live()
    # event_active()
    # channel_detail()
    # channel_child_list()
    # event_sum_live()
    # event_sum_growth()
    # channel_group()

    get_event_growth('2022-02-01',get_yesterday(),30)

    # jpype.shutdownJVM()
