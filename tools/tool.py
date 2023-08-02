#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project ：dataset_preprocess
@Product_name ：PyCharm
@File ：tool.py
@Author ：RockJim
@Date ：2023/8/2 17:07
@Description ：处理数据集的公共工具
@Version ：1.0 
'''
from datetime import datetime


def get_datetime():
    """
        获取yyyy-MM-dd hh:mm:ss格式的当前时间字符串
    :return:
    """
    now = datetime.now()
    return now.strftime('%Y-%m-%d')