# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pdf_tool_ui.ui'
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
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(504, 508)
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(12)
        Form.setFont(font)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 486, 490))
        self.verticalLayout_8 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.widget_4 = QWidget(self.scrollAreaWidgetContents)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setStyleSheet(u"")
        self.gridLayout_3 = QGridLayout(self.widget_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.line_5 = QFrame(self.widget_4)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setStyleSheet(u"border-bottom: 2px solid #888888;")
        self.line_5.setFrameShadow(QFrame.Shadow.Raised)
        self.line_5.setLineWidth(5)
        self.line_5.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_3.addWidget(self.line_5, 3, 0, 1, 2)

        self.line_7 = QFrame(self.widget_4)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setStyleSheet(u"border-bottom: 2px solid #888888;")
        self.line_7.setFrameShadow(QFrame.Shadow.Raised)
        self.line_7.setLineWidth(5)
        self.line_7.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_3.addWidget(self.line_7, 6, 0, 1, 2)

        self.commandLinkButton_encrypt = QCommandLinkButton(self.widget_4)
        self.commandLinkButton_encrypt.setObjectName(u"commandLinkButton_encrypt")
        self.commandLinkButton_encrypt.setEnabled(True)
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(12)
        self.commandLinkButton_encrypt.setFont(font1)
        self.commandLinkButton_encrypt.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_encrypt.setTabletTracking(False)
        self.commandLinkButton_encrypt.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.commandLinkButton_encrypt.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.commandLinkButton_encrypt.setToolTipDuration(-1)
        self.commandLinkButton_encrypt.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.commandLinkButton_encrypt.setAutoFillBackground(False)
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/\u9501.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_encrypt.setIcon(icon)
        self.commandLinkButton_encrypt.setIconSize(QSize(50, 50))
        self.commandLinkButton_encrypt.setCheckable(True)
        self.commandLinkButton_encrypt.setChecked(False)
        self.commandLinkButton_encrypt.setAutoRepeat(False)
        self.commandLinkButton_encrypt.setAutoExclusive(False)
        self.commandLinkButton_encrypt.setAutoDefault(False)
        self.commandLinkButton_encrypt.setDefault(False)

        self.gridLayout_3.addWidget(self.commandLinkButton_encrypt, 2, 0, 1, 1)

        self.commandLinkButton_decrypt = QCommandLinkButton(self.widget_4)
        self.commandLinkButton_decrypt.setObjectName(u"commandLinkButton_decrypt")
        self.commandLinkButton_decrypt.setEnabled(True)
        self.commandLinkButton_decrypt.setFont(font1)
        self.commandLinkButton_decrypt.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_decrypt.setTabletTracking(False)
        self.commandLinkButton_decrypt.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.commandLinkButton_decrypt.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.commandLinkButton_decrypt.setToolTipDuration(-1)
        self.commandLinkButton_decrypt.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.commandLinkButton_decrypt.setAutoFillBackground(False)
        icon1 = QIcon()
        icon1.addFile(u":/icons/resources/icons/\u94a5\u5319.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_decrypt.setIcon(icon1)
        self.commandLinkButton_decrypt.setIconSize(QSize(50, 50))
        self.commandLinkButton_decrypt.setCheckable(False)
        self.commandLinkButton_decrypt.setChecked(False)
        self.commandLinkButton_decrypt.setAutoRepeat(False)
        self.commandLinkButton_decrypt.setAutoExclusive(False)
        self.commandLinkButton_decrypt.setAutoDefault(False)
        self.commandLinkButton_decrypt.setDefault(False)

        self.gridLayout_3.addWidget(self.commandLinkButton_decrypt, 2, 1, 1, 1)

        self.commandLinkButton_delete_blank_pages = QCommandLinkButton(self.widget_4)
        self.commandLinkButton_delete_blank_pages.setObjectName(u"commandLinkButton_delete_blank_pages")
        self.commandLinkButton_delete_blank_pages.setEnabled(True)
        self.commandLinkButton_delete_blank_pages.setFont(font1)
        self.commandLinkButton_delete_blank_pages.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_delete_blank_pages.setTabletTracking(False)
        self.commandLinkButton_delete_blank_pages.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.commandLinkButton_delete_blank_pages.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.commandLinkButton_delete_blank_pages.setToolTipDuration(-1)
        self.commandLinkButton_delete_blank_pages.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.commandLinkButton_delete_blank_pages.setAutoFillBackground(False)
        icon2 = QIcon()
        icon2.addFile(u":/icons/resources/icons/\u5220\u9664.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_delete_blank_pages.setIcon(icon2)
        self.commandLinkButton_delete_blank_pages.setIconSize(QSize(50, 50))
        self.commandLinkButton_delete_blank_pages.setCheckable(True)
        self.commandLinkButton_delete_blank_pages.setChecked(False)
        self.commandLinkButton_delete_blank_pages.setAutoRepeat(False)
        self.commandLinkButton_delete_blank_pages.setAutoExclusive(False)
        self.commandLinkButton_delete_blank_pages.setAutoDefault(False)
        self.commandLinkButton_delete_blank_pages.setDefault(False)

        self.gridLayout_3.addWidget(self.commandLinkButton_delete_blank_pages, 5, 0, 1, 1)

        self.line_8 = QFrame(self.widget_4)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setStyleSheet(u"border-bottom: 2px solid #888888;")
        self.line_8.setFrameShadow(QFrame.Shadow.Raised)
        self.line_8.setLineWidth(5)
        self.line_8.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_3.addWidget(self.line_8, 1, 0, 1, 2)

        self.commandLinkButton_merge_pdf = QCommandLinkButton(self.widget_4)
        self.commandLinkButton_merge_pdf.setObjectName(u"commandLinkButton_merge_pdf")
        self.commandLinkButton_merge_pdf.setEnabled(True)
        self.commandLinkButton_merge_pdf.setFont(font1)
        self.commandLinkButton_merge_pdf.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_merge_pdf.setTabletTracking(False)
        self.commandLinkButton_merge_pdf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.commandLinkButton_merge_pdf.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.commandLinkButton_merge_pdf.setToolTipDuration(-1)
        self.commandLinkButton_merge_pdf.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.commandLinkButton_merge_pdf.setAutoFillBackground(False)
        icon3 = QIcon()
        icon3.addFile(u":/icons/resources/icons/\u5408\u5e76.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_merge_pdf.setIcon(icon3)
        self.commandLinkButton_merge_pdf.setIconSize(QSize(50, 50))
        self.commandLinkButton_merge_pdf.setCheckable(True)
        self.commandLinkButton_merge_pdf.setChecked(False)
        self.commandLinkButton_merge_pdf.setAutoRepeat(False)
        self.commandLinkButton_merge_pdf.setAutoExclusive(False)
        self.commandLinkButton_merge_pdf.setAutoDefault(False)
        self.commandLinkButton_merge_pdf.setDefault(False)

        self.gridLayout_3.addWidget(self.commandLinkButton_merge_pdf, 0, 0, 1, 1)

        self.commandLinkButton_split_pdf = QCommandLinkButton(self.widget_4)
        self.commandLinkButton_split_pdf.setObjectName(u"commandLinkButton_split_pdf")
        self.commandLinkButton_split_pdf.setEnabled(True)
        self.commandLinkButton_split_pdf.setFont(font1)
        self.commandLinkButton_split_pdf.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_split_pdf.setTabletTracking(False)
        self.commandLinkButton_split_pdf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.commandLinkButton_split_pdf.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.commandLinkButton_split_pdf.setToolTipDuration(-1)
        self.commandLinkButton_split_pdf.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.commandLinkButton_split_pdf.setAutoFillBackground(False)
        icon4 = QIcon()
        icon4.addFile(u":/icons/resources/icons/\u62c6\u5206.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_split_pdf.setIcon(icon4)
        self.commandLinkButton_split_pdf.setIconSize(QSize(50, 50))
        self.commandLinkButton_split_pdf.setCheckable(True)
        self.commandLinkButton_split_pdf.setChecked(False)
        self.commandLinkButton_split_pdf.setAutoRepeat(False)
        self.commandLinkButton_split_pdf.setAutoExclusive(False)
        self.commandLinkButton_split_pdf.setAutoDefault(False)
        self.commandLinkButton_split_pdf.setDefault(False)

        self.gridLayout_3.addWidget(self.commandLinkButton_split_pdf, 0, 1, 1, 1)

        self.commandLinkButton_add_watermark = QCommandLinkButton(self.widget_4)
        self.commandLinkButton_add_watermark.setObjectName(u"commandLinkButton_add_watermark")
        self.commandLinkButton_add_watermark.setFont(font1)
        icon5 = QIcon()
        icon5.addFile(u":/icons/resources/icons/\u6c34\u5370.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_add_watermark.setIcon(icon5)
        self.commandLinkButton_add_watermark.setIconSize(QSize(50, 50))

        self.gridLayout_3.addWidget(self.commandLinkButton_add_watermark, 5, 1, 1, 1)


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
        self.commandLinkButton_encrypt.setText(QCoreApplication.translate("Form", u"PDF\u52a0\u5bc6", None))
        self.commandLinkButton_encrypt.setDescription(QCoreApplication.translate("Form", u"\u8bbe\u7f6ePDF\u6253\u5f00\u3001\u7f16\u8f91\u5bc6\u7801", None))
        self.commandLinkButton_decrypt.setText(QCoreApplication.translate("Form", u"PDF\u89e3\u5bc6", None))
        self.commandLinkButton_decrypt.setDescription(QCoreApplication.translate("Form", u"\u4ecePDF\u6587\u6863\u4e2d\u79fb\u9664\u5bc6\u7801\u4fdd\u62a4", None))
        self.commandLinkButton_delete_blank_pages.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u7a7a\u767d\u9875", None))
        self.commandLinkButton_delete_blank_pages.setDescription(QCoreApplication.translate("Form", u"\u6279\u91cf\u5220\u9664PDF\u6587\u4ef6\u4e2d\u7684\u7a7a\u767d\u9875", None))
        self.commandLinkButton_merge_pdf.setText(QCoreApplication.translate("Form", u"\u5408\u5e76", None))
        self.commandLinkButton_merge_pdf.setDescription(QCoreApplication.translate("Form", u"\u5408\u5e76\u591a\u4e2aPDF\u4e3a\u4e00\u4e2a", None))
        self.commandLinkButton_split_pdf.setText(QCoreApplication.translate("Form", u"\u62c6\u5206", None))
        self.commandLinkButton_split_pdf.setDescription(QCoreApplication.translate("Form", u"\u628a\u4e00\u4e2aPDF\u62c6\u5206\u6210\u591a\u4e2a", None))
        self.commandLinkButton_add_watermark.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0\u6c34\u5370", None))
        self.commandLinkButton_add_watermark.setDescription(QCoreApplication.translate("Form", u"\u5728PDF\u4e2d\u6dfb\u52a0\u81ea\u5b9a\u4e49\u6c34\u5370", None))
    # retranslateUi

