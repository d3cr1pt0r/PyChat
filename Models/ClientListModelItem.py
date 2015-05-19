__author__ = 'd3cr1pt0r'

class ClientListModelItem():
    displayName = None
    clientSocket = None

    def __init__(self, name, clientSocket):
        self.displayName = name
        self.clientSocket = clientSocket