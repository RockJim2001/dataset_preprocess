#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project ：dataset_preprocess
@Product_name ：PyCharm
@File ：mini-coco.py
@Author ：RockJim
@Date ：2023/8/2 19:46
@Description ：对coco数据集进行重新划分，只取其中的五分之一
@Version ：1.0
"""

RESULT_ROOT_PATH = r"C:\Users\25760\Desktop\result"
# COCO 2017 数据集的root目录路径
COCO_JSON_ANNOTATIONS_DIR = (
    r"D:\Code\PythonProject\datasets/coco/annotations/"
)


def coco_json_split(json_dir, json_name, flag):
    import os
    full_json_path = os.path.join(json_dir, json_name)
    if not os.path.exists(full_json_path):
        print("路径：{}不存在！".format(full_json_path))
        return
    import json
    with open(full_json_path, 'r') as coco_data:
        data_all = json.load(coco_data)
        ann_data = data_all['annotations']
    statistics_list = [0 for i in range(0, 91)]
    print(statistics_list)
    print(len(ann_data))
    for i in ann_data:
        print(i)
        print(int(i['category_id']))
        try:
            statistics_list[i['category_id']] += 1
        except Exception as e:
            print("报错id:" + i['category_id'])
            # print(statistics_list[i['category_id']])
            print(e.with_traceback())
        except IndexError as error:
            print(error.with_traceback())
    print('根据统计结果进行写入')

    # file_write.write(json.dumps({'info': data_all['info']}))
    # file_write.write(json.dumps({'licenses': data_all['licenses']}))
    # file_write.write(json.dumps({'images': data_all['images']}))

    file_dict_list = list()
    statistics_now = [0 for i in range(0, 91)]
    # 按照前1/5进行选取
    for i in ann_data:
        id = i['category_id']
        if statistics_now[id] <= (int(statistics_list[id] * 0.2) + 1):
            file_dict_list.append(i)
            statistics_now[id] += 1
    # 不重复的随机采样
    # for i in ann_data:
    #     id = i['category_id']
    #     # 生成

    print(len(ann_data))
    result = {'info': data_all['info'], 'licenses': data_all['licenses'], 'images': data_all['images'],
              'annotations': file_dict_list, 'categories': data_all['categories']}
    with open(os.path.join(RESULT_ROOT_PATH, json_name), 'w') as f:
        json.dump(result, f)
    f.close()

    # 将结果写入到csv文件当中，然后使用excel进行分析
    file_csv = open(os.path.join(RESULT_ROOT_PATH, 'result_' + flag + '2017.csv'), 'w')
    labels = str(None)
    label = data_all['categories']
    name_list = ['-' for n in range(91)]
    for i in label:
        name_list[i['id']] = i['name']
    for i in name_list:
        labels += i
        labels += ","

    labels += "\t\n"
    for item in statistics_list:
        labels += str(item)
        labels += ","
    labels += "\t\n"
    for item in statistics_now:
        labels += str(item)
        labels += ','
    labels += '\t\n'
    file_csv.write(labels)
    file_csv.close()


if __name__ == '__main__':
    coco_json_split(COCO_JSON_ANNOTATIONS_DIR, "instances_train2017.json", 'train')
    coco_json_split(COCO_JSON_ANNOTATIONS_DIR, "instances_val2017.json", 'val')
