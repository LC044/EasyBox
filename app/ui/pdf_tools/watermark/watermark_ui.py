# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'watermark_ui.ui'
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
    QLineEdit, QProgressBar, QPushButton, QSizePolicy, 
    QSlider, QSpacerItem, QSpinBox, QVBoxLayout, QWidget, QColorDialog)
import resource_rc

class Ui_watermark_view(object):
    def setupUi(self, watermark_view):
        if not watermark_view.objectName():
            watermark_view.setObjectName(u"watermark_view")
        watermark_view.resize(800, 700)
        watermark_view.setMinimumSize(QSize(800, 700))
        watermark_view.setStyleSheet(u"")
        
        self.verticalLayout = QVBoxLayout(watermark_view)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        # 标题
        self.label_title = QLabel(watermark_view)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_title.setFont(font)
        self.verticalLayout.addWidget(self.label_title)
        
        # 文件选择区域
        self.groupBox_files = QGroupBox(watermark_view)
        self.groupBox_files.setObjectName(u"groupBox_files")
        self.verticalLayout_files = QVBoxLayout(self.groupBox_files)
        self.verticalLayout_files.setObjectName(u"verticalLayout_files")
        
        # 单文件选择
        self.horizontalLayout_file = QHBoxLayout()
        self.horizontalLayout_file.setObjectName(u"horizontalLayout_file")
        self.label_file = QLabel(self.groupBox_files)
        self.label_file.setObjectName(u"label_file")
        self.horizontalLayout_file.addWidget(self.label_file)
        
        self.lineEdit_pdf_path = QLineEdit(self.groupBox_files)
        self.lineEdit_pdf_path.setObjectName(u"lineEdit_pdf_path")
        self.lineEdit_pdf_path.setReadOnly(True)
        self.horizontalLayout_file.addWidget(self.lineEdit_pdf_path)
        
        self.btn_choose_file = QPushButton(self.groupBox_files)
        self.btn_choose_file.setObjectName(u"btn_choose_file")
        self.horizontalLayout_file.addWidget(self.btn_choose_file)
        
        self.verticalLayout_files.addLayout(self.horizontalLayout_file)
        
        # 批量文件选择
        self.horizontalLayout_batch = QHBoxLayout()
        self.horizontalLayout_batch.setObjectName(u"horizontalLayout_batch")
        
        self.label_batch = QLabel(self.groupBox_files)
        self.label_batch.setObjectName(u"label_batch")
        self.horizontalLayout_batch.addWidget(self.label_batch)
        
        self.horizontalSpacer_batch = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_batch.addItem(self.horizontalSpacer_batch)
        
        self.btn_add_files = QPushButton(self.groupBox_files)
        self.btn_add_files.setObjectName(u"btn_add_files")
        self.horizontalLayout_batch.addWidget(self.btn_add_files)
        
        self.btn_remove_selected = QPushButton(self.groupBox_files)
        self.btn_remove_selected.setObjectName(u"btn_remove_selected")
        self.horizontalLayout_batch.addWidget(self.btn_remove_selected)
        
        self.verticalLayout_files.addLayout(self.horizontalLayout_batch)
        
        # 文件列表区域
        self.frame_files = QFrame(self.groupBox_files)
        self.frame_files.setObjectName(u"frame_files")
        self.frame_files.setMinimumSize(QSize(0, 150))
        self.frame_files.setFrameShape(QFrame.Box)
        self.frame_files.setFrameShadow(QFrame.Raised)
        
        self.verticalLayout_file_list = QVBoxLayout(self.frame_files)
        self.verticalLayout_file_list.setObjectName(u"verticalLayout_file_list")
        
        self.verticalLayout_files.addWidget(self.frame_files)
        self.verticalLayout.addWidget(self.groupBox_files)
        
        # 水印设置区域
        self.groupBox_settings = QGroupBox(watermark_view)
        self.groupBox_settings.setObjectName(u"groupBox_settings")
        
        self.verticalLayout_settings = QVBoxLayout(self.groupBox_settings)
        self.verticalLayout_settings.setObjectName(u"verticalLayout_settings")
        
        # 水印类型选择
        self.horizontalLayout_type = QHBoxLayout()
        self.horizontalLayout_type.setObjectName(u"horizontalLayout_type")
        
        self.label_type = QLabel(self.groupBox_settings)
        self.label_type.setObjectName(u"label_type")
        self.horizontalLayout_type.addWidget(self.label_type)
        
        self.comboBox_type = QComboBox(self.groupBox_settings)
        self.comboBox_type.addItem("")
        self.comboBox_type.addItem("")
        self.comboBox_type.setObjectName(u"comboBox_type")
        self.horizontalLayout_type.addWidget(self.comboBox_type)
        
        self.horizontalSpacer_type = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_type.addItem(self.horizontalSpacer_type)
        
        self.verticalLayout_settings.addLayout(self.horizontalLayout_type)
        
        # 水印文本设置
        self.horizontalLayout_text = QHBoxLayout()
        self.horizontalLayout_text.setObjectName(u"horizontalLayout_text")
        
        self.label_text = QLabel(self.groupBox_settings)
        self.label_text.setObjectName(u"label_text")
        self.horizontalLayout_text.addWidget(self.label_text)
        
        self.lineEdit_text = QLineEdit(self.groupBox_settings)
        self.lineEdit_text.setObjectName(u"lineEdit_text")
        self.horizontalLayout_text.addWidget(self.lineEdit_text)
        
        self.verticalLayout_settings.addLayout(self.horizontalLayout_text)
        
        # 水印字体设置
        self.horizontalLayout_font = QHBoxLayout()
        self.horizontalLayout_font.setObjectName(u"horizontalLayout_font")
        
        self.label_font = QLabel(self.groupBox_settings)
        self.label_font.setObjectName(u"label_font")
        self.horizontalLayout_font.addWidget(self.label_font)
        
        self.comboBox_font = QComboBox(self.groupBox_settings)
        self.comboBox_font.setObjectName(u"comboBox_font")
        self.horizontalLayout_font.addWidget(self.comboBox_font)
        
        self.label_size = QLabel(self.groupBox_settings)
        self.label_size.setObjectName(u"label_size")
        self.horizontalLayout_font.addWidget(self.label_size)
        
        self.spinBox_size = QSpinBox(self.groupBox_settings)
        self.spinBox_size.setObjectName(u"spinBox_size")
        self.spinBox_size.setMinimum(8)
        self.spinBox_size.setMaximum(72)
        self.spinBox_size.setValue(36)
        self.horizontalLayout_font.addWidget(self.spinBox_size)
        
        self.horizontalSpacer_font = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_font.addItem(self.horizontalSpacer_font)
        
        self.verticalLayout_settings.addLayout(self.horizontalLayout_font)
        
        # 水印颜色和透明度
        self.horizontalLayout_color = QHBoxLayout()
        self.horizontalLayout_color.setObjectName(u"horizontalLayout_color")
        
        self.label_color = QLabel(self.groupBox_settings)
        self.label_color.setObjectName(u"label_color")
        self.horizontalLayout_color.addWidget(self.label_color)
        
        self.btn_color = QPushButton(self.groupBox_settings)
        self.btn_color.setObjectName(u"btn_color")
        self.btn_color.setMinimumSize(QSize(80, 30))
        self.horizontalLayout_color.addWidget(self.btn_color)
        
        self.label_opacity = QLabel(self.groupBox_settings)
        self.label_opacity.setObjectName(u"label_opacity")
        self.horizontalLayout_color.addWidget(self.label_opacity)
        
        self.slider_opacity = QSlider(self.groupBox_settings)
        self.slider_opacity.setObjectName(u"slider_opacity")
        self.slider_opacity.setOrientation(Qt.Horizontal)
        self.slider_opacity.setMinimum(10)
        self.slider_opacity.setMaximum(100)
        self.slider_opacity.setValue(50)
        self.horizontalLayout_color.addWidget(self.slider_opacity)
        
        self.label_opacity_value = QLabel(self.groupBox_settings)
        self.label_opacity_value.setObjectName(u"label_opacity_value")
        self.label_opacity_value.setMinimumSize(QSize(30, 0))
        self.horizontalLayout_color.addWidget(self.label_opacity_value)
        
        self.horizontalSpacer_color = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_color.addItem(self.horizontalSpacer_color)
        
        self.verticalLayout_settings.addLayout(self.horizontalLayout_color)
        
        # 水印位置设置
        self.horizontalLayout_position = QHBoxLayout()
        self.horizontalLayout_position.setObjectName(u"horizontalLayout_position")
        
        self.label_position = QLabel(self.groupBox_settings)
        self.label_position.setObjectName(u"label_position")
        self.horizontalLayout_position.addWidget(self.label_position)
        
        self.comboBox_position = QComboBox(self.groupBox_settings)
        self.comboBox_position.addItem("")
        self.comboBox_position.addItem("")
        self.comboBox_position.addItem("")
        self.comboBox_position.addItem("")
        self.comboBox_position.addItem("")
        self.comboBox_position.addItem("")
        self.comboBox_position.addItem("")
        self.comboBox_position.addItem("")
        self.comboBox_position.addItem("")
        self.comboBox_position.setObjectName(u"comboBox_position")
        self.horizontalLayout_position.addWidget(self.comboBox_position)
        
        self.label_rotation = QLabel(self.groupBox_settings)
        self.label_rotation.setObjectName(u"label_rotation")
        self.horizontalLayout_position.addWidget(self.label_rotation)
        
        self.spinBox_rotation = QSpinBox(self.groupBox_settings)
        self.spinBox_rotation.setObjectName(u"spinBox_rotation")
        self.spinBox_rotation.setMinimum(-180)
        self.spinBox_rotation.setMaximum(180)
        self.spinBox_rotation.setValue(45)
        self.horizontalLayout_position.addWidget(self.spinBox_rotation)
        
        self.horizontalSpacer_position = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_position.addItem(self.horizontalSpacer_position)
        
        self.verticalLayout_settings.addLayout(self.horizontalLayout_position)
        
        # 水印预览
        self.btn_preview = QPushButton(self.groupBox_settings)
        self.btn_preview.setObjectName(u"btn_preview")
        self.btn_preview.setMinimumSize(QSize(120, 30))
        
        self.horizontalLayout_preview = QHBoxLayout()
        self.horizontalLayout_preview.setObjectName(u"horizontalLayout_preview")
        
        self.horizontalSpacer_preview = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_preview.addItem(self.horizontalSpacer_preview)
        
        self.horizontalLayout_preview.addWidget(self.btn_preview)
        
        self.horizontalSpacer_preview2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_preview.addItem(self.horizontalSpacer_preview2)
        
        self.verticalLayout_settings.addLayout(self.horizontalLayout_preview)
        
        self.verticalLayout.addWidget(self.groupBox_settings)
        
        # 输出设置区域
        self.groupBox_output = QGroupBox(watermark_view)
        self.groupBox_output.setObjectName(u"groupBox_output")
        
        self.verticalLayout_output = QVBoxLayout(self.groupBox_output)
        self.verticalLayout_output.setObjectName(u"verticalLayout_output")
        
        # 输出目录选择
        self.horizontalLayout_output_dir = QHBoxLayout()
        self.horizontalLayout_output_dir.setObjectName(u"horizontalLayout_output_dir")
        
        self.label_output_dir = QLabel(self.groupBox_output)
        self.label_output_dir.setObjectName(u"label_output_dir")
        self.horizontalLayout_output_dir.addWidget(self.label_output_dir)
        
        self.comboBox_output_dir = QComboBox(self.groupBox_output)
        self.comboBox_output_dir.addItem("")
        self.comboBox_output_dir.addItem("")
        self.comboBox_output_dir.setObjectName(u"comboBox_output_dir")
        self.horizontalLayout_output_dir.addWidget(self.comboBox_output_dir)
        
        self.label_custom_dir = QLabel(self.groupBox_output)
        self.label_custom_dir.setObjectName(u"label_custom_dir")
        self.horizontalLayout_output_dir.addWidget(self.label_custom_dir)
        
        self.btn_choose_output_dir = QPushButton(self.groupBox_output)
        self.btn_choose_output_dir.setObjectName(u"btn_choose_output_dir")
        self.horizontalLayout_output_dir.addWidget(self.btn_choose_output_dir)
        
        self.horizontalSpacer_output_dir = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_output_dir.addItem(self.horizontalSpacer_output_dir)
        
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
        
        self.horizontalSpacer_suffix = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_suffix.addItem(self.horizontalSpacer_suffix)
        
        self.verticalLayout_output.addLayout(self.horizontalLayout_suffix)
        
        self.verticalLayout.addWidget(self.groupBox_output)
        
        # 进度条
        self.progressBar = QProgressBar(watermark_view)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.verticalLayout.addWidget(self.progressBar)
        
        # 操作按钮
        self.horizontalLayout_process = QHBoxLayout()
        self.horizontalLayout_process.setObjectName(u"horizontalLayout_process")
        
        self.horizontalSpacer_process = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_process.addItem(self.horizontalSpacer_process)
        
        self.btn_process = QPushButton(watermark_view)
        self.btn_process.setObjectName(u"btn_process")
        self.btn_process.setMinimumSize(QSize(150, 40))
        self.horizontalLayout_process.addWidget(self.btn_process)
        
        self.verticalLayout.addLayout(self.horizontalLayout_process)

        self.retranslateUi(watermark_view)

        QMetaObject.connectSlotsByName(watermark_view)
    # setupUi

    def retranslateUi(self, watermark_view):
        watermark_view.setWindowTitle(QCoreApplication.translate("watermark_view", u"添加水印", None))
        self.label_title.setText(QCoreApplication.translate("watermark_view", u"PDF添加水印", None))
        self.groupBox_files.setTitle(QCoreApplication.translate("watermark_view", u"文件选择", None))
        self.label_file.setText(QCoreApplication.translate("watermark_view", u"PDF文件:", None))
        self.btn_choose_file.setText(QCoreApplication.translate("watermark_view", u"选择PDF", None))
        self.label_batch.setText(QCoreApplication.translate("watermark_view", u"批量处理:", None))
        self.btn_add_files.setText(QCoreApplication.translate("watermark_view", u"添加文件", None))
        self.btn_remove_selected.setText(QCoreApplication.translate("watermark_view", u"移除选中", None))
        
        self.groupBox_settings.setTitle(QCoreApplication.translate("watermark_view", u"水印设置", None))
        self.label_type.setText(QCoreApplication.translate("watermark_view", u"水印类型:", None))
        self.comboBox_type.setItemText(0, QCoreApplication.translate("watermark_view", u"文本水印", None))
        self.comboBox_type.setItemText(1, QCoreApplication.translate("watermark_view", u"图片水印", None))
        self.label_text.setText(QCoreApplication.translate("watermark_view", u"水印文本:", None))
        self.lineEdit_text.setText(QCoreApplication.translate("watermark_view", u"机密文件", None))
        self.label_font.setText(QCoreApplication.translate("watermark_view", u"字体:", None))
        self.label_size.setText(QCoreApplication.translate("watermark_view", u"字号:", None))
        self.label_color.setText(QCoreApplication.translate("watermark_view", u"颜色:", None))
        self.btn_color.setText(QCoreApplication.translate("watermark_view", u"选择颜色", None))
        self.label_opacity.setText(QCoreApplication.translate("watermark_view", u"透明度:", None))
        self.label_opacity_value.setText(QCoreApplication.translate("watermark_view", u"50%", None))
        self.label_position.setText(QCoreApplication.translate("watermark_view", u"位置:", None))
        self.comboBox_position.setItemText(0, QCoreApplication.translate("watermark_view", u"居中", None))
        self.comboBox_position.setItemText(1, QCoreApplication.translate("watermark_view", u"左上角", None))
        self.comboBox_position.setItemText(2, QCoreApplication.translate("watermark_view", u"右上角", None))
        self.comboBox_position.setItemText(3, QCoreApplication.translate("watermark_view", u"左下角", None))
        self.comboBox_position.setItemText(4, QCoreApplication.translate("watermark_view", u"右下角", None))
        self.comboBox_position.setItemText(5, QCoreApplication.translate("watermark_view", u"顶部居中", None))
        self.comboBox_position.setItemText(6, QCoreApplication.translate("watermark_view", u"底部居中", None))
        self.comboBox_position.setItemText(7, QCoreApplication.translate("watermark_view", u"左侧居中", None))
        self.comboBox_position.setItemText(8, QCoreApplication.translate("watermark_view", u"右侧居中", None))
        self.label_rotation.setText(QCoreApplication.translate("watermark_view", u"旋转角度:", None))
        self.btn_preview.setText(QCoreApplication.translate("watermark_view", u"预览水印效果", None))
        
        self.groupBox_output.setTitle(QCoreApplication.translate("watermark_view", u"输出设置", None))
        self.label_output_dir.setText(QCoreApplication.translate("watermark_view", u"输出位置:", None))
        self.comboBox_output_dir.setItemText(0, QCoreApplication.translate("watermark_view", u"PDF相同目录", None))
        self.comboBox_output_dir.setItemText(1, QCoreApplication.translate("watermark_view", u"自定义目录", None))
        self.label_custom_dir.setText(QCoreApplication.translate("watermark_view", u"指定目录", None))
        self.btn_choose_output_dir.setText(QCoreApplication.translate("watermark_view", u"选择", None))
        self.label_suffix.setText(QCoreApplication.translate("watermark_view", u"文件名后缀:", None))
        self.lineEdit_suffix.setText(QCoreApplication.translate("watermark_view", u"_水印", None))
        self.checkBox_backup.setText(QCoreApplication.translate("watermark_view", u"创建备份", None))
        self.btn_process.setText(QCoreApplication.translate("watermark_view", u"添加水印", None))
    # retranslateUi 