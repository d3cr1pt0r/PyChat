__author__ = 'd3cr1pt0r'

import socket, thread
from PySide import QtGui
from UserInterface.Parts.ListView import ListView

class ClientWindow(QtGui.QWidget):
    client = None

    def __init__(self, width=500, height=200, parent=None):
        super(ClientWindow, self).__init__(parent)
        self.initUI(width, height)

    def initUI(self, width, height):
        self.setStyleSheet(open("assets/darkorange.stylesheet", "r").read())
        self.setGeometry(300, 540, width, height)
        self.setWindowTitle('Client')

        hlayout = QtGui.QHBoxLayout()
        vlayout1 = QtGui.QVBoxLayout()
        vlayout2 = QtGui.QVBoxLayout()

        self.clientListView = ListView()

        self.messageArea = QtGui.QTextEdit()
        self.messageArea.setMinimumWidth(550)
        self.messageArea.setReadOnly(True)

        self.hostText = QtGui.QLineEdit()
        self.hostText.setText('93.103.137.194')

        self.portText = QtGui.QLineEdit()
        self.portText.setText('1994')

        self.toggleConnectButton = QtGui.QPushButton('Connect')
        self.toggleConnectButton.clicked.connect(self.toggleConnect)

        vlayout1.addWidget(self.messageArea)
        vlayout2.addWidget(self.clientListView)
        vlayout2.addWidget(self.hostText)
        vlayout2.addWidget(self.portText)
        vlayout2.addWidget(self.toggleConnectButton)

        hlayout.addLayout(vlayout1)
        hlayout.addLayout(vlayout2)

        self.setLayout(hlayout)

    def toggleConnect(self):
        host = self.hostText.text()
        port = self.portText.text()

        self.addLine('Connecting to ' + host + ':' + port)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, int(port)))

        self.addLine('Connected')

        thread.start_new_thread(self.listenForData, ())
        #self.client.shutdown(socket.SHUT_RDWR)
        #self.client.close()

    def listenForData(self):
        while True:
            data = self.client.recv(1024)
            print str(data)

    def addLine(self, line=''):
        current_text = self.messageArea.toPlainText()
        current_text += line + '\n'
        self.messageArea.setPlainText(current_text)