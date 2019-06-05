#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QBrush, QColor


class ProxyTableView(QTableView):
    def __init__(self, source_model=None, proxy_model=None):
        if proxy_model is None:
            proxy_model = QSortFilterProxyModel()
        elif not isinstance(proxy_model, QSortFilterProxyModel):
            raise TypeError('proxy_model')

        super().__init__()
        self.proxy_model = proxy_model
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

    @property
    def source_model(self):
        return self.proxy_model.sourceModel()


class ProxyModel(QSortFilterProxyModel):
    def __init__(self, conditions=None):
        super().__init__()
        self.conditions = {}
        self.row_rules = {}
        self.column_rules = {}
        for cond in conditions:
            self.conditions[cond.key] = cond
            if cond.is_standard:
                self.row_rules[cond.key] = cond.row_rule
                self.column_rules[cond.key] = cond.column_rule

    def filterAcceptsRow(self, row, model_index):
        record = self.sourceModel().model_data[row]
        return all(rule(record) for rule in self.row_rules.values())

    def filterAcceptsColumn(self, column, model_index):
        header = self.sourceModel().get_column_header(column)
        return all(rule(header) for rule in self.column_rules.values())

    def get_condition_value(self, key):
        return self.conditions[key].standard_value

    def update_condition_value(self, key, value):
        condition = self.conditions[key]

        self.beginResetModel()
        condition.standard_value = value
        self._update_rules_by_condition(condition)
        self.endResetModel()

    def change_condition(self, condition):
        self.beginResetModel()
        self.conditions[condition.key] = condition
        self._update_rules_by_condition(condition)
        self.endResetModel()

    def _update_rules_by_condition(self, condition):
        if condition.is_standard:
            self.row_rules[condition.key] = condition.row_rule
            self.column_rules[condition.key] = condition.column_rule
        else:  # remove old rule if existed
            self.row_rules.pop(condition.key, None)
            self.column_rules.pop(condition.key, None)


class ProxyModelCondition(object):
    @staticmethod
    def generate_default_record_getter(key):
        return lambda record: getattr(record, key)

    @staticmethod
    def generate_default_comparator():
        return lambda record_value, standard: record_value == standard

    def __init__(self, key, value=None, getter=None, comparator=None, hidden_column=None):
        """
        :param key: Id, usually use attr name
        :param value: Standard value
        :param getter: Getter for value-from-record.
        :param comparator: How to compare record-value with standard-value.
        :param hidden_column: The hidden column when is_standard.
        """
        self.key = key
        self.standard_value = value
        self._init_getter(getter)
        self._init_comparator(comparator)
        self._init_hidden_column(hidden_column, comparator)

    def _init_getter(self, getter):
        if getter is None:
            getter = self.generate_default_record_getter(self.key)
        self.record_getter = getter

    def _init_comparator(self, comparator):
        if comparator is None:
            comparator = self.generate_default_comparator()
        self.comparator = comparator

    def _init_hidden_column(self, hidden_column, comparator):
        if hidden_column is None:
            hidden_column = True if comparator is None else False
        self.hidden_column = hidden_column

    @property
    def is_standard(self):
        return self.standard_value is not None

    @property
    def row_rule(self):
        if not self.is_standard:
            raise ValueError
        return lambda record: self.comparator(
            self.record_getter(record), self.standard_value)

    @property
    def column_rule(self):
        if not self.is_standard:
            raise ValueError
        return lambda header: header != self.hidden_column


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

        class FilterZ3ProxyModel(QSortFilterProxyModel):
            def filterAcceptsRow(self, row, model_index):
                # Filter if value mod 3 is 0
                return self.sourceModel().model_data[row] % 3 != 0

            def filterAcceptsColumn(self, column, model_index):
                return True  # Filter none

        @staticmethod
        @launch_application
        def launch_simple_filter_view():
            return ProxyTableView(_Illustration.SimpleModel(),
                                  proxy_model=_Illustration.FilterZ3ProxyModel())

        class Filter9ProxyModel(ProxyModel):
            def __init__(self):
                conditions = (
                    ProxyModelCondition(
                        key='int', value=9, getter=lambda rec: rec,
                        comparator=lambda value, std: value != std),
                )
                super().__init__(conditions)

        @staticmethod
        @launch_application
        def launch_condition_filter_view():
            return ProxyTableView(_Illustration.SimpleModel(),
                                  proxy_model=_Illustration.Filter9ProxyModel())

    # _Illustration.launch_simple_view()
    # _Illustration.launch_simple_filter_view()
    _Illustration.launch_condition_filter_view()
