import os.path
from typing import List

import fitz
from PySide6.QtCore import Signal, QThread, QUrl, Qt, QFile, QIODevice, QTextStream
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon, QFont, QFontMetrics
from PySide6.QtWidgets import (QWidget, QMessageBox, QFileDialog, QDialog, QPushButton, 
                              QVBoxLayout, QLabel, QDialogButtonBox, QListWidget, 
                              QListWidgetItem, QHBoxLayout, QFrame)

from app.model import PdfFile
from app.ui.components.QCursorGif import QCursorGif
from app.ui.Icon import Icon
from app.util import common
from app.ui.pdf_tools.security.encrypt_ui import Ui_encrypt_pdf_view
from app.ui.components.router import Router
from app.log import logger


def open_file_explorer(path):
    # 使用QDesktopServices打开文件管理器
    if os.path.isfile(path):
        path = os.path.dirname(path)
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))


class EncryptControl(QWidget, Ui_encrypt_pdf_view, QCursorGif):
    okSignal = Signal(bool)
    childRouterSignal = Signal(str)

    def __init__(self, router: Router, parent=None):
        super().__init__(parent)
        self.input_file_paths = []  # 改为存储多个文件路径
        self.output_dir = ""
        self.router = router
        self.router_path = (self.parent().router_path if self.parent() else '') + '/加密PDF'
        self.child_routes = {}
        self.worker = None
        self.setupUi(self)
        # 设置忙碌光标图片数组
        self.initCursor([':/icons/icons/Cursors/%d.png' %
                        i for i in range(8)], self)
        self.setCursorTimeout(100)
        self.init_ui()
        
        # 创建文件列表组件
        self.list_frame = QFrame(self)
        self.list_frame.setFrameShape(QFrame.StyledPanel)
        self.list_frame.setFrameShadow(QFrame.Raised)
        self.list_frame.setObjectName("list_frame")
        
        self.list_layout = QVBoxLayout(self.list_frame)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        
        self.list_label = QLabel("已选择的PDF文件:", self.list_frame)
        self.list_layout.addWidget(self.list_label)
        
        self.file_list = QListWidget(self.list_frame)
        self.file_list.setAlternatingRowColors(True)
        self.file_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.list_layout.addWidget(self.file_list)
        
        # 文件列表操作按钮
        self.list_buttons_layout = QHBoxLayout()
        self.btn_remove_selected = QPushButton("移除选中", self.list_frame)
        self.btn_remove_all = QPushButton("清空列表", self.list_frame)
        self.btn_remove_selected.clicked.connect(self.remove_selected_files)
        self.btn_remove_all.clicked.connect(self.clear_file_list)
        
        self.list_buttons_layout.addWidget(self.btn_remove_selected)
        self.list_buttons_layout.addWidget(self.btn_remove_all)
        self.list_layout.addLayout(self.list_buttons_layout)
        
        # 添加文件列表到主布局
        self.verticalLayout.insertWidget(1, self.list_frame)
        
        # 按钮连接
        self.btn_choose_file.setText("选择文件")
        self.btn_choose_file.clicked.connect(self.open_file_dialog)
        self.btn_choose_file.setIcon(Icon.Add_Icon)
        self.btn_encrypt.clicked.connect(self.encrypt_pdf)
        
        # 将说明标签替换为按钮
        self.label_pwd_info.hide()  # 隐藏原始标签
        self.btn_help = QPushButton("点击查看说明", self)
        self.btn_help.setStyleSheet("text-align: left; border: none; color: blue; text-decoration: underline;")
        self.btn_help.setCursor(Qt.PointingHandCursor)
        self.btn_help.clicked.connect(self.show_help_dialog)
        # 将按钮添加到原标签的位置
        self.verticalLayout.insertWidget(self.verticalLayout.indexOf(self.label_pwd_info), self.btn_help)
        
        # 帮助文本
        self.base_help_text = "说明：\n1. 用户密码：打开文档时需要输入的密码\n2. 所有者密码：修改文档权限或解密时需要的密码\n\n"
        self.config_help_text = "建议：可以只设置一种密码，也可以两种同时设置。如只需限制查看，仅设置用户密码即可；如只需限制编辑，仅设置所有者密码即可。"
        
        # 密码输入监听
        self.lineEdit_user_pwd.textChanged.connect(self.update_password_status)
        self.lineEdit_owner_pwd.textChanged.connect(self.update_password_status)
        
        # 输出选项连接
        self.comboBox_output_dir.activated.connect(self.select_output_dir)
        self.btn_choose_output_dir.clicked.connect(self.set_output_dir)
        
        # 初始界面设置
        self.label_output_dir.setVisible(False)
        self.btn_choose_output_dir.setVisible(False)
        self.btn_encrypt.setEnabled(False)
        
        # 隐藏单文件模式下的文件名设置
        self.label_filename.setVisible(False)
        self.lineEdit_filename.setVisible(False)
        
    def init_ui(self):
        self.btn_encrypt.setObjectName('border')
        if not self.parent():
            pixmap = QPixmap(Icon.logo_ico_path)
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)
            self.setWindowTitle('PDF加密')
            style_qss_file = QFile(":/data/resources/QSS/style.qss")
            if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(style_qss_file)
                style_content = stream.readAll()
                self.setStyleSheet(style_content)
                style_qss_file.close()
    
    def show_help_dialog(self):
        """显示密码设置说明对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("PDF加密设置说明")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # 添加基本说明
        help_text = self.base_help_text + self.config_help_text
        help_label = QLabel(help_text)
        help_label.setWordWrap(True)
        layout.addWidget(help_label)
        
        # 添加确定按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
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
    
    def remove_selected_files(self):
        """移除选中的文件"""
        for item in self.file_list.selectedItems():
            file_path = item.data(Qt.UserRole)
            self.file_list.takeItem(self.file_list.row(item))
            self.input_file_paths.remove(file_path)
        
        # 更新按钮状态
        self.btn_encrypt.setEnabled(len(self.input_file_paths) > 0)
    
    def clear_file_list(self):
        """清空文件列表"""
        self.file_list.clear()
        self.input_file_paths.clear()
        self.btn_encrypt.setEnabled(False)
    
    def open_file_dialog(self):
        # 打开文件对话框，选择多个PDF文件
        files, _ = QFileDialog.getOpenFileNames(self, "选择PDF文件", "", "PDF Files (*.pdf);;All Files (*)")
        if not files:
            return
        
        # 遍历所有选择的文件
        for file_path in files:
            # 检查文件是否已在列表中
            if file_path in self.input_file_paths:
                continue
                
            # 获取PDF信息
            try:
                with fitz.open(file_path) as pdf:
                    # 如果PDF已加密，提示用户但仍然添加
                    if pdf.is_encrypted:
                        QMessageBox.warning(self, "警告", f"文件 {os.path.basename(file_path)} 已加密，重新加密可能会导致无法打开。")
            except Exception as e:
                logger.error(f"读取PDF文件错误: {str(e)}")
                QMessageBox.warning(self, "警告", f"无法读取文件 {os.path.basename(file_path)}: {str(e)}")
                continue
            
            # 添加到文件列表
            self.input_file_paths.append(file_path)
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(Qt.UserRole, file_path)
            self.file_list.addItem(item)
        
        # 如果添加了文件，启用加密按钮
        if self.input_file_paths:
            self.btn_encrypt.setEnabled(True)
            
            # 如果未设置输出目录，默认使用与第一个PDF相同的目录
            if not self.output_dir and self.input_file_paths:
                self.output_dir = os.path.dirname(self.input_file_paths[0])
                font_metrics = QFontMetrics(self.label_output_dir.font())
                elided_text = font_metrics.elidedText(self.output_dir, Qt.ElideRight, self.label_output_dir.width() - 10)
                self.label_output_dir.setText(elided_text)
                self.label_output_dir.setToolTip(self.output_dir)
    
    def encrypt_pdf(self):
        if not self.input_file_paths:
            QMessageBox.critical(self, "错误", "请先选择PDF文件")
            return
        
        # 验证密码
        user_password = self.lineEdit_user_pwd.text()
        confirm_user_password = self.lineEdit_confirm_user_pwd.text()
        owner_password = self.lineEdit_owner_pwd.text()
        confirm_owner_password = self.lineEdit_confirm_owner_pwd.text()
        
        if user_password and user_password != confirm_user_password:
            QMessageBox.warning(self, "警告", "用户密码与确认密码不一致")
            return
            
        if owner_password and owner_password != confirm_owner_password:
            QMessageBox.warning(self, "警告", "所有者密码与确认密码不一致")
            return
            
        if not user_password and not owner_password:
            reply = QMessageBox.question(self, "提示", 
                "您没有设置任何密码，是否继续？\n\n" +
                "- 如需限制查看文档，请设置用户密码\n" +
                "- 如需限制编辑文档，请设置所有者密码",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        
        # 获取权限设置
        permissions = 0
        if self.checkBox_print.isChecked():
            permissions |= fitz.PDF_PERM_PRINT
        if self.checkBox_copy.isChecked():
            permissions |= fitz.PDF_PERM_COPY
        if self.checkBox_modify.isChecked():
            permissions |= fitz.PDF_PERM_MODIFY
        if self.checkBox_annotate.isChecked():
            permissions |= fitz.PDF_PERM_ANNOTATE
        
        # 确定加密方法
        encrypt_method = fitz.PDF_ENCRYPT_AES_128
        encrypt_method_text = self.comboBox_enc_level.currentText()
        if "128位RC4" in encrypt_method_text:
            encrypt_method = fitz.PDF_ENCRYPT_RC4_128
        elif "40位RC4" in encrypt_method_text:
            encrypt_method = fitz.PDF_ENCRYPT_RC4_40
        
        # 获取输出目录
        if self.comboBox_output_dir.currentText() == '自定义目录' and self.output_dir:
            output_directory = self.output_dir
        else:
            # 使用第一个文件的目录作为默认输出目录
            output_directory = os.path.dirname(self.input_file_paths[0])
        
        # 如果输出目录不存在，创建它
        if not os.path.exists(output_directory):
            try:
                os.makedirs(output_directory)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法创建输出目录: {str(e)}")
                return
        
        # 禁用按钮，开始任务
        self.btn_encrypt.setEnabled(False)
        self.startBusy()
        
        # 创建批量处理线程
        self.worker = BatchEncryptThread(
            input_files=self.input_file_paths,
            output_dir=output_directory,
            user_password=user_password,
            owner_password=owner_password,
            permissions=permissions,
            encrypt_method=encrypt_method
        )
        self.worker.progressSignal.connect(self.update_progress)
        self.worker.okSignal.connect(self.encrypt_finish)
        self.worker.start()
    
    def update_progress(self, value):
        self.progressBar.setValue(value)
    
    def encrypt_finish(self, result_data):
        self.stopBusy()
        success_count, failed_count, output_dir = result_data
        
        if success_count > 0:
            user_pwd = self.lineEdit_user_pwd.text()
            owner_pwd = self.lineEdit_owner_pwd.text()
            
            # 根据密码设置情况提供不同的提示
            success_text = f"成功加密 {success_count} 个文件"
            if failed_count > 0:
                success_text += f"，失败 {failed_count} 个"
                
            if user_pwd and owner_pwd:
                if user_pwd == owner_pwd:
                    success_text += f"\n\n密码: {user_pwd}\n(用户密码和所有者密码相同)"
                else:
                    success_text += f"\n\n用户密码: {user_pwd} (用于打开文档)\n所有者密码: {owner_pwd} (用于解除保护)"
            elif user_pwd:
                success_text += f"\n\n用户密码: {user_pwd} (用于打开文档)"
            elif owner_pwd:
                success_text += f"\n\n所有者密码: {owner_pwd} (用于解除保护和编辑)"
            else:
                success_text += "\n\n已设置权限控制，但未使用密码保护"
            
            reply = QMessageBox(self)
            reply.setIcon(QMessageBox.Information)
            reply.setWindowTitle('完成')
            reply.setText(success_text)
            btn = reply.addButton('打开文件夹', QMessageBox.ActionRole)
            btn.clicked.connect(lambda: open_file_explorer(output_dir))
            reply.addButton("确认", QMessageBox.AcceptRole)
            reply.exec_()
        else:
            QMessageBox.critical(self, "错误", f"PDF加密失败，所有文件均未能成功加密")
        
        # 恢复UI状态
        self.btn_encrypt.setEnabled(True)
        self.progressBar.setValue(0)
        self.worker = None
    
    def closeEvent(self, event):
        super().closeEvent(event)
        self.okSignal.emit(True)

    def update_password_status(self):
        """更新密码设置状态提示"""
        user_pwd = self.lineEdit_user_pwd.text()
        owner_pwd = self.lineEdit_owner_pwd.text()
        
        # 根据密码设置情况更新帮助文本
        if user_pwd and owner_pwd:
            if user_pwd == owner_pwd:
                self.config_help_text = "当前设置：两种密码相同，文档将受到完全保护，但管理不便。\n建议使用不同的密码以便分别控制查看和编辑权限。"
            else:
                self.config_help_text = "当前设置：两种密码都已设置，文档将受到完全保护。输入用户密码可阅读，输入所有者密码可编辑。"
        elif user_pwd:
            self.config_help_text = "当前设置：仅设置用户密码，他人需要密码才能打开文档，但有所有者权限的用户可以编辑。"
        elif owner_pwd:
            self.config_help_text = "当前设置：仅设置所有者密码，任何人都能查看，但需要密码才能编辑文档。"
        else:
            self.config_help_text = "建议：可以只设置一种密码，也可以两种同时设置。如只需限制查看，仅设置用户密码即可；如只需限制编辑，仅设置所有者密码即可。"


class BatchEncryptThread(QThread):
    okSignal = Signal(tuple)  # (success_count, failed_count, output_dir)
    progressSignal = Signal(int)

    def __init__(self, input_files: List[str], output_dir: str, user_password="", owner_password="", 
                 permissions=0, encrypt_method=fitz.PDF_ENCRYPT_AES_128):
        super().__init__()
        self.input_files = input_files
        self.output_dir = output_dir
        self.user_password = user_password
        self.owner_password = owner_password
        self.permissions = permissions
        self.encrypt_method = encrypt_method
    
    def run(self):
        success_count = 0
        failed_count = 0
        total_files = len(self.input_files)
        
        for index, file_path in enumerate(self.input_files):
            try:
                # 打开输入PDF
                pdf_document = fitz.open(file_path)
                
                # 如果PDF已加密，先尝试解密
                if pdf_document.is_encrypted:
                    try:
                        # 尝试用空密码解密，如果之前是无密码文档
                        pdf_document.authenticate("")
                    except:
                        pass
                
                # 生成输出文件名：原文件名+加密+文件.pdf
                filename = os.path.basename(file_path)
                filename_without_ext = os.path.splitext(filename)[0]
                output_filename = f"{filename_without_ext}_加密文件.pdf"
                output_path = os.path.join(self.output_dir, output_filename)
                output_path = common.usable_filepath(output_path)
                
                # 确保至少有一个密码
                if not self.owner_password and not self.user_password:
                    # 如果用户确认不使用密码，只使用权限控制
                    owner_pw = ""
                    user_pw = ""
                else:
                    # 将所有者密码设置为用户密码（如果未提供）
                    owner_pw = self.owner_password if self.owner_password else self.user_password
                    # 将用户密码设置为所有者密码（如果未提供）
                    user_pw = self.user_password if self.user_password else ""
                
                # 设置文档权限并保存
                pdf_document.save(
                    output_path,
                    encryption=self.encrypt_method,
                    owner_pw=owner_pw,
                    user_pw=user_pw,
                    permissions=self.permissions
                )
                
                pdf_document.close()
                success_count += 1
                
            except Exception as e:
                logger.error(f"PDF加密错误 {file_path}: {str(e)}")
                failed_count += 1
            
            # 更新进度
            progress = int((index + 1) / total_files * 100)
            self.progressSignal.emit(progress)
        
        self.okSignal.emit((success_count, failed_count, self.output_dir))


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys
    from PySide6.QtGui import QFont
    
    app = QApplication(sys.argv)
    font = QFont('微软雅黑', 10)
    app.setFont(font)
    router = Router(None)
    view = EncryptControl(router)
    view.show()
    sys.exit(app.exec()) 