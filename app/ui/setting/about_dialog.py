import json
import os
import subprocess
import time

from PyQt5.QtCore import QSize, QUrl, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QDesktopServices, QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from app import config

version = '2.0.x'
contact = '701805520'
github = 'https://github.com/LC044/WeChatMsg'
website = 'https://memotrace.cn/tools/'
copyright = '© 2022-2024 忆墨痕'
license = 'GPLv3'
description = [
    '1. PDF工具箱<br>',
    '2. 文档转换<br>',
    '3. “留痕”增强<br>',
]
about = f'''
    版本：{config.version}<br>
    QQ交流群:请关注微信公众号回复：联系方式<br>
    官网：<a href='{website}'>{website}</a><br>
    新特性:<br>{''.join(['' + i for i in description])}<br>
    Copyright {copyright}
'''

from PyQt5 import QtCore, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(553, 394)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_version = QtWidgets.QLabel(Dialog)
        self.label_version.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_version.setAlignment(QtCore.Qt.AlignCenter)
        self.label_version.setObjectName("label_version")
        self.verticalLayout.addWidget(self.label_version)
        self.label_logo = QtWidgets.QLabel(Dialog)
        self.label_logo.setMinimumSize(QtCore.QSize(100, 100))
        self.label_logo.setObjectName("label_logo")
        self.verticalLayout.addWidget(self.label_logo)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout.addWidget(self.textBrowser)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_weixin = QtWidgets.QLabel(Dialog)
        self.label_weixin.setAlignment(QtCore.Qt.AlignCenter)
        self.label_weixin.setObjectName("label_weixin")
        self.verticalLayout_2.addWidget(self.label_weixin)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)  # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_version.setText(_translate("Dialog", "TextLabel"))
        self.label_logo.setText(_translate("Dialog", "logo"))
        self.label_weixin.setText(_translate("Dialog", "TextLabel"))


class AboutDialog(QDialog, Ui_Dialog):
    def __init__(self, main_window, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('关于')
        self.resize(QSize(640, 520))
        self.init_main_window(main_window)
        self.init_ui()

    def init_main_window(self, main_window):
        return

    def update_(self, url, is_update_online):
        if is_update_online:
            print('更新软件', url)
            exe_path = r'./update.exe'
            self.close()
            if os.path.exists(exe_path):
                subprocess.run(f'start /B {exe_path} --url {url}', shell=True, check=True)
            sys.exit()
        else:
            QDesktopServices.openUrl(QUrl("https://memotrace.cn/"))

    def init_ui(self):
        pixmap = QPixmap(':/icons/icons/logo.png').scaled(60, 60)
        self.label_logo.setPixmap(pixmap)
        pixmap = QPixmap(':/icons/icons/weixin.png').scaled(300, 115)
        self.label_weixin.setPixmap(pixmap)
        self.label_version.setText('《留痕》')
        self.textBrowser.setHtml(about)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.anchorClicked.connect(self.handleAnchorClicked)

    def handleAnchorClicked(self, url):
        # 打开默认浏览器
        QUrl(url).openUrl(url)

    def about(self):
        """
        关于
        """
        self.about_view.show()


class UpdateThread(QThread):
    updateSignal = pyqtSignal(dict)

    def __init__(self, check_time=False):
        super().__init__()
        self.check_time = check_time

    def run(self):
        now_time = time.time()
        try:
            with open('./app/data/info.json', "r", encoding="utf-8") as f:
                data = json.load(f)
            update_time = data.get('update_time')
            if update_time:
                if now_time - update_time < 14400 and self.check_time:
                    return
        except:
            os.makedirs('./app/data', exist_ok=True)
            data = {
                'update_time': now_time
            }
        data['update_time'] = now_time

        with open('./app/data/info.json', "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        server_url = 'https://api.memotrace.cn/update'
        data = {'version': version}
        try:
            response = requests.post(server_url, json=data)
            if response.status_code == 200:
                update_info = response.json()
                self.updateSignal.emit(update_info)
            else:
                print("检查更新失败")
        except:
            update_info = {'update_available': False}
            self.updateSignal.emit(update_info)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dialog = AboutDialog()
    result = dialog.exec_()  # 使用exec_()获取用户的操作结果
    if result == QDialog.Accepted:
        print("用户点击了导出按钮")
    else:
        print("用户点击了取消按钮")
    sys.exit(app.exec_())
