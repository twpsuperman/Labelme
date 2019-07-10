# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 10:55:33 2019

@author: Administrator
"""
import argparse
import json
import os
import os.path as osp
import warnings
import copy

import numpy as np
import PIL.Image
from skimage import io
import yaml

from labelme import utils

NAME_LABEL_MAP = {
    '_background_': 0,
    "sheep": 1,
    "bus": 2,
    "car": 3,
    "cat": 4,
    "grass":5,
    "dog":6,
    "aircraft":7
    }
#
#LABEL_NAME_MAP = {
#    0: '_background_',
#    1: "airplane",
#    2: "ship",
#    3: "storage_tank",
#    4: "baseball_diamond",
#    5: "tennis_court",
#    6: "basketball_court",
#    7: "ground_track_field",
#    8: "harbor",
#    9: "bridge",
#    10: "vehicle",
#}
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('json_file')
    parser.add_argument('-o', '--out', default=None)
    args = parser.parse_args()

    json_file = args.json_file

    list = os.listdir(json_file)
    for i in range(0, len(list)):
        path = os.path.join(json_file, list[i])
        filename = list[i][:-5]       # .json
        if os.path.isfile(path):
            data = json.load(open(path))
            img = utils.image.img_b64_to_arr(data['imageData'])
            #lbl存储 mask，lbl_names 存储对应的label,字典
            lbl, lbl_names = utils.shape.labelme_shapes_to_label(img.shape, data['shapes'])  # labelme_shapes_to_label

            # modify labels according to NAME_LABEL_MAP
            lbl_tmp = copy.copy(lbl)
            for key_name in lbl_names:
                old_lbl_val = lbl_names[key_name]
                new_lbl_val = NAME_LABEL_MAP[key_name]
                lbl_tmp[lbl == old_lbl_val] = new_lbl_val
            lbl_names_tmp = {}
            for key_name in lbl_names:
                lbl_names_tmp[key_name] = NAME_LABEL_MAP[key_name]

            # Assign the new label to lbl and lbl_names dict
            lbl = np.array(lbl_tmp, dtype=np.int8)
            lbl_names = lbl_names_tmp

            #captions = ['%d: %s' % (l, name) for l, name in enumerate(NAME_LABEL_MAP)]
            captions = ['{}: {}'.format(lv, ln) for ln, lv in NAME_LABEL_MAP.items()]
            
            
            lbl_viz = utils.draw.draw_label(lbl, img, captions)
                
            out_dir = osp.basename(list[i]).replace('.', '_')
            out_dir = osp.join(osp.dirname(list[i]), out_dir)
            out_dir = args.out + "\\"+ out_dir
            if not osp.exists(out_dir):
                os.makedirs(out_dir)

            #存储原图
            PIL.Image.fromarray(img).save(osp.join(out_dir, '{}.png'.format(filename)))
            #存储标签图
            #PIL.Image.fromarray(lbl).save(osp.join(out_dir, '{}_gt.png'.format(filename)))
            utils.lblsave(osp.join(out_dir,'{}_gt.png'.format(filename)), lbl)
            #存储可视化图
            PIL.Image.fromarray(lbl_viz).save(osp.join(out_dir, '{}_viz.png'.format(filename)))

            with open(osp.join(out_dir, 'label_names.txt'), 'w') as f:
                for lbl_name in lbl_names:
                    f.write(lbl_name + '\n')

            warnings.warn('info.yaml is being replaced by label_names.txt')
            info = dict(label_names=lbl_names)
            with open(osp.join(out_dir, 'info.yaml'), 'w') as f:
                yaml.safe_dump(info, f, default_flow_style=False)

            print('Saved to: %s' % out_dir)

if __name__ == '__main__':
    main()