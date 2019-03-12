#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import unittest
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect

from ..Window import BaseWindow


class Simple:
    CONFIG = {
        "title": "T",
        "width": 100,
        "height": 200,
        "x_axis": 3,
        "y_axis": 4
    }

    class SimpleWindow(BaseWindow):
        def _create_main_panel(self):
            return QWidget(self)

        def _load_config(self):
            return Simple.CONFIG


class ConfigApplicationTest(unittest.TestCase):
    def test_simple_window(self):
        app = QApplication(sys.argv)
        window = Simple.SimpleWindow()
        self.assertEqual("T", window.windowTitle())
        self.assertEqual(QRect(3, 4, 100, 200), window.geometry())
