from PyQt5.QtCore import pyqtSignal, QThread, QObject


class GlobalSignals(QObject):
    status_bar_message = pyqtSignal(tuple)  # 全局变量，用于存储状态栏的消息
    pdf_file_name = pyqtSignal(str)  # 打印PDF的信号，值为HTML的路径
    pdf_file = pyqtSignal(tuple)  # 打印PDF的信号，(HTML临时路径, 基础文件夹)
    not_vip = pyqtSignal(bool)  # 不是VIP的信号
    audio_not_enough = pyqtSignal(bool)  # 语音余额不足的信号
    set_member_info = pyqtSignal(dict)  # 用户信息的信号
    information = pyqtSignal(str)  # 警告弹窗信号
    main_window_close = pyqtSignal(bool)
    logout = pyqtSignal(bool)


globalSignals = GlobalSignals()
