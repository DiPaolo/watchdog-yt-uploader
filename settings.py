from enum import Enum
from PySide6.QtCore import QSettings


class SettingsKey(Enum):
    WINDOW_GEOMETRY = 'windowGeometry'
    WINDOW_STATE = 'windowState'
    SOURCE_FOLDER = 'sourceFolder'
    TARGET_FILES_MASK = 'targetFilesMask'
    TITLE_TEMPLATE = 'titleTemplate'
    CHECK_PERIOD_MSECS = 'checkPeriodMsecs'


def get_settings_str_value(key: SettingsKey, default: str = ''):
    settings = QSettings()
    return settings.value(key.value, default)


def set_settings_str_value(key: SettingsKey, value: str):
    settings = QSettings()
    settings.setValue(key.value, value)


def get_settings_int_value(key: SettingsKey, default: int = 0):
    settings = QSettings()
    return settings.value(key.value, default)


def set_settings_int_value(key: SettingsKey, value: int):
    settings = QSettings()
    settings.setValue(key.value, value)


def get_settings_byte_array_value(key: SettingsKey, default: bytes = None):
    settings = QSettings()
    return settings.value(key.value, default)


def set_settings_byte_array_value(key: SettingsKey, value: str):
    settings = QSettings()
    settings.setValue(key.value, value)
