import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from folder_watcher import FolderWatcher
from main_dialog import MainDialog

if __name__ == "__main__":
    QCoreApplication.setOrganizationName("DiPaolo")
    QCoreApplication.setOrganizationDomain("dipaolo.com")
    QCoreApplication.setApplicationName("watchdog-yt-uploader")

    app = QApplication(sys.argv)

    # watchdog = FolderWatcher()
    # watchdog.start('/Users/dipaolo/repos/watchdog-yt-uploader')

    mainDlg = MainDialog()
    mainDlg.show()

    sys.exit(app.exec())
