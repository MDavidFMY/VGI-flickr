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
File_list = []

def getPicinfo(pic_name):
    table_name = pic_name.split('-')[0]
    pic_id = pic_name.split('-')[1].split('.')[0]
    selectsql = 'select {0},{1},{2},{3},{4} from {5} where id = {6}'.format('description','tags','lon','lat','url_o',table_name,pic_id)
    print selectsql
    result = sql_select(db,selectsql)
    pic_dic = {'id':pic_id,'table_name':table_name,'description':'','tags':'','lon':'','lat':'','url_o':''}
    for pic_info in result:
        pic_dic['description'] = pic_info[0]
        pic_dic['tags'] = pic_info[1]
        pic_dic['lon'] = pic_info[2]
        pic_dic['lat']= pic_info[3]
        pic_dic['url_o'] = pic_info[4]
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

def get_file_list(data_path):
    '''
    迭代获取指定路径下所有文件
    :param data_path:
    :return:
    '''
    if os.path.isfile(data_path):
        File_list.append(data_path)
        #print data_path
    elif os.path.isdir(data_path):
        file_list = os.listdir(data_path)
        for f in file_list:
            new_dir = os.path.join(data_path,f)
            get_file_list(new_dir)

def get_building_pic_tags(storfile):
    get_file_list(r'D:\VGI_Data\building')
    total_num = len(File_list)
    for i in File_list:
        nl = i.split('\\')
        pic_name = nl[len(nl) - 1]
        pic_info = getPicinfo(pic_name)
        # tag = pic_info['tags']
        # if tag != '':
        #     storfile.write(tag + '\n')
        storfile.write(str(pic_info)+'\n')
        total_num -= 1
        print 'remain %d' % total_num
if __name__ == "__main__":
    #下载原图
    # dic = getpic_dic_list()
    # url_download(dic)

    #获取图片tag,lat,lon等信息
    storfile = file(r'D:\VGI_Data\building\building.txt','a+')
    get_building_pic_tags(storfile)
    storfile.close()





