import os.path
import re
from typing import List, Tuple

import fitz
from PySide6.QtCore import Signal, QThread, QUrl, Qt, QFile, QIODevice, QTextStream
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon, QFont, QFontMetrics
from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog, QButtonGroup, QDialog

from app.model import PdfFile
from app.ui.components.QCursorGif import QCursorGif
from app.ui.Icon import Icon
from app.util import common
from app.ui.pdf_tools.split.split_ui import Ui_split_pdf_view
from app.ui.components.router import Router
from app.log import logger


def open_file_explorer(path):
    # 使用QDesktopServices打开文件管理器
    if os.path.isfile(path):
        path = os.path.dirname(path)
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))


class SplitControl(QWidget, Ui_split_pdf_view, QCursorGif):
    okSignal = Signal(bool)
    childRouterSignal = Signal(str)

    def __init__(self, router: Router, parent=None):
        super().__init__(parent)
        self.input_file_path = ""
        self.output_dir = ""
        self.output_prefix = "拆分文件"
        self.total_pages = 0
        self.router = router
        self.router_path = (self.parent().router_path if self.parent() else '') + '/拆分PDF'
        self.child_routes = {}
        self.worker = None
        self.running_flag = False
        self.setupUi(self)
        # 设置忙碌光标图片数组
        self.initCursor([':/icons/icons/Cursors/%d.png' %
                        i for i in range(8)], self)
        self.setCursorTimeout(100)
        self.init_ui()
        
        # 按钮连接
        self.btn_choose_file.clicked.connect(self.open_file_dialog)
        self.btn_choose_file.setIcon(Icon.Add_Icon)
        self.btn_split.clicked.connect(self.split_pdf)
        
        # 选项按钮组
        self.option_group = QButtonGroup(self)
        self.option_group.addButton(self.radioButton_by_pages)
        self.option_group.addButton(self.radioButton_by_ranges)
        self.option_group.addButton(self.radioButton_single_page)
        self.option_group.addButton(self.radioButton_all_pages)
        self.radioButton_by_pages.toggled.connect(self.update_option_ui)
        self.radioButton_by_ranges.toggled.connect(self.update_option_ui)
        self.radioButton_single_page.toggled.connect(self.update_option_ui)
        self.radioButton_all_pages.toggled.connect(self.update_option_ui)
        
        # 输出选项连接
        self.lineEdit_prefix.textChanged.connect(self.change_output_prefix)
        self.comboBox_output_dir.activated.connect(self.select_output_dir)
        self.btn_choose_output_dir.clicked.connect(self.set_output_dir)
        
        # 初始界面设置
        self.label_output_dir.setVisible(False)
        self.btn_choose_output_dir.setVisible(False)
        self.btn_split.setEnabled(False)
        
    def init_ui(self):
        self.btn_split.setObjectName('border')
        if not self.parent():
            pixmap = QPixmap(Icon.logo_ico_path)
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)
            self.setWindowTitle('拆分PDF')
            style_qss_file = QFile(":/data/resources/QSS/style.qss")
            if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(style_qss_file)
                style_content = stream.readAll()
                self.setStyleSheet(style_content)
                style_qss_file.close()
        self.lineEdit_prefix.setText(self.output_prefix)
    
    def update_option_ui(self):
        # 更新选项界面状态
        self.spinBox_pages.setEnabled(self.radioButton_by_pages.isChecked())
        self.lineEdit_ranges.setEnabled(self.radioButton_by_ranges.isChecked())
        self.spinBox_single.setEnabled(self.radioButton_single_page.isChecked())
        
        # 更新单页提取的最大值
        if self.total_pages > 0 and self.radioButton_single_page.isChecked():
            self.spinBox_single.setMaximum(self.total_pages)
    
    def change_output_prefix(self):
        self.output_prefix = common.correct_filename(self.lineEdit_prefix.text())
    
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
        # 打开文件对话框，选择PDF文件
        file_path, _ = QFileDialog.getOpenFileName(self, "选择PDF文件", "", "PDF Files (*.pdf);;All Files (*)")
        if file_path:
            self.input_file_path = file_path
            self.lineEdit_pdf_path.setText(file_path)
            self.btn_split.setEnabled(True)
            
            # 获取PDF页数
            try:
                with fitz.open(file_path) as pdf:
                    self.total_pages = len(pdf)
                    # 更新单页提取的最大值
                    self.spinBox_single.setMaximum(self.total_pages)
            except Exception as e:
                logger.error(f"读取PDF文件错误: {str(e)}")
                QMessageBox.critical(self, "错误", f"无法读取PDF文件: {str(e)}")
                self.btn_split.setEnabled(False)
                return
            
            # 如果未设置输出目录，默认使用与PDF相同的目录
            if not self.output_dir:
                self.output_dir = os.path.dirname(file_path)
                font_metrics = QFontMetrics(self.label_output_dir.font())
                elided_text = font_metrics.elidedText(self.output_dir, Qt.ElideRight, self.label_output_dir.width() - 10)
                self.label_output_dir.setText(elided_text)
                self.label_output_dir.setToolTip(self.output_dir)
                
            # 输出文件前缀格式：原文件名+拆分+文件
            filename = os.path.basename(file_path)
            filename_without_ext = os.path.splitext(filename)[0]
            new_prefix = f"{filename_without_ext}_拆分文件"
            self.output_prefix = new_prefix
            self.lineEdit_prefix.setText(new_prefix)
    
    def split_pdf(self):
        if not os.path.exists(self.input_file_path):
            QMessageBox.critical(self, "错误", "请先选择PDF文件")
            return
        
        # 获取输出目录
        if self.comboBox_output_dir.currentText() == '自定义目录' and self.output_dir:
            output_directory = self.output_dir
        else:
            output_directory = os.path.dirname(self.input_file_path)
        
        # 如果输出目录不存在，创建它
        if not os.path.exists(output_directory):
            try:
                os.makedirs(output_directory)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法创建输出目录: {str(e)}")
                return
        
        # 根据选项确定拆分方式
        split_ranges = []
        
        # 按页数拆分
        if self.radioButton_by_pages.isChecked():
            pages_per_file = self.spinBox_pages.value()
            if pages_per_file <= 0:
                QMessageBox.warning(self, "警告", "每个文件的页数必须大于0")
                return
                
            # 计算拆分范围
            for i in range(0, self.total_pages, pages_per_file):
                end = min(i + pages_per_file - 1, self.total_pages - 1)
                split_ranges.append((i, end))
        
        # 按页码范围拆分
        elif self.radioButton_by_ranges.isChecked():
            ranges_text = self.lineEdit_ranges.text().strip()
            if not ranges_text:
                QMessageBox.warning(self, "警告", "请输入页码范围")
                return
                
            try:
                split_ranges = self.parse_page_ranges(ranges_text)
                if not split_ranges:
                    QMessageBox.warning(self, "警告", "无效的页码范围")
                    return
                    
                # 验证页码是否在范围内
                for start, end in split_ranges:
                    if start < 0 or end >= self.total_pages or start > end:
                        QMessageBox.warning(self, "警告", f"页码范围 {start+1}-{end+1} 超出文件范围(1-{self.total_pages})")
                        return
            except ValueError as e:
                QMessageBox.warning(self, "警告", str(e))
                return
        
        # 提取单页
        elif self.radioButton_single_page.isChecked():
            page_num = self.spinBox_single.value() - 1  # 转为0基索引
            if page_num < 0 or page_num >= self.total_pages:
                QMessageBox.warning(self, "警告", f"页码必须在1到{self.total_pages}之间")
                return
                
            split_ranges = [(page_num, page_num)]
        
        # 拆分为单页
        elif self.radioButton_all_pages.isChecked():
            split_ranges = [(i, i) for i in range(self.total_pages)]
        
        # 禁用按钮，开始任务
        self.btn_split.setEnabled(False)
        self.startBusy()
        
        # 创建并启动工作线程
        input_file = PdfFile(self.input_file_path)
        self.worker = SplitThread(input_file, self.output_prefix, output_directory, split_ranges)
        self.worker.progressSignal.connect(self.update_progress)
        self.worker.okSignal.connect(self.split_finish)
        self.worker.start()
    
    def update_progress(self, value):
        self.progressBar.setValue(value)
    
    def split_finish(self, result_data):
        self.stopBusy()
        success, output_dir = result_data
        
        if success:
            reply = QMessageBox(self)
            reply.setIcon(QMessageBox.Information)
            reply.setWindowTitle('完成')
            reply.setText(f"PDF拆分成功")
            btn = reply.addButton('打开文件夹', QMessageBox.ActionRole)
            btn.clicked.connect(lambda: open_file_explorer(output_dir))
            reply.addButton("确认", QMessageBox.AcceptRole)
            reply.exec_()
        else:
            QMessageBox.critical(self, "错误", f"PDF拆分失败: {output_dir}")
        
        # 恢复UI状态
        self.btn_split.setEnabled(True)
        self.progressBar.setValue(0)
        self.worker = None
    
    def parse_page_ranges(self, ranges_text: str) -> List[Tuple[int, int]]:
        """解析页码范围文本，返回(开始页,结束页)的列表，页码从0开始"""
        result = []
        # 验证格式
        if not re.match(r'^(\d+(-\d+)?)(,\d+(-\d+)?)*$', ranges_text):
            raise ValueError("页码范围格式不正确。正确格式示例: 1-5,7,10-12")
            
        ranges = ranges_text.split(',')
        for r in ranges:
            if '-' in r:
                start, end = r.split('-')
                try:
                    start_idx = int(start) - 1  # 转为0基索引
                    end_idx = int(end) - 1
                    if start_idx > end_idx:
                        raise ValueError(f"范围 {start}-{end} 中，起始页不能大于结束页")
                    result.append((start_idx, end_idx))
                except ValueError:
                    raise ValueError(f"无效的页码范围: {r}")
            else:
                try:
                    page_idx = int(r) - 1  # 转为0基索引
                    result.append((page_idx, page_idx))
                except ValueError:
                    raise ValueError(f"无效的页码: {r}")
        return result
    
    def closeEvent(self, event):
        super().closeEvent(event)
        self.okSignal.emit(True)


