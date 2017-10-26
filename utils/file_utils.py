# -*- coding: utf-8 -*-
"""
Created on 2017/10/12 22:49

@author: ding_x
"""
import shutil
import os
File_list = []

def readFile(path,data_form):
    '''
    解析文本（dic、list），提取字典中字段
    :param path:
    :param data_form:
    :return:
    '''
    f = file(path)
    lines = []
    contents = f.readlines()
    for content in contents:
        if data_form == 'dic':
            photo_dic = eval(content)
            id = photo_dic['id']
            table_name = photo_dic['table_name']
            lat = photo_dic['lat']
            lon = photo_dic['lon']
            tags = photo_dic['tags']
            line = ','.join([id,table_name,lon,lat,tags])
            lines.append(line)
        elif data_form == 'list':
            building = content.replace('\n','')
            lines.append(building)
    return lines

def readFiledic(path,f_type):
    '''
    解析文本（dic、list），提取字典中字段
    :param path:
    :param data_form:
    :return:
    '''
    f = file(path)
    dic = {}
    contents = f.readlines()
    err = 0
    for content in contents:
        content = content.replace('\n','')
        if f_type == 'building':
            id = content.split(',')[0]
            name = content.split(',')[1]
            type = content.split(',')[2]
            lon = content.split(',')[3]
            lat = content.split(',')[4]
            dic[id] = {'name':name,'type':type,'lon':lon,'lat':lat}
        else :
            id = content.split(',')[0]
            table_name = content.split(',')[1]
            lon = content.split(',')[2]
            lat = content.split(',')[3]
            dic[id] = {'table_name':table_name,'lon':lon,'lat':lat}
    return dic

def storlist(list,path):
    f = file(path,'a+')
    for i in list :
        f.write(str(i)+'\n')
    f.close()

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

def getPareInfo():
    # 统计所有图片数量大于1的建筑
    f = file(r'D:\VGI_Data\range 200\building_buffer\osm-flickr_picname.txt')
    pic_dic = readFiledic(r'D:\VGI_Data\building_pic_dbf.txt', 'pic')
    building_dic = readFiledic(r'D:\OSMData\greater-london-latest-free.shp\building_with_name.txt', 'building')
    contents = f.readlines()
    building_list = []
    pic_temp_dic = {}
    for content in contents:
        building_pic = eval(content)
        building = building_pic.keys()[0]
        pic_name_list = building_pic[building]
        if len(pic_name_list) > 1:
            building_name = building_dic[building]['name']
            type = building_dic[building]['type']
            lon = building_dic[building]['lon']
            lat = building_dic[building]['lat']
            line = ','.join([building, building_name, type, lon, lat])
            building_list.append(line)
            for pic_name in pic_name_list:
                pic_name = pic_name.split('-')[1]
                pic_temp_dic[pic_name] = pic_dic[pic_name]
    pic_list = []
    for key in pic_temp_dic.keys():
        table_name = pic_temp_dic[key]['table_name']
        lon = pic_temp_dic[key]['lon']
        lat = pic_temp_dic[key]['lat']
        line = ','.join([key, table_name, lon, lat])
        pic_list.append(line)
    return pic_list

def getName_tagsInfo():
    # 统计所有图片数量大于1的建筑
    f = file(r'D:\VGI_Data\range 200\pic_buffer\name_in_tags.txt')
    pic_dic = readFiledic(r'D:\VGI_Data\building_pic_dbf.txt', 'pic')
    building_dic = readFiledic(r'D:\OSMData\greater-london-latest-free.shp\building_with_name.txt', 'building')
    contents = f.readlines()
    building_list = []
    building_temp_dic = {}
    for content in contents:
        building_pic = eval(content)
        pic = building_pic.keys()[0]
        table_name = pic_temp_dic[key]['table_name']
        lon = pic_temp_dic[key]['lon']
        lat = pic_temp_dic[key]['lat']
        line = ','.join([key, table_name, lon, lat])
        building_list.append(line)
        for building_name in building_id_list:
            building_name = building_name.split('-')[1]
            building_temp_dic[pic_name] = building_dic[pic_name]
    pic_list = []
    for key in pic_temp_dic.keys():
        building_id_list = building_pic[building]
        building_name = building_dic[building]['name']
        type = building_dic[building]['type']
        lon = building_dic[building]['lon']
        lat = building_dic[building]['lat']
        line = ','.join([building, building_name, type, lon, lat])
        pic_list.append(line)
    return pic_list

if __name__ == "__main__":
    #从dic格式数据格式化为数据库可识别格式
    # pic_list = readFile(r'D:\VGI_Data\building_pic.txt','dic')
    # path = r'D:\VGI_Data\building_pic_dbf.txt'
    # storlist(pic_list,path)

    #将所有建筑图片存放至一个文件夹
    # get_file_list(r'D:\VGI_Data\building')
    # newstorpath = r'D:\VGI_Data\total_building'
    # for i in File_list:
    #     nl = i.split('\\')
    #     pic_name = nl[len(nl) - 1]
    #     print pic_name
    #     newfile = os.path.join(newstorpath,pic_name)
    #     shutil.copyfile(i, newfile)

    # 统计所有图片数量大于1的建筑
    pic_list = getPareInfo()
    storlist(pic_list,r'D:\VGI_Data\range 200\building_buffer\building_buffer_pic.txt')



