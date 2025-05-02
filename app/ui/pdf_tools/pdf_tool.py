from PySide6.QtCore import Signal, QThread, QSize, QFile, QIODevice, QTextStream
from PySide6.QtWidgets import QWidget

from app.ui.Icon import Icon
from app.ui.components.QCursorGif import QCursorGif
from app.ui.global_signal import globalSignals
from app.ui.pdf_tools.merge import MergeControl
from app.ui.pdf_tools.pdf_tool_ui import Ui_Form
from app.ui.components.router import Router


class PDFToolControl(QWidget, Ui_Form, QCursorGif):
    DecryptSignal = Signal(str)
    get_wxidSignal = Signal(str)
    versionErrorSignal = Signal(str)
    childRouterSignal = Signal(str)

    def __init__(self, router: Router, parent=None):
        super(PDFToolControl, self).__init__(parent)
        self.pdf2image_view = None
        self.router = router
        self.router_path = (self.parent().router_path if self.parent() else '') + '/PDF工具箱'
        self.child_routes = {}
        self.merge_view = None
        self.running_flag = False
        self.init_ui()
        self.setupUi(self)
        # 设置忙碌光标图片数组
        self.initCursor([':/icons/icons/Cursors/%d.png' %
                         i for i in range(8)], self)
        self.setCursorTimeout(100)

        self.commandLinkButton_merge_pdf.clicked.connect(self.merge_pdf)
        self.commandLinkButton_split_pdf.clicked.connect(self.split_pdf)
        self.commandLinkButton_encrypt.clicked.connect(self.encrypt_pdf)
        self.commandLinkButton_decrypt.clicked.connect(self.decrypt_pdf)
        self.commandLinkButton_delete_blank_pages.clicked.connect(globalSignals.not_support)
        self.commandLinkButton_add_watermark.clicked.connect(globalSignals.not_support)

    def init_ui(self):
        if not self.parent():
            pixmap = QPixmap(Icon.logo_ico_path)
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)
            self.setWindowTitle('PDF工具箱')
            style_qss_file = QFile(":/data/resources/QSS/style.qss")
            if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(style_qss_file)
                style_content = stream.readAll()
                self.setStyleSheet(style_content)
                style_qss_file.close()
        self.resize(QSize(640, 480))

    def merge_pdf(self):
        if not self.merge_view:
            self.merge_view = MergeControl(router=self.router, parent=self if self.parent() else None)
            self.merge_view.okSignal.connect(self.merge_finish)
            self.router.add_route(self.merge_view.router_path, self.merge_view)
            self.child_routes[self.merge_view.router_path] = 0
            self.childRouterSignal.emit(self.merge_view.router_path)
            self.router.navigate(self.merge_view.router_path)
        else:
            self.router.navigate(self.merge_view.router_path)

    def split_pdf(self):
        from app.ui.pdf_tools.split.split import SplitControl
        if not hasattr(self, 'split_view') or not self.split_view:
            self.split_view = SplitControl(router=self.router, parent=self if self.parent() else None)
            self.split_view.okSignal.connect(self.split_finish)
            self.router.add_route(self.split_view.router_path, self.split_view)
            self.child_routes[self.split_view.router_path] = 0
            self.childRouterSignal.emit(self.split_view.router_path)
            self.router.navigate(self.split_view.router_path)
        else:
            self.router.navigate(self.split_view.router_path)

    def encrypt_pdf(self):
        from app.ui.pdf_tools.security.encrypt import EncryptControl
        if not hasattr(self, 'encrypt_view') or not self.encrypt_view:
            self.encrypt_view = EncryptControl(router=self.router, parent=self if self.parent() else None)
            self.encrypt_view.okSignal.connect(self.encrypt_finish)
            self.router.add_route(self.encrypt_view.router_path, self.encrypt_view)
            self.child_routes[self.encrypt_view.router_path] = 0
            self.childRouterSignal.emit(self.encrypt_view.router_path)
            self.router.navigate(self.encrypt_view.router_path)
        else:
            self.router.navigate(self.encrypt_view.router_path)

    def decrypt_pdf(self):
        from app.ui.pdf_tools.security.decrypt import DecryptControl
        if not hasattr(self, 'decrypt_view') or not self.decrypt_view:
            self.decrypt_view = DecryptControl(router=self.router, parent=self if self.parent() else None)
            self.decrypt_view.okSignal.connect(self.decrypt_finish)
            self.router.add_route(self.decrypt_view.router_path, self.decrypt_view)
            self.child_routes[self.decrypt_view.router_path] = 0
            self.childRouterSignal.emit(self.decrypt_view.router_path)
            self.router.navigate(self.decrypt_view.router_path)
        else:
            self.router.navigate(self.decrypt_view.router_path)

    def encrypt_finish(self):
        self.encrypt_view = None

    def decrypt_finish(self):
        self.decrypt_view = None

    def split_finish(self):
        self.split_view = None

    def merge_finish(self):
        self.merge_view = None

    def __del__(self):
        self.merge_view = None


if __name__ == '__main__':
    from PySide6.QtWidgets import QWidget, QApplication
    import sys
    from PySide6.QtGui import QFont, QPixmap, QIcon
    from PySide6.QtCore import Qt

    app = QApplication(sys.argv)
    font = QFont('微软雅黑', 10)  # 使用 Times New Roman 字体，字体大小为 14
    app.setFont(font)
    router = Router(None)
    view = PDFToolControl(router)
    view.show()
    sys.exit(app.exec())
