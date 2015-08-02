# encoding=utf-8
from twisted.internet.protocol import Factory


class RFIDFactory(Factory):
    def __init__(self, name=None, protocol=None):
        self.instanceFactoryName = name
        self.protocol = protocol

        self.numProtocols = 0
        self.conn = None
        self.onlineSession = None
        print self.instanceFactoryName + ' 服务器开始监听 '

    def get_message(self, name, message):
        print name, message

    def message_sibling(self, message):
        self.root.message_child(self.name, message)
