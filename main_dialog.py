import datetime
import fnmatch
import os

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QFileDialog
from PySide6.QtCore import Slot, QTimer

import logger
import settings
import uploader.youtube_uploader
from storage import storage
from storage.storage_item import StorageItemStatus
from uploader.youtube_uploader import YouTubeUploader, UploadedFileInfo
from folder_watcher import FolderWatcher
from settings import SettingsKey
from storage.storage import Storage
from ui_main_dialog import Ui_Dialog

_STATUS_MAP = dict(
    ON_TARGET=QtGui.QColor(0xFF, 0x99, 0x33),  # orange
    UPLOADING=Qt.darkBlue,
    UPLOAD_FAILED=Qt.red,
    UPLOADED=Qt.darkGreen
)


def _get_color_from_status(status: StorageItemStatus) -> QtGui.QColor:
    return _STATUS_MAP.get(status.name, Qt.black)


def _set_foreground_for_item(item: QtWidgets.QTreeWidgetItem, color: QtGui.QColor):
    item.setForeground(0, color)
    item.setForeground(1, color)
    item.setForeground(2, color)


class MainDialog(QDialog):
    def __init__(self):
        super(MainDialog, self).__init__()

        self.storage = Storage()
        self.storage.load()

        self.watcher = FolderWatcher()
        self.uploader = YouTubeUploader()
        self.uploader.fileUploaded.connect(self._update_tree_item)

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

        # file tree
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
        self.uploader.stop()
        self.storage.save()

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
        file_mask = self.ui.target_files_mask.text().split(' ')

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

            new_item = QtWidgets.QTreeWidgetItem()

            # dir or not
            full_path = os.path.join(path, filename)
            if os.path.isdir(full_path):
                new_item.setText(0, filename)
            else:
                stats['total_files'] += 1

                # check mask
                is_target = False
                for mask in file_mask:
                    is_target = len(fnmatch.filter([filename], mask)) > 0
                    if is_target:
                        break

                if is_target or not show_target_files_only:
                    new_item.setText(0, filename)

                if is_target:
                    new_item.setDisabled(False)

                    # try to find such one in storage
                    media_file = self.storage.get_media_file_by_name(full_path)
                    if media_file:
                        if media_file.status() == StorageItemStatus.ON_TARGET:
                            self.uploader.queue_media_file(
                                uploader.youtube_uploader.MediaFile(media_file.uuid(), full_path, 'My title',
                                                                    'My desc'))
                    else:
                        media_file = self.storage.add_new_media_file(full_path)
                        if not media_file:
                            logger.error(f'failed to add file {filename} into storage')
                            return None
                        else:
                            self.uploader.queue_media_file(uploader.youtube_uploader.MediaFile(media_file.uuid(), full_path, 'My title', 'My desc'))

                    # stats['target_files'] += 1

                    new_item.setData(0, Qt.UserRole, media_file.uuid())
                    new_item.setText(1, media_file.status().value)
                    cccc = _get_color_from_status(media_file.status())
                    _set_foreground_for_item(new_item, cccc)
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

        self.uploader.start()

    @Slot()
    def _stop_watch(self):
        self.watcher.stop()
        self._set_all_controls_enabled(False)
        self.ui.start_watch.setEnabled(True)

        self.uploader.stop()

    @Slot()
    def _update_tree_item(self, uploaded_file_info: UploadedFileInfo):
        if not uploaded_file_info:
            logger.error(f"failed to update tree element's info: empty uploaded file info received")
            return

        if not uploaded_file_info.uuid:
            logger.error(f"failed to update tree element's info: got invalid uploaded file info (UUID='{uploaded_file_info.uuid}', "
                         f"error='{uploaded_file_info.err_msg}'")
            return

        tree_item = self._find_tree_item_by_uuid(uploaded_file_info.uuid)
        if not tree_item:
            logger.error(f"failed to update tree element's info: unable to find tree element with UUID='{uploaded_file_info.uuid}'")
            return

        media_file = self.storage.get_media_file_by_uuid(uploaded_file_info.uuid)

        upload_failed = uploaded_file_info.err_msg != ''
        media_file.set_status(StorageItemStatus.UPLOAD_FAILED if upload_failed else StorageItemStatus.UPLOADED)

        tree_item.setText(1, media_file.status().value)
        _set_foreground_for_item(tree_item, _get_color_from_status(media_file.status()))

        # self._sync_to_storage(media_file)

    @Slot()
    def _sync_to_storage(self, media_file: storage.MediaFile):
        self.storage.update_media_file(media_file)

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

    def _find_tree_item_by_uuid(self, uuid: str) -> QtWidgets.QTreeWidgetItem:
        if not uuid:
            return None

        def find_in_children(parent: QtWidgets.QTreeWidgetItem, uuid: str):
            for i in range(0, parent.childCount()):
                child_item = parent.child(i)
                if child_item.data(0, Qt.UserRole) == uuid:
                    return child_item
                elif child_item.childCount() > 0:
                    found_item = find_in_children(child_item, uuid)
                    if found_item:
                        return found_item
            return None

        for i in range(0, self.ui.files_tree.topLevelItemCount()):
            top_level_item = self.ui.files_tree.topLevelItem(i)
            if top_level_item.data(0, Qt.UserRole) == uuid:
                return top_level_item
            elif top_level_item.childCount() > 0:
                found_item = find_in_children(top_level_item, uuid)
                if found_item:
                    return found_item
        return None
