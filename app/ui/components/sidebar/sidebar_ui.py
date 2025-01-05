# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sidebar_ui.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHBoxLayout,
    QListView, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Sidebar(object):
    def setupUi(self, Sidebar):
        if not Sidebar.objectName():
            Sidebar.setObjectName(u"Sidebar")
        Sidebar.resize(291, 807)
        Sidebar.setAutoFillBackground(False)
        Sidebar.setStyleSheet(u"QWidget{\n"
"       background: rgb(235,238,241);\n"
"	border:none;\n"
" }\n"
"QFrame{\n"
"	border-right: 1px solid  rgb(227,228,222);\n"
"}\n"
"QListWidget {\n"
"margin-left:0px;\n"
"    border:none;\n"
"}\n"
"QListWidget::item{\n"
"border:none;\n"
"}\n"
"QListWidget::item:hover {\n"
"border:none;\n"
"}\n"
"/*\u88ab\u9009\u4e2d\u65f6\u7684\u80cc\u666f\u989c\u8272\u548c\u5de6\u8fb9\u6846\u989c\u8272*/\n"
"QListWidget::item:selected {\n"
"border:none;\n"
"}")
        self.verticalLayout = QVBoxLayout(Sidebar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 0, 2, 9)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_back = QPushButton(Sidebar)
        self.btn_back.setObjectName(u"btn_back")
        self.btn_back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.btn_back)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_toggle = QPushButton(Sidebar)
        self.btn_toggle.setObjectName(u"btn_toggle")
        self.btn_toggle.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.btn_toggle)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.listWidget = QListWidget(Sidebar)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMinimumSize(QSize(0, 240))
        self.listWidget.setStyleSheet(u"")
        self.listWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.listWidget.setFrameShadow(QFrame.Shadow.Plain)
        self.listWidget.setLineWidth(0)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.listWidget.setAutoScroll(True)
        self.listWidget.setAutoScrollMargin(16)
        self.listWidget.setTabKeyNavigation(True)
        self.listWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.listWidget.setResizeMode(QListView.ResizeMode.Adjust)
        self.listWidget.setViewMode(QListView.ViewMode.ListMode)

        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btn_setting = QPushButton(Sidebar)
        self.btn_setting.setObjectName(u"btn_setting")
        self.btn_setting.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.btn_setting)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Sidebar)

        QMetaObject.connectSlotsByName(Sidebar)
    # setupUi

    def retranslateUi(self, Sidebar):
        Sidebar.setWindowTitle(QCoreApplication.translate("Sidebar", u"Form", None))
        self.btn_back.setText(QCoreApplication.translate("Sidebar", u"\u8fd4\u56de", None))
        self.btn_toggle.setText(QCoreApplication.translate("Sidebar", u"\u6298\u53e0", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Sidebar", u"\u65b0\u5efa\u9879\u76ee", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Sidebar", u"\u65b0\u5efa\u9879\u76ee", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("Sidebar", u"\u65b0\u5efa\u9879\u76ee", None));
        ___qlistwidgetitem3 = self.listWidget.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("Sidebar", u"\u65b0\u5efa\u9879\u76ee", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.btn_setting.setText(QCoreApplication.translate("Sidebar", u"\u8bbe\u7f6e", None))
    # retranslateUi

