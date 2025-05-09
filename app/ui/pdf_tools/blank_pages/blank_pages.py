import os.path
import shutil
import tempfile
from typing import List, Dict, Tuple, Set

import fitz
import numpy as np
from PIL import Image
from PySide6.QtCore import Signal, QThread, QUrl, Qt, QFile, QIODevice, QTextStream
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon, QFont, QFontMetrics, QImage
from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog, QListWidgetItem, QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

from app.model import PdfFile
from app.ui.components.QCursorGif import QCursorGif
from app.ui.Icon import Icon
from app.util import common
from app.ui.pdf_tools.blank_pages.blank_pages_ui import Ui_blank_pages_view
from app.ui.components.router import Router
from app.log import logger


def open_file_explorer(path):
    # 使用QDesktopServices打开文件管理器
    if os.path.isfile(path):
        path = os.path.dirname(path)
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))


class BlankPagesControl(QWidget, Ui_blank_pages_view, QCursorGif):
    okSignal = Signal(bool)
    childRouterSignal = Signal(str)

    def __init__(self, router: Router, parent=None):
        super().__init__(parent)
        self.input_file_path = ""
        self.output_dir = ""
        self.output_suffix = "_无空白页"
        self.batch_files = []  # 批量处理文件列表
        self.blank_pages_dict = {}  # 存储每个文件的空白页信息 {file_path: [page_nums]}
        self.router = router
        self.router_path = (self.parent().router_path if self.parent() else '') + '/删除空白页'
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
        self.btn_process.clicked.connect(self.process_files)
        self.btn_preview.clicked.connect(self.preview_blank_page)
        
        # 批量文件操作
        self.btn_add_files.clicked.connect(self.add_files)
        self.btn_remove_file.clicked.connect(self.remove_file)
        self.btn_clear_files.clicked.connect(self.clear_files)
        self.listWidget_files.itemClicked.connect(self.select_file)
        
        # 输出选项连接
        self.lineEdit_suffix.textChanged.connect(self.change_output_suffix)
        self.comboBox_output_dir.activated.connect(self.select_output_dir)
        self.btn_choose_output_dir.clicked.connect(self.set_output_dir)
        
        # 初始界面设置
        self.label_output_dir.setVisible(False)
        self.btn_choose_output_dir.setVisible(False)
        self.btn_process.setEnabled(False)
        self.btn_preview.setEnabled(False)
        
    def init_ui(self):
        self.btn_process.setObjectName('border')
        if not self.parent():
            pixmap = QPixmap(Icon.logo_ico_path)
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)
            self.setWindowTitle('删除PDF空白页')
            style_qss_file = QFile(":/data/resources/QSS/style.qss")
            if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(style_qss_file)
                style_content = stream.readAll()
                self.setStyleSheet(style_content)
                style_qss_file.close()
        self.lineEdit_suffix.setText(self.output_suffix)
    
    def change_output_suffix(self):
        self.output_suffix = common.correct_filename(self.lineEdit_suffix.text())
    
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
            self.add_file_to_batch(file_path)
            
            # 如果未设置输出目录，默认使用与PDF相同的目录
            if not self.output_dir:
                self.output_dir = os.path.dirname(file_path)
                font_metrics = QFontMetrics(self.label_output_dir.font())
                elided_text = font_metrics.elidedText(self.output_dir, Qt.ElideRight, self.label_output_dir.width() - 10)
                self.label_output_dir.setText(elided_text)
                self.label_output_dir.setToolTip(self.output_dir)
                
            # 检测空白页
            self.detect_blank_pages(file_path)
    
    def add_files(self):
        # 打开文件对话框，选择多个PDF文件
        file_paths, _ = QFileDialog.getOpenFileNames(self, "选择PDF文件", "", "PDF Files (*.pdf);;All Files (*)")
        if file_paths:
            for file_path in file_paths:
                self.add_file_to_batch(file_path)
            
            # 如果未设置输出目录，默认使用第一个PDF的目录
            if not self.output_dir and file_paths:
                self.output_dir = os.path.dirname(file_paths[0])
                font_metrics = QFontMetrics(self.label_output_dir.font())
                elided_text = font_metrics.elidedText(self.output_dir, Qt.ElideRight, self.label_output_dir.width() - 10)
                self.label_output_dir.setText(elided_text)
                self.label_output_dir.setToolTip(self.output_dir)
                
            # 检测第一个文件的空白页
            if file_paths:
                self.detect_blank_pages(file_paths[0])
    
    def add_file_to_batch(self, file_path):
        # 添加文件到批量处理列表
        if file_path not in self.batch_files:
            self.batch_files.append(file_path)
            filename = os.path.basename(file_path)
            item = QListWidgetItem(filename)
            item.setToolTip(file_path)
            self.listWidget_files.addItem(item)
            self.btn_process.setEnabled(True)
    
    def remove_file(self):
        # 从批量处理列表中移除选中的文件
        selected_items = self.listWidget_files.selectedItems()
        if selected_items:
            for item in selected_items:
                file_path = item.toolTip()
                if file_path in self.batch_files:
                    self.batch_files.remove(file_path)
                    # 如果有空白页信息，也一并移除
                    if file_path in self.blank_pages_dict:
                        del self.blank_pages_dict[file_path]
                row = self.listWidget_files.row(item)
                self.listWidget_files.takeItem(row)
            
            # 如果列表为空，禁用处理按钮
            if not self.batch_files:
                self.btn_process.setEnabled(False)
                self.clear_blank_pages_list()
            # 如果还有文件，选择第一个进行显示
            elif self.listWidget_files.count() > 0:
                self.listWidget_files.setCurrentRow(0)
                self.select_file(self.listWidget_files.item(0))
    
    def clear_files(self):
        # 清空批量处理列表
        self.batch_files = []
        self.blank_pages_dict = {}
        self.listWidget_files.clear()
        self.clear_blank_pages_list()
        self.btn_process.setEnabled(False)
    
    def select_file(self, item):
        # 当选择文件列表中的一个文件时
        if item:
            file_path = item.toolTip()
            self.input_file_path = file_path
            self.lineEdit_pdf_path.setText(file_path)
            self.detect_blank_pages(file_path)
    
    def clear_blank_pages_list(self):
        # 清空空白页列表
        self.listWidget_blank_pages.clear()
        self.btn_preview.setEnabled(False)
    
    def detect_blank_pages(self, file_path):
        # 检测文件中的空白页
        self.clear_blank_pages_list()
        
        # 如果已经检测过，直接显示结果
        if file_path in self.blank_pages_dict:
            self.display_blank_pages(file_path, self.blank_pages_dict[file_path])
            return
        
        # 否则启动检测线程
        self.startBusy()
        self.progressBar.setValue(0)
        
        self.worker = BlankPagesDetectThread(file_path)
        self.worker.progressSignal.connect(self.update_progress)
        self.worker.resultSignal.connect(self.detection_complete)
        self.worker.start()
    
    def display_blank_pages(self, file_path, blank_pages):
        # 显示空白页列表
        self.listWidget_blank_pages.clear()
        
        if blank_pages:
            for page_num in blank_pages:
                item = QListWidgetItem(f"第 {page_num + 1} 页")
                item.setData(Qt.UserRole, page_num)
                self.listWidget_blank_pages.addItem(item)
            self.btn_preview.setEnabled(True)
        else:
            self.listWidget_blank_pages.addItem("未检测到空白页")
            self.btn_preview.setEnabled(False)
    
    def detection_complete(self, result):
        # 空白页检测完成
        self.stopBusy()
        self.progressBar.setValue(100)
        
        file_path, blank_pages = result
        
        # 保存检测结果
        self.blank_pages_dict[file_path] = blank_pages
        
        # 显示检测结果
        self.display_blank_pages(file_path, blank_pages)
    
    def preview_blank_page(self):
        # 预览选中的空白页
        selected_items = self.listWidget_blank_pages.selectedItems()
        if not selected_items:
            # 如果没有选择任何项，则预览所有空白页
            self.preview_all_blank_pages()
            return
        
        # 获取当前选中的文件和页面
        file_path = self.input_file_path
        page_num = selected_items[0].data(Qt.UserRole)
        
        # 显示预览对话框
        preview_dialog = BlankPagePreviewDialog(file_path, page_num, self)
        preview_dialog.exec_()
    
    def preview_all_blank_pages(self):
        # 预览当前文件所有检测到的空白页
        file_path = self.input_file_path
        if not file_path or file_path not in self.blank_pages_dict:
            QMessageBox.information(self, "提示", "请先选择一个PDF文件并检测空白页")
            return
        
        blank_pages = self.blank_pages_dict[file_path]
        if not blank_pages:
            QMessageBox.information(self, "提示", "当前文件未检测到空白页")
            return
        
        # 显示所有空白页预览对话框
        preview_dialog = AllBlankPagesPreviewDialog(file_path, blank_pages, self)
        preview_dialog.exec_()
    
    def process_files(self):
        # 处理所有文件，删除空白页
        if not self.batch_files:
            QMessageBox.warning(self, "警告", "请先添加要处理的PDF文件")
            return
        
        # 检查是否有需要处理的文件（有空白页的文件）
        files_to_process = []
        for file_path in self.batch_files:
            # 如果还未检测，先检测空白页
            if file_path not in self.blank_pages_dict:
                QMessageBox.information(self, "提示", f"需要先检测 {os.path.basename(file_path)} 中的空白页")
                return
            
            # 有空白页的文件才需要处理
            if self.blank_pages_dict[file_path]:
                files_to_process.append(file_path)
        
        if not files_to_process:
            QMessageBox.information(self, "提示", "所有文件中都没有空白页，无需处理")
            return
        
        # 获取输出目录
        if self.comboBox_output_dir.currentText() == '自定义目录' and self.output_dir:
            output_directory = self.output_dir
        else:
            # 如果使用PDF相同目录，每个文件使用自己的目录
            output_directory = ""
        
        # 如果是自定义目录且不存在，创建它
        if output_directory and not os.path.exists(output_directory):
            try:
                os.makedirs(output_directory)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法创建输出目录: {str(e)}")
                return
        
        # 确认是否创建备份
        create_backup = self.checkBox_backup.isChecked()
        
        # 启动处理线程
        self.startBusy()
        self.progressBar.setValue(0)
        self.btn_process.setEnabled(False)
        
        self.worker = BlankPagesRemoveThread(
            files_to_process,
            self.blank_pages_dict,
            output_directory,
            self.output_suffix,
            create_backup
        )
        self.worker.progressSignal.connect(self.update_progress)
        self.worker.resultSignal.connect(self.process_complete)
        self.worker.start()
    
    def update_progress(self, value):
        self.progressBar.setValue(value)
    
    def process_complete(self, result):
        # 处理完成
        self.stopBusy()
        self.progressBar.setValue(100)
        self.btn_process.setEnabled(True)
        
        success, output_dir, processed_files = result
        
        if success:
            reply = QMessageBox(self)
            reply.setIcon(QMessageBox.Information)
            reply.setWindowTitle('完成')
            
            # 生成详细信息
            details = ""
            total_blank_pages = 0
            for file_path, blank_pages in processed_files.items():
                filename = os.path.basename(file_path)
                blank_count = len(blank_pages)
                total_blank_pages += blank_count
                details += f"{filename}: 删除了 {blank_count} 个空白页\n"
            
            reply.setText(f"空白页删除完成\n共处理 {len(processed_files)} 个文件，删除 {total_blank_pages} 个空白页")
            reply.setDetailedText(details)
            
            btn = reply.addButton('打开输出文件夹', QMessageBox.ActionRole)
            btn.clicked.connect(lambda: open_file_explorer(output_dir))
            reply.addButton("确认", QMessageBox.AcceptRole)
            reply.exec_()
        else:
            # output_dir 在这种情况下包含错误信息
            QMessageBox.critical(self, "错误", f"处理失败: {output_dir}")
    
    def closeEvent(self, event):
        super().closeEvent(event)
        self.okSignal.emit(True)


