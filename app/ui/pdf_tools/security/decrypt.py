import os.path
import io
import subprocess
import tempfile
import threading
import time

import fitz
from PyPDF2 import PdfReader, PdfWriter
from PySide6.QtCore import Signal, QThread, QUrl, Qt, QFile, QIODevice, QTextStream
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon, QFont, QFontMetrics
from PySide6.QtWidgets import (QWidget, QMessageBox, QFileDialog, QRadioButton, 
                              QButtonGroup, QHBoxLayout, QLabel, QCheckBox, 
                              QProgressDialog, QDialog, QVBoxLayout, QPushButton,
                              QLineEdit, QComboBox)

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
            "timeout": 0         # 超时时间(秒)，0表示不限制
        }
        
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
        dialog.setMinimumWidth(400)
        
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
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("确定")
        cancel_btn = QPushButton("取消")
        
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        
        # 连接按钮事件
        ok_btn.clicked.connect(lambda: self.save_crack_settings(
            mode_combo.currentIndex() == 0,
            dict_path.text(),
            min_length.text(),
            max_length.text(),
            charset_combo.currentIndex(),
            "0",  # 总是传递0作为超时时间
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
        
        update_ui()
        mode_combo.currentIndexChanged.connect(update_ui)
        
        dialog.exec_()
    
    def select_dict_file(self, line_edit):
        """选择字典文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择密码字典文件", "", "文本文件 (*.txt);;所有文件 (*)")
        if file_path:
            line_edit.setText(file_path)
    
    def save_crack_settings(self, is_dict_mode, dict_path, min_length, max_length, charset_index, timeout, dialog):
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
            
            if min_len < 1 or max_len < min_len:
                raise ValueError("无效的参数值")
        except ValueError:
            QMessageBox.warning(self, "警告", "请输入有效的数字")
            return
        
        # 保存设置
        charset_map = ["digits", "lowercase", "uppercase", "alphanumeric", "all"]
        self.crack_settings = {
            "mode": "dictionary" if is_dict_mode else "bruteforce",
            "dict_path": dict_path,
            "min_length": min_len,
            "max_length": max_len,
            "charset": charset_map[charset_index],
            "timeout": timeout_val  # 始终为0，表示不限制时间
        }
        
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
            
            # 如果是字典模式，直接使用字典文件尝试密码
            if self.crack_settings.get("mode") == "dictionary":
                dict_path = self.crack_settings.get("dict_path", "")
                if os.path.exists(dict_path):
                    try:
                        logger.info(f"使用字典文件直接尝试密码: {dict_path}")
                        total_lines = sum(1 for _ in open(dict_path, 'r', encoding='utf-8', errors='ignore'))
                        current_line = 0
                        
                        with open(dict_path, 'r', encoding='utf-8', errors='ignore') as dict_file:
                            for line in dict_file:
                                if self.isInterruptionRequested():
                                    logger.info("破解过程被用户终止")
                                    self.okSignal.emit((False, "用户终止了破解过程"))
                                    return
                                    
                                pwd = line.strip()
                                if not pwd:  # 跳过空行
                                    continue
                                
                                # 更新当前尝试的密码
                                self.current_pwd_signal.emit(f"字典破解: {pwd}")
                                
                                # 更新进度
                                current_line += 1
                                progress = 30 + int(current_line / total_lines * 60)
                                self.progressSignal.emit(min(progress, 90))
                                
                                try:
                                    with fitz.open(self.input_file.file_path) as pdf:
                                        if pdf.authenticate(pwd):
                                            logger.info(f"使用字典中的密码'{pwd}'成功解密")
                                            
                                            # 保存解密后的PDF
                                            pdf.save(self.output_path)
                                            self.progressSignal.emit(100)
                                            success_message = f"{os.path.dirname(self.output_path)}\n成功使用密码: {pwd}"
                                            self.okSignal.emit((True, success_message))
                                            return
                                except Exception as e:
                                    # 这个密码尝试失败，继续下一个
                                    continue
                    except Exception as e:
                        logger.error(f"读取字典文件失败: {str(e)}")
            
            # 暴力破解模式 - 使用排列组合方式
            if self.crack_settings.get("mode") == "bruteforce":
                min_len = self.crack_settings.get("min_length", 4)
                max_len = self.crack_settings.get("max_length", 8)
                charset = self.crack_settings.get("charset", "digits")
                
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
                
                logger.info(f"开始暴力破解，字符集: {charset}, 长度范围: {min_len}-{max_len}")
                
                # 使用itertools实现高效的密码生成
                import itertools
                
                # 生成所有可能的密码长度
                for length in range(min_len, max_len + 1):
                    logger.info(f"尝试长度为 {length} 的密码")
                    self.current_pwd_signal.emit(f"准备破解长度: {length}")
                    
                    # 使用笛卡尔积生成指定长度的所有可能组合
                    total_combinations = len(charset_chars) ** length
                    logger.info(f"长度为 {length} 的可能组合数: {total_combinations}")
                    
                    # 显示预计时间
                    if length > 4 and charset != "digits":
                        self.current_pwd_signal.emit(f"长度: {length}, 组合数: {total_combinations}, 将耗时较长...")
                    
                    # 如果长度大于6，给出警告
                    if length > 6 and charset != "digits":
                        self.current_pwd_signal.emit(f"警告: 长度为 {length} 的破解可能非常耗时!")
                    
                    # 记录当前组合索引，用于进度计算
                    combination_count = 0
                    last_progress_update = time.time()
                    
                    # 逐个生成密码尝试
                    for pwd_tuple in itertools.product(charset_chars, repeat=length):
                        if self.isInterruptionRequested():
                            logger.info("破解过程被用户终止")
                            self.okSignal.emit((False, "用户终止了破解过程"))
                            return
                            
                        # 转换为字符串
                        pwd = ''.join(pwd_tuple)
                        
                        # 更新计数
                        combination_count += 1
                        
                        # 每1000次更新一次进度和当前密码显示
                        if combination_count % 1000 == 0 or time.time() - last_progress_update > 0.5:
                            # 计算进度
                            progress_percent = (combination_count / total_combinations) * 100
                            # 总进度取决于当前长度相对于总长度范围的位置
                            total_progress = 30 + min(60 * (length - min_len + progress_percent/100) / (max_len - min_len + 1), 60)
                            self.progressSignal.emit(min(int(total_progress), 90))
                            
                            # 更新当前尝试的密码
                            self.current_pwd_signal.emit(f"暴力破解: {pwd} ({combination_count}/{total_combinations})")
                            last_progress_update = time.time()
                        
                        try:
                            with fitz.open(self.input_file.file_path) as pdf:
                                if pdf.authenticate(pwd):
                                    logger.info(f"破解成功，密码: {pwd}")
                                    pdf.save(self.output_path)
                                    self.progressSignal.emit(100)
                                    success_message = f"{os.path.dirname(self.output_path)}\n成功破解密码: {pwd}"
                                    self.okSignal.emit((True, success_message))
                                    return
                        except Exception as e:
                            # 忽略单个密码的错误，继续尝试
                            continue
                
            # 如果所有尝试都失败，返回未成功消息
            logger.info("所有密码尝试均失败")
            self.okSignal.emit((False, "未能破解密码，请尝试其他解密方法"))
            
        except Exception as e:
            logger.error(f"PDF破解错误: {str(e)}")
            self.okSignal.emit((False, f"PDF破解失败: {str(e)}"))
            return
    
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