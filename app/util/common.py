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
from datetime import datetime


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


start_time = datetime(1970, 1, 1, 0, 0, 0)
end_time = datetime(2035, 1, 1, 0, 0, 0)


def is_within_range(dt, start, end):
    """
    检查给定时间是否在指定范围内
    :param dt: 要检查的时间 (datetime 对象)
    :param start: 范围起始时间 (datetime 对象)
    :param end: 范围结束时间 (datetime 对象)
    :return: 布尔值，True 表示在范围内，False 表示不在范围内
    """
    return start <= dt <= end

def valid_time(dt):
    if start_time <= dt <= end_time:
        return dt
    else:
        return None

def extract_datetime_from_filename(filename) -> datetime | None:
    # 定义正则表达式，匹配常见的时间格式
    patterns = [
        r"(\d{8})_(\d{6})",  # 格式：YYYYMMDD_HHMMSS
        r"(\d{13}|\d{10})",  # 格式：TIMESTAMP (13位毫秒级时间戳)
        r"(\d{8})_(\d{6}).*?"  # 格式：YYYYMMDD_HHMMSS[其他内容]
    ]
    result = None
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            if len(match.groups()) == 2:  # 包含日期和时间
                date_part, time_part = match.groups()
                try:
                    result = datetime.strptime(date_part + time_part, "%Y%m%d%H%M%S")
                    return valid_time(result)
                except ValueError:
                    continue
            elif len(match.groups()) == 1:  # 只包含时间戳
                timestamp = match.group(1)
                try:
                    if len(timestamp) == 13:
                        result = datetime.fromtimestamp(int(timestamp) / 1000)  # 转换为秒
                    else:
                        result = datetime.fromtimestamp(int(timestamp))  # 转换为秒
                    return valid_time(result)
                except (ValueError, OverflowError):
                    continue
    return None


if __name__ == '__main__':
    pass
