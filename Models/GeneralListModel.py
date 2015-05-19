from PySide import QtGui, QtCore

class GeneralListModel(QtCore.QAbstractListModel):
    _data = []

    def __init__(self):
        super(GeneralListModel, self).__init__(None)
        self._data = []

    def rowCount(self, parent):
        return len(self._data)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()].displayName

    def add(self, item):
        self.beginInsertRows(QtCore.QModelIndex(), len(self._data), len(self._data))
        self._data.append(item)
        self.endInsertRows()