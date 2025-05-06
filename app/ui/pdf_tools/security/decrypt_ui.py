from PySide6.QtCore import QCoreApplication, QMetaObject, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QLabel, QLineEdit, QProgressBar, QPushButton,
                             QSizePolicy, QSpacerItem, QVBoxLayout, QHBoxLayout, QWidget,
                             QGroupBox, QComboBox)


class Ui_decrypt_pdf_view(object):
    def setupUi(self, decrypt_pdf_view):
        if not decrypt_pdf_view.objectName():
            decrypt_pdf_view.setObjectName(u"decrypt_pdf_view")
        decrypt_pdf_view.resize(800, 600)
        self.verticalLayout = QVBoxLayout(decrypt_pdf_view)
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        # 文件选择区域
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(decrypt_pdf_view)
        self.label.setObjectName(u"label")
        self.horizontalLayout.addWidget(self.label)
        
        self.lineEdit_pdf_path = QLineEdit(decrypt_pdf_view)
        self.lineEdit_pdf_path.setObjectName(u"lineEdit_pdf_path")
        self.lineEdit_pdf_path.setReadOnly(True)
        self.horizontalLayout.addWidget(self.lineEdit_pdf_path)
        
        self.btn_choose_file = QPushButton(decrypt_pdf_view)
        self.btn_choose_file.setObjectName(u"btn_choose_file")
        self.horizontalLayout.addWidget(self.btn_choose_file)
        
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        # 解密设置区域
        self.groupBox_decrypt_options = QGroupBox(decrypt_pdf_view)
        self.groupBox_decrypt_options.setObjectName(u"groupBox_decrypt_options")
        self.verticalLayout_options = QVBoxLayout(self.groupBox_decrypt_options)
        self.verticalLayout_options.setObjectName(u"verticalLayout_options")
        
        # 所有者密码
        self.horizontalLayout_owner_pwd = QHBoxLayout()
        self.horizontalLayout_owner_pwd.setObjectName(u"horizontalLayout_owner_pwd")
        self.label_owner_pwd = QLabel(self.groupBox_decrypt_options)
        self.label_owner_pwd.setObjectName(u"label_owner_pwd")
        self.horizontalLayout_owner_pwd.addWidget(self.label_owner_pwd)
        
        self.lineEdit_owner_pwd = QLineEdit(self.groupBox_decrypt_options)
        self.lineEdit_owner_pwd.setObjectName(u"lineEdit_owner_pwd")
        self.lineEdit_owner_pwd.setEchoMode(QLineEdit.Password)
        self.horizontalLayout_owner_pwd.addWidget(self.lineEdit_owner_pwd)
        
        self.verticalLayout_options.addLayout(self.horizontalLayout_owner_pwd)
        
        # 用户密码
        self.horizontalLayout_user_pwd = QHBoxLayout()
        self.horizontalLayout_user_pwd.setObjectName(u"horizontalLayout_user_pwd")
        self.label_user_pwd = QLabel(self.groupBox_decrypt_options)
        self.label_user_pwd.setObjectName(u"label_user_pwd")
        self.horizontalLayout_user_pwd.addWidget(self.label_user_pwd)
        
        self.lineEdit_user_pwd = QLineEdit(self.groupBox_decrypt_options)
        self.lineEdit_user_pwd.setObjectName(u"lineEdit_user_pwd")
        self.lineEdit_user_pwd.setEchoMode(QLineEdit.Password)
        self.horizontalLayout_user_pwd.addWidget(self.lineEdit_user_pwd)
        
        self.verticalLayout_options.addLayout(self.horizontalLayout_user_pwd)
        
        # 密码说明
        self.label_pwd_info = QLabel(self.groupBox_decrypt_options)
        self.label_pwd_info.setObjectName(u"label_pwd_info")
        self.verticalLayout_options.addWidget(self.label_pwd_info)
        
        self.verticalLayout.addWidget(self.groupBox_decrypt_options)
        
        # 输出选项区域
        self.groupBox_output = QGroupBox(decrypt_pdf_view)
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
        
        # 文件名
        self.horizontalLayout_filename = QHBoxLayout()
        self.horizontalLayout_filename.setObjectName(u"horizontalLayout_filename")
        self.label_filename = QLabel(self.groupBox_output)
        self.label_filename.setObjectName(u"label_filename")
        self.horizontalLayout_filename.addWidget(self.label_filename)
        
        self.lineEdit_filename = QLineEdit(self.groupBox_output)
        self.lineEdit_filename.setObjectName(u"lineEdit_filename")
        self.horizontalLayout_filename.addWidget(self.lineEdit_filename)
        
        self.verticalLayout_output.addLayout(self.horizontalLayout_filename)
        
        self.verticalLayout.addWidget(self.groupBox_output)
        
        # 进度条
        self.progressBar = QProgressBar(decrypt_pdf_view)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.verticalLayout.addWidget(self.progressBar)
        
        # 解密按钮
        self.horizontalLayout_decrypt = QHBoxLayout()
        self.horizontalLayout_decrypt.setObjectName(u"horizontalLayout_decrypt")
        self.horizontalLayout_decrypt.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.btn_decrypt = QPushButton(decrypt_pdf_view)
        self.btn_decrypt.setObjectName(u"btn_decrypt")
        self.btn_decrypt.setMinimumSize(QSize(120, 40))
        self.horizontalLayout_decrypt.addWidget(self.btn_decrypt)
        
        self.horizontalLayout_decrypt.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout_decrypt)

        self.retranslateUi(decrypt_pdf_view)

        QMetaObject.connectSlotsByName(decrypt_pdf_view)
    
    def retranslateUi(self, decrypt_pdf_view):
        decrypt_pdf_view.setWindowTitle(QCoreApplication.translate("decrypt_pdf_view", u"PDF解密", None))
        self.label.setText(QCoreApplication.translate("decrypt_pdf_view", u"选择PDF文件:", None))
        self.btn_choose_file.setText(QCoreApplication.translate("decrypt_pdf_view", u"选择文件", None))
        
        self.groupBox_decrypt_options.setTitle(QCoreApplication.translate("decrypt_pdf_view", u"解密设置", None))
        self.label_owner_pwd.setText(QCoreApplication.translate("decrypt_pdf_view", u"所有者密码:", None))
        self.label_user_pwd.setText(QCoreApplication.translate("decrypt_pdf_view", u"用户密码:", None))
        self.label_pwd_info.setText(QCoreApplication.translate("decrypt_pdf_view", u"注：解密PDF文件需要所有者密码，如果没有所有者密码可以尝试使用用户密码", None))
        
        self.groupBox_output.setTitle(QCoreApplication.translate("decrypt_pdf_view", u"输出选项", None))
        self.label_output.setText(QCoreApplication.translate("decrypt_pdf_view", u"输出目录:", None))
        self.label_output_dir.setText(QCoreApplication.translate("decrypt_pdf_view", u"", None))
        self.btn_choose_output_dir.setText(QCoreApplication.translate("decrypt_pdf_view", u"选择目录", None))
        
        self.label_filename.setText(QCoreApplication.translate("decrypt_pdf_view", u"文件名:", None))
        self.lineEdit_filename.setText(QCoreApplication.translate("decrypt_pdf_view", u"解密文件", None))
        
        self.btn_decrypt.setText(QCoreApplication.translate("decrypt_pdf_view", u"解密PDF", None)) 