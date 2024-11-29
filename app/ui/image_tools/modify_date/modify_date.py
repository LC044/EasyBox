import os.path
import shutil
import traceback
from datetime import datetime
from multiprocessing import Queue, Process
from typing import List

from PIL import Image
import piexif
from PySide6.QtCore import Signal, QThread, QUrl, Qt, QFile, QIODevice, QTextStream, QDir, QSortFilterProxyModel
from PySide6.QtGui import QDesktopServices, QPixmap, QIcon, QFont, QFontMetrics
from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog, QApplication, QDialog, QFileSystemModel, QTreeView, \
    QTableWidgetItem

from app.log import logger
from app.model.file_model import ImageFile
from app.ui.components.QCursorGif import QCursorGif
from app.ui.Icon import Icon
from app.ui.image_tools.modify_date.modify_date_ui import Ui_modify_date_view
from app.ui.components.router import Router
from app.util import common


def open_file_explorer(path):
    # 使用QDesktopServices打开文件管理器
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))


image_extensions = ['jpg', 'jpeg', 'bmp', 'riff', 'webp']
image_extensions_filter = ['*.jpg', '*.jpeg', '*.bmp', '*.riff', '*.webp']

exif_keys = ['DateTime', 'DateTimeOriginal', 'Make', 'Model', 'Software', 'ImageWidth', 'ImageLength']


class ModifyDateControl(QWidget, Ui_modify_date_view, QCursorGif):
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
        # 设置忙碌光标图片数组
        self.initCursor([':/icons/icons/Cursors/%d.png' %
                         i for i in range(8)], self)
        self.setCursorTimeout(100)
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
            style_qss_file = QFile(":/data/resources/QSS/style.qss")
            if style_qss_file.open(QIODevice.ReadOnly | QIODevice.Text):
                stream = QTextStream(style_qss_file)
                style_content = stream.readAll()
                self.setStyleSheet(style_content)
                style_qss_file.close()
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
            self.given_date = self.dateTimeEdit.dateTime().toPyDateTime()
        else:
            self.given_date = None
            self.dateTimeEdit.setVisible(False)

    def set_given_date(self):
        self.given_date = self.dateTimeEdit.dateTime().toPyDateTime()

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
        if self.is_image(file_path):
            self.display_image(file_path)

    def is_image(self, file_path):
        """判断文件是否为图片"""
        return any(file_path.lower().endswith(ext) for ext in image_extensions)

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

    def start(self):
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
        self.worker.start()

    def finish(self, a):
        self.stopBusy()
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
        self.btn_start.setEnabled(True)
        # self.list_view.clear()
        self.progressBar.setValue(0)
        self.worker = None


class TaskItem:
    """
    线程分配的单个任务，
    包括多个image_files
    """

    def __init__(self, image_files: List[ImageFile], given_date, is_force):
        self.image_files = image_files
        self.task_num = len(image_files)
        self.given_date = given_date
        self.is_force = is_force

    def __len__(self):
        return len(self.image_files)


def get_exif_date(exif_dict, field, key='Exif', default="Unknown"):
    """
    安全获取 EXIF 字段的日期，如果字段不存在或解析失败，返回默认值。
    """
    try:
        date_str = exif_dict[key].get(field, b"").decode("utf-8")
        return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except (KeyError, ValueError, UnicodeDecodeError):
        return default


def modify_image(image_file: ImageFile, given_date, is_force):
    """
    修改图片的拍摄时间为given_date
    :param image_file:
    :param given_date:
    :param is_force: 是否强制设置为given_date,否：取当前图片拍摄时间和给定时间的最小值
    :return:
    """
    file_path = image_file.file_path
    if not given_date:
        given_date = image_file.get_file_time_by_name()
    try:
        # 打开图片并加载 EXIF 数据
        img = Image.open(file_path)
        try:
            exif_dict = piexif.load(img.info.get("exif", b""))
            # 获取 EXIF 日期
            date_time_original = get_exif_date(exif_dict, piexif.ExifIFD.DateTimeOriginal, 'Exif', None)
            if is_force:
                modify_date = get_exif_date(exif_dict, piexif.ImageIFD.DateTime, '0th', None)
                dates = [d for d in [date_time_original, modify_date, given_date] if d is not None]
                earliest_date = min(dates)
            else:
                earliest_date = given_date
            # 如果 DateTimeOriginal 已经是最早的，则无需修改
            if date_time_original != earliest_date:
                # 更新 DateTimeOriginal
                exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = earliest_date.strftime("%Y:%m:%d %H:%M:%S").encode(
                    "utf-8")
                exif_dict["0th"][piexif.ImageIFD.Make] = 'MemoTrace'.encode("utf-8")
                exif_dict["0th"][piexif.ImageIFD.Model] = 'EasyBox'.encode("utf-8")
                exif_dict["0th"][piexif.ImageIFD.Software] = 'EasyBox-0.1.0'.encode("utf-8")
        except:
            earliest_date = given_date
            exif_dict = {
                '0th': {},
                'Exif': {}
            }
            if earliest_date:
                # 更新 DateTimeOriginal
                exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = earliest_date.strftime("%Y:%m:%d %H:%M:%S").encode(
                    "utf-8")
            exif_dict["0th"][piexif.ImageIFD.Make] = 'MemoTrace'.encode("utf-8")
            exif_dict["0th"][piexif.ImageIFD.Model] = 'EasyBox'.encode("utf-8")
            exif_dict["0th"][piexif.ImageIFD.Software] = 'EasyBox-0.1.0'.encode("utf-8")
        # 保存修改后的图片
        exif_bytes = piexif.dump(exif_dict)
        # img.save(image_file.save_path, exif=exif_bytes, quality=image_file.save_quality, subsampling=0)
        if image_file.save_path != image_file.file_path:
            shutil.copy(file_path, image_file.save_path)
        piexif.insert(exif_bytes, image_file.save_path)
        print(f"DateTimeOriginal 已更新为最早日期：{earliest_date}")
    except Exception as e:
        print(f"处理图片时出错：{e} {traceback.format_exc()}")


