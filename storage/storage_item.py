# represents items that used by Storage;
# can be either a directory or media file, or non-media file
import abc
import hashlib
import os
import uuid
from enum import Enum


class StorageItemStatus(Enum):
    UNKNOWN = 'Unknown'
    ON_TARGET = 'On Target'
    UPLOADING = 'Uploading'
    UPLOAD_FAILED = 'Upload Failed'
    UPLOADED = 'Uploaded'


class StorageItem(abc.ABC):
    def __init__(self, path: str, uuid_str: str = None):
        self._uuid = uuid_str if uuid_str else str(uuid.uuid1())
        self._path = os.path.abspath(path)
        self._hash = None
        self._status = StorageItemStatus.UNKNOWN

    @abc.abstractmethod
    def is_dir(self):
        pass

    def uuid(self):
        return self._uuid

    def path(self):
        return self._path

    def hash(self):
        return self._hash

    def status(self):
        return self._status

    def set_status(self, status: StorageItemStatus):
        self._status = status

    def _calc_hash(self):
        if self._path is None or self._path == '':
            self._hash = None
            return

        h = hashlib.sha256()
        if not self.is_dir():
            b = bytearray(256 * 1024)
            mv = memoryview(b)
            with open(self._path, 'rb', buffering=0) as f:
                for n in iter(lambda: f.readinto(mv), 0):
                    h.update(mv[:n])
            self._hash = h.hexdigest()
        else:
            h.update(os.path.abspath(self._path))

        digest = h.digest()
        digest_str = ''
        for b in digest:
            digest_str += f'{b:02x}'
        self._hash = digest_str


# class Directory(StorageItem):
#     def __init__(self, path: str):
#         super(Directory, self).__init__(path)
#
#     def is_dir(self):
#         return True


class File(StorageItem):
    def __init__(self, path: str, uuid_str: str = None):
        super(File, self).__init__(path, uuid_str)

    def is_dir(self):
        return False


class MediaFile(File):
    def __init__(self, path: str, uuid_str: str = None):
        super(MediaFile, self).__init__(path, uuid_str)
        self._calc_hash()
