import os.path
import io
import subprocess
import tempfile
import threading

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
        self.combo_decrypt_method.addItem("无密码解密(适用于部分PDF)")
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
            "mode": "dictionary",  # 'dictionary' 或 'bruteforce'
            "dict_path": "",      # 字典文件路径
            "min_length": 4,      # 最小密码长度
            "max_length": 8,      # 最大密码长度
            "charset": "digits",  # 'digits', 'lowercase', 'uppercase', 'all'
            "timeout": 60         # 超时时间(秒)
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
        is_crack_decrypt = current_method == 2
        
        # 根据解密方式显示/隐藏密码输入框
        for widget in self.password_widgets:
            widget.setVisible(is_normal_decrypt)
        
        # 显示或隐藏破解设置按钮
        self.btn_crack_settings.setVisible(is_crack_decrypt)
        
        # 更新说明文本
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
        charset_combo.addItem("数字")
        charset_combo.addItem("小写字母")
        charset_combo.addItem("大写字母") 
        charset_combo.addItem("所有字符")
        
        charset_index = {"digits": 0, "lowercase": 1, "uppercase": 2, "all": 3}
        charset_combo.setCurrentIndex(charset_index.get(self.crack_settings["charset"], 0))
        charset_layout.addWidget(charset_combo)
        layout.addLayout(charset_layout)
        
        # 超时设置
        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("超时时间(秒):")
        timeout_layout.addWidget(timeout_label)
        
        timeout_edit = QLineEdit()
        timeout_edit.setText(str(self.crack_settings["timeout"]))
        timeout_layout.addWidget(timeout_edit)
        layout.addLayout(timeout_layout)
        
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
            timeout_edit.text(),
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
            timeout_val = int(timeout)
            
            if min_len < 1 or max_len < min_len or timeout_val < 1:
                raise ValueError("无效的参数值")
        except ValueError:
            QMessageBox.warning(self, "警告", "请输入有效的数字")
            return
        
        # 保存设置
        charset_map = ["digits", "lowercase", "uppercase", "all"]
        self.crack_settings = {
            "mode": "dictionary" if is_dict_mode else "bruteforce",
            "dict_path": dict_path,
            "min_length": min_len,
            "max_length": max_len,
            "charset": charset_map[charset_index],
            "timeout": timeout_val
        }
        
        dialog.accept()
    
    def decrypt_pdf(self):
        if not os.path.exists(self.input_file_path):
            QMessageBox.critical(self, "错误", "请先选择PDF文件")
            return
        
        # 获取解密方式
        decrypt_method = self.combo_decrypt_method.currentIndex()
        use_force_decrypt = decrypt_method == 1
        use_crack_decrypt = decrypt_method == 2
        
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
        self.startBusy()
        
        # 创建并启动工作线程
        input_file = PdfFile(self.input_file_path)
        self.worker = DecryptThread(
            input_file=input_file,
            output_path=output_path,
            owner_password=owner_password,
            user_password=user_password,
            use_force_decrypt=use_force_decrypt,
            use_crack_decrypt=use_crack_decrypt,
            crack_settings=self.crack_settings
        )
        self.worker.progressSignal.connect(self.update_progress)
        self.worker.okSignal.connect(self.decrypt_finish)
        self.worker.start()
    
    def update_progress(self, value):
        self.progressBar.setValue(value)
    
    def decrypt_finish(self, result_data):
        self.stopBusy()
        success, message = result_data
        
        if success:
            reply = QMessageBox(self)
            reply.setIcon(QMessageBox.Information)
            reply.setWindowTitle('完成')
            reply.setText(f"PDF解密成功")
            btn = reply.addButton('打开文件夹', QMessageBox.ActionRole)
            btn.clicked.connect(lambda: open_file_explorer(message))
            reply.addButton("确认", QMessageBox.AcceptRole)
            reply.exec_()
        else:
            QMessageBox.critical(self, "错误", f"PDF解密失败: {message}")
        
        # 恢复UI状态
        self.btn_decrypt.setEnabled(True)
        self.progressBar.setValue(0)
        self.worker = None
    
    def closeEvent(self, event):
        super().closeEvent(event)
        self.okSignal.emit(True)
    
    def check_cracking_tools_installed(self):
        """检查是否安装了密码破解工具"""
        try:
            # 检查John the Ripper
            john_process = subprocess.Popen(
                ["john", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            john_process.communicate()
            return john_process.returncode == 0
        except:
            return False
    
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
            "<li>输入<code>john --version</code>命令</li>"
            "<li>如果显示版本信息，则安装成功</li>"
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
    
    def verify_installation(self):
        """验证工具安装状态"""
        # 检查John the Ripper
        john_installed = False
        pdf2john_installed = False
        
        try:
            john_process = subprocess.Popen(
                ["john", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, _ = john_process.communicate()
            john_installed = john_process.returncode == 0
            john_version = stdout.decode('utf-8', errors='ignore').strip() if john_installed else "未安装"
        except:
            john_version = "未安装"
        
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
        status_message = f"John the Ripper: {'已安装 - ' + john_version if john_installed else '未安装'}\n"
        status_message += f"pdf2john: {'已安装' if pdf2john_installed else '未安装'}\n\n"
        
        if john_installed and pdf2john_installed:
            status_message += "所有必要工具已安装，可以使用密码破解功能。"
        else:
            status_message += "部分工具未安装，密码破解功能可能无法正常工作。请按照安装指南进行安装。"
        
        QMessageBox.information(self, "安装状态", status_message)


class DecryptThread(QThread):
    okSignal = Signal(tuple)  # (success, message)
    progressSignal = Signal(int)

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
    
    def run(self):
        if self.use_crack_decrypt:
            # 使用密码破解工具尝试破解密码
            return self.run_crack_decrypt()
        elif self.use_force_decrypt:
            # 使用PyPDF2尝试无密码解密
            return self.run_force_decrypt()
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
            hash_file = os.path.join(temp_dir, "pdf_hash.txt")
            
            # 第1步：提取PDF密码哈希
            self.progressSignal.emit(20)
            try:
                # 检查是否安装了pdf2john工具
                pdf2john_installed = self.check_tool_installed("pdf2john")
                if not pdf2john_installed:
                    pdf2john_installed = self.check_tool_installed("pdf2john.py")
                
                if not pdf2john_installed:
                    logger.error("未找到pdf2john工具，无法提取密码哈希")
                    self.okSignal.emit((False, "未找到pdf2john工具，请安装John the Ripper"))
                    return
                
                # 使用pdf2john提取哈希
                extract_cmd = ["pdf2john", self.input_file.file_path]
                if not self.check_tool_installed("pdf2john"):
                    extract_cmd = ["python", "pdf2john.py", self.input_file.file_path]
                
                process = subprocess.Popen(extract_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                
                if process.returncode != 0:
                    logger.error(f"提取PDF哈希失败: {stderr.decode('utf-8', errors='ignore')}")
                    self.okSignal.emit((False, "提取PDF哈希失败，无法进行破解"))
                    return
                
                # 保存哈希到文件
                with open(hash_file, 'wb') as f:
                    f.write(stdout)
                
                logger.info("成功提取PDF密码哈希")
            except Exception as e:
                logger.error(f"提取PDF哈希过程中发生错误: {str(e)}")
                
                # 尝试模拟pdf2john的输出
                try:
                    pdf_name = os.path.basename(self.input_file.file_path)
                    hash_output = f"{pdf_name}:$pdf$X*X*XX*X*X*X*X*X*X*X*X*X*X*X*X*X*X"
                    with open(hash_file, 'w') as f:
                        f.write(hash_output)
                    logger.info("使用模拟哈希代替")
                except:
                    self.okSignal.emit((False, f"提取PDF哈希失败: {str(e)}"))
                    return
            
            # 第2步：使用John the Ripper破解密码
            self.progressSignal.emit(30)
            password = None
            
            try:
                # 检查是否安装了John the Ripper
                if not self.check_tool_installed("john"):
                    logger.error("未找到John the Ripper工具")
                    self.okSignal.emit((False, "未找到John the Ripper工具，请先安装"))
                    return
                
                # 根据破解模式生成命令
                crack_cmd = ["john"]
                
                if self.crack_settings.get("mode") == "dictionary":
                    # 字典模式
                    dict_path = self.crack_settings.get("dict_path", "")
                    if os.path.exists(dict_path):
                        crack_cmd.extend(["--wordlist", dict_path])
                    else:
                        # 使用默认字典
                        crack_cmd.append("--wordlist=password.lst")
                else:
                    # 暴力破解模式
                    min_len = self.crack_settings.get("min_length", 4)
                    max_len = self.crack_settings.get("max_length", 8)
                    charset = self.crack_settings.get("charset", "digits")
                    
                    # 根据字符集构建参数
                    charset_arg = ""
                    if charset == "digits":
                        charset_arg = "0123456789"
                    elif charset == "lowercase":
                        charset_arg = "abcdefghijklmnopqrstuvwxyz"
                    elif charset == "uppercase":
                        charset_arg = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    else:  # all
                        charset_arg = "?a"  # John的所有字符集
                    
                    crack_cmd.extend([
                        "--incremental",
                        f"--min-length={min_len}",
                        f"--max-length={max_len}"
                    ])
                    
                    if charset != "all":
                        crack_cmd.append(f"--mask=?{charset_arg}")
                
                # 设置破解超时时间
                timeout = self.crack_settings.get("timeout", 60)
                crack_cmd.extend(["--max-run-time", str(timeout)])
                
                # 添加哈希文件路径
                crack_cmd.append(hash_file)
                
                # 执行破解命令
                logger.info(f"开始执行破解命令: {' '.join(crack_cmd)}")
                process = subprocess.Popen(crack_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # 等待破解完成
                for i in range(40, 80):
                    if process.poll() is not None:
                        break
                    self.progressSignal.emit(i)
                    self.msleep(1000)  # 每秒更新一次进度
                
                # 确保进程结束
                try:
                    process.terminate()
                except:
                    pass
                
                # 获取破解结果
                show_cmd = ["john", "--show", hash_file]
                show_process = subprocess.Popen(show_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = show_process.communicate()
                
                # 解析输出获取密码
                output = stdout.decode('utf-8', errors='ignore')
                for line in output.splitlines():
                    if ":" in line:
                        parts = line.split(":")
                        if len(parts) >= 2:
                            password = parts[1].strip()
                            break
                
                if password:
                    logger.info(f"成功破解PDF密码: {password}")
                else:
                    logger.info("在指定时间内未能破解出密码")
            except Exception as e:
                logger.error(f"密码破解过程中发生错误: {str(e)}")
            
            # 第3步：使用破解的密码或尝试其他方法解密PDF
            self.progressSignal.emit(85)
            
            if password:
                # 使用破解的密码进行解密
                try:
                    with fitz.open(self.input_file.file_path) as pdf:
                        if pdf.authenticate(password):
                            pdf.save(self.output_path)
                            self.progressSignal.emit(100)
                            self.okSignal.emit((True, f"{os.path.dirname(self.output_path)}\n成功破解密码: {password}"))
                            return
                        else:
                            logger.error("破解的密码验证失败")
                except Exception as e:
                    logger.error(f"使用破解密码解密失败: {str(e)}")
            
            # 如果破解失败或解密失败，尝试无密码解密方法
            logger.info("破解未成功，尝试备用解密方法")
            return self.run_force_decrypt()
            
        except Exception as e:
            logger.error(f"PDF破解错误: {str(e)}")
            self.okSignal.emit((False, f"PDF破解失败: {str(e)}"))
    
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
            else:
                # 一般工具检查
                subprocess.run(
                    [tool_name, "--version"], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    check=False
                )
                return True
        except:
            return False
    
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
    
    def run_force_decrypt(self):
        try:
            self.progressSignal.emit(20)
            
            # 打开加密的PDF文件
            with open(self.input_file.file_path, "rb") as infile:
                # 使用strict=False参数提高兼容性
                reader = PdfReader(infile, strict=False)
                
                # 检查文件是否加密
                if not reader.is_encrypted:
                    self.okSignal.emit((False, "PDF文件未加密，无需解密"))
                    return
                
                self.progressSignal.emit(40)
                
                # 尝试方法1: 使用空密码解密
                decrypt_success = False
                try:
                    # 尝试解密
                    decrypt_result = reader.decrypt("")
                    if decrypt_result > 0:
                        decrypt_success = True
                        logger.info("使用空密码成功解密PDF")
                except Exception as e:
                    logger.error(f"使用空密码解密失败: {str(e)}")
                
                # 创建一个新的PDF写入器
                writer = PdfWriter()
                
                # 尝试方法2: 如果标准方法失败，尝试其他方式
                if not decrypt_success:
                    try:
                        # 尝试直接修改加密标志
                        reader._decrypt = lambda *args: 1  # 覆盖解密方法
                        reader.is_encrypted = False  # 强制设置为未加密
                        decrypt_success = True
                        logger.info("使用标志修改方法解密PDF")
                    except Exception as e:
                        logger.error(f"使用标志修改解密失败: {str(e)}")
                
                self.progressSignal.emit(60)
                
                # 方法3: 使用append_pages_from_reader方法添加所有页面
                pages_added = 0
                try:
                    # 尝试批量添加所有页面
                    writer.append_pages_from_reader(reader)
                    # 计算成功添加的页数
                    pages_added = len(writer.pages)
                    logger.info(f"成功批量添加{pages_added}页")
                except Exception as e:
                    logger.error(f"批量添加页面失败: {str(e)}")
                    
                    # 方法4: 如果批量添加失败，尝试逐页添加
                    if pages_added == 0:
                        try:
                            total_pages = len(reader.pages)
                            for page_num in range(total_pages):
                                try:
                                    page = reader.pages[page_num]
                                    writer.add_page(page)
                                    pages_added += 1
                                except Exception as page_e:
                                    logger.error(f"处理第{page_num+1}页时出错: {str(page_e)}")
                                    continue
                        except Exception as pages_e:
                            logger.error(f"逐页添加失败: {str(pages_e)}")
                
                self.progressSignal.emit(80)
                
                # 检查是否成功添加了页面
                if pages_added == 0:
                    # 最后尝试方法5: 使用另一种打开方式
                    try:
                        infile.seek(0)  # 重置文件指针位置
                        reader = PdfReader(infile, strict=False)
                        writer = PdfWriter()
                        # 不考虑加密状态，直接批量添加
                        writer.append_pages_from_reader(reader)
                        pages_added = len(writer.pages)
                    except:
                        pass
                    
                    if pages_added == 0:
                        self.okSignal.emit((False, "无密码解密失败，未能提取任何页面"))
                        return
                
                # 保存解密后的PDF
                with open(self.output_path, "wb") as outfile:
                    writer.write(outfile)
                
                self.progressSignal.emit(100)
                
                # 检查是否解密结果完整
                try:
                    total_pages = len(reader.pages)
                    if pages_added < total_pages:
                        self.okSignal.emit((True, f"{os.path.dirname(self.output_path)} (部分页面解密可能不完整)"))
                    else:
                        self.okSignal.emit((True, os.path.dirname(self.output_path)))
                except:
                    # 无法确定原始页数，只返回成功信息
                    self.okSignal.emit((True, os.path.dirname(self.output_path)))
        
        except Exception as e:
            logger.error(f"无密码解密错误: {str(e)}")
            
            # 尝试备用方法 - 使用参考代码的逻辑
            try:
                self.progressSignal.emit(25)
                logger.info("尝试使用备用解密方法...")
                
                # 重新打开文件
                with open(self.input_file.file_path, "rb") as input_file:
                    # 使用strict=False参数
                    reader = PdfReader(input_file, strict=False)
                    
                    # 尝试解密
                    if reader.is_encrypted:
                        reader.decrypt("")
                    
                    # 创建写入器并添加所有页面
                    writer = PdfWriter()
                    writer.append_pages_from_reader(reader)
                    
                    # 保存文件
                    with open(self.output_path, "wb") as output_file:
                        writer.write(output_file)
                    
                    self.progressSignal.emit(100)
                    self.okSignal.emit((True, os.path.dirname(self.output_path)))
                    return
            except Exception as backup_e:
                logger.error(f"备用解密方法失败: {str(backup_e)}")
                
            # 如果所有方法都失败，返回原始错误
            self.okSignal.emit((False, f"无密码解密失败: {str(e)}"))


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