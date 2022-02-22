import asyncio
import typing
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQml import *
from PyQt5.QtQuick import *
from PyQt5 import *
import sys
import json
import os
import subprocess

from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
view = QQmlApplicationEngine(app)


class TextController(QObject):
    def __init__(self, filter_proxy_model: QSortFilterProxyModel, app: QApplication):
        super().__init__()
        self.app = app
        self.filter_proxy_model = filter_proxy_model
        self.thread = QThreadImpl(self)

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

    def __init__(self, parent=None):
        super().__init__(parent)
        self.command = None
        self.finished.connect(self.on_finished)

    def on_finished(self):
        app.exit(0)

    def set_command(self, command):
        self.command = command

    def run(self):
        os.system("(" + self.command + "& ) && exit")


data = None
with open('config.json') as json_file:
    data = json.load(json_file)

program_list_model = ProgramsListModel(data)
filter_proxy_model = QSortFilterProxyModel()
filter_proxy_model.setFilterRole(0)
filter_proxy_model.setSourceModel(program_list_model)
program_list_model.setParent(filter_proxy_model)

text_controller = TextController(filter_proxy_model, app)

view.rootContext().setContextProperty("filter", filter_proxy_model)
view.rootContext().setContextProperty("text_controller", text_controller)
view.load("window.qml")
root_object = view.rootObjects()[0]

sys.exit(app.exec())
