from PySide6.QtCore import Signal, QThread, QObject


class GlobalSignals(QObject):
    not_support = Signal(bool)
    information = Signal(str)  # 警告弹窗信号


globalSignals = GlobalSignals()
