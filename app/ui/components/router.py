from PySide6.QtCore import QObject, Signal


class Router(QObject):
    """ 路由管理器，用于管理页面和路由路径 """
    route_changed = Signal(str)
    history_changed = Signal(int)

    def __init__(self, stack):
        """

        :param stack: 存储页面的stackWidget组件，可通过索引直接显示某个页面，如果为None则直接调用页面的show方法显示到独立窗口上
        """
        super(Router, self).__init__()
        self.stack = stack
        self.routes = {}
        self.history = []
        self.now_router_path = ''

    def add_route(self, path, widget):
        """添加路径和页面的映射"""
        if self.stack is not None:
            index = self.stack.addWidget(widget)
            self.routes[path] = index
        else:
            self.routes[path] = widget
            index = len(self.routes)
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
            if self.stack is not None:
                self.stack.setCurrentIndex(self.routes[path])
            else:
                self.routes[path].show()
            self.route_changed.emit(path)
            self.now_router_path = path
            print('页面切换：',self.now_router_path)
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
