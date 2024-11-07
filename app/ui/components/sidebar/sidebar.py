#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2024/11/7 10:50 
@Author      : SiYuan 
@Email       : 863909694@qq.com 
@File        : EasyBox-sidebar.py 
@Description : 
"""
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QSizePolicy
from PyQt5.QtCore import QSize, QRect, QPropertyAnimation
from PyQt5.QtGui import QIcon

from app.ui.components.router import Router

try:
    from sidebar_ui import Ui_Form
except:
    from app.ui.components.sidebar.sidebar_ui import Ui_Form


class SidebarButton(QPushButton):
    def __init__(self, icon, text, parent=None):
        super(SidebarButton, self).__init__(icon, text, parent)
        self._text = text
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet(self.default_style())

    def sizeHint(self):
        return QSize(100, 60)  # 设置合适的宽高

    def default_style(self):
        return """
            QPushButton {
                border-radius: 0px;
                padding: 10px;
                border: none;
                text-align: left;
            }
            QPushButton:hover {
                background-color: rgb(230,235,240);
            }
        """

    def selected_style(self):
        return """
            QPushButton {
                border-radius: 0px;
                border-left: 3px solid rgb(133,135,138);
                text-align: left;
            }
        """

    def set_selected(self, selected):
        if selected:
            self.setStyleSheet(self.selected_style())
        else:
            self.setStyleSheet(self.default_style())


class Sidebar(QWidget, Ui_Form):
    def __init__(self, stack, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.expanded = True
        self.default_width = 150  # 展开时的宽度
        self.collapsed_width = 60  # 折叠时的宽度
        self.router = Router(stack)
        self.buttons = []
        self.btn_back.clicked.connect(self.router.turn_back)
        self.btn_back.setEnabled(False)
        self.btn_setting.setObjectName('border')
        self.listWidget.clear()
        self.btn_toggle.clicked.connect(self.toggle_sidebar)
        self.setMinimumWidth(self.default_width)

    def set_turn_back_enable(self, flag):
        """
        设置返回按钮的状态
        :param flag: True: 可用, False:不可用
        :return:
        """
        self.btn_back.setEnabled(flag)

    def add_widget(self, icon, text):
        item = QListWidgetItem()
        button = SidebarButton(icon, text)
        self.listWidget.addItem(item)
        item.setSizeHint(button.sizeHint())
        self.listWidget.setItemWidget(item, button)

    def add_button(self, button):
        item = QListWidgetItem()
        self.listWidget.addItem(item)
        item.setSizeHint(button.sizeHint())
        self.listWidget.setItemWidget(item, button)

    def add_nav_button(self, icon, text, router_path, action):
        item = QListWidgetItem()
        button = SidebarButton(icon, text)
        self.add_button(button)
        self.buttons.append((button, router_path))
        self.listWidget.setItemWidget(item, button)
        button.clicked.connect(action)

    def toggle_sidebar(self):
        if not self.expanded:
            self.setMinimumWidth(self.default_width)
            self.btn_toggle.setText("折叠")
            # 恢复文字
            for i in range(self.listWidget.count()):
                item_widget = self.listWidget.itemWidget(self.listWidget.item(i))
                item_widget.setText(item_widget._text)
        else:
            self.btn_toggle.setText("展开")
            self.setMinimumWidth(self.collapsed_width)
            # 隐藏文字
            for i in range(self.listWidget.count()):
                item_widget = self.listWidget.itemWidget(self.listWidget.item(i))
                item_widget.setText("")
        # 切换状态
        self.expanded = not self.expanded

    def update_sidebar_selection(self, path):
        """ 根据当前路由层级自动选择父级路径 """
        # 解析并选择父路径（仅主路径）
        parent_path = self.get_parent_path(path)

        # 更新按钮状态
        for button, button_path in self.buttons:
            button.set_selected(button_path == parent_path)

    def get_parent_path(self, path):
        """ 获取给定路径的最顶层父路径 """
        if '/' in path:
            return '/' + path.split('/')[1]
        return path


if __name__ == '__main__':
    # 测试应用
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout(window)
    sidebar = Sidebar(window)
    layout.addWidget(sidebar)
    window.setGeometry(100, 100, 300, 400)  # 初始窗口大小
    window.show()
    app.exec_()
