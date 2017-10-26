# -*- coding: utf-8 -*-
"""
Created on 2017/9/7 10:31

@author: ding_x
"""
from utils.nltkwork import *
from utils.mysql_utils import *
import math
import os

datapath = r'D:\VGI_Data\tags'
storpath = r'D:\VGI_Data\tags'
def getContent(file_name,resultlist):
    files = open(os.path.join(datapath,file_name))
    try:
        contents = files.readlines()
        for content in contents:
            content = content.replace("\n","")
            result_list = content.split(' ')
            keyword_list = []
            for i in result_list:
                keyword_list.append(i)
            resultlist.extend(keyword_list)
    except Exception as e:
        print e

def getKeyWord(keyword_list):
    keyword_dic = {}
    for k in keyword_list:
        if keyword_dic.has_key(k):
            keyword_dic[k] = keyword_dic[k]+1
        else :
            keyword_dic[k] = 1
    keyword_dic = sorted(keyword_dic.items(), key=lambda item: item[1], reverse=True)
    return keyword_dic

def storresult(result):
    for k in result:
        resultfile = file(os.path.join(storpath,'resultfile.txt'),'a+')
        resultfile .write(k[0]+" " +str(k[1]))
        resultfile.write("\n")
    resultfile.close()

def tag_tf_idf(tags):
    dic = {}
    db = connect_sql("vgiwork")
    for content in tags:
        tag = content.split(' ')[0]
        count = float(content.split(' ')[1])
        select_all_tags =  'select count(*) from london_tags_all where tags like "%{}%"'.format(tag)
        print select_all_tags
        df = sql_select(db,select_all_tags)
        N = 135534
        for i in df:
            df = i [0]
        if float(df)!=0:
            idf = math.log(float(N)/float(df))
            tf = count/200478
            dic[tag] = tf*idf*100000
    dic = sorted(dic.items(), key=lambda item: item[1], reverse=True)
    return dic

if __name__=="__main__":
    # resultlist=[]
    # getContent('london_distinct_tags.txt', resultlist)
    # result = getKeyWord(resultlist)
    # storresult(result)

    f = file(os.path.join(datapath,'building_tag_counts.txt'))
    tags = f.readlines()
    result = tag_tf_idf(tags[:50])
    re = file(os.path.join(datapath,'resulttfidf.txt'),'a+')
    for i in result:
        re.write("%s %s" %(i[0],str(i[1]))+'\n')
    re.close()




