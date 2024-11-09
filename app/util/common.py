#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2024/11/9 16:36 
@Author      : SiYuan 
@Email       : 863909694@qq.com 
@File        : EasyBox-common.py 
@Description : 
"""
import os.path
import re


def correct_filename(filename):
    filename = re.sub(r'[\\/:*?"<>|\s\.]', '_', filename)
    return filename


def usable_filepath(filepath: str):
    if not os.path.exists(filepath):
        return filepath
    extension = filepath.split('.')[-1]
    filepath = '.'.join(filepath.split('.')[:-1])
    for i in range(1, 10086):
        new_path = filepath + f'({i}).{extension}'
        if not os.path.exists(new_path):
            return new_path
    return ''


if __name__ == '__main__':
    pass
