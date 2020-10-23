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

    ####################################################
    #       定义生成校验字段的函数
    #       inputStr:需要传入一个已经转换为16进制的字符串
    #####################################################
    # add crc 16 check at the end of the string
    def crc16(self,inputStr):
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
        crc = self.leftPad(crc[2:], 4)
        # outputStr = inputStr + crc
        outputStr = crc
        return outputStr

    # pad zero to the left of the string if not long enough
    def leftPad(self,inputStr, strLen):
        if (strLen > len(inputStr)):
            outputStr = "0000000000000000000000000000000000000000" + inputStr
            outputStr = outputStr[len(outputStr) - strLen:]
            return outputStr
        else:
            return inputStr

    # pad zero to the right of the string if not long enough
    def rightPad(self,inputStr, strLen):
        if (strLen > len(inputStr)):
            outputStr = inputStr + "0000000000000000000000000000000000000000"
            outputStr = outputStr[: strLen]
            return outputStr
        else:
            return inputStr

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
    print(ResponseBase().hexDate2date("01c329ed065"))
    print(ResponseBase().hexTimestamp2date("5e60723b"))
    print(ResponseBase().hex2string("312c312c767374322e76616e64796f2e636e2c383030332c302c434d4e45542c7975616e686f6e672c70617373776f72640d0a"))


