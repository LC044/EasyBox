#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2024/11/10 21:13 
@Author      : SiYuan 
@Email       : 863909694@qq.com 
@File        : EasyBox-encrypt_dialog.py 
@Description : 
"""
import fitz
import pymupdf
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox
from pymupdf import mupdf

from app.ui.pdf_tools.merge.encrypt_dialog_ui import Ui_Dialog


class EncryptControl(QDialog, Ui_Dialog):
    okSignal = pyqtSignal(bool)
    childRouterSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('填写加密选项')
        self.buttonBox.setObjectName('border')

    def accept(self):
        owner_pw1 = self.lineEdit_owner_pw1.text()
        owner_pw2 = self.lineEdit_owner_pw2.text()
        if not owner_pw1 or not owner_pw2:
            QMessageBox.warning(self, '警告', '请输入编辑密码')
            return
        if owner_pw1 != owner_pw2:
            QMessageBox.warning(self, '警告', '两次管理员密码输入不一致')
            return
        user_pw1 = self.lineEdit_user_pw1.text()
        user_pw2 = self.lineEdit_user_pw2.text()
        if user_pw1 != user_pw2:
            QMessageBox.warning(self, '警告', '两次用户密码输入不一致')
            return
        super().accept()

    def get_data(self):
        print('123')
        owner_pw1 = self.lineEdit_owner_pw1.text()
        owner_pw2 = self.lineEdit_owner_pw2.text()
        user_pw1 = self.lineEdit_user_pw1.text()
        user_pw2 = self.lineEdit_user_pw2.text()
        permissions = 0
        if self.checkBox_edit.isChecked():
            permissions |= mupdf.PDF_PERM_MODIFY
        if self.checkBox_copy.isChecked():
            permissions |= mupdf.PDF_PERM_COPY
        if self.checkBox_annotate.isChecked():
            permissions |= mupdf.PDF_PERM_ANNOTATE
        if self.radioButton_print.isChecked():
            permissions |= mupdf.PDF_PERM_PRINT | mupdf.PDF_PERM_PRINT_HQ
        elif self.radioButton_print_low.isChecked():
            permissions |= mupdf.PDF_PERM_PRINT
        else:
            if permissions == 0:
                permissions = 0
        return {
            "encryption": mupdf.PDF_ENCRYPT_AES_256,
            'owner_pw': owner_pw1,
            'user_pw': user_pw1,
            "permissions": permissions
        }


if __name__ == '__main__':
    pass
