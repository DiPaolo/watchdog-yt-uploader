import datetime
import fnmatch
import os

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QFileDialog
from PySide6.QtCore import Slot, QTimer

import config
import logger
import settings
from folder_watcher import FolderWatcher
from settings import SettingsKey
from storage.storage import Storage
from ui_main_dialog import Ui_Dialog


class MainDialog(QDialog):
    def __init__(self):
        super(MainDialog, self).__init__()

        self.storage = Storage()
        self.watcher = FolderWatcher()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # restore position and state
        # self.setWindowState(settings.get_settings_byte_array_value(SettingsKey.WINDOW_STATE, QtCore.Qt.WindowNoState))
        self.restoreGeometry(settings.get_settings_byte_array_value(SettingsKey.WINDOW_GEOMETRY))

        # source folder
        self.ui.source_folder.setText(settings.get_settings_str_value(SettingsKey.SOURCE_FOLDER, ''))
        self.ui.choose_source_folder.clicked.connect(self._choose_source_folder)
        self.ui.source_folder.textChanged.connect(self._scan_folder)

        # target files mask
        self.ui.target_files_mask.setText(settings.get_settings_str_value(SettingsKey.TARGET_FILES_MASK))
        self.ui.apply_target_files_mask.clicked.connect(self._scan_folder)
        self.ui.apply_target_files_mask.clicked.connect(
            lambda: settings.set_settings_str_value(SettingsKey.TARGET_FILES_MASK, self.ui.target_files_mask.text())
        )

        # show target files only
        self.ui.show_target_files_only.clicked.connect(self._scan_folder)

        #
        # file tree
        #

        self._scan_folder()

        def resize_file_tree_columns():
            file_tree_width = self.ui.files_tree.width()
            self.ui.files_tree.setColumnWidth(0, file_tree_width * 0.7)
            self.ui.files_tree.setColumnWidth(1, file_tree_width * 0.1)
            self.ui.files_tree.setColumnWidth(2, file_tree_width * 0.1)

        # wait while the main dialog has been resized
        QTimer.singleShot(200, resize_file_tree_columns)

        # check period
        self.ui.check_period.setTime(QtCore.QTime.fromMSecsSinceStartOfDay(
            settings.get_settings_int_value(SettingsKey.CHECK_PERIOD_MSECS, 15 * 1000 * 60)))
        self.ui.check_period.timeChanged.connect(
            lambda val: settings.set_settings_str_value(SettingsKey.CHECK_PERIOD_MSECS, val.msecsSinceStartOfDay())
        )

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
    def _scan_folder(self):
        # self.ui.files_tree.clear()
        # file_mask = self._get_target_file_mask_list()
        file_mask = self.ui.target_files_mask.text().split(' ')

        if config.DEBUG:
            print('====\n'
                  f'  mask {file_mask} or {str(file_mask)}\n'
                  '====\n')

        show_target_files_only = self.ui.show_target_files_only.isChecked()
        stats = dict(
            total_files=0,
            target_files=0,
            queued_files=0,
            uploaded_files=0,
            error_files=0,
        )

        def add_item(path: str, filename: str, parent: QtWidgets.QTreeWidgetItem) -> QtWidgets.QTreeWidgetItem:
            """
            Add new item into the tree widget

            :param filename:
            :param path:
            :param parent: can be None what means the new item must be added on top level
            :return: the newly created item or None if failed
            """
            if config.DEBUG:
                print(f"{filename} {'   DIR' if os.path.isdir(path) else None}")

            new_item = QtWidgets.QTreeWidgetItem()

            # dir or not
            full_path = os.path.join(path, filename)
            if os.path.isdir(full_path):
                new_item.setText(0, filename)
            else:
                stats['total_files'] += 1
                # check mask
                file_ext = os.path.splitext(filename)
                is_target = False
                for mask in file_mask:
                    par1 = [filename]
                    par2 = mask
                    if config.DEBUG:
                        print(f"fnmatch.filter({par1}, {par2}) = {fnmatch.filter(par1, par2)}")
                        print('')
                    is_target = len(fnmatch.filter(par1, par2)) > 0
                    if is_target:
                        break

                if is_target or not show_target_files_only:
                    new_item.setText(0, filename)

                if is_target:
                    stats['target_files'] += 1
                    new_item.setDisabled(False)
                    new_item.setText(1, 'On Target')
                    cur_file_hash = self.storage.add_media_file(full_path)
                    if cur_file_hash == '':
                        # parent.removeChild(parent)
                        logger.error(f'failed to add file {filename} into storage')
                        return None
                    else:
                        new_item.setData(0, Qt.UserRole, cur_file_hash)

                    # orange
                    orange = QtGui.QColor(0xFF, 0x99, 0x33)
                    new_item.setForeground(0, orange)
                    new_item.setForeground(1, orange)
                    new_item.setForeground(2, orange)
                elif new_item:
                    new_item.setDisabled(True)

            parent.addChild(new_item) if parent else self.ui.files_tree.addTopLevelItem(new_item)
            return new_item

        def iterate(cur_dir: str, cur_item: QtWidgets.QTreeWidgetItem):

            def iterate_child_items(parent_item: QtWidgets.QTreeWidgetItem, func):
                if parent_item is None:
                    for idx in range(0, self.ui.files_tree.topLevelItemCount()):
                        func(self.ui.files_tree.topLevelItem(idx))
                else:
                    for idx in range(0, parent_item.childCount()):
                        func(parent_item.child(idx))

            # prepare two sets (current state of disk + current state in TreeWidget) to compare them later
            disk_set = set(os.listdir(cur_dir))
            ui_set = set()
            iterate_child_items(cur_item, lambda child_item: ui_set.add(child_item.text(0)))

            # 1. remove outdated items from tree
            items_to_remove = ui_set - disk_set
            for item in items_to_remove:
                if cur_item is None:
                    for i in range(0, self.ui.files_tree.topLevelItemCount()):
                        if item == self.ui.files_tree.topLevelItem(i).text(0):
                            self.ui.files_tree.takeTopLevelItem(i)
                            break
                else:
                    for i in range(0, cur_item.childCount()):
                        ui_item = cur_item.child(i)
                        if item == ui_item.text(0):
                            cur_item.removeChild(ui_item)
                            break

                # TODO remove from storage

            # 2. add new ones to the tree
            items_to_add = disk_set - ui_set
            for item in items_to_add:
                add_item(cur_dir, item, cur_item)

            # 3. iterate over current sub-directories
            def iterate_subdir(subdir_item: QtWidgets.QTreeWidgetItem):
                full_path = os.path.join(cur_dir, subdir_item.text(0))
                if os.path.isdir(full_path):
                    iterate(full_path, subdir_item)

            iterate_child_items(cur_item, iterate_subdir)

        iterate(self.ui.source_folder.text(), None)
        self.ui.target_files_stats.setText(f"Total files: {stats['total_files']} | "
                                           f"on target: {stats['target_files']} | "
                                           f"queued: {stats['queued_files']}"
                                           f"uploaded: {stats['uploaded_files']} | "
                                           f"error files: {stats['error_files']}")

    @Slot()
    def _start_watch(self):
        check_time_in_msec = self.ui.check_period.time().msecsSinceStartOfDay()
        # expand all items to let the user ability to see all the items while they're disabled
        # self.ui.files_tree.expandAll()
        self.watcher.start(self._scan_folder, datetime.timedelta(milliseconds=check_time_in_msec))
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
        # self.ui.show_target_files_only.setEnabled(enabled)
        # self.ui.files_tree.setEnabled(enabled)
        self.ui.check_period.setEnabled(enabled)
        self.ui.start_watch.setEnabled(enabled)
        self.ui.stop_watch.setEnabled(enabled)
