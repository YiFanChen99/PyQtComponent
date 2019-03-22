#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *

from Utility import launch_application


class Actable(object):
    def _create_action(self, name, trigger):
        action = QAction(name, self)
        action.triggered.connect(trigger)
        return action


class _Illustration:
    @staticmethod
    @launch_application
    def launch_actablebutton():
        return _Illustration.ActableButton()

    class ActableButton(Actable, QToolButton):
        def __init__(self):
            super().__init__()
            action_log = self._create_action('logging', lambda: print("On action logging."))
            self.setDefaultAction(action_log)


if __name__ == "__main__":
    _Illustration.launch_actablebutton()
