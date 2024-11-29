# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'merge_ui.ui'
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
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_merge_pdf_view(object):
    def setupUi(self, merge_pdf_view):
        if not merge_pdf_view.objectName():
            merge_pdf_view.setObjectName(u"merge_pdf_view")
        merge_pdf_view.resize(627, 614)
        merge_pdf_view.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(merge_pdf_view)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_8 = QLabel(merge_pdf_view)
        self.label_8.setObjectName(u"label_8")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_8.setFont(font)

        self.verticalLayout_3.addWidget(self.label_8)

        self.frame1 = QFrame(merge_pdf_view)
        self.frame1.setObjectName(u"frame1")
        self.frame1.setStyleSheet(u"QWidget{\n"
"	background: rgb(248,248,251);\n"
"	border-radius: 0px;\n"
"}\n"
"#frame1{\n"
"	border: 1px solid #e8e8e8;\n"
"}\n"
"\n"
"QPushButton{\n"
"    background-color: rgb(250,252,253);\n"
"    border-radius: 5px;\n"
"	padding:0px;\n"
"}\n"
"QPushButton:hover {\n"
"	color: rgb(148,133,247)\n"
"}\n"
"QCommandLinkButton{\n"
"    background-color: rgb(250,252,253);\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"    border:none;\n"
"}\n"
"QProgressBar{\n"
"    font-family: 'Arial Unicode MS';\n"
"    height:22px;\n"
"    text-align:center;\n"
"    font-size:14px;\n"
"    color:black;\n"
"    border-radius:11px;\n"
"    background:#EBEEF5;\n"
"}\n"
"QProgressBar::chunk{\n"
"    border-radius:11px;\n"
"    background:qlineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 #99ffff,stop:1 #9900ff);\n"
"}\n"
"QMessageBox QPushButton{\n"
"    background-color: rgb(250,252,253);\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"    border-right: 2px solid #888888;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd"
                        "\uff0c\u767d\u8272 */\n"
"    border-bottom: 2px solid #888888;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-left: 1px solid #ffffff;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-top: 1px solid #ffffff;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"}\n"
"QListView {\n"
"    color: black;\n"
"    border: none;\n"
"}\n"
"QListView::item {\n"
"    margin: 0px;\n"
"	border-bottom: 1px solid black;\n"
"}\n"
"QListView::item:hover {\n"
"    background: none;\n"
"}\n"
"/* \u88ab\u9009\u4e2d\u65f6\u7684\u80cc\u666f\u989c\u8272\u548c\u5de6\u8fb9\u6846\u989c\u8272 */\n"
"QListView::item:selected {\n"
"    border-radius: 0px;\n"
"	border-left: 0px solid rgb(62, 62, 62);\n"
"    background: none;\n"
"}")
        self.frame1.setFrameShape(QFrame.Box)
        self.frame1.setFrameShadow(QFrame.Raised)
        self.frame1.setLineWidth(2)
        self.verticalLayout_2 = QVBoxLayout(self.frame1)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, 0, 9, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.checkBox_select_all = QCheckBox(self.frame1)
        self.checkBox_select_all.setObjectName(u"checkBox_select_all")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_select_all.sizePolicy().hasHeightForWidth())
        self.checkBox_select_all.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.checkBox_select_all)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_order_inc = QPushButton(self.frame1)
        self.btn_order_inc.setObjectName(u"btn_order_inc")
        sizePolicy.setHeightForWidth(self.btn_order_inc.sizePolicy().hasHeightForWidth())
        self.btn_order_inc.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.btn_order_inc)

        self.btn_order_des = QPushButton(self.frame1)
        self.btn_order_des.setObjectName(u"btn_order_des")
        sizePolicy.setHeightForWidth(self.btn_order_des.sizePolicy().hasHeightForWidth())
        self.btn_order_des.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.btn_order_des)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.label = QLabel(self.frame1)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(50, 0))
        self.label.setMaximumSize(QSize(40, 16777215))
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label)

        self.label_2 = QLabel(self.frame1)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setMinimumSize(QSize(100, 0))
        self.label_2.setMaximumSize(QSize(100, 16777215))
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(self.frame1)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(100, 0))
        self.label_3.setMaximumSize(QSize(100, 16777215))
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.label_4 = QLabel(self.frame1)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)
        self.label_4.setMinimumSize(QSize(100, 0))
        self.label_4.setMaximumSize(QSize(100, 16777215))
        self.label_4.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.line_8 = QFrame(self.frame1)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setStyleSheet(u"border-bottom: 2px solid #888888;")
        self.line_8.setFrameShadow(QFrame.Raised)
        self.line_8.setLineWidth(5)
        self.line_8.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout_2.addWidget(self.line_8)


        self.verticalLayout_3.addWidget(self.frame1)

        self.widget1 = QWidget(merge_pdf_view)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setStyleSheet(u"#widget1{\n"
"	background: rgb(249,250,250);\n"
"	border-radius: 0px;\n"
"	border-right: 0px solid rgb(245,245,245);  \n"
"    border-bottom: 1px solid rgb(245,245,245);\n"
"    border-left: 0px solid rgb(245,245,245); \n"
"    border-top: 1px solid rgb(245,245,245);  \n"
"}\n"
"QPushButton:hover {\n"
"	color: rgb(148,133,247)\n"
"}\n"
"QWidget{\n"
"	background: rgb(238,244,249);\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton{\n"
"    background-color: rgb(250,252,253);\n"
"    border-radius: 5px;\n"
"	padding:0px;\n"
"}\n"
"QPushButton:hover {\n"
"	color: rgb(148,133,247)\n"
"}\n"
"QCommandLinkButton{\n"
"    background-color: rgb(250,252,253);\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"    border:none;\n"
"}\n"
"QProgressBar{\n"
"    font-family: 'Arial Unicode MS';\n"
"    height:22px;\n"
"    text-align:center;\n"
"    font-size:14px;\n"
"    color:black;\n"
"    border-radius:11px;\n"
"    background:#EBEEF5;\n"
"}\n"
"QProgressBar::chunk{\n"
"    border-radius:11px;\n"
"    background:ql"
                        "ineargradient(spread:pad,x1:0,y1:0,x2:1,y2:0,stop:0 #99ffff,stop:1 #9900ff);\n"
"}\n"
"QMessageBox QPushButton{\n"
"    background-color: rgb(250,252,253);\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"    border-right: 2px solid #888888;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-bottom: 2px solid #888888;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-left: 1px solid #ffffff;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-top: 1px solid #ffffff;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"}\n"
"QListView {\n"
"    color: black;\n"
"    border: none;\n"
"}\n"
"QListView::item {\n"
"    margin: 0px;\n"
"	border-bottom: 1px solid black;\n"
"}\n"
"QListView::item:hover {\n"
"    background: none;\n"
"}\n"
"/* \u88ab\u9009\u4e2d\u65f6\u7684\u80cc\u666f\u989c\u8272\u548c\u5de6\u8fb9\u6846\u989c\u8272 */\n"
"QListView::item:selected {\n"
"    border-radius: 0px;\n"
"	border-left: 0"
                        "px solid rgb(62, 62, 62);\n"
"    background: none;\n"
"}")
        self.horizontalLayout_2 = QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 9, -1, 9)
        self.btn_remove_selected = QPushButton(self.widget1)
        self.btn_remove_selected.setObjectName(u"btn_remove_selected")

        self.horizontalLayout_2.addWidget(self.btn_remove_selected)

        self.horizontalSpacer_2 = QSpacerItem(243, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.btn_choose_files = QPushButton(self.widget1)
        self.btn_choose_files.setObjectName(u"btn_choose_files")
        self.btn_choose_files.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_choose_files.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_2.addWidget(self.btn_choose_files)

        self.horizontalSpacer_3 = QSpacerItem(243, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.btn_setting = QPushButton(self.widget1)
        self.btn_setting.setObjectName(u"btn_setting")

        self.horizontalLayout_2.addWidget(self.btn_setting)


        self.verticalLayout_3.addWidget(self.widget1)

        self.progressBar = QProgressBar(merge_pdf_view)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout_3.addWidget(self.progressBar)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 9, -1, -1)
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(15)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 9, -1, -1)
        self.checkBox_picture_pdf = QCheckBox(merge_pdf_view)
        self.checkBox_picture_pdf.setObjectName(u"checkBox_picture_pdf")

        self.gridLayout.addWidget(self.checkBox_picture_pdf, 0, 2, 1, 2)

        self.label_6 = QLabel(merge_pdf_view)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)

        self.label_9 = QLabel(merge_pdf_view)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 2, 0, 1, 1)

        self.btn_merge = QPushButton(merge_pdf_view)
        self.btn_merge.setObjectName(u"btn_merge")
        self.btn_merge.setMinimumSize(QSize(80, 0))
        self.btn_merge.setStyleSheet(u"QPushButton {\n"
"    background-color: #3498db; /* \u6309\u94ae\u80cc\u666f\u8272 */\n"
"    color: white; /* \u5b57\u4f53\u989c\u8272 */\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #2980b9; /* \u60ac\u6d6e\u65f6\u80cc\u666f\u8272 */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #1c6e91; /* \u70b9\u51fb\u65f6\u80cc\u666f\u8272 */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.btn_merge, 2, 7, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 6, 1, 1)

        self.lineEdit_filename = QLineEdit(merge_pdf_view)
        self.lineEdit_filename.setObjectName(u"lineEdit_filename")

        self.gridLayout.addWidget(self.lineEdit_filename, 1, 1, 1, 3)

        self.label_5 = QLabel(merge_pdf_view)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.label_10 = QLabel(merge_pdf_view)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 1, 4, 1, 1)

        self.checkBox_watermark = QCheckBox(merge_pdf_view)
        self.checkBox_watermark.setObjectName(u"checkBox_watermark")

        self.gridLayout.addWidget(self.checkBox_watermark, 0, 4, 1, 1)

        self.checkBox_doc_encrypt = QCheckBox(merge_pdf_view)
        self.checkBox_doc_encrypt.setObjectName(u"checkBox_doc_encrypt")

        self.gridLayout.addWidget(self.checkBox_doc_encrypt, 0, 1, 1, 1)

        self.comboBox_output_dir = QComboBox(merge_pdf_view)
        self.comboBox_output_dir.addItem("")
        self.comboBox_output_dir.addItem("")
        self.comboBox_output_dir.setObjectName(u"comboBox_output_dir")

        self.gridLayout.addWidget(self.comboBox_output_dir, 2, 1, 1, 1)

        self.btn_choose_output_dir = QPushButton(merge_pdf_view)
        self.btn_choose_output_dir.setObjectName(u"btn_choose_output_dir")

        self.gridLayout.addWidget(self.btn_choose_output_dir, 2, 5, 1, 1)

        self.label_output_dir = QLabel(merge_pdf_view)
        self.label_output_dir.setObjectName(u"label_output_dir")

        self.gridLayout.addWidget(self.label_output_dir, 2, 2, 1, 3)


        self.horizontalLayout_4.addLayout(self.gridLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.retranslateUi(merge_pdf_view)

        QMetaObject.connectSlotsByName(merge_pdf_view)
    # setupUi

    def retranslateUi(self, merge_pdf_view):
        merge_pdf_view.setWindowTitle(QCoreApplication.translate("merge_pdf_view", u"Form", None))
        self.label_8.setText(QCoreApplication.translate("merge_pdf_view", u"\u5408\u5e76\u591a\u4e2aPDF", None))
        self.checkBox_select_all.setText(QCoreApplication.translate("merge_pdf_view", u"\u540d\u79f0", None))
        self.btn_order_inc.setText(QCoreApplication.translate("merge_pdf_view", u"\u25b2", None))
        self.btn_order_des.setText(QCoreApplication.translate("merge_pdf_view", u"\u25bc", None))
        self.label.setText(QCoreApplication.translate("merge_pdf_view", u"\u9875\u6570", None))
        self.label_2.setText(QCoreApplication.translate("merge_pdf_view", u"\u8f93\u51fa\u8303\u56f4", None))
        self.label_3.setText(QCoreApplication.translate("merge_pdf_view", u"\u72b6\u6001", None))
        self.label_4.setText(QCoreApplication.translate("merge_pdf_view", u"\u64cd\u4f5c", None))
        self.btn_remove_selected.setText(QCoreApplication.translate("merge_pdf_view", u"\u6e05\u9664\u9009\u4e2d", None))
        self.btn_choose_files.setText(QCoreApplication.translate("merge_pdf_view", u"\u6dfb\u52a0\u6587\u4ef6", None))
        self.btn_setting.setText(QCoreApplication.translate("merge_pdf_view", u"\u8bbe\u7f6e", None))
        self.checkBox_picture_pdf.setText(QCoreApplication.translate("merge_pdf_view", u"\u56fe\u7247\u578bPDF", None))
        self.label_6.setText(QCoreApplication.translate("merge_pdf_view", u"\u8f93\u51fa\u540d\u79f0:", None))
        self.label_9.setText(QCoreApplication.translate("merge_pdf_view", u"\u8f93\u51fa\u76ee\u5f55:", None))
        self.btn_merge.setText(QCoreApplication.translate("merge_pdf_view", u"\u5f00\u59cb\u5408\u5e76", None))
        self.label_5.setText(QCoreApplication.translate("merge_pdf_view", u"\u5b89\u5168\u8bbe\u7f6e:", None))
        self.label_10.setText(QCoreApplication.translate("merge_pdf_view", u".pdf", None))
        self.checkBox_watermark.setText(QCoreApplication.translate("merge_pdf_view", u"\u81ea\u5b9a\u4e49\u6c34\u5370", None))
        self.checkBox_doc_encrypt.setText(QCoreApplication.translate("merge_pdf_view", u"\u6587\u6863\u52a0\u5bc6", None))
        self.comboBox_output_dir.setItemText(0, QCoreApplication.translate("merge_pdf_view", u"PDF\u76f8\u540c\u76ee\u5f55", None))
        self.comboBox_output_dir.setItemText(1, QCoreApplication.translate("merge_pdf_view", u"\u81ea\u5b9a\u4e49\u76ee\u5f55", None))

        self.btn_choose_output_dir.setText(QCoreApplication.translate("merge_pdf_view", u"\u00b7\u00b7\u00b7", None))
        self.label_output_dir.setText(QCoreApplication.translate("merge_pdf_view", u"\u76ee\u5f55", None))
    # retranslateUi

