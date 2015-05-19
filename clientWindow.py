__author__ = 'd3cr1pt0r'

import sys
from PySide import QtGui
from UserInterface.ClientWindow import ClientWindow

app = QtGui.QApplication(sys.argv)

serverWindow = ClientWindow(800, 400)
serverWindow.show()

sys.exit(app.exec_())