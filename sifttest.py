# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:36:45 2017

@author: ding_x
"""
from download_pic import *
from utils.mysql_utils import *
import os
data_path = 'E:\\building\\used_labels\\apartment_building-outdoor\\'
db = connect_sql('vgiwork')

def getPicinfo(pic_name):
    table_name = pic_name.split('-')[0]
    pic_id = pic_name.split('-')[1][:11]
    selectsql = 'select {0},{1},{2},{3},{4},{5} from {6} where id = {7}'.format('title','description','tags','lon','lat','url_o',table_name,pic_id)
    print selectsql
    result = sql_select(db,selectsql)
    pic_dic = {'title':'','description':'','tags':'','lon':'','lat':'','url_o':''}
    for pic_info in result:
        pic_dic['title'] = pic_info[0]
        pic_dic['description'] = pic_info[1]
        pic_dic['tags'] = pic_info[2]
        pic_dic['lon'] = pic_info[3]
        pic_dic['lat']= pic_info[4]
        pic_dic['url_o'] = pic_info[5]
    return pic_dic

def getpic_dic_list():
    '''
    获取分类结果为建筑图片的原图下载链接
    :return:
    '''
    pic_list = os.listdir(data_path)
    result_dic = {}
    for pic_name in pic_list:
        table_name = pic_name.split('-')[0]
        if result_dic.has_key(table_name):
            pic_dic = getPicinfo(pic_name)
            if pic_dic['url_o'] !='':
                result_dic[table_name].append(pic_dic['url_o'])
        else:
            result_dic[table_name]=[]
    return result_dic

if __name__ == "__main__":
    dic = getpic_dic_list()
    f = open('E:\\building\\origin\\dic.txt')
    f = f.write(dic)
    url_download(dic)


