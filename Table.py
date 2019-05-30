#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QBrush, QColor


class ProxyTableView(QTableView):
    def __init__(self, source_model=None, proxy_class=QSortFilterProxyModel):
        if not issubclass(proxy_class, QSortFilterProxyModel):
            raise TypeError

        super().__init__()
        self.proxy_model = proxy_class()
        if source_model:
            self.setSourceModel(source_model)
        self.setModel(self.proxy_model)

        self.resizeColumnsToContents()
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    # noinspection PyPep8Naming
    def setSourceModel(self, model):
        self.proxy_model.setSourceModel(model)


class BaseTableModel(QAbstractTableModel):
    """
    QAbstractTableModel with cache-data
    """
    @classmethod
    def get_column_headers(cls, *args):
        raise NotImplementedError

    @classmethod
    def get_model_data(cls, *args):
        raise NotImplementedError

    def __init__(self, *args):
        super().__init__()
        self._init_data(*args)

    def _init_data(self, *args):
        self.column_headers = self.get_column_headers(*args)
        self.model_data = self.get_model_data(*args)

    def rowCount(self, *args):
        return len(self.model_data)

    def columnCount(self, *args):
        return len(self.column_headers)

    def data(self, q_index, role=None):
        if role == Qt.DisplayRole:
            return self.get_cell_data(q_index)
        if role == Qt.BackgroundRole:
            return QBrush(Qt.darkGray)
        if role == Qt.TextColorRole:
            return QBrush(QColor(QVariant("#b0d4b0")))

    def get_cell_data(self, q_index):
        raise NotImplementedError

    def headerData(self, index, orientation, role=None):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.get_column_header(index)
            else:
                return self.get_row_header(index)

    def get_column_header(self, index):
        return self.column_headers[index][0]

    # noinspection PyMethodMayBeStatic
    def get_row_header(self, index):
        return index


# noinspection PyAbstractClass
class BaseDbRecordTableModel(BaseTableModel):
    MODEL = None

    def __init__(self):
        if not self.MODEL:
            raise NotImplementedError
        super().__init__()

    def get_row_header(self, index):
        return self.model_data[index].id


if __name__ == "__main__":
    from Utility import launch_application

    class _Illustration:
        class SimpleModel(BaseTableModel):
            @classmethod
            def get_column_headers(cls, *args):
                # header: tuple(Display i, i)
                return tuple(("Display %d" % i, str(i)) for i in range(3))

            @classmethod
            def get_model_data(cls, *args):
                return [1, 4, 9, 16]

            def get_cell_data(self, q_index):
                return self.model_data[q_index.row()] + q_index.column()

        @staticmethod
        @launch_application
        def launch_simple_view():
            return ProxyTableView(_Illustration.SimpleModel())

        class Filter3ProxyModel(QSortFilterProxyModel):
            def filterAcceptsRow(self, row, model_index):
                # Filter if value mod 3 is 0
                return self.sourceModel().model_data[row] % 3 != 0

            def filterAcceptsColumn(self, column, model_index):
                return True  # Filter none

        @staticmethod
        @launch_application
        def launch_filter_view():
            return ProxyTableView(_Illustration.SimpleModel(),
                                  proxy_class=_Illustration.Filter3ProxyModel)

    # _Illustration.launch_simple_view()
    _Illustration.launch_filter_view()
