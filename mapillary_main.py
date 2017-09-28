# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:36:45 2017

@author: ding_x
"""
import urllib,urllib2
from utils.grab_utils import *
url = 'https://a.mapillary.com/v3/images?client_id=ekcyWUdPNnkwSlRrMThjMVhWTFV0dzphYjRiMmE0MzM3YzQzMTAy&closeto={}&lookat={}&start_time={}&end_time={}&radius=5566'
pic_url = 'https://d1cuyjsrcm0gby.cloudfront.net/<IMAGE_KEY>/thumb-640.jpg'

'''
调用flickr api的search接口，实现flickr的自动抓取
'''
client_id='ekcyWUdPNnkwSlRrMThjMVhWTFV0dzphYjRiMmE0MzM3YzQzMTAy'

stor_path = "E:\\VGI_Data"



def grab_date_data(city_name,last_days):
    '''
    根据城市名，自动抓取该城市的指定日期的mapillary数据
    :param city_name:
    :param last_days:
    :return:
    '''
    add_one_day()
    city_coor_list = load_city_area(city_name)
    '''
    while last_days >0 :
        data_count = 0
        date = get_grab_date()
        print u'==============正在抓取日期：%s ==============' % (date["start_time"].split(" ")[0])
        datapath =  os.path.join(stor_path ,date['year'] ,date['month'],date['day'])
        if os.path.isdir(datapath):
            filename =os.path.join(datapath ,city_name + '.txt')
        else:
            os.makedirs(datapath)
            filename = os.path.join(datapath, city_name + '.txt')

        start_time = date["start_time"]
        min_time = convert_grab_date(start_time,'ISO')[0]
        max_time =  convert_grab_date(start_time,'ISO')[1]
        coor_index = 0
        for coor_index in range(len(city_coor_list)):
            coordinate = city_coor_list[coor_index]
            print u'----抓取%s第 %d 区域----'% (city_name,coor_index)
            err_num = 0
            params = urllib.urlencode(zip(['closeto', 'start_time', 'end_time', 'radius', 'lookat']))  #closeto--longitude,latitude .
            query = urllib2.urlopen(MAPILLARY_API_IM_SEARCH_URL + params).read()
            query = json.loads(query)
            coor = str(coordinate[0])[:5] + " " + str(coordinate[1])[:5]
            print u"抓取 %s 坐标为 : %s 的第 %d 页数据" % (city_name,coor,page_index)
            dic = json.loads(json_obj)
            if dic["stat"] == "ok":
                    pages = int(dic["photos"]["pages"])
                    total = int(dic["photos"]["total"])
                    photos = dic["photos"]["photo"]
                    # <-----抓取失败，重新抓取该区域该页面----->
                    if total == 0:
                        print u'<-----取空----->'
                        page_index -= 1
                        err_num += 1
                        if err_num > 3:
                            break
                        else:
                            continue
                    # <-----抓取成功----->
                    else:
                        # <-----页面只有一页，直接跳转下一区域----->
                        if pages == 1:
                            sto_photos(photos, filename)
                            break
                        else:
                            sto_photos(photos, filename)
            else:
                    print dic["stat"]
            print u'该区域共 %d 条数据' % (total)
            data_count += total
            except Exception as e:
                print e
        data_static(city_name,date["start_time"].split(" ")[0],data_count)
        last_days -= 1
        add_one_day()
        '''
if __name__=="__main__":
    city_name = raw_input("请输入所需要下载的城市名称：")
    city_name = 'london'
    last_days = 2
    grab_date_data(city_name,last_days)
