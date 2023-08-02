#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project ：dataset_preprocess
@Product_name ：PyCharm
@File ：transform.py
@Author ：RockJim
@Date ：2023/8/2 17:24
@Description ：在这个py文件中主要工作是：将Pascal VOC2012格式的数据集转换为COCO数据集格式
@Version ：1.0
"""

import json
import os
import shutil
import cv2
import xml.etree.ElementTree as ET
from format.config.dataset_path_config import VOC_2017_ANNOTATIONS_DIR, VOC2COCO_ROOT
from format.voc2coco.Id_mapping_table import Annotation_mapping_table, Image_id_mapping_table
from tools.tool import get_datetime

# 创建VOC2COCO 数据集文件夹
dir_list = ['annotations', 'train2012', 'val2012', 'trainval2012']

# 定义VOC标签和COCO类别映射关系
voc_labels = ["person",
              "bicycle",
              "car",
              "motorbike",
              "aeroplane",
              "bus",
              "train",
              "boat",
              "bird",
              "cat",
              "dog",
              "horse",
              "sheep",
              "cow",
              "bottle",
              "chair",
              "diningtable",
              "pottedplant",
              "sofa",
              "tvmonitor"
              ]
coco_data = {
    "info": {
        "description": "Pascal VOC to COCO conversion",
        "version": "1.0",
        "year": 2023,
        "contributor": "Rock Jim",
        "date_created": "2023-06-29"
    },
    "licenses": [
        {
            "id": 1,
            "name": "RockJim",
            "url": "https://www.whut.edu.cn"
        }
    ],
    "categories": [
        {
            "supercategory": "person",
            "id": 1,
            "name": "person"
        },

        {
            "supercategory": "vehicle",
            "id": 2,
            "name": "bicycle"
        },
        {
            "supercategory": "vehicle",
            "id": 3,
            "name": "car"
        },
        {
            "supercategory": "vehicle",
            "id": 4,
            "name": "motorbike"
        },
        {
            "supercategory": "vehicle",
            "id": 5,
            "name": "aeroplane"
        },
        {
            "supercategory": "vehicle",
            "id": 6,
            "name": "bus"
        },
        {
            "supercategory": "vehicle",
            "id": 7,
            "name": "train"
        },
        {
            "supercategory": "vehicle",
            "id": 8,
            "name": "boat"
        },

        {
            "supercategory": "animal",
            "id": 9,
            "name": "bird"
        },
        {
            "supercategory": "animal",
            "id": 10,
            "name": "cat"
        },
        {
            "supercategory": "animal",
            "id": 11,
            "name": "dog"
        },
        {
            "supercategory": "animal",
            "id": 12,
            "name": "horse"
        },
        {
            "supercategory": "animal",
            "id": 13,
            "name": "sheep"
        },
        {
            "supercategory": "animal",
            "id": 14,
            "name": "cow"
        },

        {
            "supercategory": "household",
            "id": 15,
            "name": "bottle"
        },
        {
            "supercategory": "household",
            "id": 16,
            "name": "chair"
        },
        {
            "supercategory": "household",
            "id": 17,
            "name": "dining table"
        },
        {
            "supercategory": "household",
            "id": 18,
            "name": "potted plant"
        },
        {
            "supercategory": "household",
            "id": 19,
            "name": "sofa"
        },
        {
            "supercategory": "household",
            "id": 20,
            "name": "tvmonitor"
        }
    ],
    "images": [],
    "annotations": []
}

# 图片名称-编号映射表
image_id_mapping = None

# annotation序号
annotation_id_mapping = None


def images_processing(filename: str, flag: int):
    """
        根据filename找到数据集中的图片，读取改图片的信息，保存成coco格式
    :param flag:    标识符
    :param filename:    图片名称
    :return:
    """
    image = cv2.imread(os.path.join(VOC_2017_ANNOTATIONS_DIR, 'JPEGImages/' + filename + '.jpg'))

    copy_image(filename, dir_list[flag])
    # 添加图像信息到COCO数据集
    height, width, _ = image.shape
    # 添加图片信息
    return {
        "id": image_id_mapping.get_serial_id_by_image(filename),
        "width": width,
        "height": height,
        "file_name": str(filename + '.jpg'),
        "license": "",
        "flickr_url": "",
        "coco_url": os.path.join("https://images.cocodataset.org/" + dir_list[1] + '/' + filename + ".jpg"),
        "date_captured": get_datetime(),
    }


def annotation_processing(filename: str):
    """
        利用filename来将Pascal VOC2012的${filename}.xml文件转为coco中的annotation格式
    :param filename:    图片名称
    :return:
    """
    # 从文件中读取标注信息
    annotation_name = os.path.join(VOC_2017_ANNOTATIONS_DIR, 'Annotations/' + filename + '.xml')
    assert os.path.exists(annotation_name), print("路径{}所指示的文件不存在".format(annotation_name))
    root = ET.parse(annotation_name)
    annotation_list = []
    # 遍历每个对象标注
    for object_elem in root.findall('object'):
        # 提取类别标签
        category = object_elem.find('name').text
        # 提取边界框信息
        bbox_elem = object_elem.find('bndbox')
        xmin = int(bbox_elem.find('xmin').text)
        ymin = int(bbox_elem.find('ymin').text)
        xmax = int(bbox_elem.find('xmax').text)
        ymax = int(bbox_elem.find('ymax').text)
        # 计算面积
        width = max(xmax, xmin) - min(xmax, xmin)
        height = max(ymax, ymin) - min(ymax, ymin)

        annotation_list.append({
            "iscrowd": 0,
            "image_id": image_id_mapping.get_serial_id_by_image(filename),
            "id": annotation_id_mapping.get_id(),
            "category_id": voc_labels.index(category),
            "area": float(width * height),
            "bbox": [
                min(xmax, xmin),
                min(ymax, ymin),
                width,
                height
            ]
        })
    return annotation_list


def copy_image(filename: str, folder: str):
    f"""
        将Pascal VOC2012文件夹JPEGImages/${filename}.jpg复制到voc2coco文件夹下${folder}/下
    :param filename: 图片名称
    :param folder:  文件夹名称
    :return: 
    """
    full_filename = os.path.join(VOC_2017_ANNOTATIONS_DIR, 'JPEGImages/' + filename + '.jpg')
    full_filename_new = os.path.join(VOC2COCO_ROOT, folder, filename + '.jpg')
    assert os.path.exists(full_filename), print("文件{}不存在".format(full_filename))
    shutil.copy(full_filename, full_filename_new)


def save_info(info: dict, flag: int):
    """
        将train、val、trainval的信息保存到对应的文件当中
    :param info:
    :param flag:
    :return:
    """
    full_file_path = os.path.join(VOC2COCO_ROOT, 'annotations', 'voc2coco_' + dir_list[flag] + '.json')
    #   将字典保存到json文件当中
    with open(full_file_path, 'w') as f:
        json.dump(info, f)
    print("文件{}保存成功".format('voc2coco_' + dir_list[flag] + '.json'))


def pascal2coco(VOC_2017_ANNOTATIONS_DIR_: str, filename: str):
    """
        按照train.txt、val.txt以及trainval.txt文件进行划分
    :param filename: 文件名称
    :param VOC_2017_ANNOTATIONS_DIR_:   voc数据集划分文件路径
    :return:
    """
    # 判断所传入文件夹的路径是否正确
    import os
    assert os.path.isdir(VOC_2017_ANNOTATIONS_DIR), print(
        "所传入的Pascal VOC 2012数据集的根目录{}不存在".format(VOC_2017_ANNOTATIONS_DIR))
    if not os.path.isdir(VOC2COCO_ROOT):
        print("所传入的VOC2COCO数据集的根目录{}不存在,已经自动创建！".format(VOC2COCO_ROOT))
        os.mkdir(VOC2COCO_ROOT)

    # 在VOC2COCO数据集根目录下面创建coco数据集所需要的文件夹
    for item in dir_list:
        temp = os.path.join(VOC2COCO_ROOT, item)
        if not os.path.exists(temp):
            os.mkdir(temp)

    if filename.startswith('train.'):
        flag = 1
    elif filename.startswith('val.'):
        flag = 2
    elif filename.startswith('trainval.'):
        flag = 3
    full_filename = os.path.join(VOC_2017_ANNOTATIONS_DIR_, 'ImageSets/Main', filename)
    result = coco_data.copy()
    with open(full_filename, 'r') as file_temp:
        line = file_temp.readline().strip()
        while line:
            result['images'].append(images_processing(line, flag))
            result['annotations'].extend(annotation_processing(line))
            line = file_temp.readline().strip()

    # 将文件进行保存
    save_info(result, flag)


if __name__ == '__main__':
    # 从trainval.txt文件中读取所有的数据，进行编号
    temp_path = os.path.join(VOC_2017_ANNOTATIONS_DIR, 'ImageSets/Main')
    image_id_mapping = Image_id_mapping_table(temp_path, 'trainval.txt')
    annotation_id_mapping = Annotation_mapping_table()
    # 按照train.txt、val.txt、trainval.txt进行划分
    for item in ['train.txt', 'val.txt']:
        pascal2coco(VOC_2017_ANNOTATIONS_DIR, item)
    annotation_id_mapping = Annotation_mapping_table()
    pascal2coco(VOC_2017_ANNOTATIONS_DIR, 'trainval.txt')
