#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor


class Actable(object):
    def _create_action(self, name, trigger):
        action = QAction(name, self)
        action.triggered.connect(trigger)
        return action


class RightClickable(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_right_click_menu()

    def _init_right_click_menu(self):
        self.right_click_menu = QMenu(self)
        self._init_right_click_menu_actions()

    def _init_right_click_menu_actions(self):
        raise NotImplementedError

    # noinspection PyPep8Naming
    def contextMenuEvent(self, event):
        if not isinstance(self, QWidget):
            raise TypeError

        self.right_click_menu.popup(QCursor.pos())
        super().contextMenuEvent(event)


class ComboBox(QComboBox):
    def __init__(self, items=None, default_index=0, default_index_data=None):
        if items is None:
            raise ValueError

        super().__init__()
        self._init_items(items)
        if default_index_data:
            self.setCurrentData(default_index_data)
        else:
            self.setCurrentIndex(default_index)

    def _init_items(self, items):
        for item in items:
            self.addItem(item, item)

    # noinspection PyPep8Naming
    def setCurrentData(self, data):
        index = self.findData(data)
        self.setCurrentIndex(index)


# class MapComboBox(ComboBox):
#     def _init_items(self, config):
#         if isinstance(config, (dict, OrderedDict)):
#             for data, text in config.items():
#                 self.addItem(text, data)
#         elif issubclass(config, Enum):
#             for type_ in config:
#                 self.addItem(type_.value, type_)
#         else:
#             raise ValueError


if __name__ == "__main__":
    from Utility import launch_application

    class _Illustration:
        @staticmethod
        @launch_application
        def launch_actablebutton():
            return _Illustration.ActableButton()

        @staticmethod
        @launch_application
        def launch_simplerightclickable():
            return _Illustration.SimpleRightClickable("Text")

        class ActableButton(Actable, QToolButton):
            def __init__(self):
                super().__init__()
                action_log = self._create_action('logging', lambda: print("On action logging."))
                self.setDefaultAction(action_log)

        class SimpleRightClickable(RightClickable, Actable, QLabel):
            def _init_right_click_menu_actions(self):
                menu = self.right_click_menu

                action_log_a = self._create_action('Log A', lambda: print("AAA"))
                menu.addAction(action_log_a)

                action_log_b = self._create_action('Log B', lambda: print("BBB"))
                menu.addAction(action_log_b)

        class SimpleComboBox(ComboBox):
            def __init__(self):
                super().__init__(items=["name", "class", "grade"])

        @staticmethod
        @launch_application
        def launch_simple_combobox():
            return _Illustration.SimpleComboBox()

    #_Illustration.launch_actablebutton()
    #_Illustration.launch_simplerightclickable()
    _Illustration.launch_simple_combobox()
