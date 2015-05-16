from PySide import QtGui, QtCore

class GeneralListModel(QtCore.QAbstractListModel):

    def __init__(self):
        super(GeneralListModel, self).__init__(None)
        self.data = []

    def rowCount(self, parent):
        return len(self.data)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            item = self.data[index.row()]
            return item.getDisplayName()

    def add(self, item):
        self.beginInsertRows(QtCore.QModelIndex(), len(self.data), len(self.data))
        self.data.append(item)
        self.endInsertRows()