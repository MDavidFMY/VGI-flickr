
# -*- coding: utf-8 -*-
"""
Created on 17-9-25下午5:41
@author: ding_x
"""
import sys
sys.path.append('/home/ding_x/caffe/caffe-master/python')
import caffe
import os
import shutil
import numpy as np
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

caffe_root = '/home/ding_x/caffe/caffe-master/'
model_root = '/home/ding_x/caffe/caffe-master/model/'


data_root = '/media/ding_x/软件/VGI_Data/Flickr_pic/london/2016/1/'
test_root = '/home/ding_x/caffe/1/'


def caffe_cf(used_labels,few_building):
    caffe.set_mode_gpu()
    model_def = model_root + 'deploy_vgg16_places365.prototxt'
    model_weights = model_root + 'vgg16_places365.caffemodel'
    net = caffe.Net(model_def,      # defines the structure of the model
                    model_weights,  # contains the trained weights
                    caffe.TEST)     # use test mode (e.g., don't perform dropout)

    #net.forward()  # run once before timing to set up memory
    net.forward()

    # load the mean ImageNet image (as distributed with Caffe) for subtraction
    mu = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
    mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
    print 'mean-subtracted values:', zip('BGR', mu)

    # create transformer for the input called 'data'
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

    transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
    transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
    transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
    transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

    # set the size of the input (we can skip this if we're happy
    #  with the default; we can also change it later, e.g., for different batch sizes)
    net.blobs['data'].reshape(1,        # batch size
                              3,         # 3-channel (BGR) images
                              224, 224)  # image size is 227x227


    result_list = []
    pic_list = os.listdir(test_root)
    pic_file_list = []
    for pic in pic_list:
        if '.jpg' in pic:
            pic_file_list.append(pic)
    for pic in pic_file_list:
        pic_path = os.path.join(test_root, pic)
        try:
            image = caffe.io.load_image(pic_path)
            transformed_image = transformer.preprocess('data', image)
        except Exception as e:
            print e
        # copy the image data into the memory allocated for the net
        net.blobs['data'].data[...] = transformed_image

        ### perform classification
        output = net.forward()

        output_prob = output['prob'][0]  # the output probability vector for the first image in the batch

        print '------------------'
        print 'predicted class is:', output_prob.argmax()

        # load ImageNet labels
        labels_file = model_root + 'categories_place365.txt'
        labels = np.loadtxt(labels_file, str, delimiter='\t')
        label_name = labels[output_prob.argmax()].split(' ')[0]
        print label_name

        # stor photos by their category name
        label_name_list = label_name.split('/')
        if len(label_name_list)>3:
            label_name = label_name_list[2] + "-" + label_name_list[3]
            movefile(label_name, used_labels, few_building, pic_path)
            # print 'output label:', label_name
            # result_list.append(label_name)
        else:
            label_name = label_name_list[2]
            newpath = os.path.join(test_root, label_name)
            movefile(label_name, used_labels, few_building, pic_path)
            # print 'output label:', label_name
            # result_list.append(label_name)
    #return result_list
def movefile(label_name,used_labels,few_building,oldpath):
    if label_name in used_labels:
        newpath = os.path.join(test_root,'used_labels',label_name)
        if os.path.isdir(newpath):
            shutil.move(oldpath, newpath)
        else:
            os.makedirs(newpath)
            shutil.move(oldpath, newpath)
    elif label_name in few_building:
        newpath = os.path.join(test_root,'few_building',label_name)
        if os.path.isdir(newpath):
            shutil.move(oldpath, newpath)
        else:
            os.makedirs(newpath)
            shutil.move(oldpath, newpath)

def sort_result(result_list):
    result_dic = {}
    for k in result_list:
        k = k.replace("\n", "")
        if result_dic.has_key(k):
            result_dic[k] = result_dic[k] + 1
        else:
            result_dic[k] = 1
    result_dic = sorted(result_dic.items(), key=lambda item: item[1], reverse=True)
    return result_dic
#
# File_list =[]
# def get_file_list(data_path):
#     '''
#     迭代获取指定路径下所有文件
#     :param data_path:
#     :return:
#     '''
#     if os.path.isfile(data_path):
#         File_list.append(data_path)
#         #print data_path
#     elif os.path.isdir(data_path):
#         file_list = os.listdir(data_path)
#         for f in file_list:
#             new_dir = os.path.join(data_path,f)
#             get_file_list(new_dir)

if __name__ == "__main__":
    few_building = open('/home/ding_x/caffe/few_building.txt')
    few_building = few_building.readlines()
    used_labels = open('/home/ding_x/caffe/used_labels.txt')
    used_labels = used_labels.readlines()
    new_few = []
    new_used = []
    for i in few_building:
        i=i.strip('\n')
        new_few.append(i)
    for i in used_labels:
        i = i.strip('\n')
        new_used.append(i)
    caffe_cf(new_used,new_few)

    # get_file_list('/home/ding_x/caffe/testdata/')
    # for oldpath in File_list:
    #     movefile(oldpath,'/home/ding_x/caffe/testdata/')