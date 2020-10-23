#coding:utf-8

'''
定义一个升级应答数据包
'''

from lib.protocol.report.ProtocolBase import ProtocolBase

class Update_response(ProtocolBase):
    def __init__(self,msgCount = 1,WATER_CODE = 1000,DEV_ID = "M121501010001",status="00"):
        super().__init__()
        self.msgCount = int(msgCount)
        self.WATER_CODE = int(WATER_CODE);      # 设置默认消息流水号
        self.DEV_ID = DEV_ID                    # 设置默认设备id
        self.status = status                    #应答状态

    def setStatus(self,data):
        self.status = data

    #####################################################
    #               生成 升级应答 消息
    #####################################################
    def generateUpdateMsg(self):
        self.getProtocalHeader()
        info = ""
        HEADER = "4040"                                                     #消息头
        WATER_CODE = self.getWaterCode(self.WATER_CODE)                     #消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)                          #设备id
        FUN_ID = "0300"                                                     # 功能id
        data = ""                                                           #数据段
        for i in range(0,self.msgCount):
            data += self.generateUpdatePkg(self.generateUpdateData())
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
    #               创建 升级应答 数据包，包含包个数
    #####################################################
    def generateUpdatePkg(self,data):
        return data

    #####################################################
    #               创建 升级应答 数据段
    #####################################################
    def generateUpdateData(self):
        data = ""
        status = self.status
        data = status
        return data

if __name__ == "__main__":
    print(Update_response().generateUpdateMsg())