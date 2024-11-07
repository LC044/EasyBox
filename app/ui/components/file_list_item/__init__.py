#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2024/11/8 2:04 
@Author      : SiYuan 
@Email       : 863909694@qq.com 
@File        : EasyBox-__init__.py.py 
@Description : 
"""
import os

from PyQt5.QtWidgets import QWidget

from app.ui.components.file_list_item.file_item_ui import Ui_file_item_widget


class FileItemWidget(QWidget, Ui_file_item_widget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.checkBox_name.setText(os.path.basename(text))
        self.progressBar.setVisible(False)
        self.label_result.setVisible(False)
        self.btn_open.setVisible(False)


if __name__ == '__main__':
    pass
