import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel

class ScreenRecorderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Screen Recorder")
        self.setGeometry(200, 200, 300, 150)

        # 创建按钮和标签
        self.start_button = QPushButton("Start Recording", self)
        self.stop_button = QPushButton("Stop Recording", self)
        self.status_label = QLabel("Status: Idle", self)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

        # 按钮事件
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)

        self.recording_process = None

    def start_recording(self):
        self.status_label.setText("Status: Recording...")
        # 使用 FFmpeg 开始屏幕录制
        command = [
            r"E:\Project\Python\MemoTrace\app\resources\data\ffmpeg.exe",
            "-f", "x11grab",        # X11屏幕抓取
            "-s", "1920x1080",      # 分辨率
            "-i", ":0.0",           # 输入设备，屏幕
            r"E:\Project\Python\EasyBox\screenshot\output.mp4"            # 输出文件
        ]
        # 启动子进程
        self.recording_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_recording(self):
        self.status_label.setText("Status: Stopped")
        if self.recording_process:
            self.recording_process.terminate()  # 终止录制进程
            self.recording_process = None
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenRecorderApp()
    window.show()
    sys.exit(app.exec_())
