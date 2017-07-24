#!/usr/bin/env python
'''
Julian Engel
jse13
'''

import socket
import logging

socket.setdefaulttimeout(2.0)

logging.basicConfig(level=logging.INFO)

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
        self.sock_fd = self.sock.makefile('arb')
        self.sock.connect(self.addr)
        

    def request(self, method, url, headers=None):
        self.connect()
        request_header = method.upper() + ' ' + url + ' ' + 'HTTP/1.1\n' + 'Host: ' + self.host + '\n\n'

        if headers is not None:
            for key, value in headers.iteritems():
                request_header += "{} {}\n".format(key, value)

        logging.debug("Sending this header: \"{}\"".format(request_header))
        self.sock.send(request_header)
        self.request_sent = True
        self.close()

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

        # Number of bytes read by the read() function
        self.bytes_read = 0

        response = self.sock_fd.readline().split()
        logging.debug("First line of response is {}".format(response))

        self.version = response[0].replace("HTTP/", "")
        self.status = response[1]
        self.reason = response[2]

        self.headers = list()
        for line in self.sock_fd:
            # The separator between the headers and the content is both a 
            # carriage return and a newline character
            if line == "\r\n":
                break
            else:
                logging.debug("Reading line \"{}\"".format(line))
                x = line.replace("\r\n", "").split(":")
                self.headers.append((x[0], x[1].lstrip()))

        
        logging.debug("Headers are:\n{}".format("\n".join(str(x) for x in self.headers)))

        # Get the rest of the contents of the request
        self.resp_body = ""

        if "Content-Length" in dict(self.headers):
            logging.debug("Content-Length of {} given".format(dict(self.headers)["Content-Length"]))
            self.resp_body += self.sock_fd.read(int(dict(self.headers)["Content-Length"]))

        elif "Transfer-Encoding" in dict(self.headers) \
        and dict(self.headers)["Transfer-Encoding"] == "chunked":
            more_data = True
            next_line = ""
            chunk_size = 0
            while more_data:
                next_line = self.sock_fd.readline()
                if next_line == "\r\n":
                    continue
                try:
                    chunk_size = int(next_line.replace('\n','').replace('\r', ''), 16)
                except Exception:
                    continue
                logging.debug("Chunk size is {}".format(chunk_size))
                if chunk_size == 0:
                    more_data = False
                self.resp_body += self.sock_fd.read(chunk_size)

        self.bytes_read = 0


    def read(self, num_bytes=None):
        to_return = ""
        if num_bytes is None:
            to_return = self.resp_body[self.bytes_read:]
            self.bytes_read = len(self.resp_body)

        elif self.bytes_read >= len(self.resp_body):
            to_return = ""

        elif self.bytes_read + num_bytes > len(self.resp_body):
            to_return = self.resp_body[self.bytes_read :]
            self.bytes_read = len(self.resp_body)

        else:
            to_return = self.resp_body[self.bytes_read : self.bytes_read+num_bytes]
            self.bytes_read += num_bytes

        return to_return


    def getheader(self, name):
        for header in self.headers:
            if header[0] == name:
                return header[1]
        return None

    def getheaders(self):
        if len(self.headers) > 0:
            return self.headers
        else:
            return None
