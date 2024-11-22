from PyQt5.QtCore import pyqtSignal, QThread, QObject


class GlobalSignals(QObject):
    not_support = pyqtSignal(bool)
    information = pyqtSignal(str)  # 警告弹窗信号


globalSignals = GlobalSignals()
