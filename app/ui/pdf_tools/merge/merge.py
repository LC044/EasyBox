import json
import os.path
import re
import sys
import traceback

import fitz
from PyQt5.QtCore import pyqtSignal, QThread, QFile, QIODevice, QTextStream, QUrl, Qt, QSize
from PyQt5.QtGui import QDesktopServices, QPixmap, QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QAbstractItemView, QLabel, QPushButton, QHBoxLayout, \
    QStyledItemDelegate
from PyQt5 import QtCore, QtGui, QtWidgets

from app.ui.components import ScrollBar
from app.ui.components.QCursorGif import QCursorGif
from app.ui.Icon import Icon
from .merge_ui import Ui_merge_pdf_view
from ...components.file_list_item import FileItemWidget
from ...components.router import Router


def open_file_explorer(path):
    # 使用QDesktopServices打开文件管理器
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))


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
        self.btn_down= QPushButton("↓")
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
        height = 50  # 默认高度
        # if data.filename:
        #     height = max(50, len(data.filename) // 2)

        return QSize(200, height)  # 固定宽度为200，高度动态变化


class FileInfo:
    def __init__(self, file, index):
        self.filename = file
        self.index = index

    def __str__(self):
        return f"FileInfo(filename={self.filename}, index={self.index})"

    def __repr__(self):
        return f"FileInfo(filename={self.filename}, index={self.index})"

    def __eq__(self, other):
        return self.filename == other.filename

    def __lt__(self, other):
        return self.filename < other.filename


class FileItem(QStandardItem):
    """自定义的 QStandardItem 用于存储小部件的文本内容"""

    def __init__(self, filename, index):
        super(FileItem, self).__init__()
        self.setData(FileInfo(filename, index), Qt.UserRole)  # 存储自定义文本数据

    def get_filename(self):
        """读取存储的数据"""
        return self.data(Qt.UserRole).filename

    def get_index(self):
        return self.data(Qt.UserRole).index


