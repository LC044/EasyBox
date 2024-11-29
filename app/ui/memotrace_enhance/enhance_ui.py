# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'enhance_ui.ui'
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
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(448, 839)
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
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 430, 821))
        self.verticalLayout_8 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.widget_4 = QWidget(self.scrollAreaWidgetContents)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setStyleSheet(u"")
        self.gridLayout_3 = QGridLayout(self.widget_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.commandLinkButton_toc = QCommandLinkButton(self.widget_4)
        self.commandLinkButton_toc.setObjectName(u"commandLinkButton_toc")
        self.commandLinkButton_toc.setEnabled(True)
        font = QFont()
        font.setPointSize(12)
        self.commandLinkButton_toc.setFont(font)
        self.commandLinkButton_toc.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_toc.setTabletTracking(False)
        self.commandLinkButton_toc.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.commandLinkButton_toc.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.commandLinkButton_toc.setToolTipDuration(-1)
        self.commandLinkButton_toc.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.commandLinkButton_toc.setAutoFillBackground(False)
        icon = QIcon()
        icon.addFile(u"../../../resources/icons/strategy.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_toc.setIcon(icon)
        self.commandLinkButton_toc.setCheckable(True)
        self.commandLinkButton_toc.setChecked(False)
        self.commandLinkButton_toc.setAutoRepeat(False)
        self.commandLinkButton_toc.setAutoExclusive(False)
        self.commandLinkButton_toc.setAutoDefault(False)
        self.commandLinkButton_toc.setDefault(False)

        self.gridLayout_3.addWidget(self.commandLinkButton_toc, 0, 1, 1, 1)

        self.commandLinkButton_pdf2word = QCommandLinkButton(self.widget_4)
        self.commandLinkButton_pdf2word.setObjectName(u"commandLinkButton_pdf2word")
        self.commandLinkButton_pdf2word.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
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
        icon1 = QIcon()
        icon1.addFile(u"../../../resources/icons/PDF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_pdf2word.setIcon(icon1)
        self.commandLinkButton_pdf2word.setCheckable(True)
        self.commandLinkButton_pdf2word.setChecked(False)
        self.commandLinkButton_pdf2word.setAutoRepeat(False)
        self.commandLinkButton_pdf2word.setAutoExclusive(False)
        self.commandLinkButton_pdf2word.setAutoDefault(False)
        self.commandLinkButton_pdf2word.setDefault(False)

        self.gridLayout_3.addWidget(self.commandLinkButton_pdf2word, 0, 0, 1, 1)

        self.line_8 = QFrame(self.widget_4)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setStyleSheet(u"border-bottom: 2px solid #888888;")
        self.line_8.setFrameShadow(QFrame.Shadow.Raised)
        self.line_8.setLineWidth(5)
        self.line_8.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_3.addWidget(self.line_8, 1, 0, 1, 2)

        self.commandLinkButton_pdf2txt = QCommandLinkButton(self.widget_4)
        self.commandLinkButton_pdf2txt.setObjectName(u"commandLinkButton_pdf2txt")
        self.commandLinkButton_pdf2txt.setEnabled(True)
        self.commandLinkButton_pdf2txt.setFont(font)
        self.commandLinkButton_pdf2txt.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_pdf2txt.setTabletTracking(False)
        self.commandLinkButton_pdf2txt.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.commandLinkButton_pdf2txt.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.commandLinkButton_pdf2txt.setToolTipDuration(-1)
        self.commandLinkButton_pdf2txt.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.commandLinkButton_pdf2txt.setAutoFillBackground(False)
        icon2 = QIcon()
        icon2.addFile(u"../../../resources/icons/random.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_pdf2txt.setIcon(icon2)
        self.commandLinkButton_pdf2txt.setCheckable(True)
        self.commandLinkButton_pdf2txt.setChecked(False)
        self.commandLinkButton_pdf2txt.setAutoRepeat(False)
        self.commandLinkButton_pdf2txt.setAutoExclusive(False)
        self.commandLinkButton_pdf2txt.setAutoDefault(False)
        self.commandLinkButton_pdf2txt.setDefault(False)

        self.gridLayout_3.addWidget(self.commandLinkButton_pdf2txt, 2, 0, 1, 1)

        self.commandLinkButton_pdf2excel = QCommandLinkButton(self.widget_4)
        self.commandLinkButton_pdf2excel.setObjectName(u"commandLinkButton_pdf2excel")
        self.commandLinkButton_pdf2excel.setEnabled(True)
        self.commandLinkButton_pdf2excel.setFont(font)
        self.commandLinkButton_pdf2excel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_pdf2excel.setTabletTracking(False)
        self.commandLinkButton_pdf2excel.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.commandLinkButton_pdf2excel.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.commandLinkButton_pdf2excel.setToolTipDuration(-1)
        self.commandLinkButton_pdf2excel.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.commandLinkButton_pdf2excel.setAutoFillBackground(False)
        icon3 = QIcon()
        icon3.addFile(u"../../../resources/icons/ratio.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_pdf2excel.setIcon(icon3)
        self.commandLinkButton_pdf2excel.setCheckable(False)
        self.commandLinkButton_pdf2excel.setChecked(False)
        self.commandLinkButton_pdf2excel.setAutoRepeat(False)
        self.commandLinkButton_pdf2excel.setAutoExclusive(False)
        self.commandLinkButton_pdf2excel.setAutoDefault(False)
        self.commandLinkButton_pdf2excel.setDefault(False)

        self.gridLayout_3.addWidget(self.commandLinkButton_pdf2excel, 2, 1, 1, 1)

        self.line_5 = QFrame(self.widget_4)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setStyleSheet(u"border-bottom: 2px solid #888888;")
        self.line_5.setFrameShadow(QFrame.Shadow.Raised)
        self.line_5.setLineWidth(5)
        self.line_5.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_3.addWidget(self.line_5, 3, 0, 1, 2)


        self.verticalLayout_8.addWidget(self.widget_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.commandLinkButton_toc.setText(QCoreApplication.translate("Form", u"\u751f\u6210PDF\u76ee\u5f55", None))
        self.commandLinkButton_toc.setDescription(QCoreApplication.translate("Form", u"\u6309\u65e5\u671f\u751f\u6210PDF\u4e66\u7b7e\u76ee\u5f55", None))
        self.commandLinkButton_pdf2word.setText(QCoreApplication.translate("Form", u"PDF\u8f6cWord", None))
        self.commandLinkButton_pdf2word.setDescription(QCoreApplication.translate("Form", u"\u5c06PDF\u8f6c\u4e3aWord\u683c\u5f0f", None))
        self.commandLinkButton_pdf2txt.setText(QCoreApplication.translate("Form", u"PDF\u8f6c\u6587\u672c", None))
        self.commandLinkButton_pdf2txt.setDescription(QCoreApplication.translate("Form", u"\u5c06PDF\u8f6c\u6362\u4e3a\u6587\u672c\u683c\u5f0f", None))
        self.commandLinkButton_pdf2excel.setText(QCoreApplication.translate("Form", u"PDF\u8f6cExcel", None))
        self.commandLinkButton_pdf2excel.setDescription(QCoreApplication.translate("Form", u"\u63d0\u53d6\u51faPDF\u4e2d\u7684\u8868\u683c\u5e76\u5c06\u5176\u8f6c\u6362\u4e3aExcel", None))
    # retranslateUi

