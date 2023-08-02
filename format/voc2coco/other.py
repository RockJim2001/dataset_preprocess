#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project ：dataset_preprocess
@Product_name ：PyCharm
@File ：other.py
@Author ：RockJim
@Date ：2023/8/2 18:23
@Description ：voc转coco的一些函数
@Version ：1.0 
'''
import os

from format.config.dataset_path_config import VOC_2017_ANNOTATIONS_DIR
from format.voc2coco.transform import save_info, coco_data, images_processing, annotation_processing, copy_image, \
    dir_list


def analysis_every_file(filename: str):
    """
        根据文件名来读取每个类中所采用的图片名称
    :param filename: 文件名称
    :return: 一个图片名称的list
    """
    result_list = []
    with open(os.path.join(VOC_2017_ANNOTATIONS_DIR, 'ImageSets/Main/' + filename), 'r') as filedata:
        line = filedata.readline()
        while line:
            line = line.strip()  # 剔除行末的换行符
            temp, flag = str(line).split()
            if flag == '1':
                result_list.append(temp)
            line = filedata.readline()
    return result_list

def prepare_save_info(dict_list: dict, flag: int, image_id: int, annotation_id: int):
    """
        将所有的信息都统计到dict中方便进行存储成json文件
    :param dict_list: 存储train、val、trainval中所用图片的一个dict，key为类名
    :param flag: 一个标识符，表示那个文件夹，0-train2012、1-val2012、2-trainval2012
    :return:
    """
    result = coco_data.copy()
    for key, values in dict_list.items():
        for item in values:
            result['images'].append(images_processing(item))
            result['annotations'].append(annotation_processing(item))
            # global image_id
            image_id += 1
            # global annotation_id
            annotation_id += 1
            # 进行照片的复制
            copy_image(item, dir_list[flag])
    return result


def pascal2coco_category(voc_dataset_path: str, voc2coco_path: str):
    """
        按类别进行
        将Pascal VOC2012数据集转为COCO2017数据集的格式（主要处理目标检测数据集，其他的数据集不管）
        @ params:
            voc_dataset_path: 原始Pascal VOC 2012数据集存储路径（根目录）
            voc2coco_path:  转换之后VOC2COCO数据集的存储路径（根目录）
    """

    # 统计每一个类别所包含的图像----train集、val集、trainval集
    train_category_dict_image_list = {}
    val_category_dict_image_list = {}
    trainval_category_dict_image_list = {}
    for filename in os.listdir(os.path.join(voc_dataset_path, 'ImageSets/Main')):
        try:
            category, filetype = filename.split("_")
        except ValueError:
            print("出现了ValueError异常，filename文件为{}".format(filename))
        finally:
            print("程序执行出现异常，执行结束")

        if filetype == "train.txt":  # 训练集
            train_category_dict_image_list[category] = analysis_every_file(filename)
        elif filetype == "val.txt":  # 验证集
            val_category_dict_image_list[category] = analysis_every_file(filename)
        elif filetype == "trainval.txt":  # 训练验证集
            trainval_category_dict_image_list[category] = analysis_every_file(filename)
            # continue

    # 对train、val、trainval这三种情况的list进行格式转换，转换成coco中的images和annotations格式
    # 全局维护的图片和标注信息的编号
    image_id = 1
    annotation_id = 1
    #   1、 先处理train情况
    train_voc2coco = prepare_save_info(train_category_dict_image_list, 0, image_id, annotation_id)
    #   2、 处理val情况
    val_voc2coco = prepare_save_info(val_category_dict_image_list, 1, image_id, annotation_id)
    # global image_id, annotation_id
    image_id, annotation_id = 1
    #   3、 处理trainval情况
    trainval_voc2coco = prepare_save_info(trainval_category_dict_image_list, 2, image_id, annotation_id)

    # 文件保存
    save_info(train_voc2coco, 'voc2coco_train2012.json')
    save_info(val_voc2coco, 'voc2coco_val2012.json')
    save_info(trainval_voc2coco, 'voc2coco_trainval2012.json')
    print("hahahh")