class BlankPagePreviewDialog(QDialog):
    def __init__(self, file_path, page_num, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.page_num = page_num
        self.is_thumbnail = True  # 默认显示缩略图
        self.setWindowTitle(f"空白页预览 - 第 {page_num + 1} 页")
        self.setMinimumSize(600, 800)
        
        layout = QVBoxLayout()
        
        # 添加预览图像
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.preview_label)
        
        # 添加查看模式切换按钮
        btn_layout = QHBoxLayout()
        self.btn_toggle_view = QPushButton("查看原始尺寸")
        self.btn_toggle_view.clicked.connect(self.toggle_view_mode)
        btn_layout.addWidget(self.btn_toggle_view)
        
        # 关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.accept)
        btn_layout.addWidget(close_button)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # 加载预览图像
        self.load_preview()
    
    def toggle_view_mode(self):
        self.is_thumbnail = not self.is_thumbnail
        if self.is_thumbnail:
            self.btn_toggle_view.setText("查看原始尺寸")
        else:
            self.btn_toggle_view.setText("查看缩略图")
        self.load_preview()
    
    def load_preview(self):
        try:
            # 打开PDF文件
            with fitz.open(self.file_path) as pdf:
                if 0 <= self.page_num < len(pdf):
                    # 获取页面
                    page = pdf[self.page_num]
                    
                    # 根据模式选择缩放比例
                    if self.is_thumbnail:
                        # 缩略图模式
                        scale_factor = 0.5
                    else:
                        # 原始尺寸模式
                        scale_factor = 2.0
                    
                    # 生成图像
                    pix = page.get_pixmap(matrix=fitz.Matrix(scale_factor, scale_factor))
                    
                    # 转换为QPixmap
                    img_data = pix.samples
                    
                    # 使用PIL转换
                    image = Image.frombytes("RGB", [pix.width, pix.height], img_data)
                    img_data = image.tobytes("raw", "RGB")
                    
                    qimg = QImage(img_data, pix.width, pix.height, QImage.Format_RGB888)
                    qpixmap = QPixmap.fromImage(qimg)
                    
                    # 如果是缩略图模式，调整图像大小以适应窗口
                    if self.is_thumbnail:
                        qpixmap = qpixmap.scaled(self.width() - 40, self.height() - 80, 
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    
                    # 显示图像
                    self.preview_label.setPixmap(qpixmap)
                    
                    # 如果是原始尺寸模式，可能需要调整窗口大小
                    if not self.is_thumbnail:
                        # 确保窗口足够大以显示原始尺寸图像
                        self.resize(max(600, pix.width + 80), max(800, pix.height + 120))
        except Exception as e:
            logger.error(f"加载预览时出错: {str(e)}")
            self.preview_label.setText(f"无法加载预览: {str(e)}")


class BlankPagesDetectThread(QThread):
    progressSignal = Signal(int)
    resultSignal = Signal(tuple)  # (file_path, blank_pages)
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        try:
            blank_pages = []
            
            # 打开PDF文件
            with fitz.open(self.file_path) as pdf:
                total_pages = len(pdf)
                
                # 遍历所有页面
                for page_num in range(total_pages):
                    # 更新进度
                    progress = int((page_num + 1) / total_pages * 90)
                    self.progressSignal.emit(progress)
                    
                    # 检查是否为空白页
                    is_blank = self.is_blank_page(pdf, page_num)
                    if is_blank:
                        blank_pages.append(page_num)
            
            # 发送结果信号
            self.resultSignal.emit((self.file_path, blank_pages))
            
        except Exception as e:
            logger.error(f"检测空白页出错: {str(e)}")
            self.resultSignal.emit((self.file_path, []))
    
    def is_blank_page(self, pdf, page_num):
        """检查页面是否为空白页"""
        try:
            # 获取页面
            page = pdf[page_num]
            
            # 获取页面文本
            text = page.get_text().strip()
            if text:
                return False  # 有文本，不是空白页
            
            # 渲染页面为图像
            pix = page.get_pixmap()
            
            # 计算非白色像素的比例
            img_data = pix.samples
            arr = np.frombuffer(img_data, dtype=np.uint8)
            
            # 重塑为(height, width, 3)形状的数组 (RGB图像)
            img_array = arr.reshape(pix.height, pix.width, 3 if pix.n == 3 else 4)
            
            # 计算非白色像素的数量
            # 我们将白色定义为RGB值都大于240的像素
            non_white_pixels = np.sum(np.any(img_array < 240, axis=2))
            total_pixels = pix.width * pix.height
            
            # 计算非白色像素的比例
            non_white_ratio = non_white_pixels / total_pixels
            
            # 如果非白色像素比例小于阈值，认为是空白页
            # 这里我们使用一个很小的阈值，例如0.5%
            return non_white_ratio < 0.005
            
        except Exception as e:
            logger.error(f"判断空白页出错: {str(e)}")
            return False


class BlankPagesRemoveThread(QThread):
    progressSignal = Signal(int)
    resultSignal = Signal(tuple)  # (success, output_dir, processed_files)
    
    def __init__(self, files, blank_pages_dict, output_dir, output_suffix, create_backup):
        super().__init__()
        self.files = files
        self.blank_pages_dict = blank_pages_dict
        self.output_dir = output_dir
        self.output_suffix = output_suffix
        self.create_backup = create_backup
    
    def run(self):
        try:
            processed_files = {}
            total_files = len(self.files)
            
            for i, file_path in enumerate(self.files):
                # 更新进度
                progress = int((i / total_files) * 90)
                self.progressSignal.emit(progress)
                
                # 获取要删除的空白页
                blank_pages = self.blank_pages_dict.get(file_path, [])
                
                if not blank_pages:
                    # 没有空白页，跳过处理
                    continue
                
                # 处理单个文件
                success = self.process_single_file(file_path, blank_pages)
                
                if success:
                    processed_files[file_path] = blank_pages
            
            # 检查是否处理成功
            if processed_files:
                # 使用第一个文件的目录作为输出目录（如果未指定）
                output_dir = self.output_dir
                if not output_dir and self.files:
                    output_dir = os.path.dirname(self.files[0])
                
                self.progressSignal.emit(100)
                self.resultSignal.emit((True, output_dir, processed_files))
            else:
                self.resultSignal.emit((False, "没有文件被处理", {}))
                
        except Exception as e:
            logger.error(f"删除空白页出错: {str(e)}")
            self.resultSignal.emit((False, str(e), {}))
    
    def process_single_file(self, file_path, blank_pages):
        """处理单个文件的空白页删除"""
        try:
            # 获取输出文件路径
            file_dir = os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            name, ext = os.path.splitext(file_name)
            
            # 确定输出目录
            output_dir = self.output_dir if self.output_dir else file_dir
            
            # 生成输出文件名
            output_file = os.path.join(output_dir, f"{name}{self.output_suffix}{ext}")
            
            # 确保输出文件路径可用
            output_file = common.usable_filepath(output_file)
            
            # 如果创建备份且源文件和目标文件不同
            if self.create_backup and file_path != output_file:
                backup_file = os.path.join(output_dir, f"{name}_备份{ext}")
                backup_file = common.usable_filepath(backup_file)
                shutil.copy2(file_path, backup_file)
            
            # 打开源文件
            with fitz.open(file_path) as src_pdf:
                # 创建新PDF
                dst_pdf = fitz.open()
                
                # 获取所有页面，排除空白页
                for page_num in range(len(src_pdf)):
                    if page_num not in blank_pages:
                        # 复制非空白页
                        dst_pdf.insert_pdf(src_pdf, from_page=page_num, to_page=page_num)
                
                # 保存新PDF
                dst_pdf.save(output_file)
                dst_pdf.close()
            
            return True
            
        except Exception as e:
            logger.error(f"处理文件 {file_path} 出错: {str(e)}")
            return False


class AllBlankPagesPreviewDialog(QDialog):
    def __init__(self, file_path, blank_pages, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.blank_pages = blank_pages
        self.current_index = 0
        self.is_thumbnail = True  # 默认显示缩略图
        self.setWindowTitle(f"空白页预览 - 全部 ({len(blank_pages)} 页)")
        self.setMinimumSize(700, 800)
        
        layout = QVBoxLayout()
        
        # 预览标题
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.title_label.setFont(font)
        layout.addWidget(self.title_label)
        
        # 预览图像
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.preview_label)
        
        # 导航按钮
        nav_layout = QHBoxLayout()
        
        self.btn_prev = QPushButton("上一页")
        self.btn_prev.clicked.connect(self.show_prev_page)
        nav_layout.addWidget(self.btn_prev)
        
        self.page_label = QLabel()
        self.page_label.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(self.page_label)
        
        self.btn_next = QPushButton("下一页")
        self.btn_next.clicked.connect(self.show_next_page)
        nav_layout.addWidget(self.btn_next)
        
        layout.addLayout(nav_layout)
        
        # 切换视图模式和关闭按钮
        btn_layout = QHBoxLayout()
        
        self.btn_toggle_view = QPushButton("查看原始尺寸")
        self.btn_toggle_view.clicked.connect(self.toggle_view_mode)
        btn_layout.addWidget(self.btn_toggle_view)
        
        # 关闭按钮
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.accept)
        btn_layout.addWidget(close_button)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # 加载第一页
        self.update_page()
    
    def toggle_view_mode(self):
        self.is_thumbnail = not self.is_thumbnail
        if self.is_thumbnail:
            self.btn_toggle_view.setText("查看原始尺寸")
        else:
            self.btn_toggle_view.setText("查看缩略图")
        self.update_page()
    
    def update_page(self):
        if not self.blank_pages:
            return
        
        page_num = self.blank_pages[self.current_index]
        self.title_label.setText(f"第 {page_num + 1} 页 (空白页 {self.current_index + 1}/{len(self.blank_pages)})")
        self.page_label.setText(f"{self.current_index + 1} / {len(self.blank_pages)}")
        
        # 更新导航按钮状态
        self.btn_prev.setEnabled(self.current_index > 0)
        self.btn_next.setEnabled(self.current_index < len(self.blank_pages) - 1)
        
        # 加载预览图像
        self.load_preview(page_num)
    
    def show_prev_page(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_page()
    
    def show_next_page(self):
        if self.current_index < len(self.blank_pages) - 1:
            self.current_index += 1
            self.update_page()
    
    def load_preview(self, page_num):
        try:
            # 打开PDF文件
            with fitz.open(self.file_path) as pdf:
                if 0 <= page_num < len(pdf):
                    # 获取页面
                    page = pdf[page_num]
                    
                    # 根据模式选择缩放比例
                    if self.is_thumbnail:
                        # 缩略图模式
                        scale_factor = 0.5
                    else:
                        # 原始尺寸模式
                        scale_factor = 2.0
                    
                    # 生成图像
                    pix = page.get_pixmap(matrix=fitz.Matrix(scale_factor, scale_factor))
                    
                    # 转换为QPixmap
                    img_data = pix.samples
                    
                    # 使用PIL转换
                    image = Image.frombytes("RGB", [pix.width, pix.height], img_data)
                    img_data = image.tobytes("raw", "RGB")
                    
                    qimg = QImage(img_data, pix.width, pix.height, QImage.Format_RGB888)
                    qpixmap = QPixmap.fromImage(qimg)
                    
                    # 如果是缩略图模式，调整图像大小以适应窗口
                    if self.is_thumbnail:
                        qpixmap = qpixmap.scaled(self.width() - 40, self.height() - 120, 
                                          Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    
                    # 显示图像
                    self.preview_label.setPixmap(qpixmap)
                    
                    # 如果是原始尺寸模式，可能需要调整窗口大小
                    if not self.is_thumbnail:
                        # 确保窗口足够大以显示原始尺寸图像
                        self.resize(max(700, pix.width + 80), max(800, pix.height + 160))
        except Exception as e:
            logger.error(f"加载预览时出错: {str(e)}")
            self.preview_label.setText(f"无法加载预览: {str(e)}")


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys
    from PySide6.QtGui import QFont
    
    app = QApplication(sys.argv)
    font = QFont('微软雅黑', 10)
    app.setFont(font)
    router = Router(None)
    view = BlankPagesControl(router)
    view.show()
    sys.exit(app.exec()) 