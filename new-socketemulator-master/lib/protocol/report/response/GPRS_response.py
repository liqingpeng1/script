#coding:utf-8

'''
定义一个查询GPRS应答数据包
'''

from lib.protocol.report.ProtocolBase import ProtocolBase

class GPRS_response(ProtocolBase):
    dataDefault = [{"serverIndex":"1","serverAddressType":0,"serverAddress":"10.100.12.31","comPort":"9008","comType":0,"APN":"tnet", \
            "username":"yuanhong","password":"123456"},{"serverIndex":"1","serverAddressType":0,"serverAddress":"10.100.12.32","comPort":"9008","comType":0,"APN":"tnet", \
            "username":"yuanhong","password":"123456"},{"serverIndex":"1","serverAddressType":0,"serverAddress":"10.100.12.33","comPort":"9008","comType":0,"APN":"tnet", \
            "username":"yuanhong","password":"123456"}]
    def __init__(self,msgCount = 1,WATER_CODE = 1000,DEV_ID = "M121501010001",data=[{"serverIndex":"1","serverAddressType":0,"serverAddress":"10.100.12.31","comPort":"9008","comType":0,"APN":"tnet", \
            "username":"yuanhong","password":"123456"},{"serverIndex":"2","serverAddressType":0,"serverAddress":"10.100.12.32","comPort":"9008","comType":0,"APN":"tnet", \
            "username":"yuanhong","password":"123456"},{"serverIndex":"3","serverAddressType":0,"serverAddress":"10.100.12.33","comPort":"9008","comType":0,"APN":"tnet", \
            "username":"yuanhong","password":"123456"}]):
        super().__init__()
        self.msgCount = int(msgCount)
        self.WATER_CODE = int(WATER_CODE);      # 设置默认消息流水号
        self.DEV_ID = DEV_ID                    # 设置默认设备id
        self.data = data

    #####################################################
    #               生成 GPRS应答 消息
    #####################################################
    def generateMsg(self):
        self.getProtocalHeader()
        info = ""
        HEADER = "4040"                                                     #消息头
        WATER_CODE = self.getWaterCode(self.WATER_CODE)                     #消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)                          #设备id
        FUN_ID = "0105"                                                     # 功能id
        data = ""                                                           #数据段
        data += self.generateUpdateData()
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
    #               创建 GPRS应答 数据段
    #####################################################
    def generateUpdateData(self):
        dataHex = ""
        for i in range(0,len(self.data)):
            dataHex = dataHex + self.str2Hex(self.data[i]["serverIndex"])                        #服务器索引号，从1开始
            dataHex = dataHex + "2c"                                                             #逗号
            dataHex = dataHex + self.str2Hex(str(self.data[i]["serverAddressType"]))             #服务器地址类型：0-IP地址，1-域名
            dataHex = dataHex + "2c"                                                             #逗号
            dataHex = dataHex + self.str2Hex(self.data[i]["serverAddress"])                      #服务器地址
            dataHex = dataHex + "2c"                                                             #逗号
            dataHex = dataHex + self.str2Hex(self.data[i]["comPort"])                            #TCP/UDP端口
            dataHex = dataHex + "2c"                                                             #逗号
            dataHex = dataHex + self.str2Hex(str(self.data[i]["comType"]))                       #通讯模式：0-TCP，1-UDP
            dataHex = dataHex + "2c"                                                             #逗号
            dataHex = dataHex + self.str2Hex(self.data[i]["APN"])                                #APN名称
            dataHex = dataHex + "2c"                                                             #逗号
            dataHex = dataHex + self.str2Hex(self.data[i]["username"])                           #用户名
            dataHex = dataHex + "2c"                                                             #逗号
            dataHex = dataHex + self.str2Hex(self.data[i]["password"])                           #密码
            dataHex = dataHex + "0d"                                                             #分隔符:0x0D
            dataHex = dataHex + "0a"                                                             #分隔符:0x0A
        return dataHex

if __name__ == "__main__":
    print(GPRS_response().generateMsg())


