#!/usr/bin/env python3

# Copyright (C) 2017 Adam Smith

# This file is part of Reaper

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import traceback

import qdarkstyle
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QDesktopServices

from components.job_queue import Queue
from components.keys import KeyPage
from components.sources import SourceTabs
from components.widgets.nodes import PrimaryInputWindow
from components.widgets.progress import ProgressWidget
from components.widgets.queue import QueueTable
from components.windows import *
from components.globals import *
from ui.mainwindow import Ui_MainWindow


class Reaper(Ui_MainWindow):

    def __init__(self, window, app, splash, show=True):
        super().__init__()

        self.version = "v2.5.4"
        self.source_file = "sources.xml"
        self.encoding = "utf-8"
        self.cache_enabled = True

        self.window = window
        self.app = app
        self.splash = splash

        self.splash_msg("Setting up UI")
        self.setupUi(window)

        self.window.setWindowIcon(QIcon("ui/icon.png"))
        self.window.setWindowTitle(f"Reaper {self.version}")

        self.advanced_mode = False
        self.dark_mode = False

        self.splash_msg("Identifying app type")

        # Add windows and actions
        self.splash_msg("Connecting widgets")
        self.add_windows()
        self.add_actions()

        # Create queue page
        self.splash_msg("Creating Queue")
        self.queue = Queue(self)
        self.queue.job_error.connect(self.error_window.job_error)
        self.queue.job_error_log.connect(self.error_window.log_error)
        self.error_window.cancelButton.clicked.connect(self.queue.stop_retrying)

        self.splash_msg("Adding icons")
        self.set_icons()

        # Create queue table
        self.splash_msg("Creating job queue")
        self.queue_table = QueueTable()
        self.queueLayout.addWidget(self.queue_table)

        # Create window for primary key input
        self.splash_msg("Creating input window")
        self.primaryInputWindow = PrimaryInputWindow(window)

        # Create api key page
        self.splash_msg("Creating API tab")
        self.key_page = KeyPage(self.scrollAreaWidgetContents, DATA_DIR)

        # Create sources page
        self.splash_msg("Creating Source tab")
        self.source_tabs = SourceTabs(
            self, self.key_page, self.source_file, self.primaryInputWindow
        )

        # Create progress page
        self.splash_msg("Creating progress tab")
        self.progress_page = ProgressWidget(self.queue.job_update, self.tabWidget)
        self.progressLayout.addWidget(self.progress_page)

        if show:
            self.splash_msg("Showing window")
            window.show()

    def splash_msg(self, message):
        self.splash.showMessage(message)

    def enable_advanced_mode(self, bool):
        self.advanced_mode = bool

    def enable_dark_mode(self, bool):
        if bool:
            self.app.setStyleSheet("")
        else:
            self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    def add_actions(self):
        self.actionErrorManager.triggered.connect(self.show_error_manager)
        self.actionAdvanced_mode.toggled.connect(self.enable_advanced_mode)
        self.actionDark_mode.toggled.connect(
            lambda x: self.settings_window.set_light_mode(not x)
        )
        self.actionQuit.triggered.connect(self.quit)
        self.actionHelp.triggered.connect(self.open_website)
        self.actionAbout.triggered.connect(self.open_website)
        self.actionReport_a_bug.triggered.connect(self.open_report)
        self.actionWebsite.triggered.connect(self.open_website)
        self.actionAPI_Key_file.triggered.connect(self.import_keys)
        self.actionAPI_Keys.triggered.connect(self.export_keys)

    def add_windows(self):
        self.license_window = LicenseWindow(self.window)
        self.actionLicenses.triggered.connect(self.license_window.pop)

        self.error_window = ErrorWindow(self.window)

        self.settings_window = SettingsWindow(self)
        self.actionSettings.triggered.connect(self.settings_window.show)

    def set_icons(self):
        self.queueUp.setIcon(QIcon(f"{BUNDLE_DIR}{sep}ui/up.png"))
        self.queueDown.setIcon(QIcon(f"{BUNDLE_DIR}{sep}ui/down.png"))
        self.queueRemove.setIcon(QIcon(f"{BUNDLE_DIR}{sep}ui/remove.png"))
        self.window.setWindowIcon(QIcon(f"{BUNDLE_DIR}{sep}ui/icon.ico"))

    def show_error_manager(self, _):
        self.error_window.show()

    def open_website(self, _):
        QDesktopServices.openUrl(QUrl("http://reaper.social"))

    def open_report(self, _):
        QDesktopServices.openUrl(QUrl("https://github.com/scriptsmith/reaper/issues"))

    def export_keys(self, _):
        title = "Export Reaper keys"
        filter = "JSON File (*.json)"
        options = QtWidgets.QFileDialog.Options()

        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(
            caption=title,
            directory=self.settings_window.get_save_path(),
            filter=filter,
            options=options,
        )
        if filePath:
            with open(filePath, "w") as f:
                json.dump(self.key_page.sources, f)

    def import_keys(self, _):
        title = "Import Reaper keys"
        filter = "JSON File (*.json)"
        options = QtWidgets.QFileDialog.Options()

        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            caption=title,
            directory=self.settings_window.get_save_path(),
            filter=filter,
            options=options,
        )
        if filePath:
            with open(filePath, "r") as f:
                sources = json.load(f)

                for i in range(self.key_page.scrollWidget.layout.count()):
                    self.key_page.scrollWidget.layout.takeAt(i)

                for source in sources.keys():
                    self.key_page.add_source(source, sources[source].keys())

    def quit(self, _):
        self.app.quit()


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)

        pixmap = QtGui.QPixmap("ui/splash.png")
        splash = QtWidgets.QSplashScreen(pixmap)
        splash.show()
        splash.showMessage("Starting reaper")
        app.processEvents()

        main_window = QtWidgets.QMainWindow()
        ui = Reaper(main_window, app, splash)

        splash.finish(main_window)

        sys.exit(app.exec_())
    except Exception as e:
        with open(LOG_DIR + "/log.log", "a") as f:
            f.write(str(e))
            f.write(traceback.format_exc())
