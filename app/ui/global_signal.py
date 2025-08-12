from PySide6.QtCore import Signal, QThread, QObject


class GlobalSignals(QObject):
    not_support = Signal(bool)
    information = Signal(str)  # 警告弹窗信号
    start_busy = Signal(bool) # 鼠标切换为忙碌状态
    stop_busy = Signal(bool) # 鼠标切换为正常状态


globalSignals = GlobalSignals()
