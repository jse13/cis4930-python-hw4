#!/usr/bin/env python
'''
Julian Engel
jse13
'''

import socket
import logging

logging.basicConfig(level=logging.DEBUG)

GET_REQUEST = "GET <path> HTTP/1.1\nHost: <host>"

class HTTPConnection(object):

    def __init__(self, host, port=80):
        self.host = host
        self.port = port

        # A tuple containing host and port, to make interactions
        # with the socket library a bit cleaner
        self.addr = (host, port)

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.addr)
        

    def request(self, method, url, headers=None):
        pass

    def getresponse(self):
        to_return = HTTPResponse(None)

        return to_return

    def close(self):
        pass


class HTTPResponse(object):

    def __init__(self, sock):
        self.sock = sock
        
        self.version = None
        self.status = None
        self.reason = None

    def read(self, num_bytes=None):
        pass

    def getheader(self, name):
        pass

    def getheaders():
        pass
