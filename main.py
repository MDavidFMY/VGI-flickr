# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 11:36:45 2017

@author: d_xuan
"""
import flickrapi

from utils.grab_utils import *

api_key = '5b3bf647e7b5ad46255ba8b8ebad6a4e'
api_secret= 'dc6af0c6dad6c128'
flickr=flickrapi.FlickrAPI(api_key,api_secret,cache=True,format='json')
stor_path = "C:\\Users\\xgxy03\\Desktop\\data"



def grab_date_data(city_name,last_days):
    city_coor_list = load_city_area(city_name)
    while last_days >0 :
        data_count = 0
        date = get_grab_date()
        print u'==============正在抓取日期：' + date["start_time"].split(" ")[0]+u'=============='
        datapath =  stor_path + '\\' + date['year'] + '\\' + date['month'] + '\\' + date['day']
        if os.path.isdir(datapath):
            filename =datapath + '\\' +city_name + '.txt'
        else:
            os.makedirs(datapath)
            filename = datapath + '\\' + city_name + '.txt'

        start_time = date["start_time"]
        min_time = convert_grab_date(start_time)[0]
        max_time =  convert_grab_date(start_time)[1]
        coor_index = 0
        for coor_index in range(len(city_coor_list)):
            coordinate = city_coor_list[coor_index]
            print u'----抓取'+city_name+ u'第 ' + str(coor_index) + u' 区域----'
            err_num = 0
            page_index = 1
            pages = 1
            try:
                while page_index <= pages:
                    json_obj = flickr.photos.search(page=page_index, perpage=200, radius=5.566, has_geo=1,
                                                    lat=coordinate[0], lon=coordinate[1], min_upload_date=min_time,
                                                    max_upload_date=max_time,
                                                    extras='description,date_upload,owner_name,last_update,geo,tags,machine_tags,url_m,url_c,url_o')
                    coor = str(coordinate[0])[:5] + " " + str(coordinate[1])[:5]
                    print u"抓取 " + city_name + u" 坐标为 : " + coor + u" 的第 " + str(page_index) + u" 页数据"
                    page_index += 1
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
                print u'该区域共' + str(total) + u'条数据'
                data_count += total
            except Exception as e:
                print e
        data_static(city_name,date["start_time"].split(" ")[0],data_count)
        last_days -= 1
        add_one_day()

if __name__=="__main__":
    # city_name = raw_input("请输入所需要下载的城市名称：")
    city_name = 'london'
    last_days = 2
    grab_date_data(city_name,last_days)