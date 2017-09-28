# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:36:45 2017

@author: ding_x
"""
from utils.mysql_utils import *

def getPicinfo(pic_name):
    db = connect_sql('vgiwork')
    table_name = pic_name.split('-')[0]
    pic_id = pic_name.split('-')[0][:10]
    selectsql = 'select {0},{1},{2},{3},{4} from {5}'.format('title','description','tags','lon','lat',table_name)
    print selectsql
    result = sql_select(db,selectsql)
    pic_dic = {'title':'','description':'','tags':'','lon':'','lat':''}
    for pic_info in result:
        pic_dic['title'] = pic_info[0]
        pic_dic['description'] = pic_info[1]
        pic_dic['tags'] = pic_info[2]
        pic_dic['lon'] = pic_info[3]
        pic_dic['lat']= pic_info[4]
    return pic_dic

if __name__=="__main__":
    pic_dic = getPicinfo('london_2016_5-9796467635.jpg')
    print pic_dic['description']

