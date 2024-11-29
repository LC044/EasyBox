# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'file_item_ui.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QFrame,
    QHBoxLayout, QLabel, QProgressBar, QPushButton,
    QSizePolicy, QSpinBox, QVBoxLayout, QWidget)

class Ui_file_item_widget(object):
    def setupUi(self, file_item_widget):
        if not file_item_widget.objectName():
            file_item_widget.setObjectName(u"file_item_widget")
        file_item_widget.resize(668, 33)
        font = QFont()
        font.setPointSize(8)
        file_item_widget.setFont(font)
        file_item_widget.setAcceptDrops(True)
        file_item_widget.setStyleSheet(u"QWidget{\n"
"	background: rgb(248,248,251);\n"
"}\n"
"\n"
"QPushButton{\n"
"    border-radius: 5px;\n"
"    border:none;\n"
"	padding:0px;\n"
"}\n"
"QPushButton:hover { \n"
"    color: rgb(148,133,247)\n"
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
"}")
        self.horizontalLayout_3 = QHBoxLayout(file_item_widget)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.checkBox_name = QCheckBox(file_item_widget)
        self.checkBox_name.setObjectName(u"checkBox_name")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_name.sizePolicy().hasHeightForWidth())
        self.checkBox_name.setSizePolicy(sizePolicy)
        self.checkBox_name.setFont(font)
        self.checkBox_name.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.checkBox_name)

        self.label_size = QLabel(file_item_widget)
        self.label_size.setObjectName(u"label_size")
        self.label_size.setMinimumSize(QSize(50, 0))
        self.label_size.setMaximumSize(QSize(50, 16777215))
        self.label_size.setFont(font)
        self.label_size.setStyleSheet(u"")
        self.label_size.setFrameShape(QFrame.NoFrame)
        self.label_size.setScaledContents(False)
        self.label_size.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_size)

        self.label_page_num = QLabel(file_item_widget)
        self.label_page_num.setObjectName(u"label_page_num")
        self.label_page_num.setMinimumSize(QSize(50, 0))
        self.label_page_num.setMaximumSize(QSize(50, 16777215))
        self.label_page_num.setFont(font)
        self.label_page_num.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_page_num)

        self.widget_3 = QWidget(file_item_widget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(99, 0))
        self.widget_3.setMaximumSize(QSize(99, 16777215))
        self.widget_3.setFont(font)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.spinBox_start = QSpinBox(self.widget_3)
        self.spinBox_start.setObjectName(u"spinBox_start")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.spinBox_start.sizePolicy().hasHeightForWidth())
        self.spinBox_start.setSizePolicy(sizePolicy1)
        self.spinBox_start.setMinimumSize(QSize(46, 0))
        self.spinBox_start.setMaximumSize(QSize(46, 16777215))
        self.spinBox_start.setFont(font)
        self.spinBox_start.setAlignment(Qt.AlignCenter)
        self.spinBox_start.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_start.setMinimum(1)

        self.horizontalLayout_2.addWidget(self.spinBox_start)

        self.label_2 = QLabel(self.widget_3)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        self.label_2.setMinimumSize(QSize(6, 0))
        self.label_2.setMaximumSize(QSize(6, 16777215))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.spinBox_end = QSpinBox(self.widget_3)
        self.spinBox_end.setObjectName(u"spinBox_end")
        sizePolicy1.setHeightForWidth(self.spinBox_end.sizePolicy().hasHeightForWidth())
        self.spinBox_end.setSizePolicy(sizePolicy1)
        self.spinBox_end.setMinimumSize(QSize(46, 0))
        self.spinBox_end.setMaximumSize(QSize(46, 16777215))
        self.spinBox_end.setFont(font)
        self.spinBox_end.setAlignment(Qt.AlignCenter)
        self.spinBox_end.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spinBox_end.setMinimum(1)

        self.horizontalLayout_2.addWidget(self.spinBox_end)


        self.horizontalLayout_3.addWidget(self.widget_3)

        self.widget = QWidget(file_item_widget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(99, 0))
        self.widget.setMaximumSize(QSize(99, 16777215))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.progressBar = QProgressBar(self.widget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)

        self.label_result = QLabel(self.widget)
        self.label_result.setObjectName(u"label_result")
        self.label_result.setFont(font)

        self.verticalLayout.addWidget(self.label_result)


        self.horizontalLayout_3.addWidget(self.widget)

        self.widget_2 = QWidget(file_item_widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(99, 0))
        self.widget_2.setMaximumSize(QSize(99, 16777215))
        self.widget_2.setFont(font)
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_open = QPushButton(self.widget_2)
        self.btn_open.setObjectName(u"btn_open")
        self.btn_open.setFont(font)
        self.btn_open.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.btn_open)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        self.verticalLayout_2.addLayout(self.verticalLayout_4)

        self.btn_up = QPushButton(self.widget_2)
        self.btn_up.setObjectName(u"btn_up")
        self.btn_up.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout_2.addWidget(self.btn_up)

        self.btn_down = QPushButton(self.widget_2)
        self.btn_down.setObjectName(u"btn_down")
        self.btn_down.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout_2.addWidget(self.btn_down)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")

        self.verticalLayout_2.addLayout(self.verticalLayout_3)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.btn_delete = QPushButton(self.widget_2)
        self.btn_delete.setObjectName(u"btn_delete")
        self.btn_delete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.btn_delete)


        self.horizontalLayout_3.addWidget(self.widget_2)


        self.retranslateUi(file_item_widget)

        QMetaObject.connectSlotsByName(file_item_widget)
    # setupUi

    def retranslateUi(self, file_item_widget):
        file_item_widget.setWindowTitle(QCoreApplication.translate("file_item_widget", u"Form", None))
        self.checkBox_name.setText(QCoreApplication.translate("file_item_widget", u"\u540d\u79f0", None))
        self.label_size.setText(QCoreApplication.translate("file_item_widget", u"0M", None))
        self.label_page_num.setText(QCoreApplication.translate("file_item_widget", u"0", None))
        self.label_2.setText(QCoreApplication.translate("file_item_widget", u"-", None))
        self.label_result.setText(QCoreApplication.translate("file_item_widget", u"TextLabel", None))
