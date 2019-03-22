#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *


def launch_application(creator):
    def wrapper():
        import sys
        app = QApplication(sys.argv)
        widget = creator()
        widget.show()
        app.exec_()
    return wrapper
