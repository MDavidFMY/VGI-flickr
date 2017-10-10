# -*- coding: utf-8 -*-
"""
Created on 2017/9/7 10:31

@author: ding_x
"""
from utils.nltkwork import *
import os

datapath = 'C:\\Users\\VGI-Group\\Desktop\\test'
storpath = 'C:\\Users\\d_x\\Desktop\\Flickr_contents'
def getContent(file_name,resultlist):
    files = open(os.path.join(datapath,file_name))
    try:
        contents = files.readlines()
        for content in contents:
            content = content.replace("\n","")
            result_list = nltk_main(content)
            keyword_list = []
            for i in result_list:
                if ' ' in i:
                    words = i.split(' ')
                    for keyword in words:
                        keyword_list.append(keyword)
                else :
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
        print k[0]
        print k[1]
    #     resultfile = file(os.path.join(storpath,'resultfile.txt'),'a+')
    #     resultfile .write(k+"   " +str(result[k]))
    #     resultfile.write("\n")
    # resultfile.close()

if __name__=="__main__":
    resultlist=[]
    getContent('london_tags.txt', resultlist)
    # result = getKeyWord(resultlist)
    # storresult(result)

    f = file(os.path.join(datapath, 'result.txt'),'a+')
    for i in resultlist:
        f.write(i+' ')
    f.close()



    #nltk_main("2002 london dorothy cafe african south band jazz dec masuka")




