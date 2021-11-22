import fnmatch
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

        # target files mask
        self.ui.target_files_mask.setText(settings.get_settings_str_value(SettingsKey.TARGET_FILES_MASK))
        self.ui.apply_target_files_mask.clicked.connect(self._populate_file_tree)
        self.ui.apply_target_files_mask.clicked.connect(
            lambda: settings.set_settings_str_value(SettingsKey.TARGET_FILES_MASK, self.ui.target_files_mask.text())
        )

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

    @Slot()
    def _populate_file_tree(self):
        raw_file_mask_str = self.ui.target_files_mask.text()
        print("=== FILE MASK ===\n"
              "before")
        print(raw_file_mask_str)

        if raw_file_mask_str != '':
            file_mask = ' '.split(raw_file_mask_str)
        else:
            file_mask = []

        file_mask = raw_file_mask_str

        print("after")
        print(file_mask)

        self.ui.files_tree.clear()

        print('====\n'
              f'  mask {file_mask} or {str(file_mask)}\n'
              '====\n')

        def iterate(cur_dir, cur_item):
            for f in os.listdir(cur_dir):
                # dir or not
                path = os.path.join(cur_dir, f)
                print(f"{f} {'   DIR' if os.path.isdir(path) else None}")
                if os.path.isdir(path):
                    dir_item = QtWidgets.QTreeWidgetItem(cur_item)
                    dir_item.setText(0, f)
                    dir_item.setDisabled(True)
                    iterate(path, dir_item)
                else:
                    file_item = QtWidgets.QTreeWidgetItem(cur_item)
                    file_item.setText(0, f)

                    # check mask
                    file_ext = os.path.splitext(f)
                    par1 = [f]
                    par2 = file_mask
                    print(f"fnmatch.filter({par1}, {par2}) = {fnmatch.filter(par1, par2)}")
                    print('')
                    is_target = fnmatch.filter(par1, par2)
                    if is_target:
                        file_item.setText(1, 'Ready')
                    else:
                        file_item.setDisabled(True)

        iterate(self.ui.source_folder.text(), self.ui.files_tree)
