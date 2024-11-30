import os.path
import random
import re
from multiprocessing import Process, Queue
from typing import List

import fitz
from PySide6.QtCore import Signal, QThread, QUrl, Qt, QFile, QIODevice, QTextStream, QTimer
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon, QFont, QFontMetrics, QGuiApplication, QCursor
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog, QApplication, QDialog, QLabel, QPushButton

from app.model import PdfFile
from app.model.doc_cov_model import Pdf2ImageOpt, Web2PdfOpt
from app.ui.components import FlowLayout
from app.ui.components.QCursorGif import QCursorGif
from app.ui.Icon import Icon
from app.ui.doc_convert.web2pdf.web2pdf_ui import Ui_web2pdf_view
from app.util import common
from app.ui.components.file_list import FileListView
from app.ui.components.router import Router


def open_file_explorer(path):
    # 使用QDesktopServices打开文件管理器
    if os.path.isfile(path):
        path = os.path.dirname(path)
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))


class Web2PdfControl(QWidget, Ui_web2pdf_view, QCursorGif):
    okSignal = Signal(bool)
    childRouterSignal = Signal(str)

    def __init__(self, router: Router, parent=None):
        super().__init__(parent)
        self.total_task_num = 0
        self.finish_task_num = 0
        self.input_urls = []
        self.webs = {}
        self.output_dir = ''
        self.router = router
        self.router_path = (self.parent().router_path if self.parent() else '') + '/网页转PDF'
        self.child_routes = {}
        self.worker = None
        self.running_flag = False

        self.setupUi(self)
        # 设置忙碌光标图片数组
        self.initCursor([':/icons/icons/Cursors/%d.png' %
                         i for i in range(8)], self)
        self.setCursorTimeout(100)

        self.btn_start.clicked.connect(self.merge)

        self.btn_choose_output_dir.setVisible(False)
        self.label_output_dir.setVisible(False)
        self.output_dir = os.path.join(common.get_system_desktop_dir(), 'EasyBox-url2pdf')
        self.comboBox_output_dir.activated.connect(self.select_output_dir)
        self.btn_choose_output_dir.clicked.connect(self.set_output_dir)
        self.lineEdit.textChanged.connect(self.change_url)
        self.input_files = []
        self.output_path = ''
        self.init_ui()
        self.layout = FlowLayout()
        self.widget_urls.setLayout(self.layout)

    def init_ui(self):
        if not self.parent():
            pixmap = QPixmap(Icon.logo_ico_path)
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)
            self.setWindowTitle('网页转PDF')
            style_qss_file = QFile(":/data/resources/QSS/style.qss")
            if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(style_qss_file)
                style_content = stream.readAll()
                self.setStyleSheet(style_content)
                style_qss_file.close()
        # 遍历窗口中的所有子控件并删除按钮
        for child in self.widget_urls.children():
            if isinstance(child, QPushButton):
                child.deleteLater()  # 删除按钮

    def change_url(self):
        text = self.lineEdit.text()

        def extract_links(text):
            # 定义正则表达式来匹配URL
            url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'

            # 使用findall方法查找所有匹配的URL
            links = re.findall(url_pattern, text)

            return links

        self.input_urls = extract_links(text)
        print(self.input_urls)
        if len(self.input_urls) > 0:
            # 遍历布局中的所有控件并删除它们
            for i in reversed(range(self.layout.count())):
                widget = self.layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()
            for url in self.input_urls:
                label = QPushButton()
                label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                label.setMaximumWidth(250)
                font_metrics = QFontMetrics(self.label_output_dir.font())
                # 使用 elidedText 根据按钮宽度生成省略文字
                elided_text = font_metrics.elidedText(url, Qt.ElideRight,
                                                      240)
                label.setText(elided_text)
                label.clicked.connect(
                    lambda checked, url_=url: QDesktopServices.openUrl(QUrl(url_))
                )
                # label.lin
                self.layout.addWidget(label)

    def select_output_dir(self):
        text = self.comboBox_output_dir.currentText()
        if text == '下载目录':
            self.output_dir = os.path.join(common.get_system_download_dir(), 'EasyBox-url2pdf')
            self.label_output_dir.setVisible(False)
            self.btn_choose_output_dir.setVisible(False)
        elif text == '文档目录':
            self.output_dir = os.path.join(common.get_system_document_dir(), 'EasyBox-url2pdf')
            self.label_output_dir.setVisible(False)
            self.btn_choose_output_dir.setVisible(False)
        elif text == '桌面':
            self.output_dir = os.path.join(common.get_system_desktop_dir(), 'EasyBox-url2pdf')
            self.label_output_dir.setVisible(False)
            self.btn_choose_output_dir.setVisible(False)
        elif text == '自定义目录':
            self.label_output_dir.setVisible(True)
            self.btn_choose_output_dir.setVisible(True)
            self.set_output_dir()

    def set_output_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if folder:
            self.output_dir = folder
            font_metrics = QFontMetrics(self.label_output_dir.font())
            # 使用 elidedText 根据按钮宽度生成省略文字
            elided_text = font_metrics.elidedText(self.output_dir, Qt.ElideRight,
                                                  self.label_output_dir.width() - 10)
            self.label_output_dir.setText(elided_text)
            self.label_output_dir.setToolTip(self.output_dir)

    def merge(self):

        if len(self.input_urls) == 0:
            QMessageBox.information(self, '错误', '未识别到链接')
            return
        if self.comboBox_output_dir.currentText() == '自定义目录':
            self.output_path = self.output_dir
        else:
            pass
        cnt = 0
        self.btn_start.setEnabled(False)
        self.startBusy()
        self.total_task_num = len(self.input_urls)
        self.finish_task_num = 0
        while len(self.input_urls) > 0 and cnt < 4:
            cnt += 1
            task = Web2PdfOpt(self.input_urls.pop(0), self.output_dir)
            view = HTMLToPDFConverter(task, title='正在导出PDF，请不要退出')
            view.finishSignal.connect(self.print_one)
            self.startBusy()
            # 获取屏幕信息
            screen = QGuiApplication.primaryScreen().geometry()
            screen_width = screen.width()
            screen_height = screen.height()

            # 确保窗口不会超出屏幕范围
            window_width = 650  # 假设窗口宽度
            window_height = 520  # 假设窗口高度

            # 生成随机位置
            random_x = random.randint(100, max(screen_width - window_width, 102))
            random_y = random.randint(50, max(screen_height - window_height, 52))
            # 将窗口移动到随机位置
            view.move(random_x, random_y)

            view.show()
            self.webs[view.pdf_id] = view

    def print_one(self, pdf_id):
        del self.webs[pdf_id]
        self.finish_task_num += 1
        if len(self.input_urls) > 0:
            task = Web2PdfOpt(self.input_urls.pop(0), self.output_dir)
            view = HTMLToPDFConverter(task, title=f'正在导出PDF，剩余任务{len(self.input_urls)}')
            view.finishSignal.connect(self.print_one)
            self.startBusy()
            # 获取屏幕信息
            screen = QGuiApplication.primaryScreen().geometry()
            screen_width = screen.width()
            screen_height = screen.height()

            # 确保窗口不会超出屏幕范围
            window_width = 650  # 假设窗口宽度
            window_height = 520  # 假设窗口高度

            # 生成随机位置
            random_x = random.randint(100, max(screen_width - window_width, 102))
            random_y = random.randint(50, max(screen_height - window_height, 52))
            # 将窗口移动到随机位置
            view.move(random_x, random_y)

            view.show()
            self.webs[view.pdf_id] = view
        else:
            if self.finish_task_num == self.total_task_num:
                self.stopBusy()
                self.merge_finish(True)

    def update_progress(self, value):
        self.progressBar.setValue(value)

    def merge_finish(self, success):
        self.stopBusy()
        reply = QMessageBox(self)
        reply.setIcon(QMessageBox.Information)
        reply.setWindowTitle('OK')
        reply.setText(f"PDF转换成功")
        btn = reply.addButton('打开', QMessageBox.ActionRole)
        btn.clicked.connect(
            lambda x: open_file_explorer(
                self.output_dir
            )
        )
        # reply.addButton(btn)
        reply.addButton("确认", QMessageBox.AcceptRole)
        reply.addButton("取消", QMessageBox.RejectRole)
        api = reply.exec_()
        # self.close()
        self.btn_start.setEnabled(True)
        self.progressBar.setValue(0)
        self.worker = None

    def closeEvent(self, a0):
        super().closeEvent(a0)
        self.okSignal.emit(True)


