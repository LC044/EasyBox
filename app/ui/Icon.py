from PySide6.QtGui import QIcon

import resource_rc

var = resource_rc.qt_resource_name


class Icon:
    logo_path = ':/icons/resources/icons/logo.png'
    logo_ico_path = ':/icons/resources/icons/logo.ico'
    # MainWindow_Icon = QIcon(':/icons/icons/logo.svg')
    Back = QIcon(':/icons/resources/icons/back.svg')
    Tool_Icon = QIcon(':/icons/resources/icons/工具箱.svg')
    Arrow_left_Icon = QIcon(':/icons/resources/icons/arrow-left.svg')
    Arrow_right_Icon = QIcon(':/icons/resources/icons/arrow-right.svg')
    Setting_Icon = QIcon(':/icons/resources/icons/setting.svg')
    Add_Icon = QIcon(':/icons/icons/resources/批量添加.svg')
    Exp_left_Icon = QIcon(':/icons/resources/icons/左展开.svg')
    Exp_right_Icon = QIcon(':/icons/resources/icons/右展开.svg')
    Img_Icon = QIcon(':/icons/resources/icons/图片.svg')
    PDF_Icon = QIcon(':/icons/resources/icons/pdf.svg')
    Doc_Transfer_Icon = QIcon(':/icons/resources/icons/文档转换.svg')
    Batch_Icon = QIcon(':/icons/resources/icons/批量操作.svg')
    Video_Icon = QIcon(':/icons/resources/icons/视频.svg')