class MergeControl(QWidget, Ui_merge_pdf_view, QCursorGif):
    okSignal = pyqtSignal(bool)
    childRouterSignal = pyqtSignal(str)

    def __init__(self, router: Router, parent=None):
        super().__init__(parent)
        self.router = router
        self.router_path = self.parent().router_path + '/合并PDF'
        self.child_routes = {}
        self.worker = None
        self.running_flag = False
        self.setupUi(self)
        # 设置忙碌光标图片数组
        self.initCursor([':/icons/icons/Cursors/%d.png' %
                         i for i in range(8)], self)
        self.setCursorTimeout(100)
        self.init_ui()
        self.btn_choose_files.clicked.connect(self.open_file_dialog)
        self.btn_merge.clicked.connect(self.merge)
        self.list_view.setVerticalScrollBar(ScrollBar())
        self.list_view.setDragDropMode(QAbstractItemView.InternalMove)  # 启用拖动排序
        self.list_view.setDefaultDropAction(Qt.MoveAction)

        self.model = QStandardItemModel(self.list_view)
        self.list_view.setModel(self.model)
        delegate = CustomDelegate(self.list_view)
        self.list_view.setItemDelegate(delegate)
        self.list_view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        # 监听模型改变，更新小部件
        self.model.rowsInserted.connect(self.update_list_view)
        self.model.rowsRemoved.connect(self.update_list_view)
        self.model.rowsMoved.connect(self.update_list_view)

        self.input_files = []
        self.output_path = ''

    def init_ui(self):
        pixmap = QPixmap(Icon.logo_ico_path)
        icon = QIcon(pixmap)

    def on_selection_changed(self, selected):
        for index in selected.indexes():
            print("Selected item:", index.data(Qt.UserRole))
            widget = self.list_view.indexWidget(index)
            # widget.is_select = True

    def open_file_dialog(self):
        # 打开文件对话框，设置多文件选择和 PDF 文件过滤
        files, _ = QFileDialog.getOpenFileNames(self, "选择 PDF 文件", "", "PDF Files (*.pdf);;All Files (*)")
        if files:
            print(files)
            self.input_files = files
            for index, file in enumerate(files):
                self.add_item(file, index)

    def merge(self):
        items = [self.model.item(i).data(Qt.UserRole).filename for i in range(self.model.rowCount())]
        self.input_files = items
        print(items)
        if len(self.input_files) < 2:
            QMessageBox.information(self, '温馨提示', "请至少选择两个文件")
            return
        root_path = os.path.dirname(self.input_files[0])
        output = QFileDialog.getSaveFileName(None, "save file", os.path.join(root_path, '合并.PDF'),
                                             "csv files (*.csv);;all files(*.*)")
        if not output[0]:
            return
        self.output_path = output[0]
        self.startBusy()
        self.worker = MergeThread(self.input_files, self.output_path)
        self.worker.okSignal.connect(self.merge_finish)
        self.worker.progressSignal.connect(self.update_progress)
        self.worker.start()

    def update_progress(self, value):
        self.progressBar.setValue(value)

    def merge_finish(self, success):
        self.worker = None
        self.stopBusy()
        reply = QMessageBox(self)
        reply.setIcon(QMessageBox.Information)
        reply.setWindowTitle('OK')
        reply.setText(f"PDF合并成功")
        btn = reply.addButton('打开', QMessageBox.ActionRole)
        btn.clicked.connect(
            lambda x: open_file_explorer(
                os.path.dirname(self.output_path)
            )
        )
        # reply.addButton(btn)
        reply.addButton("确认", QMessageBox.AcceptRole)
        reply.addButton("取消", QMessageBox.RejectRole)
        api = reply.exec_()
        self.close()

    def add_item(self, text, index):
        """添加自定义组件到 QListView"""
        item = FileItem(text, index)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)  # 设置为可拖动
        self.model.appendRow(item)
        self.set_item_widget(item)

    def set_item_widget(self, item):
        if not item:
            return
        """设置或更新QListView中的自定义小部件"""
        fileinfo = item.data(Qt.UserRole)
        if not fileinfo:
            return
        text = fileinfo.filename
        # widget = CustomWidget(text)
        widget = FileItemWidget(text)
        # self.widgets.append(widget)
        index = self.model.indexFromItem(item)
        self.list_view.setIndexWidget(index, widget)
        self.model.setData(
            index,
            FileInfo(item.data(Qt.UserRole).filename, index.row()),
            Qt.UserRole
        )
        # 连接删除按钮事件
        widget.btn_delete.clicked.connect(lambda: self.remove_item(item))
        widget.btn_up.clicked.connect(lambda: self.move_item_up(item))
        widget.btn_down.clicked.connect(lambda: self.move_item_down(item))

    def remove_item(self, item):
        """从 QListView 中删除项"""
        self.model.removeRow(item.row())

    def move_item_up(self, item):
        """将项向上移动"""
        row = item.row()  # 获取项的当前行号
        if row > 0:  # 确保当前项不是第一行
            new_item = FileItem(item.data(Qt.UserRole).filename, item.data(Qt.UserRole).index)
            new_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)  # 设置为可拖动
            self.model.removeRow(item.row())
            self.model.insertRow(row - 1, new_item)
            self.list_view.setCurrentIndex(self.model.index(row - 1, 0))

    def move_item_down(self, item):
        """将项向下移动"""
        index = self.model.indexFromItem(item)  # 获取该项的索引
        row = item.row()  # 获取项的当前行号
        if row < self.model.rowCount() - 1:  # 确保当前项不是最后一行
            new_item = FileItem(item.data(Qt.UserRole).filename, item.data(Qt.UserRole).index)
            new_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsDragEnabled)  # 设置为可拖动
            self.model.removeRow(item.row())
            self.model.insertRow(row + 1, new_item)
            self.list_view.setCurrentIndex(self.model.index(row + 1, 0))

    def update_list_view(self):
        """更新 QListView 中所有项目的小部件"""
        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            self.set_item_widget(item)

    def sort_alphabetical(self):
        """按字母顺序排序"""
        items = [self.model.item(i).data(Qt.UserRole) for i in range(self.model.rowCount())]
        print(items)
        items.sort()
        print(items)
        # 重新排序模型中的项
        self.model.clear()
        for index, fileinfo in enumerate(items):
            self.add_item(fileinfo.filename, index)

    def sort_by_order(self):
        """按添加顺序排序，假设项目初始顺序是 'Item 1', 'Item 2'..."""
        self.model.clear()
        for i in range(5):
            self.add_item(f"Item {i + 1}", i)

    def print(self):
        items = [self.model.item(i).data(Qt.UserRole) for i in range(self.model.rowCount())]
        print(items)

    def closeEvent(self, a0):
        super().closeEvent(a0)
        self.okSignal.emit(True)


