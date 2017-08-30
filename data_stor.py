# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:36:45 2017

@author: d_xuan
"""
import os
import json
from utils.mysql_utils import *
table_name = 'london_2016-1'
creat_sql = "CREATE TABLE `"+table_name+"` (`id` varchar(10) CHARACTER SET utf8 DEFAULT NULL, `owner_id` varchar(15) CHARACTER SET utf8 DEFAULT NULL,`owner_name` varchar(30) CHARACTER SET utf8 DEFAULT NULL,`place_id` varchar(20) CHARACTER SET utf8 DEFAULT NULL, `lon` varchar(12) CHARACTER SET utf8 DEFAULT NULL, `lat` varchar(12) CHARACTER SET utf8 DEFAULT NULL, `title` text CHARACTER SET utf8, `description` text CHARACTER SET utf8, `tags` text CHARACTER SET utf8, `server` varchar(255) CHARACTER SET utf8 DEFAULT NULL, `secret` varchar(10) CHARACTER SET utf8 DEFAULT NULL, `url_o` varchar(80) CHARACTER SET utf8 DEFAULT NULL,`url_m` varchar(80) CHARACTER SET utf8 DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET= utf8"
insert_sql = "INSERT INTO `"+table_name+"` (id,owner_id,owner_name.place_id,lon,lat,title,description,tags,server,secret,url_o,url_m) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

def read_json_file(data_path):
    file_list = []
    if os.path.isfile(data_path):
        file_list.append(data_path)
    elif os.path.isdir(data_path):
        file_list = os.listdir(data_path)
        for f in file_list:
            new_dir = os.path.join(data_path,f)
            read_json_file(new_dir)
    return file_list

def read_file (data_path):
    data_file = open(data_path)
    content = data_file.readlines()
    flickr_list = []
    for string in content:
        flickr = json.loads(string)
        id = flickr["id"]
        owner_id = flickr["owner"]
        owner_name = flickr["ownername"]
        place_id = flickr["place_id"]
        lon = flickr["longitude"]
        lat = flickr["latitude"]
        title = flickr["title"]
        description = json.loads(flickr["description"])["_content"]
        tags = flickr["tags"]
        server = flickr["server"]
        secret = flickr["secret"]
        url_o = flickr["url_o"]
        url_m = flickr["url_m"]
        flickr_l = [id,owner_id,owner_name.place_id,lon,lat,title,description,tags,server,secret,url_o,url_m]
        flickr_list.append(flickr_l)
    return flickr_list




if __name__ == '__main__':
    #read_json_file('C:\\Users\\xgxy03\\Desktop\\data\\2016\\1\\1')
    print creat_sql

