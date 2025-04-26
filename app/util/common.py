#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2024/11/9 16:36 
@Author      : SiYuan 
@Email       : siyuan044@qq.com 
@File        : EasyBox-common.py 
@Description : 
"""
import os.path
import platform
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


def usable_dir(dir: str):
    if not os.path.exists(dir):
        return dir
    for i in range(1, 10086):
        new_dir = dir + f'({i})'
        if not os.path.exists(new_dir):
            return new_dir
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
        r"(\d{4})[ _\.-](\d{2})[ _\.-](\d{2})[ _\.-](\d{2})[ _\.-](\d{2})[ _\.-](\d{2})",  # 格式：YYYY_MM_DD_HH-MM-SS
        r"(\d{4})[ _\.-](\d{2})[ _\.-](\d{2})[ _\.-](\d{6})",  # 格式：YYYY-MM-DD_HHMMSS YYYY-MM-DD HHMMSS
        r"(\d{2})[ _\.-](\d{2})[ _\.-](\d{4})[ _\.-](\d{6})",  # 格式：DD-MM-YYYY_HHMMSS
        r"(\d{8})[ _\.-](\d{2})[ _\.-](\d{2})[ _\.-](\d{2})",  # 格式：YYYYMMDD_HH-MM-SS
        r"(\d{8})[ _\.-](\d{6})"  # 格式：YYYYMMDD_HHMMSS
        r"(\d{8})T(\d{6})",  # 格式：YYYYMMDDTHHMMSS
        r"(\d{14})",         # 格式：YYYYMMDDHHMMSS
        r"(\d{13}|\d{10})",  # 格式：TIMESTAMP (13位毫秒级时间戳)
    ]
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            # 根据匹配的模式提取日期和时间
            if len(match.groups()) == 2:  # 格式：YYYYMMDD_HHMMSS
                date_str = match.group(1)
                time_str = match.group(2)
                dt = datetime.strptime(f"{date_str} {time_str}", "%Y%m%d %H%M%S")
                return dt
            elif len(match.groups()) == 1:  # 格式：TIMESTAMP
                timestamp = match.group(1)
                try:
                    if len(timestamp) == 14:
                        datetime_str = match.group(1)
                        dt = datetime.strptime(datetime_str, "%Y%m%d%H%M%S")
                        return dt
                    elif len(timestamp) == 13:
                        result = datetime.fromtimestamp(int(timestamp) / 1000)  # 转换为秒
                        return valid_time(result)
                    else:
                        result = datetime.fromtimestamp(int(timestamp))  # 转换为秒
                        return valid_time(result)
                except (ValueError, OverflowError):
                    continue
            elif len(match.groups()) == 4:  # 格式：YYYY-MM-DD HHMMSS
                year, month, day, time_str = match.groups()
                if len(year) == 4:
                    # 格式：YYYY-MM-DD_HHMMSS YYYY-MM-DD HHMMSS
                    dt = datetime.strptime(f"{year}-{month}-{day} {time_str}", "%Y-%m-%d %H%M%S")
                elif len(year) == 8:
                    # 格式：YYYYMMDD_HH-MM-SS
                    dt = datetime.strptime(f"{year} {month}-{day}-{time_str}", "%Y%m%d %H-%-M-%S")
                else:
                    # DD-MM-YYYY_HHMMSS
                    dt = datetime.strptime(f"{year}-{month}-{day} {time_str}", "%m-%d-%Y %H%M%S")
                return dt
            elif len(match.groups()) == 6:  # 格式：YYYY_MM_DD_HH-MM-SS
                year, month, day, hour, minute, second = match.groups()
                dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
                return dt

    return None  # 如果没有匹配到任何模式，返回 None


import os
from pathlib import Path


def get_system_download_dir():
    system = platform.system()

    if system == 'Windows':
        # Windows: 使用注册表获取下载目录
        import winreg
        try:
            # 打开注册表键 HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
            path, _ = winreg.QueryValueEx(reg_key, '{374DE290-123F-4565-9164-39C4925E467B}')
            return os.path.expandvars(path)
        except FileNotFoundError:
            try:
                # 打开注册表键 HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                         r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
                path, _ = winreg.QueryValueEx(reg_key, '{7D83EE9B-2244-4E70-B1F5-5393042AF1E4}')
                return os.path.expandvars(path)
            except FileNotFoundError:
                # 如果未找到，返回默认的 Downloads 路径
                return os.path.expanduser('~\\Downloads')

    elif system == 'Darwin':  # macOS
        # macOS 默认下载目录是 ~/Downloads
        return os.path.expanduser('~/Downloads')

    elif system == 'Linux':
        # Linux 通常默认下载目录是 ~/Downloads
        return os.path.expanduser('~/Downloads')

    else:
        return '.'  # 如果是未知的操作系统，返回 None


def get_system_document_dir():
    system = platform.system()

    if system == 'Windows':
        # Windows 使用注册表获取
        import winreg
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
            path, _ = winreg.QueryValueEx(reg_key, 'Personal')
            return os.path.expandvars(path)
        except FileNotFoundError:
            return os.path.expanduser('~')

    elif system == 'Darwin':  # macOS
        return os.path.expanduser('~/Documents')

    elif system == 'Linux':
        # Linux 通常使用 ~/Documents
        return os.path.expanduser('~/Documents')

    return '.'  # 未知系统


def get_system_desktop_dir():
    system = platform.system()

    if system == 'Windows':
        # Windows 使用注册表获取
        import winreg
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                     r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
            path, _ = winreg.QueryValueEx(reg_key, 'Desktop')
            return os.path.expandvars(path)
        except FileNotFoundError:
            return os.path.expanduser('~')

    elif system == 'Darwin':  # macOS
        return os.path.expanduser('~/Documents')

    elif system == 'Linux':
        # Linux 通常使用 ~/Documents
        return os.path.expanduser('~/Documents')

    return '.'  # 未知系统


if __name__ == '__main__':
    print(get_system_document_dir())
    print(get_system_download_dir())
    print(get_system_desktop_dir())

