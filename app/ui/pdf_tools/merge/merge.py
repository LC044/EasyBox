import json
import os.path
import re
import sys
import traceback

import fitz
from PyQt5.QtCore import pyqtSignal, QThread, QFile, QIODevice, QTextStream, QUrl, Qt, QSize, QMimeData, QPoint
from PyQt5.QtGui import QDesktopServices, QPixmap, QIcon, QStandardItemModel, QStandardItem, QDrag
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QAbstractItemView, QLabel, QPushButton, QHBoxLayout, \
    QStyledItemDelegate, QListView
from PyQt5 import QtCore, QtGui, QtWidgets

from app.ui.components import ScrollBar
from app.ui.components.QCursorGif import QCursorGif
from app.ui.Icon import Icon
from .merge_ui import Ui_merge_pdf_view
from ...components.file_list import FileItemWidget
from ...components.file_list import FileListView
from ...components.router import Router


def open_file_explorer(path):
    # 使用QDesktopServices打开文件管理器
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))


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

        self.list_view = FileListView(self)
        self.btn_setting.clicked.connect(self.list_view.print)
        self.btn_order_inc.clicked.connect(lambda x: self.list_view.sort_by_name(reverse=False))
        self.btn_order_des.clicked.connect(lambda x: self.list_view.sort_by_name(reverse=True))
        self.verticalLayout_2.addWidget(self.list_view)

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
        self.list_view.add_item(text, index)

    def print(self):
        self.list_view.parent()

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
