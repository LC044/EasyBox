#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2025/8/12 23:23 
@Author      : SiYuan 
@Email       : siyuan044@gmail.com
@File        : EasyBox-exiftool.py 
@Description : 
"""
import os.path
import traceback
from importlib.metadata import metadata
from typing import List

import exiftool
from datetime import datetime


def format_tag(tag_dict):
    return [f"-{tag}={value}".encode('utf-8') for tag, value in tag_dict.items()]

fmt_time_tag = {
    "jpg":"EXIF:DateTimeOriginal",
    "jpeg":"EXIF:DateTimeOriginal",
    "mp4":"EXIF:CreateDate",
    "mov":"EXIF:CreateDate"
}

class PyExifTool:
    def __init__(self, executable, overwrite_original=True):
        self.et = exiftool.ExifToolHelper(executable=executable,encoding='utf-8')
        self.overwrite_original = overwrite_original

    def set_executable(self, executor_path):
        self.et.terminate()
        self.et = exiftool.ExifToolHelper(executable=executor_path,encoding='utf-8')

    def close(self):
        self.et.terminate(_del=True)

    def execute(self, args: dict, filepath):
        try:
            args = format_tag(args)
            if self.overwrite_original:
                args.append("-overwrite_original")
            args.append(filepath.encode('utf-8'))
            self.et.execute(*args)
        except:
            print(traceback.format_exc())
            print(self.et.last_stderr)

    def get_file_time(self,filepath) -> datetime|None:
        fmt = os.path.basename(filepath).split('.')[-1]
        if not fmt or fmt not in fmt_time_tag:
            return None
        try:
            metadata_list = self.et.get_metadata(filepath)
            if metadata_list:
                metadata_ = metadata_list[0]
                original_date_str = metadata_.get(fmt_time_tag[fmt])
                if original_date_str:
                    return datetime.strptime(original_date_str, "%Y:%m:%d %H:%M:%S")
        except:
            print(traceback.format_exc())
            print(self.et.last_stderr)
        return None

    def modify_image_time(self, new_datetime: datetime | str, filepath):
        if not new_datetime:
            return
        try:
            if isinstance(new_datetime, datetime):
                dt_str = new_datetime.strftime("%Y:%m:%d %H:%M:%S")
            else:
                # todo 检查格式，格式必须为 %Y:%m:%d %H:%M:%S
                dt_str = new_datetime
        except:
            traceback.format_exc()
            return
        metadata_dict = {
            "DateTimeOriginal": dt_str,
            "DateTimeDigitized": dt_str,
            "DateTime": dt_str
        }
        self.execute(metadata_dict, filepath)

    def modify_video_time(self, new_datetime: datetime | str, filepath):
        if isinstance(new_datetime, datetime):
            dt_str = new_datetime.strftime("%Y:%m:%d %H:%M:%S")
        else:
            # todo 检查格式，格式必须为 %Y:%m:%d %H:%M:%S
            dt_str = new_datetime
        metadata_dict = {
            "CreateDate": dt_str,
            "ModifyDate": dt_str,
            "MediaCreateDate": dt_str,
            "TrackCreateDate": dt_str,
            "TrackModifyDate": dt_str
        }
        self.execute(metadata_dict, filepath)

if __name__ == '__main__':
    et = PyExifTool(r"E:\Project\Python\EasyBox\resources\third_party\exiftool-13.33_64\exiftool(-k).exe",overwrite_original=True)
    image_dir = r"E:\Project\Python\EasyBox\test_data\output\图片"
    for file in os.listdir(image_dir):
        if not file.endswith('jpg'):
            continue
        filepath = os.path.join(image_dir,file)
        et.modify_image_time(datetime(2026, 5, 10, 14, 30, 0),filepath)
    et.close()