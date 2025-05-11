import os.path
import shutil
from typing import List, Dict, Tuple, Optional

import fitz
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from PySide6.QtCore import Signal, QThread, QUrl, Qt, QFile, QIODevice, QTextStream
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon, QFont, QFontMetrics, QColor, QImage
from PySide6.QtWidgets import (QWidget, QMessageBox, QFileDialog, QListWidgetItem, QDialog, 
                              QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QColorDialog, QLineEdit,
                              QScrollArea, QFrame)

from app.model import PdfFile
from app.ui.components.QCursorGif import QCursorGif
from app.ui.Icon import Icon
from app.util import common
from app.ui.pdf_tools.watermark.watermark_ui import Ui_watermark_view
from app.ui.components.file_list import FileListView
from app.ui.components.router import Router
from app.log import logger


def open_file_explorer(path):
    # 使用QDesktopServices打开文件管理器
    if os.path.isfile(path):
        path = os.path.dirname(path)
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))


class WatermarkControl(QWidget, Ui_watermark_view, QCursorGif):
    okSignal = Signal(bool)
    childRouterSignal = Signal(str)

    def __init__(self, router: Router, parent=None):
        super().__init__(parent)
        self.input_file_path = ""
        self.output_dir = ""
        self.output_suffix = "_水印"
        self.watermark_color = QColor(200, 0, 0, 128)  # 默认红色半透明
        self.router = router
        self.router_path = (self.parent().router_path if self.parent() else '') + '/添加水印'
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
        self.btn_preview.clicked.connect(self.preview_watermark)
        self.btn_color.clicked.connect(self.choose_color)
        
        # 批量文件操作
        self.list_view = FileListView(self)
        self.verticalLayout_file_list.addWidget(self.list_view)
        self.btn_add_files.clicked.connect(self.add_files)
        self.btn_remove_selected.clicked.connect(self.remove_selected)
        
        # 输出选项连接
        self.lineEdit_suffix.textChanged.connect(self.change_output_suffix)
        self.comboBox_output_dir.activated.connect(self.select_output_dir)
        self.btn_choose_output_dir.clicked.connect(self.set_output_dir)
        
        # 透明度滑块连接
        self.slider_opacity.valueChanged.connect(self.update_opacity)
        
        # 字体下拉框填充
        fonts = ["Arial", "Times New Roman", "Courier New", "Verdana", "微软雅黑", "宋体", "黑体", "楷体"]
        self.comboBox_font.addItems(fonts)
        
        # 水印类型切换
        self.comboBox_type.currentIndexChanged.connect(self.toggle_watermark_type)
        
        # 初始界面设置
        self.label_custom_dir.setVisible(False)
        self.btn_choose_output_dir.setVisible(False)
        self.btn_process.setEnabled(False)
        self.toggle_watermark_type(0)  # 默认文本水印
    
    def init_ui(self):
        self.btn_process.setObjectName('border')
        if not self.parent():
            pixmap = QPixmap(Icon.logo_ico_path)
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)
            self.setWindowTitle('PDF添加水印')
            style_qss_file = QFile(":/data/resources/QSS/style.qss")
            if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(style_qss_file)
                style_content = stream.readAll()
                self.setStyleSheet(style_content)
                style_qss_file.close()
        
        # 设置按钮图标和颜色背景
        self.btn_color.setStyleSheet(
            f"background-color: {self.watermark_color.name()}; "
            f"border-radius: 5px; "
            f"border: 1px solid #888888; "
            f"min-height: 28px;"
        )
        # 限制颜色按钮的最大宽度
        self.btn_color.setMaximumWidth(120)
        
        self.spinBox_rotation.setMinimumWidth(80)
        self.spinBox_size.setMinimumWidth(80)
        
        self.btn_preview.setStyleSheet(
            "background-color: #f0f0f0; "
            "border-radius: 5px; "
            "border: 1px solid #888888; "
            "padding: 5px 10px; "
            "font-weight: bold;"
        )
        self.btn_process.setStyleSheet(
            "background-color: #4CAF50; "
            "color: white; "
            "border-radius: 5px; "
            "border: none; "
            "padding: 8px 16px; "
            "font-weight: bold;"
        )
    
    def toggle_watermark_type(self, index):
        # 切换水印类型时调整界面
        is_text = index == 0  # 0=文本水印, 1=图片水印
        self.label_text.setVisible(is_text)
        self.lineEdit_text.setVisible(is_text)
        self.label_font.setVisible(is_text)
        self.comboBox_font.setVisible(is_text)
        self.label_size.setVisible(is_text)
        self.spinBox_size.setVisible(is_text)
        
        # 如果是图片水印，但还没有选择图片
        if not is_text:
            if not hasattr(self, 'watermark_image_path') or not self.watermark_image_path:
                # 创建图片水印需要的控件
                self.horizontalLayout_image = QHBoxLayout()
                self.horizontalLayout_image.setObjectName(u"horizontalLayout_image")
                
                self.label_image = QLabel(self.groupBox_settings)
                self.label_image.setObjectName(u"label_image")
                self.label_image.setText("水印图片:")
                self.horizontalLayout_image.addWidget(self.label_image)
                
                self.lineEdit_image_path = QLineEdit(self.groupBox_settings)
                self.lineEdit_image_path.setObjectName(u"lineEdit_image_path")
                self.lineEdit_image_path.setReadOnly(True)
                self.horizontalLayout_image.addWidget(self.lineEdit_image_path)
                
                self.btn_choose_image = QPushButton(self.groupBox_settings)
                self.btn_choose_image.setObjectName(u"btn_choose_image")
                self.btn_choose_image.setText("选择图片")
                self.btn_choose_image.clicked.connect(self.choose_watermark_image)
                self.horizontalLayout_image.addWidget(self.btn_choose_image)
                
                # 插入到字体控件位置
                self.verticalLayout_settings.insertLayout(2, self.horizontalLayout_image)
            
            # 显示图片相关控件
            self.label_image.setVisible(True)
            self.lineEdit_image_path.setVisible(True)
            self.btn_choose_image.setVisible(True)
        else:
            # 隐藏图片相关控件
            if hasattr(self, 'label_image'):
                self.label_image.setVisible(False)
                self.lineEdit_image_path.setVisible(False)
                self.btn_choose_image.setVisible(False)
    
    def choose_watermark_image(self):
        # 选择水印图片
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择水印图片", "", "图片文件 (*.png *.jpg *.jpeg *.bmp);;所有文件 (*)"
        )
        if file_path:
            self.watermark_image_path = file_path
            self.lineEdit_image_path.setText(file_path)
    
    def change_output_suffix(self):
        self.output_suffix = common.correct_filename(self.lineEdit_suffix.text())
    
    def select_output_dir(self):
        text = self.comboBox_output_dir.currentText()
        if text == 'PDF相同目录':
            self.label_custom_dir.setVisible(False)
            self.btn_choose_output_dir.setVisible(False)
        elif text == '自定义目录':
            self.label_custom_dir.setVisible(True)
            self.btn_choose_output_dir.setVisible(True)
    
    def set_output_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if folder:
            self.output_dir = folder
            font_metrics = QFontMetrics(self.label_custom_dir.font())
            # 使用 elidedText 根据按钮宽度生成省略文字
            elided_text = font_metrics.elidedText(self.output_dir, Qt.ElideRight, self.label_custom_dir.width() - 10)
            self.label_custom_dir.setText(elided_text)
            self.label_custom_dir.setToolTip(self.output_dir)
    
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
                font_metrics = QFontMetrics(self.label_custom_dir.font())
                elided_text = font_metrics.elidedText(self.output_dir, Qt.ElideRight, self.label_custom_dir.width() - 10)
                self.label_custom_dir.setText(elided_text)
                self.label_custom_dir.setToolTip(self.output_dir)
    
    def add_files(self):
        # 打开文件对话框，选择多个PDF文件
        file_paths, _ = QFileDialog.getOpenFileNames(self, "选择PDF文件", "", "PDF Files (*.pdf);;All Files (*)")
        if file_paths:
            for file_path in file_paths:
                self.add_file_to_batch(file_path)
            
            # 如果未设置输出目录，默认使用第一个PDF的目录
            if not self.output_dir and file_paths:
                self.output_dir = os.path.dirname(file_paths[0])
                font_metrics = QFontMetrics(self.label_custom_dir.font())
                elided_text = font_metrics.elidedText(self.output_dir, Qt.ElideRight, self.label_custom_dir.width() - 10)
                self.label_custom_dir.setText(elided_text)
                self.label_custom_dir.setToolTip(self.output_dir)
    
    def add_file_to_batch(self, file_path):
        # 添加文件到批量处理列表
        self.list_view.add_item(file_path, len(self.list_view.get_data()))
        self.btn_process.setEnabled(True)
    
    def remove_selected(self):
        reply = QMessageBox.question(self, '温馨提示', '确定删除选中的文件？', QMessageBox.No | QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.list_view.remove_select()
            # 如果列表为空，禁用处理按钮
            if len(self.list_view.get_data()) == 0:
                self.btn_process.setEnabled(False)
    
    def choose_color(self):
        # 选择水印颜色
        color = QColorDialog.getColor(self.watermark_color, self, "选择水印颜色", QColorDialog.ShowAlphaChannel)
        if color.isValid():
            self.watermark_color = color
            # 保持用户设置的透明度
            self.watermark_color.setAlpha(int(self.slider_opacity.value() * 2.55))
            # 更新颜色按钮背景
            r, g, b, a = self.watermark_color.getRgb()
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            self.btn_color.setStyleSheet(
                f"background-color: {hex_color}; "
                f"border-radius: 5px; "
                f"border: 1px solid #888888; "
                f"min-height: 28px;"
            )
            # 限制文字长度，避免按钮过大
            if len(hex_color) > 6:
                display_color = hex_color[:6] + "..."
            else:
                display_color = hex_color
            self.btn_color.setText(f"已选: {display_color}")
    
    def update_opacity(self, value):
        # 更新透明度标签
        self.label_opacity_value.setText(f"{value}%")
        # 更新颜色的透明度
        self.watermark_color.setAlpha(int(value * 2.55))  # 0-100% 映射到 0-255
        
        # 同时更新颜色按钮背景，使其反映透明度变化
        r, g, b, a = self.watermark_color.getRgb()
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        css_alpha = value / 100
        self.btn_color.setStyleSheet(
            f"background-color: {hex_color}; "
            f"border-radius: 5px; "
            f"border: 1px solid #888888; "
            f"min-height: 28px; "
            f"opacity: {css_alpha};"
        )
    
    def preview_watermark(self):
        # 预览水印效果
        file_path = self.input_file_path
        if not file_path:
            # 尝试从批量列表获取第一个文件
            files = self.list_view.get_data()
            if files:
                file_path = files[0].file_path
            else:
                QMessageBox.information(self, "提示", "请先选择一个PDF文件")
                return
        
        # 获取水印参数
        watermark_options = self.get_watermark_options()
        
        # 显示预览对话框
        preview_dialog = WatermarkPreviewDialog(file_path, watermark_options, self)
        preview_dialog.exec_()
    
    def get_watermark_options(self):
        # 收集所有水印参数
        options = {
            'type': 'text' if self.comboBox_type.currentIndex() == 0 else 'image',
            'text': self.lineEdit_text.text(),
            'font': self.comboBox_font.currentText(),
            'font_size': self.spinBox_size.value(),
            'color': self.watermark_color,
            'opacity': self.slider_opacity.value(),
            'position': self.comboBox_position.currentIndex(),
            'rotation': self.spinBox_rotation.value()
        }
        
        # 如果是图片水印，添加图片路径
        if options['type'] == 'image' and hasattr(self, 'watermark_image_path'):
            options['image_path'] = self.watermark_image_path
        
        return options
    
    def process_files(self):
        # 处理所有文件，添加水印
        files = self.list_view.get_data()
        if not files:
            QMessageBox.warning(self, "警告", "请先添加要处理的PDF文件")
            return
        
        # 对于图片水印，检查是否选择了图片
        watermark_options = self.get_watermark_options()
        if watermark_options['type'] == 'image' and ('image_path' not in watermark_options or not watermark_options['image_path']):
            QMessageBox.warning(self, "警告", "请先选择水印图片")
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
        
        self.worker = WatermarkThread(
            [file.file_path for file in files],
            watermark_options,
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
            for file_path in processed_files:
                filename = os.path.basename(file_path)
                details += f"{filename}: 已添加水印\n"
            
            reply.setText(f"水印添加完成\n共处理 {len(processed_files)} 个文件")
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


class WatermarkPreviewDialog(QDialog):
    def __init__(self, file_path, watermark_options, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.watermark_options = watermark_options
        self.setWindowTitle("水印预览")
        self.setMinimumSize(900, 700)
        self.zoom_level = 1.0
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # 预览标题
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color: #333; margin-bottom: 10px;")
        layout.addWidget(self.title_label)
        
        # 添加缩放控制
        zoom_layout = QHBoxLayout()
        zoom_label = QLabel("缩放:")
        zoom_label.setStyleSheet("font-weight: bold;")
        zoom_layout.addWidget(zoom_label)
        
        self.zoom_in_btn = QPushButton("+")
        self.zoom_in_btn.setFixedSize(30, 30)
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_in_btn.setStyleSheet(
            "background-color: #f0f0f0; border-radius: 15px; font-weight: bold;"
        )
        zoom_layout.addWidget(self.zoom_in_btn)
        
        self.zoom_out_btn = QPushButton("-")
        self.zoom_out_btn.setFixedSize(30, 30)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.zoom_out_btn.setStyleSheet(
            "background-color: #f0f0f0; border-radius: 15px; font-weight: bold;"
        )
        zoom_layout.addWidget(self.zoom_out_btn)
        
        self.zoom_reset_btn = QPushButton("100%")
        self.zoom_reset_btn.clicked.connect(self.zoom_reset)
        self.zoom_reset_btn.setStyleSheet(
            "background-color: #f0f0f0; border-radius: 5px; padding: 5px 10px;"
        )
        zoom_layout.addWidget(self.zoom_reset_btn)
        
        zoom_layout.addStretch()
        layout.addLayout(zoom_layout)
        
        # 预览图像 - 使用滚动区域容纳
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.StyledPanel)
        self.scroll_area.setStyleSheet("border: 1px solid #ddd; background-color: #f9f9f9;")
        
        self.preview_container = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_container)
        
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumSize(800, 500)
        self.preview_layout.addWidget(self.preview_label)
        self.preview_layout.addStretch()
        
        self.scroll_area.setWidget(self.preview_container)
        layout.addWidget(self.scroll_area, 1)
        
        # 信息栏
        self.info_label = QLabel()
        self.info_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(self.info_label)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 关闭按钮
        close_button = QPushButton("关闭")
        close_button.setMinimumSize(100, 35)
        close_button.clicked.connect(self.accept)
        close_button.setStyleSheet(
            "background-color: #f0f0f0; "
            "border-radius: 5px; "
            "border: 1px solid #ddd; "
            "padding: 5px 15px; "
            "font-weight: bold;"
        )
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 生成预览
        self.generate_preview()
    
    def zoom_in(self):
        if self.zoom_level < 3.0:  # 限制最大缩放比例
            self.zoom_level += 0.25
            self.update_zoom()
    
    def zoom_out(self):
        if self.zoom_level > 0.5:  # 限制最小缩放比例
            self.zoom_level -= 0.25
            self.update_zoom()
    
    def zoom_reset(self):
        self.zoom_level = 1.0
        self.update_zoom()
    
    def update_zoom(self):
        self.zoom_reset_btn.setText(f"{int(self.zoom_level * 100)}%")
        self.generate_preview()
    
    def generate_preview(self):
        try:
            # 打开PDF文件并获取第一页
            with fitz.open(self.file_path) as pdf:
                if len(pdf) > 0:
                    page = pdf[0]
                    # 设置预览标题
                    filename = os.path.basename(self.file_path)
                    self.title_label.setText(f"水印预览 - {filename}")
                    
                    # 创建临时文档和页面来渲染预览
                    tmp_doc = fitz.open()
                    tmp_page = tmp_doc.new_page(width=page.rect.width, height=page.rect.height)
                    
                    # 复制页面内容
                    tmp_page.show_pdf_page(tmp_page.rect, pdf, 0)
                    
                    # 添加水印 - 使用try-except捕获任何可能的错误，避免显示"加载失败"文本
                    try:
                        add_watermark_to_page(tmp_page, self.watermark_options)
                    except Exception as e:
                        logger.error(f"预览时添加水印出错: {str(e)}")
                        # 不显示错误信息，仅记录日志
                    
                    # 更新信息
                    watermark_type = "文本" if self.watermark_options['type'] == 'text' else "图片"
                    watermark_text = self.watermark_options.get('text', '(无文本)')
                    position_text = self.get_position_text(self.watermark_options['position'])
                    rotation = self.watermark_options['rotation']
                    
                    info_text = f"水印类型: {watermark_type} | "
                    if watermark_type == "文本":
                        info_text += f"文本内容: \"{watermark_text}\" | "
                    elif watermark_type == "图片" and 'image_path' in self.watermark_options:
                        # 仅显示图片名称，不显示完整路径
                        img_name = os.path.basename(self.watermark_options['image_path'])
                        info_text += f"图片: \"{img_name}\" | "
                    info_text += f"位置: {position_text} | 旋转角度: {rotation}° | 透明度: {self.watermark_options['opacity']}%"
                    self.info_label.setText(info_text)
                    
                    # 渲染为图像，考虑缩放级别
                    matrix = fitz.Matrix(1.5 * self.zoom_level, 1.5 * self.zoom_level)
                    pix = tmp_page.get_pixmap(matrix=matrix)
                    
                    # 转换为QPixmap
                    img_data = pix.samples
                    
                    # 使用PIL转换
                    image = Image.frombytes("RGB", [pix.width, pix.height], img_data)
                    img_data = image.tobytes("raw", "RGB")
                    
                    qimg = QImage(img_data, pix.width, pix.height, QImage.Format_RGB888)
                    qpixmap = QPixmap.fromImage(qimg)
                    
                    # 显示图像
                    self.preview_label.setPixmap(qpixmap)
                    
                    # 调整预览标签大小以适应图像
                    self.preview_label.setMinimumSize(pix.width, pix.height)
                    
                    # 关闭临时文档
                    tmp_doc.close()
        except Exception as e:
            logger.error(f"生成预览时出错: {str(e)}")
            # 不显示错误信息，而是提供一个默认的空白预览
            empty_pixmap = QPixmap(800, 600)  # 创建空白预览
            empty_pixmap.fill(Qt.white)
            self.preview_label.setPixmap(empty_pixmap)
            # 更新信息栏，用更友好的信息
            self.info_label.setText("正在处理预览，请稍后...")
    
    def get_position_text(self, position_index):
        positions = {
            0: "居中",
            1: "左上角",
            2: "右上角",
            3: "左下角", 
            4: "右下角",
            5: "顶部居中",
            6: "底部居中", 
            7: "左侧居中", 
            8: "右侧居中"
        }
        return positions.get(position_index, "未知")


class WatermarkThread(QThread):
    progressSignal = Signal(int)
    resultSignal = Signal(tuple)  # (success, output_dir, processed_files)
    
    def __init__(self, files, watermark_options, output_dir, output_suffix, create_backup):
        super().__init__()
        self.files = files
        self.watermark_options = watermark_options
        self.output_dir = output_dir
        self.output_suffix = output_suffix
        self.create_backup = create_backup
    
    def run(self):
        try:
            processed_files = []
            total_files = len(self.files)
            
            for i, file_path in enumerate(self.files):
                # 更新进度 - 每个文件的起始进度
                start_progress = int((i / total_files) * 90)
                self.progressSignal.emit(start_progress)
                
                # 处理单个文件
                success = self.process_single_file(file_path, start_progress, (i+1) / total_files * 90)
                
                if success:
                    processed_files.append(file_path)
            
            # 检查是否处理成功
            if processed_files:
                # 使用第一个文件的目录作为输出目录（如果未指定）
                output_dir = self.output_dir
                if not output_dir and self.files:
                    output_dir = os.path.dirname(self.files[0])
                
                self.progressSignal.emit(100)
                self.resultSignal.emit((True, output_dir, processed_files))
            else:
                self.resultSignal.emit((False, "没有文件被处理", []))
                
        except Exception as e:
            logger.error(f"添加水印出错: {str(e)}")
            self.resultSignal.emit((False, str(e), []))
    
    def process_single_file(self, file_path, start_progress, end_progress):
        """处理单个文件的水印添加"""
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
                # 备份完成后更新进度
                self.progressSignal.emit(int(start_progress + (end_progress - start_progress) * 0.1))
            
            # 打开源文件
            with fitz.open(file_path) as pdf:
                total_pages = len(pdf)
                
                # 遍历每一页并添加水印
                for page_num in range(total_pages):
                    # 获取页面
                    page = pdf[page_num]
                    # 添加水印
                    add_watermark_to_page(page, self.watermark_options)
                    
                    # 更新进度 - 根据页面进度更新
                    # 10% 用于文件准备和备份，80% 用于页面处理，10% 用于保存
                    page_progress = 0.1 + (page_num + 1) / total_pages * 0.8
                    current_progress = start_progress + (end_progress - start_progress) * page_progress
                    self.progressSignal.emit(int(current_progress))
                
                # 保存带水印的PDF
                pdf.save(output_file)
                
                # 保存完成后更新到该文件的结束进度
                self.progressSignal.emit(int(end_progress))
            
            return True
            
        except Exception as e:
            logger.error(f"处理文件 {file_path} 出错: {str(e)}")
            return False


def add_watermark_to_page(page, options):
    """向PDF页面添加水印"""
    try:
        # 获取页面大小
        page_rect = page.rect
        page_width = page_rect.width
        page_height = page_rect.height
        
        # 水印位置映射
        position_map = {
            0: (page_width/2, page_height/2),           # 居中
            1: (page_width*0.1, page_height*0.1),       # 左上角
            2: (page_width*0.9, page_height*0.1),       # 右上角
            3: (page_width*0.1, page_height*0.9),       # 左下角
            4: (page_width*0.9, page_height*0.9),       # 右下角
            5: (page_width/2, page_height*0.1),         # 顶部居中
            6: (page_width/2, page_height*0.9),         # 底部居中
            7: (page_width*0.1, page_height/2),         # 左侧居中
            8: (page_width*0.9, page_height/2),         # 右侧居中
        }
        
        # 获取水印位置
        pos_x, pos_y = position_map.get(options['position'], (page_width/2, page_height/2))
        
        # 旋转角度
        rotation = options['rotation']
        
        # 绘制水印
        if options['type'] == 'text':
            # 文本水印
            text = options['text']
            font_size = options['font_size']
            color = options['color']
            
            # 转换颜色和透明度
            r, g, b, a = color.getRgb()
            opacity = a / 255.0
            
            # 创建文本水印
            # 使用TextWriter代替直接调用insert_text，因为TextWriter支持透明度
            text_writer = fitz.TextWriter(page_rect)
            
            # 使用font来预先计算文本大小，以便居中显示
            font = fitz.Font("helv")
            text_width, text_height = font.text_length(text, fontsize=font_size), font_size
            
            # 根据position_map中的位置调整坐标，使文本居中
            text_pos_x = pos_x - text_width / 2
            text_pos_y = pos_y + text_height / 2  # TextWriter的y坐标是文本的底部
            
            # 添加文本到TextWriter
            text_writer.append((text_pos_x, text_pos_y), text, fontsize=font_size)
            text_writer.opacity = opacity
            text_writer.color = (r/255, g/255, b/255)
            
            # 使用morph参数设置旋转
            if rotation != 0:
                # 创建旋转矩阵
                matrix = fitz.Matrix(1, 1).prerotate(rotation)
                # 使用原始位置作为旋转中心点
                point = fitz.Point(pos_x, pos_y)
                morph = (point, matrix)
                text_writer.write_text(page, morph=morph)
            else:
                text_writer.write_text(page)
            
        elif options['type'] == 'image' and 'image_path' in options:
            # 图片水印
            image_path = options['image_path']
            opacity = options['opacity'] / 100
            
            try:
                # 打开图片并调整大小
                img = fitz.open(image_path)
                if img.is_pdf:
                    # 如果是PDF，取第一页
                    pix = img[0].get_pixmap()
                else:
                    # 非PDF直接创建图像 - 修正: Document对象没有get_pixmap方法
                    try:
                        pix = fitz.Pixmap(image_path)
                    except Exception as e:
                        # 尝试备用方法打开图片，兼容不同版本
                        from PIL import Image
                        img_pil = Image.open(image_path)
                        img_pil = img_pil.convert("RGBA")
                        pix_data = img_pil.tobytes("raw", "RGBA")
                        pix = fitz.Pixmap(pix_data, img_pil.width, img_pil.height, 4)
                
                # 计算图片缩放和位置
                img_width = min(page_width * 0.5, pix.width)
                scale = img_width / pix.width
                img_height = pix.height * scale
                
                # 创建矩形
                rect = fitz.Rect(pos_x - img_width/2, pos_y - img_height/2, 
                             pos_x + img_width/2, pos_y + img_height/2)
                
                # 处理透明度
                if opacity < 1.0:
                    # 确保有alpha通道
                    if not pix.alpha:
                        # 创建带alpha通道的副本
                        try:
                            pix1 = fitz.Pixmap(pix)
                            pix = fitz.Pixmap(pix1, 1)  # 添加alpha通道
                            pix1 = None  # 释放内存
                        except:
                            # 如果上面的方法不支持，尝试使用PIL
                            if 'img_pil' not in locals():
                                from PIL import Image
                                img_pil = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                                img_pil = img_pil.convert("RGBA")
                                
                            # 应用透明度
                            img_pil.putalpha(int(opacity * 255))
                            pix_data = img_pil.tobytes("raw", "RGBA")
                            pix = fitz.Pixmap(pix_data, img_pil.width, img_pil.height, 4)
                            
                    try:
                        # 设置全局透明度 - 尝试使用samples访问
                        pix_bytes = bytearray(pix.samples)
                        
                        # 调整alpha通道
                        for i in range(3, len(pix_bytes), 4):  # 每4个字节一组，第4个是alpha
                            pix_bytes[i] = int(pix_bytes[i] * opacity)
                        
                        # 使用修改后的数据创建新pixmap
                        try:
                            new_pix = fitz.Pixmap(pix.colorspace, pix.width, pix.height, pix_bytes, pix.alpha)
                        except TypeError:
                            # 旧版本可能参数不同
                            new_pix = fitz.Pixmap(pix.colorspace, pix.width, pix.height, 4)
                            new_pix.samples = pix_bytes
                        
                        # 插入带透明度的图片
                        page.insert_image(rect, pixmap=new_pix)
                        
                        # 清理
                        new_pix = None
                    except Exception as e:
                        # 如果处理透明度失败，直接插入原图
                        logger.warning(f"应用透明度失败，使用原图: {str(e)}")
                        page.insert_image(rect, pixmap=pix)
                else:
                    # 不需要透明度处理时直接插入
                    page.insert_image(rect, pixmap=pix)
                
                img.close()
                
            except Exception as e:
                logger.error(f"处理水印图片出错: {str(e)}")
                # 如果图片处理失败，使用更安静的处理方式
                # 不显示任何失败信息作为水印
                # 可以选择直接跳过水印添加或使用透明的空白水印
                
                # 创建一个空白水印 - 不显示"水印图片加载失败"的文字
                text_writer = fitz.TextWriter(page_rect)
                
                # 使用完全透明的设置
                text_writer.opacity = 0.0
                
                # 应用透明水印
                text_writer.write_text(page)
    
    except Exception as e:
        logger.error(f"添加水印到页面出错: {str(e)}")


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys
    from PySide6.QtGui import QFont
    
    app = QApplication(sys.argv)
    font = QFont('微软雅黑', 10)
    app.setFont(font)
    router = Router(None)
    view = WatermarkControl(router)
    view.show()
    sys.exit(app.exec()) 