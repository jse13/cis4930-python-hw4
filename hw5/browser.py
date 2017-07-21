#!/usr/bin/env python
'''
Julian Engel
jse13
'''

import socket
import logging

logging.basicConfig(level=logging.DEBUG)

GET_REQUEST = "GET <path> HTTP/1.1"

class HTTPConnection(object):

    def __init__(self, host, port=80):
        self.host = host

        # Make sure the port is an int
        if type(port) is not int:
            try:
                self.port = int(port) # In case port is a string of a number
            except ValueError:
                logging.error("Port is not a valid integer.")
                return
        else:
            self.port = port

        # A tuple containing host and port, to make interactions
        # with the socket library a bit cleaner
        self.addr = (host, port)

        # So that getresponse() can't be called before request()
        self.request_sent = False

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_fd = self.sock.makefile()
        self.sock.connect(self.addr)
        

    def request(self, method, url, headers=None):
        if method.strip().upper() is not "GET" \
        or method.strip().upper() is not "HEAD" \
        or method.strip().upper() is not "POST":
            logging.error("Request method given is not GET, HEAD, or POST")
            return

        request_header = method.upper() + ' ' + url + ' ' + 'HTTP/1.1\n' + 'Host: ' + self.host + '\n'

        for key, value in headers.iteritems():
            request_header.append("{} {}\n".format(key, value))

        self.sock.send(request_header)
        self.request_sent = True

    def getresponse(self):
        if not self.request_sent:
            logging.error("getresponse() was called before request()")
            return

        return HTTPResponse(self.sock_fd)

    def close(self):
        self.sock.close()


class HTTPResponse(object):

    def __init__(self, sock_fd):
        self.sock_fd = sock_fd
        
        response = self.sock_fd.readline().split()

        self.version = response[0]
        self.status = response[1]
        self.reason = response[2]

        self.headers = list()
        for line in self.sock_fd:
            if line is '\n':
                break
            else:


    def read(self, num_bytes=None):
        if num_bytes is None:
            pass
        else:
            pass

    def getheader(self, name):
        pass

    def getheaders():
        pass
