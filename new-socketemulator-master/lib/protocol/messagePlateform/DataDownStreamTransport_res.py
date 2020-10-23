#encoding:utf-8

'''
定义平台通用应答消息解码类
'''
from lib.protocol.message.MessageBase import MessageBase
from lib.protocol.messagePlateform.ResponseBase import ResponseBase


class DataDownStreamTransport_res(ResponseBase):
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
        #透传消息类型
        #0xF1	驾驶行程数据（熄火发送）
        # 0xF2	故障码数据（状态改变发送）
        # 0xF3	休眠进入(进入休眠模式发送)
        # 0xF4	休眠唤醒（退出休眠模式发送）
        msgType = body[:2]                                      #消息类型
        msgContent = body[2:]                                   #消息内容
        if msgType == "F1":
            msgContent = self.getDrivingJsonData(msgContent)              #驾驶行程数据（熄火发送）
        elif msgType == "F2":
            msgContent = self.getTroubleCodeJsonData(msgContent)          #故障码数据（状态改变发送）
        elif msgType == "F3":
            msgContent = self.getIntoSleepJsonData(msgContent)            #休眠进入(进入休眠模式发送)
        elif msgType == "F4":
            msgContent = self.getOutSleepJsonData(msgContent)             #休眠唤醒（退出休眠模式发送）
        json_body["msgType"] = msgType
        json_body["msgContent"] = msgContent
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

    #######################################################
    # 驾驶行程数据（熄火发送）
    #######################################################
    def getDrivingJsonData(self,msgContent):
        json_content = []
        #time_1
        item_0 = {}
        item_0["msgId"] = msgContent[:4]
        item_0["length"] = self.hexString2int(msgContent[4:6])
        item_0["time_1"] = self.getBCD2GMTTime(msgContent[6:18])
        json_content.append(item_0)
        msgContent = msgContent[18:]
        # time_2
        item_1 = {}
        item_1["msgId"] = msgContent[:4]
        item_1["length"] = self.hexString2int(msgContent[4:6])
        item_1["time_2"] = self.getBCD2GMTTime(msgContent[6:18])
        json_content.append(item_1)
        msgContent = msgContent[18:]
        #获取点火纬度，单位：0.000001 度，Bit31=0/1	北纬/南纬  ; :北纬  1：南纬  （2147483648）
        item_2 = {}
        item_2["msgId"] = msgContent[:4]
        item_2["length"] = self.hexString2int(msgContent[4:6])
        item_2["fireLatitude"] = - self.hexString2int(msgContent[6:14])
        json_content.append(item_2)
        msgContent = msgContent[14:]
        #点火经度，单位：0.000001 度，Bit31=0/1	东经/西经 ; 0:东经  1：西经  （2147483648）
        item_3 = {}
        item_3["msgId"] = msgContent[:4]
        item_3["length"] = self.hexString2int(msgContent[4:6])
        item_3["fireLongitude"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_3)
        msgContent = msgContent[14:]
        #获取熄火纬度，单位：0.000001 度，Bit31=0/1	北纬/南纬 ; 0:北纬  1：南纬  （2147483648）
        item_4 = {}
        item_4["msgId"] = msgContent[:4]
        item_4["length"] = self.hexString2int(msgContent[4:6])
        item_4["unFireLatitude"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_4)
        msgContent = msgContent[14:]
        #熄火经度，单位：0.000001 度，Bit31=0/1	东经/西经 ; 0:东经  1：西经  （2147483648）
        item_5 = {}
        item_5["msgId"] = msgContent[:4]
        item_5["length"] = self.hexString2int(msgContent[4:6])
        item_5["unFireLongitude"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_5)
        msgContent = msgContent[14:]
        #驾驶循环标签
        item_6 = {}
        item_6["msgId"] = msgContent[:4]
        item_6["length"] = self.hexString2int(msgContent[4:6])
        item_6["drivingCircleLabel"] = self.hexString2int(msgContent[6:10])
        json_content.append(item_6)
        msgContent = msgContent[10:]
        #一个驾驶循环总里程类型
        item_7 = {}
        item_7["msgId"] = msgContent[:4]
        item_7["length"] = self.hexString2int(msgContent[4:6])
        item_7["drivingCircleTotalMileageType"] = msgContent[6:8]
        json_content.append(item_7)
        msgContent = msgContent[8:]
        #一个驾驶循环总里程，单位米
        item_8 = {}
        item_8["msgId"] = msgContent[:4]
        item_8["length"] = self.hexString2int(msgContent[4:6])
        item_8["drivingCircleTotalMileage"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_8)
        msgContent = msgContent[14:]
        #一个驾驶循环总耗油，单位毫升(ml)
        item_9 = {}
        item_9["msgId"] = msgContent[:4]
        item_9["length"] = self.hexString2int(msgContent[4:6])
        item_9["drivingCircleTotalOil"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_9)
        msgContent = msgContent[14:]
        #一个驾驶循环总时长，单位秒
        item_10 = {}
        item_10["msgId"] = msgContent[:4]
        item_10["length"] = self.hexString2int(msgContent[4:6])
        item_10["drivingCircleTotalTime"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_10)
        msgContent = msgContent[14:]
        #一个驾驶循环超速累计时长，单位秒
        item_11 = {}
        item_11["msgId"] = msgContent[:4]
        item_11["length"] = self.hexString2int(msgContent[4:6])
        item_11["drivingCircleOverSpeedTotalTime"] = self.hexString2int(msgContent[6:10])
        json_content.append(item_11)
        msgContent = msgContent[10:]
        #一个驾驶循环超速次数，单位次
        item_12 = {}
        item_12["msgId"] = msgContent[:4]
        item_12["length"] = self.hexString2int(msgContent[4:6])
        item_12["drivingCircleOverSpeedTotalTimes"] = self.hexString2int(msgContent[6:10])
        json_content.append(item_12)
        msgContent = msgContent[10:]
        #一个驾驶循环平均车速，单位 KM/H
        item_13 = {}
        item_13["msgId"] = msgContent[:4]
        item_13["length"] = self.hexString2int(msgContent[4:6])
        item_13["drivingCircleAverageSpeed"] = self.hexString2int(msgContent[6:8])
        json_content.append(item_13)
        msgContent = msgContent[8:]
        # 一个驾驶循环最大车速，单位 KM/H
        item_14 = {}
        item_14["msgId"] = msgContent[:4]
        item_14["length"] = self.hexString2int(msgContent[4:6])
        item_14["drivingCircleMaxSpeed"] = self.hexString2int(msgContent[6:8])
        json_content.append(item_14)
        msgContent = msgContent[8:]
        # 一个驾驶循环怠速时长，单位秒
        item_15 = {}
        item_15["msgId"] = msgContent[:4]
        item_15["length"] = self.hexString2int(msgContent[4:6])
        item_15["drivingCircleIdlingTime"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_15)
        msgContent = msgContent[14:]
        # 一个驾驶循环脚刹次数支持与否，1 为支持
        item_16 = {}
        item_16["msgId"] = msgContent[:4]
        item_16["length"] = self.hexString2int(msgContent[4:6])
        item_16["drivingCircleFootBrakeIsSupport"] = self.hexString2int(msgContent[6:8])
        json_content.append(item_16)
        msgContent = msgContent[8:]
        # 一个驾驶循环脚刹总次数，单位次
        item_17 = {}
        item_17["msgId"] = msgContent[:4]
        item_17["length"] = self.hexString2int(msgContent[4:6])
        item_17["drivingCircleFootBrakeTatalTimes"] = self.hexString2int(msgContent[6:10])
        json_content.append(item_17)
        msgContent = msgContent[10:]
        # 一个驾驶循环急加速次数
        item_18 = {}
        item_18["msgId"] = msgContent[:4]
        item_18["length"] = self.hexString2int(msgContent[4:6])
        item_18["drivingCircleRapidlyAccelerateTimes"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_18)
        msgContent = msgContent[14:]
        # 一个驾驶循环急减速次数
        item_19 = {}
        item_19["msgId"] = msgContent[:4]
        item_19["length"] = self.hexString2int(msgContent[4:6])
        item_19["drivingCircleSharpSlowdownTimes"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_19)
        msgContent = msgContent[14:]
        # 一个驾驶循环急转弯次数
        item_20 = {}
        item_20["msgId"] = msgContent[:4]
        item_20["length"] = self.hexString2int(msgContent[4:6])
        item_20["drivingCircleSharpCurveTimes"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_20)
        msgContent = msgContent[14:]
        # 速度为-20Km/H 的里程,单位:m
        item_21 = {}
        item_21["msgId"] = msgContent[:4]
        item_21["length"] = self.hexString2int(msgContent[4:6])
        item_21["speedIn20"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_21)
        msgContent = msgContent[14:]
        # 速度为 20-40Km/H 的里程,单位:m
        item_22 = {}
        item_22["msgId"] = msgContent[:4]
        item_22["length"] = self.hexString2int(msgContent[4:6])
        item_22["speedIn20_40"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_22)
        msgContent = msgContent[14:]
        # 速度为 40-60Km/H 的里程,单位:m
        item_23 = {}
        item_23["msgId"] = msgContent[:4]
        item_23["length"] = self.hexString2int(msgContent[4:6])
        item_23["speedIn40_60"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_23)
        msgContent = msgContent[14:]
        # 速度为 60-80Km/H 的里程,单位:m
        item_24 = {}
        item_24["msgId"] = msgContent[:4]
        item_24["length"] = self.hexString2int(msgContent[4:6])
        item_24["speedIn60_80"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_24)
        msgContent = msgContent[14:]
        # 速度为 80-100Km/H 的里程,单位:m
        item_25 = {}
        item_25["msgId"] = msgContent[:4]
        item_25["length"] = self.hexString2int(msgContent[4:6])
        item_25["speedIn80_100"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_25)
        msgContent = msgContent[14:]
        # 速度为 100-120Km/H 的里程,单位:m
        item_26 = {}
        item_26["msgId"] = msgContent[:4]
        item_26["length"] = self.hexString2int(msgContent[4:6])
        item_26["speedIn100_120"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_26)
        msgContent = msgContent[14:]
        # 速度为 120Km/H 以上的里程,单位:m
        item_27 = {}
        item_27["msgId"] = msgContent[:4]
        item_27["length"] = self.hexString2int(msgContent[4:6])
        item_27["speedOut120"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_27)
        msgContent = msgContent[14:]
        # 急加速总次数
        item_28 = {}
        item_28["msgId"] = msgContent[:4]
        item_28["length"] = self.hexString2int(msgContent[4:6])
        item_28["rapidlyAccelerateTimes"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_28)
        msgContent = msgContent[14:]
        # 急减速总次数
        item_29 = {}
        item_29["msgId"] = msgContent[:4]
        item_29["length"] = self.hexString2int(msgContent[4:6])
        item_29["rapidlySharpSlowdownTimes"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_29)
        msgContent = msgContent[14:]
        # 急转弯总次数
        item_30 = {}
        item_30["msgId"] = msgContent[:4]
        item_30["length"] = self.hexString2int(msgContent[4:6])
        item_30["sharpCurveTimes"] = self.hexString2int(msgContent[6:14])
        json_content.append(item_30)
        msgContent = msgContent[14:]
        if msgContent != "":
            raise RuntimeError('还有数据未解析！')
        return json_content

    #######################################################
    # 获取故障码数据
    #######################################################
    def getTroubleCodeJsonData(self,msgContent):
        json_content = {}
        # time
        json_content["infoTime"] = self.getBCD2GMTTime(msgContent[:12])
        msgContent = msgContent[12:]
        # 单位：0.000001 度，Bit31=0/1	北纬/南纬
        json_content["latitude"] = self.hexString2int(msgContent[:8])
        msgContent = msgContent[8:]
        # 单位：0.000001 度，Bit31=0/1	东经/西经
        json_content["longitude"] = self.hexString2int(msgContent[:8])
        msgContent = msgContent[8:]
        # 为 0 表示无故障码，非 0 为故障码个数
        json_content["troubleCodeNums"] = self.hexString2int(msgContent[:2])
        msgContent = msgContent[2:]
        troubleCodeCounts = json_content["troubleCodeNums"]
        troubleCode = []
        for i in range(0,troubleCodeCounts):
            item = {}
            item["systemId"] = self.hexString2int(msgContent[:2])
            item["code1"] = self.hexString2int(msgContent[2:4])
            item["code2"] = self.hexString2int(msgContent[4:6])
            item["code3"] = self.hexString2int(msgContent[6:8])
            troubleCode.append(item)
            msgContent = msgContent[8:]
            json_content["troubleCode"] = troubleCode
        return json_content

    #######################################################
    # 获取进入休眠数据包
    #######################################################
    def getIntoSleepJsonData(self,msgContent):
        json_content = {}
        # time
        json_content["infoTime"] = self.getBCD2GMTTime(msgContent[:12])
        return json_content

    #######################################################
    # 获取休眠唤醒数据包
    #######################################################
    def getOutSleepJsonData(self,msgContent):
        json_content = {}
        # time
        json_content["infoTime"] = self.getBCD2GMTTime(msgContent[:12])
        msgContent = msgContent[12:]
        # 休眠唤醒类型
        # 0x01：休眠定时唤醒
        # 0x02：CAN1
        # 0x04：CAN2
        # 0x08：gSensor 0x10：电压变
        json_content["outSleepType"] = msgContent[:2]
        msgContent = msgContent[2:]
        # 车辆电压，单位 0.1V
        json_content["carVoltage"] = self.hexString2int(msgContent[:4])
        msgContent = msgContent[4:]
        # 振动唤醒加速度值，单位 mg
        json_content["vibrateOutSleepSpeedUpVal"] = self.hexString2int(msgContent[:4])
        return json_content













if __name__ == "__main__":
    # print(DataDownStreamTransport_res("7e090000ca0131462011190001F100010620020522073000020620020715175600030401c0a6380004040659ad7a00050401c0a6380006040659ad7a000702007b00080101000904000094ca000A0400012688000B04000b13f0000C02d2f0000D020065000E0141000F017b00100400c042c00011010100120100200013040000004f0014040000000a001504000000210016040000042c001704000007d024001804000076c000190400009088001A04000028a0001B0400001388001C0400000c80001D0400000bb8001E0400000db3001F0400000244817e").getMsg())
    # print(DataDownStreamTransport_res("7e0900001c0131462011190001F220020611315601c0a6380659ad7a03010a141e010a141e010a141e3f7e").getMsg())
    # print(DataDownStreamTransport_res("7e090000070131462011190001F3200206113156f07e").getMsg())
    print(DataDownStreamTransport_res("7e0900000c0131462011190001F42002061131560101680e74ee7e").getMsg())













