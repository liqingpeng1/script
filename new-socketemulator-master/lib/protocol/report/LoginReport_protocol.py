#coding:utf-8

'''
定义一个终端登录协议的类
'''

from lib.protocol.report.ProtocolBase import ProtocolBase

class LoginReport_protocol(ProtocolBase):
    def __init__(self,WATER_CODE = "0002",DEV_ID = "M121501010001",cpuId="CPU-ID001122334455667788",imsi="IMSI13145678902",ccid="CCID1122334455667788",imei="IMEI12233445566"):
        super().__init__()
        self.WATER_CODE = int(WATER_CODE);  # 设置默认消息流水号
        self.DEV_ID = DEV_ID  # 设置默认设备id

        self.cpuId = cpuId       #设置默认cupId值
        self.imsi = imsi         #设置默认imsi值
        self.ccid = ccid         #设置默认ccid值
        self.imei = imei         #设置默认imei值

    #####################################################
    #               生成终端登录消息
    #####################################################
    def generateLoginMsg(self):
        self.getProtocalHeader()
        info = ""
        HEADER = "4040"      # 消息头
        WATER_CODE = self.getWaterCode(self.WATER_CODE)   # 消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)   # 设备id
        FUN_ID = "0002"         # 功能id(终端登录功能id)

        data = self.generateLoginData()          # 数据段

        LENGTH = self.getMsgLength(int(len(WATER_CODE + DEV_ID + FUN_ID + data) / 2))   # 消息长度

        info += HEADER
        info += LENGTH
        info += WATER_CODE
        info += DEV_ID
        info += FUN_ID
        info += data
        CHECK_CODE = self.getCheckCode(info)    # 校验字段
        info += CHECK_CODE
        return info

    #####################################################
    #               创建终端登录数据段
    #####################################################
    def generateLoginData(self):
        data = ""
        CPU_ID = self.getCPU_IDHex(self.cpuId)        #CPU-ID
        IMSI = self.getIMSIHex(self.imsi)             #IMSI
        CCID = self.getCCIDHex(self.ccid)             #CCID
        IMEI = self.getIMEIHex(self.imei)             #IMEI

        data = data + CPU_ID + IMSI +CCID +IMEI
        return data

    #####################################################
    #               获取CPU_ID对应的16进制数据
    #####################################################
    def getCPU_IDHex(self,data):
        return self.str2Hex(data)

    #####################################################
    #               获取IMSI对应的16进制数据
    #####################################################
    def getIMSIHex(self,data):
        return self.str2Hex(data)

    #####################################################
    #               获取CCID对应的16进制数据
    #####################################################
    def getCCIDHex(self,data):
        return self.str2Hex(data)

    #####################################################
    #               获取IMDE对应的16进制数据
    #####################################################
    def getIMEIHex(self,data):
        return self.str2Hex(data)


if __name__ == "__main__":
    print(LoginReport_protocol().generateLoginData())