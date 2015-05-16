__author__ = 'd3cr1pt0r'
import socket
import thread
from PySide import QtCore
from Core.ClientObject import ClientObject

class Server(QtCore.QObject):
    onNewConnection = QtCore.Signal(object)
    clients = []
    isServerRunning = False

    def __init__(self, port):
        super(Server, self).__init__()
        self.port = port

    def start(self):
        print 'Starting server on port ' + str(self.port)

        self.socket = socket.socket()
        self.socket.setblocking(0)
        self.socket.bind((socket.gethostname(), self.port))
        self.socket.listen(5)
        self.isServerRunning = True

        thread.start_new_thread(self.awaitConnections, ())

    def stop(self):
        for client in self.clients:
            client.client.close()

        self.isServerRunning = False
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            print 'Failed to shutdown socket...'
        try:
            self.socket.close()
        except:
            print 'Failed to close socket...'

    def getClientList(self):
        return self.clients

    def awaitConnections(self):
        while True and self.isServerRunning:
            try:
                c, addr = self.socket.accept()
            except:
                continue

            c.send('yolo')
            clientObject = ClientObject(c)
            clientObject.address = addr
            clientObject.name = 'None'
            clientObject.nickname = 'None'

            self.clients.append(clientObject)
            self.onNewConnection.emit(clientObject)

            thread.start_new_thread(self.handleClient, (clientObject,))

    def handleClient(self, clientObject):
        while self.isServerRunning:
            try:
                data = clientObject.client.recv(1024)
            except:
                continue

            if not data:
                continue

            print 'Data recieved:'
            print data