#encoding:utf-8
from lib.protocol.Base import Base

'''
定义协议类的基类
'''

class ProtocolBase(Base):

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

    #####################################################
    #               设备id转换为16进制字符串
    #####################################################
    def devid2hexString(self, id):
        # 获取第一个字符的ASCII值
        ascii = ord(id[0:1])
        # 将10进制的ASCII值转换为16进制
        ascii = self.int2hexString(int(ascii))
        devid = str(ascii) + id[1:]
        return devid

    ####################################################
    #               获取消息体长度
    #####################################################
    def getMsgLength(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData


    #####################################################
    #               获取流水号
    #####################################################
    def getWaterCode(self,num):
        hexData = self.int2hexString(num)
        while len(hexData) < 4:
            hexData = "0" + hexData
        return hexData

    #####################################################
    #               获取校验码
    #####################################################
    def getCheckCode(self,data):
        return self.crc16(data)

    #####################################################
    #                 定义生成校验字段的函数(自己翻译的函数，简化了很多步骤)
    #                 通过我实现的方式
    #####################################################
    def myCrc16(self,msg):
        msg = self.str2Ascsii(msg)
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
    #                 将字符串转换为对应的ascii值数组
    #####################################################
    def str2Ascsii(self,s):
        asciiArr = []
        for i in range(0, len(s)):
            asciiValue = ord(s[i])
            asciiArr.append(asciiValue)
        return asciiArr

    #####################################################
    #   将字符串转换为对应的ascii字母对应的16进制字符串
    #####################################################
    def str2Hex(self,s):
        sHex = ""
        tem = ""
        for i in s:
            tem = ord(i)
            sHex += hex(tem)[2:]
        return sHex


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

    #####################################################
    #               将UTC时间转换为16进制，
    #        例如：2020-01-02   20:30:00 （年取后面2字节）则将20,01，02,20,30,00 转换为对应的6个字节
    #        theTime:传入一个类似：2020-01-03 13:05:13的一个字符串
    #####################################################
    def getUTCTimeHex(self, theTime):
        # 获取当前时间，时间格式为：2020-01-03 13:05:13
        # now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 将2020-01-03 13:05:13时间格式转换为一个数组
        # timeStr = "2020-01-03 13:05:13"
        timeStr = theTime
        timeArr = []
        timeArr.append(timeStr[2:4])
        timeArr.append(timeStr[5:7])
        timeArr.append(timeStr[8:10])
        timeArr.append(timeStr[11:13])
        timeArr.append(timeStr[14:16])
        timeArr.append(timeStr[17:19])
        UTCTime = ""
        for i in range(0, len(timeArr)):
            UTCTime += self.int2hexString(int(timeArr[i]))
        return UTCTime

    #####################################################
    #16进制转换为UTC时间格式
    #####################################################
    def hex2UTCTime(self,dataHex):
        theTime = "20"
        theTime = theTime + str(int(dataHex[:2],16))
        theTime = theTime + "-" + str(int(dataHex[2:4],16))
        theTime = theTime + "-" + str(int(dataHex[4:6],16))
        theTime = theTime + " " + str(int(dataHex[6:8],16))
        theTime = theTime + ":" + str(int(dataHex[8:10],16))
        theTime = theTime + ":" + str(int(dataHex[10:],16))
        return theTime

    ####################################################
    #       将整数转换为有符号的整数
    #####################################################
    def num2signedNum(self,num):
        return num & 0xff


if __name__ == "__main__":
    # print(ProtocolBase().str2Hex("a"))
    # print(ProtocolBase().int2hexStringByBytes(1,6))
    # print(ProtocolBase().num2signedNum(-5))
    print(ProtocolBase().getUTCTimeHex("2020-01-03 13:05:13"))
    # print(ProtocolBase().hex2UTCTime("1401030d050d"))
    # print(ProtocolBase().hex2UTCTime("14020a07122b"))
    # print(ProtocolBase().crc16("4040007000064d20191201000200120114030503202d26d7fffff0000000000505000000143c00000bb80100000fa00000000a0000000000005e60723b723b39331e100055320000001312001007d0001e0000000000000096000000280096ffff3e0001f40000003e0000000000000000000000"))
    # print(ProtocolBase().myCrc16("4040007000064d20191201000200120114030503202d26d7fffff0000000000505000000143c00000bb80100000fa00000000a0000000000005e60723b723b39331e100055320000001312001007d0001e0000000000000096000000280096ffff3e0001f40000003e0000000000000000000000"))