#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project ：voc2coco
@Product_name ：PyCharm
@File ：Id_mapping_table.py
@Author ：RockJim
@Date ：2023/8/2 15:32
@Description ：全局编号管理
@Version ：1.0 
'''
import logging
import os.path

class Image_id_mapping_table:
    """
        根据${Pascal VOC2012}/ImageSets/Main/trainval.txt中的图片，
        为每一张图片进行生成一个在整个数据集中唯一的全局编号
        能够实现通过${filename}查询并获取对应图片的编号
        能够实现通过${serial_id}查询并获取对应图片的名称
        Tips：
            文件的名称不带文件格式
    """
    # 初始化
    def __init__(self, rootpath, filepath):
        self.image_info_dict = {}
        self.rootpath = rootpath
        self.filepath = filepath
        # 判断路径是否存在
        full_file_path = os.path.join(self.rootpath, self.filepath)
        assert os.path.exists(full_file_path), logging.error("文件路径{}不存在".format(full_file_path))
        # 通过路径来初始化映射表
        serial_id = 1  # 序列的初始编号
        with open(full_file_path, 'r') as file_temp:
            line = file_temp.readline().strip()
            while line:
                self.image_info_dict[line] = serial_id
                serial_id += 1
                line = file_temp.readline().strip()

    # 通过编号来查询图片名称
    def get_image_by_serial_id(self, serial_id: int):
        for item_name, item_id in self.image_info_dict.items():
            if item_id == serial_id:
                return item_name
        return None

    # 通过图片名称来查询编号
    def get_serial_id_by_image(self, image_name: str):
        temp_id = self.image_info_dict[image_name]
        if temp_id is not None:
            return temp_id
        else:
            return -1  # 表示没有找到相关的信息


class Annotation_mapping_table:
    def __init__(self):
        self.number = 1

    def get_id(self):
        temp = self.number
        self.number += 1
        return temp