class SplitThread(QThread):
    okSignal = Signal(tuple)  # (success, output_dir)
    progressSignal = Signal(int)

    def __init__(self, input_file: PdfFile, output_prefix: str, output_dir: str, page_ranges: List[Tuple[int, int]]):
        super().__init__()
        self.input_file = input_file
        self.output_prefix = output_prefix
        self.output_dir = output_dir
        self.page_ranges = page_ranges
    
    def run(self):
        try:
            # 打开输入PDF
            pdf_document = fitz.open(self.input_file.file_path)
            total_ranges = len(self.page_ranges)
            
            for i, (start_page, end_page) in enumerate(self.page_ranges):
                # 创建新的PDF文档
                output_pdf = fitz.open()
                
                # 复制页面
                for page_num in range(start_page, end_page + 1):
                    output_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
                
                # 生成输出文件名
                if len(self.page_ranges) == 1:
                    output_filename = f"{self.output_prefix}.pdf"
                else:
                    # 根据页码范围生成文件名
                    if start_page == end_page:
                        page_part = f"{start_page + 1}"
                    else:
                        page_part = f"{start_page + 1}-{end_page + 1}"
                    output_filename = f"{self.output_prefix}_{page_part}.pdf"
                
                output_path = os.path.join(self.output_dir, output_filename)
                output_path = common.usable_filepath(output_path)
                
                # 保存PDF
                output_pdf.save(output_path)
                output_pdf.close()
                
                # 更新进度
                progress = int((i + 1) / total_ranges * 100)
                self.progressSignal.emit(progress)
            
            pdf_document.close()
            self.okSignal.emit((True, self.output_dir))
            
        except Exception as e:
            logger.error(f"PDF拆分错误: {str(e)}")
            self.okSignal.emit((False, str(e)))


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys
    from PySide6.QtGui import QFont
    
    app = QApplication(sys.argv)
    font = QFont('微软雅黑', 10)
    app.setFont(font)
    router = Router(None)
    view = SplitControl(router)
    view.show()
    sys.exit(app.exec()) 