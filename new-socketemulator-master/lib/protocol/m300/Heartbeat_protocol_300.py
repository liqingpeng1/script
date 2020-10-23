#encoding:utf-8

from lib.protocol.m300.M300Base import M300Base

'''
定义心跳议类
'''

class Heartbeat_protocol_300(M300Base):
    def __init__(self,waterCode = 3,DEV_ID = "M121501010001",encryptionType=0):
        super().__init__()                            # 不执行该方法，无法使用父类里面定义的属性
        self.waterCode = waterCode                    #消息流水号
        self.DEV_ID = DEV_ID                          #设备Id
        self.encryptionType = encryptionType          #消息属性里面的是否加密字段

    #################################################
    # 生成消息
    #################################################
    def generateMsg(self):
        msg = self.IDENTIFY
        FUNID = "0004"                                                   #功能id
        waterCode = self.int2hexStringByBytes(self.waterCode,2)          #消息流水号
        DEV_ID = self.devid2hexString(self.DEV_ID)                       #设备id
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
        data = ""
        return data

if __name__ == "__main__":
    print(Heartbeat_protocol_300().generateMsg())

