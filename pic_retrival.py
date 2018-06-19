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
    selectsql = 'select {0},{1},{2},{3},{4},{5} from {6} where id = {7}'.format('description','tags','lon','lat','url_m','url_o',table_name,pic_id)
    print selectsql
    result = sql_select(db,selectsql)
    pic_dic = {'id':pic_id,'table_name':table_name,'description':'','tags':'','lon':'','lat':'','url_m':'','url_o':''}
    for pic_info in result:
        pic_dic['description'] = pic_info[0]
        pic_dic['tags'] = pic_info[1]
        pic_dic['lon'] = pic_info[2]
        pic_dic['lat']= pic_info[3]
        pic_dic['url_m'] = pic_info[4]
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
    get_file_list(r'D:\VGI_Data\building_demo\Hot place\Hampton Palace\analyze_files')
    total_num = len(File_list)
    for i in File_list:
        nl = i.split('\\')
        pic_name = nl[len(nl) - 1]
        pic_info = getPicinfo(pic_name)
        lat = pic_info['lat']
        lon = pic_info['lon']
        storfile.write(' '.join([pic_name,lon,lat]) + '\n')
        total_num -= 1
        print 'remain %d' % total_num

def copyPicDetailSQL():
    fl = os.listdir(r'D:\VGI_Data\total_building\err_img')
    list = []
    for pic_name in fl:
        if '.jpg' in pic_name:
            table_name = pic_name.split('-')[0]
            pic_id = pic_name.split('-')[1].split('.')[0]
            selectsql = 'select {0},{1},{2},{3},{4},{5} from {6} where id = {7}'.format('description', 'tags', 'lon',
                                                                                        'lat',
                                                                                        'url_m', 'url_o', table_name,
                                                                                        pic_id)
            print selectsql
            result = sql_select(db, selectsql)
            for pic_info in result:
                pic = [pic_id, table_name, pic_info[2], pic_info[3], pic_info[4], pic_info[5], pic_info[0], pic_info[1]]
                list.append(pic)
    insert_sql = "INSERT IGNORE INTO `london_building_pic_info" \
                 "` (id,table_name,lon,lat,url_m, url_o,description,tags)" \
                 " values (%s, %s, %s, %s, %s, %s, %s, %s)"
    patch_num = 1000  # 设置单次批量导入的数量
    index = len(list) / patch_num
    for i in range(index):
        print '---- start insert part ' + str(i) + ' ----'
        sql_insert_many(db, insert_sql, list[i * patch_num:(i + 1) * patch_num])
    print '---- start insert part ' + str(index) + ' ----'
    sql_insert_many(db, insert_sql, list[(i + 1) * patch_num:])

def tag_search():
    # 通过搜索tag方式获取图片数据
    datapath = r"D:\VGI_Data\building_demo\not hot place\Imperial War Museum\tag_select"
    selectsql = "select {0},{1},{2} from london_building_pic_info where tags like '%{3}%'".format("id","table_name", "url_m",
                                                                                              "imperialwarmuseum")
    print selectsql
    result = sql_select(db, selectsql)
    for pic_info in result:
        pic_name = pic_info[1] +"-"+pic_info[0]+ '.jpg'
        url = pic_info[2]
        try:
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
                f = open(filename, "wb")
                f.write(img.content)
                f.close()
        except Exception as e:
            print e

if __name__ == "__main__":
    #下载原图
    # dic = getpic_dic_list()
    # url_download(dic)

    #tag_search()

    # 获取图片tag,lat,lon等信息
    #rm = 0
    #tagfile = file(r"D:\VGI_Data\building_demo\Hot place\King's Cross\analyze_files\Hampton_Palace_tag.txt",'a+')
    picfile = file(r"D:\OSMData\building_points\Hampton_Court_Palace_w.txt",'a+')
    filelist = os.listdir(r"D:\VGI_Data\building_demo\Hot place\Hampton Palace")
    for img in filelist:
        if '.jpg' in img:
            pic_info = getPicinfo(img)
            lat = pic_info['lat']
            lon = pic_info['lon']
            tag =  pic_info['tags']
            # if 'nationalgallery' in tag or 'nationalgallery' in tag:
            #     rm += 1
            picfile.write(' '.join([img, lon, lat]) + '\n')
            # if tag!='':
            #     tagfile.write(tag + '\n')
    #tagfile.close()
    picfile.close()
    #print rm







