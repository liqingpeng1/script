#encoding:utf-8

'''
定义终端心跳消息
'''
from lib.protocol.message.MessageBase import MessageBase


class TerminalHeartbeat_msg(MessageBase):
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

    # 生成一条完整的消息，针对图形界面，可传递参数
    def generateMsg_GUI(self,msgID="0002",phoneNum="13146201119",msgWaterCode=1,encryptionType=0,subPkg=0):
        msg = ""
        msgBody = self.getMsgBody()
        msgHeader = self.getMsgHeader_GUI(msgID, phoneNum, msgWaterCode, encryptionType, subPkg,msgBody)
        checkCode = self.getCheckCode(msgHeader + msgBody)
        msg = msg + self.IDENTIFY
        info = msgHeader + msgBody + checkCode
        info = self.replace7e7d(info)
        msg = msg + info
        msg = msg + self.IDENTIFY
        return msg

    # 生成一条完整的消息，数据随机产生
    def generateMsg_random(self):
        msgID="0002"
        phoneNum=self.getRandomStr(11,"0123456789")
        msgWaterCode=self.getRandomNum(1,65535)
        encryptionType=0
        subPkg=self.getRandomNum(intArr=[0,8192],mult=1)
        msg = ""
        msgHeader = self.getMsgHeader_GUI(msgID, phoneNum, msgWaterCode, encryptionType, subPkg)
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
        return msg

    #######################################################
    # 获取消息头
    #######################################################
    def getMsgHeader(self):
        # msgID = self.int2hexStringByBytes(102,2)                                                           #消息id
        msgID = "0002"
        subPkg = 0
        msgBodyProperty = self.getMsgBodyProperty(msgBodyLen=int(len(self.getMsgBody()) / 2),subPkg=subPkg)  #消息体属性
        phoneNum = self.int2BCD(13146201118)                                                                 #终端手机号
        msgWaterCode = self.int2hexStringByBytes(6,2)                                                        #消息流水号
        if subPkg != 8192:
            subPkgContent = ""                                                                               #消息包封装项
        else:
            subPkgContent = self.getMsgPackage()
        data = msgID + msgBodyProperty + phoneNum + msgWaterCode + subPkgContent
        return data

    #获取消息体属性
    def getMsgBodyProperty(self,msgBodyLen=128,encryptionType=0,subPkg=0):
        if msgBodyLen >= 512:
            raise RuntimeError('消息体长度超长！')
        msgBodyLen = msgBodyLen                                  #消息体长度
        encryptionType = encryptionType << 10                    #加密方式
        subPkg = subPkg  << 13                                   #分包
        retain = 0                                               #保留位
        data = msgBodyLen + encryptionType + subPkg + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex

    #获取消息体属性，针对图形界面，可传递参数
    def getMsgBodyProperty_GUI(self,msgBodyLen=128,encryptionType=0,subPkg=0):
        if msgBodyLen >= 512:
            raise RuntimeError('消息体长度超长！')
        msgBodyLen = msgBodyLen                                  #消息体长度
        encryptionType = encryptionType                          #加密方式
        subPkg = subPkg                                          #分包
        retain = 0                                               #保留位
        data = msgBodyLen + encryptionType + subPkg + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex


if __name__ == "__main__":
    print(TerminalHeartbeat_msg().generateMsg())
    print(TerminalHeartbeat_msg().getMsgBodyProperty())