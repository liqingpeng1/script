#coding:utf-8

'''
定义一个上报电瓶采样协议的类
'''

from lib.protocol.report.ProtocolBase import ProtocolBase

class VoltageDataReport_protocol(ProtocolBase):
    def __init__(self,WATER_CODE = "0002",DEV_ID = "M121501010001",sampleNums=1,sampleData=[{"sampleTime":"2020-04-09 16:20:22","voltage":12}]):
        super().__init__()
        self.WATER_CODE = int(WATER_CODE);                            # 设置默认消息流水号
        self.DEV_ID = DEV_ID                                          # 设置默认设备id

        self.sampleNums = sampleNums                                  #采样个数
        self.sampleData = sampleData                                  #采样数据

    #####################################################
    #               生成终端登录消息
    #####################################################
    def generateMsg(self):
        self.getProtocalHeader()
        info = ""
        HEADER = "4040"                                                        # 消息头
        WATER_CODE = self.getWaterCode(self.WATER_CODE)                        # 消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)                             # 设备id
        FUN_ID = "000A"                                                        # 功能id(终端登录功能id)

        data = self.generateData()                                             # 数据段

        LENGTH = self.getMsgLength(int(len(WATER_CODE + DEV_ID + FUN_ID + data) / 2))   # 消息长度
        info += HEADER
        info += LENGTH
        info += WATER_CODE
        info += DEV_ID
        info += FUN_ID
        info += data
        CHECK_CODE = self.getCheckCode(info)                                   # 校验字段
        info += CHECK_CODE
        return info

    #####################################################
    #               创建终端登录数据段
    #####################################################
    def generateData(self):
        data = ""
        sampleNums = self.int2hexStringByBytes(self.sampleNums)
        data = data + sampleNums
        for i in range(0,self.sampleNums):
            sampleData = self.getUTCTimeHex(self.sampleData[i]["sampleTime"]) + self.int2hexStringByBytes(int(self.sampleData[i]["voltage"]),2)
            data = data + sampleData
        return data

if __name__ == "__main__":
    print(VoltageDataReport_protocol().generateMsg())