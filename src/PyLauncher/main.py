import encodings
import typing
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *
from PyQt5 import *
import sys
import json
import os
from . import config
from . import data
import importlib.resources as pkg_resources
from PyQt5.QtWidgets import QApplication


class TextController(QObject):
    def __init__(self, filter_proxy_model: QSortFilterProxyModel, app: QApplication, parent=None):
        super().__init__(parent=parent)
        self.app = app
        self.filter_proxy_model = filter_proxy_model
        self.thread = QThreadImpl(app, self)

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
        self.quit()
        self.app.quit()

    def set_command(self, command):
        self.command = command

    def run(self):
        os.system("(" + self.command + "& ) && exit")


def start():
    app = QApplication(sys.argv)
    view = QQmlApplicationEngine(app)

    user_config_file_path = os.path.expanduser("~") + "/.config/PyLauncher/config.json"
    user_config_folder_path = os.path.expanduser("~") + "/.config/PyLauncher/"

    if not os.path.exists(user_config_file_path):
        os.mkdir(user_config_folder_path)
        config_json = pkg_resources.read_text(config, "config.json")
        with open(user_config_file_path, 'w+') as file:
            file.write(config_json)

    with open(user_config_file_path, 'r') as file:
        json_data = json.load(file)

    program_list_model = ProgramsListModel(json_data)
    filter_proxy_model = QSortFilterProxyModel(view)
    filter_proxy_model.setFilterRole(0)
    filter_proxy_model.setSourceModel(program_list_model)
    program_list_model.setParent(view)

    text_controller = TextController(filter_proxy_model, app, view)

    view.rootContext().setContextProperty("filter", filter_proxy_model)
    view.rootContext().setContextProperty("text_controller", text_controller)

    # Loading file manually because of a strange error that attaches /home/lorenzo in front
    # of the path passed as parameter in the method QQmlApplicationEngine::load(url: QUrl)
    window_qml = pkg_resources.read_text(data, "window.qml")
    # Loading file from an array of bytes
    view.loadData(QByteArray(bytearray(window_qml, "utf_8")))

    sys.exit(app.exec())
