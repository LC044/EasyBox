from PyQt5.QtCore import QObject, pyqtSignal


class Router(QObject):
    """ 路由管理器，用于管理页面和路由路径 """
    route_changed = pyqtSignal(str)
    history_changed = pyqtSignal(int)

    def __init__(self, stack):
        super(Router, self).__init__()
        self.stack = stack
        self.routes = {}
        self.history = []
        self.now_router_path = ''

    def add_route(self, path, widget):
        """添加路径和页面的映射"""
        index = self.stack.addWidget(widget)
        self.routes[path] = index
        return index

    def navigate(self, path, turn_back=False):
        """
        根据路径切换到对应的页面
        :param path:
        :param turn_back: 是否是返回调用的页面切换
        :return:
        """
        if self.now_router_path and not turn_back:
            self.history.append(self.now_router_path)
            self.history_changed.emit(len(self.history))
        if path in self.routes:
            self.stack.setCurrentIndex(self.routes[path])
            self.route_changed.emit(path)
            self.now_router_path = path
        else:
            print(f"Route '{path}' not found")

    def turn_back(self):
        if len(self.history) > 0:
            path = self.history.pop()
            self.navigate(path, True)
            print(f'返回:{path}')
            self.history_changed.emit(len(self.history))
            return True
        else:
            print(f'无法返回')
            return False
