#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2025/4/3 16:31 
@Author      : SiYuan 
@Email       : 863909694@qq.com 
@File        : EasyBox-theme.py
@Description : 
"""
from enum import Enum

from PySide6.QtCore import QFile, QIODevice, QTextStream, QIODeviceBase
from PySide6.QtCore import QUrl, QFile, QIODevice, QTextStream

from app import config


def set_theme(widget, theme: config.Theme):
    if config.UI_THEME_SETTING == config.Theme.system:
        theme = config.get_system_theme()
        config.UI_THEME = theme
    print('修改主题', theme)
    if theme == config.Theme.dark:
        style_qss_file = QFile(":/data/resources/QSS/style-dark.qss")
    else:
        style_qss_file = QFile(":/data/resources/QSS/style.qss")
    if style_qss_file.open(QIODeviceBase.OpenModeFlag.ReadOnly | QIODeviceBase.OpenModeFlag.Text):
        stream = QTextStream(style_qss_file)
        style_content = stream.readAll().strip()
        widget.setStyleSheet(style_content)
        style_qss_file.close()


if __name__ == '__main__':
    pass
