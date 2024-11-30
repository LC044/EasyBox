# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'web2pdf_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QProgressBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)
import resource_rc

class Ui_web2pdf_view(object):
    def setupUi(self, web2pdf_view):
        if not web2pdf_view.objectName():
            web2pdf_view.setObjectName(u"web2pdf_view")
        web2pdf_view.resize(806, 887)
        web2pdf_view.setStyleSheet(u"QLineEdit {\n"
"    background: transparent;\n"
"    border-radius: 10px;\n"
"    border: 1px solid rgb(227, 228, 222);\n"
"    border-style: outset;\n"
"    background-color: rgb(247, 248, 252);\n"
"    /* Adding a linear gradient from left to right */\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 rgba(230, 235, 246, 255), stop: 1 rgba(242, 233, 242, 255));\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    background-color: rgb(238, 241, 248);\n"
"}\n"
"")
        self.verticalLayout_3 = QVBoxLayout(web2pdf_view)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_8 = QLabel(web2pdf_view)
        self.label_8.setObjectName(u"label_8")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_3.addWidget(self.label_8)

        self.tabWidget = QTabWidget(web2pdf_view)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.North)
        self.tabWidget.setIconSize(QSize(16, 16))
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.lineEdit = QLineEdit(self.tab)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy1)
        self.lineEdit.setMinimumSize(QSize(0, 40))
        self.lineEdit.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit.setMaxLength(99999)

        self.horizontalLayout.addWidget(self.lineEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.scrollArea = QScrollArea(self.tab)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 762, 676))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget_urls = QWidget(self.scrollAreaWidgetContents)
        self.widget_urls.setObjectName(u"widget_urls")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.widget_urls.sizePolicy().hasHeightForWidth())
        self.widget_urls.setSizePolicy(sizePolicy2)
        self.widget_urls.setMinimumSize(QSize(0, 100))
        self.widget_urls.setStyleSheet(u"QPushButton{\n"
"    background: transparent;\n"
"    border-radius: 10px;\n"
"    border: 1px solid rgb(227, 228, 222);\n"
"    border-style: outset;\n"
"	padding:5px;\n"
"    background-color: rgb(247, 248, 252);\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 rgba(230, 235, 246, 255), stop: 1 rgba(242, 233, 242, 255));\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(238, 241, 248);\n"
"}\n"
"")
        self.pushButton_2 = QPushButton(self.widget_urls)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(30, 40, 121, 31))
        self.pushButton_3 = QPushButton(self.widget_urls)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(30, 90, 121, 31))
        self.pushButton_4 = QPushButton(self.widget_urls)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(190, 40, 121, 31))
        self.pushButton_5 = QPushButton(self.widget_urls)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(190, 90, 121, 31))
        self.pushButton_6 = QPushButton(self.widget_urls)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(330, 40, 121, 31))
        self.pushButton_7 = QPushButton(self.widget_urls)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(330, 90, 121, 31))

        self.verticalLayout_4.addWidget(self.widget_urls)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_2 = QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButton = QPushButton(self.tab_2)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_2.addWidget(self.pushButton)

        self.listWidget = QListWidget(self.tab_2)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout_2.addWidget(self.listWidget)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.progressBar = QProgressBar(web2pdf_view)
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
        self.comboBox_output_dir = QComboBox(web2pdf_view)
        self.comboBox_output_dir.addItem("")
        self.comboBox_output_dir.addItem("")
        self.comboBox_output_dir.addItem("")
        self.comboBox_output_dir.addItem("")
        self.comboBox_output_dir.setObjectName(u"comboBox_output_dir")

        self.gridLayout.addWidget(self.comboBox_output_dir, 0, 1, 1, 1)

        self.btn_choose_output_dir = QPushButton(web2pdf_view)
        self.btn_choose_output_dir.setObjectName(u"btn_choose_output_dir")

        self.gridLayout.addWidget(self.btn_choose_output_dir, 0, 4, 1, 1)

        self.label_9 = QLabel(web2pdf_view)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)

        self.label_output_dir = QLabel(web2pdf_view)
        self.label_output_dir.setObjectName(u"label_output_dir")
        self.label_output_dir.setMinimumSize(QSize(150, 0))

        self.gridLayout.addWidget(self.label_output_dir, 0, 2, 1, 2)


        self.horizontalLayout_4.addLayout(self.gridLayout)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.btn_start = QPushButton(web2pdf_view)
        self.btn_start.setObjectName(u"btn_start")
        self.btn_start.setMinimumSize(QSize(60, 40))
        self.btn_start.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout_4.addWidget(self.btn_start)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.retranslateUi(web2pdf_view)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(web2pdf_view)
    # setupUi

    def retranslateUi(self, web2pdf_view):
        web2pdf_view.setWindowTitle(QCoreApplication.translate("web2pdf_view", u"Form", None))
        self.label_8.setText(QCoreApplication.translate("web2pdf_view", u"\u7f51\u9875\u8f6cPDF", None))
        self.pushButton_2.setText(QCoreApplication.translate("web2pdf_view", u"http://baidu.com", None))
        self.pushButton_3.setText(QCoreApplication.translate("web2pdf_view", u"http://baidu.com", None))
        self.pushButton_4.setText(QCoreApplication.translate("web2pdf_view", u"http://baidu.com", None))
        self.pushButton_5.setText(QCoreApplication.translate("web2pdf_view", u"http://baidu.com", None))
        self.pushButton_6.setText(QCoreApplication.translate("web2pdf_view", u"http://baidu.com", None))
        self.pushButton_7.setText(QCoreApplication.translate("web2pdf_view", u"http://baidu.com", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("web2pdf_view", u"\u624b\u52a8\u8f93\u5165", None))
        self.pushButton.setText(QCoreApplication.translate("web2pdf_view", u"PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("web2pdf_view", u"\u5bfc\u5165\u6587\u4ef6", None))
        self.comboBox_output_dir.setItemText(0, QCoreApplication.translate("web2pdf_view", u"\u684c\u9762", None))
        self.comboBox_output_dir.setItemText(1, QCoreApplication.translate("web2pdf_view", u"\u4e0b\u8f7d\u76ee\u5f55", None))
        self.comboBox_output_dir.setItemText(2, QCoreApplication.translate("web2pdf_view", u"\u6587\u6863\u76ee\u5f55", None))
        self.comboBox_output_dir.setItemText(3, QCoreApplication.translate("web2pdf_view", u"\u81ea\u5b9a\u4e49\u76ee\u5f55", None))

        self.btn_choose_output_dir.setText(QCoreApplication.translate("web2pdf_view", u"\u00b7\u00b7\u00b7", None))
        self.label_9.setText(QCoreApplication.translate("web2pdf_view", u"\u8f93\u51fa\u76ee\u5f55:", None))
        self.label_output_dir.setText(QCoreApplication.translate("web2pdf_view", u"\u76ee\u5f55", None))
        self.btn_start.setText(QCoreApplication.translate("web2pdf_view", u"\u5f00\u59cb", None))
    # retranslateUi

