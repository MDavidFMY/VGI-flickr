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
storpath = 'D:\\VGI_Data\\Flickr_pic'
def geturl():
    result_dic = {}
    db = connect_sql('vgiwork')
    month = 4
    while month <= 6:
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
    return result_dic

def url_download(result_dic):
    for table_name in result_dic:
        for url in result_dic[table_name]:
            pic_id = url.split('/')[4].split('_')[0]
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
    result_dic = geturl()
    url_download(result_dic)

