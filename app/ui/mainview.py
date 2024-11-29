from PySide6 import QtWidgets, QtGui

from app.ui import mainwindow
from PySide6.QtCore import Signal, QFile, QIODevice, QTextStream, QSize, Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QListWidgetItem, QLabel, QPushButton, QSizePolicy, QSplitter, QMessageBox

from app.ui.Icon import Icon
from app.ui.components.QCursorGif import QCursorGif
from app.ui.components.router import Router
from app.ui.components import Sidebar, SidebarButton
from app.ui.doc_convert.doc_convert import DocConvertControl
from app.ui.global_signal import globalSignals
from app.ui.image_tools.image_tool import ImageToolControl
from app.ui.memotrace_enhance.enhance import EnhanceControl
from app.ui.pdf_tools.pdf_tool import PDFToolControl
from app.ui.setting.setting import SettingWindow
from app.ui.video_tools.video_tool import VideoToolControl


class MainWinController(QMainWindow, mainwindow.Ui_MainWindow, QCursorGif):
    exitSignal = Signal(bool)
    okSignal = Signal(bool)
    childRouterSignal = Signal(str)

    # username = ''
    def __init__(self, parent=None):
        super(MainWinController, self).__init__(parent)
        self.setupUi(self)
        self.router_path = ''
        self.init_ui()
        # 设置无边框
        # self.setWindowFlag(Qt.FramelessWindowHint)
        globalSignals.not_support.connect(self.show_not_support)
        globalSignals.information.connect(self.show_information)

    def init_ui(self):
        self.initCursor([':/icons/icons/Cursors/%d.png' %
                         i for i in range(8)], self)
        self.setCursorTimeout(100)
        # pixmap = QPixmap(Icon.logo_ico_path)
        # icon = QIcon(pixmap)
        # self.setWindowIcon(icon)

        style_qss_file = QFile(":/data/resources/QSS/style.qss")
        if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
            stream = QTextStream(style_qss_file)
            style_content = stream.readAll()
            self.setStyleSheet(style_content)
            style_qss_file.close()

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # C尽可能挤压B
        # font = QtGui.QFont()
        # font.setFamily("Microsoft YaHei UI")
        # font.setPointSize(150)
        # font.setBold(True)
        # font.setWeight(50)
        # self.stackedWidget.setFont(font)
        # self.stackedWidget.setObjectName("stackedWidget")

        self.router = Router(self.stackedWidget)
        self.sidebar = Sidebar(self.stackedWidget, parent=self)
        self.sidebar.btn_setting.clicked.connect(self.show_setting)
        self.sidebar.btn_back.setText('')
        self.sidebar.btn_setting.setIcon(Icon.Setting_Icon)
        self.sidebar.btn_back.setIcon(Icon.Back)
        self.sidebar.btn_back.clicked.connect(self.router.turn_back)
        self.router.history_changed.connect(self.sidebar.set_turn_back_enable)
        self.horizontalLayout.addWidget(self.sidebar)
        self.horizontalLayout.addWidget(self.stackedWidget)

        self.setting_view = SettingWindow()

        pdf_view = PDFToolControl(self.router, parent=self)
        self.add_widget(Icon.PDF_Icon, 'PDF工具', pdf_view.router_path, pdf_view)

        # l1 = QLabel('文档转换', self)
        doc_view = DocConvertControl(self.router, parent=self)
        self.add_widget(Icon.Doc_Transfer_Icon, '文档转换', '/文档转换', doc_view)

        image_view = ImageToolControl(self.router, parent=self)
        self.add_widget(Icon.Img_Icon, '图片工具', '/图片工具', image_view)

        # Screen_record_view = ScreenRecordControl(self.router, parent=self)
        Video_view = VideoToolControl(self.router, parent=self)
        self.add_widget(Icon.Video_Icon, '视频工具', '/视频工具', Video_view)

        l4 = QLabel('批量操作', self)
        self.add_widget(Icon.Batch_Icon, '批量操作', '/批量操作', l4)

        enhance_view = EnhanceControl(self.router, parent=self)
        self.add_widget(Icon.Tool_Icon, '留痕增强', '/留痕增强', enhance_view)

        # 连接信号槽：切换选中按钮样式
        self.router.route_changed.connect(self.sidebar.update_sidebar_selection)
        self.router.navigate(pdf_view.router_path)  # 初始页面

    def add_widget(self, icon, text, router_path, widget):
        # """ 创建侧边栏按钮并连接路径导航 """

        self.sidebar.add_nav_button(icon, text, router_path, action=lambda: self.router.navigate(router_path))
        index = self.router.add_route(router_path, widget)

    def show_setting(self):
        self.setting_view.show()

    def show_not_support(self, a):
        self.show_information('暂不支持该功能！')

    def show_information(self, msg):
        QMessageBox.information(self, '温馨提示', msg)
