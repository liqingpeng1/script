#coding:utf-8
from lib.protocol.report.ProtocolBase import ProtocolBase

'''
终端上报故障码数据包
'''

class TroubleReport_protocol(ProtocolBase):

    def __init__(self,WATER_CODE = 26,DEV_ID = "M121501010001",infoTime="2020-01-20 11:55:58",troubleCount=1,byte0="02",byte1=2,byte2=3,byte3=0,MILStatus=1):
        super().__init__()
        self.WATER_CODE = int(WATER_CODE);  # 设置默认消息流水号
        self.DEV_ID = DEV_ID  # 设置默认设备id

        self.infoTime = infoTime                                #时间信息
        self.troubleCount = int(troubleCount)                        #故障码个数
        self.byte0 = byte0                                      #系统id
        self.byte1 = int(byte1)                                      #故障码内容
        self.byte2 = int(byte2)                                      #故障码内容
        self.byte3 = int(byte3)                                      #故障码状态
        self.MILStatus = int(MILStatus)                              #MIL状态

    #####################################################
    #               生成故障码消息
    #####################################################
    def generateTroubleMsg(self):
        self.getProtocalHeader()
        info = ""
        HEADER = "4040"                                         # 消息头
        WATER_CODE = self.getWaterCode(self.WATER_CODE)         # 消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)              # 设备id
        FUN_ID = "001A"                                         # 功能id(GPS功能id)
        data = self.generateTroubleData(self.troubleCount)      # 数据段
        # 消息长度
        LENGTH = self.getMsgLength(int(len(WATER_CODE + DEV_ID + FUN_ID + data) / 2))
        info += HEADER
        info += LENGTH
        info += WATER_CODE
        info += DEV_ID
        info += FUN_ID
        info += data
        CHECK_CODE = self.getCheckCode(info)
        info += CHECK_CODE                          # 校验字段
        return info

    #####################################################
    #               创建故障码数据段
    #####################################################
    def generateTroubleData(self,troubleCount):
        data = ""
        infoTime = self.getUTCTimeHex(self.infoTime)                 #时间信息
        data += infoTime
        data += self.int2hexString(troubleCount)
        for i in range(0,troubleCount):
            data = data + self.generateTroubleCode()
        data = data + self.int2hexString(self.MILStatus)
        return data

    #####################################################
    #               生成一个故障码数据
    #####################################################
    def generateTroubleCode(self):
        byte0 = self.byte0                                          #系统ID
        byte1 = self.getByte1Hex(self.byte1)                        #故障码内容
        byte2 = self.getByte2Hex(self.byte2)                        #故障码内容
        byte3 = self.getByte3Hex(self.byte3)                        #故障码状态

        data = byte0 + byte1 +byte2 + byte3
        return data

    #####################################################
    #               获取系统ID的16进制数据
    #               0x00: 发动机故障码
    #               0x01: 变速箱故障码
    #               0x02: ABS故障码
    #               0x03: 安全气囊故障码
    #                其它预留
    #####################################################
    def getByte0Hex(self, data):
        return "02"

    #####################################################
    #               获取故障码内容的16进制数据
    #####################################################
    def getByte1Hex(self,data):
        hexData = self.int2hexString(data)
        return hexData

    #####################################################
    #               获取故障码内容的16进制数据
    #####################################################
    def getByte2Hex(self, data):
        hexData = self.int2hexString(data)
        return hexData


    #####################################################
    #               获取故障码状态的16进制数据
    #####################################################
    def getByte3Hex(self, data):
        hexData = self.int2hexString(data)
        return hexData
