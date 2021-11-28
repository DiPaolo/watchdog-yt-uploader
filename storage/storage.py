import json
import os.path

from PySide6.QtCore import QStandardPaths

import config
import logger
from storage.storage_item import MediaFile, StorageItemStatus


class Storage(object):

    def __init__(self):
        self.files = dict()

    def save(self):
        try:
            if not os.path.exists(self._get_storage_dir()):
                os.mkdir(self._get_storage_dir())

            with open(self._get_storage_full_filename(), 'w+') as f:
                data = dict()
                data['version'] = config.STORAGE_VERSION
                data_files = list()
                for uuid, file in self.files.items():
                    data_files.append({
                        'fullFilename': file.path(),
                        'hash': file.hash(),
                        'status': file.status().name
                    })
                data['files'] = data_files
                f.write(json.dumps(data, indent=4))
        except Exception as e:
            logger.error(f'failed to save data: {e}')

    def load(self):
        try:
            with open(self._get_storage_full_filename(), 'r') as f:
                data = json.load(f)
                # TODO check version and implement data migration
                if 'files' in data:
                    for file in data['files']:
                        media_file = MediaFile(file['fullFilename'])
                        media_file.set_status(StorageItemStatus[file['status']])
                        # TODO check hash and compare with the one stored in the file
                        self._add_media_file(media_file)
        except FileNotFoundError as e:
            pass
        except Exception as e:
            logger.error(f'failed to load data: {e}')

    def add_new_media_file(self, file: str) -> MediaFile:
        """
        Add media file

        :param file:
        :return: UUID of the newly created item
        """
        media_file = MediaFile(file)

        if self.contains_media_file(media_file):
            logger.error('failed to add file into storage: file already exists')
            return ''

        self._add_media_file(media_file)
        media_file.set_status(StorageItemStatus.ON_TARGET)
        return media_file

    def get_media_file_by_name(self, filename: str):
        for uuid, f in self.files.items():
            if filename == f.path():
                return f
        return None

    def get_media_file_by_uuid(self, uuid: str):
        return self.files[uuid] if uuid in self.files else None

    def update_media_file(self, media_file: MediaFile):
        f = self.get_media_file_by_uuid(media_file.uuid())
        if not f:
            self._add_media_file(media_file)
        else:
            self.files[media_file.uuid()] = media_file

    def contains_media_file(self, file: MediaFile):
        for uuid, f in self.files.items():
            if file.hash() == f.hash():
                return True
        return False

    def _add_media_file(self, media_file: MediaFile):
        if media_file.uuid() in self.files:
            logger.error(f"media file already in storage: UUID {media_file.uuid()}")
            return

        self.files[media_file.uuid()] = media_file

    def _get_storage_dir(self):
        return QStandardPaths.standardLocations(QStandardPaths.AppDataLocation)[0]

    def _get_storage_full_filename(self):
        storage_dir = self._get_storage_dir()
        return os.path.join(storage_dir, config.STORAGE_FILENAME)
