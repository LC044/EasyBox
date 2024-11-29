# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'encrypt_dialog_ui.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QGridLayout, QLabel,
    QLineEdit, QRadioButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(323, 323)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.lineEdit_owner_pw1 = QLineEdit(Dialog)
        self.lineEdit_owner_pw1.setObjectName(u"lineEdit_owner_pw1")
        self.lineEdit_owner_pw1.setMaxLength(16)
        self.lineEdit_owner_pw1.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_owner_pw1)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.lineEdit_owner_pw2 = QLineEdit(Dialog)
        self.lineEdit_owner_pw2.setObjectName(u"lineEdit_owner_pw2")
        self.lineEdit_owner_pw2.setMaxLength(16)
        self.lineEdit_owner_pw2.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_owner_pw2)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.label_2)


        self.verticalLayout.addLayout(self.formLayout)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_6)

        self.lineEdit_user_pw1 = QLineEdit(Dialog)
        self.lineEdit_user_pw1.setObjectName(u"lineEdit_user_pw1")
        self.lineEdit_user_pw1.setMaxLength(16)
        self.lineEdit_user_pw1.setEchoMode(QLineEdit.Password)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.lineEdit_user_pw1)

        self.label_7 = QLabel(Dialog)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_7)

        self.lineEdit_user_pw2 = QLineEdit(Dialog)
        self.lineEdit_user_pw2.setObjectName(u"lineEdit_user_pw2")
        self.lineEdit_user_pw2.setMaxLength(16)
        self.lineEdit_user_pw2.setEchoMode(QLineEdit.Password)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.lineEdit_user_pw2)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)

        self.formLayout_2.setWidget(0, QFormLayout.SpanningRole, self.label_5)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.label_8 = QLabel(Dialog)
        self.label_8.setObjectName(u"label_8")
        font1 = QFont()
        font1.setPointSize(8)
        self.label_8.setFont(font1)
        self.label_8.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_8)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBox_edit = QCheckBox(Dialog)
        self.checkBox_edit.setObjectName(u"checkBox_edit")
        self.checkBox_edit.setChecked(True)

        self.gridLayout.addWidget(self.checkBox_edit, 0, 0, 1, 1)

        self.checkBox_copy = QCheckBox(Dialog)
        self.checkBox_copy.setObjectName(u"checkBox_copy")
        self.checkBox_copy.setChecked(True)

        self.gridLayout.addWidget(self.checkBox_copy, 0, 1, 1, 1)

        self.checkBox_annotate = QCheckBox(Dialog)
        self.checkBox_annotate.setObjectName(u"checkBox_annotate")
        self.checkBox_annotate.setChecked(True)

        self.gridLayout.addWidget(self.checkBox_annotate, 0, 2, 1, 2)

        self.radioButton_print = QRadioButton(Dialog)
        self.radioButton_print.setObjectName(u"radioButton_print")
        self.radioButton_print.setChecked(True)

        self.gridLayout.addWidget(self.radioButton_print, 1, 0, 1, 1)

        self.radioButton_print_low = QRadioButton(Dialog)
        self.radioButton_print_low.setObjectName(u"radioButton_print_low")
        self.radioButton_print_low.setChecked(False)

        self.gridLayout.addWidget(self.radioButton_print_low, 1, 1, 1, 1)

        self.radioButton_no_print = QRadioButton(Dialog)
        self.radioButton_no_print.setObjectName(u"radioButton_no_print")

        self.gridLayout.addWidget(self.radioButton_no_print, 1, 2, 1, 2)


        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStyleSheet(u"QPushButton{\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"    border-right: 2px solid #888888;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-bottom: 2px solid #888888;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-left: 1px solid #ffffff;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-top: 1px solid #ffffff;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: lightgray;\n"
"}")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u6587\u6863\u52a0\u5bc6", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u5bc6\u7801:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u786e\u8ba4:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u7f16\u8f91\u5bc6\u7801:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"\u5bc6\u7801:", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"\u786e\u8ba4:", None))
        self.lineEdit_user_pw2.setText("")
        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u6253\u5f00\u5bc6\u7801:", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"\u6ce8\u610f:\u53ea\u6709\u8bbe\u5b9a\u4e86\u4ee5\u4e0a\u5bc6\u7801\uff0c\u4ee5\u4e0b\u6743\u9650\u5185\u5bb9\u624d\u4f1a\u751f\u6548\uff0c\u5e76\u80fd\u9632\u6b62\u8fd9\u4e9b\u8bbe\u7f6e\u88ab\u4ed6\u4eba\u4fee\u6539\u3002\u8be5\u8bbe\u7f6e\u5bf9\u672c\u6b21\u6dfb\u52a0\u7684\u6240\u6709\u6587\u4ef6\u6709\u6548\u3002", None))
        self.checkBox_edit.setText(QCoreApplication.translate("Dialog", u"\u5141\u8bb8\u4fee\u6539", None))
        self.checkBox_copy.setText(QCoreApplication.translate("Dialog", u"\u5141\u8bb8\u590d\u5236", None))
        self.checkBox_annotate.setText(QCoreApplication.translate("Dialog", u"\u5141\u8bb8\u6dfb\u52a0\u6279\u6ce8", None))
        self.radioButton_print.setText(QCoreApplication.translate("Dialog", u"\u4e0d\u53d7\u9650\u6253\u5370", None))
        self.radioButton_print_low.setText(QCoreApplication.translate("Dialog", u"\u4f4e\u8d28\u91cf\u6253\u5370", None))
        self.radioButton_no_print.setText(QCoreApplication.translate("Dialog", u"\u4e0d\u5141\u8bb8\u6253\u5370", None))
    # retranslateUi

