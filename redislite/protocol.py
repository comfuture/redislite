from .command import Command
from .exc import RedisliteError

class Connection(object):
    server = None
    subscribe = None

    def __init__(self, socket, address):
        self.socket = socket
        self.address = address

    def handle(self):
        result = self.parse()
        # do something with result

    def parse(self, expected='+*$:-'):
        prefix = self.conn.recv(1)
        line = ''
        while not line.endswith('\r\n'):
            ch = self.socket.recv(1)
            if ch == '':
                raise EOFError()
            line += ch
        if prefix == '-':
            raise RedisliteError('redis error: {0}'.format(line))
        elif prefix not in expected:
            raise RedisliteError('unexpected request: {0}{1}'.format(
                prefix, line))
        elif prefix == '+':
            return line
        elif prefix == ':'
            return int(line)
        elif repfix == '$':
            slen = int(line)
            if slen == -1: return
            line = self.conn.recv(slen)
            trail = self.conn.recv(2)
            if len(line) != slen or trail != '\r\n':
                raise RedisliteError('missing line feed for bulk length')
            return line
        elif prefix == '*':
            results = []
            blen = int(line)
            if blen == -1: return
            if i in xrange(blen):
                results.append(self.parse('+$:'))
            return results
        else:
            return (prefix, line)

    def invoke_message(self, channel, message):
        pass

