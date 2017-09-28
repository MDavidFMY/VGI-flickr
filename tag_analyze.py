# -*- coding: utf-8 -*-
"""
Created on 2017/9/7 10:31

@author: ding_x
"""
from utils.nltkwork import *
import os

datapath = 'C:\\Users\\VGI-Group\\Desktop\\test'
storpath = 'C:\\Users\\d_x\\Desktop\\Flickr_contents'
def getContent(file_name):
    files = open(os.path.join(datapath,file_name))
    try:
        contents = files.readlines()
        for content in contents:
            content = content.replace("\n","")
            result_list = nltk_main(content)
            print len(result_list)
            # result = getKeyWord(result_list)
            # storresult(result)
    except Exception as e:
        print e

def getKeyWord(keyword_list):
    keyword_dic = {}
    for k in keyword_list:
        if keyword_dic.has_key(k):
            keyword_dic[k] = keyword_dic[k]+1
        else :
            keyword_dic[k] = 0
    keyword_dic = sorted(keyword_dic.items(),key=lambda item:item[1])
    return keyword_dic

def storresult(result):
    for k in result:
        print k
        print result[k]
        #resultfile = file(os.path.join(storpath,'resultfile.txt'),'a+')
    #     resultfile .write(k+"   " +str(result[k]))
    #     resultfile.write("\n")
    # resultfile.close()

if __name__=="__main__":
    getContent('test.txt')

    #nltk_main("2002 london dorothy cafe african south band jazz dec masuka")




