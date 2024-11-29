# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'screen_record_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpinBox,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(448, 300)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(30, 40, 355, 124))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.format_label = QLabel(self.widget)
        self.format_label.setObjectName(u"format_label")

        self.gridLayout.addWidget(self.format_label, 0, 0, 1, 1)

        self.format_combo = QComboBox(self.widget)
        self.format_combo.addItem("")
        self.format_combo.addItem("")
        self.format_combo.setObjectName(u"format_combo")

        self.gridLayout.addWidget(self.format_combo, 0, 1, 1, 3)

        self.fps_label = QLabel(self.widget)
        self.fps_label.setObjectName(u"fps_label")

        self.gridLayout.addWidget(self.fps_label, 1, 0, 1, 1)

        self.fps_spin = QSpinBox(self.widget)
        self.fps_spin.setObjectName(u"fps_spin")

        self.gridLayout.addWidget(self.fps_spin, 1, 1, 1, 3)

        self.path_label = QLabel(self.widget)
        self.path_label.setObjectName(u"path_label")

        self.gridLayout.addWidget(self.path_label, 2, 0, 1, 1)

        self.path_edit = QLineEdit(self.widget)
        self.path_edit.setObjectName(u"path_edit")

        self.gridLayout.addWidget(self.path_edit, 2, 1, 1, 2)

        self.browse_button = QPushButton(self.widget)
        self.browse_button.setObjectName(u"browse_button")

        self.gridLayout.addWidget(self.browse_button, 2, 3, 1, 1)

        self.start_button = QPushButton(self.widget)
        self.start_button.setObjectName(u"start_button")

        self.gridLayout.addWidget(self.start_button, 3, 0, 1, 2)

        self.stop_button = QPushButton(self.widget)
        self.stop_button.setObjectName(u"stop_button")

        self.gridLayout.addWidget(self.stop_button, 3, 2, 1, 2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.format_label.setText(QCoreApplication.translate("Form", u"\u5f55\u5236\u683c\u5f0f\uff1a", None))
        self.format_combo.setItemText(0, QCoreApplication.translate("Form", u"mp4", None))
        self.format_combo.setItemText(1, QCoreApplication.translate("Form", u"avi", None))

        self.fps_label.setText(QCoreApplication.translate("Form", u"\u5e27\u7387\uff1a", None))
        self.path_label.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u8def\u5f84\uff1a", None))
        self.browse_button.setText(QCoreApplication.translate("Form", u"\u9009\u62e9\u8def\u5f84", None))
        self.start_button.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u5f55\u5236", None))
        self.stop_button.setText(QCoreApplication.translate("Form", u"\u7ed3\u675f\u5f55\u5236", None))
    # retranslateUi

