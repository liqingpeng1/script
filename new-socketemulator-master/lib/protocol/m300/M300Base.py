#encoding:utf-8
import datetime
import random
import time

from lib.protocol.Base import Base

'''
定义消息协议类的基类
'''

class M300Base(Base):
    def __init__(self):
        self.IDENTIFY = "7e"     #标识位

    #获取消息属性
    def getMsgProperty(self,msgBodyLen=128,encryptionType=0):
        if msgBodyLen >= 512:
            raise RuntimeError('消息体长度超长！')
        msgBodyLen = msgBodyLen                                  #消息体长度
        encryptionType = encryptionType                          #加密方式
        retain = 0                                               #保留位
        data = msgBodyLen + encryptionType + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex

    #######################################################
    # 获取消息体
    #######################################################
    def getMsgBody(self):
        return ""

    #######################################################
    # 获取校验码
    #######################################################
    def getCheckCode(self,data="aa"):
        if len(data) % 2 == 1:
            raise RuntimeError('数据段错误！')
        start = data[0:2]
        tmp = int(start,16)
        for i in range(2,len(data),2):
            tmp = tmp ^ int(data[i:i + 2],16)
        dataHex = self.int2hexStringByBytes(tmp)
        return dataHex

    #######################################################
    # 替换消息中的7e7d字符
    #######################################################
    def replace7e7d(self,data):
        tmpR = data
        tmp = tmpR[0:2]
        tmpA = tmpR[0:2]
        tmpR = tmpR[2:]
        data = ""
        while tmpA != "":
            if tmp == "7d":
                tmp = "7d01"
            elif tmp == "7e":
                tmp = "7d02"
            data = data + tmp
            tmp = tmpR[0:2]
            tmpA = tmpR[0:2]
            tmpR = tmpR[2:]
        return data

    #######################################################
    # 字符串转16进制
    #######################################################
    def str2Hex(self,data):
        dataHex = ""
        tem = ""
        for i in data:
            tem = ord(i)
            dataHex += hex(tem)[2:]
        return dataHex

    #######################################################
    # 16进制转字符串
    #######################################################
    def hex2Str(self,data):
        theStr = ""
        while data != "":
            tmp = data[:2]
            data = data[2:]
            theStr = theStr + chr(int(tmp,16))
        return theStr

    #####################################################
    # 将字符串转换为对应的ascii值数组
    #####################################################
    def str2Ascsii(self,data):
        asciiArr = []
        for i in range(0, len(data)):
            asciiValue = ord(data[i])
            asciiArr.append(asciiValue)
        return asciiArr

    ####################################################
    # 将整数转换为有符号的整数
    #####################################################
    def num2signedNum(self,num):
        return num & 0xff

    #####################################################
    # 数字转换为16进制字符串，通过传入字节数可自动补0
    # 传入数据格式所占字节数
    #####################################################
    def int2hexStringByBytes(self, num,bytescount=1):
        hexStr = hex(num)[2:]
        while len(hexStr) < (bytescount * 2):
            hexStr = "0" + hexStr
        return hexStr

    ####################################################
    # 将10进制转换位8421码
    #####################################################
    def int2BCD(self,data,bytescount=6):
        data = str(data)
        while len(data) < bytescount * 2:
            data = "0" + data
        return data

    #####################################################
    # 设备id转换为16进制的设备id
    #####################################################
    def devid2hexString(self, id):
        # 获取第一个字符的ASCII值
        ascii = ord(id[0:1])
        # 将10进制的ASCII值转换为16进制
        ascii = self.int2hexStringByBytes(ascii)
        devid = str(ascii) + id[1:]
        return devid


if __name__ == "__main__":
    pass
