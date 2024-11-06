from app.ui import mainwindow
from PyQt5.QtCore import pyqtSignal, QFile, QIODevice, QTextStream, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QLabel

from app.ui.Icon import Icon
from app.ui.components.QCursorGif import QCursorGif
from app.ui.components.router import Router
from app.ui.pdf_tools.pdf_tool import PDFToolControl


class MainWinController(QMainWindow, mainwindow.Ui_MainWindow, QCursorGif):
    exitSignal = pyqtSignal(bool)
    okSignal = pyqtSignal(bool)
    childRouterSignal = pyqtSignal(str)

    # username = ''
    def __init__(self, parent=None):
        super(MainWinController, self).__init__(parent)
        self.setupUi(self)
        self.router_list = []
        self.child_routes = {}
        self.router_path = ''
        self.router = Router(self.stackedWidget)
        self.router.route_changed.connect(self.setCurrentClick)
        self.btn_back.clicked.connect(self.router.turn_back)
        self.listWidget.currentRowChanged.connect(self.setCurrentIndex)
        self.init_ui()
        self.router.navigate('PDF工具箱')

    def init_ui(self):
        self.initCursor([':/icons/icons/Cursors/%d.png' %
                         i for i in range(8)], self)
        self.setCursorTimeout(100)
        self.btn_setting.setObjectName('border')
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

        self.listWidget.clear()

        pdf_view = PDFToolControl(self.router, parent=self)
        self.add_widget(Icon.Tool_Icon, 'PDF工具', pdf_view.router_path, pdf_view)

        l1 = QLabel('聊天', self)
        self.add_widget(Icon.Chat_Icon, '聊天', '聊天', l1)

        l2 = QLabel('好友', self)
        self.add_widget(Icon.Contact_Icon, '好友', '好友', l2)

        l3 = QLabel('留痕增强', self)
        self.add_widget(Icon.Home_Icon, '留痕增强', '留痕增强', l3)

    def add_widget(self, icon, text, router_path, widget):
        item = QListWidgetItem(icon, text, self.listWidget)
        index = self.router.add_route(router_path, widget)
        self.router_list.append(router_path)
        self.child_routes[router_path] = len(self.router_list) - 1
        try:
            widget.childRouterSignal.connect(self.add_child_router)
        except:
            pass
        try:
            for router in widget.child_routes.keys():
                self.child_routes[router] = index
        except:
            pass

    def setCurrentIndex(self, row):
        self.router.navigate(self.router_list[row])

    def setCurrentClick(self, path):
        if path in self.child_routes:
            row = self.child_routes[path]
            self.listWidget.currentRowChanged.disconnect()
            self.listWidget.setCurrentRow(row)
            self.listWidget.currentRowChanged.connect(self.setCurrentIndex)

    def add_child_router(self, path):
        path = path.strip('/')
        root = path.split('/')
        self.child_routes[root[-1]] = self.child_routes[root[0]]

    def turn_back(self):
        self.router.turn_back()
