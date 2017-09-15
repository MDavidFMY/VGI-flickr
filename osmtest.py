# -*- coding: utf-8 -*-
"""
Created on 2017/9/11 11:45

@author: ding_x
"""
from utils.mysql_utils import *
from utils.grab_utils import *
import os

prov_file_path = 'C:\\Users\\d_x\\Desktop\\prov.txt'
def formatjson(prov_file_path):
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

if __name__=="__main__":
    tablename = ['road_identity','place']
    formatjson(prov_file_path)




