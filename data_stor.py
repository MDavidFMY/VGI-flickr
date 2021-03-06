# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:36:45 2017

@author: ding_x
"""
import os
import json
from utils.mysql_utils import *
File_list = []

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

def read_flickr_file (data_path,grabdate):
    '''
    json数据的解析，提取所需字段
    :param data_path:
    :param grabdate:
    :return:
    '''
    print 'extracting '+ data_path
    data_file = open(data_path)
    content = data_file.readlines()
    flickr_list = []
    for string in content:
        flickr = json.loads(string)
        id = flickr["id"]
        owner_id = flickr["owner"]
        owner_name = flickr["ownername"].encode("utf-8")
        if flickr.has_key("place_id"):
            place_id = flickr["place_id"]
        else:
            place_id = ''.decode()
        lon = flickr["longitude"]
        lat = flickr["latitude"]
        title = flickr["title"].encode("utf-8")
        description = flickr["description"]["_content"].encode("utf-8")
        tags = flickr["tags"].encode("utf-8")
        server = flickr["server"]
        secret = flickr["secret"]
        dateupload = flickr["dateupload"]
        if flickr.has_key("url_o"):
            url_o = flickr["url_o"]
        else:
            url_o = ''.decode()
        if flickr.has_key("url_m"):
            url_m = flickr["url_m"]
        else:
            url_m = ''.decode()
        flickr_l = [id,owner_id,owner_name,place_id,lon,lat,title,description,tags,server,secret,url_o,url_m,dateupload,grabdate]
        flickr_list.append(flickr_l)
    return flickr_list

def stor_data_by_month(file_list,city_name):
    '''
    将从文件中提取出的数据列表，批量存入数据库
    :param file_list:
    :param city_name:
    :return:
    '''
    db = connect_sql("vgiwork")
    for f in file_list :
        f_s = f.split("data")[1].split(city_name)
        date = f_s[0].split('\\')
        year = date[1]
        month = date[2]
        day = date[3]
        table_name = city_name+"_"+year+"_"+month
        creat_sql = "CREATE TABLE `" + table_name + "` (`id` varchar(11) CHARACTER SET utf8 DEFAULT NULL, " \
                                                    "`owner_id` varchar(15) CHARACTER SET utf8 DEFAULT NULL," \
                                                    "`owner_name` varchar(50) CHARACTER SET utf8 DEFAULT NULL," \
                                                    "`place_id` varchar(20) CHARACTER SET utf8 DEFAULT NULL," \
                                                    " `lon` varchar(12) CHARACTER SET utf8 DEFAULT NULL, " \
                                                    "`lat` varchar(12) CHARACTER SET utf8 DEFAULT NULL," \
                                                    " `title` text CHARACTER SET utf8," \
                                                    " `description` text CHARACTER SET utf8," \
                                                    " `tags` text CHARACTER SET utf8, " \
                                                    "`server` varchar(5) CHARACTER SET utf8 DEFAULT NULL, " \
                                                    "`secret` varchar(10) CHARACTER SET utf8 DEFAULT NULL," \
                                                    " `url_o` varchar(80) CHARACTER SET utf8 DEFAULT NULL," \
                                                    "`url_m` varchar(80) CHARACTER SET utf8 DEFAULT NULL ," \
                                                    "`dateupload` varchar(10) CHARACTER SET utf8 DEFAULT NULL ," \
                                                    "`grabdate` varchar(2) CHARACTER SET utf8 DEFAULT NULL ," \
                                                    "PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET= utf8"
        insert_sql = "INSERT IGNORE INTO `" + table_name + \
                     "` (id,owner_id,owner_name,place_id,lon,lat,title,description,tags,server,secret,url_o,url_m,dateupload,grabdate)" \
                     " values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        if table_exist(db,table_name,"vgiwork") ==0:
            creat_table(db, creat_sql, table_name)
        flickr_list = read_flickr_file(f,day)
        patch_num = 3000 #设置单次批量导入的数量
        index = len(flickr_list)/patch_num
        for i in range(index):
            print '---- start insert '+f+' part '+str(i)+' ----'
            sql_insert_many(db,insert_sql,flickr_list[i*patch_num:(i+1)*patch_num])
        print '---- start insert ' + f + ' part ' + str(index) + ' ----'
        sql_insert_many(db, insert_sql, flickr_list[(i + 1) * patch_num:])
    close_sql(db)

def read_mapillary_file(data_path):
    '''
    json数据的解析，提取所需字段
    :param data_path:
    :return:
    '''
    print 'extracting '+ data_path
    data_file = open(data_path)
    content = data_file.readlines()
    mapillary_list = []
    for string in content:
        image = json.loads(string)
        properties = image["properties"]
        ca = properties["ca"]
        camera_make = properties["camera_make"]
        camera_model = properties["camera_model"]
        captured_at = str(properties["captured_at"])
        year = captured_at.split('T')[0].split('-')[0]
        month = captured_at.split('T')[0].split('-')[1]
        date = captured_at.split('T')[0].split('-')[2]
        time =captured_at.split('T')[1].split('.')[0]
        key = properties["key"]
        pano = str(properties["pano"])
        user_key = properties["user_key"]
        username = properties["username"]
        geometry = image["geometry"]
        coordinates = geometry["coordinates"]
        lat = coordinates[1]
        lon = coordinates[0]
        mapillary = [key,user_key,username,camera_make,camera_model,ca,lon,lat,pano,captured_at,year,month,date,time]
        #print mapillary
        mapillary_list.append(mapillary)
    return mapillary_list

def stor_mapillary_data_by_month(file_list,city_name):
    '''
    将从文件中提取出的数据列表，批量存入数据库
    :param file_list:
    :param city_name:
    :return:
    '''
    db = connect_sql("vgiwork")
    table_name = city_name + '_mapillary'
    creat_sql = "CREATE TABLE `" + table_name + "` (`key` varchar(22) CHARACTER SET utf8 Not NULL, " \
                                                "`user_key` varchar(22) CHARACTER SET utf8 DEFAULT NULL," \
                                                "`username` varchar(50) CHARACTER SET utf8 DEFAULT NULL," \
                                                "`camera_make` varchar(20) CHARACTER SET utf8 DEFAULT NULL," \
                                                "`camera_model` varchar(20) CHARACTER SET utf8 DEFAULT NULL," \
                                                "`ca` varchar(20) CHARACTER SET utf8 DEFAULT NULL," \
                                                "`lon` varchar(20) CHARACTER SET utf8 DEFAULT NULL, " \
                                                "`lat` varchar(20) CHARACTER SET utf8 DEFAULT NULL," \
                                                "`pano` varchar(5) CHARACTER SET utf8 DEFAULT NULL, " \
                                                "`captured_at` varchar(24) CHARACTER SET utf8 DEFAULT NULL ," \
                                                "`year` varchar(2) CHARACTER SET utf8 DEFAULT NULL ," \
                                                "`month` varchar(2) CHARACTER SET utf8 DEFAULT NULL ," \
                                                "`date` varchar(2) CHARACTER SET utf8 DEFAULT NULL ," \
                                                "`time` varchar(8) CHARACTER SET utf8 DEFAULT NULL ," \
                                                "`gvi` varchar(8) CHARACTER SET utf8 DEFAULT NULL ," \
                                                "PRIMARY KEY (`key`)) ENGINE=InnoDB DEFAULT CHARSET= utf8"

    if table_exist(db, table_name, "vgiwork") == 0:
        creat_table(db, creat_sql, table_name)
    for f in file_list :
        insert_sql = "INSERT IGNORE INTO `" + table_name + \
                     "` (key,user_key,username,camera_make,camera_model,ca,lon,lat,pano,captured_at,year,month,date,time)" \
                     " values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mapillary_list = read_mapillary_file(f)
        print '---- start insert '+f+' ----'
        sql_insert_many(db,insert_sql,mapillary_list)
    close_sql(db)


if __name__ == '__main__':
    # # Flickr
    # get_file_list('C:\\Users\\xgxy03\\Desktop\\data\\2016')
    # stor_data_by_month(File_list,"london")

    # Mapillary
    get_file_list(r'D:\MapillaryData\SourceData\2015\1')
    stor_mapillary_data_by_month(File_list,"london")







