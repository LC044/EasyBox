import sys
import traceback
from app.config import version
from app.log.exception_handling import ExceptionHanding
from app.ui.Icon import Icon
from multiprocessing import freeze_support

widget = None


def excepthook(exc_type, exc_value, traceback_):
    # 将异常信息转为字符串
    # 在这里处理全局异常
    error_message = ExceptionHanding(exc_type, exc_value, traceback_)
    txt = '您可添加QQ群:620777918发送日志文件以便解决该问题\n入群密码：memotrace0806'
    msg = f"Exception Type: {exc_type.__name__}\nException Value: {exc_value}\ndetails: {error_message}\n\n{txt}"

    logger.error(f'程序发生了错误:\n\n{msg}')
    # 创建一个 QMessageBox 对象
    error_box = QMessageBox()
    # 设置对话框的标题
    error_box.setWindowTitle("未知错误")
    pixmap = QPixmap(Icon.logo_ico_path)
    icon = QIcon(pixmap)
    error_box.setWindowIcon(icon)
    # 设置对话框的文本消息
    error_box.setText(msg)
    # 设置对话框的图标，使用 QMessageBox.Critical 作为图标类型
    error_box.setIcon(QMessageBox.Critical)
    # 添加一个“确定”按钮
    error_box.addButton(QMessageBox.Ok)
    # 显示对话框
    error_box.exec()
    # 调用原始的 excepthook，以便程序正常退出
    sys.__excepthook__(exc_type, exc_value, traceback_)


# 设置 excepthook
sys.excepthook = excepthook
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from app.log import logger
from app.ui import mainview

QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)


class ViewController(QWidget):
    def __init__(self):
        super().__init__()
        self.viewLogin = None
        self.viewMainWindow = None
        self.viewDecrypt = None

    def loadPCDecryptView(self):
        """
        登录界面
        :return:
        """

    def loadLoginView(self):
        """
        登录界面
        :return:
        """

    def login(self, username):
        self.loadMainWinView(username)

    def loadMainWinView(self, username=''):
        """
        聊天界面
        :param username: 账号
        :return:
        """
        self.viewMainWindow = mainview.MainWinController()
        self.viewMainWindow.setWindowTitle(f"EasyBox-{version}")
        self.viewMainWindow.exitSignal.connect(self.close)
        try:
            self.viewMainWindow.show()
        except Exception as e:
            print(f"Exception: {e}")
            logger.error(traceback.format_exc())

    def close(self) -> bool:
        super().close()


if __name__ == '__main__':
    freeze_support()
    app = QApplication(sys.argv)
    font = QFont('微软雅黑', 12)  # 使用 Times New Roman 字体，字体大小为 14
    app.setFont(font)
    view = ViewController()
    widget = view.viewMainWindow
    try:
        # view.loadPCDecryptView()
        # view.loadLoginView()
        view.loadMainWinView()
        # view.show()
        # view.show_success()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Exception: {e}")
        logger.error(traceback.format_exc())
