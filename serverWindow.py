__author__ = 'd3cr1pt0r'

import sys
from PySide import QtGui
from UserInterface.ServerWindow import ServerWindow

app = QtGui.QApplication(sys.argv)

serverWindow = ServerWindow(800, 400)
serverWindow.show()

sys.exit(app.exec_())