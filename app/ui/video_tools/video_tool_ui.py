# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'video_tool_ui.ui'
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
        Form.resize(448, 292)
        Form.setStyleSheet(u"QPushButton{\n"
"    background-color: rgb(250,252,253);\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"	font-size:12pt;\n"
"    border-right: 2px solid #888888;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-bottom: 2px solid #888888;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-left: 1px solid #ffffff;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-top: 1px solid #ffffff;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"}\n"
"\n"
"\n"
"QCommandLinkButton{\n"
"    background-color: rgb(214,227,242);\n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"    border-right: 1px solid #888888;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-bottom: 1px solid #888888;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-left: 0px solid #ffffff;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-top: 0px"
                        " solid #ffffff;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"}\n"
"QPushButton:hover { \n"
"	border-right: 2px solid #888888;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-bottom: 2px solid #888888;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-left: 1px solid #ffffff;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"    border-top: 1px solid #ffffff;  /* \u6309\u94ae\u8fb9\u6846\uff0c2px\u5bbd\uff0c\u767d\u8272 */\n"
"}\n"
"QPushButton:pressed { \n"
"    background-color: lightgray;\n"
"	border: 2px solid #888888;\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 430, 274))
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
        self.line_5.setFrameShadow(QFrame.Raised)
        self.line_5.setLineWidth(5)
        self.line_5.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_3.addWidget(self.line_5, 1, 0, 1, 2)

        self.commandLinkButton_convert = QCommandLinkButton(self.widget_4)
        self.commandLinkButton_convert.setObjectName(u"commandLinkButton_convert")
        self.commandLinkButton_convert.setEnabled(True)
        self.commandLinkButton_convert.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_convert.setTabletTracking(False)
        self.commandLinkButton_convert.setFocusPolicy(Qt.StrongFocus)
        self.commandLinkButton_convert.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.commandLinkButton_convert.setToolTipDuration(-1)
        self.commandLinkButton_convert.setLayoutDirection(Qt.LeftToRight)
        self.commandLinkButton_convert.setAutoFillBackground(False)
        icon = QIcon()
        icon.addFile(u"../../../resources/icons/strategy.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_convert.setIcon(icon)
        self.commandLinkButton_convert.setCheckable(True)
        self.commandLinkButton_convert.setChecked(False)
        self.commandLinkButton_convert.setAutoRepeat(False)
        self.commandLinkButton_convert.setAutoExclusive(False)
        self.commandLinkButton_convert.setAutoDefault(False)
        self.commandLinkButton_convert.setDefault(False)

        self.gridLayout_3.addWidget(self.commandLinkButton_convert, 0, 1, 1, 1)

        self.commandLinkButton_screenshoot = QCommandLinkButton(self.widget_4)
        self.commandLinkButton_screenshoot.setObjectName(u"commandLinkButton_screenshoot")
        self.commandLinkButton_screenshoot.setEnabled(True)
        self.commandLinkButton_screenshoot.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_screenshoot.setTabletTracking(False)
        self.commandLinkButton_screenshoot.setFocusPolicy(Qt.StrongFocus)
        self.commandLinkButton_screenshoot.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.commandLinkButton_screenshoot.setToolTipDuration(-1)
        self.commandLinkButton_screenshoot.setLayoutDirection(Qt.LeftToRight)
        self.commandLinkButton_screenshoot.setAutoFillBackground(False)
        icon1 = QIcon()
        icon1.addFile(u"../../../resources/icons/PDF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_screenshoot.setIcon(icon1)
        self.commandLinkButton_screenshoot.setCheckable(True)
        self.commandLinkButton_screenshoot.setChecked(False)
        self.commandLinkButton_screenshoot.setAutoRepeat(False)
        self.commandLinkButton_screenshoot.setAutoExclusive(False)
        self.commandLinkButton_screenshoot.setAutoDefault(False)
        self.commandLinkButton_screenshoot.setDefault(False)

        self.gridLayout_3.addWidget(self.commandLinkButton_screenshoot, 0, 0, 1, 1)


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
        self.commandLinkButton_convert.setText(QCoreApplication.translate("Form", u"\u683c\u5f0f\u8f6c\u6362", None))
        self.commandLinkButton_convert.setDescription(QCoreApplication.translate("Form", u"\u89c6\u9891\u6587\u4ef6\u7c7b\u578b\u8f6c\u6362", None))
        self.commandLinkButton_screenshoot.setText(QCoreApplication.translate("Form", u"\u5f55\u5c4f", None))
        self.commandLinkButton_screenshoot.setDescription(QCoreApplication.translate("Form", u"\u5c4f\u5e55\u5f55\u5236", None))
    # retranslateUi

