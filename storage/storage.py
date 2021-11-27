import fnmatch
import os
from PySide6.QtCore import QDir
from PySide6.QtWidgets import QApplication

import logger
from storage.storage_item import MediaFile


class Storage(object):

    def __init__(self):
        # self.watch_folder = None
        # self.media_files = list()
        # self.target_file_mask = '*.mp4 *.mov *.ts *.mkv'
        self.files = list()

    def add_media_file(self, file: str) -> str:
        media_file = MediaFile(file)

        if self.contains_media_file(media_file):
            logger.error('failed to add file into storage: file already exists')
            return ''

        self.files.append(media_file)
        hash = media_file.hash()
        print(hash)
        return hash

    def contains_media_file(self, file: MediaFile):
        for f in self.files:
            if file.hash() == f.hash():
                return True
        return False

    # def _get_filename(self):
    #     storage_dir = os.path.join(QDir.homePath(), QApplication.applicationName())
    #     if not (os.path.exists(storage_dir) and os.path.isdir(storage_dir)):
    #         os.mkdir(storage_dir)
    #
    #     return storage_dir
    #
    # def set_target_file_mask(self, mask: str):
    #     self.target_file_mask = mask
    #
    # def get_target_file_mask(self) -> str:
    #     return self.target_file_mask
    #
    # def get_watch_folders(self):
    #     pass

    # def set_watch_folder(self, watch_folder: str):
    #     self.media_files.clear()
    #     self.watch_folder = watch_folder
    #     self.scan_folder(self.watch_folder)

    # def scan_folder(self, folder: str):
    #     for f in os.listdir(folder):
    #         # dir or not
    #         path = os.path.join(folder, f)
    #         print(f"{f} {'   DIR' if os.path.isdir(path) else None}")
    #         if os.path.isdir(path):
    #             # dir_item = QtWidgets.QTreeWidgetItem(cur_item)
    #             # dir_item.setText(0, f)
    #             self.scan_folder(path)
    #         else:
    #             # stats['total_files'] += 1
    #             # check mask
    #             file_ext = os.path.splitext(f)
    #             is_target = False
    #             for mask in self.target_file_mask:
    #                 par1 = [f]
    #                 par2 = mask
    #                 print(f"fnmatch.filter({par1}, {par2}) = {fnmatch.filter(par1, par2)}")
    #                 print('')
    #                 is_target = len(fnmatch.filter(par1, par2)) > 0
    #                 if is_target:
    #                     break
    #
    #             file_item = None
    #             if is_target:
    #                 pass
    #                 # stats['target_files'] += 1
    #                 # file_item.setDisabled(False)
    #                 # file_item.setText(1, 'On Target')
    #                 # # orange
    #                 # orange = QtGui.QColor(0xFF, 0x99, 0x33)
    #                 # file_item.setForeground(0, orange)
    #                 # file_item.setForeground(1, orange)
    #                 # file_item.setForeground(2, orange)
    #             elif file_item:
    #                 # file_item.setDisabled(True)
    #                 pass
