__author__ = 'd3cr1pt0r'

import sys
from PySide import QtGui
from UserInterface.ServerWindow import ServerWindow
from UserInterface.ClientWindow import ClientWindow

app = QtGui.QApplication(sys.argv)

serverWindow = ServerWindow(800, 400)
serverWindow.show()

clientWindow = ClientWindow(800, 400)
clientWindow.show()

sys.exit(app.exec_())