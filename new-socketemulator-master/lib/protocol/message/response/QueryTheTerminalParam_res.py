#encoding:utf-8

'''
定义查询指定终端参数应答消息
'''
from lib.protocol.message.MessageBase import MessageBase
from lib.protocol.messagePlateform.ResponseBase import ResponseBase


class QueryTheTerminalParam_res(MessageBase,ResponseBase):
    def __init__(self):
        super().__init__()                     #不执行该方法，无法使用父类里面定义的属性
        self.msgRes = ""                       #需要回复的消息的16进制报文
        pass

    #######################################################
    # 设置需要回复的消息
    #######################################################
    def setMsgRes(self,data):
        self.msgRes = data

    #######################################################
    # 获取需要回复消息的消息体
    #######################################################
    def getMsgResBody(self):
        data = self.msgRes[28:][:-4]
        data = self.restore_7e7d(data)
        return data

    #######################################################
    # 获取需要回复消息的消息流水号
    #######################################################
    def getQueryWaterCode(self):
        wc = self.msgRes[22:26]
        return wc

    #######################################################
    # 获取需要回复消息的消息手机号
    #######################################################
    def getQueryPhoneNum(self):
        phoneNum = self.msgRes[10:22]
        return phoneNum

    #######################################################
    # 将消息体转换为需要查询的终端参数
    #######################################################
    def getQueryParams(self):
        body = self.getMsgResBody()
        params = []
        param = body[0:8]
        body = body[8:]
        while param != "":
            params.append(param)
            param = body[0:8]
            body = body[8:]
        return params

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
        resWaterCode = self.getQueryWaterCode()                                           #应答流水号,对应的终端参数查询消息的流水号
        resParamCounts = self.int2hexStringByBytes(len(self.getQueryParams()))            #应答参数个数
        paramList = self.getParamList()                                                   #参数项列表
        msg = resWaterCode + resParamCounts + paramList
        return msg

    #######################################################
    # 获取消息头
    #######################################################
    def getMsgHeader(self):
        msgID = "0104"
        subPkg = 0
        msgBodyProperty = self.getMsgBodyProperty(msgBodyLen=int(len(self.getMsgBody()) / 2),subPkg=subPkg)    #消息体属性
        phoneNum = self.int2BCD(self.getQueryPhoneNum())                                                       #终端手机号
        msgWaterCode = self.int2hexStringByBytes(1,2)                                                          #消息流水号
        if subPkg != 8192:
            subPkgContent = ""                                                                                 #消息包封装项
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

    #######################################################
    # 获取参数项列表
    #######################################################
    def getParamList(self):
        queryParams = self.getQueryParams()
        paramNums = 0                                                                         #参数总数
        data = ""
        if "00000010" in queryParams:
            content = self.str2Hex("tnet")
            data = data + "00000010" + self.int2hexStringByBytes(int(len(content) / 2)) + content
            paramNums = paramNums + 1
        if "00000011" in queryParams:
            content = self.str2Hex("yuanhong")
            data = data + "00000011" + self.int2hexStringByBytes(int(len(content) / 2)) + content
            paramNums = paramNums + 1
        if "00000012" in queryParams:
            content = self.str2Hex("123456")
            data = data + "00000012" + self.int2hexStringByBytes(int(len(content) / 2)) + content
            paramNums = paramNums + 1
        if "00000013" in queryParams:
            content = self.str2Hex("10.100.12.30")
            data = data + "00000013" + self.int2hexStringByBytes(int(len(content) / 2)) + content
            paramNums = paramNums + 1
        if "00000014" in queryParams:
            content = self.str2Hex("CDMA")
            data = data + "00000014" + self.int2hexStringByBytes(int(len(content) / 2)) + content
            paramNums = paramNums + 1
        if "00000015" in queryParams:
            content = self.str2Hex("yuanhong2")
            data = data + "00000015" + self.int2hexStringByBytes(int(len(content) / 2)) + content
            paramNums = paramNums + 1
        if "00000016" in queryParams:
            content = self.str2Hex("1234567")
            data = data + "00000016" + self.int2hexStringByBytes(int(len(content) / 2)) + content
            paramNums = paramNums + 1
        if "00000017" in queryParams:
            content = self.str2Hex("10.100.12.31")
            data = data + "00000017" + self.int2hexStringByBytes(int(len(content) / 2)) + content
            paramNums = paramNums + 1
        if "00000018" in queryParams:
            content = self.int2hexStringByBytes(9001,4)
            data = data + "00000018" + self.int2hexStringByBytes(int(len(content) / 2)) + content
            paramNums = paramNums + 1
        if "00000019" in queryParams:
            content = self.int2hexStringByBytes(9002,4)
            data = data + "00000019" + self.int2hexStringByBytes(int(len(content) / 2)) + content
            paramNums = paramNums + 1
        paramNums = self.int2hexStringByBytes(paramNums)
        data = paramNums + data
        return data



if __name__ == "__main__":
    obj = QueryTheTerminalParam_res()
    obj.setMsgRes("7e8106002901220150001000060a00000010000000110000001200000013000000180000001400000015000000160000001700000019c17e")
    body = obj.getMsgResBody()
    print(obj.getQueryParams())
    print(obj.getQueryWaterCode())
    print(obj.generateMsg())