#if QT_CONFIG(tooltip)
        self.btn_open.setToolTip(QCoreApplication.translate("file_item_widget", u"\u6253\u5f00\u6587\u4ef6", None))
#endif // QT_CONFIG(tooltip)
        self.btn_open.setText(QCoreApplication.translate("file_item_widget", u"\u6253\u5f00", None))
#if QT_CONFIG(tooltip)
        self.btn_up.setToolTip(QCoreApplication.translate("file_item_widget", u"\u4e0a\u79fb", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.btn_up.setWhatsThis(QCoreApplication.translate("file_item_widget", u"\u4e0a\u79fb", None))
#endif // QT_CONFIG(whatsthis)
        self.btn_up.setText(QCoreApplication.translate("file_item_widget", u"\u25b2", None))
#if QT_CONFIG(tooltip)
        self.btn_down.setToolTip(QCoreApplication.translate("file_item_widget", u"\u4e0b\u79fb", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.btn_down.setWhatsThis(QCoreApplication.translate("file_item_widget", u"\u4e0b\u79fb", None))
#endif // QT_CONFIG(whatsthis)
        self.btn_down.setText(QCoreApplication.translate("file_item_widget", u"\u25bc", None))
#if QT_CONFIG(tooltip)
        self.btn_delete.setToolTip(QCoreApplication.translate("file_item_widget", u"\u53d6\u6d88", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.btn_delete.setStatusTip(QCoreApplication.translate("file_item_widget", u"\u53d6\u6d88", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.btn_delete.setWhatsThis(QCoreApplication.translate("file_item_widget", u"\u5220\u9664\u8fd9\u4e2a\u5143\u7d20", None))
#endif // QT_CONFIG(whatsthis)
        self.btn_delete.setText(QCoreApplication.translate("file_item_widget", u"\u2718", None))
    # retranslateUi

