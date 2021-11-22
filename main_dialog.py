import os

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QDialog, QFileDialog
from PySide6.QtCore import Slot, QSettings, QTimer

import settings
from settings import SettingsKey
import youtube_uploader
from ui_main_dialog import Ui_Dialog


class MainDialog(QDialog):
    def __init__(self):
        super(MainDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # restore position and state
        # self.setWindowState(settings.get_settings_byte_array_value(SettingsKey.WINDOW_STATE, QtCore.Qt.WindowNoState))
        self.restoreGeometry(settings.get_settings_byte_array_value(SettingsKey.WINDOW_GEOMETRY))

        # source folder
        self.ui.source_folder.setText(settings.get_settings_str_value(SettingsKey.SOURCE_FOLDER, ''))
        self.ui.choose_source_folder.clicked.connect(self._choose_source_folder)
        self.ui.source_folder.textChanged.connect(self._populate_file_tree)

        # source file
        self.ui.choose_source_file.clicked.connect(self._choose_source_file)

        # upload file
        self.ui.upload_media.clicked.connect(self._upload_cur_media_file)

        # file tree

        self._populate_file_tree()

        def resize_file_tree_columns():
            file_tree_width = self.ui.files_tree.width()
            self.ui.files_tree.setColumnWidth(0, file_tree_width * 0.7)
            self.ui.files_tree.setColumnWidth(1, file_tree_width * 0.1)
            self.ui.files_tree.setColumnWidth(2, file_tree_width * 0.1)

        QTimer.singleShot(200, resize_file_tree_columns)

    def closeEvent(self, event):
        # save window position and size
        settings.set_settings_byte_array_value(SettingsKey.WINDOW_GEOMETRY, self.saveGeometry())
        # settings.set_settings_byte_array_value(SettingsKey.WINDOW_STATE, self.windowState())

        event.accept()

    @Slot()
    def _choose_source_folder(self):
        src_dir = QFileDialog.getExistingDirectory(self,
                                                   "Choose Source Folder",
                                                   settings.get_settings_str_value(SettingsKey.SOURCE_FOLDER, '')
                                                   )

        self.ui.source_folder.setText(src_dir)
        settings.set_settings_str_value(SettingsKey.SOURCE_FOLDER, src_dir)

    @Slot(str)
    def on_folder_path_changed(self, new_text):
        print(new_text)

    @Slot()
    def _choose_source_file(self):
        src_file = QFileDialog.getOpenFileName(self,
                                               "Choose Source File",
                                               # "/home/jana"
                                               filter='Video (*.mp4 *.mov *.ts *.mkv);;'
                                                      'All Files (*.*)')

        if type(src_file) is tuple:
            self.ui.source_file.setText(src_file[0])

    @Slot()
    def _upload_cur_media_file(self):
        youtube_uploader.upload_media_file(self.ui.source_file.text(), 'Test naming нна русском языке')

    @Slot()
    def _populate_file_tree(self):
        self.ui.files_tree.clear()

        def iterate(cur_dir, cur_item):
            for f in os.listdir(cur_dir):
                path = os.path.join(cur_dir, f)
                if os.path.isdir(path):
                    dir_item = QtWidgets.QTreeWidgetItem(cur_item)
                    dir_item.setText(0, f)
                    iterate(path, dir_item)
                else:
                    file_item = QtWidgets.QTreeWidgetItem(cur_item)
                    file_item.setText(0, f)

        iterate(self.ui.source_folder.text(), self.ui.files_tree)
