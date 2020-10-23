#encoding:utf-8
import binascii
import time

from lib.protocol.Base import Base

class ResponseBase(Base):
    def __init__(self):
        pass

    #####################################################
    #               数字转换为16进制字符串
    #####################################################
    def int2hexString(self, num):
        hexStr = hex(num)[2:]
        if (len(hexStr) % 2) == 1:
            hexStr = "0" + hexStr
        return hexStr

    #####################################################
    #               数字转换为16进制字符串，通过传入字节数可自动补0
    #               传入数据格式所占字节数
    #####################################################
    def int2hexStringByBytes(self, num,bytescount=1):
        hexStr = hex(num)[2:]
        while len(hexStr) < (bytescount * 2):
            hexStr = "0" + hexStr
        return hexStr

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
    # utc 时间格式的16进制字符串转时间
    ######################################################
    def hexDate2date(self,hexData):
        UTCTime = "20"
        UTCTime = UTCTime + str(self.hexString2int(hexData[:2]))
        UTCTime = UTCTime + "-" +  str(self.hexString2int(hexData[2:4]))
        UTCTime = UTCTime + "-" +  str(self.hexString2int(hexData[4:6]))
        UTCTime = UTCTime + " " +  str(self.hexString2int(hexData[6:8]))
        UTCTime = UTCTime + ":" +  str(self.hexString2int(hexData[8:10]))
        UTCTime = UTCTime + ":" +  str(self.hexString2int(hexData[10:12]))
        return UTCTime

    #######################################################
    # 时间戳的16进制字符串转时间
    ######################################################
    def hexTimestamp2date(self,hexData):
        timeStamp = self.hexString2int(hexData)
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

if __name__ == "__main__":
    # print(ResponseBase().hexDate2date("01c329ed065"))
    # print(ResponseBase().hexTimestamp2date("5e60723b"))
    print(ResponseBase().hex2string("4d3530304142303230322e303030432c3131312e31302e32342e3133312c32312c7673742c767374323031332c4d3530304142303230322e303030432e42494e2c"))


