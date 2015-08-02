# encoding=utf-8
import binascii
import functools
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from RFIDController import RFIDController
from RFIDFrame import rfidFrame


class RFIDProtocol(Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.data_list = ""  # 用来拼接阅读器发送过来的的不完整的数据
        self.rfid = RFIDController()
        self.getOnlineSession = self.factory.onlineSession.online_session

    def connectionMade(self):
        self.factory.numProtocols += 1  # 工厂创造的protocol数目加1
        print '<----------- 连接成功,当前连接的RFID设备数目为: ' + str(self.factory.numProtocols) + ' ---------->'

        self.divName  = str(self) + "  of  " + self.__class__.__name__
        self.factory.onlineSession.add_client(self.divName, self.transport)
        self.ping(timeout=1)
        return

    def ping(self, timeout):
        frame = "\xFF\xFF\xF1\x06\x06\xF1"
        self.transport.write(frame)
        cb = functools.partial(self.ping, timeout=timeout)
        reactor.callLater(timeout, cb)  # 定时器,timeout秒后调用cb函数

    def connectionFailed(self):
        print "Connection Failed:", self.__class__.__name__
        reactor.stop()

    def connectionLost(self, reason):
        print 'conn lost reason --> ' + str(reason) + "\n"
        self.factory.numProtocols -= 1

        print 'current conn num is ' + str(self.factory.numProtocols) + "\n"
        self.factory.onlineSession.del_client(self.divName)
        return

    def dataReceived(self, data):
        '''因为没有办法对字节流进行判断所以先转换成十六进制数从而判断是否接收的完整'''

        self.data_list += binascii.b2a_hex(data)  # 接受字节流的数据转化成十六进制字符串
        # print self.data_list
        if len(self.data_list) > 4:  # 对接收的数据包的丢包处理
            if self.data_list[0:4] != "ffff":
                self.data_list = "ffff" + self.data_list.split("ffff")[-1]
                # else:
                #      self.data_list = "ffff" + self.data_list.split("ffff")[0]
        frame = bytearray.fromhex(self.data_list)  # 将十六进制的数再次转化成字节流
        pkgs, leftovers = self.rfid.parse_pkgs(frame)  # 解析字节流转化为可识别的指令码存在pkgs,剩下的存在leftovers
        if self.factory.onlineSession.get_online_session('echo'):
                self.factory.onlineSession.get_online_session('echo').write(pkgs)
        if len(pkgs) != 0 and len(leftovers) == 0:
            rfidFrame.handle_data(pkgs)

            # self.transport.write(str(bytearray.fromhex(frame)))  #只能传输字符串所以先转换为字节流

# if CRC_XModem(strHex_toHex(self.data_list)) != 0:
#         self.data_list = ''
#         return
#
#         important_data = self.data_p(pkgs)
#         # print important_data
#         for div in self.getOnlineSession:
#             if div == self.divName:
#                 print "设备" + div + "正在把数据-->"
#         for div in self.getOnlineSession:
#             if div.split("##")[-1] == 'RFIDProtocol':
#
#                 if len(important_data) == 1:
#                     print "数据为空\n"
#
#                 if len(important_data) != 1:
#                     print important_data
#                     # self.getOnlineSession[div].write(important_data)
#                     print "传递 给:" + div
#                     #  important_data = ""
#
#         else:
#             print important_data
#
#         print "\n"
#         # print self.data_list
#         important_data = ""
#         self.data_list = ""
#     return
#
# def data_p(self, pkgs):
#
#     data = ""  # 处理卡号和触发器id
#     important_data = ""
#     for pkg in pkgs[0].data.block:
#         cardID = pkg.CardID
#         if cardID[0] == 1:
#             print dec_to_hex(cardID[1]) + dec_to_hex(cardID[2]), "电量异常"
#         data += dec_to_hex(cardID[1])
#         data += dec_to_hex(cardID[2])
#
#         triggerID = pkg.triggerID
#         if triggerID != 0:
#             important_data += hex_to_dec(data) + ":" + str(triggerID) + ","
#         data = ""
#
#     important_data = important_data[0:-1] + "\n"
#     return important_data