class HTMLToPDFConverter(QWebEngineView):
    pdf_id = 0  # 计数器，每次实例化对象计数器加一
    finishSignal = Signal(int)

    def __init__(self, opt: Web2PdfOpt, title: str = ''):
        super().__init__()
        self.scroll_worker = None
        HTMLToPDFConverter.pdf_id += 1
        self.id = HTMLToPDFConverter.pdf_id  # 记录下当前对象的id
        """
        self.html_file: 实际存在的HTML路径或网页URL
        self.new_html_file: 将HTML路径移动到该路径下并删除原来的HTML文件
        filename: 网页URL生成PDF的文件名
        base_dir: 图片等文件所在的文件夹(移动之后new_html_file所在的文件夹)
        """
        self.task_opt = opt
        if not os.path.exists(self.task_opt.o_dir):
            os.makedirs(self.task_opt.o_dir, exist_ok=True)
        if title:
            self.setWindowTitle(title)
        else:
            self.setWindowTitle("正在生成PDF，请耐心等待")
        pixmap = QPixmap(Icon.logo_ico_path)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)
        # 设置页面加载完成后的槽函数
        self.loadFinished.connect(self.onLoadFinished)
        self.page().pdfPrintingFinished.connect(self.finish)
        if self.task_opt.is_url:
            self.setFixedHeight(2000)
        else:
            self.setFixedHeight(500)
        # 加载 HTML 文件
        if self.task_opt.is_url:
            self.setUrl(QUrl(self.task_opt.url))
        else:
            if os.path.exists(self.task_opt.url):
                self.load(QUrl.fromLocalFile(self.task_opt.url))
            else:
                self.setHtml(self.task_opt.url)

    def on_scroll_finished(self, result):
        # 再次等待一段时间，确保所有资源加载完毕
        QTimer.singleShot(5000, self.print_to_pdf)

    def print_to_pdf(self):
        pdf_path = os.path.join(self.task_opt.o_dir, self.task_opt.o_name)
        # 设置页面布局
        self.page().printToPdf(pdf_path)

    def scroll_window(self):
        scroll_script = """
            var scrollDistance = 200;
            var interval = setInterval(function() {
                window.scrollBy(0, scrollDistance);
                if ((window.innerHeight + window.scrollY) >= document.body.scrollHeight) {
                    clearInterval(interval);
                    console.log('Scroll finished');
                }
            }, 100);  // 增加滚动时间间隔
        """
        self.page().runJavaScript(scroll_script)

    def onLoadFinished(self, success):
        if success:
            if self.task_opt.is_url:
                QTimer.singleShot(2000, self.scroll_window)
                # 延时等待所有资源加载完成
                QTimer.singleShot(10000, self.print_to_pdf)
            else:
                self.print_to_pdf()
            # globalSignals.status_bar_message.emit((f"正在导出PDF，请不要退出", 60))

    def add_custom_css(self):
        # 添加 CSS 以防止页面内部分割
        script = """
        window.scrollTo({
          top: document.body.scrollHeight,
          behavior: 'smooth' // 平滑滚动到页面底部
        });
        """
        # self.page().runJavaScript(script)

    def finish(self, success):
        self.finishSignal.emit(self.id)
        self.close()

    def stop(self):
        self.page().thread().quit()


if __name__ == '__main__':
    from PySide6.QtWidgets import QWidget, QApplication
    import sys
    from PySide6.QtGui import QFont, QPixmap, QIcon
    from PySide6.QtCore import Qt

    app = QApplication(sys.argv)
    font = QFont('微软雅黑', 10)  # 使用 Times New Roman 字体，字体大小为 14
    app.setFont(font)
    view = Web2PdfControl(None)
    view.show()
    sys.exit(app.exec())
