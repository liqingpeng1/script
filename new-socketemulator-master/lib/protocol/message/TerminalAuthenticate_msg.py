#encoding:utf-8

'''
定义终端鉴权消息
'''
from lib.protocol.message.MessageBase import MessageBase


class TerminalAuthenticate_msg(MessageBase):
    def __init__(self):
        super().__init__()          #不执行该方法，无法使用父类里面定义的属性
        pass

    #######################################################
    # 生成一条完整的消息
    #######################################################
    def generateMsg(self):
        msg = ""
        msgHeader = self.getMsgHeader()
        msgBody = self.getMsgBody()
        checkCode = self.getCheckCode(msgHeader + msgBody)
        msg = msg + self.IDENTIFY
        info = msgHeader + msgBody + checkCode
        info = self.replace7e7d(info)
        msg = msg + info
        msg = msg + self.IDENTIFY
        return msg

    #######################################################
    # 获取消息体
    #######################################################
    def getMsgBody(self):
        msg = ""
        #鉴权码
        authenticateCode = str("asuyx7".encode("gbk"))
        authenticateCode = authenticateCode[2:len(authenticateCode) - 1]
        authenticateCode = self.str2Hex(authenticateCode)
        msg = authenticateCode
        return msg

    #######################################################
    # 获取消息头
    #######################################################
    def getMsgHeader(self):
        # msgID = self.int2hexStringByBytes(102,2)                 #消息id
        msgID = "0102"
        msgBodyProperty = self.getMsgBodyProperty(int(len(self.getMsgBody()) / 2))              #消息体属性
        phoneNum = self.int2BCD(13146201119)                     #终端手机号
        msgWaterCode = self.int2hexStringByBytes(1,2)                           #消息流水号
        subPkgContent = ""                                       #消息包封装项
        data = msgID + msgBodyProperty + phoneNum + msgWaterCode + subPkgContent
        return data

    #获取消息体属性
    def getMsgBodyProperty(self,msgBodyLen=128,encryptionType=0,subPkg=0):
        if msgBodyLen >= 512:
            raise RuntimeError('消息体长度超长！')
        msgBodyLen = msgBodyLen                                  #消息体长度
        encryptionType = encryptionType                          #加密方式
        subPkg = subPkg                                          #分包
        retain = 0                                               #保留位
        data = msgBodyLen + encryptionType + subPkg + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex