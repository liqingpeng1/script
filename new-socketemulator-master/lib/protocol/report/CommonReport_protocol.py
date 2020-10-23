#coding:utf-8

'''
定义一个通用应答数据包
'''

from lib.protocol.report.ProtocolBase import ProtocolBase

class CommonReport_protocol(ProtocolBase):
    def __init__(self,msgCount = 1,WATER_CODE = 1000,DEV_ID = "M121501010001",resId="8205",status="00"):
        super().__init__()
        self.msgCount = int(msgCount)
        self.WATER_CODE = int(WATER_CODE);      # 设置默认消息流水号
        self.DEV_ID = DEV_ID                    # 设置默认设备id
        self.resId = resId                      #应答的功能ID
        self.status = status                    #应答状态

    def setResId(self,data):
        self.resId = data
    def setStatus(self,data):
        self.status = data

    #####################################################
    #               生成 通用应答 消息
    #####################################################
    def generateCommonMsg(self):
        self.getProtocalHeader()
        info = ""
        HEADER = "4040"                                                     #消息头
        WATER_CODE = self.getWaterCode(self.WATER_CODE)                     #消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)                          #设备id
        FUN_ID = "0000"                                                     # 功能id
        data = ""                                                           #数据段
        for i in range(0,self.msgCount):
            data += self.generateCommonPkg(self.generateCommonData())
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
    def generateCommonPkg(self,data):
        return data

    #####################################################
    #               创建 版本信息 数据段
    #####################################################
    def generateCommonData(self):
        data = ""
        resId = self.resId
        status = self.status
        data = resId + status
        return data

if __name__ == "__main__":
    print(CommonReport_protocol().generateCommonMsg())