#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2024/11/26 0:56 
@Author      : SiYuan 
@Email       : siyuan044@qq.com 
@File        : EasyBox-doc_cov_model.py 
@Description : 描述文档转换的配置选项
"""
import re


def format_file_name(filename):
    return re.sub(r'[\\/:*?"<>|\s\.]', '_', filename)


class Pdf2DocxOpt:
    def __init__(self, output_path):
        self.o_dir = output_path


class Pdf2ImageOpt:
    def __init__(self, output_dir, format_='png', dpi=200):
        self.o_dir = output_dir
        self.o_fmt = format_
        self.o_name = '(转图片)'
        self.o_quality = 100
        self.o_dpi = dpi


class Web2PdfOpt:
    def __init__(self, url: str, output_dir='.'):
        self.url = url
        self.is_url = url.startswith('http')
        self.o_dir = output_dir
        self.o_name = ''
        self.set_name(url)

    def set_name(self, name: str):
        name = format_file_name(name)
        if name.endswith('.pdf'):
            self.o_name = name
        else:
            self.o_name = name + '.pdf'

        return self.o_name


if __name__ == '__main__':
    pass
