#encoding:utf-8

'''
定义终端通用应答
'''
from lib.protocol.message.MessageBase import MessageBase


class TerminalCommonMsgRes_msg(MessageBase):
    def __init__(self,resId="0002",phoneNum=13146201119,resWaterCode="0001",sn=1):
        super().__init__()          #不执行该方法，无法使用父类里面定义的属性
        self.resId = resId
        self.phoneNum = phoneNum
        self.resWaterCode = resWaterCode
        self.sn = sn
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
        resWaterCode = self.resWaterCode           #对应的平台消息的流水号
        msgId = self.resId                         #消息id，对应的平台消息的 ID
        reslult = self.int2hexStringByBytes(0)     #0：成功/确认；1：失败；2：消息有误；3：不支持
        data = ""
        msg = data + resWaterCode + msgId + reslult
        return msg

    #######################################################
    # 获取消息头
    #######################################################
    def getMsgHeader(self):
        # msgID = self.int2hexStringByBytes(102,2)                 #消息id
        msgID = "0001"                                             #消息id
        msgBodyProperty = self.getMsgBodyProperty(int(len(self.getMsgBody()) / 2))              #消息体属性
        phoneNum = self.int2BCD(int(self.phoneNum))                           #终端手机号
        msgWaterCode = self.int2hexStringByBytes(self.sn,2)                         #消息流水号
        subPkgContent = ""                                       #消息包封装项
        data = msgID + msgBodyProperty + phoneNum + msgWaterCode + subPkgContent
        return data


if __name__ == "__main__":
    print(TerminalCommonMsgRes_msg().generateMsg())