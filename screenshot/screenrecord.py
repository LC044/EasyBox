import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QMessageBox
)
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import QTimer, QThread, pyqtSignal


class ScreenRecorder(QThread):
    recording_started = pyqtSignal()
    recording_stopped = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, output_file):
        super().__init__()
        self.output_file = output_file
        self.recording = False

    def run(self):
        try:
            screen = QGuiApplication.primaryScreen()
            if not screen:
                self.error_occurred.emit("未找到主屏幕，无法录制。")
                return

            size = screen.size()
            width, height = size.width(), size.height()
            print(f"屏幕尺寸: {width}x{height}")
            fps = 20  # 帧率

            # 初始化视频写入器
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(self.output_file, fourcc, fps, (width, height))

            self.recording = True
            self.recording_started.emit()

            while self.recording:
                pixmap = screen.grabWindow(0)
                img = pixmap.toImage()
                buffer = img.bits().asstring(img.byteCount())
                frame = np.frombuffer(buffer, dtype=np.uint8).reshape((height, width, 4))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                out.write(frame)
                self.msleep(int(1000 / fps))  # 控制帧率

            out.release()
            self.recording_stopped.emit()

        except Exception as e:
            self.error_occurred.emit(str(e))

    def stop(self):
        self.recording = False


class RecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("屏幕录制软件")
        self.setGeometry(100, 100, 300, 200)

        self.recorder = None
        self.output_file = None

        # 设置界面
        layout = QVBoxLayout()
        self.label_status = QLabel("状态: 未录制")
        layout.addWidget(self.label_status)

        self.btn_start = QPushButton("开始录制")
        self.btn_start.clicked.connect(self.start_recording)
        layout.addWidget(self.btn_start)

        self.btn_stop = QPushButton("停止录制")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_recording)
        layout.addWidget(self.btn_stop)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_recording(self):
        # 选择输出文件
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.output_file, _ = QFileDialog.getSaveFileName(
            self, "保存视频", "", "MP4 文件 (*.mp4);;所有文件 (*)", options=options
        )

        if not self.output_file:
            QMessageBox.warning(self, "未选择文件", "请先选择保存路径。")
            return

        self.recorder = ScreenRecorder(self.output_file)
        self.recorder.recording_started.connect(self.on_recording_started)
        self.recorder.recording_stopped.connect(self.on_recording_stopped)
        self.recorder.error_occurred.connect(self.on_error_occurred)
        self.recorder.start()

    def stop_recording(self):
        if self.recorder and self.recorder.recording:
            self.recorder.stop()

    def on_recording_started(self):
        self.label_status.setText("状态: 正在录制")
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)

    def on_recording_stopped(self):
        self.label_status.setText("状态: 录制停止")
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        QMessageBox.information(self, "完成", f"视频已保存到: {self.output_file}")

    def on_error_occurred(self, error_message):
        QMessageBox.critical(self, "错误", error_message)
        self.label_status.setText("状态: 未录制")
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecorderApp()
    window.show()
    sys.exit(app.exec_())
