#encoding:utf-8

'''
定义终端登录应答消息解码类
'''
import json

from lib.protocol.reportPlateform.ResponseBase import ResponseBase


class Login_res(ResponseBase):
    def __init__(self, msg):
        super().__init__()
        if type(msg) == bytes:
            self.msg = self.binary2ascii(msg)
        else:
            self.msg = msg
        pass

    #######################################################
    # 获取解析后的消息
    #######################################################
    def getMsg(self):
        json_msg = {}
        json_msg["header"] = self.msg[0:4]
        json_msg["msgLen"] = self.getMsgLen()
        json_msg["waterCode"] = self.hexString2int(self.msg[8:12])
        json_msg["devId"] = self.hex2string(self.msg[12:14]) + self.msg[14:26]
        json_msg["funcId"] = self.msg[26:30]
        json_msg["body"] = self.getMsgBody()
        json_msg["checkCode"] = self.msg[-4:]
        json_msg["calculateCheckCode"] = self.getCalculateCheckCode()  # 自己计算消息后得到的校验码
        json_msg = json.dumps(json_msg)
        return json_msg

    #######################################################
    # 获取消息长度
    #######################################################
    def getMsgLen(self):
        msgLenHex = self.msg[4:8]
        msgLen = self.hexString2int(msgLenHex)
        return msgLen

    #######################################################
    # 获取消息体
    #######################################################
    def getMsgBody(self):
        data = {}
        msgbody = self.msg[30:][:-4]
        data["data"] = msgbody
        return data

    #######################################################
    # 获取自己计算得到的校验码
    #######################################################
    def getCalculateCheckCode(self):
        checkCode = self.crc16(self.msg[:-4])
        return checkCode


if __name__ == "__main__":
    print(Login_res("4040000e00024d1215010100018000000300482a").getMsg())

