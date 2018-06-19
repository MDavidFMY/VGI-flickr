# -*- coding: utf-8 -*-
"""
Created on 2017/10/27 20:28

@author: ding_x
"""
# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import pydot
import shutil

test_path = "D:/VGI_Data/VLFeat/demo/test"
thumbnail_path = "D:/VGI_Data/VLFeat/demo/test/thumbnail"
building_img_path = 'D:/VGI_Data/total_building'
data_path = 'D:/VGI_Data/building_demo/Hot place'

def get_imlist(path):
    return [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]


def sift(img1, img2):
    img1 = cv2.imread(img1)
    img2 = cv2.imread(img2)
    # 生成灰度图像
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 调用sift算法检测并返回特征描述（坐标，半径，角度）及描述子（128维）
    sift = cv2.SIFT()
    kp1, des1 = sift.detectAndCompute(img1_gray, None)
    kp2, des2 = sift.detectAndCompute(img2_gray, None)

    # 生成特征匹配矩阵，寻找与每个img1特征点的k个最近似img2特征点,返回matchs列表
    # matches结构为：[[<img1_keypoint1,img2_keypoint_n1>,<img1_keypoint1,img2_keypoint_n2>],[<img1_keypoint2,img2_keypoint_n1>,<img1_keypoint1,img2_keypoint_n2>]...]
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # matchs过滤，去除误配点
    # 原理：对于图像im1中的某个SIFT特征点point1，通过在im2图像上所有SIFT关键点查找到与point1最近的SIFT关键点point21(记该关键点point21到point1的距离为dis1)和次近的关键点point22(记该关键点point22到point1的距离为dis2)，如果dis1/dis2<0.8，则我们将其视为正确匹配的点对，否则则为错配的点对予以剔除。
    match_num = 0
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * 0.75:
            match_num += 1
    return match_num


def get_matchscores(img_list):
    n = len(img_list)
    matchscores = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            img_name_1 = img_list[i].split('\\')[2]
            img_name_2 = img_list[j].split('\\')[2]
            print 'comparing ', img_name_1, img_name_2
            match_num = 0
            try:
                match_num = sift(img_list[i], img_list[j])
            except Exception as e:
                print e
            matchscores[i, j] = match_num
    matchscores += matchscores.T - np.diag(matchscores.diagonal())
    return matchscores

def cluster_img(img_list,matchscores,threshold):
    cluster_path = os.path.join(img_list[0].split('\\')[0], 'cluster')
    print cluster_path
    if not os.path.isdir(cluster_path):
        os.makedirs(cluster_path)
    for i in range(len(img_list)):
        for j in range(i + 1, len(img_list)):
            img_name_1 = img_list[i].split('\\')[2]
            img_name_2 = img_list[j].split('\\')[2]
            if matchscores[i, j] > threshold:
                cluster_img1 = os.path.join(cluster_path,img_name_1)
                if not os.path.exists(cluster_img1):
                    shutil.copyfile(img_list[i],cluster_img1)
                cluster_img2 = os.path.join(cluster_path, img_name_2)
                if not os.path.exists(cluster_img2):
                    shutil.copyfile(img_list[j], cluster_img2)



def draw_graph(img_list, matchscores, threshold):
    g = pydot.Dot(graph_type='graph')
    for i in range(len(img_list)):
        for j in range(i + 1, len(img_list)):
            if matchscores[i, j] > threshold:
                img_name_1 = img_list[i].split('\\')[2]
                img1 = cv2.imread(img_list[i])
                res1 = cv2.resize(img1, (100, 100), interpolation=cv2.INTER_CUBIC)
                img1_thumbnail = os.path.join(thumbnail_path, img_name_1)
                cv2.imwrite(img1_thumbnail, res1)
                g.add_node(pydot.Node(str(i), fontcolor='transparent',shape='rectangle', image=img1_thumbnail))

                img_name_2 = img_list[j].split('\\')[2]
                img2 = cv2.imread(img_list[j])
                res2 = cv2.resize(img2, (200, 200), interpolation=cv2.INTER_CUBIC)
                img2_thumbnail = os.path.join(thumbnail_path, img_name_2)
                cv2.imwrite(img2_thumbnail, res2)
                g.add_node(pydot.Node(str(j), fontcolor='transparent',shape='rectangle', image=img2_thumbnail))
                g.add_edge(pydot.Edge(str(i), str(j)))
    g.write_png(os.path.join(test_path, 'test.png'))

def search_similar_img(target_imgs,sample_imgs,sample_path):
    for target_img in target_imgs:
        for sample_img in sample_imgs:
            match_score = 0
            try:
                temp_score = (sift(target_img, sample_img),sift(sample_img, target_img))
                match_score = min(temp_score)
            except Exception as e:
                print e
            sample_img_name = sample_img.split('\\')[1]
            if match_score > 30:
                print '%s %s %d'% (target_img,sample_img,match_score)
                #buffer_path = os.path.join(sample_path.split('sample')[0], sample_img_name)
                buffer_path = os.path.join(sample_path, sample_img_name)
                if not os.path.exists(buffer_path):
                    shutil.copyfile(sample_img,os.path.join(sample_path,sample_img_name))


if __name__ == "__main__":
    # for path in [os.path.join(data_path, f,'target') for f in os.listdir(data_path)]:
    #     print path
    #     target_imgs = get_imlist(path)
    #     sample_path = os.path.join(data_path,path.split('\\')[1],'sample')
    #     sample_imgs = get_imlist(building_img_path)
    #     search_similar_img(target_imgs,sample_imgs,sample_path)

    path = r"D:\VGI_Data\building_demo\Hot place\Buckingham Palace\target"
    target_imgs = get_imlist(path)
    sample_path = r"D:\VGI_Data\building_demo\Hot place\Buckingham Palace\matched"
    #sample_imgs = get_imlist(building_img_path)
    sample_imgs = get_imlist( "D:/VGI_Data/building_demo/Hot place/Buckingham Palace")
    search_similar_img(target_imgs,sample_imgs,sample_path)

    # cluster_test = r"D:\VGI_Data\osm-flickr\5208404"
    # test_imgs = get_imlist(path)





