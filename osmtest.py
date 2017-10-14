# -*- coding: utf-8 -*-
"""
Created on 2017/9/11 11:45

@author: ding_x
"""
from utils.mysql_utils import *
from utils.grab_utils import *
from utils.file_utils import *
import utils.shapefile as shapefile
import os
import shutil

from math import *
EARTH_RADIUS = 6371
prov_file_path = 'C:\\Users\\d_x\\Desktop\\prov.txt'
stor_path = r'D:\OSMData\greater-london-latest-free.shp'
def formatjson(prov_file_path):
    '''
    统计各省份poi点数量
    :param prov_file_path:
    :return:
    '''
    db = connect_sql('shpdb')
    provFile = open(prov_file_path)
    provlist = provFile.readlines()
    json_dic = {}
    for prov_a in provlist :
        prov_a =  prov_a.replace("\n", "")
        prov_a = prov_a.split('	')
        prov_e = prov_a[0]
        prov_c = prov_a[1]
        selectsql = "select count(*) from pois_identity where NAME_1 ='%s';" % prov_e
        #selectsql= "select count(*) from traffic_identity where NAME_1 ='%s' and code = '%s';" % (prov_e,'5111')
        count =  sql_select(db,selectsql)[0][0]
        #data = "{name:'%s',value:%s}," % (prov_c, count)
        data = prov_c +" " + str(count)
        print data

def getBuildingCoor():
    '''
    提取shp文件中面要素坐标信息，并计算其中心点
    :return:
    '''
    shp_file = open(r"D:\OSMData\greater-london-latest-free.shp\gis.osm_buildings_a_free_1.shp", "rb")
    dbf_file = open(r"D:\OSMData\greater-london-latest-free.shp\gis.osm_buildings_a_free_1.dbf", "rb")
    shapes = shapefile.Reader(shp=shp_file, dbf=dbf_file)
    shapep = shapes.shapes()
    recordp = shapes.records()
    shape_list = []
    f = file(os.path.join(stor_path,'london_building.txt'),'a+')
    total = len(recordp)
    for i in range(total):
        osmid = recordp[i][0]
        name = recordp[i][3].replace(',','')
        type = recordp[i][4].replace(',','')
        point_list = shapep[i].points
        centerPoint = getCenterPoint(point_list)
        lon = '%f'%centerPoint[0]
        lat = '%f'%centerPoint[1]
        building =  ','.join([osmid,name,type,lon,lat])
        f.write(building+'\n')
        print 'remain %d' % (total - i -1)
    f.close()

def getCenterPoint(point_list):
    point_num = len(point_list)
    lat_sum = 0.0
    lon_sum = 0.0
    centerPoint = []
    for i in point_list:
        lat_sum += i[1]
        lon_sum += i[0]
    centerPoint.append(lon_sum/point_num)
    centerPoint.append(lat_sum/point_num)
    return centerPoint

def hav(theta):
    s = sin(theta / 2)
    return s * s

def get_distance_hav(lat0, lng0, lat1, lng1):
    "用haversine公式计算球面两点间的距离。"
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))*1000
    return distance

def cal_building_buffer(buffer_range):
    photos = readFile(r'D:\VGI_Data\building_pic.txt', 'dic')
    buildings = readFile(r'D:\OSMData\greater-london-latest-free.shp\building_with_name.txt', 'list')
    result_list = []
    buffer_range = float(buffer_range)
    total = len(buildings)
    for building in buildings:
        dic = {}
        building = building.split(',')
        osmid = building[0]
        blat = float(building[4])
        blon = float(building[3])
        bbox = getbbox(blon,blat,buffer_range)
        for photo in photos:
            photo = photo.split(',')
            picid = photo[0]
            table_name = photo[1]
            pic_name =table_name+"-"+picid
            plat = float(photo[3])
            plon = float(photo[2])
            if inbbox(plon,plat,bbox):
                distance = get_distance_hav(plat,plon,blat,blon)
                if distance <buffer_range:
                    dic.setdefault(osmid, []).append(pic_name)
        total -= 1
        print 'remain %d ' % total
        if  len(dic) != 0 :
            result_list.append(dic)
    storlist(result_list,r'D:\VGI_Data\osm-flickr_picname.txt')

def getbbox(lon,lat,distance):
    tempcoor = distance*0.001/get_distance_hav(0.001,0.001,0.002,0.001)
    dic={'minlat':lat-tempcoor,'minlon':lon-tempcoor,'maxlat':lat+tempcoor,'maxlon':lon+tempcoor}
    return dic

def inbbox(lon,lat,bbox):
    minlat = bbox['minlat']
    maxlat = bbox['maxlat']
    minlon = bbox['minlon']
    maxlon = bbox['maxlon']
    return minlat<lat<maxlat and minlon<lon<maxlon

def storPicbyOsmid(sourcepath,storpath):
    f = file(r'D:\VGI_Data\osm-flickr_picname.txt')
    relation_list = f.readlines()
    for dic in relation_list:
        dic = eval(dic)
        for osmid in dic.keys():
            pic_list = dic[osmid]
            for pic in pic_list:
                sourcefile = os.path.join(sourcepath,pic+'.jpg')
                newpath = os.path.join(storpath,osmid)
                if os.path.isdir(newpath):
                    targetfile = os.path.join(newpath,pic+'.jpg')
                    shutil.copyfile(sourcefile,targetfile)
                else:
                    os.makedirs(newpath)
                    targetfile = os.path.join(newpath, pic + '.jpg')
                    shutil.copyfile(sourcefile, targetfile)

if __name__=="__main__":
    #formatjson(prov_file_path)
    # 计算缓冲区
    # cal_building_buffer(200)
    #按osmid储存pic
    sourcepath = r'D:\VGI_Data\total_building'
    storpath = r'D:\VGI_Data\osm-flickr'
    storPicbyOsmid(sourcepath,storpath)





