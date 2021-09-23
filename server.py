#  coding: utf-8
import socketserver
import os, re, sys
from urllib import request
import os.path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

path = 'www'
www_files = os.listdir(path)


class MyWebServer(socketserver.BaseRequestHandler):
    def get_file_type(self, file_name):
        file_type = re.findall('(?:.*\.)(\w+)', file_name)

        return file_type[0]

    def read_user_request(self, required_file):
        if not re.match('^/$', required_file):
            try:
                if not re.search('\.', required_file):
                    if not os.path.exists("www" + required_file):

                        self.request.sendall(
                            bytes("HTTP/1.1 404 Not Found\r\n", "utf-8"))

                    elif re.search('(?:\/(\w+)+)\/', required_file):

                        file_folder = '\r\n'.join(
                            os.listdir('www' + required_file))
                        self.request.sendall(
                            bytes("HTTP/1.1 200 OK\r\n", "utf-8"))

                        self.request.send(("Content-type: text/%s \r\n\r\n" %
                                           'html').encode('utf-8'))

                        with open('www' + required_file + 'index.html',
                                  'rb') as user_file:
                            file_data = user_file.read()
                        self.request.sendall(file_data)
                    else:

                        self.request.sendall(
                            bytes("HTTP/1.1 301 Moved Permanently\r\n",
                                  "utf-8"))
                        self.request.sendall(
                            bytes('www' + required_file + '/', 'utf-8'))

                elif re.search('\.', required_file):
                    with open('www' + required_file, 'rb') as user_file:
                        file_data = user_file.read()
                        file_type = self.get_file_type(required_file)
                        self.request.sendall(
                            bytes("HTTP/1.1 200 OK\r\n", "utf-8"))

                        self.request.send(("Content-type: text/%s \r\n\r\n" %
                                           file_type).encode('utf-8'))
                        self.request.sendall(file_data)

            except:
                self.request.send(
                    "HTTP/1.1 404 Not Found \r\n".encode('utf-8'))

        elif re.match('^/$', required_file):
            file_folder = '\r\n'.join(os.listdir('www'))
            self.request.sendall(bytes("HTTP/1.1 200 OK\r\n", "utf-8"))

            self.request.send(
                ("Content-type: text/%s \r\n\r\n" % 'html').encode('utf-8'))

            with open('www/' + 'index.html', 'rb') as user_file:
                file_data = user_file.read()
            self.request.sendall(file_data)

        else:
            pass

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("Got a request of: %s\r\n" % self.data)
        print(f'\r\nuser_data: {self.data.decode()}')

        if re.search('GET', self.data.decode()):
            required_file = re.findall('(?:GET\s)([^\s]+)(?:\s.+)',
                                       self.data.decode())
            self.read_user_request(required_file[0])
        else:
            self.request.sendall(bytes("HTTP/1.1 405 Not Allowed\r\n",
                                       "utf-8"))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
