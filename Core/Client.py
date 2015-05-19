__author__ = 'd3cr1pt0r'

from PySide import QtCore
import socket
import thread

class Client(QtCore.QObject):
    onConnectionEstablished = QtCore.Signal(object)
    onConnectionTerminated = QtCore.Signal()
    onDataReceived = QtCore.Signal(object)

    host = None
    port = None
    client = None

    def __init__(self, host=None, port=None):
        super(Client, self).__init__()
        self.host = host
        self.port = port

    def connectToHost(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client.connect((self.host, int(self.port)))
        except:
            return False

        self.onConnectionEstablished.emit(self.client)
        thread.start_new_thread(self.listenForData, ())

        return True

    def disconnectFromHost(self):
        try:
            self.client.shutdown(socket.SHUT_RDWR)
        except:
            print 'Failed to shutdown socket...'
        try:
            self.client.close()
        except:
            print 'Failed to close socket...'

        self.onConnectionTerminated.emit()

    def sendText(self, text):
        self.client.send(text)

    def listenForData(self):
        while True:
            data = self.client.recv(1024)
            self.onDataReceived.emit(data)