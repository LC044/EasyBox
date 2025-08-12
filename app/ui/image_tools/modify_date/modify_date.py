import os.path
import shutil
import traceback
from datetime import datetime
from typing import List

from PIL import Image
import piexif
from PySide6.QtCore import Signal, QThread, QUrl, Qt, QFile, QIODevice, QTextStream, QDir, QSortFilterProxyModel
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon, QFont, QFontMetrics
from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog, QApplication, QDialog, QFileSystemModel, QTreeView, \
    QTableWidgetItem

from app import config
from app.log import logger
from app.model.file_model import ImageFile
from app.ui.Icon import Icon
from app.ui.global_signal import globalSignals
from app.ui.image_tools.modify_date.modify_date_ui import Ui_modify_date_view
from app.ui.components.router import Router
from app.ui.theme import set_theme
from app.util import common
from app.util.pyexiftool import PyExifTool


def open_file_explorer(path):
    # 使用QDesktopServices打开文件管理器
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))


image_extensions = ['jpg', 'jpeg', 'bmp', 'riff', 'webp']
video_extensions = ['mp4', 'mov', 'avi']
image_extensions_filter = ['*.jpg', '*.jpeg', '*.bmp', '*.riff', '*.webp']

exif_keys = ['DateTime', 'DateTimeOriginal', 'Make', 'Model', 'Software', 'ImageWidth', 'ImageLength']


def is_image(file_path):
    """判断文件是否为图片"""
    return any(file_path.lower().endswith(ext) for ext in image_extensions)

def is_video(file_path):
    """判断文件是否为图片"""
    return any(file_path.lower().endswith(ext) for ext in video_extensions)

