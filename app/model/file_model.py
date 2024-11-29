#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2024/11/20 14:31 
@Author      : SiYuan 
@Email       : 863909694@qq.com 
@File        : EasyBox-file_model.py 
@Description : 描述各种类型的文件
"""
import os
import re
import shutil
from enum import Enum

import pymupdf
from PIL import Image

from app.log import logger
from app.util import common


class FileType(Enum):
    UNKNOWN = 0
    PDF = 1
    DOCX = 2
    DOC = 3
    XLSX = 4
    CSV = 5
    TXT = 6
    HTML = 7


def format_numbers(s):
    # 找到字符串中的所有数字
    def format_match(match):
        # 对每个数字部分进行格式化（7位数字）
        return match.group(0).zfill(7)

    # 使用正则表达式替换数字部分，保留其他部分不变
    return re.sub(r'\d+', format_match, s)


class FileInfo:
    file_id = 0  # 文件id

    def __init__(self, file):
        FileInfo.file_id += 1
        self.file_id = FileInfo.file_id
        self.save_path = file
        self.file_name = os.path.basename(file)  # 文件名
        self.file_path = file  # 文件完整路径
        self.selected = True  # 该文件是否被选中
        self.file_type: FileType = self._file_type()
        if os.path.exists(file):
            # 设置文件大小
            self.file_size = os.path.getsize(file)
        else:
            self.file_size = 0

    def copy(self):
        return FileInfo(self.file_path)

    def _file_type(self):
        extension: str = self.file_name.split('.')[-1]
        extension = extension.lower()
        match extension:
            case 'pdf':
                return FileType.PDF
            case 'docx':
                return FileType.DOCX
            case 'txt':
                return FileType.TXT
            case _:
                return FileType.UNKNOWN

    def size(self, unit='MB', decimal_places=1):
        """
        Convert byte size to a specific unit.
        :param unit: str, Target unit ("B", "KB", "MB", "GB", "TB", etc.)
        :param decimal_places: int, Number of decimal places to round to
        :return: str, Converted size with unit
        """
        # Define conversion factors
        units = {"B": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3, "TB": 1024 ** 4}

        # Check if the unit is valid
        if unit not in units:
            raise ValueError(f"Invalid unit '{unit}'. Valid units are: {', '.join(units.keys())}")

        converted_size = self.file_size / units[unit]
        # Format the result
        return f"{converted_size:.{decimal_places}f}"

    def __str__(self):
        return f"FileInfo(file_name={self.file_name},{self.selected}"

    def __repr__(self):
        return f"FileInfo(file_name={self.file_name},{self.selected}"

    def __eq__(self, other):
        return format_numbers(self.file_name) == format_numbers(other.file_name)

    def __lt__(self, other):
        return format_numbers(self.file_name) < format_numbers(other.file_name)

    def __gt__(self, other):
        return format_numbers(self.file_name) > format_numbers(other.file_name)


class PdfFile(FileInfo):
    def __init__(self, file):
        super().__init__(file)
        self.start_page_num = 1
        self.end_page_num = 1
        self.page_num = -1
        self.encryption = None
        self.owner_pw = None
        self.user_pw = None
        self.permissions = set()
        self.encryption_options = {}
        """
        {
            "encryption": fitz.PDF_ENCRYPT_AES_256,  # 使用 AES-256 加密
            "owner_pw": owner_password,              # 管理员密码
            "user_pw": user_password,                # 用户密码
            "permissions": permissions               # 权限设置
        }
        """
        if os.path.exists(file):
            # 设置文件大小
            self.file_size = os.path.getsize(file)
            # 设置页码范围
            try:
                with pymupdf.open(file) as doc:
                    self.page_num = len(doc)
                    self.end_page_num = self.page_num
            except:
                pass

    def copy(self):
        return PdfFile(self.file_path)


class ImageFile(FileInfo):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.save_inplace = True
        self.save_fmt = 'auto'
        self.save_quality = 95

    def get_file_time_by_name(self):
        return common.extract_datetime_from_filename(self.file_name)

    def copy(self) -> bool:
        try:
            if not self.save_inplace:
                shutil.copy(self.file_path, self.save_path)
                return True
        except:
            logger.error(f'{self.save_path}保存失败')
            return False

    def save(self, img: Image.Image, exif=None):
        if not self.save_path:
            return False
        img.save(self.save_path, exif=exif, format='jpeg', quality=self.save_quality)


if __name__ == '__main__':
    pass
