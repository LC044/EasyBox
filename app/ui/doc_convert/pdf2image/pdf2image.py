import os.path
from multiprocessing import Process, Queue
from typing import List

import fitz
from PySide6.QtCore import Signal, QThread, QUrl, Qt, QFile, QIODevice, QTextStream
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon, QFont, QFontMetrics
from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog, QApplication, QDialog

from app.model import PdfFile
from app.model.doc_cov_model import Pdf2ImageOpt
from app.ui.components.QCursorGif import QCursorGif
from app.ui.Icon import Icon
from app.ui.doc_convert.pdf2image.pdf2image_ui import Ui_pdf2image_view
from app.util import common
from app.ui.components.file_list import FileListView
from app.ui.components.router import Router


def open_file_explorer(path):
    # 使用QDesktopServices打开文件管理器
    if os.path.isfile(path):
        path = os.path.dirname(path)
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))


class Pdf2ImageControl(QWidget, Ui_pdf2image_view, QCursorGif):
    okSignal = Signal(bool)
    childRouterSignal = Signal(str)

    def __init__(self, router: Router, parent=None):
        super().__init__(parent)
        self.output_dir = ''
        self.encryption_options = {}
        self.dialog = None
        self.output_filename = '合并PDF'
        self.router = router
        self.router_path = (self.parent().router_path if self.parent() else '') + '/PDF转图片'
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
        self.btn_start.clicked.connect(self.merge)
        self.list_view = FileListView(self)
        self.btn_setting.clicked.connect(self.list_view.print)
        self.checkBox_select_all.clicked.connect(self.select_all)
        self.btn_remove_selected.setEnabled(False)
        self.btn_remove_selected.clicked.connect(self.remove_selected)

        self.label_output_dir.setVisible(False)
        self.btn_choose_output_dir.setVisible(False)

        self.comboBox_output_dir.activated.connect(self.select_output_dir)
        self.btn_choose_output_dir.clicked.connect(self.set_output_dir)

        self.verticalLayout_2.addWidget(self.list_view)
        self.input_files = []
        self.output_path = ''

    def init_ui(self):
        self.btn_start.setObjectName('border')
        if not self.parent():
            pixmap = QPixmap(Icon.logo_ico_path)
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)
            self.setWindowTitle('PDF转图片')
            style_qss_file = QFile(":/data/QSS/style.qss")
            if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(style_qss_file)
                style_content = stream.readAll()
                self.setStyleSheet(style_content)
                style_qss_file.close()

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

    def merge(self):
        input_files = self.list_view.get_data()
        self.btn_start.setEnabled(False)
        self.startBusy()

        if self.comboBox_output_dir.currentText() == '自定义目录':
            self.output_path = self.output_dir
        else:
            fileinfo = input_files[0]
            self.output_path = os.path.dirname(fileinfo.file_path)

        output_opt = Pdf2ImageOpt(self.output_path, format_='png', dpi=200)
        self.worker = Pdf2ImageThread(input_files, output_opt)
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
        reply.setText(f"PDF转图片成功")
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
        self.btn_start.setEnabled(True)
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



class Pdf2ImageThread(QThread):
    okSignal = Signal(bool)
    progressSignal = Signal(int)

    def __init__(self, input_file_infos: List[PdfFile], output_opt: Pdf2ImageOpt):
        super().__init__()
        self.input_file_infos = input_file_infos
        self.output_opt = output_opt

    def run(self):
        dpi = self.output_opt.o_dpi
        # 计算缩放比例
        zoom_x = dpi / 72  # 水平缩放因子
        zoom_y = dpi / 72  # 垂直缩放因子
        mat = fitz.Matrix(zoom_x, zoom_y)  # 缩放矩阵
        task_queue = Queue()
        result_queue = Queue()
        processes = []

        try:
            # 创建多进程任务
            for fileinfo in self.input_file_infos:
                fileinfo.save_path = self.output_opt.o_dir
                task_queue.put(fileinfo)

            num_processes = min(len(self.input_file_infos), os.cpu_count())
            for _ in range(num_processes):
                p = Process(target=self.process_task, args=(task_queue, result_queue, mat))
                p.start()
                processes.append(p)

            completed_tasks = 0
            total_tasks = len(self.input_file_infos)

            while completed_tasks < total_tasks:
                result = result_queue.get()
                if result["status"] == "success":
                    completed_tasks += 1
                    progress = min(completed_tasks * 100 // total_tasks, 99)
                    self.progressSignal.emit(progress)
                else:
                    print(f"处理文件出错: {result['error']} 文件: {result['filepath']}")

            self.progressSignal.emit(100)
            print(f"PDF转图片完成")
        except Exception as e:
            print(f"合并过程中出错: {e}")
        finally:
            for p in processes:
                p.join()
        self.okSignal.emit(True)

    @staticmethod
    def process_task(task_queue: Queue, result_queue: Queue, mat):
        while not task_queue.empty():
            try:
                fileinfo = task_queue.get_nowait()
                pdf_path = fileinfo.file_path

                if not os.path.isfile(pdf_path):
                    result_queue.put({"status": "error", "error": "文件未找到", "filepath": pdf_path})
                    continue

                pdf_path = fileinfo.file_path
                if not os.path.isfile(pdf_path):
                    print(f"文件未找到: {pdf_path}")
                    continue

                file_name = fileinfo.file_name.rstrip('.pdf')
                output_dir = fileinfo.save_path + '/' + file_name
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                try:
                    pdf_document = fitz.open(pdf_path)
                    # 获取总页数
                    total_pages = len(pdf_document)
                    digit_count = len(str(total_pages))  # 计算页码需要的位数
                    start_page_num = fileinfo.start_page_num - 1
                    end_page_num = fileinfo.end_page_num - 1

                    # 遍历当前文件的每一页
                    for page_num in range(start_page_num, end_page_num + 1):
                        page = pdf_document.load_page(page_num)
                        pix = page.get_pixmap(matrix=mat)
                        # 保存图片
                        formatted_page_number = str(page_num + 1).zfill(digit_count)  # 用零填充到固定宽度
                        output_path = f"{output_dir}/{file_name}_{formatted_page_number}.png"
                        pix.save(output_path)

                    pdf_document.close()
                    print(f"已成功添加文件: {pdf_path}")
                    result_queue.put({"status": "success", "filepath": pdf_path})
                except Exception as e:
                    print(f"合并文件 {pdf_path} 时出错: {e}")
                    result_queue.put({"status": "error", "error": str(e), "filepath": pdf_path})
            except Exception as e:
                result_queue.put({"status": "error", "error": str(e), "filepath": None})


if __name__ == '__main__':
    from PySide6.QtWidgets import QWidget, QApplication
    import sys
    from PySide6.QtGui import QFont, QPixmap, QIcon
    from PySide6.QtCore import Qt

    app = QApplication(sys.argv)
    font = QFont('微软雅黑', 10)  # 使用 Times New Roman 字体，字体大小为 14
    app.setFont(font)
    view = Pdf2ImageControl(None)
    view.show()
    sys.exit(app.exec())
