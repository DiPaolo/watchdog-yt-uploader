# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTableWidget, QTableWidgetItem,
    QTimeEdit, QToolButton, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1134, 776)
        self.gridLayout_2 = QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.gridLayout_2.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout = QGridLayout(self.tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 5, -1, 5)
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.source_folder = QLineEdit(self.tab)
        self.source_folder.setObjectName(u"source_folder")

        self.horizontalLayout_2.addWidget(self.source_folder)

        self.choose_source_folder = QToolButton(self.tab)
        self.choose_source_folder.setObjectName(u"choose_source_folder")

        self.horizontalLayout_2.addWidget(self.choose_source_folder)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.tab)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.target_files_mask = QLineEdit(self.tab)
        self.target_files_mask.setObjectName(u"target_files_mask")

        self.horizontalLayout_5.addWidget(self.target_files_mask)

        self.apply_target_files_mask = QPushButton(self.tab)
        self.apply_target_files_mask.setObjectName(u"apply_target_files_mask")

        self.horizontalLayout_5.addWidget(self.apply_target_files_mask)


        self.gridLayout.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
#ifndef Q_OS_MAC
        self.horizontalLayout.setSpacing(-1)
#endif
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, -1, 0)
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.yt_channel_name = QLineEdit(self.tab)
        self.yt_channel_name.setObjectName(u"yt_channel_name")
        self.yt_channel_name.setEnabled(True)
        self.yt_channel_name.setReadOnly(True)

        self.horizontalLayout.addWidget(self.yt_channel_name)

        self.upload_media = QPushButton(self.tab)
        self.upload_media.setObjectName(u"upload_media")

        self.horizontalLayout.addWidget(self.upload_media)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.target_files_stats = QLabel(self.tab)
        self.target_files_stats.setObjectName(u"target_files_stats")

        self.horizontalLayout_3.addWidget(self.target_files_stats)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.show_target_files_only = QCheckBox(self.tab)
        self.show_target_files_only.setObjectName(u"show_target_files_only")

        self.horizontalLayout_3.addWidget(self.show_target_files_only)


        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)

        self.files_tree = QTreeWidget(self.tab)
        self.files_tree.setObjectName(u"files_tree")
        self.files_tree.header().setStretchLastSection(True)

        self.gridLayout.addWidget(self.files_tree, 4, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(self.tab)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.check_period = QTimeEdit(self.tab)
        self.check_period.setObjectName(u"check_period")
        self.check_period.setTime(QTime(0, 15, 0))

        self.horizontalLayout_6.addWidget(self.check_period)

        self.label_7 = QLabel(self.tab)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_6.addWidget(self.label_7)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.start_watch = QPushButton(self.tab)
        self.start_watch.setObjectName(u"start_watch")

        self.horizontalLayout_6.addWidget(self.start_watch)

        self.stop_watch = QPushButton(self.tab)
        self.stop_watch.setObjectName(u"stop_watch")

        self.horizontalLayout_6.addWidget(self.stop_watch)


        self.gridLayout.addLayout(self.horizontalLayout_6, 5, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_3 = QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.log_list = QTableWidget(self.tab_2)
        self.log_list.setObjectName(u"log_list")

        self.gridLayout_3.addWidget(self.log_list, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_2.addWidget(self.tabWidget, 1, 0, 1, 1)

        QWidget.setTabOrder(self.tabWidget, self.source_folder)
        QWidget.setTabOrder(self.source_folder, self.choose_source_folder)
        QWidget.setTabOrder(self.choose_source_folder, self.target_files_mask)
        QWidget.setTabOrder(self.target_files_mask, self.apply_target_files_mask)
        QWidget.setTabOrder(self.apply_target_files_mask, self.yt_channel_name)
        QWidget.setTabOrder(self.yt_channel_name, self.upload_media)
        QWidget.setTabOrder(self.upload_media, self.files_tree)
        QWidget.setTabOrder(self.files_tree, self.check_period)
        QWidget.setTabOrder(self.check_period, self.start_watch)
        QWidget.setTabOrder(self.start_watch, self.stop_watch)
        QWidget.setTabOrder(self.stop_watch, self.log_list)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Source Folder:", None))
        self.choose_source_folder.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Target Files Mask", None))
        self.apply_target_files_mask.setText(QCoreApplication.translate("Dialog", u"Apply", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"YouTube Channel:", None))
        self.upload_media.setText(QCoreApplication.translate("Dialog", u"Change", None))
        self.target_files_stats.setText(QCoreApplication.translate("Dialog", u"<placeholder>", None))
        self.show_target_files_only.setText(QCoreApplication.translate("Dialog", u"Show Target Files Only", None))
        ___qtreewidgetitem = self.files_tree.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Dialog", u"Actions", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Dialog", u"Status", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Dialog", u"File", None));
        self.label_6.setText(QCoreApplication.translate("Dialog", u"Check Period:", None))
        self.check_period.setDisplayFormat(QCoreApplication.translate("Dialog", u"HH:mm:ss", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"(HH:mm:ss)", None))
        self.start_watch.setText(QCoreApplication.translate("Dialog", u"Start Watch", None))
        self.stop_watch.setText(QCoreApplication.translate("Dialog", u"Stop Watch", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Dialog", u"Setup", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Dialog", u"Log", None))
    # retranslateUi

