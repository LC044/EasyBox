import json
import os.path
import re
import sys
import traceback
from urllib.parse import urljoin

from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog
from app.ui.components.QCursorGif import QCursorGif
from app import config
from app.log import logger
from .merge.merge import MergeControl
from .pdf_tool_ui import Ui_Form
from ..components.router import Router


class PDFToolControl(QWidget, Ui_Form, QCursorGif):
    DecryptSignal = pyqtSignal(str)
    get_wxidSignal = pyqtSignal(str)
    versionErrorSignal = pyqtSignal(str)
    childRouterSignal = pyqtSignal(str)

    def __init__(self, router: Router, parent=None):
        super(PDFToolControl, self).__init__(parent)
        self.router = router
        self.router_path = '/PDF工具箱'
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
        self.commandLinkButton_merge_pdf.clicked.connect(self.merge_pdf)

    def merge_pdf(self):
        if not self.merge_view:
            self.merge_view = MergeControl(router=self.router, parent=self)
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
