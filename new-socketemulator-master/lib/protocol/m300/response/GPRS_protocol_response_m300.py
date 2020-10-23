#encoding:utf-8

from lib.protocol.m300.M300Base import M300Base

'''
定义终端版本协议类
'''

class GPRS_protocol_response_m300(M300Base):
    dataTest = [{"serverIndex":"1","serverAddressType":0,"serverAddress":"10.100.12.31","comPort":"9008","comType":0,"APN":"tnet", \
            "username":"yuanhong","password":"123456"},{"serverIndex":"2","serverAddressType":0,"serverAddress":"10.100.12.31","comPort":"9008","comType":0,"APN":"tnet", \
            "username":"yuanhong","password":"123456"},{"serverIndex":"3","serverAddressType":0,"serverAddress":"10.100.12.31","comPort":"9008","comType":0,"APN":"tnet", \
            "username":"yuanhong","password":"123456"}]
    def __init__(self,waterCode = 3,DEV_ID = "M121501010001",encryptionType=0,data=[{"serverIndex":"1","serverAddressType":0,"serverAddress":"10.100.12.31","comPort":"9008","comType":0,"APN":"tnet", \
            "username":"yuanhong","password":"123456"},{"serverIndex":"2","serverAddressType":0,"serverAddress":"10.100.12.32","comPort":"9008","comType":0,"APN":"tnet", \
            "username":"yuanhong","password":"123456"},{"serverIndex":"3","serverAddressType":0,"serverAddress":"10.100.12.33","comPort":"9008","comType":0,"APN":"tnet", \
            "username":"yuanhong","password":"123456"}]):
        super().__init__()                            # 不执行该方法，无法使用父类里面定义的属性
        self.waterCode = waterCode                    #消息流水号
        self.DEV_ID = DEV_ID                          #设备Id
        self.encryptionType = encryptionType          #消息属性里面的是否加密字段
        self.data = data


    #################################################
    # 生成消息
    #################################################
    def generateMsg(self):
        msg = self.IDENTIFY
        FUNID = "0104"                                                  #功能id
        waterCode = self.int2hexStringByBytes(self.waterCode,2)         #消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)                      #设备id
        msgBody = self.getMsgBody()  # 消息体
        msgLen = int(len(msgBody) / 2)
        property = self.getMsgProperty(msgBodyLen=msgLen,encryptionType=self.encryptionType)
        checkCode = self.getCheckCode(FUNID + waterCode + DEV_ID + property + msgBody)
        msg = msg + FUNID + waterCode + DEV_ID + property + msgBody + checkCode + self.IDENTIFY
        return msg

    #################################################
    # 获取消息体
    #################################################
    def getMsgBody(self):
        dataHex = ""
        lenHex = self.int2hexStringByBytes(len(self.data))
        dataHex = dataHex + lenHex
        for i in range(0,len(self.data)):
            dataHex = dataHex + self.str2Hex(self.data[i]["serverIndex"])                        #服务器索引号，从1开始
            dataHex = dataHex + "2c"                                                          #逗号
            dataHex = dataHex + self.str2Hex(str(self.data[i]["serverAddressType"]))             #服务器地址类型：0-IP地址，1-域名
            dataHex = dataHex + "2c"                                                          #逗号
            dataHex = dataHex + self.str2Hex(self.data[i]["serverAddress"])                      #服务器地址
            dataHex = dataHex + "2c"                                                          #逗号
            dataHex = dataHex + self.str2Hex(self.data[i]["comPort"])                            #TCP/UDP端口
            dataHex = dataHex + "2c"                                                          #逗号
            dataHex = dataHex + self.str2Hex(str(self.data[i]["comType"]))                       #通讯模式：0-TCP，1-UDP
            dataHex = dataHex + "2c"                                                          #逗号
            dataHex = dataHex + self.str2Hex(self.data[i]["APN"])                                #APN名称
            dataHex = dataHex + "2c"                                                          #逗号
            dataHex = dataHex + self.str2Hex(self.data[i]["username"])                           #用户名
            dataHex = dataHex + "2c"                                                          #逗号
            dataHex = dataHex + self.str2Hex(self.data[i]["password"])                           #密码
            dataHex = dataHex + "0d"                                                          #分隔符:0x0D
            dataHex = dataHex + "0a"                                                          #分隔符:0x0A
        return dataHex

if __name__ == "__main__":
    print(GPRS_protocol_response_m300().generateMsg())