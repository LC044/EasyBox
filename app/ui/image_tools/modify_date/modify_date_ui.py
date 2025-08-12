# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'modify_date_ui.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QComboBox,
    QDateTimeEdit, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QListWidget, QListWidgetItem, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QSplitter,
    QTabWidget, QTableWidget, QTableWidgetItem, QTreeView,
    QVBoxLayout, QWidget)

class Ui_modify_date_view(object):
    def setupUi(self, modify_date_view):
        if not modify_date_view.objectName():
            modify_date_view.setObjectName(u"modify_date_view")
        modify_date_view.resize(600, 662)
        modify_date_view.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(modify_date_view)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_8 = QLabel(modify_date_view)
        self.label_8.setObjectName(u"label_8")
        font = QFont()
        font.setPointSize(20)
        self.label_8.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_8)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.dateTimeEdit = QDateTimeEdit(modify_date_view)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setFrame(True)
        self.dateTimeEdit.setAccelerated(False)
        self.dateTimeEdit.setKeyboardTracking(True)
        self.dateTimeEdit.setProperty(u"showGroupSeparator", False)
        self.dateTimeEdit.setCalendarPopup(True)

        self.horizontalLayout_2.addWidget(self.dateTimeEdit)

        self.comboBox_time_opt = QComboBox(modify_date_view)
        self.comboBox_time_opt.addItem("")
        self.comboBox_time_opt.addItem("")
        self.comboBox_time_opt.setObjectName(u"comboBox_time_opt")

        self.horizontalLayout_2.addWidget(self.comboBox_time_opt)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.splitter_3 = QSplitter(modify_date_view)
        self.splitter_3.setObjectName(u"splitter_3")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_3.sizePolicy().hasHeightForWidth())
        self.splitter_3.setSizePolicy(sizePolicy)
        self.splitter_3.setFrameShape(QFrame.Shape.Box)
        self.splitter_3.setOrientation(Qt.Orientation.Horizontal)
        self.widget_2 = QWidget(self.splitter_3)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.widget_2.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btn_choose_folder = QPushButton(self.widget_2)
        self.btn_choose_folder.setObjectName(u"btn_choose_folder")
        self.btn_choose_folder.setMaximumSize(QSize(200, 16777215))

        self.horizontalLayout_4.addWidget(self.btn_choose_folder)

        self.label_input_folder = QLabel(self.widget_2)
        self.label_input_folder.setObjectName(u"label_input_folder")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_input_folder.sizePolicy().hasHeightForWidth())
        self.label_input_folder.setSizePolicy(sizePolicy2)
        self.label_input_folder.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.horizontalLayout_4.addWidget(self.label_input_folder)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.splitter = QSplitter(self.widget_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.treeView = QTreeView(self.splitter)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setFrameShape(QFrame.Shape.Panel)
        self.treeView.setFrameShadow(QFrame.Shadow.Raised)
        self.splitter.addWidget(self.treeView)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 150))
        self.label_preview = QLabel(self.widget)
        self.label_preview.setObjectName(u"label_preview")
        self.label_preview.setGeometry(QRect(0, 0, 291, 241))
        self.label_preview.setAutoFillBackground(False)
        self.label_preview.setScaledContents(False)
        self.label_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.splitter.addWidget(self.widget)

        self.verticalLayout_3.addWidget(self.splitter)

        self.splitter_3.addWidget(self.widget_2)
        self.tabWidget = QTabWidget(self.splitter_3)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.tab)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tableWidget.setObjectName(u"tableWidget")
        font1 = QFont()
        font1.setPointSize(8)
        self.tableWidget.setFont(font1)
        self.tableWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidget.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.tableWidget)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_5 = QVBoxLayout(self.tab_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_2 = QLabel(self.tab_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_4.addWidget(self.label_2)

        self.listWidget = QListWidget(self.tab_2)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        QListWidgetItem(self.listWidget)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout_4.addWidget(self.listWidget)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.tabWidget.addTab(self.tab_2, "")
        self.splitter_3.addWidget(self.tabWidget)

        self.verticalLayout.addWidget(self.splitter_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.checkBox_apply_child = QCheckBox(modify_date_view)
        self.checkBox_apply_child.setObjectName(u"checkBox_apply_child")
        self.checkBox_apply_child.setChecked(True)

        self.horizontalLayout_3.addWidget(self.checkBox_apply_child)

        self.checkBox_compress = QCheckBox(modify_date_view)
        self.checkBox_compress.setObjectName(u"checkBox_compress")

        self.horizontalLayout_3.addWidget(self.checkBox_compress)

        self.checkBox_force_modify = QCheckBox(modify_date_view)
        self.checkBox_force_modify.setObjectName(u"checkBox_force_modify")

        self.horizontalLayout_3.addWidget(self.checkBox_force_modify)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(modify_date_view)
        self.label.setObjectName(u"label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy3)

        self.horizontalLayout_5.addWidget(self.label)

        self.comboBox_output_opt = QComboBox(modify_date_view)
        self.comboBox_output_opt.addItem("")
        self.comboBox_output_opt.addItem("")
        self.comboBox_output_opt.setObjectName(u"comboBox_output_opt")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.comboBox_output_opt.sizePolicy().hasHeightForWidth())
        self.comboBox_output_opt.setSizePolicy(sizePolicy4)

        self.horizontalLayout_5.addWidget(self.comboBox_output_opt)

        self.label_output_dir = QLabel(modify_date_view)
        self.label_output_dir.setObjectName(u"label_output_dir")
        sizePolicy2.setHeightForWidth(self.label_output_dir.sizePolicy().hasHeightForWidth())
        self.label_output_dir.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.label_output_dir)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.progressBar = QProgressBar(modify_date_view)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.progressBar)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 9, -1, -1)
        self.label_current_file = QLabel(modify_date_view)
        self.label_current_file.setObjectName(u"label_current_file")
        self.label_current_file.setMaximumSize(QSize(400, 16777215))

        self.horizontalLayout.addWidget(self.label_current_file)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_start = QPushButton(modify_date_view)
        self.btn_start.setObjectName(u"btn_start")
        self.btn_start.setMinimumSize(QSize(60, 40))

        self.horizontalLayout.addWidget(self.btn_start)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(modify_date_view)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(modify_date_view)
    # setupUi

    def retranslateUi(self, modify_date_view):
        modify_date_view.setWindowTitle(QCoreApplication.translate("modify_date_view", u"Form", None))
        self.label_8.setText(QCoreApplication.translate("modify_date_view", u"\u4fee\u6539\u56fe\u7247\u62cd\u6444\u65e5\u671f", None))
        self.dateTimeEdit.setDisplayFormat(QCoreApplication.translate("modify_date_view", u"yyyy/M/d HH:mm:ss", None))
        self.comboBox_time_opt.setItemText(0, QCoreApplication.translate("modify_date_view", u"\u6839\u636e\u6587\u4ef6\u540d\u4fee\u6539", None))
        self.comboBox_time_opt.setItemText(1, QCoreApplication.translate("modify_date_view", u"\u81ea\u5b9a\u4e49\u65f6\u95f4", None))

        self.btn_choose_folder.setText(QCoreApplication.translate("modify_date_view", u"\u9009\u62e9\u76ee\u5f55", None))
        self.label_input_folder.setText("")
        self.label_preview.setText(QCoreApplication.translate("modify_date_view", u"\u9884\u89c8", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("modify_date_view", u"\u5b57\u6bb5", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("modify_date_view", u"\u539f\u59cb\u503c", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("modify_date_view", u"\u4fee\u6539\u540e", None));
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("modify_date_view", u"  \u7ed3\u679c\u9884\u89c8", None))
        self.label_2.setText(QCoreApplication.translate("modify_date_view", u"\u5f85\u5b9e\u73b0\u529f\u80fd", None))

        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        ___qlistwidgetitem = self.listWidget.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("modify_date_view", u"\u652f\u6301\u4fee\u6539GPS\u6570\u636e", None));
        ___qlistwidgetitem1 = self.listWidget.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("modify_date_view", u"\u652f\u6301\u66f4\u591a\u6587\u4ef6\u7c7b\u578b", None));
        ___qlistwidgetitem2 = self.listWidget.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("modify_date_view", u"\u652f\u6301\u4fee\u6539\u62cd\u6444\u8bbe\u5907", None));
        ___qlistwidgetitem3 = self.listWidget.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("modify_date_view", u"\u652f\u6301\u5bfc\u51fa\u62cd\u6444\u53c2\u6570", None));
        self.listWidget.setSortingEnabled(__sortingEnabled)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("modify_date_view", u"\u8bbe\u7f6e", None))
