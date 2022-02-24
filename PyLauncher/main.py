import typing
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *
from PyQt5 import *
import sys
import json
import os
import shutil
import importlib.resources as pkg_resources
from . import configs

from PyQt5.QtWidgets import QApplication


class TextController(QObject):
    def __init__(self, filter_proxy_model: QSortFilterProxyModel, app: QApplication):
        super().__init__()
        self.app = app
        self.filter_proxy_model = filter_proxy_model
        self.thread = QThreadImpl(self, app)

    @pyqtSlot(str)
    def on_enter(self, text):
        self.thread.set_command(text)
        self.thread.start()
        self.thread.wait()

    @pyqtSlot(str)
    def on_edit(self, text):
        self.filter_proxy_model.setFilterRegularExpression("^" + text + "(.*)")
        self.filter_proxy_model.invalidateFilter()


class ProgramsListModel(QAbstractListModel):

    def rowCount(self, parent: QModelIndex = ...) -> int:
        if parent.isValid():
            return 0
        else:
            return len(self.entries)

    def roleNames(self) -> typing.Dict[int, 'QByteArray']:

        return {0: QByteArray(b"name")}

    def __init__(self, entries):
        super().__init__()
        self.entries = entries

    def data(self, model_index: QModelIndex, role=None):
        return self.entries[model_index.row()]


class QThreadImpl(QThread):

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.command = None
        self.finished.connect(self.on_finished)

    def on_finished(self):
        self.app.exit(0)

    def set_command(self, command):
        self.command = command

    def run(self):
        os.system("(" + self.command + "& ) && exit")


def start():
    app = QApplication(sys.argv)
    view = QQmlApplicationEngine(app)

    user_config_file_path = os.path.expanduser("~") + "/.config/PyLauncher/config.json"

    if not os.path.exists(user_config_file_path):
        config = pkg_resources.read_text(configs, "config.json")
        with open(user_config_file_path, 'w') as file:
            file.write(config)

    with open(user_config_file_path, 'w') as file:
        data = json.load(file)

    program_list_model = ProgramsListModel(data)
    filter_proxy_model = QSortFilterProxyModel()
    filter_proxy_model.setFilterRole(0)
    filter_proxy_model.setSourceModel(program_list_model)
    program_list_model.setParent(filter_proxy_model)

    text_controller = TextController(filter_proxy_model, app)

    view.rootContext().setContextProperty("filter", filter_proxy_model)
    view.rootContext().setContextProperty("text_controller", text_controller)
    view.load("window.qml")

    sys.exit(app.exec())
