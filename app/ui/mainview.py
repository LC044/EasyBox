from PyQt5 import QtWidgets, QtGui

from app.ui import mainwindow
from PyQt5.QtCore import pyqtSignal, QFile, QIODevice, QTextStream, QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QLabel, QPushButton, QSizePolicy, QSplitter

from app.ui.Icon import Icon
from app.ui.components.QCursorGif import QCursorGif
from app.ui.components.router import Router
from app.ui.components import Sidebar, SidebarButton
from app.ui.doc_convert.doc_convert import DocConvertControl
from app.ui.pdf_tools.pdf_tool import PDFToolControl


class MainWinController(QMainWindow, mainwindow.Ui_MainWindow, QCursorGif):
    exitSignal = pyqtSignal(bool)
    okSignal = pyqtSignal(bool)
    childRouterSignal = pyqtSignal(str)

    # username = ''
    def __init__(self, parent=None):
        super(MainWinController, self).__init__(parent)
        self.setupUi(self)
        self.router_path = ''
        self.init_ui()

    def init_ui(self):
        self.initCursor([':/icons/icons/Cursors/%d.png' %
                         i for i in range(8)], self)
        self.setCursorTimeout(100)
        pixmap = QPixmap(Icon.logo_ico_path)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)
        self.setWindowTitle('合并PDF')
        style_qss_file = QFile(":/data/QSS/style.qss")
        if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
            stream = QTextStream(style_qss_file)
            style_content = stream.readAll()
            self.setStyleSheet(style_content)
            style_qss_file.close()

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # C尽可能挤压B
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.stackedWidget.setFont(font)
        self.stackedWidget.setObjectName("stackedWidget")

        self.router = Router(self.stackedWidget)
        self.sidebar = Sidebar(self.stackedWidget, parent=self)
        self.sidebar.btn_back.setText('')
        self.sidebar.btn_setting.setIcon(Icon.Setting_Icon)
        self.sidebar.btn_back.setIcon(Icon.Back)
        self.sidebar.btn_back.clicked.connect(self.router.turn_back)
        self.router.history_changed.connect(self.sidebar.set_turn_back_enable)
        self.horizontalLayout.addWidget(self.sidebar)
        self.horizontalLayout.addWidget(self.stackedWidget)

        pdf_view = PDFToolControl(self.router, parent=self)
        self.add_widget(Icon.PDF_Icon, 'PDF工具', pdf_view.router_path, pdf_view)

        # l1 = QLabel('文档转换', self)
        doc_view = DocConvertControl(self.router, parent=self)
        self.add_widget(Icon.Doc_Transfer_Icon, '文档转换', '/文档转换', doc_view )

        l2 = QLabel('图片工具', self)
        self.add_widget(Icon.Img_Icon, '图片工具', '/图片工具', l2)

        l4 = QLabel('批量操作', self)
        self.add_widget(Icon.Batch_Icon, '批量操作', '/批量操作', l4)

        l3 = QLabel('留痕增强', self)
        self.add_widget(Icon.Tool_Icon, '留痕增强', '/留痕增强', l3)

        # 连接信号槽：切换选中按钮样式
        self.router.route_changed.connect(self.sidebar.update_sidebar_selection)
        self.router.navigate(pdf_view.router_path)  # 初始页面

    def add_widget(self, icon, text, router_path, widget):
        # """ 创建侧边栏按钮并连接路径导航 """

        self.sidebar.add_nav_button(icon, text, router_path, action=lambda: self.router.navigate(router_path))
        index = self.router.add_route(router_path, widget)
