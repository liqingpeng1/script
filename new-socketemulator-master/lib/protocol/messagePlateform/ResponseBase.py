#encoding:utf-8
import binascii

from lib.protocol.Base import Base

class ResponseBase(Base):
    def __init__(self):
        pass

    #######################################################
    # 二进制转换为ascii码
    #######################################################
    def binary2ascii(self,binData):
        strs = binascii.b2a_hex(binData)
        strsLen = len(str(strs))
        data = str(strs)[2:strsLen - 1]
        return data

    #######################################################
    # 还原消息中被转换过的7e和7d
    #######################################################
    def restore_7e7d(self,data):
        data = data.replace("7d02", "7e")
        data = data.replace("7d01", "7d")
        return data

    #######################################################
    # 去除标识位
    #######################################################
    def removeIdentify(self,data):
        dataLen = len(data)
        data = data[2:dataLen - 2]
        return data

    #######################################################
    # 10进制转换为2进制字符串
    #######################################################
    def int2binStr(self,data,bytescount=1):
        binStr = bin(data)
        binStr = binStr[2:]
        bytesLen = bytescount * 8
        while len(binStr) < bytesLen:
            binStr = "0" + binStr
        return binStr

    #######################################################
    # 16进制字符串转换为整数
    #######################################################
    def hexString2int(self, data):
        val = int(data,16)
        return val

    #######################################################
    # 16进制字符串转换为ascii字符串
    #######################################################
    def hex2string(self,data):
        theStr = ""
        while data != "":
            tmp = data[:2]
            data = data[2:]
            theStr = theStr + chr(int(tmp, 16))
        return theStr

    #######################################################
    # BCD时间格式转换为GMD时间格式
    #######################################################
    def getBCD2GMTTime(self,data):
        theTime = "20"
        theTime = theTime + data[:2]
        theTime = theTime + "-" + data[2:4]
        theTime = theTime + "-" + data[4:6]
        theTime = theTime + " " + data[6:8]
        theTime = theTime + ":" + data[8:10]
        theTime = theTime + ":" + data[10:]
        return theTime

    #######################################################
    # 通过原始数据，获取消息id
    #######################################################
    def getMsgId(self, data):
        data = self.removeIdentify(data)
        data = self.restore_7e7d(data)
        header = data[:24]
        msgId = header[:4]  # 消息id
        return msgId


    #######################################################
    # 16进制转换为GBK字符串
    #######################################################
    def hex2GBKString_res(self,dataHex):
        dataStr = self.hex2Str(dataHex)
        data = bytes(map(ord,str(dataStr)))
        data = data.decode("gbk")
        return data



if __name__ == "__main__":
    # print(ResponseBase().int2binStr(7,2))
    # print(ResponseBase().getMsgId("7e0002000001314620111800065b7e"))
    # print(ResponseBase().getMsgId("7e80010005013146201118e1480006000200767e"))
    print(ResponseBase().hex2string("014c3230304142303030302c737a6c696e6779692e716963702e7669702c383838392c537a4c696e6759692c7a373254713246742c4c3230304142303130322e303030342e42494e2c2f2c"))
    print(ResponseBase().hexString2int("00001f43 "))