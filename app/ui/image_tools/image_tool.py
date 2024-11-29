from PySide6.QtCore import Signal, QThread, QSize, QFile, QIODevice, QTextStream
from PySide6.QtWidgets import QWidget

from app.ui.Icon import Icon
from app.ui.components.QCursorGif import QCursorGif
from app.ui.global_signal import globalSignals
from app.ui.image_tools.image_tool_ui import Ui_Form
from app.ui.image_tools.modify_date.modify_date import ModifyDateControl
from app.ui.pdf_tools.merge import MergeControl

from app.ui.components.router import Router


class ImageToolControl(QWidget, Ui_Form, QCursorGif):
    DecryptSignal = Signal(str)
    get_wxidSignal = Signal(str)
    versionErrorSignal = Signal(str)
    childRouterSignal = Signal(str)

    def __init__(self, router: Router, parent=None):
        super().__init__(parent)
        self.router = router
        self.router_path = (self.parent().router_path if self.parent() else '') + '/图片工具箱'
        self.child_routes = {}
        self.merge_view = None
        self.running_flag = False
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
            self.setWindowTitle('PDF工具箱')
            style_qss_file = QFile(":/data/QSS/style.qss")
            if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(style_qss_file)
                style_content = stream.readAll()
                self.setStyleSheet(style_content)
                style_qss_file.close()
        self.commandLinkButton_modify_date.clicked.connect(self.modify_date)

        self.commandLinkButton_modify_name_by_time.clicked.connect(globalSignals.not_support)


        self.resize(QSize(640, 480))

    def modify_date(self):
        if not self.merge_view:
            self.merge_view = ModifyDateControl(router=self.router, parent=self if self.parent() else None)
            self.merge_view.okSignal.connect(self.merge_finish)
            self.router.add_route(self.merge_view.router_path, self.merge_view)
            self.child_routes[self.merge_view.router_path] = 0
            self.childRouterSignal.emit(self.merge_view.router_path)
            self.router.navigate(self.merge_view.router_path)
        else:
            self.router.navigate(self.merge_view.router_path)

    def merge_finish(self):
        self.merge_view = None

    def __del__(self):
        self.merge_view = None


if __name__ == '__main__':
    from PySide6.QtWidgets import QWidget, QApplication
    import sys
    from PySide6.QtGui import QFont, QPixmap, QIcon
    from PySide6.QtCore import Qt

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    font = QFont('微软雅黑', 10)  # 使用 Times New Roman 字体，字体大小为 14
    app.setFont(font)
    router = Router(None)
    view = ImageToolControl(router)
    view.show()
    sys.exit(app.exec_())
