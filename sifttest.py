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
    selectsql = 'select {0},{1},{2},{3},{4} from {table_name}'.format('title','description','tags','lon','lat',table_name)
    result = sql_select(db,selectsql)
    for pic_info in result:
        title = pic_info[0]
        description = pic_info[1]
        tags = pic_info[2]
        lon = pic_info[3]
        lat = pic_info[4]


