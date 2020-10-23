#coding:utf-8

'''
定义一个终端版本协议的类
'''

from lib.protocol.report.ProtocolBase import ProtocolBase

class VersionReport_protocol(ProtocolBase):
    def __init__(self,msgCount = 1,WATER_CODE = 1000,DEV_ID = "M121501010001",verInfo="M100AB01010.0000",compileDate="2020-03-23",GSM="GSM_123456"):
        super().__init__()
        self.msgCount = int(msgCount)           # 设置默认要发送的GPS数据包个数

        self.WATER_CODE = int(WATER_CODE);      # 设置默认消息流水号
        self.DEV_ID = DEV_ID                    # 设置默认设备id

        self.verInfo = verInfo                  # 设置默认UTC时间度戳
        self.compileDate = compileDate          #编译日期
        self.GSM = GSM                          #GSM模块型号

    #####################################################
    #               生成 版本上报 消息
    #####################################################
    def generateVersionMsg(self):
        self.getProtocalHeader()
        info = ""
        HEADER = "4040"                                                     #消息头
        WATER_CODE = self.getWaterCode(self.WATER_CODE)                     #消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)                          #设备id
        FUN_ID = "0005"                                                     # 功能id
        data = ""                                                           #数据段
        for i in range(0,self.msgCount):
            data += self.generateVersionPkg(self.generateVersionData())
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
    def generateVersionPkg(self,data):
        return data

    #####################################################
    #               创建 版本信息 数据段
    #####################################################
    def generateVersionData(self):
        data = ""
        verInfoHex = self.str2Hex(self.verInfo)                       # 设置默认UTC时间度戳
        compileDateHex = self.str2Hex(self.compileDate)               #编译日期
        GSMHex = self.str2Hex(self.GSM)                               #GSM模块型号
        data = verInfoHex + compileDateHex + GSMHex
        return data

if __name__ == "__main__":
    print(VersionReport_protocol().generateVersionMsg())