#if QT_CONFIG(tooltip)
        self.checkBox_apply_child.setToolTip(QCoreApplication.translate("modify_date_view", u"\u4fee\u6539\u5f53\u524d\u6587\u4ef6\u5939\u53ca\u5176\u5b50\u6587\u4ef6\u5939\u4e0b\u7684\u6240\u6709\u56fe\u7247", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_apply_child.setText(QCoreApplication.translate("modify_date_view", u" \u5e94\u7528\u5230\u5b50\u6587\u4ef6\u5939", None))
        self.checkBox_compress.setText(QCoreApplication.translate("modify_date_view", u"\u56fe\u7247\u538b\u7f29", None))
#if QT_CONFIG(tooltip)
        self.checkBox_force_modify.setToolTip(QCoreApplication.translate("modify_date_view", u"\u9ed8\u8ba4\u53d6\u539f\u62cd\u6444\u65f6\u95f4\u548c\u8bbe\u5b9a\u62cd\u6444\u65f6\u95f4\u7684\u6700\u65e9\u65f6\u95f4\uff0c\u542f\u7528\u8be5\u9009\u9879\u5c06\u5f3a\u5236\u4fee\u6539\u4e3a\u6307\u5b9a\u503c", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_force_modify.setText(QCoreApplication.translate("modify_date_view", u" \u5f3a\u5236\u4fee\u6539", None))
        self.label.setText(QCoreApplication.translate("modify_date_view", u"\u8f93\u51fa\u4f4d\u7f6e\uff1a", None))
        self.comboBox_output_opt.setItemText(0, QCoreApplication.translate("modify_date_view", u"\u8986\u76d6\u539f\u56fe", None))
        self.comboBox_output_opt.setItemText(1, QCoreApplication.translate("modify_date_view", u"\u8f93\u51fa\u5230\u65b0\u6587\u4ef6\u5939", None))

        self.label_output_dir.setText("")
        self.label_current_file.setText("")
        self.btn_start.setText(QCoreApplication.translate("modify_date_view", u"\u5f00\u59cb", None))
    # retranslateUi

