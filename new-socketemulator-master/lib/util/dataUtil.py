#coding:utf-8

'''
定义一个处理数据包的辅助方法集合
'''
from binascii import *
from crcmod import *
import struct

#####################################################
# 定义生成校验字段的函数(自己翻译的函数，简化了很多步骤)
#####################################################
def myCrc16(msg):
    msg = str2Ascsii(msg)
    crc = 0xFFFF
    for i in range(0, len(msg)):
        for j in range(0, 8):
            cl5 = ((crc >> 15 & 1) == 1)
            bit = ((msg[i] >> (7 - j) & 1) == 1)
            crc <<= 1
            # 通过与0xFFFF（即二进制：1111111111111111）做了一个或运算，将其转换为一个有符号的数
            crc &= 0xFFFF
            if (cl5 ^ bit):
                crc ^= 0x1021;
    crc = hex(crc)  # 将10进制的crc转换为16进制
    crc = str(crc)[2:]  # 将16进制转换为字符串，并去掉前面的0x
    return crc


#####################################################
#                 定义生成校验字段的函数
#                inputStr:需要传入一个已经转换为16进制的字符串
#####################################################
# add crc 16 check at the end of the string
def crc16(inputStr):
    inputStrByte = bytes.fromhex(inputStr)
    crc = 0xFFFF
    for i in range(0, len(inputStrByte)):
        for j in range(0, 8):
            c15 = (crc >> 15) == 1
            bit = ((inputStrByte[i] >> (7 - j)) & 1) == 1
            crc <<= 1
            crc &= 0xFFFF
            if c15 ^ bit:
                crc ^= 0x1021
    crc = str(hex(crc))
    crc = leftPad(crc[2:], 4)
    # outputStr = inputStr + crc
    outputStr = crc
    return outputStr


# pad zero to the left of the string if not long enough
def leftPad(inputStr, strLen):
    if (strLen > len(inputStr)):
        outputStr = "0000000000000000000000000000000000000000" + inputStr
        outputStr = outputStr[len(outputStr) - strLen:]
        return outputStr
    else:
        return inputStr


# pad zero to the right of the string if not long enough
def rightPad(inputStr, strLen):
    if (strLen > len(inputStr)):
        outputStr = inputStr + "0000000000000000000000000000000000000000"
        outputStr = outputStr[: strLen]
        return outputStr
    else:
        return inputStr


#####################################################
#                 将字符串转换为16进制的数字字符串
#####################################################
def str2Hex(s):
    s_hex=""
    for i in range(len(s)):
        s_hex=s_hex+hex(ord(s[i]))[2:]+" "
    return s_hex

#####################################################
#                 将字符串转换为16进制的数字字符串,并去掉空格
#####################################################
def str2HexStrip(s):
    s = str2Hex(s)
    s2 = s.replace(" ","")
    return s2

#####################################################
#                 将字符串转换为对应的ascii值数组
#####################################################
def str2Ascsii(s):
    asciiArr = []
    for i in range(0,len(s)):
        asciiValue = ord(s[i])
        asciiArr.append(asciiValue)
    return asciiArr



if __name__ == "__main__":
    # print(crc16(str2Hex("aa")))
    # print(str2Hex("aa"))
    # print(str2HexStrip("aa"))
    # print(str2Ascsii("aa"))
    print(myCrc16("4040007000064d20191201000200120114030503202d26d7fffff0000000000505000000143c00000bb80100000fa00000000a0000000000005e60723b723b39331e100055320000001312001007d0001e0000000000000096000000280096ffff3e0001f40000003e0000000000000000000000"))
    # print(crc16(str2HexStrip("aa")))
