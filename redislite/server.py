from gevent.server import StreamServer
from .exc import RedisliteError
from .protocol import Connection
from .database import DAO

class Server(StreamServer):

    connections = []

    def __init__(self, host='127.0.0.1', port=6379, dbfile=None):
        self.host = host
        self.port = port

        self.dao = DAO(dbfile)
        self.dao.broadcast_func = self._broadcast_func()

        super(Server, self).__init__((host, port,), self.handle)

    def handle(self, sock, address):
        self.connections.append(Client(sock, address))

    def _broadcast_func(self):

        def func(channel, message):
            for conn in self.connections:
                if conn.subscribe == 'channel':
                    conn.invoke_message(message)

        return func

    def listen(self):
        self.serve_forever().start()