from PyQt5.QtGui import QIcon, QPixmap

from app.ui.resources import resource_rc

var = resource_rc.qt_resource_name


class Icon:
    logo_path = ':/icons/icons/logo.png'
    logo_ico_path = ':/icons/icons/logo.png'
    # MainWindow_Icon = QIcon(':/icons/icons/logo.svg')
    Back = QIcon(':/icons/icons/back.svg')
    Tool_Icon = QIcon(':/icons/icons/工具箱.svg')
    Arrow_left_Icon = QIcon(':/icons/icons/arrow-left.svg')
    Arrow_right_Icon = QIcon(':/icons/icons/arrow-right.svg')
    Setting_Icon = QIcon(':/icons/icons/setting.svg')
    Add_Icon = QIcon(':/icons/icons/批量添加.svg')
    Exp_left_Icon = QIcon(':/icons/icons/左展开.svg')
    Exp_right_Icon = QIcon(':/icons/icons/右展开.svg')
    Img_Icon = QIcon(':/icons/icons/图片.svg')
    PDF_Icon = QIcon(':/icons/icons/pdf.svg')
    Doc_Transfer_Icon = QIcon(':/icons/icons/文档转换.svg')
    Batch_Icon = QIcon(':/icons/icons/批量操作.svg')
    Video_Icon = QIcon(':/icons/icons/视频.svg')
