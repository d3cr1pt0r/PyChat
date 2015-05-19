__author__ = 'd3cr1pt0r'

import json
from PySide import QtGui
from Core.Server import Server
from UserInterface.Parts.ListView import ListView
from Models.ClientListModelItem import ClientListModelItem

class ServerWindow(QtGui.QWidget):
    isServerRunning = False

    def __init__(self, width=500, height=200, parent=None):
        super(ServerWindow, self).__init__(parent)
        self.server = Server(1994)
        self.server.onNewConnection.connect(self.onNewConnection)
        self.server.onDataReceived.connect(self.onDataReceived)
        self.initUI(width, height)

    def initUI(self, width, height):
        self.setStyleSheet(open("assets/darkorange.stylesheet", "r").read())
        self.setGeometry(300, 100, width, height)
        self.setWindowTitle('Server')

        hlayout = QtGui.QHBoxLayout()
        vlayout1 = QtGui.QVBoxLayout()
        vlayout2 = QtGui.QVBoxLayout()

        self.clientListView = ListView()

        self.messageArea = QtGui.QTextEdit()
        self.messageArea.setMinimumWidth(550)
        self.messageArea.setReadOnly(True)

        self.sendText = QtGui.QLineEdit()
        self.sendText.returnPressed.connect(self.onSendText)

        self.portText = QtGui.QLineEdit()
        self.portText.setText('1994')

        self.toggleServerButton = QtGui.QPushButton('Start server')
        self.toggleServerButton.clicked.connect(self.toggleServer)

        vlayout1.addWidget(self.messageArea)
        vlayout1.addWidget(self.sendText)
        vlayout2.addWidget(self.clientListView)
        vlayout2.addWidget(self.portText)
        vlayout2.addWidget(self.toggleServerButton)

        hlayout.addLayout(vlayout1)
        hlayout.addLayout(vlayout2)

        self.setLayout(hlayout)

    def toggleServer(self):
        if not self.isServerRunning:
            self.addLine('Starting server...')
            self.toggleServerButton.setText('Stop server')
            self.server.start()
        else:
            self.addLine('Stopping server...')
            self.toggleServerButton.setText('Start server')
            self.server.stop()

        self.isServerRunning = not self.isServerRunning

    def onSendText(self):
        text = self.sendText.text()
        if text != '':
            for c in self.server.clients:
                c.client.send(json.dumps({'name': 'SERVER', 'message': text}))
            self.sendText.setText('')
            self.addLine(text)

    def onNewConnection(self, clientObject):
        item = ClientListModelItem(str(clientObject.address), clientObject)
        self.clientListView.add(item)
        self.addLine('Connection request from ' + str(clientObject.address))

    def onDataReceived(self, clientObject, data):
        _data = json.loads(data)
        for c in self.server.clients:
            c.client.send(data)
        self.addLine(_data['name'] + ': ' + _data['message'])

    def addLine(self, line=''):
        current_text = self.messageArea.toPlainText()
        current_text += line + '\n'
        self.messageArea.setPlainText(current_text)