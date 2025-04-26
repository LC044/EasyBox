# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'doc_convert_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QCommandLinkButton, QFrame, QGridLayout,
    QGroupBox, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(448, 524)
        Form.setStyleSheet(u"QCommandLinkButton{\n"
"    border-radius: 10px;\n"
"    padding: 8px;\n"
"}\n"
"QPushButton:hover { \n"
"	background-color: rgb(235,237,239);\n"
"}\n"
"QPushButton:pressed { \n"
"    background-color: lightgray;\n"
"	border: 2px solid #888888;\n"
"}")
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 446, 494))
        self.verticalLayout_8 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFlat(True)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.line_5 = QFrame(self.groupBox)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setStyleSheet(u"border-bottom: 2px solid #888888;")
        self.line_5.setFrameShadow(QFrame.Shadow.Raised)
        self.line_5.setLineWidth(5)
        self.line_5.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout.addWidget(self.line_5, 1, 0, 1, 2)

        self.commandLinkButton_pdf2txt = QCommandLinkButton(self.groupBox)
        self.commandLinkButton_pdf2txt.setObjectName(u"commandLinkButton_pdf2txt")
        self.commandLinkButton_pdf2txt.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commandLinkButton_pdf2txt.sizePolicy().hasHeightForWidth())
        self.commandLinkButton_pdf2txt.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(9)
        self.commandLinkButton_pdf2txt.setFont(font)
        self.commandLinkButton_pdf2txt.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_pdf2txt.setTabletTracking(False)
        self.commandLinkButton_pdf2txt.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.commandLinkButton_pdf2txt.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.commandLinkButton_pdf2txt.setToolTipDuration(-1)
        self.commandLinkButton_pdf2txt.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.commandLinkButton_pdf2txt.setAutoFillBackground(False)
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/txt.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_pdf2txt.setIcon(icon)
        self.commandLinkButton_pdf2txt.setIconSize(QSize(50, 50))
        self.commandLinkButton_pdf2txt.setCheckable(True)
        self.commandLinkButton_pdf2txt.setChecked(False)
        self.commandLinkButton_pdf2txt.setAutoRepeat(False)
        self.commandLinkButton_pdf2txt.setAutoExclusive(False)
        self.commandLinkButton_pdf2txt.setAutoDefault(False)
        self.commandLinkButton_pdf2txt.setDefault(False)

        self.gridLayout.addWidget(self.commandLinkButton_pdf2txt, 2, 0, 1, 1)

        self.commandLinkButton_pdf2excel = QCommandLinkButton(self.groupBox)
        self.commandLinkButton_pdf2excel.setObjectName(u"commandLinkButton_pdf2excel")
        self.commandLinkButton_pdf2excel.setEnabled(True)
        sizePolicy.setHeightForWidth(self.commandLinkButton_pdf2excel.sizePolicy().hasHeightForWidth())
        self.commandLinkButton_pdf2excel.setSizePolicy(sizePolicy)
        self.commandLinkButton_pdf2excel.setFont(font)
        self.commandLinkButton_pdf2excel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_pdf2excel.setTabletTracking(False)
        self.commandLinkButton_pdf2excel.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.commandLinkButton_pdf2excel.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.commandLinkButton_pdf2excel.setToolTipDuration(-1)
        self.commandLinkButton_pdf2excel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.commandLinkButton_pdf2excel.setAutoFillBackground(False)
        icon1 = QIcon()
        icon1.addFile(u":/icons/resources/icons/Excel.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_pdf2excel.setIcon(icon1)
        self.commandLinkButton_pdf2excel.setIconSize(QSize(50, 50))
        self.commandLinkButton_pdf2excel.setCheckable(False)
        self.commandLinkButton_pdf2excel.setChecked(False)
        self.commandLinkButton_pdf2excel.setAutoRepeat(False)
        self.commandLinkButton_pdf2excel.setAutoExclusive(False)
        self.commandLinkButton_pdf2excel.setAutoDefault(False)
        self.commandLinkButton_pdf2excel.setDefault(False)

        self.gridLayout.addWidget(self.commandLinkButton_pdf2excel, 2, 1, 1, 1)

        self.commandLinkButton_pdf2img = QCommandLinkButton(self.groupBox)
        self.commandLinkButton_pdf2img.setObjectName(u"commandLinkButton_pdf2img")
        self.commandLinkButton_pdf2img.setEnabled(True)
        sizePolicy.setHeightForWidth(self.commandLinkButton_pdf2img.sizePolicy().hasHeightForWidth())
        self.commandLinkButton_pdf2img.setSizePolicy(sizePolicy)
        self.commandLinkButton_pdf2img.setFont(font)
        self.commandLinkButton_pdf2img.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_pdf2img.setTabletTracking(False)
        self.commandLinkButton_pdf2img.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.commandLinkButton_pdf2img.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.commandLinkButton_pdf2img.setToolTipDuration(-1)
        self.commandLinkButton_pdf2img.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.commandLinkButton_pdf2img.setAutoFillBackground(False)
        icon2 = QIcon()
        icon2.addFile(u":/icons/resources/icons/\u56fe\u7247.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_pdf2img.setIcon(icon2)
        self.commandLinkButton_pdf2img.setIconSize(QSize(50, 50))
        self.commandLinkButton_pdf2img.setCheckable(True)
        self.commandLinkButton_pdf2img.setChecked(False)
        self.commandLinkButton_pdf2img.setAutoRepeat(False)
        self.commandLinkButton_pdf2img.setAutoExclusive(False)
        self.commandLinkButton_pdf2img.setAutoDefault(False)
        self.commandLinkButton_pdf2img.setDefault(False)

        self.gridLayout.addWidget(self.commandLinkButton_pdf2img, 0, 1, 1, 1)

        self.commandLinkButton_pdf2word = QCommandLinkButton(self.groupBox)
        self.commandLinkButton_pdf2word.setObjectName(u"commandLinkButton_pdf2word")
        self.commandLinkButton_pdf2word.setEnabled(True)
        sizePolicy.setHeightForWidth(self.commandLinkButton_pdf2word.sizePolicy().hasHeightForWidth())
        self.commandLinkButton_pdf2word.setSizePolicy(sizePolicy)
        self.commandLinkButton_pdf2word.setFont(font)
        self.commandLinkButton_pdf2word.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_pdf2word.setTabletTracking(False)
        self.commandLinkButton_pdf2word.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.commandLinkButton_pdf2word.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.commandLinkButton_pdf2word.setToolTipDuration(-1)
        self.commandLinkButton_pdf2word.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.commandLinkButton_pdf2word.setAutoFillBackground(False)
        icon3 = QIcon()
        icon3.addFile(u":/icons/resources/icons/word.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_pdf2word.setIcon(icon3)
        self.commandLinkButton_pdf2word.setIconSize(QSize(50, 50))
        self.commandLinkButton_pdf2word.setCheckable(True)
        self.commandLinkButton_pdf2word.setChecked(False)
        self.commandLinkButton_pdf2word.setAutoRepeat(False)
        self.commandLinkButton_pdf2word.setAutoExclusive(False)
        self.commandLinkButton_pdf2word.setAutoDefault(False)
        self.commandLinkButton_pdf2word.setDefault(False)

        self.gridLayout.addWidget(self.commandLinkButton_pdf2word, 0, 0, 1, 1)


        self.verticalLayout_8.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setCheckable(False)
        self.gridLayout_3 = QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.commandLinkButton_img2pdf = QCommandLinkButton(self.groupBox_2)
        self.commandLinkButton_img2pdf.setObjectName(u"commandLinkButton_img2pdf")
        self.commandLinkButton_img2pdf.setIcon(icon2)
        self.commandLinkButton_img2pdf.setIconSize(QSize(50, 50))

        self.gridLayout_3.addWidget(self.commandLinkButton_img2pdf, 0, 0, 1, 1)

        self.commandLinkButton_web2pdf = QCommandLinkButton(self.groupBox_2)
        self.commandLinkButton_web2pdf.setObjectName(u"commandLinkButton_web2pdf")
        self.commandLinkButton_web2pdf.setFont(font)
        icon4 = QIcon()
        icon4.addFile(u":/icons/resources/icons/html.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_web2pdf.setIcon(icon4)
        self.commandLinkButton_web2pdf.setIconSize(QSize(50, 50))

        self.gridLayout_3.addWidget(self.commandLinkButton_web2pdf, 0, 1, 1, 1)

        self.commandLinkButton_md2pdf = QCommandLinkButton(self.groupBox_2)
        self.commandLinkButton_md2pdf.setObjectName(u"commandLinkButton_md2pdf")
        icon5 = QIcon()
        icon5.addFile(u":/icons/resources/icons/markdown.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_md2pdf.setIcon(icon5)
        self.commandLinkButton_md2pdf.setIconSize(QSize(50, 50))

        self.gridLayout_3.addWidget(self.commandLinkButton_md2pdf, 1, 0, 1, 1)


        self.verticalLayout_8.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"\u4ecePDF\u8f6c\u6362", None))
        self.commandLinkButton_pdf2txt.setText(QCoreApplication.translate("Form", u"PDF\u8f6c\u6587\u672c", None))
        self.commandLinkButton_pdf2txt.setDescription(QCoreApplication.translate("Form", u"\u5c06PDF\u8f6c\u6362\u4e3a\u6587\u672c\u683c\u5f0f", None))
        self.commandLinkButton_pdf2excel.setText(QCoreApplication.translate("Form", u"PDF\u8f6cExcel", None))
        self.commandLinkButton_pdf2excel.setDescription(QCoreApplication.translate("Form", u"\u63d0\u53d6\u51faPDF\u4e2d\u7684\u8868\u683c\u5e76\u5c06\u5176\u8f6c\u6362\u4e3aExcel", None))
        self.commandLinkButton_pdf2img.setText(QCoreApplication.translate("Form", u"PDF\u8f6c\u56fe\u7247", None))
        self.commandLinkButton_pdf2img.setDescription(QCoreApplication.translate("Form", u"\u5c06PDF\u8f6c\u4e3a\u56fe\u50cf", None))
        self.commandLinkButton_pdf2word.setText(QCoreApplication.translate("Form", u"PDF\u8f6cWord", None))
        self.commandLinkButton_pdf2word.setDescription(QCoreApplication.translate("Form", u"\u5c06PDF\u8f6c\u4e3aWord\u683c\u5f0f", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"\u8f6c\u6362\u6210PDF", None))
        self.commandLinkButton_img2pdf.setText(QCoreApplication.translate("Form", u"\u56fe\u7247\u8f6cPDF", None))
        self.commandLinkButton_img2pdf.setDescription(QCoreApplication.translate("Form", u"\u628a\u56fe\u7247\u8f6c\u4e3aPDF\u683c\u5f0f", None))
        self.commandLinkButton_web2pdf.setText(QCoreApplication.translate("Form", u"\u7f51\u9875\u8f6cPDF", None))
        self.commandLinkButton_web2pdf.setDescription(QCoreApplication.translate("Form", u"\u628a\u7f51\u9875\u6216HTML\u6587\u4ef6\u8f6c\u6210PDF", None))
        self.commandLinkButton_md2pdf.setText(QCoreApplication.translate("Form", u"Markdown\u8f6cPDF", None))
        self.commandLinkButton_md2pdf.setDescription(QCoreApplication.translate("Form", u"\u628aMarkdown\u6587\u6863\u8f6c\u6210PDF", None))
    # retranslateUi