class ModifyDateControl(QWidget, Ui_modify_date_view):
    okSignal = Signal(bool)
    childRouterSignal = Signal(str)

    def __init__(self, router: Router, parent=None):
        super().__init__(parent)
        self.encryption_options = {}
        self.dialog = None
        self.output_dir = ''  # 输出目标文件夹
        self.router = router
        self.router_path = (self.parent().router_path if self.parent() else '') + '/修改图片拍摄日期'
        self.child_routes = {}
        self.worker = None
        self.given_date = None
        self.running_flag = False
        self.setupUi(self)

        self.btn_choose_folder.clicked.connect(self.show_directory_dialog)
        self.comboBox_time_opt.currentIndexChanged.connect(self.set_name_rule)
        self.comboBox_output_opt.activated.connect(self.set_output_opt)
        self.dateTimeEdit.dateTimeChanged.connect(self.set_given_date)
        self.init_ui()

    def init_ui(self):
        self.btn_start.setObjectName('border')
        self.btn_choose_folder.setObjectName('border')
        self.btn_start.clicked.connect(self.start)
        self.btn_choose_folder.setIcon(Icon.PDF_Icon)
        self.dateTimeEdit.setVisible(False)
        # self.label_input_folder.s
        if not self.parent():
            pixmap = QPixmap(Icon.logo_ico_path)
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)
            self.setWindowTitle('修改图片拍摄日期')
            set_theme(self, config.UI_THEME)
        # 创建 QFileSystemModel
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())  # 设置根路径为系统的根目录

        self.treeView.setSelectionMode(QTreeView.SingleSelection)  # 单选模式
        self.treeView.clicked.connect(self.on_item_clicked)  # 监听点击事件
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(os.getcwd()))
        self.model.setNameFilters(image_extensions_filter)
        self.model.setNameFilterDisables(False)
        # 隐藏/显示列（如隐藏文件大小列等）
        self.treeView.setColumnHidden(1, True)  # 隐藏大小列
        self.treeView.setColumnHidden(2, True)  # 隐藏类型列
        self.treeView.setColumnHidden(3, True)  # 隐藏修改日期列
        self.treeView.header().setVisible(False)

        # self.label_preview.setScaledContents(True)

    def set_name_rule(self, index):
        """
        :return:
        """
        print(index, self.comboBox_output_opt.currentText())
        if index == 1:
            self.dateTimeEdit.setVisible(True)
            self.given_date = self.dateTimeEdit.dateTime().toPython()
        else:
            self.given_date = None
            self.dateTimeEdit.setVisible(False)

    def set_given_date(self):
        self.given_date = self.dateTimeEdit.dateTime().toPython()

    def set_output_opt(self, index):
        """
        设置输出文件夹
        :param index:
        :return:
        """
        print(index)
        if index == 1:
            folder = QFileDialog.getExistingDirectory(self, "选择目录")
            if folder:
                print(folder)
                self.output_dir = folder
                font_metrics = QFontMetrics(self.label_output_dir.font())
                # 使用 elidedText 根据按钮宽度生成省略文字
                elided_text = font_metrics.elidedText(folder, Qt.ElideRight, self.label_output_dir.width() - 10)
                self.label_output_dir.setText(elided_text)
        else:
            self.output_dir = ''
            self.label_output_dir.setText('')

    def closeEvent(self, a0):
        super().closeEvent(a0)
        self.okSignal.emit(True)

    def show_directory_dialog(self):
        """显示目录选择对话框并在 QTreeView 中显示该目录的内容"""
        folder = QFileDialog.getExistingDirectory(self, "选择目录")
        if folder:
            # 设置 QTreeView 的根目录为用户选择的目录
            self.treeView.setRootIndex(self.model.index(folder))
            # self.label_output_dir.setText(folder)
            # self.label_input_folder.setText(folder)
            """根据按钮宽度限制文字长度"""
            font_metrics = QFontMetrics(self.label_input_folder.font())
            # 使用 elidedText 根据按钮宽度生成省略文字
            elided_text = font_metrics.elidedText(folder, Qt.ElideRight, self.label_input_folder.width() - 10)
            self.label_input_folder.setText(elided_text)
            # self.btn_choose_folder.setText(folder)

    def on_item_clicked(self, index):
        """当点击文件时，判断是否为图片并显示该图片"""
        file_path = self.model.filePath(index)  # 获取文件的完整路径

        # 判断文件是否为图片
        if is_image(file_path):
            self.display_image(file_path)

    def display_image(self, file_path):
        """显示图片"""
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            self.label_preview.setText("无法加载图片")
        else:
            self.label_preview.resize(self.label_preview.parent().size())
            self.label_preview.setPixmap(
                pixmap.scaled(self.label_preview.parent().width(), self.label_preview.parent().height(),
                              Qt.KeepAspectRatio))  # 调整显示图片的大小
            self.show_exif_data(file_path)

    def show_exif_data(self, file_path):
        """
        显示元数据信息
        :param file_path:
        :return:
        """
        print(file_path)
        metadata = {}
        try:
            # 打开图片并加载 EXIF 数据
            img = Image.open(file_path)
            exif_dict = piexif.load(img.info.get("exif", b""))
            # 合并所有 EXIF 数据 (0th, Exif, GPS, etc.)
            for ifd_name in exif_dict:
                if not isinstance(exif_dict[ifd_name], dict):
                    continue
                for tag, value in exif_dict[ifd_name].items():
                    field_name = piexif.TAGS[ifd_name][tag]["name"]
                    metadata[field_name] = value
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"读取图片元数据失败: {e} {traceback.format_exc()}")
        finally:
            # 在 TableWidget 中显示数据
            self.populate_table(metadata)
            self.show_modify_exif_data(file_path)

    def show_modify_exif_data(self, file_path):
        """
        显示应用修改之后的元数据
        :param file_path:
        :return:
        """
        if self.given_date:
            name_date = self.given_date
        else:
            name_date = common.extract_datetime_from_filename(os.path.basename(file_path))
        if name_date:
            name_date_str = name_date.strftime('%Y:%m:%d %H:%M:%S')
            # 字段名
            field_item = QTableWidgetItem(name_date_str)
            field_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 只读
            self.tableWidget.setItem(0, 2, field_item)
            # 字段名
            field_item = QTableWidgetItem(name_date_str)
            field_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 只读
            self.tableWidget.setItem(1, 2, field_item)

    def populate_table(self, metadata):
        """
        在表格里显示元数据
        :param metadata:
        :return:
        """
        # 清空表格
        self.tableWidget.setRowCount(0)
        for row, exif_key in enumerate(exif_keys):
            value = metadata.get(exif_key, '')
            # 字段值（转为字符串显示）
            if isinstance(value, bytes):
                value = value.decode('utf-8')
            else:
                value = str(value)
            self.tableWidget.insertRow(row)
            # 字段名
            field_item = QTableWidgetItem(exif_key)
            field_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 只读
            self.tableWidget.setItem(row, 0, field_item)
            value_item = QTableWidgetItem(value)
            value_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 只读
            self.tableWidget.setItem(row, 1, value_item)
            self.tableWidget.setItem(row, 2, value_item.clone())
            # print(row, exif_key, value)

    def update_progress(self, value):
        self.progressBar.setValue(value)

    def update_current_file(self,filename):
        self.label_current_file.setText(filename)

    def start(self):
        self.running_flag = True
        globalSignals.start_busy.emit(True)
        self.btn_start.setEnabled(False)
        file_fir = self.model.filePath(self.treeView.rootIndex())
        self.worker = ModifyThread(
            file_fir,
            self.output_dir,
            self.checkBox_apply_child.isChecked(),
            self.given_date,
            self.checkBox_force_modify.isChecked()
        )
        self.worker.okSignal.connect(self.finish)
        self.worker.progressSignal.connect(self.update_progress)
        self.worker.currentFile.connect(self.update_current_file)
        self.worker.start()

    def finish(self, a):
        globalSignals.stop_busy.emit(True)
        reply = QMessageBox(self)
        reply.setIcon(QMessageBox.Information)
        reply.setWindowTitle('OK')
        reply.setText(f"成功")
        btn = reply.addButton('打开', QMessageBox.ActionRole)
        if self.output_dir:
            open_path = self.output_dir
        else:
            open_path = self.model.filePath(self.treeView.rootIndex())
        print(open_path)
        btn.clicked.connect(
            lambda x: open_file_explorer(
                os.path.dirname(open_path)
            )
        )
        reply.addButton("确认", QMessageBox.AcceptRole)
        reply.addButton("取消", QMessageBox.RejectRole)
        api = reply.exec_()
        # self.close()
        self.running_flag = False
        self.btn_start.setEnabled(True)
        # self.list_view.clear()
        self.progressBar.setValue(0)
        self.worker = None


