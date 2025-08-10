version = '0.1.4'
contact = ''
github = ''
website = 'https://memotrace.cn/tools/'
copyright = '© 2022-2024 SiYuan'
license = ''
description = [

]
about = f'''
    版本：{version}<br>
    QQ交流群:请关注微信公众号回复：联系方式<br>
    地址：<a href='{github}'>{github}</a><br>
    官网：<a href='{website}'>{website}</a><br>
    新特性:<br>{''.join(['' + i for i in description])}<br>
    Copyright {copyright}
'''

class Theme:
    light = 0
    dark = 1
    system = 2


def get_system_theme():
    from PySide6.QtGui import QDesktopServices, QPalette
    from PySide6.QtWidgets import QApplication
    """判断当前系统是否处于深色模式"""
    app = QApplication.instance() or QApplication([])  # 确保有 QApplication 实例
    palette = app.palette()  # 获取当前调色板
    background_color = palette.color(QPalette.ColorRole.Window)  # 获取窗口背景颜色
    if background_color.lightness() < 128:  # lightness() 值小于 128 说明是深色模式
        return Theme.dark
    else:
        return Theme.light


UI_THEME_SETTING = Theme.system
UI_THEME = Theme.light