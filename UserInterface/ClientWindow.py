__author__ = 'd3cr1pt0r'

import json
from PySide import QtGui
from UserInterface.Parts.ListView import ListView
from Core.Client import Client

class ClientWindow(QtGui.QWidget):
    client = None
    isClientConnected = False

    def __init__(self, width=500, height=200, parent=None):
        super(ClientWindow, self).__init__(parent)
        self.client = Client()
        self.client.onConnectionEstablished.connect(self.onConnectionEstablished)
        self.client.onConnectionTerminated.connect(self.onConnectionTerminated)
        self.client.onDataReceived.connect(self.onDataReceived)
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

        self.sendText = QtGui.QLineEdit()
        self.sendText.returnPressed.connect(self.onSendText)

        self.nameText = QtGui.QLineEdit()
        self.nameText.setText('noname')

        self.hostText = QtGui.QLineEdit()
        self.hostText.setText('93.103.137.194')

        self.portText = QtGui.QLineEdit()
        self.portText.setText('1994')

        self.toggleConnectButton = QtGui.QPushButton('Connect')
        self.toggleConnectButton.clicked.connect(self.toggleConnect)

        vlayout1.addWidget(self.messageArea)
        vlayout1.addWidget(self.sendText)
        vlayout2.addWidget(self.clientListView)
        vlayout2.addWidget(self.nameText)
        vlayout2.addWidget(self.hostText)
        vlayout2.addWidget(self.portText)
        vlayout2.addWidget(self.toggleConnectButton)

        hlayout.addLayout(vlayout1)
        hlayout.addLayout(vlayout2)

        self.setLayout(hlayout)

    def toggleConnect(self):
        if not self.isClientConnected:
            host = self.hostText.text()
            port = self.portText.text()

            self.addLine('Connecting to ' + host + ':' + port)
            if self.client.connectToHost(host, port):
                self.toggleConnectButton.setText('Disconnect')
                self.isClientConnected = True
            else:
                self.addLine('Failed to connect!')
        else:
            self.client.disconnectFromHost()
            self.toggleConnectButton.setText('Connect')
            self.isClientConnected = False

    def onSendText(self):
        name = self.nameText.text()
        text = self.sendText.text()
        if text != '':
            self.client.sendText(json.dumps({'name': name, 'message': text}))
            self.sendText.setText('')

    def onConnectionEstablished(self, s):
        self.addLine('Connection established to: ' + str(s))

    def onConnectionTerminated(self):
        self.addLine('Connection terminated')

    def onDataReceived(self, data):
        _data = json.loads(data)
        self.addLine(_data['name'] + ': ' + _data['message'])

    def addLine(self, line=''):
        current_text = self.messageArea.toPlainText()
        current_text += line + '\n'
        self.messageArea.setPlainText(current_text)