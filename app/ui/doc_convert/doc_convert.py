from PySide6.QtCore import Signal, QThread, QSize, QFile, QIODevice, QTextStream
from PySide6.QtWidgets import QWidget

from app.ui.Icon import Icon
from app.ui.components.QCursorGif import QCursorGif
from app.ui.doc_convert.pdf2image.pdf2image import Pdf2ImageControl
from app.ui.doc_convert.pdf2wordui.pdf2word import Pdf2WordControl
from app.ui.doc_convert.doc_convert_ui import Ui_Form
from app.ui.components.router import Router
from app.ui.global_signal import globalSignals


class DocConvertControl(QWidget, Ui_Form, QCursorGif):
    DecryptSignal = Signal(str)
    get_wxidSignal = Signal(str)
    versionErrorSignal = Signal(str)
    childRouterSignal = Signal(str)

    def __init__(self, router: Router, parent=None):
        super(DocConvertControl, self).__init__(parent)
        self.pdf2image_view = None
        self.router = router
        self.router_path = (self.parent().router_path if self.parent() else '') + '/文档转换'
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
            style_qss_file = QFile(":/data/resources/QSS/style.qss")
            if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(style_qss_file)
                style_content = stream.readAll()
                self.setStyleSheet(style_content)
                style_qss_file.close()
        self.commandLinkButton_pdf2word.clicked.connect(self.pdf2word)

        self.commandLinkButton_pdf2img.clicked.connect(self.pdf2image)
        self.commandLinkButton_pdf2txt.clicked.connect(globalSignals.not_support)
        self.commandLinkButton_pdf2excel.clicked.connect(globalSignals.not_support)
        self.commandLinkButton_md2pdf.clicked.connect(globalSignals.not_support)
        self.commandLinkButton_web2pdf.clicked.connect(globalSignals.not_support)
        self.commandLinkButton_img2pdf.clicked.connect(globalSignals.not_support)

        self.resize(QSize(640, 480))

    def pdf2word(self):
        if not self.merge_view:
            self.merge_view = Pdf2WordControl(router=self.router, parent=self if self.parent() else None)
            self.merge_view.okSignal.connect(self.merge_finish)
            self.router.add_route(self.merge_view.router_path, self.merge_view)
            self.child_routes[self.merge_view.router_path] = 0
            self.childRouterSignal.emit(self.merge_view.router_path)
            self.router.navigate(self.merge_view.router_path)
        else:
            self.router.navigate(self.merge_view.router_path)

    def pdf2image(self):
        if not self.pdf2image_view:
            self.pdf2image_view = Pdf2ImageControl(router=self.router, parent=self if self.parent() else None)
            self.pdf2image_view.okSignal.connect(self.pdf2image_finish)
            self.router.add_route(self.pdf2image_view.router_path, self.pdf2image_view)
            self.child_routes[self.pdf2image_view.router_path] = 0
            self.childRouterSignal.emit(self.pdf2image_view.router_path)
            self.router.navigate(self.pdf2image_view.router_path)
        else:
            self.router.navigate(self.pdf2image_view.router_path)

    def pdf2image_finish(self):
        self.pdf2image_view = None

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
    view = DocConvertControl(router)
    view.show()
    sys.exit(app.exec_())
