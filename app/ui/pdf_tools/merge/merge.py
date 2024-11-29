import os.path
from typing import List

import fitz
from PySide6.QtCore import Signal, QThread, QUrl, Qt, QFile, QIODevice, QTextStream
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon, QFont, QFontMetrics
from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog, QApplication, QDialog

from app.model import PdfFile
from app.ui.components.QCursorGif import QCursorGif
from app.ui.Icon import Icon
from app.ui.pdf_tools.merge.encrypt_dialog import EncryptControl
from app.util import common
from app.ui.pdf_tools.merge.merge_ui import Ui_merge_pdf_view
from app.ui.components.file_list import FileListView
from app.ui.components.router import Router


def open_file_explorer(path):
    # 使用QDesktopServices打开文件管理器
    if os.path.isfile(path):
        path = os.path.dirname(path)
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))


class MergeControl(QWidget, Ui_merge_pdf_view, QCursorGif):
    okSignal = Signal(bool)
    childRouterSignal = Signal(str)

    def __init__(self, router: Router, parent=None):
        super().__init__(parent)
        self.encryption_options = {}
        self.dialog = None
        self.output_filename = '合并PDF'
        self.output_dir = ''
        self.router = router
        self.router_path = (self.parent().router_path if self.parent() else '') + '/合并PDF'
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
        self.btn_choose_files.setIcon(Icon.Add_Icon)
        self.btn_merge.clicked.connect(self.merge)

        self.list_view = FileListView(self)
        self.checkBox_doc_encrypt.clicked.connect(self.set_encrypt_option)
        self.btn_setting.clicked.connect(self.list_view.print)
        self.btn_order_inc.clicked.connect(lambda x: self.list_view.sort_by_name(reverse=False))
        self.btn_order_des.clicked.connect(lambda x: self.list_view.sort_by_name(reverse=True))
        self.checkBox_select_all.clicked.connect(self.select_all)
        self.btn_remove_selected.setEnabled(False)
        self.label_output_dir.setVisible(False)
        self.btn_choose_output_dir.setVisible(False)

        self.btn_remove_selected.clicked.connect(self.remove_selected)
        self.lineEdit_filename.textChanged.connect(self.change_output_filename)

        self.comboBox_output_dir.activated.connect(self.select_output_dir)
        self.btn_choose_output_dir.clicked.connect(self.set_output_dir)

        self.verticalLayout_2.addWidget(self.list_view)

        self.input_files = []
        self.output_path = ''

    def init_ui(self):
        self.btn_merge.setObjectName('border')
        if not self.parent():
            pixmap = QPixmap(Icon.logo_ico_path)
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)
            self.setWindowTitle('合并PDF')
            style_qss_file = QFile(":/data/resources/QSS/style.qss")
            if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(style_qss_file)
                style_content = stream.readAll()
                self.setStyleSheet(style_content)
                style_qss_file.close()
        self.lineEdit_filename.setText(self.output_filename)

    def on_selection_changed(self, selected):
        for index in selected.indexes():
            print("Selected item:", index.data(Qt.UserRole))
            widget = self.list_view.indexWidget(index)
            # widget.is_select = True

    def select_all(self):
        if self.checkBox_select_all.isChecked():
            self.list_view.select_all()
        else:
            self.list_view.dis_select_all()

    def remove_selected(self):
        reply = QMessageBox.question(self, '温馨提示', '确定删除选中的文件？', QMessageBox.No | QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            pass
        else:
            return
        self.list_view.remove_select()

    def change_output_filename(self):
        self.output_filename = common.correct_filename(self.lineEdit_filename.text())

    def select_output_dir(self):
        text = self.comboBox_output_dir.currentText()
        if text == 'PDF相同目录':
            self.label_output_dir.setVisible(False)
            self.btn_choose_output_dir.setVisible(False)
        elif text == '自定义目录':
            self.label_output_dir.setVisible(True)
            self.btn_choose_output_dir.setVisible(True)

    def set_output_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if folder:
            self.output_dir = folder
            font_metrics = QFontMetrics(self.label_output_dir.font())
            # 使用 elidedText 根据按钮宽度生成省略文字
            elided_text = font_metrics.elidedText(self.output_dir, Qt.ElideRight, self.label_output_dir.width() - 10)
            self.label_output_dir.setText(elided_text)
            self.label_output_dir.setToolTip(self.output_dir)

    def open_file_dialog(self):
        # 打开文件对话框，设置多文件选择和 PDF 文件过滤
        files, _ = QFileDialog.getOpenFileNames(self, "选择 PDF 文件", "", "PDF Files (*.pdf);;All Files (*)")
        if files:
            print(files)
            self.input_files = files
            for index, file in enumerate(files):
                self.add_item(file, index)
            self.btn_remove_selected.setEnabled(True)
            self.checkBox_select_all.setChecked(True)
        if files and not self.output_dir:
            self.output_dir = os.path.dirname(files[0])
            font_metrics = QFontMetrics(self.label_output_dir.font())
            # 使用 elidedText 根据按钮宽度生成省略文字
            elided_text = font_metrics.elidedText(self.output_dir, Qt.ElideRight, self.label_output_dir.width() - 10)
            self.label_output_dir.setText(elided_text)
            self.label_output_dir.setToolTip(self.output_dir)

    def merge(self):
        input_files = self.list_view.get_data()

        if len(input_files) < 2:
            QMessageBox.information(self, '温馨提示', "请至少选择两个文件")
            return

        self.btn_merge.setEnabled(False)

        fileinfo = input_files[0]
        if self.comboBox_output_dir.currentText() == '自定义目录':
            self.output_path = os.path.join(self.output_dir, self.output_filename + '.pdf')
        else:
            self.output_path = os.path.join(os.path.dirname(fileinfo.file_path), self.output_filename + '.pdf')
        self.output_path = common.usable_filepath(self.output_path)
        self.startBusy()
        output_info = PdfFile(self.output_path)
        output_info.encryption_options = self.encryption_options
        self.worker = MergeThread(input_files, output_info)
        self.worker.okSignal.connect(self.merge_finish)
        self.worker.progressSignal.connect(self.update_progress)
        self.worker.start()

    def update_progress(self, value):
        self.progressBar.setValue(value)

    def merge_finish(self, success):

        self.stopBusy()
        reply = QMessageBox(self)
        reply.setIcon(QMessageBox.Information)
        reply.setWindowTitle('OK')
        reply.setText(f"PDF合并成功")
        btn = reply.addButton('打开', QMessageBox.ActionRole)
        btn.clicked.connect(
            lambda x: open_file_explorer(
                self.output_path
            )
        )
        # reply.addButton(btn)
        reply.addButton("确认", QMessageBox.AcceptRole)
        reply.addButton("取消", QMessageBox.RejectRole)
        api = reply.exec_()
        # self.close()
        self.btn_merge.setEnabled(True)
        self.list_view.clear()
        self.progressBar.setValue(0)
        self.worker = None

    def add_item(self, text, index):
        """添加自定义组件到 QListView"""
        self.list_view.add_item(text, index)

    def print(self):
        self.list_view.parent()

    def closeEvent(self, a0):
        super().closeEvent(a0)
        self.okSignal.emit(True)

    def set_encrypt_option(self):
        if self.dialog is None:
            self.dialog = EncryptControl(self)
        relay = self.dialog.exec_()
        if relay == QDialog.Accepted:
            self.encryption_options = self.dialog.get_data()
            self.checkBox_doc_encrypt.setChecked(True)
        else:
            self.dialog = None
            self.encryption_options = {}
            self.checkBox_doc_encrypt.setChecked(False)


class MergeThread(QThread):
    okSignal = Signal(bool)
    progressSignal = Signal(int)

    def __init__(self, input_file_infos: List[PdfFile], output_file_info: PdfFile):
        super().__init__()
        self.input_file_infos = input_file_infos
        self.output_file_info = output_file_info

    def run(self):
        # 创建一个新的空白 PDF 文件
        # 创建一个用于合并的PDF对象
        merged_pdf = fitz.open()
        save_interval = 100
        output_path = self.output_file_info.file_path
        page_count = 0  # 记录合并的总页数
        tmp_count = 0  # 记录临时文件的个数
        current_page_offset = 0  # 用于书签偏移
        toc = []  # 记录合并PDF的书签
        toc_set = set()
        try:
            for index, fileinfo in enumerate(self.input_file_infos):
                pdf_path = fileinfo.file_path
                if not os.path.isfile(pdf_path):
                    print(f"文件未找到: {pdf_path}")
                    continue

                try:
                    pdf_document = fitz.open(pdf_path)
                    # 合并当前PDF的书签,下标从1开始
                    tmp_toc = pdf_document.get_toc()  # 获取书签目录
                    start_page_num = fileinfo.start_page_num - 1
                    end_page_num = fileinfo.end_page_num - 1
                    if tmp_toc:
                        for entry in tmp_toc:
                            tmp_entry = (entry[0], entry[1])
                            if start_page_num + 1 <= entry[2] <= end_page_num + 1:
                                if tmp_entry not in toc_set:
                                    toc.append((entry[0], entry[1], entry[2] + current_page_offset))
                                    toc_set.add(tmp_entry)

                    # 遍历当前文件的每一页
                    for page_num in range(pdf_document.page_count):
                        if page_num + start_page_num > end_page_num:
                            break
                        merged_pdf.insert_pdf(pdf_document, from_page=start_page_num + page_num,
                                              to_page=start_page_num + page_num)
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
                self.progressSignal.emit(min((index + 1) * 100 // len(self.input_file_infos), 99))
            # 最后一次保存合并结果
            print(toc)
            self.progressSignal.emit(99)
            merged_pdf.set_toc(toc)
            merged_pdf.save(output_path, garbage=4, deflate_images=True, **self.output_file_info.encryption_options)
            merged_pdf.close()
            self.progressSignal.emit(100)
            print(f"合并完成，已生成文件: {output_path}")

            # 删除临时文件
            for i in range(2):
                if os.path.exists(output_path + f"{i % 2}.tmp"):
                    os.remove(output_path + f"{i % 2}.tmp")

        except Exception as e:
            print(f"合并过程中出错: {e}")
        finally:
            # 确保释放资源
            if 'merged_pdf' in locals() and not merged_pdf.is_closed:
                merged_pdf.close()
        self.okSignal.emit(True)


if __name__ == '__main__':
    from PySide6.QtWidgets import QWidget, QApplication
    import sys
    from PySide6.QtGui import QFont, QPixmap, QIcon
    from PySide6.QtCore import Qt


    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication([])
    font = QFont('微软雅黑', 10)  # 使用 Times New Roman 字体，字体大小为 14
    app.setFont(font)
    view = MergeControl(None)
    view.show()
    sys.exit(app.exec_())
