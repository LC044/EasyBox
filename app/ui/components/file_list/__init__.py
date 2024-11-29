#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2024/11/8 2:04 
@Author      : SiYuan 
@Email       : 863909694@qq.com 
@File        : EasyBox-__init__.py.py 
@Description : PySide6实现的自定义文件列表，可自由拖拽排序，点击上下移动
"""
import os
import re
from typing import List

from PySide6.QtCore import Signal, QUrl, Qt, QSize, QMimeData, QModelIndex
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon, QStandardItemModel, QStandardItem, QDrag, QDropEvent
from PySide6.QtWidgets import QWidget, QAbstractItemView, QLabel, QPushButton, QHBoxLayout, \
    QStyledItemDelegate, QListView
from PySide6 import QtCore, QtGui, QtWidgets

from app.model import PdfFile
from app.ui.components import ScrollBar
from app.ui.components.file_list.file_item_ui import Ui_file_item_widget

Stylesheet = """
QWidget,QLabel{
    background: rgb(238,244,249);
}
"""
Stylesheet_hover = """
QWidget,QLabel{
    background: rgb(230, 235, 240);
}
"""
Stylesheet_clicked = """
QWidget,QLabel{
    background: rgb(230, 235, 240);
}
"""


class CustomWidget(QWidget):
    """自定义列表项，带有标签和删除按钮"""

    def __init__(self, text):
        super(CustomWidget, self).__init__()
        self.is_selected = False
        self.label = QLabel(os.path.basename(text))
        # self.label.setStyleSheet("padding: 5px;")
        self.btn_up = QPushButton("↑")
        self.btn_down = QPushButton("↓")
        self.btn_delete = QPushButton("删除")

        # 创建布局
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        layout.addItem(spacerItem)
        layout.addWidget(self.btn_up)
        layout.addWidget(self.btn_down)
        layout.addWidget(self.btn_delete)
        # layout.addStretch(1)  # 确保按钮在一行末尾
        layout.setContentsMargins(0, 0, 10, 0)
        self.setLayout(layout)
        # self.setFixedSize(QSize(200,80))
        self.setStyleSheet(Stylesheet)

    def leaveEvent(self, e):  # 鼠标离开label
        if self.is_selected:
            return
        self.setStyleSheet(Stylesheet)

    def enterEvent(self, e):  # 鼠标移入label
        self.setStyleSheet(Stylesheet_hover)


class CustomDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def sizeHint(self, option, index):
        """根据每个项的内容返回大小"""
        item = index.model().itemFromIndex(index)
        data = item.data(Qt.UserRole)

        # 通过数据（假设是文件名）动态计算高度
        height = 35  # 默认高度
        # if data.filename:
        #     height = max(50, len(data.filename) // 2)

        return QSize(200, height)  # 固定宽度为200，高度动态变化


def format_numbers(s):
    # 找到字符串中的所有数字
    def format_match(match):
        # 对每个数字部分进行格式化（7位数字）
        return match.group(0).zfill(7)

    # 使用正则表达式替换数字部分，保留其他部分不变
    return re.sub(r'\d+', format_match, s)


class FileItem(QStandardItem):
    """自定义的 QStandardItem 用于存储小部件的文本内容"""

    def __init__(self, fileinfo):
        super(FileItem, self).__init__()
        self.setData(fileinfo, Qt.UserRole)  # 存储自定义文本数据

    def get_filename(self):
        """读取存储的数据"""
        return self.data(Qt.UserRole).filename

    def __eq__(self, other):
        return self.data(Qt.UserRole) == other.data(Qt.UserRole)

    def __lt__(self, other):
        return self.data(Qt.UserRole) < other.data(Qt.UserRole)


class FileItemWidget(QWidget, Ui_file_item_widget):
    dataChanged = Signal(bool)
    dropIndex = Signal(QModelIndex)

    def __init__(self, fileinfo: PdfFile, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.filepath = fileinfo.file_path
        self.index: QModelIndex = None
        self.checkBox_name.setText(fileinfo.file_name)
        self.checkBox_name.setToolTip(fileinfo.file_path)
        self.checkBox_name.clicked.connect(self.dataChanged)
        self.progressBar.setVisible(False)
        self.label_result.setVisible(False)
        # self.setAcceptDrops(False)
        # self.btn_open.setVisible(False)
        self.spinBox_start.valueChanged.connect(self.update_page_range)
        self.spinBox_end.valueChanged.connect(self.update_page_range)
        # 设置文件大小
        file_size = fileinfo.file_size / (1024 * 1024)
        file_size = int(round(file_size, 0))
        if file_size < 1:
            self.label_size.setText(
                "<span style='background-color: rgb(162, 172, 188); color: rgb(255, 255, 255);text-shadow: 2px "
                "2px 4px rgba(0, 0, 0, 0.5);'>1M</span>")
        elif file_size < 100:
            self.label_size.setText(
                f"<span style='background-color: rgb(162, 172, 188); color: rgb(255, 255, 255);text-shadow: 2px "
                f"2px 4px rgba(0, 0, 0, 0.5);'>{file_size}M</span>")
        else:
            self.label_size.setText("<span style='background-color: rgb(162, 172, 188); color: rgb(255, 255, "
                                    "255);text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);'>&gt;99M</span>")
        # 设置页码范围
        self.label_page_num.setText(str(fileinfo.page_num))
        self.spinBox_start.setMaximum(fileinfo.page_num)
        self.spinBox_end.setMaximum(fileinfo.page_num)
        self.spinBox_end.setValue(fileinfo.page_num)
        self.checkBox_name.setChecked(True)
        self.btn_open.clicked.connect(self.open_folder)

    def open_folder(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.filepath))

    def update_page_range(self):
        sv = self.spinBox_start.value()
        ev = self.spinBox_end.value()
        if self.sender() == self.spinBox_start:
            if sv > ev:
                self.spinBox_end.setValue(sv)
        else:
            if sv > ev:
                self.spinBox_start.setValue(ev)
        self.dataChanged.emit(True)

    def select(self):
        self.checkBox_name.setChecked(True)
        self.dataChanged.emit(True)

    def dis_select(self):
        self.checkBox_name.setChecked(False)
        self.dataChanged.emit(True)

    def dragEnterEvent(self, event):
        print('dragEnterEvent')
        # self.setStyleSheet(
        #     '''
        #     border:2px solid rgb(230, 235, 240);
        #     '''
        # )
        # event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.setStyleSheet(
            '''
            border:none;
            '''
        )
        print('leave')

    def dropEvent(self, event):
        self.setStyleSheet(
            '''
            border:none;
            '''
        )
        print(self.filepath)
        self.dropIndex.emit(self.index)


class FileListView(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_drap_index: QModelIndex = None
        self.start_drop_index = None
        self.setVerticalScrollBar(ScrollBar())
        self.setAcceptDrops(True)
        # self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)  # 启用拖动排序
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.start_drag_pos = None
        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        delegate = CustomDelegate(self)
        self.setItemDelegate(delegate)
        # self.selectionModel().selectionChanged.connect(self.on_selection_changed)
        # 监听模型改变，更新小部件
        # self.model.rowsInserted.connect(self.update_list_view)
        # self.model.rowsRemoved.connect(self.update_list_view)
        # self.model.rowsMoved.connect(self.update_list_view)

    def mousePressEvent(self, event):
        # 记录鼠标点击的起始点（相对于小部件的坐标）
        self.start_drag_pos = event.position()
        super().mousePressEvent(event)

    def startDrag(self, supportedActions):
        # 获取当前选中的索引
        index = self.currentIndex()
        self.start_drap_index = index
        # super().startDrag(supportedActions)
        # return
        if index.isValid():
            # 使用模型获取项的小部件
            item_widget = self.indexWidget(index)
            if item_widget:
                # 将自定义小部件转换为 QPixmap
                pixmap = item_widget.grab()  # 获取小部件的截图作为拖拽图像

                # 创建 QDrag 对象
                drag = QDrag(item_widget)
                mime_data = QMimeData()
                mime_data.setText(item_widget.filepath)
                drag.setMimeData(mime_data)
                drag.setPixmap(pixmap)  # 设置拖拽图像为自定义小部件的截图
                # 计算拖拽热点，使拖拽图像的初始点贴合鼠标
                if self.start_drag_pos:
                    # 将点击点相对于小部件的位置转换为拖拽热点
                    hotspot = self.start_drag_pos - item_widget.pos()
                    drag.setHotSpot(hotspot.toPoint())
                # 执行拖拽操作
                result = drag.exec(supportedActions)

        # print('拖动结束', supportedActions)
        super().startDrag(supportedActions)
        # print('拖动结束', supportedActions)

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()

        event.acceptProposedAction()
        # event.accept()

    def dragLeaveEvent(self, e):
        print('leave')
        e.accept()

    def dropEvent(self, event):
        print('dropEvent10086')
        # 实现拖拽放置时的处理
        target_index = self.indexAt(event.position().toPoint())
        print(target_index)
        # 检查是否放置到有效位置
        if target_index.isValid():
            # 获取源项 (从当前列表中获取被拖拽的项)
            source_index = self.currentIndex()
            print(source_index, target_index)
            if source_index.isValid() and source_index != target_index:
                print(source_index, target_index)
                # 获取源项和目标项的行
                source_row = source_index.row()
                target_row = target_index.row()
                print(source_row, target_row)
                # 获取源项内容
                source_item = self.model.item(source_row)
                # 创建新项并复制源项的数据
                new_item = FileItem(source_item.data(Qt.UserRole).copy())
                new_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)  # 设置为可拖动
                # 从模型中移除源项
                self.model.removeRow(source_row)
                # 插入新项到目标位置
                self.model.insertRow(target_row, new_item)
                self.set_item_widget(new_item)
                # 接受事件，标记拖放完成
                # event.accept()
            else:
                # 若源项和目标项相同，则忽略事件
                event.ignore()
        else:
            event.ignore()

    def dropEvent_(self, target_index):
        print('dropEvent10086')
        # 检查是否放置到有效位置
        if target_index.isValid():
            # 获取源项 (从当前列表中获取被拖拽的项)
            source_index = self.currentIndex()
            print(source_index, target_index)
            if source_index.isValid() and source_index != target_index:
                print(source_index, target_index)
                # 获取源项和目标项的行
                source_row = source_index.row()
                target_row = target_index.row()
                print(source_row, target_row)
                # 获取源项内容
                source_item = self.model.item(source_row)
                # 创建新项并复制源项的数据
                new_item = FileItem(source_item.data(Qt.UserRole).copy())
                new_item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsDragEnabled)  # 设置为可拖动
                # 从模型中移除源项
                self.model.removeRow(source_row)
                # 插入新项到目标位置
                self.model.insertRow(target_row, new_item)
                self.set_item_widget(new_item)
                # 接受事件，标记拖放完成
                # event.accept()

    def add_item(self, text, index):
        """添加自定义组件到 QListView"""
        item = FileItem(PdfFile(text))
        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsDragEnabled)  # 设置为可拖动
        self.model.appendRow(item)
        self.set_item_widget(item)

    def set_item_widget(self, item):
        if not item:
            return
        """设置或更新QListView中的自定义小部件"""
        fileinfo = item.data(Qt.UserRole)
        if not fileinfo or not isinstance(fileinfo, PdfFile):
            return
        text = fileinfo.file_name
        # widget = CustomWidget(text)
        widget = FileItemWidget(fileinfo)
        # self.widgets.append(widget)
        index = self.model.indexFromItem(item)
        widget.index = index
        self.setIndexWidget(index, widget)
        # 连接删除按钮事件
        widget.btn_delete.clicked.connect(lambda: self.remove_item(item))
        widget.btn_up.clicked.connect(lambda: self.move_item_up(item))
        widget.btn_down.clicked.connect(lambda: self.move_item_down(item))
        widget.dataChanged.connect(lambda: self.update_item_data(item))
        # widget.dropIndex.connect(self.dropEvent_)

    def update_item_data(self, item):
        """
        更新item的数据
        :param item:
        :return:
        """
        old_file_info = item.data(Qt.UserRole)
        row = item.row()
        index = item.index()
        widget = self.indexWidget(index)
        start_page_num = widget.spinBox_start.value()
        end_page_num = widget.spinBox_end.value()
        fileinfo = PdfFile(old_file_info.file_path)
        fileinfo.start_page_num = start_page_num
        fileinfo.end_page_num = end_page_num
        fileinfo.selected = widget.checkBox_name.isChecked()
        print(start_page_num, end_page_num, fileinfo.selected)
        self.model.setData(index, fileinfo, Qt.UserRole)

    def remove_item(self, item):
        """从 QListView 中删除项"""
        self.model.removeRow(item.row())

    def remove_select(self):
        """
        删除选中的项
        :return:
        """
        items = [(self.model.item(i).data(Qt.UserRole), self.model.item(i)) for i in range(self.model.rowCount())]
        for fileinfo, item in items:
            if fileinfo.selected:
                self.remove_item(item)

    def move_item_up(self, item):
        """将项向上移动"""
        row = item.row()  # 获取项的当前行号
        if row > 0:  # 确保当前项不是第一行
            new_item = FileItem(item.data(Qt.UserRole).copy())
            new_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)  # 设置为可拖动
            self.model.removeRow(item.row())
            self.model.insertRow(row - 1, new_item)
            self.set_item_widget(new_item)
            self.setCurrentIndex(self.model.index(row - 1, 0))

    def move_item_down(self, item):
        """将项向下移动"""
        index = self.model.indexFromItem(item)  # 获取该项的索引
        row = item.row()  # 获取项的当前行号
        if row < self.model.rowCount() - 1:  # 确保当前项不是最后一行
            new_item = FileItem(item.data(Qt.UserRole).copy())
            new_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)  # 设置为可拖动
            self.model.removeRow(item.row())
            self.model.insertRow(row + 1, new_item)
            self.set_item_widget(new_item)
            self.setCurrentIndex(self.model.index(row + 1, 0))

    def update_list_view(self, a):
        """更新 QListView 中所有项目的小部件"""
        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            self.set_item_widget(item)

    def sort_by_name(self, reverse=False):
        """
        根据文件名排序
        :param reverse: 升序 or 降序
        :return:
        """
        items = [self.model.item(i).data(Qt.UserRole) for i in range(self.model.rowCount())]
        items.sort(reverse=reverse)
        self.model.clear()
        for index, fileinfo in enumerate(items):
            self.add_item(fileinfo.file_path, index)

    def print(self):
        items = [self.model.item(i).data(Qt.UserRole) for i in range(self.model.rowCount())]
        print(items)

    def select_all(self):
        for row in range(self.model.rowCount()):
            widget = self.indexWidget(self.model.index(row, 0))
            widget.select()

    def dis_select_all(self):
        for row in range(self.model.rowCount()):
            widget = self.indexWidget(self.model.index(row, 0))
            widget.dis_select()

    def get_data(self) -> List[PdfFile]:
        items_data = [self.model.item(i).data(Qt.UserRole) for i in range(self.model.rowCount())]
        return items_data

    def clear(self):
        """
        清空视图
        :return:
        """
        self.model.clear()


if __name__ == '__main__':
    from PySide6.QtWidgets import QWidget, QApplication
    import sys
    from PySide6.QtGui import QFont, QPixmap, QIcon
    from PySide6.QtCore import Qt

    app = QApplication(sys.argv)
    font = QFont('微软雅黑', 10)  # 使用 Times New Roman 字体，字体大小为 14
    app.setFont(font)
    view = FileListView()
    for i in range(5):
        view.add_item(f'Item {i + 1}', i)
    view.show()
    sys.exit(app.exec())
