#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2024/11/26 0:56 
@Author      : SiYuan 
@Email       : 863909694@qq.com 
@File        : EasyBox-doc_cov_model.py 
@Description : 描述文档转换的配置选项
"""


class Pdf2DocxOpt:
    def __init__(self):
        pass


class Pdf2ImageOpt:
    def __init__(self, format_='png', dpi=200):
        self.o_fmt = format_
        self.o_name = '(转图片)'
        self.o_quality = 100
        self.o_dpi = dpi


if __name__ == '__main__':
    pass
