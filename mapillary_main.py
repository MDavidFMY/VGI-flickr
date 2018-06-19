# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:36:45 2017

@author: ding_x
"""
import urllib,urllib2
from utils.grab_utils import *
MAPILLARY_API_IM_SEARCH_URL = 'https://a.mapillary.com/v3/images?client_id=ekcyWUdPNnkwSlRrMThjMVhWTFV0dzphYjRiMmE0MzM3YzQzMTAy&'
MAPILLARY_IM_RETRIEVE_URL = 'https://d1cuyjsrcm0gby.cloudfront.net/%s/thumb-1024.jpg'

'''
调用flickr api的search接口，实现flickr的自动抓取
'''
client_id='ekcyWUdPNnkwSlRrMThjMVhWTFV0dzphYjRiMmE0MzM3YzQzMTAy'

stor_path = r"D:\MapillaryData\SourceData"



def grab_date_data(city_name,last_days):
    '''
    根据城市名，自动抓取该城市的指定日期的mapillary数据
    :param city_name:
    :param last_days:
    :return:
    '''
    city_coor_list = load_city_area(city_name)

    while last_days >0 :
        data_count = 0
        date = get_grab_date()
        print u'==============正在抓取日期：%s ==============' % (date["start_time"].split(" ")[0])
        datapath =  os.path.join(stor_path ,date['year'] ,date['month'])
        if os.path.isdir(datapath):
            filename =os.path.join(datapath ,city_name + '.txt')
        else:
            os.makedirs(datapath)
            filename = os.path.join(datapath, city_name + '.txt')

        start_time = date["start_time"]
        min_time = convert_grab_date(start_time,'ISO')[0]
        max_time =  convert_grab_date(start_time,'ISO')[1]
        coor_index = 0
        data_count = 0
        for coor_index in range(len(city_coor_list)):
            coordinate = city_coor_list[coor_index]
            print u'----抓取%s第 %d 区域----'% (city_name,coor_index)
            coordinate = "%f,%f" %(city_coor_list[coor_index][0],city_coor_list[coor_index][1])
            try:
                err_num = 0
                params = urllib.urlencode(zip(['closeto', 'lookat', 'start_time', 'end_time', 'per_page', 'radius'],
                                              [coordinate, coordinate, min_time, max_time, 1000,5566]))
                query = urllib2.urlopen(MAPILLARY_API_IM_SEARCH_URL + params).read()
                query = json.loads(query)
                images = query["features"]
                #coor = str(coordinate[0])[:5] + " " + str(coordinate[1])[:5]
                if len(images) >= 1000:
                    print "count over 1000"
                    date_log = "%s-%s-%s" % (date['year'],date['month'] ,date["date"])
                    e_log(city_name,date_log,coordinate)
                elif len(images)==0:
                    print "no data here"
                else :
                    sto_photos(images,filename)
                    print u'该区域共 %d 条数据' % (len(images))
                    data_count += len(images)
            except Exception as e:
                print e
        data_static(city_name, date["start_time"].split(" ")[0],data_count)
        last_days -= 1
        add_one_day()

if __name__=="__main__":
    city_name = 'london'
    last_days = 365
    grab_date_data(city_name, last_days)
