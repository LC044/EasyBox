# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'image_tool_ui.ui'
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
        font = QFont()
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 430, 274))
        self.verticalLayout_8 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.widget_4 = QWidget(self.scrollAreaWidgetContents)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setStyleSheet(u"")
        self.gridLayout_3 = QGridLayout(self.widget_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.line_8 = QFrame(self.widget_4)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setStyleSheet(u"border-bottom: 2px solid #888888;")
        self.line_8.setFrameShadow(QFrame.Shadow.Raised)
        self.line_8.setLineWidth(5)
        self.line_8.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_3.addWidget(self.line_8, 1, 0, 1, 2)

        self.commandLinkButton_modify_name_by_time = QCommandLinkButton(self.widget_4)
        self.commandLinkButton_modify_name_by_time.setObjectName(u"commandLinkButton_modify_name_by_time")
        self.commandLinkButton_modify_name_by_time.setEnabled(True)
        self.commandLinkButton_modify_name_by_time.setFont(font)
        self.commandLinkButton_modify_name_by_time.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_modify_name_by_time.setTabletTracking(False)
        self.commandLinkButton_modify_name_by_time.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.commandLinkButton_modify_name_by_time.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.commandLinkButton_modify_name_by_time.setToolTipDuration(-1)
        self.commandLinkButton_modify_name_by_time.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.commandLinkButton_modify_name_by_time.setAutoFillBackground(False)
        icon = QIcon()
        icon.addFile(u"../../../resources/icons/strategy.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_modify_name_by_time.setIcon(icon)
        self.commandLinkButton_modify_name_by_time.setCheckable(True)
        self.commandLinkButton_modify_name_by_time.setChecked(False)
        self.commandLinkButton_modify_name_by_time.setAutoRepeat(False)
        self.commandLinkButton_modify_name_by_time.setAutoExclusive(False)
        self.commandLinkButton_modify_name_by_time.setAutoDefault(False)
        self.commandLinkButton_modify_name_by_time.setDefault(False)

        self.gridLayout_3.addWidget(self.commandLinkButton_modify_name_by_time, 0, 1, 1, 1)

        self.commandLinkButton_modify_date = QCommandLinkButton(self.widget_4)
        self.commandLinkButton_modify_date.setObjectName(u"commandLinkButton_modify_date")
        self.commandLinkButton_modify_date.setEnabled(True)
        self.commandLinkButton_modify_date.setFont(font)
        self.commandLinkButton_modify_date.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.commandLinkButton_modify_date.setTabletTracking(False)
        self.commandLinkButton_modify_date.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.commandLinkButton_modify_date.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.commandLinkButton_modify_date.setToolTipDuration(-1)
        self.commandLinkButton_modify_date.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.commandLinkButton_modify_date.setAutoFillBackground(False)
        icon1 = QIcon()
        icon1.addFile(u"../../../resources/icons/PDF.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.commandLinkButton_modify_date.setIcon(icon1)
        self.commandLinkButton_modify_date.setCheckable(True)
        self.commandLinkButton_modify_date.setChecked(False)
        self.commandLinkButton_modify_date.setAutoRepeat(False)
        self.commandLinkButton_modify_date.setAutoExclusive(False)
        self.commandLinkButton_modify_date.setAutoDefault(False)
        self.commandLinkButton_modify_date.setDefault(False)

        self.gridLayout_3.addWidget(self.commandLinkButton_modify_date, 0, 0, 1, 1)


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
        self.commandLinkButton_modify_name_by_time.setText(QCoreApplication.translate("Form", u"\u91cd\u547d\u540d", None))
        self.commandLinkButton_modify_name_by_time.setDescription(QCoreApplication.translate("Form", u"\u6839\u636e\u62cd\u6444\u65e5\u671f\u4fee\u6539\u6587\u4ef6\u540d", None))
        self.commandLinkButton_modify_date.setText(QCoreApplication.translate("Form", u"\u4fee\u6539\u62cd\u6444\u65e5\u671f", None))
        self.commandLinkButton_modify_date.setDescription(QCoreApplication.translate("Form", u"\u6839\u636e\u6587\u4ef6\u540d\u4fee\u6539\u56fe\u7247\u7684\u62cd\u6444\u65e5\u671f", None))
    # retranslateUi

