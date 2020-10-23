#coding:utf-8

'''
定义一个终端休眠协议的类
'''

from lib.protocol.report.ProtocolBase import ProtocolBase

class SleepReport_protocol(ProtocolBase):
    def __init__(self,msgCount = 1,WATER_CODE = 1000,DEV_ID = "M121501010001",sleepType="01",sleepStatus=0):
        super().__init__()
        self.msgCount = int(msgCount)           # 设置默认要发送的GPS数据包个数

        self.WATER_CODE = int(WATER_CODE);      # 设置默认消息流水号
        self.DEV_ID = DEV_ID                    # 设置默认设备id
        
        self.sleepType = sleepType              #休眠类型
        self.sleepStatus = sleepStatus          #休眠状态

    #####################################################
    #               生成 版本上报 消息
    #####################################################
    def generateSleepMsg(self):
        self.getProtocalHeader()
        info = ""
        HEADER = "4040"                                                     #消息头
        WATER_CODE = self.getWaterCode(self.WATER_CODE)                     #消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)                          #设备id
        FUN_ID = "00FF"                                                     # 功能id
        data = ""                                                           #数据段
        for i in range(0,self.msgCount):
            data += self.generateSleepPkg(self.generateSleepData())
        LENGTH = self.getMsgLength(int(len(WATER_CODE + DEV_ID + FUN_ID + data)/2))      # 消息长度
        info += HEADER
        info += LENGTH
        info += WATER_CODE
        info += DEV_ID
        info += FUN_ID
        info += data
        CHECK_CODE = self.getCheckCode(info)                                # 校验字段
        info += CHECK_CODE
        return info

    #####################################################
    #               创建 版本信息 数据包，包含包个数
    #####################################################
    def generateSleepPkg(self,data):
        return data

    #####################################################
    #               创建 车机休眠数据段 数据段
    #####################################################
    def generateSleepData(self):
        sleepTypeHex = self.sleepType
        sleepStatusHex = self.int2hexString(self.sleepStatus)
        data = sleepTypeHex + sleepStatusHex
        return data

if __name__ == "__main__":
    print(SleepReport_protocol().generateSleepMsg())