#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum
from PyQt5.QtWidgets import *


class Key(str, Enum):
    DEFAULT_INDEX = 'default_index'
    TABS = 'tabs'
    CONSTRUCTOR = 'constructor'
    ARGS = 'args'
    KWARGS = 'kwargs'
    TEXT = 'text'


class BaseVBoxPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QVBoxLayout())
        self._init_layout()

    def _init_layout(self):
        raise NotImplementedError()


class TabPanel(QTabWidget):
    def __init__(self, *args, config=None):
        super().__init__(*args)

        if config is None:
            config = {}
        self.default_index = config.get(Key.DEFAULT_INDEX, 0)
        self._init_tabs(config.get(Key.TABS, []))

    def _init_tabs(self, tab_configs):
        for config in tab_configs:
            constructor = config.get(Key.CONSTRUCTOR)
            args = config.get(Key.ARGS, [])
            kwargs = config.get(Key.KWARGS, {})
            text = config.get(Key.TEXT, "")
            self.addTab(constructor(*args, **kwargs), text)

        self.setCurrentIndex(self.default_index)


if __name__ == "__main__":
    from Utility import launch_application

    class _Illustration:
        @staticmethod
        @launch_application
        def launch_simplevboxpanel():
            return _Illustration.SimpleVBoxPanel()

        @staticmethod
        @launch_application
        def launch_simpletabpanel():
            return _Illustration.SimpleTabPanel()

        class SimpleVBoxPanel(BaseVBoxPanel):
            def _init_layout(self):
                layout = self.layout()
                layout.addWidget(QLabel("Test"))
                layout.addWidget(QLineEdit())

        class SimpleTabPanel(TabPanel):
            def __init__(self):
                config = {
                    Key.TABS: [{
                        Key.CONSTRUCTOR: QLabel,
                        Key.ARGS: ['LAAAAAAAAAA'],
                        Key.TEXT: 'Label'
                    }, {
                        Key.CONSTRUCTOR: QLineEdit,
                        Key.KWARGS: {'maxLength': 3},
                        Key.TEXT: 'LE'
                    }],
                    Key.DEFAULT_INDEX: 1
                }
                super().__init__(None, config=config)

    _Illustration.launch_simplevboxpanel()
