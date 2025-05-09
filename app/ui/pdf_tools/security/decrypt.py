import os.path
import io
import subprocess
import tempfile
import threading
import time
import multiprocessing
import concurrent.futures
import queue
import math
import sys
import re

import fitz
from PyPDF2 import PdfReader, PdfWriter
from PySide6.QtCore import Signal, QThread, QUrl, Qt, QFile, QIODevice, QTextStream
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon, QFont, QFontMetrics
from PySide6.QtWidgets import (QWidget, QMessageBox, QFileDialog, QRadioButton, 
                              QButtonGroup, QHBoxLayout, QLabel, QCheckBox, 
                              QProgressDialog, QDialog, QVBoxLayout, QPushButton,
                              QLineEdit, QComboBox, QSpinBox, QGroupBox, QListWidget,
                              QListWidgetItem, QGridLayout)

from app.model import PdfFile
from app.ui.components.QCursorGif import QCursorGif
from app.ui.Icon import Icon
from app.util import common
from app.ui.pdf_tools.security.decrypt_ui import Ui_decrypt_pdf_view
from app.ui.components.router import Router
from app.log import logger


def open_file_explorer(path):
    # 使用QDesktopServices打开文件管理器
    if os.path.isfile(path):
        path = os.path.dirname(path)
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))


