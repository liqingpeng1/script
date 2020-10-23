#encoding:utf-8

'''
定义终端升级结果通知
'''
from lib.protocol.message.MessageBase import MessageBase


class TerminalUpdataResult_msg(MessageBase):
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
        #升级类型
        #00：终端
        # 12：道路运输证 IC 卡读卡器
        # 52：北斗
        updateType = "00"
        #升级结果
        #0x00：成功
        # 0x01：失败（升级超时，放弃当前升级）
        # 0x02：取消
        # 0xF0：升级相同版本，不升级（扩展）
        # 0xF1：升级版本属性错误（扩展）
        # 0xF2：升级文件校验错误（扩展）
        # 0xF3：升级文件不存在（扩展）
        updataResult = "00"
        msg = updateType + updataResult
        return msg

    #######################################################
    # 获取消息头
    #######################################################
    def getMsgHeader(self):
        # msgID = self.int2hexStringByBytes(102,2)                                                           #消息id
        msgID = "0108"
        subPkg = 0
        msgBodyProperty = self.getMsgBodyProperty(msgBodyLen=int(len(self.getMsgBody()) / 2),subPkg=subPkg)  #消息体属性
        phoneNum = self.int2BCD(13146201119)                                                                 #终端手机号
        msgWaterCode = self.int2hexStringByBytes(1,2)                                                        #消息流水号
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
        encryptionType = encryptionType                          #加密方式
        subPkg = subPkg                                          #分包
        retain = 0                                               #保留位
        data = msgBodyLen + encryptionType + subPkg + retain
        dataHex = self.int2hexStringByBytes(data,2)
        return dataHex


if __name__ == "__main__":
    print(TerminalUpdataResult_msg().generateMsg())