class MergeThread(QThread):
    okSignal = pyqtSignal(bool)
    progressSignal = pyqtSignal(int)

    def __init__(self, input_paths, output_path):
        super().__init__()
        self.input_paths = input_paths
        self.output_path = output_path

    def run(self):
        # 创建一个新的空白 PDF 文件
        # 创建一个用于合并的PDF对象
        merged_pdf = fitz.open()
        save_interval = 100
        output_path = self.output_path
        page_count = 0  # 记录合并的总页数
        tmp_count = 0  # 记录临时文件的个数
        current_page_offset = 0  # 用于书签偏移
        toc = []  # 记录合并PDF的书签
        toc_set = set()
        try:
            for index, pdf_path in enumerate(self.input_paths):
                if not os.path.isfile(pdf_path):
                    print(f"文件未找到: {pdf_path}")
                    continue

                try:
                    pdf_document = fitz.open(pdf_path)
                    # 合并当前PDF的书签
                    tmp_toc = pdf_document.get_toc()  # 获取书签目录
                    if tmp_toc:
                        for entry in tmp_toc:
                            tmp_entry = (entry[0], entry[1])
                            if tmp_entry not in toc_set:
                                toc.append((entry[0], entry[1], entry[2] + current_page_offset))
                                toc_set.add(tmp_entry)

                    # 遍历当前文件的每一页
                    for page_num in range(pdf_document.page_count):
                        merged_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
                        page_count += 1
                        current_page_offset += 1
                        # 每达到设定页数（save_interval）保存一次
                        if page_count % save_interval == 0:
                            tmp_count += 1
                            # 保存并清理无用对象
                            temp_output = output_path + f"{tmp_count % 2}.tmp"
                            merged_pdf.save(temp_output, garbage=4, deflate_images=True)
                            print(f"中间保存 {page_count} 页至文件: {temp_output}")
                            # 关闭并重新打开文件以释放内存
                            merged_pdf.close()
                            merged_pdf = fitz.open(temp_output)

                    pdf_document.close()
                    print(f"已成功添加文件: {pdf_path}")

                except Exception as e:
                    print(f"合并文件 {pdf_path} 时出错: {e}")
                    continue
                self.progressSignal.emit(min((index + 1) * 100 // len(self.input_paths), 99))
            # 最后一次保存合并结果
            print(toc)
            self.progressSignal.emit(99)
            merged_pdf.set_toc(toc)
            merged_pdf.save(output_path, garbage=4, deflate_images=True)
            merged_pdf.close()
            self.progressSignal.emit(100)
            print(f"合并完成，已生成文件: {output_path}")

            # 删除临时文件
            for i in range(2):
                os.remove(output_path + f"{i % 2}.tmp")

        except Exception as e:
            print(f"合并过程中出错: {e}")
        finally:
            # 确保释放资源
            if 'merged_pdf' in locals() and not merged_pdf.is_closed:
                merged_pdf.close()
        self.okSignal.emit(True)
