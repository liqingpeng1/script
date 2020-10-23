#encoding:utf-8

'''
定义平台版本信息包上传应答解码类
'''
import json

from lib.protocol.message.MessageBase import MessageBase
from lib.protocol.messagePlateform.ResponseBase import ResponseBase


class PlatefromVersionInfo_res(ResponseBase):
    def __init__(self,msg):
        super().__init__()
        if type(msg) == bytes:
            self.msg = self.binary2ascii(msg)
        else:
            self.msg = msg
        pass

    #######################################################
    # 获取消息
    #######################################################
    def getMsg(self):
        json_msg = {}
        json_msg["header"] = self.getMsgHeader()
        json_msg["body"] = self.getMsgBody()
        json_msg["checkCode"] = self.getCheckCode()
        json_msg["calculateCheckCode"] = self.getCalculateCheckCode()      #自己计算消息后得到的校验码
        json_msg = json.dumps(json_msg)
        return json_msg

    #######################################################
    # 获取消息头
    #######################################################
    def getMsgHeader(self):
        json_header = {}
        data = self.removeIdentify(self.msg)
        data = self.restore_7e7d(data)
        header = data[:24]
        msgId = header[:4]                                 #消息id
        msgBodyProperty = header[4:8]                      #消息体属性
        phoneNum = header[8:20]                            #终端手机号
        msgWaterCode = header[20:24]                       #消息流水号

        json_header["msgId"] = msgId
        json_header["msgBodyProperty"] = self.getMsgBodyProperty(msgBodyProperty)
        json_header["phoneNum"] = phoneNum[1:]
        json_header["msgWaterCode"] = int(msgWaterCode,16)
        return json_header

    #获取消息体属性
    def getMsgBodyProperty(self,data):
        data = self.int2binStr(int(data,16),2)
        data = self.restore_7e7d(data)
        json_data = {}
        subPkg = data[2:3]                                 #分包
        encryptionType = data[3:6]                         #加密方式
        msgBodyLen = data[6:]                              #消息体长度
        json_data["subPkg"] = int(subPkg,2)
        json_data["encryptionType"] = int(encryptionType,2)
        json_data["msgBodyLen"] = int(msgBodyLen,2)
        return json_data


    #######################################################
    # 获取消息体
    #######################################################
    def getMsgBody(self):
        json_body = {}
        data = self.removeIdentify(self.msg)
        data = self.restore_7e7d(data)
        dataLen = len(data)
        body = data[24:dataLen - 2]
        plateformCurrentTime = self.getBCD2GMTTime(body[:12])       #平台当前时间
        carId = self.hexString2int(body[12:16])                     #车型id
        displacement = self.hexString2int(body[16:20])              #排量
        isUpdate = body[20:22]                                      #是否升级，0x55 升级，其他不升级
        oilDensity = self.hexString2int(body[22:26])                #油密度
        OBDCtrType = self.hexString2int(body[26:]) >> 7
        json_body["plateformCurrentTime"] = plateformCurrentTime
        json_body["carId"] = carId
        json_body["displacement"] = displacement
        json_body["isUpdate"] = isUpdate
        json_body["oilDensity"] = oilDensity
        json_body["OBDCtrType"] = OBDCtrType
        return json_body

    #######################################################
    # 获取校验码
    #######################################################
    def getCheckCode(self):
        data = self.removeIdentify(self.msg)
        data = self.restore_7e7d(data)
        dataLen = len(data)
        checkCode = data[dataLen - 2:]
        return checkCode

    #######################################################
    # 计算消息得到校验码
    #######################################################
    def getCalculateCheckCode(self):
        data = self.removeIdentify(self.msg)
        data = self.restore_7e7d(data)
        dataLen = len(data)
        data = data[:dataLen - 2]
        calculateCheckCode = MessageBase().getCheckCode(data)
        return calculateCheckCode


    #######################################################
    # 获取最原始的消息数据（没有替换7e，7d之前的状态）
    #######################################################
    def getOriginalMsg(self):
        data = self.removeIdentify(self.msg)
        data = self.restore_7e7d(data)
        data = "7e" + data + "7e"
        return data






