# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'blank_pages_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import resource_rc


class Ui_blank_pages_view(object):
    def setupUi(self, blank_pages_view):
        if not blank_pages_view.objectName():
            blank_pages_view.setObjectName(u"blank_pages_view")
        blank_pages_view.resize(800, 600)
        self.verticalLayout = QVBoxLayout(blank_pages_view)
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        # 文件选择区域
        self.horizontalLayout_file = QHBoxLayout()
        self.horizontalLayout_file.setObjectName(u"horizontalLayout_file")
        self.label_file = QLabel(blank_pages_view)
        self.label_file.setObjectName(u"label_file")
        self.horizontalLayout_file.addWidget(self.label_file)
        self.lineEdit_pdf_path = QLineEdit(blank_pages_view)
        self.lineEdit_pdf_path.setObjectName(u"lineEdit_pdf_path")
        self.lineEdit_pdf_path.setReadOnly(True)
        self.horizontalLayout_file.addWidget(self.lineEdit_pdf_path)
        self.btn_choose_file = QPushButton(blank_pages_view)
        self.btn_choose_file.setObjectName(u"btn_choose_file")
        self.horizontalLayout_file.addWidget(self.btn_choose_file)
        self.verticalLayout.addLayout(self.horizontalLayout_file)
        
        # 批量处理区域
        self.groupBox_batch = QGroupBox(blank_pages_view)
        self.groupBox_batch.setObjectName(u"groupBox_batch")
        self.verticalLayout_batch = QVBoxLayout(self.groupBox_batch)
        self.verticalLayout_batch.setObjectName(u"verticalLayout_batch")
        
        # 文件列表
        self.listWidget_files = QListWidget(self.groupBox_batch)
        self.listWidget_files.setObjectName(u"listWidget_files")
        self.verticalLayout_batch.addWidget(self.listWidget_files)
        
        # 文件操作按钮
        self.horizontalLayout_batch_btns = QHBoxLayout()
        self.horizontalLayout_batch_btns.setObjectName(u"horizontalLayout_batch_btns")
        
        self.btn_add_files = QPushButton(self.groupBox_batch)
        self.btn_add_files.setObjectName(u"btn_add_files")
        self.horizontalLayout_batch_btns.addWidget(self.btn_add_files)
        
        self.btn_remove_file = QPushButton(self.groupBox_batch)
        self.btn_remove_file.setObjectName(u"btn_remove_file")
        self.horizontalLayout_batch_btns.addWidget(self.btn_remove_file)
        
        self.btn_clear_files = QPushButton(self.groupBox_batch)
        self.btn_clear_files.setObjectName(u"btn_clear_files")
        self.horizontalLayout_batch_btns.addWidget(self.btn_clear_files)
        
        self.verticalLayout_batch.addLayout(self.horizontalLayout_batch_btns)
        self.verticalLayout.addWidget(self.groupBox_batch)
        
        # 预览区域
        self.groupBox_preview = QGroupBox(blank_pages_view)
        self.groupBox_preview.setObjectName(u"groupBox_preview")
        self.verticalLayout_preview = QVBoxLayout(self.groupBox_preview)
        self.verticalLayout_preview.setObjectName(u"verticalLayout_preview")
        
        # 空白页列表
        self.listWidget_blank_pages = QListWidget(self.groupBox_preview)
        self.listWidget_blank_pages.setObjectName(u"listWidget_blank_pages")
        self.verticalLayout_preview.addWidget(self.listWidget_blank_pages)
        
        # 预览按钮
        self.horizontalLayout_preview_btn = QHBoxLayout()
        self.horizontalLayout_preview_btn.setObjectName(u"horizontalLayout_preview_btn")
        
        self.horizontalSpacer_preview = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_preview_btn.addItem(self.horizontalSpacer_preview)
        
        self.btn_preview = QPushButton(self.groupBox_preview)
        self.btn_preview.setObjectName(u"btn_preview")
        self.horizontalLayout_preview_btn.addWidget(self.btn_preview)
        
        self.verticalLayout_preview.addLayout(self.horizontalLayout_preview_btn)
        self.verticalLayout.addWidget(self.groupBox_preview)
        
        # 输出选项区域
        self.groupBox_output = QGroupBox(blank_pages_view)
        self.groupBox_output.setObjectName(u"groupBox_output")
        self.verticalLayout_output = QVBoxLayout(self.groupBox_output)
        self.verticalLayout_output.setObjectName(u"verticalLayout_output")
        
        # 输出目录选择
        self.horizontalLayout_output_dir = QHBoxLayout()
        self.horizontalLayout_output_dir.setObjectName(u"horizontalLayout_output_dir")
        
        self.label_output_dir_type = QLabel(self.groupBox_output)
        self.label_output_dir_type.setObjectName(u"label_output_dir_type")
        self.horizontalLayout_output_dir.addWidget(self.label_output_dir_type)
        
        self.comboBox_output_dir = QComboBox(self.groupBox_output)
        self.comboBox_output_dir.addItem("")
        self.comboBox_output_dir.addItem("")
        self.comboBox_output_dir.setObjectName(u"comboBox_output_dir")
        self.horizontalLayout_output_dir.addWidget(self.comboBox_output_dir)
        
        self.horizontalSpacer_output = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_output_dir.addItem(self.horizontalSpacer_output)
        
        self.label_output_dir = QLabel(self.groupBox_output)
        self.label_output_dir.setObjectName(u"label_output_dir")
        self.horizontalLayout_output_dir.addWidget(self.label_output_dir)
        
        self.btn_choose_output_dir = QPushButton(self.groupBox_output)
        self.btn_choose_output_dir.setObjectName(u"btn_choose_output_dir")
        self.horizontalLayout_output_dir.addWidget(self.btn_choose_output_dir)
        
        self.verticalLayout_output.addLayout(self.horizontalLayout_output_dir)
        
        # 输出文件名后缀
        self.horizontalLayout_suffix = QHBoxLayout()
        self.horizontalLayout_suffix.setObjectName(u"horizontalLayout_suffix")
        
        self.label_suffix = QLabel(self.groupBox_output)
        self.label_suffix.setObjectName(u"label_suffix")
        self.horizontalLayout_suffix.addWidget(self.label_suffix)
        
        self.lineEdit_suffix = QLineEdit(self.groupBox_output)
        self.lineEdit_suffix.setObjectName(u"lineEdit_suffix")
        self.horizontalLayout_suffix.addWidget(self.lineEdit_suffix)
        
        self.checkBox_backup = QCheckBox(self.groupBox_output)
        self.checkBox_backup.setObjectName(u"checkBox_backup")
        self.horizontalLayout_suffix.addWidget(self.checkBox_backup)
        
        self.verticalLayout_output.addLayout(self.horizontalLayout_suffix)
        self.verticalLayout.addWidget(self.groupBox_output)
        
        # 进度条和处理按钮
        self.progressBar = QProgressBar(blank_pages_view)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.verticalLayout.addWidget(self.progressBar)
        
        self.horizontalLayout_process = QHBoxLayout()
        self.horizontalLayout_process.setObjectName(u"horizontalLayout_process")
        
        self.horizontalSpacer_process = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_process.addItem(self.horizontalSpacer_process)
        
        self.btn_process = QPushButton(blank_pages_view)
        self.btn_process.setObjectName(u"btn_process")
        self.btn_process.setMinimumSize(QSize(150, 40))
        self.horizontalLayout_process.addWidget(self.btn_process)
        
        self.verticalLayout.addLayout(self.horizontalLayout_process)

        self.retranslateUi(blank_pages_view)

        QMetaObject.connectSlotsByName(blank_pages_view)
    # setupUi

    def retranslateUi(self, blank_pages_view):
        blank_pages_view.setWindowTitle(QCoreApplication.translate("blank_pages_view", u"删除空白页", None))
        self.label_file.setText(QCoreApplication.translate("blank_pages_view", u"PDF文件:", None))
        self.btn_choose_file.setText(QCoreApplication.translate("blank_pages_view", u"选择PDF", None))
        self.groupBox_batch.setTitle(QCoreApplication.translate("blank_pages_view", u"批量处理", None))
        self.btn_add_files.setText(QCoreApplication.translate("blank_pages_view", u"添加文件", None))
        self.btn_remove_file.setText(QCoreApplication.translate("blank_pages_view", u"移除文件", None))
        self.btn_clear_files.setText(QCoreApplication.translate("blank_pages_view", u"清空列表", None))
        self.groupBox_preview.setTitle(QCoreApplication.translate("blank_pages_view", u"检测到的空白页", None))
        self.btn_preview.setText(QCoreApplication.translate("blank_pages_view", u"预览所有空白页", None))
        self.groupBox_output.setTitle(QCoreApplication.translate("blank_pages_view", u"输出选项", None))
        self.label_output_dir_type.setText(QCoreApplication.translate("blank_pages_view", u"输出位置:", None))
        self.comboBox_output_dir.setItemText(0, QCoreApplication.translate("blank_pages_view", u"PDF相同目录", None))
        self.comboBox_output_dir.setItemText(1, QCoreApplication.translate("blank_pages_view", u"自定义目录", None))
        self.label_output_dir.setText(QCoreApplication.translate("blank_pages_view", u"指定目录", None))
        self.btn_choose_output_dir.setText(QCoreApplication.translate("blank_pages_view", u"选择", None))
        self.label_suffix.setText(QCoreApplication.translate("blank_pages_view", u"文件名后缀:", None))
        self.checkBox_backup.setText(QCoreApplication.translate("blank_pages_view", u"创建备份", None))
        self.btn_process.setText(QCoreApplication.translate("blank_pages_view", u"删除空白页", None))
    # retranslateUi 