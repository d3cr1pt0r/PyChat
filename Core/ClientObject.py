__author__ = 'd3cr1pt0r'

class ClientObject(object):
    name = None
    address = None

    def __init__(self, client):
        self.client = client