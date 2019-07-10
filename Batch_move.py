# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:10:41 2019

@author: Administrator
"""
import os
import shutil

GT_from_PATH = "output"#从哪里来
GT_to_PATH = "gts"#向哪里去

def copy_file(from_dir, to_dir, Name_list):
    if not os.path.isdir(to_dir):
        os.mkdir(to_dir)

    for name in Name_list:
        try:
            if not os.path.isfile(os.path.join(from_dir, name)):
                print("{} is not existed".format(os.path.join(from_dir, name)))
            shutil.copy(os.path.join(from_dir, name), os.path.join(to_dir, name))
        except:
            print("failed to move {}".format(from_dir + name))
    print("{} has copied to {}".format(from_dir, to_dir))


if __name__ == '__main__':
    filepath_list = os.listdir(GT_from_PATH)
    for i, file_path in enumerate(filepath_list):#i为序列号，file_path为json文件名
        gt_path = os.path.join(GT_from_PATH, filepath_list[i])
        gt_name = ["{}_gt.png".format(file_path[:-5])]#标签图片的名字
        gt_file_path = os.path.join(GT_from_PATH, file_path)#真实标签图片的路径
        copy_file(gt_file_path, GT_to_PATH, gt_name)