def is_image(file_path):
    """判断文件是否为图片"""
    return any(file_path.lower().endswith(ext) for ext in image_extensions)


class ModifyThread(QThread):
    okSignal = Signal(bool)
    progressSignal = Signal(int)

    def __init__(self, file_dir, output_dir, is_apply_child, given_date=None, is_force=False):
        super().__init__()
        self.file_dir = file_dir
        self.output_dir = output_dir
        self.is_apply_child = is_apply_child
        self.given_date = given_date
        self.is_force = is_force

    def run(self):
        task_queue = Queue()
        result_queue = Queue()
        processes = []
        if self.output_dir and not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
        try:
            total_tasks = 0
            num_each_process = 100
            # 创建多进程任务
            if not self.is_apply_child:
                filenames = os.listdir(self.file_dir)
                file_items = []
                for file in filenames:
                    if not is_image(file):
                        continue
                    total_tasks += 1
                    image_file = ImageFile(os.path.join(self.file_dir, file))
                    if self.output_dir:
                        image_file.save_path = os.path.join(self.output_dir, image_file.file_name)
                    file_items.append(
                        image_file
                    )
                    if total_tasks % num_each_process == 0:
                        task_queue.put(TaskItem(file_items, self.given_date, self.is_force))
                        file_items = []
                task_queue.put(TaskItem(file_items, self.given_date, self.is_force))
            else:
                file_items = []
                for filepath, dir, filenames in os.walk(self.file_dir):
                    for filename in filenames:
                        if not is_image(filename):
                            continue
                        total_tasks += 1
                        image_file = ImageFile(os.path.join(filepath, filename))
                        if self.output_dir:
                            image_file.save_path = os.path.join(self.output_dir, image_file.file_name)
                        file_items.append(
                            image_file
                        )
                        if total_tasks % num_each_process == 0:
                            task_queue.put(TaskItem(file_items, self.given_date, self.is_force))
                            file_items = []
                task_queue.put(TaskItem(file_items, self.given_date, self.is_force))
            total_tasks_process = total_tasks // num_each_process + 1
            num_processes = min(total_tasks_process, os.cpu_count())
            for _ in range(num_processes):
                p = Process(target=self.process_task, args=(task_queue, result_queue))
                p.start()
                processes.append(p)

            completed_tasks = 0

            while completed_tasks < total_tasks_process:
                result = result_queue.get()
                if result["status"] == "success":
                    completed_tasks += 1
                    progress = min(completed_tasks * 100 // total_tasks_process, 99)
                    self.progressSignal.emit(progress)
                else:
                    print(f"处理文件出错: {result['error']} 文件: {result['filepath']}")

            self.progressSignal.emit(100)
            print(f"处理完成，已生成文件")

        except Exception as e:
            print(f"处理过程中出错: {e}")
        finally:
            for p in processes:
                p.join()

        self.okSignal.emit(True)

    @staticmethod
    def process_task(task_queue: Queue, result_queue: Queue):
        while not task_queue.empty():
            try:
                task_item: TaskItem = task_queue.get_nowait()
                for image_file in task_item.image_files:
                    modify_image(image_file, task_item.given_date, task_item.is_force)
                try:
                    result_queue.put({"status": "success", "task_num": task_item.task_num})
                except Exception as e:
                    result_queue.put({"status": "error", "error": str(e)})

            except Exception as e:
                result_queue.put({"status": "error", "error": str(e), "filepath": None})


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
