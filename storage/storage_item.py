# represents items that used by Storage;
# can be either a directory or media file, or non-media file
import abc
import hashlib
import os
import uuid
from abc import ABC


class StorageItem(abc.ABC):
    def __init__(self, path: str):
        self._uuid = str(uuid.uuid1())
        self._path = os.path.abspath(path)
        self._hash = None

    @abc.abstractmethod
    def is_dir(self):
        pass

    def uuid(self):
        return self._uuid

    def path(self):
        return self._path

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
        print(self._hash)

    def hash(self):
        return self.hash


class Directory(StorageItem):
    def __init__(self, path: str):
        super(Directory, self).__init__(path)

    # @abc.abstractmethod
    def is_dir(self):
        return True


class File(StorageItem):
    def __init__(self, path: str):
        super(File, self).__init__(path)

    # @override
    def is_dir(self):
        return False


class MediaFile(File):
    def __init__(self, path: str):
        super(MediaFile, self).__init__(path)
        self._calc_hash()
    #
    # def is_dir(self):
    #     return False
