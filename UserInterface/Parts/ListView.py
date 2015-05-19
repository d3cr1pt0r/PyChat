__author__ = 'd3cr1pt0r'
from PySide import QtCore, QtGui
from Models.GeneralListModel import GeneralListModel

class ListView(QtGui.QListView):

    def __init__(self):
        super(ListView, self).__init__()
        self.model = GeneralListModel()
        self.setModel(self.model)

    def add(self, item):
        self.model.add(item)

