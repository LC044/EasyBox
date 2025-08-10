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
        Sidebar.resize(188, 807)
        Sidebar.setAutoFillBackground(False)
        Sidebar.setStyleSheet(u"")
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

        self.listWidgetSidebar = QListWidget(Sidebar)
        QListWidgetItem(self.listWidgetSidebar)
        QListWidgetItem(self.listWidgetSidebar)
        QListWidgetItem(self.listWidgetSidebar)
        QListWidgetItem(self.listWidgetSidebar)
        self.listWidgetSidebar.setObjectName(u"listWidgetSidebar")
        self.listWidgetSidebar.setMinimumSize(QSize(0, 240))
        self.listWidgetSidebar.setStyleSheet(u"")
        self.listWidgetSidebar.setFrameShape(QFrame.Shape.NoFrame)
        self.listWidgetSidebar.setFrameShadow(QFrame.Shadow.Plain)
        self.listWidgetSidebar.setLineWidth(0)
        self.listWidgetSidebar.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.listWidgetSidebar.setAutoScroll(True)
        self.listWidgetSidebar.setAutoScrollMargin(16)
        self.listWidgetSidebar.setTabKeyNavigation(True)
        self.listWidgetSidebar.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.listWidgetSidebar.setResizeMode(QListView.ResizeMode.Adjust)
        self.listWidgetSidebar.setViewMode(QListView.ViewMode.ListMode)

        self.verticalLayout.addWidget(self.listWidgetSidebar)

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
        Sidebar.setWindowTitle("")
        self.btn_back.setText(QCoreApplication.translate("Sidebar", u"\u8fd4\u56de", None))
        self.btn_toggle.setText(QCoreApplication.translate("Sidebar", u"\u6298\u53e0", None))

        __sortingEnabled = self.listWidgetSidebar.isSortingEnabled()
        self.listWidgetSidebar.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidgetSidebar.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Sidebar", u"\u65b0\u5efa\u9879\u76ee", None));
        ___qlistwidgetitem1 = self.listWidgetSidebar.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("Sidebar", u"\u65b0\u5efa\u9879\u76ee", None));
        ___qlistwidgetitem2 = self.listWidgetSidebar.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("Sidebar", u"\u65b0\u5efa\u9879\u76ee", None));
        ___qlistwidgetitem3 = self.listWidgetSidebar.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("Sidebar", u"\u65b0\u5efa\u9879\u76ee", None));
        self.listWidgetSidebar.setSortingEnabled(__sortingEnabled)

        self.btn_setting.setText(QCoreApplication.translate("Sidebar", u"\u8bbe\u7f6e", None))
    # retranslateUi

