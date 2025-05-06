from PySide6.QtCore import QCoreApplication, QMetaObject, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QCheckBox, QComboBox, QLabel, QLineEdit, QProgressBar, QPushButton,
                             QRadioButton, QSizePolicy, QSpacerItem, QVBoxLayout, QHBoxLayout, QWidget,
                             QGroupBox, QSpinBox)


class Ui_split_pdf_view(object):
    def setupUi(self, split_pdf_view):
        if not split_pdf_view.objectName():
            split_pdf_view.setObjectName(u"split_pdf_view")
        split_pdf_view.resize(800, 600)
        self.verticalLayout = QVBoxLayout(split_pdf_view)
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        # 文件选择区域
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(split_pdf_view)
        self.label.setObjectName(u"label")
        self.horizontalLayout.addWidget(self.label)
        
        self.lineEdit_pdf_path = QLineEdit(split_pdf_view)
        self.lineEdit_pdf_path.setObjectName(u"lineEdit_pdf_path")
        self.lineEdit_pdf_path.setReadOnly(True)
        self.horizontalLayout.addWidget(self.lineEdit_pdf_path)
        
        self.btn_choose_file = QPushButton(split_pdf_view)
        self.btn_choose_file.setObjectName(u"btn_choose_file")
        self.horizontalLayout.addWidget(self.btn_choose_file)
        
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        # 拆分选项区域
        self.groupBox_split_options = QGroupBox(split_pdf_view)
        self.groupBox_split_options.setObjectName(u"groupBox_split_options")
        self.verticalLayout_options = QVBoxLayout(self.groupBox_split_options)
        self.verticalLayout_options.setObjectName(u"verticalLayout_options")
        
        # 按页数拆分
        self.radioButton_by_pages = QRadioButton(self.groupBox_split_options)
        self.radioButton_by_pages.setObjectName(u"radioButton_by_pages")
        self.radioButton_by_pages.setChecked(True)
        self.verticalLayout_options.addWidget(self.radioButton_by_pages)
        
        self.horizontalLayout_pages = QHBoxLayout()
        self.horizontalLayout_pages.setObjectName(u"horizontalLayout_pages")
        self.label_pages = QLabel(self.groupBox_split_options)
        self.label_pages.setObjectName(u"label_pages")
        self.horizontalLayout_pages.addWidget(self.label_pages)
        
        self.spinBox_pages = QSpinBox(self.groupBox_split_options)
        self.spinBox_pages.setObjectName(u"spinBox_pages")
        self.spinBox_pages.setMinimum(1)
        self.spinBox_pages.setValue(1)
        self.spinBox_pages.setMinimumWidth(80)
        self.spinBox_pages.setMaximumWidth(120)
        font = self.spinBox_pages.font()
        font.setPointSize(10)
        self.spinBox_pages.setFont(font)
        self.horizontalLayout_pages.addWidget(self.spinBox_pages)
        
        self.horizontalLayout_pages.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout_options.addLayout(self.horizontalLayout_pages)
        
        # 按页码拆分
        self.radioButton_by_ranges = QRadioButton(self.groupBox_split_options)
        self.radioButton_by_ranges.setObjectName(u"radioButton_by_ranges")
        self.verticalLayout_options.addWidget(self.radioButton_by_ranges)
        
        self.horizontalLayout_ranges = QHBoxLayout()
        self.horizontalLayout_ranges.setObjectName(u"horizontalLayout_ranges")
        self.label_ranges = QLabel(self.groupBox_split_options)
        self.label_ranges.setObjectName(u"label_ranges")
        self.horizontalLayout_ranges.addWidget(self.label_ranges)
        
        self.lineEdit_ranges = QLineEdit(self.groupBox_split_options)
        self.lineEdit_ranges.setObjectName(u"lineEdit_ranges")
        self.lineEdit_ranges.setEnabled(False)
        self.lineEdit_ranges.setMinimumWidth(180)
        font = self.lineEdit_ranges.font()
        font.setPointSize(10)
        self.lineEdit_ranges.setFont(font)
        self.horizontalLayout_ranges.addWidget(self.lineEdit_ranges)
        
        self.horizontalLayout_ranges.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout_options.addLayout(self.horizontalLayout_ranges)
        
        # 提取单页
        self.radioButton_single_page = QRadioButton(self.groupBox_split_options)
        self.radioButton_single_page.setObjectName(u"radioButton_single_page")
        self.verticalLayout_options.addWidget(self.radioButton_single_page)
        
        self.horizontalLayout_single = QHBoxLayout()
        self.horizontalLayout_single.setObjectName(u"horizontalLayout_single")
        self.label_single = QLabel(self.groupBox_split_options)
        self.label_single.setObjectName(u"label_single")
        self.horizontalLayout_single.addWidget(self.label_single)
        
        self.spinBox_single = QSpinBox(self.groupBox_split_options)
        self.spinBox_single.setObjectName(u"spinBox_single")
        self.spinBox_single.setMinimum(1)
        self.spinBox_single.setValue(1)
        self.spinBox_single.setEnabled(False)
        self.spinBox_single.setMinimumWidth(80)
        self.spinBox_single.setMaximumWidth(120)
        font = self.spinBox_single.font()
        font.setPointSize(10)
        self.spinBox_single.setFont(font)
        self.horizontalLayout_single.addWidget(self.spinBox_single)
        
        self.horizontalLayout_single.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout_options.addLayout(self.horizontalLayout_single)
        
        # 拆分为单页
        self.radioButton_all_pages = QRadioButton(self.groupBox_split_options)
        self.radioButton_all_pages.setObjectName(u"radioButton_all_pages")
        self.verticalLayout_options.addWidget(self.radioButton_all_pages)
        
        self.verticalLayout.addWidget(self.groupBox_split_options)
        
        # 输出选项区域
        self.groupBox_output = QGroupBox(split_pdf_view)
        self.groupBox_output.setObjectName(u"groupBox_output")
        self.verticalLayout_output = QVBoxLayout(self.groupBox_output)
        self.verticalLayout_output.setObjectName(u"verticalLayout_output")
        
        # 输出目录选择
        self.horizontalLayout_output_dir = QHBoxLayout()
        self.horizontalLayout_output_dir.setObjectName(u"horizontalLayout_output_dir")
        self.label_output = QLabel(self.groupBox_output)
        self.label_output.setObjectName(u"label_output")
        self.horizontalLayout_output_dir.addWidget(self.label_output)
        
        self.comboBox_output_dir = QComboBox(self.groupBox_output)
        self.comboBox_output_dir.addItem("PDF相同目录")
        self.comboBox_output_dir.addItem("自定义目录")
        self.comboBox_output_dir.setObjectName(u"comboBox_output_dir")
        self.horizontalLayout_output_dir.addWidget(self.comboBox_output_dir)
        
        self.label_output_dir = QLabel(self.groupBox_output)
        self.label_output_dir.setObjectName(u"label_output_dir")
        self.horizontalLayout_output_dir.addWidget(self.label_output_dir)
        
        self.btn_choose_output_dir = QPushButton(self.groupBox_output)
        self.btn_choose_output_dir.setObjectName(u"btn_choose_output_dir")
        self.horizontalLayout_output_dir.addWidget(self.btn_choose_output_dir)
        
        self.verticalLayout_output.addLayout(self.horizontalLayout_output_dir)
        
        # 文件名前缀
        self.horizontalLayout_prefix = QHBoxLayout()
        self.horizontalLayout_prefix.setObjectName(u"horizontalLayout_prefix")
        self.label_prefix = QLabel(self.groupBox_output)
        self.label_prefix.setObjectName(u"label_prefix")
        self.horizontalLayout_prefix.addWidget(self.label_prefix)
        
        self.lineEdit_prefix = QLineEdit(self.groupBox_output)
        self.lineEdit_prefix.setObjectName(u"lineEdit_prefix")
        self.horizontalLayout_prefix.addWidget(self.lineEdit_prefix)
        
        self.verticalLayout_output.addLayout(self.horizontalLayout_prefix)
        
        self.verticalLayout.addWidget(self.groupBox_output)
        
        # 进度条
        self.progressBar = QProgressBar(split_pdf_view)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.verticalLayout.addWidget(self.progressBar)
        
        # 拆分按钮
        self.horizontalLayout_split = QHBoxLayout()
        self.horizontalLayout_split.setObjectName(u"horizontalLayout_split")
        self.horizontalLayout_split.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.btn_split = QPushButton(split_pdf_view)
        self.btn_split.setObjectName(u"btn_split")
        self.btn_split.setMinimumSize(QSize(120, 40))
        self.horizontalLayout_split.addWidget(self.btn_split)
        
        self.horizontalLayout_split.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout_split)

        self.retranslateUi(split_pdf_view)

        QMetaObject.connectSlotsByName(split_pdf_view)
    
    def retranslateUi(self, split_pdf_view):
        split_pdf_view.setWindowTitle(QCoreApplication.translate("split_pdf_view", u"PDF拆分", None))
        self.label.setText(QCoreApplication.translate("split_pdf_view", u"选择PDF文件:", None))
        self.btn_choose_file.setText(QCoreApplication.translate("split_pdf_view", u"选择文件", None))
        
        self.groupBox_split_options.setTitle(QCoreApplication.translate("split_pdf_view", u"拆分选项", None))
        self.radioButton_by_pages.setText(QCoreApplication.translate("split_pdf_view", u"按页数拆分", None))
        self.label_pages.setText(QCoreApplication.translate("split_pdf_view", u"每个文件页数:", None))
        
        self.radioButton_by_ranges.setText(QCoreApplication.translate("split_pdf_view", u"按页码范围拆分", None))
        self.label_ranges.setText(QCoreApplication.translate("split_pdf_view", u"页码范围:", None))
        self.lineEdit_ranges.setPlaceholderText(QCoreApplication.translate("split_pdf_view", u"例如: 1-5,6-10,11-15", None))
        
        self.radioButton_single_page.setText(QCoreApplication.translate("split_pdf_view", u"提取单页", None))
        self.label_single.setText(QCoreApplication.translate("split_pdf_view", u"页码:", None))
        
        self.radioButton_all_pages.setText(QCoreApplication.translate("split_pdf_view", u"拆分为单页文件", None))
        
        self.groupBox_output.setTitle(QCoreApplication.translate("split_pdf_view", u"输出选项", None))
        self.label_output.setText(QCoreApplication.translate("split_pdf_view", u"输出目录:", None))
        self.label_output_dir.setText(QCoreApplication.translate("split_pdf_view", u"", None))
        self.btn_choose_output_dir.setText(QCoreApplication.translate("split_pdf_view", u"选择目录", None))
        
        self.label_prefix.setText(QCoreApplication.translate("split_pdf_view", u"文件名:", None))
        self.lineEdit_prefix.setText(QCoreApplication.translate("split_pdf_view", u"拆分文件", None))
        
        self.btn_split.setText(QCoreApplication.translate("split_pdf_view", u"拆分PDF", None)) 