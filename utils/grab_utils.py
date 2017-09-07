# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:36:45 2017

@author: ding_x
"""
import json
import os
import MySQLdb
import time
import datetime

config_path = "../config/"
datetime_format = '%Y-%m-%d %H:%M:%S'


def grab_area(lat_min,lat_max,lon_min,lon_max) :
    '''
    根据输入的坐标范围生成抓取点阵
    :param lat_min:
    :param lat_max:
    :param lon_min:
    :param lon_max:
    :return:
    '''
    area = []
    for i in range(0,2):
        if i ==1:
            lat_min = lat_min+0.05
            lon_min = lon_min+0.05
        lat = lat_min
        while lat <lat_max :
            lon = lon_min
            while lon <lon_max :
                coordinate = (lat,lon)
                area.append(coordinate)
                lon +=0.1
            lat += 0.1
    return area


def load_city_area(city_name):
    '''
    加载指定城市的抓取范围
    :param city_name:
    :return:
    '''
    city_file = open(config_path+'city_list.txt')
    city_area=[]
    try:
        city_obj_list = city_file.readlines()
        for city_obj in city_obj_list:
            if '\xef\xbb\xbf'  in city_obj:
                city_obj = city_obj.replace('\xef\xbb\xbf','').strip()
            str_list = city_obj.split(' ')
            if city_name == str_list[0]:
                print str_list
                city_area = grab_area(float(str_list[1]),float(str_list[2]),float(str_list[3]),float(str_list[4]))
                break
    finally:
        city_file.close()
    return city_area


def get_grab_date():
    '''
    从日期配置文件中读取抓取日期
    :return:
    '''
    date = {'start_time':'','year':'','month':'','day':'','iso_time':''}
    date_file = open(config_path + 'date_config.json')
    try:
        date_config = date_file.read()
        date_dic = json.loads(date_config)
        start_time = date_dic["start_time"]
    finally:
        date_file.close()
    dt = datetime.datetime.strptime(start_time, datetime_format)
    date["start_time"] = start_time
    date["year"] = str(dt.year)
    date["month"] = str(dt.month)
    date["day"] = str(dt.day)
    date["iso_time"] = str(dt.isoformat())
    return date


def convert_grab_date(start_time,format_c):
    '''
    将日期字符串转化为对应抓取unix（ISO 8601）时间戳列表
    :param start_time:
    :return:
    '''
    covert_time = []
    if format_c == "unix":
        min_date = time.mktime(time.strptime(start_time, datetime_format))
        covert_time.append(int(min_date))
        day = datetime.datetime.strptime(start_time, datetime_format)
        delta = datetime.timedelta(days=1)
        n_day = day + delta
        max_date = time.mktime(n_day.timetuple())
        covert_time.append(int(max_date))
    elif format_c == "ISO":
        day = datetime.datetime.strptime(start_time, datetime_format)
        covert_time.append(day.isoformat())
        delta = datetime.timedelta(days=1)
        n_day = day + delta
        covert_time.append(n_day.isoformat())

    return covert_time

def add_one_day():
    '''
    实现日期配置文件中抓取日期的自动增加
    :return:
    '''
    date_file = open(config_path + 'date_config.json')
    try:
        date_config = date_file.read()
        date_dic = json.loads(date_config)
        str_datetime = json.loads(date_config)["start_time"]
        day = datetime.datetime.strptime(str_datetime,datetime_format)
        delta = datetime.timedelta(days =1)
        n_day = day+delta
        date_dic["start_time"] = n_day.strftime(datetime_format)
    finally:
        date_file.close()
    storfile = file(config_path + "date_config.json", "w+")
    storfile.write(json.dumps(date_dic))
    storfile.close()


def sto_photos (photos,filename):
    '''
    提取flickr中的photo字段，并保存本地
    :param photos:
    :param filename:
    :return:
    '''
    resultfile = file(filename, "a+")
    #print '写入文件'+ filename
    for photo in photos:
        resultfile.write(json.dumps(photo))
        resultfile.write("\n")
    resultfile.close()

def data_static(city_name,date,count):
    '''
    统计抓取城市每天的数据获取量
    :param city_name:
    :param date:
    :param count:
    :return:
    '''
    statics = {'city_name':city_name,'date':date,'count':count}
    storfile = file(config_path + "grab_statics.json", "a+")
    storfile.write(json.dumps(statics))
    storfile.write("\n")
    storfile.close()

def write_config():
    date = {"Client_ID":"ekcyWUdPNnkwSlRrMThjMVhWTFV0dzphYjRiMmE0MzM3YzQzMTAy","Client Secret":"MWQ2MWViYjBmZTRlNGJhNmYxZTZhYjI2MjczN2UzMDM="}
    storfile = file(config_path+"mapillary_token.txt","w+")
    storfile.write(json.dumps(date))
    storfile.close()

# 测试类
if __name__=="__main__":
    #write_config()
    convert_grab_date()






