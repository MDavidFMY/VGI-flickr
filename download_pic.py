# -*- coding: utf-8 -*-
"""
Created on 2017/9/14 22:29

@author: ding_x
"""
import urllib2, urllib
import json
import os
import requests
from utils.mysql_utils import *
from data_stor import *

storpath = 'D:\\MapillaryData\\ImageData'
#torpath = '/media/ding_x/Seagate Backup Plus Drive/VGI_Data/Flickr_pic/'
MAPILLARY_IM_RETRIEVE_URL = 'https://d1cuyjsrcm0gby.cloudfront.net/%s/thumb-1024.jpg'

def geturl(data_type):
    result_dic = {}
    if data_type == "Flickr":
        db = connect_sql('vgiwork')
        month = 1
        while month <= 12:
            url_temp_list = []
            table_name = 'london_2016_%d' % month
            selectsql = "select url_m from %s" % table_name
            print selectsql
            url_list = sql_select(db,selectsql)
            for url in url_list:
                if url[0] != '':
                    url_temp_list.append(url[0])
            result_dic[table_name] = url_temp_list
            month += 1
    elif data_type == "Mapillary":
        db = connect_sql('vgiwork')
        url_temp_list = []
        selectsql = "select key from london"
        print selectsql
        key_list = sql_select(db, selectsql)
        url_temp_list = [MAPILLARY_IM_RETRIEVE_URL % key[0] for key in key_list]
        result_dic[table_name] = url_temp_list
    return result_dic


def url_download(result_dic):
    for table_name in result_dic:
        for url in result_dic[table_name]:
            #pic_id = url.split('/')[4].split('_')[0]  # Flickr
            pic_id = url.split('/')[3]  # Mapillary
            try:
                pic_name = "{0}-{1}.jpg".format(table_name, pic_id)
                city = table_name.split('_')[0]
                year = table_name.split('_')[1]
                month = table_name.split('_')[2]
                datapath = os.path.join(storpath , city , year , month )
                if os.path.isdir(datapath):
                    filename = os.path.join(datapath, pic_name)
                else:
                    os.makedirs(datapath)
                    filename = os.path.join(datapath, pic_name)
                if os.path.exists(filename):
                    print 'aready download'
                else:
                    print 'downloading %s' % pic_name
                    img = requests.get(url)
                    f = open(filename,"wb")
                    f.write(img.content)
                    f.close()
            except Exception as e:
                print e

if __name__=="__main__":
    # result_dic = geturl("Mapillary")
    # url_download(result_dic)
    get_file_list(r'D:\MapillaryData\SourceData')
    for f in File_list:
        list = read_mapillary_file(f)
        for m in list :
            key = m[0]
            year = m[10]
            month = m[11]
            url = MAPILLARY_IM_RETRIEVE_URL % key
            pic_name = "london_"+year+"_"+month+"_"+key+".jpg"
            datapath = os.path.join(storpath,'london', year, month)
            if os.path.isdir(datapath):
                filename = os.path.join(datapath, pic_name)
            else:
                os.makedirs(datapath)
                filename = os.path.join(datapath, pic_name)
            if os.path.exists(filename):
                print 'aready download'
            else:
                print 'downloading %s' % pic_name
                try:
                    img = requests.get(url)
                    f = open(filename,"wb")
                    f.write(img.content)
                    f.close()
                except Exception as e:
                    print e




