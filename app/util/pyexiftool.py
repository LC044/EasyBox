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
from typing import List

import exiftool
from datetime import datetime


def format_tag(tag_dict):
    return [f"-{tag}={value}".encode('utf-8') for tag, value in tag_dict.items()]
def get_file_type(filepath):
    fmt:str = os.path.basename(filepath).split('.')[-1]
    return fmt.lower()

fmt_time_tag = {
    "jpg":"EXIF:DateTimeOriginal",
    "jpeg":"EXIF:DateTimeOriginal",
    "mp4":"EXIF:CreateDate",
    "mov":"EXIF:CreateDate"
}

class PyExifTool:
    def __init__(self, executable, overwrite_original=True, error_callback=None):
        """

        :param executable: exiftool 可执行文件路径
        :param overwrite_original: 是否覆盖原图
        :param error_callback: 错误信息回调函数
        """
        self.et = exiftool.ExifToolHelper(executable=executable,encoding='utf-8')
        self.overwrite_original = overwrite_original
        self.error_callback = error_callback

    def set_executable(self, executor_path):
        self.et.terminate()
        self.et = exiftool.ExifToolHelper(executable=executor_path,encoding='utf-8')

    def close(self):
        self.et.terminate(_del=True)
    def print_error(self,error_msg):
        if self.error_callback:
            self.error_callback(error_msg)
        else:
            print(error_msg)
    def execute(self, args: dict, filepath):
        try:
            args = format_tag(args)
            if self.overwrite_original:
                args.append("-overwrite_original")
            args.append(filepath.encode('utf-8'))
            self.et.execute(*args)
        except:
            self.print_error(traceback.format_exc())
            self.print_error(self.et.last_stderr)

    def get_file_time(self,filepath) -> datetime|None:
        fmt = get_file_type(filepath)
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
            self.print_error(traceback.format_exc())
            self.print_error(self.et.last_stderr)
        return None

    def modify_file_time(self, new_datetime: datetime | str, filepath):
        if not new_datetime:
            return None
        try:
            if isinstance(new_datetime, datetime):
                dt_str = new_datetime.strftime("%Y:%m:%d %H:%M:%S")
            else:
                # todo 检查格式，格式必须为 %Y:%m:%d %H:%M:%S
                dt_str = new_datetime
        except:
            traceback.format_exc()
            return None
        if not os.path.exists(filepath):
            return None
        fmt = get_file_type(filepath)
        if fmt in {'jpg', 'jpeg', 'bmp', 'riff', 'webp'}:
            return self.modify_image_time(dt_str,filepath)
        elif fmt in {'mp4', 'mov', 'avi'}:
            return self.modify_video_time(dt_str,filepath)
        else:
            self.print_error(f'不支持的文件类型:{fmt} {filepath}')
            return None

    def modify_image_time(self, dt_str, filepath):
        metadata_dict = {
            "DateTimeOriginal": dt_str,
            "DateTimeDigitized": dt_str,
            "DateTime": dt_str
        }
        self.execute(metadata_dict, filepath)

    def modify_video_time(self, dt_str, filepath):
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