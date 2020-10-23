#encoding:utf-8

'''
定义查询终端属性应答消息
'''
from lib.protocol.message.MessageBase import MessageBase


class QueryTerminalProperty_res(MessageBase):
    def __init__(self):
        super().__init__()          #不执行该方法，无法使用父类里面定义的属性
        pass

    #######################################################
    # 生成一条完整的消息
    #######################################################
    def generateMsg(self):
        msg = ""
        msgHeader = self.getMsgHeader()
        msgBody = self.getMsgBody()
        checkCode = self.getCheckCode(msgHeader + msgBody)
        msg = msg + self.IDENTIFY
        info = msgHeader + msgBody + checkCode
        info = self.replace7e7d(info)
        msg = msg + info
        msg = msg + self.IDENTIFY
        return msg

    #######################################################
    # 获取消息体
    #######################################################
    def getMsgBody(self):
        msg = ""
        # 终端类型
        terminalType = self.getTerminalType()
        # 制造商 ID,5 个字节，终端制造商编码
        manufacturerId = self.str2Hex("id123")
        #终端型号,20 个字节，此终端型号由制造商自行定义，位数不足时 后补“0X00”。
        terminalMode = self.str2Hex("mode_123456789012345")
        #终端 ID,7 个字节，由大写字母和数字组成，此终端 ID 由制造商 自行定义，位数不足时，后补“0X00”。
        terminalId = self.str2Hex("id121345")
        #终端 SIM 卡 ICCID
        ICCID = self.int2BCD(6238964579643234,10)
        #终端硬件版本号长度
        hardwareVersionNumLen = self.int2hexStringByBytes(10)
        #终端硬件版本号
        hardwareVersion = self.GBKString2Hex("version1.2")
        #终端固件版本号长度
        firmwareVersionLen = self.int2hexStringByBytes(11)
        #终端固件版本号
        firmwareVersion = self.GBKString2Hex("firmware1.2")
        #GNSS 模块属性
        GNSSProperty = self.getGNSSProperty()
        #通信模块属性
        communicationProperty = self.getCommunicationProperty()

        data = terminalType + manufacturerId + terminalMode + terminalId + ICCID
        data = data + hardwareVersionNumLen + hardwareVersion + firmwareVersionLen + firmwareVersion + GNSSProperty
        data = data + communicationProperty
        msg = data
        return msg

    #######################################################
    # 获取消息头
    #######################################################
    def getMsgHeader(self):
        # msgID = self.int2hexStringByBytes(102,2)                                                           #消息id
        msgID = "0107"
        subPkg = 0
        msgBodyProperty = self.getMsgBodyProperty(msgBodyLen=int(len(self.getMsgBody()) / 2),subPkg=subPkg)  #消息体属性
        phoneNum = self.int2BCD(13146201119)                                                                 #终端手机号
        msgWaterCode = self.int2hexStringByBytes(1,2)                                                        #消息流水号
        if subPkg != 8192:
            subPkgContent = ""                                                                               #消息包封装项
        else:
            subPkgContent = self.getMsgPackage()
        data = msgID + msgBodyProperty + phoneNum + msgWaterCode + subPkgContent
        return data

    #获取消息体属性
    def getMsgBodyProperty(self,msgBodyLen=128,encryptionType=0,subPkg=0):
        if msgBodyLen >= 512:
            raise RuntimeError('消息体长度超长！')
        msgBodyLen = msgBodyLen                                  #消息体长度
        encryptionType = encryptionType                          #加密方式
        subPkg = subPkg                                          #分包
        retain = 0                                               #保留位
        data = msgBodyLen + encryptionType + subPkg + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex

    #######################################################
    # 获取终端类型
    #######################################################
    def getTerminalType(self):
        #bit0，0：不适用客运车辆，1：适用客运车辆；  (1)
        # bit1，0：不适用危险品车辆，1：适用危险品车辆；  (2)
        # bit2，0：不适用普通货运车辆，1：适用普通货运车辆   (4)
        # bit3，0：不适用出租车辆，1：适用出租车辆；    (8)
        # bit6，0：不支持硬盘录像，1：支持硬盘录像；   (64)
        # bit7，0：一体机，1：分体机。          (128)
        bit0 = 1
        bit1 = 2
        bit2 = 4
        bit3 = 8
        bit6 = 64
        bit7 = 128
        data = bit0 + bit1 + bit2 + bit3 + bit6 + bit7
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex

    #######################################################
    # 获取GNSS 模块属性
    #######################################################
    def getGNSSProperty(self):
        #bit0，0：不支持 GPS 定位， 1：支持	GPS 定位；     (1)
        # bit1，0：不支持北斗定位， 1：支持北斗定位；      (2)
        # bit2，0：不支持 GLONASS 定位， 1：支持 GLONASS 定位    (4)
        # bit3，0：不支持 Galileo 定位， 1：支持 Galileo 定位    (8)
        bit0 = 1
        bit1 = 2
        bit2 = 4
        bit3 = 8
        data = bit0 +bit1 +bit2 + bit3
        dataHex = self.int2hexStringByBytes(data)
        return dataHex

    #######################################################
    # 获取通信模块属性
    #######################################################
    def getCommunicationProperty(self):
        #bit0，0：不支持 GPRS 通信， 1：支持 GPRS 通信；   (1)
        # bit1，0：不支持 CDMA 通信， 1：支持 CDMA 通信；    (2)
        # bit2，0：不支持 TD-SCDMA 通信， 1：支持 TD-SCDMA 通信   (4)
        # bit3，0：不支持 WCDMA 通信， 1：支持 WCDMA 通信；      (8)
        # bit4，0：不支持 CDMA2000 通信， 1：支持 CDMA2000 通信    (16)
        # bit5，0：不支持 TD-LTE 通信， 1：支持 TD-LTE 通信；     (32)
        # bit7，0：不支持其他通信方式， 1：支持其他通信方式     (128)
        bit0 = 1
        bit1 = 2
        bit2 = 4
        bit3 = 8
        bit4 = 16
        bit5 = 32
        bit7 = 128
        data = bit0 + bit1 + bit2 + bit3 + bit4 + bit5 +bit7
        dataHex = self.int2hexStringByBytes(data)
        return dataHex



if __name__ == "__main__":
    print(QueryTerminalProperty_res().generateMsg())