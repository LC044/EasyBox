import os.path
import os
from multiprocessing import Process, Queue
from typing import List

from PySide6.QtCore import Signal, QThread, QUrl, Qt, QFile, QIODevice, QTextStream
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon, QFontMetrics
from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog

from app.model import PdfFile, Pdf2DocxOpt
from pdf2docx import Converter
from app.ui.components.QCursorGif import QCursorGif
from app.ui.Icon import Icon
from app.ui.doc_convert.pdf2wordui.pdf2word_ui import Ui_pdf2word_view
from app.util import common
from app.ui.components.file_list import FileListView
from app.ui.components.router import Router


def open_file_explorer(path):
    # 使用QDesktopServices打开文件管理器
    if os.path.isfile(path):
        path = os.path.dirname(path)
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))


class Pdf2WordControl(QWidget, Ui_pdf2word_view, QCursorGif):
    okSignal = Signal(bool)
    childRouterSignal = Signal(str)

    def __init__(self, router: Router, parent=None):
        super().__init__(parent)
        self.output_dir = ''
        self.encryption_options = {}
        self.dialog = None
        self.output_filename = '合并PDF'
        self.router = router
        self.router_path = (self.parent().router_path if self.parent() else '') + '/PDF转Word'
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

        self.btn_setting.clicked.connect(self.list_view.print)
        self.btn_order_inc.clicked.connect(lambda x: self.list_view.sort_by_name(reverse=False))
        self.btn_order_des.clicked.connect(lambda x: self.list_view.sort_by_name(reverse=True))
        self.checkBox_select_all.clicked.connect(self.select_all)
        self.btn_remove_selected.setEnabled(False)
        self.btn_remove_selected.clicked.connect(self.remove_selected)
        self.verticalLayout_2.addWidget(self.list_view)

        self.label_output_dir.setVisible(False)
        self.btn_choose_output_dir.setVisible(False)

        self.comboBox_output_dir.activated.connect(self.select_output_dir)
        self.btn_choose_output_dir.clicked.connect(self.set_output_dir)
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

    def remove_selected(self):
        reply = QMessageBox.question(self, '温馨提示', '确定删除选中的文件？', QMessageBox.No | QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            pass
        else:
            return
        self.list_view.remove_select()

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
        if len(input_files) < 1:
            return
        self.btn_merge.setEnabled(False)

        fileinfo = input_files[0]
        if self.comboBox_output_dir.currentText() == '自定义目录':
            self.output_path = self.output_dir
        else:
            self.output_path = os.path.dirname(fileinfo.file_path)

        self.startBusy()
        output_opt = Pdf2DocxOpt(self.output_path)
        self.worker = Pdf2WordThread(input_files, output_opt)
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
        reply.setText(f"完成")
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


class Pdf2WordThread(QThread):
    okSignal = Signal(bool)
    progressSignal = Signal(int)

    def __init__(self, input_file_infos: List[PdfFile], output_opt: Pdf2DocxOpt):
        super().__init__()
        self.input_file_infos = input_file_infos
        self.output_opt = output_opt

    def run(self):
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
                p = Process(target=self.process_task, args=(task_queue, result_queue))
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
            print(f"PDF转Word完成，已生成文件")

        except Exception as e:
            print(f"合并过程中出错: {e}")
        finally:
            for p in processes:
                p.join()

        self.okSignal.emit(True)

    @staticmethod
    def process_task(task_queue: Queue, result_queue: Queue):
        while not task_queue.empty():
            try:
                fileinfo = task_queue.get_nowait()
                pdf_path = fileinfo.file_path

                if not os.path.isfile(pdf_path):
                    result_queue.put({"status": "error", "error": "文件未找到", "filepath": pdf_path})
                    continue

                start_page_num = fileinfo.start_page_num
                end_page_num = fileinfo.end_page_num

                try:
                    cv = Converter(pdf_path)
                    output_path = os.path.join(fileinfo.save_path, fileinfo.file_name.rstrip('.pdf')+'.docx')
                    cv.convert(output_path, start=start_page_num - 1, end=end_page_num)
                    cv.close()

                    result_queue.put({"status": "success", "filepath": pdf_path})
                except Exception as e:
                    result_queue.put({"status": "error", "error": str(e), "filepath": pdf_path})

            except Exception as e:
                result_queue.put({"status": "error", "error": str(e), "filepath": None})


if __name__ == '__main__':
    from PySide6.QtWidgets import QWidget, QApplication
    import sys
    from PySide6.QtGui import QFont, QPixmap, QIcon
    from PySide6.QtCore import Qt

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    font = QFont('微软雅黑', 10)  # 使用 Times New Roman 字体，字体大小为 14
    app.setFont(font)
    view = Pdf2WordControl(None)
    view.show()
    sys.exit(app.exec_())
