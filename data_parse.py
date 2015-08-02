#encoding=utf-8
from locale import atoi

base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]
def dec_to_hex(string_num):#十进制转化为十六进制,输入格式为:十进制字符串
    # print string_num
    num = int(string_num)
    # print num
    mid = []
    while True:
        num, rem = divmod(num, 16)
        mid.append(base[rem])
        if num == 0: break
        # num,rem = divmod(num, 16)
        # mid.append(base[rem])
    return ''.join([str(x) for x in mid[::-1]])

import binascii
# print dec_to_hex("18")#4141
# print binascii.a2b_hex(dec_to_hex("16705"))#AA


def dev_id0(str_hex):  # 小段存储的设备id号转化为正常的id号
    # print str_hex
    str_hex = dec_to_hex(str_hex)
    # print str_hex
    str_hex = [str_hex[i:i + 2] for i in range(0, len(str_hex), 2)]
    # print str_hex
    str_hex.reverse()
    print str_hex
    str_hex = "".join(str_hex)
    print str_hex
    return str_hex
# print dev_id0("576460752338092035")
# Container({'type': [9, 0], 'value': [0, 0, 128, 63], 'unit': [18, 0]})
def dev_id(dec_list):  # 小段存储的设备id号转化为正常的id号,输入为十进制列表

    if type(dec_list) == type([]):
        dec_list.reverse()
        strhex = ""
        for x in dec_list:
            # print x
            str_hex = dec_to_hex(str(x))
            if len(str_hex) == 1:
                strhex += '0' + str_hex
            else:
                strhex += str_hex
            # print str_hex
    else:
        str_hex = dec_to_hex(dec_list)
        # print str_hex
        str_hex = [str_hex[i:i + 2] for i in range(0, len(str_hex), 2)]
        # print str_hex
        str_hex.reverse()
        # print str_hex
        strhex = "".join(str_hex)
        # print str_hex

    return strhex
# print dev_id([0, 0, 128, 63])
# print dev_id("576460752338092035")

def dec_to_ascill(str_num):#十进制ascill码转化为字符
    import binascii
    print dec_to_hex(str_num)  # 4141
    return binascii.a2b_hex(dec_to_hex(str_num))  #AA
# print dec_to_ascill("16705")


#hex_to_dec
# 十六进制 to 十进制:int(str,n=16)
def hex_to_dec(str_num):
    return str(int(str_num.upper(), 16))
# print hex_to_dec("0E")


def hex_to_float(str_hex):#十六进制转化为浮点数
    if len(str_hex) != 8:
        print "您输入的值不是8位"
        print str_hex
        return None
    else:
        import struct
        return struct.unpack('!f',str_hex.decode('hex'))[0]


# 字符串转字节串:
#
# 字符串编码为字节码: '12abc'.encode('ascii') == > b'12abc'
# 数字或字符数组: bytes([1, 2, ord('1'), ord('2')]) == > b'\x01\x0212'
# 16
# 进制字符串: bytes().fromhex('010210') == > b'\x01\x02\x10'
# 16
# 进制字符串: bytes(map(ord, '\x01\x02\x31\x32')) == > b'\x01\x0212'
# 16
# 进制数组: bytes([0x01, 0x02, 0x31, 0x32]) == > b'\x01\x0212'



# def str_to_hex(str_hex):
#     hex_str_lisr = str.split(" ")
#     hex_str_lisr = ['\x'+x for x in hex_str_lisr]
#     print hex_str_lisr
# str_to_hex("12 34 52")

#去除空格
def del_space(str):
    return str.replace(" ","")
print del_space("23 4343 fdfd   vdvd")
#crc16反模式数据校验算法
def CRC_XModem(hex_list):
    crc_value = 0
    polynomial = 0x1021
    for x in hex_list:
        for i in range(0, 8):
            bit = x >> (7 - i) & 1
            c15 = crc_value >> 15 & 1
            crc_value <<= 1
            if c15 ^ bit:
                crc_value ^= polynomial
        # print crc_value
    crc_value &= 0xffff
    return crc_value

# print CRC_XModem(strHex_toHex('FFFFF2070884A1'))
# print CRC_XModem([0xFF, 0xFF, 0xF2, 0x07, 0x08, 0x84, 0xA1])#ok


def strHex_toHex(str_hex):#十六进制字符串转化为十进制
    list = []
    for i in range(1,len(str_hex),2):
        list.append(int(str_hex[i-1:i+1],16))
    # print list
    return list

# print strHex_toHex('FFFFF2070884A1')
# bytearray.fromhex('FFFFF2070884A1')
# print CRC_XModem(strHex_toHex('FFFFF2070884A1'))
# print type(hex(int('bf', 16)))

# list = ['10', '20', '30']
# 将str数组转换为int数组
# int_list = [int(i) for i in list]
# 将int数组转换为16进制数组
# hex_list = [hex(i) for i in int_list]
#
# print list
# print int_list
# print hex_list