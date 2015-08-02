# coding=utf-8
'''
#2015-1-28  created by wangke


###########################################################################################
'''
from construct import Struct, OptionalGreedyRange, Embed, Enum, Switch
from construct import UBInt8, UBInt16, UBInt32, UBInt64, Byte
from construct.macros import Array
from RFIDDatabase import rfidDb
from data_parse import dec_to_hex, hex_to_dec, CRC_XModem, strHex_toHex


class RfidFrame(object):
    def __init__(self):
        # 接收数据的数据格式定义
        self.rfidFrame = Struct("frame",
                                OptionalGreedyRange(
                                    Struct("packets",
                                           UBInt16("header"),
                                           Enum(UBInt8("cmdcode"),
                                                F1=0xF1,
                                                F2=0xF2,
                                                F3=0xF3,
                                                F4=0xF4,
                                                ),
                                           Switch("datas", lambda ctx: ctx.cmdcode, {
                                               "F1": Struct("sub",
                                                            UBInt8("readerID"),
                                                            UBInt8("packet_len"),
                                                            UBInt8("status"),
                                                            Array(lambda ctx: (
                                                                                  ctx.packet_len - 2 - 1 - 1 - 1 - 1 - 2) / 6,
                                                                  Struct("blocks",
                                                                         # UBInt8('elec'),
                                                                         Array(3, UBInt8('cardID')),
                                                                         UBInt8('triggerID'),
                                                                         UBInt16('relativeTime')
                                                                         )
                                                                  )
                                                            ),
                                               "F2": Struct("sub", UBInt8("packet_len"), UBInt8("readerID")),
                                               "F3": Struct("sub", UBInt8("packet_len"), UBInt8("result")),
                                               "F4": Struct("sub", UBInt8("packet_len"), UBInt8("rssl")),
                                           }
                                                  ),
                                           UBInt16("crc"),
                                           )
                                ),
                                OptionalGreedyRange(
                                    UBInt8("leftovers"),
                                ),
                                )
        self.readerID = None
        self.rssl = 1
        self.triggerID = None

    def rfidFrameParse(self, bytestream):
        return self.rfidFrame.parse(bytestream)

    def handle_data(self, pkgs):
        cmdcode = pkgs[0].cmdcode
        # datas = pkgs.packets.datas[0]
        # 对指令码判断工作模式
        if cmdcode == "F1":
            # 存储温度，湿度，以及其他数据
            print self.data_p(pkgs)
            # #rfidDb.saveID( self.cardID,self.triggerID,) #存储触发器id和卡号到数据库
            #
            # print 'the trigger ID is ：', self.triggerID
            # print 'the card ID is ：', self.cardID

        elif cmdcode == "F2":
            # 得到阅读器id
            self.readerID = self.getReaderID(pkgs)
            print self.readerID

        elif cmdcode == 'F3':  # 此处还不能写小写的f3,是字符串匹配,要和系统返回的一样.否则无法进入循环
            # 获得设置门限值的结果
            result = self.getResult(pkgs)
            result = hex(result)  # 此处result的值是2进制数要转换成16进制数来进行门限值的设置结果判断

            if result == '0xaa':
                print 'setted success'
            else:
                print 'setted falure'

        elif cmdcode == "F4":
            # 得到门限值
            self.rssl = self.getRSSI(pkgs)
            print self.rssl

    def getReaderID(self, pkgs):
        return pkgs[0].datas.readerID

    def getCardID(self, pkgs):
        return pkgs[0].datas.blocks[0].cardID

    def getTriggerID(self, pkgs):
        return pkgs[0].datas.blocks[0].triggerID

    def getResult(self, pkgs):
        return pkgs[0].datas.result

    def getRSSI(self, pkgs):
        return pkgs[0].datas.rssl

    def data_p(self, pkgs):

        data = ""  # 处理卡号和触发器id
        important_data = ""
        for pkg in pkgs[0].datas.blocks:
            cardID = pkg.cardID
            if cardID[0] == 1:
                print cardID
                print dec_to_hex(cardID[1]) + dec_to_hex(cardID[2]), "电量异常"

            data += dec_to_hex(cardID[1])
            data += dec_to_hex(cardID[2])

            triggerID = pkg.triggerID
            if triggerID != 0:
                important_data += hex_to_dec(data) + ":" + str(triggerID) + ","
            data = ""

        important_data = important_data[0:-1] + "\n"
        return important_data


rfidFrame = RfidFrame()

# if __name__ == '__main__':
#     rfid = RfidFrame()
#     data = rfid.parse_pkgs(
#         'FF FF F1 07 26 05 00 13 9A 00 00 1D 80 13 8E 00 00 1D 00 13 8C 00 00 1D 00 13 8D 00 00 15 80 13 94 00 00 13 77 F9')
#     print data
