import datetime
import fnmatch
import os

from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QDialog, QFileDialog
from PySide6.QtCore import Slot, QSettings, QTimer

import settings
from folder_watcher import FolderWatcher
from settings import SettingsKey
import youtube_uploader
from ui_main_dialog import Ui_Dialog


class MainDialog(QDialog):
    def __init__(self):
        super(MainDialog, self).__init__()

        self.watcher = FolderWatcher()

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

        # show target files only
        self.ui.show_target_files_only.clicked.connect(self._populate_file_tree)

        #
        # file tree
        #

        self._populate_file_tree()

        def resize_file_tree_columns():
            file_tree_width = self.ui.files_tree.width()
            self.ui.files_tree.setColumnWidth(0, file_tree_width * 0.7)
            self.ui.files_tree.setColumnWidth(1, file_tree_width * 0.1)
            self.ui.files_tree.setColumnWidth(2, file_tree_width * 0.1)

        # wait while the main dialog has been resized
        QTimer.singleShot(200, resize_file_tree_columns)

        # start/stop watch
        self.ui.start_watch.clicked.connect(self._start_watch)
        self.ui.stop_watch.clicked.connect(self._stop_watch)

    def closeEvent(self, event):
        self.watcher.stop()

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
        self.ui.files_tree.clear()
        # file_mask = self._get_target_file_mask_list()
        file_mask = self.ui.target_files_mask.text().split(' ')

        print('====\n'
              f'  mask {file_mask} or {str(file_mask)}\n'
              '====\n')

        show_target_files_only = self.ui.show_target_files_only.isChecked()
        stats = dict(
            total_files=0,
            target_files=0
        )

        def iterate(cur_dir, cur_item):
            for f in os.listdir(cur_dir):
                # dir or not
                path = os.path.join(cur_dir, f)
                print(f"{f} {'   DIR' if os.path.isdir(path) else None}")
                if os.path.isdir(path):
                    dir_item = QtWidgets.QTreeWidgetItem(cur_item)
                    dir_item.setText(0, f)
                    iterate(path, dir_item)
                else:
                    stats['total_files'] += 1
                    # check mask
                    file_ext = os.path.splitext(f)
                    is_target = False
                    for mask in file_mask:
                        par1 = [f]
                        par2 = mask
                        print(f"fnmatch.filter({par1}, {par2}) = {fnmatch.filter(par1, par2)}")
                        print('')
                        is_target = len(fnmatch.filter(par1, par2)) > 0
                        if is_target:
                            break

                    file_item = None
                    if is_target or not show_target_files_only:
                        file_item = QtWidgets.QTreeWidgetItem(cur_item)
                        file_item.setText(0, f)

                    if is_target:
                        stats['target_files'] += 1
                        file_item.setDisabled(False)
                        file_item.setText(1, 'Ready')
                    elif file_item:
                        file_item.setDisabled(True)

        iterate(self.ui.source_folder.text(), self.ui.files_tree)
        self.ui.target_files_stats.setText(f"Total files: {stats['total_files']} | target files: {stats['target_files']}")

    @Slot()
    def _start_watch(self):
        check_time_in_msec = self.ui.check_period.time().msecsSinceStartOfDay()
        self.watcher.start(self.ui.source_folder.text(), datetime.timedelta(milliseconds=check_time_in_msec))
        self._set_all_controls_enabled(False)
        self.ui.stop_watch.setEnabled(True)

    @Slot()
    def _stop_watch(self):
        self.watcher.stop()
        self._set_all_controls_enabled(False)
        self.ui.start_watch.setEnabled(True)

    def _set_all_controls_enabled(self, enabled: bool = True):
        self.ui.source_folder.setEnabled(enabled)
        self.ui.choose_source_folder.setEnabled(enabled)
        self.ui.target_files_mask.setEnabled(enabled)
        self.ui.apply_target_files_mask.setEnabled(enabled)
        self.ui.yt_channel_name.setEnabled(enabled)
        self.ui.upload_media.setEnabled(enabled)
        self.ui.files_tree.setEnabled(enabled)
        self.ui.check_period.setEnabled(enabled)
        self.ui.start_watch.setEnabled(enabled)
        self.ui.stop_watch.setEnabled(enabled)

    # def _get_target_file_mask_list(self) -> list[str]:
    #     raw_text = self.ui.target_files_mask.text()
    #     output = ' '.split(raw_text)
    #     return output if output != '' else [raw_text]
