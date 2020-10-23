#encoding:utf-8

'''
定义下行通用应答消息解码类
'''
import json

from lib.protocol.m300.M300Base import M300Base
from lib.protocol.m300Plateform.ResponseBase import ResponseBase

class M300Common_res(ResponseBase):
    def __init__(self,msg):
        super().__init__()
        if type(msg) == bytes:
            self.msg = self.binary2ascii(msg)
        else:
            self.msg = msg
        self.msg = self.restore_7e7d(self.msg)


    #######################################################
    # 获取消息
    #######################################################
    def getMsg(self):
        json_msg = {}
        json_msg["FUNID"] = self.msg[2:6]
        json_msg["waterCode"] = self.hexString2int(self.msg[6:10])
        json_msg["DEV_ID"] = self.msg[10:24]
        json_msg["property"] = self.getMsgProperty()
        json_msg["body"] = self.getMsgBody()
        json_msg["checkCode"] = self.msg[len(self.msg) - 4:len(self.msg) - 2]
        json_msg["calculateCheckCode"] = self.getCalculateCheckCode()      #自己计算消息后得到的校验码
        json_msg = json.dumps(json_msg)
        return json_msg

    #######################################################
    # 获取消息属性
    ######################################################
    def getMsgProperty(self):
        property = {}
        data = self.msg[24:28]
        data = self.hexString2int(data)
        data = self.int2binStr(data)
        encryptionType = data[2:6]
        length = data[6:]
        property["encryptionType"] = int(encryptionType,2)
        property["length"] = int(length, 2)
        return property

    #######################################################
    # 获取消息体
    ######################################################
    def getMsgBody(self):
        body = {}
        data = self.msg[28:len(self.msg) - 4]
        body["funId"] = data
        return body


    #######################################################
    # 计算消息得到校验码
    #######################################################
    def getCalculateCheckCode(self):
        data = self.removeIdentify(self.msg)
        dataLen = len(data)
        data = data[:dataLen - 2]
        calculateCheckCode = M300Base().getCheckCode(data)
        return calculateCheckCode

if __name__ == "__main__":
    print(M300Common_res("7e800100034d12150101000100020003c87e").getMsg())
