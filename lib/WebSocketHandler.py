import struct
import SocketServer
from base64 import b64encode
from hashlib import sha1
from mimetools import Message
from StringIO import StringIO
import threading, time, os

from Settings import Settings

class WebSocketsHandler(SocketServer.StreamRequestHandler):
    magic = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

    def checkForUpdate(self):
        update = 0
        settings = Settings(os.getcwd() + '/' +"wlc_load.db") # i coded myself into a corner
        while True:
            if update < settings.get("lastUpdate"):
                #send data to client
                self.broadCast_Msg("Hello....smells like success")
            time.sleep(2)

    def setup(self):
        SocketServer.StreamRequestHandler.setup(self)
        print "connection established", self.client_address
        self.handshake_done = False

        self.connections = []

        self.updateThread = threading.Thread(target=self.checkForUpdate)
        self.updateThread.daemon = True
        self.updateThread.start()

    def handle(self):
        while True:
            if not self.handshake_done:
                self.handshake()
            else:
                self.read_next_message()

    def read_next_message(self):
        length = ord(self.rfile.read(2)[1]) & 127
        if length == 126:
            length = struct.unpack(">H", self.rfile.read(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", self.rfile.read(8))[0]
        masks = [ord(byte) for byte in self.rfile.read(4)]
        decoded = ""
        for char in self.rfile.read(length):
            decoded += chr(ord(char) ^ masks[len(decoded) % 4])
        self.on_message(str(decoded))

    def broadCast_Msg(self, message):
        for connection in self.connections:
            connection.send(chr(129))
            length = len(message)
            if length <= 125:
                connection.send(chr(length))
            elif length >= 126 and length <= 65535:
                connection.send(126)
                connection.send(struct.pack(">H", length))
            else:
                connection.send(127)
                connection.send(struct.pack(">Q", length))
            connection.send(message)

    def send_message(self, message):
        self.request.send(chr(129))
        length = len(message)
        if length <= 125:
            self.request.send(chr(length))
        elif length >= 126 and length <= 65535:
            self.request.send(126)
            self.request.send(struct.pack(">H", length))
        else:
            self.request.send(127)
            self.request.send(struct.pack(">Q", length))
        self.request.send(message)

    def handshake(self):
        data = self.request.recv(1024).strip()
        headers = Message(StringIO(data.split('\r\n', 1)[1]))
        if headers.get("Upgrade", None) != "websocket":
            return
        print 'Handshaking...'
        key = headers['Sec-WebSocket-Key']
        digest = b64encode(sha1(key + self.magic).hexdigest().decode('hex'))
        response = 'HTTP/1.1 101 Switching Protocols\r\n'
        response += 'Upgrade: websocket\r\n'
        response += 'Connection: Upgrade\r\n'
        response += 'Sec-WebSocket-Accept: %s\r\n\r\n' % digest
        self.handshake_done = self.request.send(response)
        self.connections.append(self.request)

    def on_message(self, message):
        print message
        self.send_message("Hey from the server")