class DecryptControl(QWidget, Ui_decrypt_pdf_view, QCursorGif):
    okSignal = Signal(bool)
    childRouterSignal = Signal(str)

    def __init__(self, router: Router, parent=None):
        super().__init__(parent)
        self.input_file_path = ""
        self.output_dir = ""
        self.output_filename = "解密文件"
        self.router = router
        self.router_path = (self.parent().router_path if self.parent() else '') + '/解密PDF'
        self.child_routes = {}
        self.worker = None
        self.cracking_canceled = False
        self.setupUi(self)
        # 设置忙碌光标图片数组
        self.initCursor([':/icons/icons/Cursors/%d.png' %
                        i for i in range(8)], self)
        self.setCursorTimeout(100)
        self.init_ui()
        
        # 按钮连接
        self.btn_choose_file.clicked.connect(self.open_file_dialog)
        self.btn_choose_file.setIcon(Icon.Add_Icon)
        self.btn_decrypt.clicked.connect(self.decrypt_pdf)
        
        # 添加解密方式选项
        self.horizontal_decrypt_method = QHBoxLayout()
        self.label_decrypt_method = QLabel(self.groupBox_decrypt_options)
        self.label_decrypt_method.setText("解密方式:")
        self.horizontal_decrypt_method.addWidget(self.label_decrypt_method)
        
        # 创建解密方式下拉框替代单选按钮
        self.combo_decrypt_method = QComboBox(self.groupBox_decrypt_options)
        self.combo_decrypt_method.addItem("常规解密(需要密码)")
        self.combo_decrypt_method.addItem("密码破解(自动尝试破解密码)")
        self.horizontal_decrypt_method.addWidget(self.combo_decrypt_method)
        
        # 密码破解设置按钮
        self.btn_crack_settings = QPushButton(self.groupBox_decrypt_options)
        self.btn_crack_settings.setText("破解设置")
        self.btn_crack_settings.setVisible(False)
        self.btn_crack_settings.clicked.connect(self.show_crack_settings)
        
        # 在密码输入前添加解密方式选择
        self.verticalLayout_options.insertLayout(0, self.horizontal_decrypt_method)
        self.verticalLayout_options.addWidget(self.btn_crack_settings)
        
        # 添加当前尝试密码显示
        self.current_pwd_layout = QHBoxLayout()
        self.label_current_pwd = QLabel("当前尝试密码:")
        self.current_pwd_layout.addWidget(self.label_current_pwd)
        
        self.lineEdit_current_pwd = QLineEdit()
        self.lineEdit_current_pwd.setReadOnly(True)
        self.current_pwd_layout.addWidget(self.lineEdit_current_pwd)
        self.verticalLayout_options.addLayout(self.current_pwd_layout)
        
        # 添加终止按钮
        self.btn_stop_crack = QPushButton("终止破解")
        self.btn_stop_crack.setStyleSheet("background-color: #ff4d4d; color: white;")
        self.btn_stop_crack.clicked.connect(self.stop_cracking)
        self.verticalLayout_options.addWidget(self.btn_stop_crack)
        
        # 初始隐藏密码显示和终止按钮
        self.label_current_pwd.setVisible(False)
        self.lineEdit_current_pwd.setVisible(False)
        self.btn_stop_crack.setVisible(False)
        
        # 解密方式变更事件
        self.combo_decrypt_method.currentIndexChanged.connect(self.update_decrypt_ui)
        
        # 输出选项连接
        self.lineEdit_filename.textChanged.connect(self.change_output_filename)
        self.comboBox_output_dir.activated.connect(self.select_output_dir)
        self.btn_choose_output_dir.clicked.connect(self.set_output_dir)
        
        # 初始界面设置
        self.label_output_dir.setVisible(False)
        self.btn_choose_output_dir.setVisible(False)
        self.btn_decrypt.setEnabled(False)
        
        # 存储密码输入相关控件
        self.password_widgets = [
            self.label_owner_pwd, self.lineEdit_owner_pwd,
            self.label_user_pwd, self.lineEdit_user_pwd
        ]
        
        # 破解设置
        self.crack_settings = {
            "mode": "bruteforce",  # 'dictionary' 或 'bruteforce'，默认暴力破解
            "dict_path": "",      # 字典文件路径
            "min_length": 4,      # 最小密码长度
            "max_length": 8,      # 最大密码长度
            "charset": "digits",  # 'digits', 'lowercase', 'uppercase', 'all'
            "timeout": 0,         # 超时时间(秒)，0表示不限制
            "threads": self.get_recommended_threads(),  # 线程数，默认为推荐值
            "use_gpu": False,     # 是否使用GPU加速
            "selected_gpus": [],  # 选择的GPU设备ID列表
            "hashcat_path": "",   # hashcat安装目录
            "gpu_threads": 8,     # GPU线程数，默认为8
            "gpu_accel": 64,      # GPU加速因子，默认为64
            "workload": 3         # GPU工作负载配置(1-4)，默认为3(高负载)
        }
        
        # 检测GPU
        self.available_gpus = []  # 初始为空列表，等选择了hashcat路径后再检测
        
    def init_ui(self):
        self.btn_decrypt.setObjectName('border')
        if not self.parent():
            pixmap = QPixmap(Icon.logo_ico_path)
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)
            self.setWindowTitle('PDF解密')
            style_qss_file = QFile(":/data/resources/QSS/style.qss")
            if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(style_qss_file)
                style_content = stream.readAll()
                self.setStyleSheet(style_content)
                style_qss_file.close()
        self.lineEdit_filename.setText(self.output_filename)
    
    def update_decrypt_ui(self):
        """更新解密选项UI"""
        current_method = self.combo_decrypt_method.currentIndex()
        is_normal_decrypt = current_method == 0
        is_crack_decrypt = current_method == 1
        
        # 根据解密方式显示/隐藏密码输入框
        for widget in self.password_widgets:
            widget.setVisible(is_normal_decrypt)
        
        # 显示或隐藏破解设置按钮
        self.btn_crack_settings.setVisible(is_crack_decrypt)
        
        # 显示或隐藏当前密码和终止按钮
        self.label_current_pwd.setVisible(False)
        self.lineEdit_current_pwd.setVisible(False)
        self.btn_stop_crack.setVisible(False)
        
        # 说明文本
        if is_normal_decrypt:
            self.label_pwd_info.setText("注：解密PDF文件需要所有者密码，如果没有所有者密码可以尝试使用用户密码")
        elif is_crack_decrypt:
            self.label_pwd_info.setText("注：密码破解功能将尝试自动破解PDF密码。破解速度取决于密码复杂度和计算机性能。\n破解过程可能需要较长时间，请耐心等待。")
            
            # 如果选择了密码破解模式，检查是否安装了必要工具
            if not self.check_cracking_tools_installed():
                reply = QMessageBox.question(
                    self,
                    "缺少必要工具",
                    "使用密码破解功能需要安装John the Ripper，是否查看安装指南？",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )
                if reply == QMessageBox.Yes:
                    self.show_installation_guide()
        else:
            self.label_pwd_info.setText("注：无密码解密功能适用于部分加密保护较弱的PDF文件，将尝试直接移除加密。\n如无法解密，请尝试常规解密方式。")
    
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
        # 打开文件对话框，选择PDF文件
        file_path, _ = QFileDialog.getOpenFileName(self, "选择PDF文件", "", "PDF Files (*.pdf);;All Files (*)")
        if file_path:
            self.input_file_path = file_path
            self.lineEdit_pdf_path.setText(file_path)
            
            # 获取PDF信息
            try:
                with fitz.open(file_path) as pdf:
                    # 检查PDF是否已加密
                    if not pdf.is_encrypted:
                        QMessageBox.information(self, "提示", "选择的PDF文件未加密，无需解密。")
                        self.btn_decrypt.setEnabled(False)
                        return
                    self.btn_decrypt.setEnabled(True)
            except Exception as e:
                logger.error(f"读取PDF文件错误: {str(e)}")
                QMessageBox.critical(self, "错误", f"无法读取PDF文件: {str(e)}")
                self.btn_decrypt.setEnabled(False)
                return
            
            # 如果未设置输出目录，默认使用与PDF相同的目录
            if not self.output_dir:
                self.output_dir = os.path.dirname(file_path)
                font_metrics = QFontMetrics(self.label_output_dir.font())
                elided_text = font_metrics.elidedText(self.output_dir, Qt.ElideRight, self.label_output_dir.width() - 10)
                self.label_output_dir.setText(elided_text)
                self.label_output_dir.setToolTip(self.output_dir)
                
            # 输出文件名格式：原文件名+解密+文件
            filename = os.path.basename(file_path)
            filename_without_ext = os.path.splitext(filename)[0]
            new_filename = f"{filename_without_ext}_解密文件"
            self.output_filename = new_filename
            self.lineEdit_filename.setText(new_filename)
    
    def show_crack_settings(self):
        """显示密码破解设置对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("密码破解设置")
        dialog.setMinimumWidth(500)
        dialog.setMinimumHeight(550)  # 增加高度以容纳新的GPU设置
        
        layout = QVBoxLayout()
        
        # 破解模式选择
        mode_layout = QHBoxLayout()
        mode_label = QLabel("破解模式:")
        mode_layout.addWidget(mode_label)
        
        mode_combo = QComboBox()
        mode_combo.addItem("字典破解(推荐)")
        mode_combo.addItem("暴力破解")
        mode_combo.setCurrentIndex(0 if self.crack_settings["mode"] == "dictionary" else 1)
        mode_layout.addWidget(mode_combo)
        layout.addLayout(mode_layout)
        
        # 字典文件选择
        dict_layout = QHBoxLayout()
        dict_label = QLabel("字典文件:")
        dict_layout.addWidget(dict_label)
        
        dict_path = QLineEdit()
        dict_path.setText(self.crack_settings["dict_path"])
        dict_path.setReadOnly(True)
        dict_layout.addWidget(dict_path)
        
        dict_btn = QPushButton("选择")
        dict_btn.clicked.connect(lambda: self.select_dict_file(dict_path))
        dict_layout.addWidget(dict_btn)
        layout.addLayout(dict_layout)
        
        # 密码长度设置
        length_layout = QHBoxLayout()
        min_label = QLabel("最小长度:")
        length_layout.addWidget(min_label)
        
        min_length = QLineEdit()
        min_length.setText(str(self.crack_settings["min_length"]))
        min_length.setMaximumWidth(50)
        length_layout.addWidget(min_length)
        
        max_label = QLabel("最大长度:")
        length_layout.addWidget(max_label)
        
        max_length = QLineEdit()
        max_length.setText(str(self.crack_settings["max_length"]))
        max_length.setMaximumWidth(50)
        length_layout.addWidget(max_length)
        layout.addLayout(length_layout)
        
        # 字符集选择
        charset_layout = QHBoxLayout()
        charset_label = QLabel("字符集:")
        charset_layout.addWidget(charset_label)
        
        charset_combo = QComboBox()
        charset_combo.addItem("数字 (0-9)")
        charset_combo.addItem("小写字母 (a-z)")
        charset_combo.addItem("大写字母 (A-Z)")
        charset_combo.addItem("字母和数字 (a-zA-Z0-9)")
        charset_combo.addItem("所有字符 (包含特殊符号)")
        
        charset_map = {
            "digits": 0, 
            "lowercase": 1, 
            "uppercase": 2, 
            "alphanumeric": 3,
            "all": 4
        }
        charset_combo.setCurrentIndex(charset_map.get(self.crack_settings["charset"], 0))
        charset_layout.addWidget(charset_combo)
        layout.addLayout(charset_layout)
        
        # CPU线程设置组
        cpu_group = QGroupBox("CPU设置")
        cpu_layout = QVBoxLayout()
        
        # 添加线程数设置
        threads_layout = QHBoxLayout()
        threads_label = QLabel("CPU线程数:")
        threads_layout.addWidget(threads_label)
        
        threads_spinbox = QSpinBox()
        threads_spinbox.setMinimum(1)
        threads_spinbox.setMaximum(1000)  # 移除32线程限制
        threads_spinbox.setValue(self.crack_settings.get("threads", self.get_recommended_threads()))
        threads_spinbox.setToolTip(f"推荐线程数: {self.get_recommended_threads()} (基于CPU核心数)")
        threads_layout.addWidget(threads_spinbox)
        
        # 添加自动推荐按钮
        recommend_btn = QPushButton("推荐值")
        recommend_btn.clicked.connect(lambda: threads_spinbox.setValue(self.get_recommended_threads()))
        threads_layout.addWidget(recommend_btn)
        
        cpu_layout.addLayout(threads_layout)
        cpu_group.setLayout(cpu_layout)
        layout.addWidget(cpu_group)
        
        # 添加GPU加速设置
        gpu_group = QGroupBox("GPU加速")
        gpu_layout = QVBoxLayout()
        
        # GPU启用开关
        use_gpu_checkbox = QCheckBox("启用GPU加速")
        use_gpu_checkbox.setChecked(self.crack_settings.get("use_gpu", False))
        gpu_layout.addWidget(use_gpu_checkbox)
        
        # Hashcat路径选择
        hashcat_layout = QHBoxLayout()
        hashcat_label = QLabel("Hashcat目录:")
        hashcat_layout.addWidget(hashcat_label)
        
        hashcat_path = QLineEdit()
        hashcat_path.setText(self.crack_settings.get("hashcat_path", ""))
        hashcat_path.setReadOnly(True)
        hashcat_layout.addWidget(hashcat_path)
        
        hashcat_btn = QPushButton("选择")
        hashcat_btn.clicked.connect(lambda: self.select_hashcat_dir(hashcat_path, gpu_list))
        hashcat_layout.addWidget(hashcat_btn)
        gpu_layout.addLayout(hashcat_layout)
        
        # 检测Hashcat是否可用的状态标签
        hashcat_status_label = QLabel()
        hashcat_status_label.setText("请先选择Hashcat目录")
        gpu_layout.addWidget(hashcat_status_label)
        
        # 安装指南按钮
        install_hashcat_btn = QPushButton("查看Hashcat安装指南")
        install_hashcat_btn.clicked.connect(self.show_hashcat_installation_guide)
        gpu_layout.addWidget(install_hashcat_btn)
        
        # 添加GPU线程数设置
        gpu_threads_layout = QHBoxLayout()
        gpu_threads_label = QLabel("GPU线程数(-n):")
        gpu_threads_layout.addWidget(gpu_threads_label)
        
        gpu_threads_spinbox = QSpinBox()
        gpu_threads_spinbox.setMinimum(1)
        gpu_threads_spinbox.setMaximum(1024)
        gpu_threads_spinbox.setValue(self.crack_settings.get("gpu_threads", 8))
        gpu_threads_spinbox.setToolTip("设置GPU线程数，影响并行计算能力")
        gpu_threads_layout.addWidget(gpu_threads_spinbox)
        gpu_layout.addLayout(gpu_threads_layout)
        
        # 添加GPU加速因子设置
        gpu_accel_layout = QHBoxLayout()
        gpu_accel_label = QLabel("GPU加速因子(-u):")
        gpu_accel_layout.addWidget(gpu_accel_label)
        
        gpu_accel_spinbox = QSpinBox()
        gpu_accel_spinbox.setMinimum(1)
        gpu_accel_spinbox.setMaximum(1024)
        gpu_accel_spinbox.setValue(self.crack_settings.get("gpu_accel", 64))
        gpu_accel_spinbox.setToolTip("设置GPU加速因子，增大此值可提高GPU利用率")
        gpu_accel_layout.addWidget(gpu_accel_spinbox)
        gpu_layout.addLayout(gpu_accel_layout)
        
        # 添加工作负载配置
        workload_layout = QHBoxLayout()
        workload_label = QLabel("工作负载(-w):")
        workload_layout.addWidget(workload_label)
        
        workload_combo = QComboBox()
        workload_combo.addItem("1 - 低")
        workload_combo.addItem("2 - 默认")
        workload_combo.addItem("3 - 高")
        workload_combo.addItem("4 - 最高")
        workload_combo.setCurrentIndex(self.crack_settings.get("workload", 3) - 1)
        workload_combo.setToolTip("设置GPU工作负载，值越高利用率越高，但可能影响系统响应")
        workload_layout.addWidget(workload_combo)
        gpu_layout.addLayout(workload_layout)
        
        # GPU设备选择
        gpu_devices_label = QLabel("选择GPU设备:")
        gpu_layout.addWidget(gpu_devices_label)
        
        # GPU列表
        gpu_list = QListWidget()
        gpu_list.setSelectionMode(QListWidget.MultiSelection)
        
        # 最初的状态提示
        if not hashcat_path.text():
            item = QListWidgetItem("请先选择Hashcat目录")
            gpu_list.addItem(item)
            gpu_list.setEnabled(False)
        elif self.available_gpus:
            for i, gpu in enumerate(self.available_gpus):
                item = QListWidgetItem(f"{i}: {gpu}")
                gpu_list.addItem(item)
                # 如果之前选择了该GPU，设置为选中状态
                if i in self.crack_settings.get("selected_gpus", []):
                    item.setSelected(True)
        else:
            gpu_list.addItem("未检测到GPU设备")
            gpu_list.setEnabled(False)
        
        gpu_layout.addWidget(gpu_list)
        
        # 刷新GPU列表按钮
        refresh_gpu_btn = QPushButton("刷新GPU列表")
        refresh_gpu_btn.clicked.connect(lambda: self.refresh_gpu_list(gpu_list, hashcat_path.text()))
        gpu_layout.addWidget(refresh_gpu_btn)
        
        gpu_group.setLayout(gpu_layout)
        layout.addWidget(gpu_group)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("确定")
        cancel_btn = QPushButton("取消")
        
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        
        # 检查hashcat状态并更新UI
        def check_hashcat_status():
            path = hashcat_path.text()
            if not path:
                hashcat_status_label.setText("请先选择Hashcat目录")
                hashcat_status_label.setStyleSheet("color: black;")
                return False
                
            is_valid = self.check_hashcat_in_dir(path)
            if is_valid:
                hashcat_status_label.setText("Hashcat可用 ✓")
                hashcat_status_label.setStyleSheet("color: green;")
                return True
            else:
                hashcat_status_label.setText("所选目录中未找到有效的Hashcat ✗")
                hashcat_status_label.setStyleSheet("color: red;")
                return False
                
        # 初始检查
        hashcat_valid = check_hashcat_status()
        
        # 连接按钮事件
        ok_btn.clicked.connect(lambda: self.save_crack_settings(
            mode_combo.currentIndex() == 0,
            dict_path.text(),
            min_length.text(),
            max_length.text(),
            charset_combo.currentIndex(),
            "0",  # 总是传递0作为超时时间
            threads_spinbox.value(),
            use_gpu_checkbox.isChecked(),
            [i for i in range(gpu_list.count()) if gpu_list.item(i).isSelected() and not gpu_list.item(i).text().startswith("请先")
                and not gpu_list.item(i).text().startswith("未检测到")],
            hashcat_path.text(),
            gpu_threads_spinbox.value(),
            gpu_accel_spinbox.value(),
            workload_combo.currentIndex() + 1,
            dialog
        ))
        cancel_btn.clicked.connect(dialog.reject)
        
        # 根据模式启用/禁用控件
        def update_ui():
            is_dict_mode = mode_combo.currentIndex() == 0
            dict_path.setEnabled(is_dict_mode)
            dict_btn.setEnabled(is_dict_mode)
            
            min_length.setEnabled(not is_dict_mode)
            max_length.setEnabled(not is_dict_mode)
            charset_combo.setEnabled(not is_dict_mode)
            
            # GPU设置只在启用GPU并且有hashcat时可用
            gpu_enabled = use_gpu_checkbox.isChecked() and hashcat_valid
            gpu_list.setEnabled(gpu_enabled)
            gpu_threads_spinbox.setEnabled(gpu_enabled)
            gpu_accel_spinbox.setEnabled(gpu_enabled)
            workload_combo.setEnabled(gpu_enabled)
        
        update_ui()
        mode_combo.currentIndexChanged.connect(update_ui)
        use_gpu_checkbox.toggled.connect(update_ui)
        
        dialog.exec_()
    
    def select_hashcat_dir(self, line_edit, gpu_list=None):
        """选择Hashcat安装目录"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择Hashcat安装目录")
        if dir_path:
            # 检查目录是否包含hashcat可执行文件
            is_valid = self.check_hashcat_in_dir(dir_path)
            
            if is_valid:
                line_edit.setText(dir_path)
                # 如果提供了GPU列表，刷新它
                if gpu_list:
                    self.refresh_gpu_list(gpu_list, dir_path)
            else:
                QMessageBox.warning(
                    self, 
                    "无效的Hashcat目录", 
                    "在所选目录中未找到有效的Hashcat可执行文件。请确保选择正确的Hashcat安装目录。"
                )
    
    def check_hashcat_in_dir(self, dir_path):
        """检查指定目录中是否存在有效的hashcat可执行文件"""
        if not dir_path:
            return False
            
        # 根据操作系统确定可执行文件名
        if os.name == 'nt':  # Windows
            hashcat_exe = os.path.join(dir_path, "hashcat.exe")
        else:  # Linux/macOS
            hashcat_exe = os.path.join(dir_path, "hashcat")
            
        # 检查是否存在
        if not os.path.isfile(hashcat_exe):
            return False
            
        # 检查是否可执行
        try:
            # 使用绝对路径运行hashcat --version命令
            result = subprocess.run(
                [hashcat_exe, "--version"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            
            # 检查命令是否执行成功
            return result.returncode == 0
        except Exception as e:
            logger.error(f"检查hashcat出错: {str(e)}")
            return False
    
    def refresh_gpu_list(self, gpu_list, hashcat_dir=""):
        """刷新GPU列表"""
        # 保存当前选择的项目
        selected_indexes = [i for i in range(gpu_list.count()) 
                          if gpu_list.item(i).isSelected() and not gpu_list.item(i).text().startswith("请先")
                            and not gpu_list.item(i).text().startswith("未检测到")]
        
        # 清空列表
        gpu_list.clear()
        
        # 如果未提供hashcat目录，使用保存的路径
        if not hashcat_dir:
            hashcat_dir = self.crack_settings.get("hashcat_path", "")
        
        # 检查hashcat目录是否有效
        if not hashcat_dir or not self.check_hashcat_in_dir(hashcat_dir):
            gpu_list.addItem("请先选择有效的Hashcat目录")
            gpu_list.setEnabled(False)
            self.available_gpus = []
            return
        
        # 重新检测GPU
        self.available_gpus = self.detect_gpu_with_hashcat(hashcat_dir)
        
        # 重新填充列表
        if self.available_gpus:
            for i, gpu in enumerate(self.available_gpus):
                item = QListWidgetItem(f"{i}: {gpu}")
                gpu_list.addItem(item)
                # 如果之前选择了该索引，并且索引仍然有效，则重新选中
                if i in selected_indexes and i < len(self.available_gpus):
                    item.setSelected(True)
        else:
            gpu_list.addItem("未检测到GPU设备")
            gpu_list.setEnabled(False)
    
    def detect_gpu_with_hashcat(self, hashcat_dir):
        """使用指定目录中的hashcat检测GPU设备"""
        gpu_list = []
        
        # 确定hashcat可执行文件路径
        if os.name == 'nt':  # Windows
            hashcat_exe = os.path.join(hashcat_dir, "hashcat.exe")
        else:  # Linux/macOS
            hashcat_exe = os.path.join(hashcat_dir, "hashcat")
        
        try:
            # 检查是否存在hashcat
            if not os.path.isfile(hashcat_exe):
                logger.error(f"未找到hashcat可执行文件: {hashcat_exe}")
                return gpu_list
            
            # 执行hashcat --listdevices命令
            result = subprocess.run(
                [hashcat_exe, "--listdevices"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                # 解析输出中的GPU信息
                output = result.stdout
                # 查找形如 * Device #1: ... 的行
                device_lines = re.findall(r'Device #\d+:.*', output)
                
                for line in device_lines:
                    # 提取设备名称
                    if "CPU" not in line and ("GPU" in line or "NVIDIA" in line or "AMD" in line):
                        name_match = re.search(r'Device #\d+: (.*)', line)
                        if name_match:
                            gpu_name = name_match.group(1).strip()
                            gpu_list.append(gpu_name)
            
            # 如果hashcat未检测到GPU，尝试其他方法
            if not gpu_list:
                # 这里可以添加备用检测方法，保持与之前相同
                if os.name == 'nt':  # Windows
                    # 使用WMIC查询GPU信息
                    result = subprocess.run(
                        ["wmic", "path", "win32_VideoController", "get", "Name"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        check=False
                    )
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
                        for line in lines:
                            if line.strip():
                                gpu_list.append(line.strip())
                
                elif sys.platform == 'darwin':  # macOS
                    result = subprocess.run(
                        ["system_profiler", "SPDisplaysDataType"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        check=False
                    )
                    if result.returncode == 0:
                        for line in result.stdout.split('\n'):
                            if "Chipset Model:" in line:
                                gpu_name = line.split(':', 1)[1].strip()
                                gpu_list.append(gpu_name)
                
                else:  # Linux
                    # 尝试使用lspci
                    result = subprocess.run(
                        ["lspci", "-v"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        check=False
                    )
                    if result.returncode == 0:
                        for line in result.stdout.split('\n'):
                            if "VGA" in line or "3D" in line:
                                parts = line.split(':', 2)
                                if len(parts) >= 3:
                                    gpu_name = parts[2].strip()
                                    gpu_list.append(gpu_name)
        
        except Exception as e:
            logger.error(f"使用hashcat检测GPU出错: {str(e)}")
        
        return gpu_list
    
    def save_crack_settings(self, is_dict_mode, dict_path, min_length, max_length, charset_index, 
                          timeout, threads, use_gpu, selected_gpus, hashcat_path, 
                          gpu_threads=8, gpu_accel=64, workload=3, dialog=None):
        """保存破解设置"""
        # 验证输入
        if is_dict_mode and not os.path.exists(dict_path):
            QMessageBox.warning(self, "警告", "请选择有效的字典文件")
            return
        
        try:
            min_len = int(min_length)
            max_len = int(max_length)
            # 忽略超时参数，始终设置为0表示无限制
            timeout_val = 0
            # 线程数不再限制最大值
            thread_count = max(1, threads)
            # GPU相关参数验证
            gpu_threads_val = max(1, min(gpu_threads, 1024))
            gpu_accel_val = max(1, min(gpu_accel, 1024))
            workload_val = max(1, min(workload, 4))
            
            if min_len < 1 or max_len < min_len:
                raise ValueError("无效的参数值")
        except ValueError:
            QMessageBox.warning(self, "警告", "请输入有效的数字")
            return
        
        # 验证GPU选择
        if use_gpu:
            # 验证hashcat路径
            if not hashcat_path or not self.check_hashcat_in_dir(hashcat_path):
                QMessageBox.warning(self, "警告", "请选择有效的Hashcat目录")
                return
            
            # 验证是否选择了GPU
            if not selected_gpus:
                reply = QMessageBox.question(
                    self,
                    "未选择GPU",
                    "您启用了GPU加速但未选择任何GPU设备。是否继续？",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return
        
        # 保存设置
        charset_map = ["digits", "lowercase", "uppercase", "alphanumeric", "all"]
        self.crack_settings = {
            "mode": "dictionary" if is_dict_mode else "bruteforce",
            "dict_path": dict_path,
            "min_length": min_len,
            "max_length": max_len,
            "charset": charset_map[charset_index],
            "timeout": timeout_val,
            "threads": thread_count,
            "use_gpu": use_gpu,
            "selected_gpus": selected_gpus,
            "hashcat_path": hashcat_path,
            "gpu_threads": gpu_threads_val,
            "gpu_accel": gpu_accel_val,
            "workload": workload_val
        }
        
        if dialog:
            dialog.accept()
    
    def decrypt_pdf(self):
        if not os.path.exists(self.input_file_path):
            QMessageBox.critical(self, "错误", "请先选择PDF文件")
            return
        
        # 获取解密方式
        decrypt_method = self.combo_decrypt_method.currentIndex()
        use_crack_decrypt = decrypt_method == 1
        
        # 准备密码参数
        if decrypt_method == 0:  # 常规解密
            owner_password = self.lineEdit_owner_pwd.text()
            user_password = self.lineEdit_user_pwd.text()
            
            if not owner_password and not user_password:
                QMessageBox.warning(self, "警告", "请输入所有者密码或用户密码")
                return
        else:
            owner_password = ""
            user_password = ""
        
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
        
        # 生成输出文件路径
        output_path = os.path.join(output_directory, f"{self.output_filename}.pdf")
        output_path = common.usable_filepath(output_path)
        
        # 禁用按钮，开始任务
        self.btn_decrypt.setEnabled(False)
        self.cracking_canceled = False
        self.startBusy()
        
        # 如果是暴力破解模式，显示当前密码标签和终止按钮
        if use_crack_decrypt:
            self.label_current_pwd.setVisible(True)
            self.lineEdit_current_pwd.setVisible(True)
            self.btn_stop_crack.setVisible(True)
            self.lineEdit_current_pwd.setText("准备开始...")
        
        # 创建并启动工作线程
        input_file = PdfFile(self.input_file_path)
        self.worker = DecryptThread(
            input_file=input_file,
            output_path=output_path,
            owner_password=owner_password,
            user_password=user_password,
            use_force_decrypt=False,
            use_crack_decrypt=use_crack_decrypt,
            crack_settings=self.crack_settings
        )
        
        # 连接信号
        self.worker.progressSignal.connect(self.update_progress)
        self.worker.okSignal.connect(self.decrypt_finish)
        if use_crack_decrypt:
            self.worker.current_pwd_signal.connect(self.update_current_pwd)
        
        self.worker.start()
    
    def update_current_pwd(self, pwd):
        """更新当前尝试的密码"""
        self.lineEdit_current_pwd.setText(pwd)
    
    def stop_cracking(self):
        """终止密码破解"""
        if self.worker and self.worker.isRunning():
            # 设置标志位，告知线程需要终止
            self.cracking_canceled = True
            # 请求中断线程，但不强制终止
            self.worker.requestInterruption()
            
            # 显示正在终止
            self.lineEdit_current_pwd.setText("正在安全终止...")
            
            # 给线程一些时间来自行终止
            if not self.worker.wait(1000):  # 等待最多1秒
                # 如果线程没有及时终止，通知用户
                logger.warning("线程未能在短时间内终止，可能需要更长时间")
                self.lineEdit_current_pwd.setText("终止中，请稍候...")
                
                # 继续等待线程自行终止，避免强制终止
                if not self.worker.wait(3000):  # 再等3秒
                    logger.warning("线程仍未终止，考虑安全地结束")
                    # 不使用terminate()，避免崩溃
            
            # 恢复UI状态
            self.btn_decrypt.setEnabled(True)
            self.progressBar.setValue(0)
            # 停止忙碌光标
            self.stopBusy()
            
            # 简单提示已终止
            self.lineEdit_current_pwd.setText("已终止破解")
            # 不将worker设为None，避免线程对象被垃圾回收而引起问题
            # 而是让线程自然结束
            
            logger.info("用户手动终止破解进程")
    
    def update_progress(self, value):
        self.progressBar.setValue(value)
    
    def decrypt_finish(self, result_data):
        self.stopBusy()
        success, message = result_data
        
        # 隐藏当前密码标签和终止按钮
        self.label_current_pwd.setVisible(False)
        self.lineEdit_current_pwd.setVisible(False)
        self.btn_stop_crack.setVisible(False)
        
        if success:
            # 处理可能存在的多行消息（包含密码信息等）
            folder_path = message.split('\n')[0] if '\n' in message else message
            
            # 确保路径是有效的目录路径
            if not os.path.isdir(folder_path):
                folder_path = os.path.dirname(folder_path)
            
            reply = QMessageBox(self)
            reply.setIcon(QMessageBox.Information)
            reply.setWindowTitle('完成')
            reply.setText(f"PDF解密成功\n{message}")
            btn = reply.addButton('打开文件夹', QMessageBox.ActionRole)
            # 使用更可靠的方法打开文件夹
            btn.clicked.connect(lambda: open_file_explorer(folder_path))
            reply.addButton("确认", QMessageBox.AcceptRole)
            reply.exec_()
        else:
            if self.cracking_canceled:
                # 如果是用户终止的，不显示任何消息框，状态已在stop_cracking()中恢复
                pass
            else:
                QMessageBox.critical(self, "错误", f"PDF解密失败: {message}")
        
        # 恢复UI状态
        self.btn_decrypt.setEnabled(True)
        self.progressBar.setValue(0)
        self.worker = None
        self.cracking_canceled = False
    
    def closeEvent(self, event):
        super().closeEvent(event)
        self.okSignal.emit(True)
    
    def check_cracking_tools_installed(self):
        """检查是否安装了密码破解工具"""
        # 全局变量，用于调试
        global johnOutput
        johnOutput = ""
        
        try:
            # 检查John the Ripper
            logger.info("开始检查John the Ripper是否安装...")
            
            # 尝试方法1：直接运行john命令
            john_process = subprocess.Popen(
                ["john"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            stdout, stderr = john_process.communicate()
            
            # 记录输出到全局变量和日志
            john_stdout = stdout.decode('utf-8', errors='ignore')
            john_stderr = stderr.decode('utf-8', errors='ignore')
            johnOutput = f"STDOUT: {john_stdout}\nSTDERR: {john_stderr}"
            
            logger.info(f"John命令输出: {johnOutput}")
            
            # 宽松检查：只要命令成功运行就认为已安装
            if john_process.returncode == 0 or "john" in john_stdout.lower() or "john" in john_stderr.lower():
                logger.info("检测到John the Ripper已安装(命令成功或包含关键字)")
                return True
                
            logger.info("第一种方法未检测到John the Ripper")
            
            # 尝试方法2：使用shell执行
            try:
                if os.name == 'nt':  # Windows系统
                    result = subprocess.run("where john", shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        logger.info("通过where命令找到john路径")
                        return True
                else:  # Unix系统
                    result = subprocess.run("which john", shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        logger.info("通过which命令找到john路径")
                        return True
            except Exception as e:
                logger.error(f"尝试检测john路径时出错: {str(e)}")
            
            logger.info("未能检测到John the Ripper的安装")
            return False
            
        except Exception as e:
            logger.error(f"检查John the Ripper安装出错: {str(e)}")
            return False
    
    def verify_installation(self):
        """验证工具安装状态"""
        # 检查John the Ripper
        john_installed = False
        pdf2john_installed = False
        
        # 全局变量，用于调试
        global johnOutput
        
        try:
            logger.info("验证John the Ripper安装...")
            john_process = subprocess.Popen(
                ["john"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            stdout, stderr = john_process.communicate()
            
            # 记录输出到全局变量
            john_stdout = stdout.decode('utf-8', errors='ignore')
            john_stderr = stderr.decode('utf-8', errors='ignore')
            johnOutput = f"STDOUT: {john_stdout}\nSTDERR: {john_stderr}"
            
            logger.info(f"验证时John命令输出: {johnOutput}")
            
            # 宽松判断是否已安装
            john_installed = john_process.returncode == 0 or "john" in john_stdout.lower() or "john" in john_stderr.lower()
            
            # 判断是否包含版本信息
            john_version = "已安装"
            
            # 优先使用stderr，因为john的版本信息常常显示在stderr
            if "john" in john_stderr.lower():
                version_lines = john_stderr.split('\n')
                if version_lines:
                    john_version = version_lines[0].strip()
            elif "john" in john_stdout.lower():
                version_lines = john_stdout.split('\n')
                if version_lines:
                    john_version = version_lines[0].strip()
            
            # 如果没有安装，查看全局输出
            if not john_installed:
                john_version = f"未安装 - 命令输出: {johnOutput}"
            
        except Exception as e:
            logger.error(f"验证John the Ripper安装出错: {str(e)}")
            john_version = f"未安装 - 错误: {str(e)}"
        
        try:
            pdf2john_process = subprocess.Popen(
                ["where", "pdf2john"] if os.name == "nt" else ["which", "pdf2john"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            pdf2john_process.communicate()
            pdf2john_installed = pdf2john_process.returncode == 0
        except:
            pass
        
        if not pdf2john_installed:
            try:
                pdf2john_process = subprocess.Popen(
                    ["where", "pdf2john.py"] if os.name == "nt" else ["which", "pdf2john.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                pdf2john_process.communicate()
                pdf2john_installed = pdf2john_process.returncode == 0
            except:
                pass
        
        # 显示安装状态
        status_message = f"John the Ripper: {'已安装 - ' + john_version if john_installed else john_version}\n"
        status_message += f"pdf2john: {'已安装' if pdf2john_installed else '未安装'}\n\n"
        
        if john_installed and pdf2john_installed:
            status_message += "所有必要工具已安装，可以使用密码破解功能。"
        else:
            status_message += "部分工具未安装，密码破解功能可能无法正常工作。请按照安装指南进行安装。"
        
        QMessageBox.information(self, "安装状态", status_message)
    
    def show_installation_guide(self):
        """显示工具安装指南"""
        dialog = QDialog(self)
        dialog.setWindowTitle("密码破解工具安装指南")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        
        # 添加安装说明
        info_label = QLabel()
        info_label.setWordWrap(True)
        info_label.setText(
            "<h3>安装John the Ripper的步骤</h3>"
            "<p><b>1. Windows系统：</b></p>"
            "<ul>"
            "<li>访问官方网站下载：<a href='https://www.openwall.com/john/'>https://www.openwall.com/john/</a></li>"
            "<li>下载Windows版本(John the Ripper 1.9.0 jumbo-1)</li>"
            "<li>解压下载的ZIP文件</li>"
            "<li>将解压后的run文件夹添加到系统PATH环境变量</li>"
            "</ul>"
            "<p><b>2. Linux系统：</b></p>"
            "<ul>"
            "<li>Ubuntu/Debian: <code>sudo apt-get install john</code></li>"
            "<li>Fedora: <code>sudo dnf install john</code></li>"
            "<li>Arch Linux: <code>sudo pacman -S john</code></li>"
            "</ul>"
            "<p><b>3. macOS系统：</b></p>"
            "<ul>"
            "<li>使用Homebrew: <code>brew install john</code></li>"
            "</ul>"
            "<p><b>验证安装：</b></p>"
            "<ul>"
            "<li>打开命令行或终端</li>"
            "<li>输入<code>john</code>命令</li>"
            "<li>如果显示包含\"John the Ripper\"的信息，则安装成功</li>"
            "</ul>"
            "<p><b>注意事项：</b></p>"
            "<ul>"
            "<li>命令安装：pip install pdf2john"
            "</ul>"
        )
        
        layout.addWidget(info_label)
        
        # 检查安装状态按钮
        check_btn = QPushButton("检查安装状态")
        check_btn.clicked.connect(self.verify_installation)
        layout.addWidget(check_btn)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def get_recommended_threads(self):
        """根据系统CPU核心数推荐合适的线程数"""
        # 获取CPU核心数
        cpu_count = multiprocessing.cpu_count()
        # 推荐使用核心数-1的线程数，最少为2
        return max(2, cpu_count - 1)

    def show_hashcat_installation_guide(self):
        """显示Hashcat安装指南"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Hashcat安装指南")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        
        # 添加安装说明
        info_label = QLabel()
        info_label.setWordWrap(True)
        info_label.setText(
            "<h3>安装Hashcat的步骤</h3>"
            "<p><b>1. Windows系统：</b></p>"
            "<ul>"
            "<li>访问官方网站下载：<a href='https://github.com/hashcat/hashcat/releases'>https://github.com/hashcat/hashcat/releases</a></li>"
            "<li>下载Windows版本的.7z文件(如hashcat-6.2.6.7z)</li>"
            "<li>使用7zip解压下载的文件到任意目录</li>"
            "<li>在PDF解密工具中选择刚才解压出来的目录作为Hashcat目录</li>"
            "<li><b>注意：</b>目录中应当直接包含hashcat.exe文件</li>"
            "</ul>"
            "<p><b>2. Linux系统：</b></p>"
            "<ul>"
            "<li>从发行版仓库安装: <code>sudo apt-get install hashcat</code>(Ubuntu/Debian) 或相应命令</li>"
            "<li>或从官网下载Linux版本并解压到任意目录</li>"
            "<li>在PDF解密工具中选择hashcat的安装目录</li>"
            "</ul>"
            "<p><b>3. macOS系统：</b></p>"
            "<ul>"
            "<li>使用Homebrew安装: <code>brew install hashcat</code></li>"
            "<li>找到安装路径(通常是/usr/local/bin/或/opt/homebrew/bin/)</li>"
            "<li>在PDF解密工具中选择该目录</li>"
            "</ul>"
            "<p><b>验证安装：</b></p>"
            "<ul>"
            "<li>在PDF解密工具中选择好Hashcat目录后，可以看到\"Hashcat可用 ✓\"的提示</li>"
            "<li>如果看到错误提示，请确认选择的目录中直接包含hashcat可执行文件</li>"
            "</ul>"
            "<p><b>注意事项：</b></p>"
            "<ul>"
            "<li>确保已安装GPU驱动程序（NVIDIA或AMD）</li>"
            "<li>例如：NVIDIA需要安装CUDA</li>"
            "<li>使用Hashcat进行GPU加速需要OpenCL支持</li>"
            "<li>某些集成显卡可能不支持或性能较差</li>"
            "<li>如果不确定Hashcat的具体目录，请在系统中找到hashcat可执行文件，然后选择其所在目录</li>"
            "</ul>"
        )
        
        layout.addWidget(info_label)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec_()


class DecryptThread(QThread):
    okSignal = Signal(tuple)  # (success, message)
    progressSignal = Signal(int)
    current_pwd_signal = Signal(str)  # 新增信号，用于传递当前尝试的密码

    def __init__(self, input_file, output_path, owner_password="", user_password="", 
                 use_force_decrypt=False, use_crack_decrypt=False, crack_settings=None):
        super().__init__()
        self.input_file = input_file
        self.output_path = output_path
        self.owner_password = owner_password
        self.user_password = user_password
        self.use_force_decrypt = use_force_decrypt
        self.use_crack_decrypt = use_crack_decrypt
        self.crack_settings = crack_settings or {}
        self.should_stop = False  # 添加停止标记
    
    def check_tool_installed(self, tool_name):
        """检查是否安装了指定工具"""
        try:
            if tool_name in ["pdf2john.py", "pdf2john"]:
                # 特殊处理pdf2john
                process = subprocess.Popen(
                    ["where", tool_name] if os.name == "nt" else ["which", tool_name], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE
                )
                process.communicate()
                return process.returncode == 0
            elif tool_name == "john":
                # 特殊处理john
                john_process = subprocess.Popen(
                    ["john"], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    shell=True
                )
                stdout, stderr = john_process.communicate()
                
                # 记录输出用于调试
                john_stdout = stdout.decode('utf-8', errors='ignore')
                john_stderr = stderr.decode('utf-8', errors='ignore')
                
                # 宽松检查
                return john_process.returncode == 0 or "john" in john_stdout.lower() or "john" in john_stderr.lower()
            else:
                # 一般工具检查
                subprocess.run(
                    [tool_name, "--version"], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    check=False
                )
                return True
        except Exception as e:
            logger.error(f"检查{tool_name}工具安装出错: {str(e)}")
            return False
    
    def run(self):
        if self.use_crack_decrypt:
            # 使用密码破解工具尝试破解密码
            return self.run_crack_decrypt()
        else:
            # 使用PyMuPDF带密码解密
            return self.run_normal_decrypt()
        
    def run_crack_decrypt(self):
        """使用密码破解工具尝试破解PDF密码"""
        try:
            self.progressSignal.emit(10)
            logger.info("开始尝试破解PDF密码")
            
            # 确认PDF是否加密
            try:
                with fitz.open(self.input_file.file_path) as pdf:
                    if not pdf.is_encrypted:
                        self.okSignal.emit((False, "PDF文件未加密，无需解密"))
                        return
            except Exception as e:
                logger.error(f"检查PDF加密状态失败: {str(e)}")
            
            # 准备临时文件
            temp_dir = tempfile.mkdtemp()
            
            # 直接尝试常见密码
            self.progressSignal.emit(20)
            common_passwords = ['', '1234', '0000', '1111', '9999', '123456', 'password', 'admin', 'qwerty']
            logger.info("尝试一些常见密码...")
            
            for pwd in common_passwords:
                if self.isInterruptionRequested():
                    logger.info("破解过程被用户终止")
                    self.okSignal.emit((False, "用户终止了破解过程"))
                    return
                    
                self.current_pwd_signal.emit(f"尝试常见密码: {pwd}")
                try:
                    with fitz.open(self.input_file.file_path) as pdf:
                        if pdf.authenticate(pwd):
                            # 成功找到密码
                            logger.info(f"使用常见密码'{pwd}'成功解密")
                            
                            # 保存解密后的PDF
                            pdf.save(self.output_path)
                            self.progressSignal.emit(100)
                            success_message = f"{os.path.dirname(self.output_path)}\n成功使用密码: {pwd}"
                            self.okSignal.emit((True, success_message))
                            return
                except Exception as e:
                    logger.error(f"尝试密码'{pwd}'失败: {str(e)}")
            
            # 检查是否需要使用GPU加速
            use_gpu = self.crack_settings.get("use_gpu", False)
            
            # 如果启用GPU且Hashcat可用，使用Hashcat进行GPU加速破解
            if use_gpu and self.check_tool_installed("hashcat"):
                return self.run_gpu_crack()
                
            # 根据模式选择破解方法
            if self.crack_settings.get("mode") == "dictionary":
                return self.run_dict_crack()
            
            # 暴力破解模式 - 使用排列组合方式，多线程处理
            if self.crack_settings.get("mode") == "bruteforce":
                return self.run_bruteforce_crack()
            
            # 如果所有尝试都失败，返回未成功消息
            logger.info("所有密码尝试均失败")
            self.okSignal.emit((False, "未能破解密码，请尝试其他解密方法"))
            
        except Exception as e:
            logger.error(f"PDF破解错误: {str(e)}")
            self.okSignal.emit((False, f"PDF破解失败: {str(e)}"))
            return
    
    def run_gpu_crack(self):
        """使用GPU加速进行密码破解"""
        try:
            # 获取设置
            is_dict_mode = self.crack_settings.get("mode") == "dictionary"
            selected_gpus = self.crack_settings.get("selected_gpus", [])
            hashcat_dir = self.crack_settings.get("hashcat_path", "")
            gpu_threads = self.crack_settings.get("gpu_threads", 8)
            gpu_accel = self.crack_settings.get("gpu_accel", 64)
            workload = self.crack_settings.get("workload", 3)
            
            # 检查hashcat路径
            if not hashcat_dir:
                self.okSignal.emit((False, "未指定Hashcat目录"))
                return
                
            # 确定hashcat可执行文件路径
            if os.name == 'nt':  # Windows
                hashcat_exe = os.path.join(hashcat_dir, "hashcat.exe")
            else:  # Linux/macOS
                hashcat_exe = os.path.join(hashcat_dir, "hashcat")
                
            # 检查是否存在hashcat
            if not os.path.isfile(hashcat_exe):
                self.okSignal.emit((False, f"未找到Hashcat可执行文件: {hashcat_exe}"))
                return
            
            # 创建临时目录
            temp_dir = tempfile.mkdtemp()
            hash_file = os.path.join(temp_dir, "pdf_hash.txt")
            
            # 提取PDF密码哈希
            self.current_pwd_signal.emit("正在提取PDF密码哈希...")
            
            # 使用pdf2john提取哈希
            try:
                # 尝试直接使用pdf2john
                pdf2john_cmd = ["pdf2john", self.input_file.file_path]
                result = subprocess.run(
                    pdf2john_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False
                )
                
                if result.returncode != 0:
                    # 尝试使用pdf2john.py
                    pdf2john_cmd = ["pdf2john.py", self.input_file.file_path]
                    result = subprocess.run(
                        pdf2john_cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        check=False
                    )
                
                if result.returncode != 0:
                    self.okSignal.emit((False, "提取PDF密码哈希失败，无法使用GPU加速"))
                    return
                
                # 保存哈希到文件
                hash_content = result.stdout.strip()
                with open(hash_file, 'w') as f:
                    f.write(hash_content)
                
                logger.info(f"成功提取PDF密码哈希: {hash_content[:50]}...")
                
            except Exception as e:
                logger.error(f"提取PDF密码哈希失败: {str(e)}")
                self.okSignal.emit((False, f"提取PDF密码哈希失败: {str(e)}"))
                return
            
            # 准备hashcat命令
            hashcat_cmd = [hashcat_exe]  # 使用指定目录的hashcat可执行文件
            
            # 添加设备选项
            if selected_gpus:
                devices_str = ",".join(str(gpu) for gpu in selected_gpus)
                hashcat_cmd.extend(["-d", devices_str])
            
            # 添加哈希类型 (PDF的哈希类型为10400/10500/10600，取决于PDF版本)
            hashcat_cmd.extend(["-m", "10500"])  # 尝试使用PDF 1.4-1.6格式
            
            # 添加GPU优化参数
            hashcat_cmd.extend(["-n", str(gpu_threads)])  # GPU线程数
            hashcat_cmd.extend(["-u", str(gpu_accel)])    # GPU加速因子
            hashcat_cmd.extend(["-w", str(workload)])     # 工作负载
            
            # 优化参数
            hashcat_cmd.extend(["--opencl-device-types=1,2,3"])  # 使用所有类型的OpenCL设备
            hashcat_cmd.extend(["--force"])  # 忽略警告
            hashcat_cmd.extend(["--optimized-kernel-enable"])  # 启用优化内核
            
            # 添加哈希文件
            hashcat_cmd.append(hash_file)
            
            # 根据模式添加字典或掩码
            if is_dict_mode:
                # 字典模式
                dict_path = self.crack_settings.get("dict_path", "")
                if not os.path.exists(dict_path):
                    self.okSignal.emit((False, "字典文件不存在"))
                    return
                
                hashcat_cmd.append(dict_path)
                
                self.current_pwd_signal.emit(f"正在使用GPU加速进行字典破解 (线程数:{gpu_threads}, 加速因子:{gpu_accel})...")
                logger.info(f"执行GPU字典破解命令: {' '.join(hashcat_cmd)}")
                
            else:
                # 暴力破解模式
                min_len = self.crack_settings.get("min_length", 4)
                max_len = self.crack_settings.get("max_length", 8)
                charset = self.crack_settings.get("charset", "digits")
                
                # 定义字符集掩码
                charset_mask = ""
                if charset == "digits":
                    charset_mask = "?d"  # 数字
                elif charset == "lowercase":
                    charset_mask = "?l"  # 小写字母
                elif charset == "uppercase":
                    charset_mask = "?u"  # 大写字母
                elif charset == "alphanumeric":
                    charset_mask = "?a"  # 字母数字
                else:  # all
                    charset_mask = "?a"  # 所有字符
                
                # 构建掩码
                mask = charset_mask * min_len
                
                # 添加掩码参数
                hashcat_cmd.append(mask)
                
                # 如果有长度范围，添加增量模式
                if min_len < max_len:
                    increment_str = f"--increment --increment-min={min_len} --increment-max={max_len}"
                    hashcat_cmd.extend(increment_str.split())
                
                self.current_pwd_signal.emit(
                    f"正在使用GPU加速进行暴力破解 (长度: {min_len}-{max_len}, 线程数:{gpu_threads}, 加速因子:{gpu_accel})..."
                )
                logger.info(f"执行GPU暴力破解命令: {' '.join(hashcat_cmd)}")
            
            # 添加其他选项
            hashcat_cmd.extend(["--status", "--potfile-disable"])
            
            # 运行hashcat进程
            self.progressSignal.emit(30)
            hashcat_process = subprocess.Popen(
                hashcat_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # 创建读取输出的线程，防止阻塞
            def read_output():
                found_password = None
                for line in hashcat_process.stdout:
                    if self.isInterruptionRequested():
                        hashcat_process.terminate()
                        break
                    
                    # 解析hashcat输出，更新进度和找到的密码
                    if "STATUS" in line:
                        try:
                            progress = re.search(r'PROGRESS\s*:\s*(\d+)', line)
                            if progress:
                                progress_val = min(int(progress.group(1)), 100)
                                self.progressSignal.emit(30 + int(progress_val * 0.6))
                        except:
                            pass
                    
                    if "Session.Name..." in line:
                        self.current_pwd_signal.emit("GPU加速初始化完成，开始破解...")
                    
                    # 更新进度信息
                    if "Speed.Dev" in line:
                        speed_match = re.search(r'Speed.Dev.*:\s*([\d.]+)\s*([A-Za-z/]+)', line)
                        if speed_match:
                            speed = speed_match.group(1)
                            unit = speed_match.group(2)
                            self.current_pwd_signal.emit(f"GPU破解速度: {speed} {unit}")
                    
                    # 更新GPU利用率信息（如果有）
                    if "Util:" in line:
                        util_match = re.search(r'Util:\s*(\d+)%', line)
                        if util_match:
                            util = util_match.group(1)
                            self.current_pwd_signal.emit(f"GPU利用率: {util}%")
                    
                    # 检查是否找到密码
                    if "Recovered" in line and ":" in line and "0/1 (0.00%)" not in line:
                        self.current_pwd_signal.emit("已找到密码！正在验证...")
                        # 尝试从输出中提取密码
                        password_match = re.search(r':\s*(.+?)$', line)
                        if password_match:
                            found_password = password_match.group(1).strip()
                        
                        # 如果找到了密码，结束循环
                        if found_password:
                            break
            
            # 创建读取stderr的线程，可能包含更多调试信息
            def read_stderr():
                for line in hashcat_process.stderr:
                    if self.isInterruptionRequested():
                        break
                    
                    # 记录错误信息
                    logger.debug(f"Hashcat stderr: {line.strip()}")
                    
                    # 如果包含重要信息，也更新UI
                    if "CUDA" in line or "OpenCL" in line or "Error" in line:
                        self.current_pwd_signal.emit(f"GPU信息: {line.strip()}")
            
            # 启动输出读取线程
            output_thread = threading.Thread(target=read_output)
            output_thread.daemon = True
            output_thread.start()
            
            # 启动错误读取线程
            stderr_thread = threading.Thread(target=read_stderr)
            stderr_thread.daemon = True
            stderr_thread.start()
            
            # 等待hashcat进程完成或用户中断
            start_time = time.time()
            while hashcat_process.poll() is None:
                if self.isInterruptionRequested():
                    hashcat_process.terminate()
                    self.okSignal.emit((False, "用户终止了破解过程"))
                    return
                
                # 检查是否超时
                if time.time() - start_time > 300:  # 5分钟超时
                    self.current_pwd_signal.emit("GPU破解超时，尝试读取结果...")
                    break
                
                time.sleep(0.5)
            
            # 等待输出线程结束
            output_thread.join(timeout=2)
            stderr_thread.join(timeout=2)
            
            # 检查破解结果
            return_code = hashcat_process.poll() or 0
            stdout, stderr = hashcat_process.communicate()
            
            # 查找密码
            password = None
            
            # 在输出中查找密码
            potfile_path = os.path.join(temp_dir, "hashcat.potfile")
            if os.path.exists(potfile_path):
                with open(potfile_path, 'r') as f:
                    potfile_content = f.read()
                    if ":" in potfile_content:
                        password = potfile_content.split(":", 1)[1].strip()
            
            # 如果没有找到密码，尝试从stdout中解析
            if not password and stdout:
                password_match = re.search(r'Hash\.Target\s*:\s*.*:(.*?)$', stdout, re.MULTILINE)
                if password_match:
                    password = password_match.group(1).strip()
            
            if not password:
                # 尝试从结果目录查找
                cracked_files = [f for f in os.listdir(temp_dir) if f.endswith('.cracked')]
                for cracked_file in cracked_files:
                    with open(os.path.join(temp_dir, cracked_file), 'r') as f:
                        content = f.read().strip()
                        if content:
                            password_parts = content.split(':')
                            if len(password_parts) > 1:
                                password = password_parts[-1].strip()
                                break
            
            # 如果找到了密码，验证并保存解密后的PDF
            if password:
                try:
                    # 验证密码
                    self.current_pwd_signal.emit(f"验证密码: {password}")
                    with fitz.open(self.input_file.file_path) as pdf:
                        if pdf.authenticate(password):
                            # 保存解密后的PDF
                            pdf.save(self.output_path)
                            self.progressSignal.emit(100)
                            success_message = f"{os.path.dirname(self.output_path)}\n成功破解密码: {password}"
                            self.okSignal.emit((True, success_message))
                            return
                except Exception as e:
                    logger.error(f"验证密码失败: {str(e)}")
            
            # 如果GPU破解失败，尝试回退到CPU方法
            self.current_pwd_signal.emit("GPU破解未找到密码，切换到CPU方法...")
            
            if self.crack_settings.get("mode") == "dictionary":
                return self.run_dict_crack()
            else:
                return self.run_bruteforce_crack()
            
        except Exception as e:
            logger.error(f"GPU破解出错: {str(e)}")
            self.okSignal.emit((False, f"GPU破解失败: {str(e)}"))
            return
    
    def run_dict_crack(self):
        """使用字典破解密码 - 多线程版本"""
        dict_path = self.crack_settings.get("dict_path", "")
        if not os.path.exists(dict_path):
            self.okSignal.emit((False, "字典文件不存在"))
            return
            
        try:
            logger.info(f"使用字典文件多线程破解: {dict_path}")
            # 获取线程数
            thread_count = self.crack_settings.get("threads", 4)
            logger.info(f"使用 {thread_count} 个线程进行字典破解")
            
            # 读取字典文件中的密码列表
            passwords = []
            with open(dict_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    pwd = line.strip()
                    if pwd:  # 跳过空行
                        passwords.append(pwd)
            
            if not passwords:
                self.okSignal.emit((False, "字典文件为空或格式不正确"))
                return
                
            total_passwords = len(passwords)
            logger.info(f"字典中共有 {total_passwords} 个密码")
            self.current_pwd_signal.emit(f"正在使用 {thread_count} 个线程破解字典中的 {total_passwords} 个密码...")
            
            # 创建一个用于状态同步的对象
            class CrackState:
                def __init__(self):
                    self.success = False
                    self.found_password = None
                    self.processed_count = 0
                    self.lock = threading.Lock()
                    
            crack_state = CrackState()
            
            # 定义测试密码的函数
            def test_password(pwd):
                if crack_state.success:
                    return  # 如果已经成功，就不再测试
                
                try:
                    with fitz.open(self.input_file.file_path) as pdf:
                        if pdf.authenticate(pwd):
                            with crack_state.lock:
                                if not crack_state.success:  # 双重检查
                                    crack_state.success = True
                                    crack_state.found_password = pwd
                                    logger.info(f"字典破解成功，密码: {pwd}")
                except Exception as e:
                    logger.debug(f"尝试密码 '{pwd}' 失败: {str(e)}")
                
                # 更新处理计数
                with crack_state.lock:
                    crack_state.processed_count += 1
                    progress = int(crack_state.processed_count / total_passwords * 60) + 30
                    self.progressSignal.emit(min(progress, 90))
                    
                    # 每处理100个密码更新一次UI
                    if crack_state.processed_count % 100 == 0 or crack_state.processed_count == total_passwords:
                        percentage = int(crack_state.processed_count / total_passwords * 100)
                        self.current_pwd_signal.emit(f"字典破解: 已尝试 {crack_state.processed_count}/{total_passwords} 个密码 ({percentage}%)")
            
            # 创建线程池
            with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
                # 提交任务
                futures = []
                for pwd in passwords:
                    if self.isInterruptionRequested():
                        break
                    futures.append(executor.submit(test_password, pwd))
                
                # 等待任务完成
                for future in concurrent.futures.as_completed(futures):
                    if self.isInterruptionRequested() or crack_state.success:
                        # 如果破解成功或用户请求终止，取消所有未完成的任务
                        for f in futures:
                            f.cancel()
                        break
                    
                    # 获取任务结果（可能产生异常）
                    try:
                        future.result()
                    except Exception as e:
                        logger.error(f"字典破解线程出错: {str(e)}")
            
            # 检查是否成功
            if crack_state.success and crack_state.found_password:
                # 保存解密后的PDF
                with fitz.open(self.input_file.file_path) as pdf:
                    pdf.authenticate(crack_state.found_password)
                    pdf.save(self.output_path)
                
                self.progressSignal.emit(100)
                success_message = f"{os.path.dirname(self.output_path)}\n成功使用密码: {crack_state.found_password}"
                self.okSignal.emit((True, success_message))
                return
            
            # 如果被终止
            if self.isInterruptionRequested():
                logger.info("字典破解过程被用户终止")
                self.okSignal.emit((False, "用户终止了破解过程"))
                return
                
            # 所有密码都尝试过了，但没有成功
            logger.info("字典中所有密码尝试均失败")
            self.okSignal.emit((False, "字典中所有密码尝试均失败，请尝试其他解密方法"))
            
        except Exception as e:
            logger.error(f"字典破解出错: {str(e)}")
            self.okSignal.emit((False, f"字典破解失败: {str(e)}"))
    
    def run_bruteforce_crack(self):
        """使用暴力破解方式 - 多线程版本"""
        min_len = self.crack_settings.get("min_length", 4)
        max_len = self.crack_settings.get("max_length", 8)
        charset = self.crack_settings.get("charset", "digits")
        thread_count = self.crack_settings.get("threads", 4)
        
        logger.info(f"使用 {thread_count} 个线程进行暴力破解")
        
        # 定义字符集
        charset_chars = ""
        if charset == "digits":
            charset_chars = "0123456789"
        elif charset == "lowercase":
            charset_chars = "abcdefghijklmnopqrstuvwxyz"
        elif charset == "uppercase":
            charset_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        elif charset == "alphanumeric":
            charset_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        else:  # all
            charset_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-=[]{}|;:,.<>?/"
        
        logger.info(f"开始多线程暴力破解，字符集: {charset}, 长度范围: {min_len}-{max_len}")
        
        import itertools
        
        # 创建一个用于状态同步的对象
        class CrackState:
            def __init__(self):
                self.success = False
                self.found_password = None
                self.current_length = min_len
                self.current_count = 0
                self.total_combinations = 0
                self.lock = threading.Lock()
                
        crack_state = CrackState()
        
        # 定义密码检查函数
        def check_password(pwd):
            if crack_state.success:
                return  # 如果已经成功，就不再测试
                
            try:
                with fitz.open(self.input_file.file_path) as pdf:
                    if pdf.authenticate(pwd):
                        with crack_state.lock:
                            if not crack_state.success:  # 双重检查
                                crack_state.success = True
                                crack_state.found_password = pwd
                                logger.info(f"暴力破解成功，密码: {pwd}")
            except Exception as e:
                logger.debug(f"尝试密码 '{pwd}' 失败: {str(e)}")
                
            # 更新处理计数
            with crack_state.lock:
                crack_state.current_count += 1
                
                # 每处理1000个密码或每0.5秒更新一次进度
                if crack_state.current_count % 1000 == 0:
                    percent = (crack_state.current_count / crack_state.total_combinations * 100) 
                    if crack_state.total_combinations > 0:
                        length_progress = (crack_state.current_length - min_len) / (max_len - min_len + 1)
                        total_progress = 30 + min(60 * (length_progress + percent / 100 / (max_len - min_len + 1)), 60)
                        self.progressSignal.emit(min(int(total_progress), 90))
                    
                    self.current_pwd_signal.emit(
                        f"暴力破解(长度{crack_state.current_length}): {pwd} "
                        f"({crack_state.current_count}/{crack_state.total_combinations}, "
                        f"{thread_count}线程)"
                    )
        
        # 按照密码长度逐一尝试
        for length in range(min_len, max_len + 1):
            if self.isInterruptionRequested() or crack_state.success:
                break
                
            crack_state.current_length = length
            crack_state.current_count = 0
            crack_state.total_combinations = len(charset_chars) ** length
                
            logger.info(f"尝试长度为 {length} 的密码，组合总数: {crack_state.total_combinations}")
            self.current_pwd_signal.emit(f"准备破解长度: {length}，组合总数: {crack_state.total_combinations}...")
            
            # 如果组合数太多，警告用户
            if crack_state.total_combinations > 10000000:  # 1千万
                logger.warning(f"长度 {length} 的组合数超过1千万，可能需要很长时间")
                self.current_pwd_signal.emit(f"警告: 长度 {length} 的组合数很大，破解可能需要很长时间!")
            
            # 分批生成密码并多线程处理
            # 计算合适的批次大小
            batch_size = min(10000, max(1000, crack_state.total_combinations // (thread_count * 10)))
            
            # 创建密码队列
            password_queue = queue.Queue(maxsize=batch_size * 2)  # 队列大小为批次大小的两倍
            
            # 生产者线程 - 生成密码并放入队列
            def password_producer():
                for pwd_tuple in itertools.product(charset_chars, repeat=length):
                    if self.isInterruptionRequested() or crack_state.success:
                        break
                    pwd = ''.join(pwd_tuple)
                    password_queue.put(pwd)
                # 添加结束标记
                for _ in range(thread_count):
                    password_queue.put(None)
            
            # 启动生产者线程
            producer_thread = threading.Thread(target=password_producer)
            producer_thread.daemon = True
            producer_thread.start()
            
            # 消费者函数 - 从队列中获取密码并检查
            def password_consumer():
                while not self.isInterruptionRequested() and not crack_state.success:
                    pwd = password_queue.get()
                    if pwd is None:  # 结束标记
                        break
                    check_password(pwd)
                    password_queue.task_done()
            
            # 启动消费者线程
            consumer_threads = []
            for _ in range(thread_count):
                t = threading.Thread(target=password_consumer)
                t.daemon = True
                t.start()
                consumer_threads.append(t)
            
            # 等待所有密码处理完成或找到密码
            for t in consumer_threads:
                t.join()
            
            # 如果已经找到密码或用户要求终止，就退出循环
            if crack_state.success or self.isInterruptionRequested():
                break
        
        # 检查最终结果
        if crack_state.success and crack_state.found_password:
            # 保存解密后的PDF
            with fitz.open(self.input_file.file_path) as pdf:
                pdf.authenticate(crack_state.found_password)
                pdf.save(self.output_path)
            
            self.progressSignal.emit(100)
            success_message = f"{os.path.dirname(self.output_path)}\n成功破解密码: {crack_state.found_password}"
            self.okSignal.emit((True, success_message))
            return
        
        # 如果被终止
        if self.isInterruptionRequested():
            logger.info("暴力破解过程被用户终止")
            self.okSignal.emit((False, "用户终止了破解过程"))
            return
        
        # 所有组合都尝试过了，但没有成功
        logger.info("暴力破解尝试所有可能的密码组合均失败")
        self.okSignal.emit((False, "所有可能的密码组合尝试均失败，请使用其他方法"))
    
    def run_normal_decrypt(self):
        try:
            # 打开输入PDF
            pdf_document = fitz.open(self.input_file.file_path)
            
            # 如果PDF不是加密的，直接返回错误
            if not pdf_document.is_encrypted:
                pdf_document.close()
                self.okSignal.emit((False, "PDF文件未加密，无需解密"))
                return
            
            # 设置进度信号
            self.progressSignal.emit(30)
            
            # 尝试使用所有者密码解密
            auth_success = False
            error_message = "解密失败: 密码错误或权限不足"
            
            if self.owner_password:
                try:
                    auth_success = pdf_document.authenticate(self.owner_password)
                except Exception as e:
                    logger.error(f"使用所有者密码解密失败: {str(e)}")
            
            # 如果所有者密码解密失败，尝试使用用户密码
            if not auth_success and self.user_password:
                try:
                    auth_success = pdf_document.authenticate(self.user_password)
                except Exception as e:
                    logger.error(f"使用用户密码解密失败: {str(e)}")
            
            if not auth_success:
                pdf_document.close()
                self.okSignal.emit((False, error_message))
                return
            
            # 确认是否已获取足够权限
            if not pdf_document.metadata:
                pdf_document.close()
                self.okSignal.emit((False, "密码正确，但权限不足，无法解密"))
                return
            
            # 设置进度信号
            self.progressSignal.emit(60)
            
            # 保存为无加密的副本
            pdf_document.save(self.output_path)
            
            self.progressSignal.emit(100)
            pdf_document.close()
            
            # 记录成功使用的密码
            password_used = self.owner_password if auth_success else self.user_password
            success_message = os.path.dirname(self.output_path)
            if password_used:
                success_message += f"\n使用密码: {password_used} 成功解密"
            
            self.okSignal.emit((True, success_message))
            
        except Exception as e:
            logger.error(f"PDF解密错误: {str(e)}")
            self.okSignal.emit((False, str(e)))


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys
    from PySide6.QtGui import QFont
    
    app = QApplication(sys.argv)
    font = QFont('微软雅黑', 10)
    app.setFont(font)
    router = Router(None)
    view = DecryptControl(router)
    view.show()
    sys.exit(app.exec()) 