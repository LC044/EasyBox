from multiprocessing import Process

from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import pyqtSignal, QThread, QSize, QFile, QIODevice, QTextStream, QTimer, QDateTime
from PyQt5.QtGui import QPixmap, QIcon, QGuiApplication

from app.ui.Icon import Icon
from app.ui.components.QCursorGif import QCursorGif
from app.ui.screen_record.screen_record_ui import Ui_Form
from app.ui.components.router import Router
from app.ui.global_signal import globalSignals

import numpy as np
import cv2
import threading
import queue
import time


class ScreenRecordControl(QWidget, Ui_Form, QCursorGif):
    DecryptSignal = pyqtSignal(str)
    get_wxidSignal = pyqtSignal(str)
    versionErrorSignal = pyqtSignal(str)
    childRouterSignal = pyqtSignal(str)

    def __init__(self, router: Router, parent=None):
        super(ScreenRecordControl, self).__init__(parent)
        self.router = router
        self.router_path = (self.parent().router_path if self.parent() else '') + '/录屏工具'
        self.child_routes = {}
        # 获取主屏幕对象
        self.screen = QGuiApplication.primaryScreen()
        self.dpr = self.screen.devicePixelRatio()
        self.height, self.width = int(self.screen.size().height() * self.dpr), int(self.screen.size().width() * self.dpr)
        self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # 默认使用 mp4v 编码器
        self.recording = False
        self.output_path = ""
        self.format = "mp4"
        self.fps = 20
        self.timer = QTimer()
        self.timer.timeout.connect(self.record_frame)
        self.frames = queue.Queue()
        self.stop_event = threading.Event()
        self.writer_thread = None
        self.capture_thread = None
        self.setupUi(self)
        # 设置忙碌光标图片数组
        self.initCursor([':/icons/icons/Cursors/%d.png' %
                         i for i in range(8)], self)
        self.setCursorTimeout(100)
        self.init_ui()

    def init_ui(self):
        if not self.parent():
            pixmap = QPixmap(Icon.logo_ico_path)
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)
            self.setWindowTitle('录屏工具')
            style_qss_file = QFile(":/data/QSS/style.qss")
            if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(style_qss_file)
                style_content = stream.readAll()
                self.setStyleSheet(style_content)
                style_qss_file.close()
        self.format_combo.currentTextChanged.connect(self.update_format)
        self.fps_spin.valueChanged.connect(self.update_fps)
        self.browse_button.clicked.connect(self.choose_path)
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)

    def update_format(self, format):
        self.format = format
        if format == "avi":
            self.fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        else:
            self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    def update_fps(self, fps):
        self.fps = fps

    def choose_path(self):
        now = QDateTime.currentDateTime()
        self.filename = f"录屏_{now.toString('yyyyMMddHHmmss')}.{self.format}"
        file_dialog = QFileDialog.getSaveFileName(self, "保存文件", self.filename, f"视频文件 (*.{self.format})")
        if file_dialog[0]:
            self.output_path = file_dialog[0]
            self.path_edit.setText(self.output_path)

    def start_recording(self):
        if not self.output_path:
            globalSignals.information.emit("请先选择保存路径")
            return
        self.recording = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        # Initialize threads
        self.stop_event.clear()
        self.capture_thread = threading.Thread(target=self.capture_frames)
        # self.capture_thread = Process(target=self.capture_frames, args=())
        self.writer_thread = threading.Thread(target=self.write_frames)
        # self.writer_thread = Process(target=self.write_frames, args=())

        # Start threads
        self.capture_thread.start()
        self.writer_thread.start()
        # self.timer.start(int(5))

    def capture_frames(self):
        next_time = time.perf_counter()
        while not self.stop_event.is_set():
            interval = 1.0 / self.fps  # 每帧的时间间隔
            now = time.perf_counter()
            if now >= next_time or abs(now - next_time) < 0.1 / self.fps:
                self.record_frame()
                next_time += interval
            time.sleep(0.001)

    def record_frame(self):
        if not self.screen:
            globalSignals.information.emit("无法获取屏幕对象")
            return
        print("获取时间：", QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss.zzz"))
        pixmap = self.screen.grabWindow(0)  # 0 表示捕获整个屏幕
        self.frames.put(pixmap)

    def write_frames(self):
        out = cv2.VideoWriter(self.output_path, self.fourcc, self.fps, (self.width, self.height))
        while not self.stop_event.is_set():
            if not self.frames.empty():
                pixmap = self.frames.get()
                img = pixmap.toImage()
                buffer = img.bits().asstring(img.byteCount())
                frame = np.frombuffer(buffer, dtype=np.uint8).reshape((self.height, self.width, 4))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                out.write(frame)
        out.release()

    def stop_recording(self):
        self.recording = False
        self.stop_event.set()
        # self.timer.stop()
        self.capture_thread.join()
        self.writer_thread.join()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

        globalSignals.information.emit("录制完成")


if __name__ == '__main__':
    from PyQt5.QtWidgets import QWidget, QApplication
    import sys
    from PyQt5.QtGui import QFont, QPixmap, QIcon
    from PyQt5.QtCore import Qt

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    font = QFont('微软雅黑', 10)  # 使用 Times New Roman 字体，字体大小为 14
    app.setFont(font)
    router = Router(None)
    view = ScreenRecordControl(router)
    view.show()
    sys.exit(app.exec_())
