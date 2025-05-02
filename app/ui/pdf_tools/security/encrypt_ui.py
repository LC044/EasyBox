from PySide6.QtCore import QCoreApplication, QMetaObject, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QCheckBox, QComboBox, QLabel, QLineEdit, QProgressBar, QPushButton,
                             QSizePolicy, QSpacerItem, QVBoxLayout, QHBoxLayout, QWidget,
                             QGroupBox, QSpinBox)


class Ui_encrypt_pdf_view(object):
    def setupUi(self, encrypt_pdf_view):
        if not encrypt_pdf_view.objectName():
            encrypt_pdf_view.setObjectName(u"encrypt_pdf_view")
        encrypt_pdf_view.resize(800, 600)
        self.verticalLayout = QVBoxLayout(encrypt_pdf_view)
        self.verticalLayout.setObjectName(u"verticalLayout")
        
        # 文件选择区域
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(encrypt_pdf_view)
        self.label.setObjectName(u"label")
        self.horizontalLayout.addWidget(self.label)
        
        self.lineEdit_pdf_path = QLineEdit(encrypt_pdf_view)
        self.lineEdit_pdf_path.setObjectName(u"lineEdit_pdf_path")
        self.lineEdit_pdf_path.setReadOnly(True)
        self.horizontalLayout.addWidget(self.lineEdit_pdf_path)
        
        self.btn_choose_file = QPushButton(encrypt_pdf_view)
        self.btn_choose_file.setObjectName(u"btn_choose_file")
        self.horizontalLayout.addWidget(self.btn_choose_file)
        
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        # 加密设置区域
        self.groupBox_encrypt_options = QGroupBox(encrypt_pdf_view)
        self.groupBox_encrypt_options.setObjectName(u"groupBox_encrypt_options")
        self.verticalLayout_options = QVBoxLayout(self.groupBox_encrypt_options)
        self.verticalLayout_options.setObjectName(u"verticalLayout_options")
        
        # 密码说明
        self.label_pwd_info = QLabel(self.groupBox_encrypt_options)
        self.label_pwd_info.setObjectName(u"label_pwd_info")
        self.label_pwd_info.setWordWrap(True)
        self.verticalLayout_options.addWidget(self.label_pwd_info)
        
        # 用户密码
        self.horizontalLayout_user_pwd = QHBoxLayout()
        self.horizontalLayout_user_pwd.setObjectName(u"horizontalLayout_user_pwd")
        self.label_user_pwd = QLabel(self.groupBox_encrypt_options)
        self.label_user_pwd.setObjectName(u"label_user_pwd")
        self.horizontalLayout_user_pwd.addWidget(self.label_user_pwd)
        
        self.lineEdit_user_pwd = QLineEdit(self.groupBox_encrypt_options)
        self.lineEdit_user_pwd.setObjectName(u"lineEdit_user_pwd")
        self.lineEdit_user_pwd.setEchoMode(QLineEdit.Password)
        self.horizontalLayout_user_pwd.addWidget(self.lineEdit_user_pwd)
        
        self.verticalLayout_options.addLayout(self.horizontalLayout_user_pwd)
        
        # 确认用户密码
        self.horizontalLayout_confirm_user_pwd = QHBoxLayout()
        self.horizontalLayout_confirm_user_pwd.setObjectName(u"horizontalLayout_confirm_user_pwd")
        self.label_confirm_user_pwd = QLabel(self.groupBox_encrypt_options)
        self.label_confirm_user_pwd.setObjectName(u"label_confirm_user_pwd")
        self.horizontalLayout_confirm_user_pwd.addWidget(self.label_confirm_user_pwd)
        
        self.lineEdit_confirm_user_pwd = QLineEdit(self.groupBox_encrypt_options)
        self.lineEdit_confirm_user_pwd.setObjectName(u"lineEdit_confirm_user_pwd")
        self.lineEdit_confirm_user_pwd.setEchoMode(QLineEdit.Password)
        self.horizontalLayout_confirm_user_pwd.addWidget(self.lineEdit_confirm_user_pwd)
        
        self.verticalLayout_options.addLayout(self.horizontalLayout_confirm_user_pwd)
        
        # 所有者密码
        self.horizontalLayout_owner_pwd = QHBoxLayout()
        self.horizontalLayout_owner_pwd.setObjectName(u"horizontalLayout_owner_pwd")
        self.label_owner_pwd = QLabel(self.groupBox_encrypt_options)
        self.label_owner_pwd.setObjectName(u"label_owner_pwd")
        self.horizontalLayout_owner_pwd.addWidget(self.label_owner_pwd)
        
        self.lineEdit_owner_pwd = QLineEdit(self.groupBox_encrypt_options)
        self.lineEdit_owner_pwd.setObjectName(u"lineEdit_owner_pwd")
        self.lineEdit_owner_pwd.setEchoMode(QLineEdit.Password)
        self.horizontalLayout_owner_pwd.addWidget(self.lineEdit_owner_pwd)
        
        self.verticalLayout_options.addLayout(self.horizontalLayout_owner_pwd)
        
        # 确认所有者密码
        self.horizontalLayout_confirm_owner_pwd = QHBoxLayout()
        self.horizontalLayout_confirm_owner_pwd.setObjectName(u"horizontalLayout_confirm_owner_pwd")
        self.label_confirm_owner_pwd = QLabel(self.groupBox_encrypt_options)
        self.label_confirm_owner_pwd.setObjectName(u"label_confirm_owner_pwd")
        self.horizontalLayout_confirm_owner_pwd.addWidget(self.label_confirm_owner_pwd)
        
        self.lineEdit_confirm_owner_pwd = QLineEdit(self.groupBox_encrypt_options)
        self.lineEdit_confirm_owner_pwd.setObjectName(u"lineEdit_confirm_owner_pwd")
        self.lineEdit_confirm_owner_pwd.setEchoMode(QLineEdit.Password)
        self.horizontalLayout_confirm_owner_pwd.addWidget(self.lineEdit_confirm_owner_pwd)
        
        self.verticalLayout_options.addLayout(self.horizontalLayout_confirm_owner_pwd)
        
        # 加密级别
        self.horizontalLayout_enc_level = QHBoxLayout()
        self.horizontalLayout_enc_level.setObjectName(u"horizontalLayout_enc_level")
        self.label_enc_level = QLabel(self.groupBox_encrypt_options)
        self.label_enc_level.setObjectName(u"label_enc_level")
        self.horizontalLayout_enc_level.addWidget(self.label_enc_level)
        
        self.comboBox_enc_level = QComboBox(self.groupBox_encrypt_options)
        self.comboBox_enc_level.addItem("128位AES（推荐）")
        self.comboBox_enc_level.addItem("128位RC4")
        self.comboBox_enc_level.addItem("40位RC4（兼容）")
        self.comboBox_enc_level.setObjectName(u"comboBox_enc_level")
        self.horizontalLayout_enc_level.addWidget(self.comboBox_enc_level)
        
        self.horizontalLayout_enc_level.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout_options.addLayout(self.horizontalLayout_enc_level)
        
        # 权限设置
        self.label_permissions = QLabel(self.groupBox_encrypt_options)
        self.label_permissions.setObjectName(u"label_permissions")
        self.verticalLayout_options.addWidget(self.label_permissions)
        
        # 打印权限
        self.checkBox_print = QCheckBox(self.groupBox_encrypt_options)
        self.checkBox_print.setObjectName(u"checkBox_print")
        self.checkBox_print.setChecked(True)
        self.verticalLayout_options.addWidget(self.checkBox_print)
        
        # 复制权限
        self.checkBox_copy = QCheckBox(self.groupBox_encrypt_options)
        self.checkBox_copy.setObjectName(u"checkBox_copy")
        self.checkBox_copy.setChecked(True)
        self.verticalLayout_options.addWidget(self.checkBox_copy)
        
        # 修改权限
        self.checkBox_modify = QCheckBox(self.groupBox_encrypt_options)
        self.checkBox_modify.setObjectName(u"checkBox_modify")
        self.checkBox_modify.setChecked(True)
        self.verticalLayout_options.addWidget(self.checkBox_modify)
        
        # 注释权限
        self.checkBox_annotate = QCheckBox(self.groupBox_encrypt_options)
        self.checkBox_annotate.setObjectName(u"checkBox_annotate")
        self.checkBox_annotate.setChecked(True)
        self.verticalLayout_options.addWidget(self.checkBox_annotate)
        
        self.verticalLayout.addWidget(self.groupBox_encrypt_options)
        
        # 输出选项区域
        self.groupBox_output = QGroupBox(encrypt_pdf_view)
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
        self.progressBar = QProgressBar(encrypt_pdf_view)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.verticalLayout.addWidget(self.progressBar)
        
        # 加密按钮
        self.horizontalLayout_encrypt = QHBoxLayout()
        self.horizontalLayout_encrypt.setObjectName(u"horizontalLayout_encrypt")
        self.horizontalLayout_encrypt.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.btn_encrypt = QPushButton(encrypt_pdf_view)
        self.btn_encrypt.setObjectName(u"btn_encrypt")
        self.btn_encrypt.setMinimumSize(QSize(120, 40))
        self.horizontalLayout_encrypt.addWidget(self.btn_encrypt)
        
        self.horizontalLayout_encrypt.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.verticalLayout.addLayout(self.horizontalLayout_encrypt)

        self.retranslateUi(encrypt_pdf_view)

        QMetaObject.connectSlotsByName(encrypt_pdf_view)
    
    def retranslateUi(self, encrypt_pdf_view):
        encrypt_pdf_view.setWindowTitle(QCoreApplication.translate("encrypt_pdf_view", u"PDF加密", None))
        self.label.setText(QCoreApplication.translate("encrypt_pdf_view", u"选择PDF文件:", None))
        self.btn_choose_file.setText(QCoreApplication.translate("encrypt_pdf_view", u"选择文件", None))
        
        self.groupBox_encrypt_options.setTitle(QCoreApplication.translate("encrypt_pdf_view", u"加密设置", None))
        self.label_pwd_info.setText(QCoreApplication.translate("encrypt_pdf_view", u"说明：\n1. 用户密码：打开文档时需要输入的密码\n2. 所有者密码：修改文档权限或解密时需要的密码\n\n建议：可以只设置一种密码，也可以两种同时设置。如只需限制查看，仅设置用户密码即可；如只需限制编辑，仅设置所有者密码即可。", None))
        self.label_user_pwd.setText(QCoreApplication.translate("encrypt_pdf_view", u"用户密码:", None))
        self.label_confirm_user_pwd.setText(QCoreApplication.translate("encrypt_pdf_view", u"确认用户密码:", None))
        self.label_owner_pwd.setText(QCoreApplication.translate("encrypt_pdf_view", u"所有者密码:", None))
        self.label_confirm_owner_pwd.setText(QCoreApplication.translate("encrypt_pdf_view", u"确认所有者密码:", None))
        
        self.label_enc_level.setText(QCoreApplication.translate("encrypt_pdf_view", u"加密级别:", None))
        self.label_permissions.setText(QCoreApplication.translate("encrypt_pdf_view", u"权限设置:", None))
        self.checkBox_print.setText(QCoreApplication.translate("encrypt_pdf_view", u"允许打印", None))
        self.checkBox_copy.setText(QCoreApplication.translate("encrypt_pdf_view", u"允许复制内容", None))
        self.checkBox_modify.setText(QCoreApplication.translate("encrypt_pdf_view", u"允许修改文档", None))
        self.checkBox_annotate.setText(QCoreApplication.translate("encrypt_pdf_view", u"允许添加注释", None))
        
        self.groupBox_output.setTitle(QCoreApplication.translate("encrypt_pdf_view", u"输出选项", None))
        self.label_output.setText(QCoreApplication.translate("encrypt_pdf_view", u"输出目录:", None))
        self.label_output_dir.setText(QCoreApplication.translate("encrypt_pdf_view", u"", None))
        self.btn_choose_output_dir.setText(QCoreApplication.translate("encrypt_pdf_view", u"选择目录", None))
        
        self.label_filename.setText(QCoreApplication.translate("encrypt_pdf_view", u"文件名:", None))
        self.lineEdit_filename.setText(QCoreApplication.translate("encrypt_pdf_view", u"加密文件", None))
        
        self.btn_encrypt.setText(QCoreApplication.translate("encrypt_pdf_view", u"加密PDF", None)) 