class ModifyThread(QThread):
    okSignal = Signal(bool)
    progressSignal = Signal(int)
    currentFile = Signal(str)

    def __init__(self, file_dir, output_dir, is_apply_child, given_date=None, is_force=False):
        super().__init__()
        self.file_dir = file_dir
        self.output_dir = output_dir
        self.is_apply_child = is_apply_child
        self.given_date = given_date
        self.is_force = is_force

    def scan_files(self) -> List[ImageFile]:
        file_items = []
        if self.output_dir and not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
        # 统计任务个数
        if not self.is_apply_child:
            filenames = os.listdir(self.file_dir)
            for file in filenames:
                if not is_image(file):
                    continue
                image_file = ImageFile(os.path.join(self.file_dir, file))
                if self.output_dir:
                    image_file.save_path = os.path.join(self.output_dir, image_file.file_name)
                file_items.append(
                    image_file
                )
        else:
            # 考虑子文件夹
            for filepath, dir, filenames in os.walk(self.file_dir):
                for filename in filenames:
                    if not is_image(filename):
                        continue
                    image_file = ImageFile(os.path.join(filepath, filename))
                    if self.output_dir:
                        # 计算当前目录相对于源目录的相对路径
                        relative_path = os.path.relpath(filepath, self.file_dir)
                        # 构建目标目录中对应的路径
                        target_path = os.path.join(self.output_dir, relative_path)
                        # 创建目标目录中对应的子目录（如果不存在）
                        os.makedirs(target_path, exist_ok=True)
                        image_file.save_path = os.path.join(target_path, image_file.file_name)
                    file_items.append(
                        image_file
                    )
        return file_items

    def run(self):
        try:
            self.progressSignal.emit(1)
            files = self.scan_files()
            exiftool = PyExifTool(r".\resources\third_party\exiftool-13.33_64\exiftool(-k).exe",overwrite_original=True)
            progress = 1
            total_task = len(files)
            for index,file in enumerate(files):
                try:
                    new_progress = (index + 1)*100 // total_task
                    if new_progress > progress:
                        progress = new_progress
                        self.progressSignal.emit(progress)
                    if index % 10 == 0:
                        self.currentFile.emit(file.file_name)
                    if not self.given_date:
                        new_datetime = file.get_file_time_by_name()
                    else:
                        new_datetime = self.given_date
                    if not new_datetime:
                        continue
                    if not os.path.exists(file.save_path):
                        shutil.copy(file.file_path,file.save_path)
                    if not self.is_force:
                        file_time = exiftool.get_file_time(file.save_path)
                        if file_time and new_datetime < file_time:
                            new_datetime = file_time
                            exiftool.modify_image_time(new_datetime, file.save_path)
                    else:
                        exiftool.modify_image_time(new_datetime, file.save_path)
                except Exception as e:
                    print(e)
                    print(traceback.format_exc())
            exiftool.close()
            self.progressSignal.emit(100)
            print(f"处理完成，已生成文件")
        except Exception as e:
            print(f"处理过程中出错: {e}\n{traceback.format_exc()}")
        finally:
            self.okSignal.emit(True)


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
    view = ModifyDateControl(None)
    view.show()
    sys.exit(app.exec_())
