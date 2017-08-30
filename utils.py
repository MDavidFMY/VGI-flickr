# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:36:45 2017

@author: d_xuan
"""
import json
import os
import MySQLdb
import time
import datetime
config_path = "./config/"
datetime_format = '%Y-%m-%d %H:%M:%S'


#根据输入坐标范围，生成抓取位置点
def grab_area(lat_min,lat_max,lon_min,lon_max) :
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

#加载城市列表及对应抓取范围  cityformat:city_name lat_min lat_max lon_min lon_max
def load_city_area(city_name):
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

#从配置文件中读取抓取日期
def get_grab_date():
    date = {'start_time':'','year':'','month':'','day':''}
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
    return date

#将日期转化为对应抓取unix时间戳列表
def convert_grab_date(start_time):
    unix_time = []
    min_date = time.mktime(time.strptime(start_time, datetime_format))
    unix_time.append(int(min_date))
    day = datetime.datetime.strptime(start_time, datetime_format)
    delta = datetime.timedelta(days=1)
    n_day = day + delta
    max_date = time.mktime(n_day.timetuple())
    unix_time.append(int(max_date))
    return unix_time

#日期配置文件的日期增加操作
def add_one_day():
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
    resultfile = file(filename, "a+")
    #print '写入文件'+ filename
    for photo in photos:
        resultfile.write(json.dumps(photo))
        resultfile.write("\n")
    resultfile.close()

def data_static(city_name,date,count):
    statics = {'city_name':city_name,'date':date,'count':count}
    storfile = file(config_path + "grab_statics.json", "a+")
    storfile.write(json.dumps(statics))
    storfile.write("\n")
    storfile.close()

def write_config():
    date = {"start_time":"2016-02-01 00:00:00"}
    storfile = file(config_path+"date_config.json","w+")
    storfile.write(json.dumps(date))
    storfile.close()

# 测试类
if __name__=="__main__":
    write_config()








