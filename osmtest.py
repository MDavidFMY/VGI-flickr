# -*- coding: utf-8 -*-
"""
Created on 2017/9/11 11:45

@author: ding_x
"""
from utils.mysql_utils import *
from utils.grab_utils import *
from utils.file_utils import *
from pic_retrival import *
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
    '''
    获取osmbuilding周围的照片
    :param buffer_range:
    :return:
    '''
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

def cal_pic_buffer(buffer_range):
    '''
    获取照片周围的building,并比较tag是否符合building属性
    :param buffer_range:
    :return:
    '''
    photos = readFile(r'D:\VGI_Data\building_pic.txt', 'dic')
    buildings = readFile(r'D:\OSMData\greater-london-latest-free.shp\building_with_name.txt', 'list')
    name_list = []
    type_list = []
    buffer_range = float(buffer_range)
    total = len(photos)
    for photo in photos:
        photo = photo.split(',')
        picid = photo[0]
        table_name = photo[1]
        pic_name = table_name + "-" + picid
        plat = float(photo[3])
        plon = float(photo[2])
        tags = photo[4]
        #dic = {}
        dic_type ={}
        dic_name = {}
        for building in buildings:
            building = building.split(',')
            osmid = building[0]
            building_name = building[1].lower()
            building_type = building[2].replace('_',' ')
            blat = float(building[4])
            blon = float(building[3])
            bbox = getbbox(plon, plat, buffer_range)
            if inbbox(blon,blat,bbox):
                distance = get_distance_hav(plat,plon,blat,blon)
                if distance <buffer_range:
                    if building_type in tags and building_type!='':
                        dic_type.setdefault(pic_name, []).append(osmid)
                    if building_name in tags:
                        dic_name.setdefault(pic_name, []).append(osmid)
        total -= 1
        print 'remain %d ' % total
        if  len(dic_type) != 0 :
            type_list.append(dic_type)
        if  len(dic_name) != 0 :
            name_list.append(dic_name)
    storlist(type_list, r'D:\VGI_Data\range 600\pic_buffer\type_in_tags.txt')
    storlist(name_list, r'D:\VGI_Data\range 600\pic_buffer\name_in_tags.txt')

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
# 求方差
def calDx(list,path,building):
    length = len(list)
    nlist = set(list)
    Dx = 0.0
    Ex = 0.0
    distance_file = file(os.path.join(path,"distance.txt"), 'a+')
    d1 = 0
    d2 = 0
    d3 = 0
    d4 = 0
    d5 = 0
    d6 = 0
    d7 = 0
    for i in nlist:
        n = list.count(i)
        distance = i*10
        distance_file.write("%s %d" %(distance,n)+'\n')
        if distance>0 and distance<50:
            d1 += n
        elif distance>=50 and distance<100:
            d2 +=n
        elif distance>=100 and distance<150:
            d3 +=n
        elif distance>=150 and distance<200:
            d4 +=n
        elif distance>=200 and distance<250:
            d5 +=n
        elif distance>=250 and distance<300:
            d6 +=n
        elif distance>300 and distance<1000:
            d7 +=n

        p = float(n)/float(length)
        Ex += i * p
    for i in nlist:
        n = list.count(i)
        p = float(n) / float(length)
        Dx = (i - Ex)*(i-Ex)*p
    result_dic = {
        "name":building,
        "data": [
            {"value": d7, "name": '>300'},
            {"value": d6, "name": '250-300'},
            {"value": d5, "name": '200-250'},
            {"value": d4, "name": '150-200'},
            {"value": d3, "name": '100-150'},
            {"value": d2, "name": '50-100'},
            {"value": d1, "name": '0-50'},
        ]
    }
    # distance_file.write(str(result_dic)+'\n')
    # distance_file.write("Ex: %f, Dx: %f" % (Ex,Dx))
    # distance_file.close()
    print result_dic

def cal_min_dis(dic):  #buckingham palace 51.500833,-0.141944 Ex: 156.652688, Dx: 736.025349 # St Paul's Cathedral 51.513611,-0.098056 Ex: 112.665946, Dx: 818.898774 # British Museum  -.127146,51.519452 Ex: 107.052083, Dx: 8.289987
    for building in dic :
        blon = dic[building][1]
        blat = dic[building][0]
        path = os.path.join(r"D:\VGI_Data\building_demo\Hot place",building)
        pics = os.listdir(path)
        zeroCount = len(os.listdir(os.path.join(path,'in')))
        dis_list = []
        for i in range(zeroCount):
            dis_list.append(0)
        for pic in pics:
            if pic.endswith('.jpg'):
                lat = float(getPicinfo(pic)['lat'])
                lon = float(getPicinfo(pic)['lon'])
                dis_list.append( int(get_distance_hav(blat,blon,lat,lon))/10)
        dis_list.sort()
        print dis_list
        calDx(dis_list,os.path.join(path,"analyze_files"),building)

if __name__=="__main__":
    #formatjson(prov_file_path)
    # 计算距离分布
    building_dic ={"British Museum":(51.519459,-0.126931),"Buckingham Palace":(51.500833,-0.141944),"City Hall":(51.504722,-0.078333),
                    "Hampton Palace":(51.403333,-0.3375),"Imperial War Museum":(51.49619,-0.10855),"National Gallery":(51.5086, -0.1283),
                    "Royal Albert Hall":(51.500944,-0.177436),"St Paul's Cathedral":(51.513611,-0.098056),"Westminster Abbey":(51.499444,-0.1275)}
    #building_dic = {"Hampton Palace": (51.403333, -0.3375)}
    cal_min_dis(building_dic)
    #
    # #cal_building_buffer(500)
    # # #按osmid储存pic
    # # sourcepath = r'D:\VGI_Data\total_building'
    # # storpath = r'D:\VGI_Data\osm-flickr'
    # # storPicbyOsmid(sourcepath,storpath)
    #
    #
    # # #移动建筑物内部照片
    # path = r"D:\VGI_Data\building_demo\Hot place\Hampton Palace"
    # newpath = r"D:\VGI_Data\building_demo\Hot place\Hampton Palace\in"
    # f = file(r"D:\OSMData\greater-london-latest-free.shp\result\Hampton Court Palace\inthebuilding.txt")
    # points = f.readlines()
    # for p in points:
    #     picname = p.split(',')[1]
    #     shutil.move(os.path.join(path, picname), os.path.join(newpath, picname))
