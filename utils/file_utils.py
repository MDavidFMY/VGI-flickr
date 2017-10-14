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
            line = ','.join([id,table_name,lon,lat])
            lines.append(line)
        elif data_form == 'list':
            building = content.replace('\n','')
            lines.append(building)
    return lines

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


if __name__ == "__main__":
    #从dic格式数据格式化为数据库可识别格式
    # pic_list = readFile(r'D:\VGI_Data\building_pic.txt','dic')
    # path = r'D:\VGI_Data\building_pic_dbf.txt'
    # storlist(pic_list,path)
    get_file_list(r'D:\VGI_Data\building')
    newstorpath = r'D:\VGI_Data\total_building'
    for i in File_list:
        nl = i.split('\\')
        pic_name = nl[len(nl) - 1]
        print pic_name
        newfile = os.path.join(newstorpath,pic_name)
        shutil.copyfile(i, newfile)

