import os.path
import sys

from PySide6.QtCore import Qt, Signal, QThread, QUrl, QFile, QIODevice, QTextStream, QStringConverter
from PySide6.QtGui import QFont, QDesktopServices, QPixmap, QIcon
from PySide6.QtWidgets import QWidget, QMessageBox, QApplication, QListWidgetItem, QLabel

from app.ui.Icon import Icon
from app.ui.global_signal import globalSignals
from app.ui.setting.about_dialog import AboutDialog
from app.ui.setting.seetingUi import Ui_Form

Stylesheet = """
"""


class SettingWindow(QWidget, Ui_Form):
    load_finish_signal = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.init_ui()
        # self.setStyleSheet(Stylesheet)

    def init_ui(self):
        pixmap = QPixmap(Icon.logo_ico_path)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)
        self.setWindowTitle('设置')
        self.listWidget.currentRowChanged.connect(self.setCurrentIndex)
        account_item = QListWidgetItem('PDF设置', self.listWidget)
        tool_item = QListWidgetItem('图片设置', self.listWidget)
        chat_item = QListWidgetItem('文件管理', self.listWidget)
        myinfo_item = QListWidgetItem('关于', self.listWidget)
        self.account_setting_window = QLabel('敬请期待', self)
        self.report_setting_window = QLabel('敬请期待', self)
        self.file_setting_window = QLabel('敬请期待', self)
        self.about_window = AboutDialog(main_window=self, parent=self)
        self.about_window.buttonBox.setVisible(False)
        self.listWidget.setCurrentRow(0)
        self.stackedWidget.addWidget(self.account_setting_window)
        self.stackedWidget.addWidget(self.report_setting_window)
        self.stackedWidget.addWidget(self.file_setting_window)
        self.stackedWidget.addWidget(self.about_window)
        style_qss_file = QFile(":/data/QSS/style.qss")
        if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
            stream = QTextStream(style_qss_file)
            stream.setEncoding(QStringConverter.Encoding.System)
            style_content = stream.readAll()
            print(style_content)
            self.setStyleSheet(style_content)
            style_qss_file.close()

    def setCurrentIndex(self, row):
        self.stackedWidget.setCurrentIndex(row)

    def logout(self, flag):
        if flag:
            globalSignals.logout.emit(True)
            self.close()

    def reload(self):
        self.account_setting_window.init_ui()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont('微软雅黑', 12)  # 使用 Times New Roman 字体，字体大小为 14
    app.setFont(font)
    view = SettingWindow()
    view.show()
    sys.exit(app.exec())
