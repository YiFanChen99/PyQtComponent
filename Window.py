#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class Key(str, Enum):
    TITLE = 'title'
    WIDTH = 'width'
    HEIGHT = 'height'
    X_AXIS = 'x_axis'
    Y_AXIS = 'y_axis'


class BaseWindow(QMainWindow):
    def __init__(self, parent=None, config=None):
        if config is None:
            config = self._load_config()

        super().__init__(parent)
        self._init_central_widget()
        self._init_layout()
        self.apply_config(config)
        self.setWindowModality(Qt.WindowModal)

    @property
    def central_layout(self):
        return self.centralWidget().layout()

    def _init_central_widget(self):
        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        self.setCentralWidget(widget)

    def _init_layout(self):
        self._init_main_panel()

    def _init_main_panel(self):
        self.main_panel = self._create_main_panel()
        self.central_layout.addWidget(self.main_panel)

    def _create_main_panel(self):
        raise NotImplementedError()

    def _load_config(self):
        raise NotImplementedError()

    def apply_config(self, config):
        self.resize(config[Key.WIDTH], config[Key.HEIGHT])
        self.move(config[Key.X_AXIS], config[Key.Y_AXIS])
        self.setWindowTitle(config[Key.TITLE])


class _WindowExtendable(object):
    def __init__(self, **kwargs):
        if not isinstance(self, BaseWindow):
            raise TypeError("Not a BaseWindow.")

        super().__init__(**kwargs)


if __name__ == "__main__":
    from Utility import launch_application

    class _Illustration:
        @staticmethod
        @launch_application
        def launch_simplewindow():
            return _Illustration.SimpleWindow()

        class SimpleWindow(BaseWindow):
            def _create_main_panel(self):
                return QWidget(self)

            def _load_config(self):
                return {
                    "title": "T",
                    "width": 100,
                    "height": 200,
                    "x_axis": 3,
                    "y_axis": 4
                }

    _Illustration.launch_simplewindow()
