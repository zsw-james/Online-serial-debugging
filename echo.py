# encoding=utf-8
from twisted.internet.protocol import Protocol


class EchoProtocol(Protocol):
    def connectionMade(self):
        print 'connected ok'
        self.factory.onlineSession.add_client('echo', self.transport)
        self.divName = str(self) + "  of  " + self.__class__.__name__

    def connectionLost(self, reason):
        self.factory.onlineSession.del_client(self.divName)
        return

    def dataReceived(self, data):
        print data


from twisted.internet.protocol import Factory


class EchoFactory(Factory):
    def __init__(self, quote=None, protocol=None):
        self.quote = quote
        self.protocol = protocol
        print self.quote + ' service listener is started!'
